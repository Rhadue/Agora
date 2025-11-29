# validator.py - API Key Validation

from typing import List
import config

def validate_api_keys() -> List[str]:
    """
    Verifică care API keys sunt valide și returnează lista modelelor active.
    Rulează LA PORNIRE.
    
    Returns:
        Listă cu numele modelelor care au API keys valide
    """
    active_models = []
    
    # Claude
    if config.CLAUDE_API_KEY and len(config.CLAUDE_API_KEY) > 10:
        active_models.append("claude")
    
    # GPT
    if config.OPENAI_API_KEY and len(config.OPENAI_API_KEY) > 10:
        active_models.append("gpt")
    
    # Gemini
    if config.GEMINI_API_KEY and len(config.GEMINI_API_KEY) > 10:
        active_models.append("gemini")
    
    # Grok
    if config.GROK_API_KEY and len(config.GROK_API_KEY) > 10:
        active_models.append("grok")
    
    return active_models

def print_active_models(active_models: List[str]):
    """Afișează modelele active la pornire."""
    if not active_models:
        print("❌ EROARE: Niciun API key valid găsit!")
        print("Te rog adaugă cel puțin un API key în config.py")
        return
    
    print(f"\n✅ Modele active ({len(active_models)}):")
    for model in active_models:
        print(f"   - {model}")
    print()