# main.py - SOLUTION B with θ-Logos Integration

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from datetime import datetime
from typing import List, Dict
from contextlib import asynccontextmanager

import config
import validator
from dice_roller import DiceRoller
from context_builder import build_context_from_rounds, detect_hallucinations
from llm_clients import call_claude, call_gpt, call_gemini, call_grok
from exporter import export_conversation, generate_diagnostic_report

# Global state
ACTIVE_MODELS: List[str] = []
dice_roller = DiceRoller()
rounds: List[Dict] = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler."""
    global ACTIVE_MODELS
    ACTIVE_MODELS = validator.validate_api_keys()
    validator.print_active_models(ACTIVE_MODELS)
    
    if not ACTIVE_MODELS:
        print("⚠️  Server pornit dar FĂRĂ modele active!")
        print("   Adaugă API keys în config.py și restartează.")
    
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {
        "status": "AGORA MVP 2025 - θ-Logos Integration Ready",
        "active_models": ACTIVE_MODELS,
        "total_rounds": len(rounds),
        "theta_enabled": config.THETA_ENABLED,
        "theta_mode": config.THETA_MODE,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/message")
async def send_message(message: dict):
    """
    Send message to multi-LLM conversation.
    
    Request format:
    {
        "content": "user message",
        "token_limit": 300,  # optional
        "theta_enabled": false  # optional, toggles θ-Logos mode
    }
    """
    global rounds
    
    content = message.get("content", "").strip()
    if not content:
        return {"error": "Mesaj gol"}
    
    if not ACTIVE_MODELS:
        return {"error": "Niciun model activ"}
    
    # Token limit
    token_limit = message.get("token_limit", config.TOKEN_LIMIT_DEFAULT)
    token_limit = max(config.TOKEN_LIMIT_MIN, min(config.TOKEN_LIMIT_MAX, token_limit))
    
    # θ-Logos toggle (from UI request)
    theta_enabled = message.get("theta_enabled", False)
    
    # Temporarily set θ-Logos state for this request
    original_theta_state = config.THETA_ENABLED
    config.THETA_ENABLED = theta_enabled
    
    # Use θ token limit if in θ mode
    if theta_enabled:
        token_limit = config.THETA_TOKEN_LIMIT
    
    # === RUNDĂ USER ===
    user_round = {
        "round_number": len(rounds) + 1,
        "type": "user",
        "content": content,
        "theta_enabled": theta_enabled,
        "timestamp": datetime.now().isoformat()
    }
    rounds.append(user_round)
    
    # === DICE ROLL pentru ordinea LLM-urilor ===
    order = dice_roller.roll(ACTIVE_MODELS)
    
    # === FIECARE LLM = O RUNDĂ SEPARATĂ ===
    llm_responses = []
    
    for position, model_name in enumerate(order):
        # Context PERSONALIZAT pentru fiecare model
        context_sent = build_context_from_rounds(rounds, model_name)
        
        # Apelează modelul
        if model_name == "claude":
            text, tokens, timeout, error = call_claude(context_sent, token_limit)
        elif model_name == "gpt":
            text, tokens, timeout, error = call_gpt(context_sent, token_limit)
        elif model_name == "gemini":
            text, tokens, timeout, error = call_gemini(context_sent, token_limit)
        elif model_name == "grok":
            text, tokens, timeout, error = call_grok(context_sent, token_limit)
        else:
            text, tokens, timeout, error = "[model necunoscut]", 0, False, "Unknown"
        
        # Detectează halucinații
        hallucination_flags = detect_hallucinations(text, model_name, order, position)
        
        # === RUNDĂ LLM ===
        llm_round = {
            "round_number": len(rounds) + 1,
            "type": "assistant",
            "model": model_name,
            "content": text,
            "tokens": tokens,
            "timeout": timeout,
            "error": error,
            "context_sent": context_sent,
            "hallucination_flags": hallucination_flags,
            "theta_enabled": theta_enabled,
            "theta_mode": config.THETA_MODE if theta_enabled else None,
            "timestamp": datetime.now().isoformat()
        }
        rounds.append(llm_round)
        
        # Pentru response UI
        llm_responses.append({
            "model": model_name,
            "content": text,
            "tokens": tokens,
            "timeout": timeout
        })
    
    # Restore original θ state
    config.THETA_ENABLED = original_theta_state
    
    # Return pentru UI
    return {
        "order": order,
        "responses": llm_responses,
        "theta_enabled": theta_enabled
    }

@app.get("/export")
def export():
    """Exportă conversația."""
    if not rounds:
        return {"error": "Nicio conversație"}
    
    # Adaptăm structura pentru export
    export_data = {
        "conversation_id": datetime.now().isoformat(),
        "export_timestamp": datetime.now().isoformat(),
        "total_rounds": len(rounds),
        "solution": "B - Context personalizat per model + θ-Logos",
        "theta_mode": config.THETA_MODE,
        "rounds": rounds
    }
    
    filename = f"agora_theta_{int(datetime.now().timestamp() * 1000)}.json"
    
    import json
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    return FileResponse(filename, media_type="application/json", filename=filename)

@app.get("/diagnostics")
def diagnostics():
    """Raport diagnostic."""
    if not rounds:
        return {"error": "Nicio conversație"}
    
    total_llm_rounds = len([r for r in rounds if r["type"] == "assistant"])
    hallucinations = sum(
        1 for r in rounds 
        if r["type"] == "assistant" and any(r.get("hallucination_flags", {}).values())
    )
    
    # Count θ-Logos rounds
    theta_rounds = len([r for r in rounds if r.get("theta_enabled", False)])
    
    # Statistici per model
    model_stats = {}
    for model in ["claude", "gpt", "gemini", "grok"]:
        model_rounds = [r for r in rounds if r.get("model") == model]
        if model_rounds:
            model_stats[model] = {
                "total_rounds": len(model_rounds),
                "total_tokens": sum(r.get("tokens", 0) for r in model_rounds),
                "errors": len([r for r in model_rounds if r.get("error")]),
                "hallucinations": len([r for r in model_rounds if any(r.get("hallucination_flags", {}).values())]),
                "theta_rounds": len([r for r in model_rounds if r.get("theta_enabled", False)])
            }
    
    return {
        "solution": "B - Context personalizat per model + θ-Logos",
        "total_rounds": len(rounds),
        "user_rounds": len([r for r in rounds if r["type"] == "user"]),
        "llm_rounds": total_llm_rounds,
        "theta_rounds": theta_rounds,
        "hallucinations_detected": hallucinations,
        "model_stats": model_stats
    }

@app.post("/reset")
def reset_conversation():
    """Reset conversație."""
    global rounds
    rounds = []
    return {"status": "Reset", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("AGORA - θ-Logos Integration Ready")
    print("="*60)
    print("\nFeatures:")
    print("  ✓ Multi-LLM conversation (Solution B)")
    print("  ✓ θ-Logos notation support (ultra-minimal)")
    print("  ✓ Toggle θ mode per-request from UI")
    print("  ✓ Dice roller for randomized order")
    print("  ✓ Context propagation")
    print(f"\nθ-Logos Mode: {config.THETA_MODE}")
    print(f"θ-Logos Token Limit: {config.THETA_TOKEN_LIMIT}")
    print("="*60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
