# llm_clients.py - LLM API Calls with θ-Logos Integration

from anthropic import Anthropic
from openai import OpenAI
import google.generativeai as genai
import httpx
from typing import Tuple, List, Dict
import config
from theta_prompts import get_theta_prompt

# === INITIALIZE CLIENTS ===
_claude_client = None
_openai_client = None
_gemini_model = None

if config.CLAUDE_API_KEY:
    _claude_client = Anthropic(api_key=config.CLAUDE_API_KEY)

if config.OPENAI_API_KEY:
    _openai_client = OpenAI(api_key=config.OPENAI_API_KEY)

if config.GEMINI_API_KEY:
    genai.configure(api_key=config.GEMINI_API_KEY)
    _gemini_model = genai.GenerativeModel(config.MODELS["gemini"]["api_model_name"])


def _inject_theta_prompt(messages: List[Dict], max_tokens: int) -> List[Dict]:
    """
    Inject θ-Logos system prompt if enabled.
    
    Args:
        messages: Original conversation messages
        max_tokens: Token limit for this round
        
    Returns:
        Messages with θ-Logos system prompt prepended (if enabled)
    """
    if not config.THETA_ENABLED:
        return messages
    
    theta_system_prompt = get_theta_prompt(
        mode=config.THETA_MODE,
        token_limit=max_tokens
    )
    
    # Prepend system message
    return [{"role": "system", "content": theta_system_prompt}] + messages


def _convert_to_gemini_format(messages: List[Dict]) -> str:
    """Convert messages to Gemini format."""
    parts = []
    for m in messages:
        role = "user" if m["role"] == "user" else "model"
        parts.append(f"{role}: {m['content']}")
    return "\n".join(parts)


def call_claude(messages: List[Dict], max_tokens: int) -> Tuple[str, int, bool, str]:
    """Call Claude API with optional θ-Logos system prompt."""
    if not _claude_client:
        return "[API key lipsă]", 0, False, "No API key"
    
    model_config = config.MODELS["claude"]
    
    # Extract system prompt if present (Claude uses separate system parameter)
    system_prompt = None
    messages_filtered = messages
    
    if config.THETA_ENABLED:
        system_prompt = get_theta_prompt(mode=config.THETA_MODE, token_limit=max_tokens)
    
    # RETRY LOGIC: 2 attempts if content empty
    for attempt in range(2):
        try:
            # Claude API uses system parameter, not system role in messages
            if system_prompt:
                resp = _claude_client.messages.create(
                    model=model_config["api_model_name"],
                    max_tokens=max_tokens,
                    temperature=model_config["temperature"],
                    system=system_prompt,
                    messages=messages_filtered,
                    timeout=model_config["timeout"]
                )
            else:
                resp = _claude_client.messages.create(
                    model=model_config["api_model_name"],
                    max_tokens=max_tokens,
                    temperature=model_config["temperature"],
                    messages=messages_filtered,
                    timeout=model_config["timeout"]
                )
            
            # DEFENSIVE CHECKS
            if not resp:
                if attempt == 0:
                    print(f"[Claude] Null response, retry {attempt + 1}/2")
                    continue
                return "[răspuns null de la API]", 0, False, "Null response after retry"
            
            if not hasattr(resp, 'content') or not resp.content:
                if attempt == 0:
                    print(f"[Claude] Empty content attribute, retry {attempt + 1}/2")
                    continue
                return "[răspuns fără content]", 0, False, "Empty content after retry"
            
            if len(resp.content) == 0:
                if attempt == 0:
                    print(f"[Claude] Empty content array, retry {attempt + 1}/2")
                    continue
                return "[content array gol]", 0, False, "Empty content array after retry"
            
            if not hasattr(resp.content[0], 'text'):
                if attempt == 0:
                    print(f"[Claude] No text in content block, retry {attempt + 1}/2")
                    continue
                return "[content block fără text]", 0, False, "No text after retry"
            
            text = resp.content[0].text.strip()
            
            if not text:
                if attempt == 0:
                    print(f"[Claude] Empty text after strip, retry {attempt + 1}/2")
                    continue
                return "[text gol]", 0, False, "Empty text after retry"
            
            # SUCCESS
            tokens = 0
            if hasattr(resp, 'usage') and resp.usage:
                tokens = resp.usage.output_tokens if hasattr(resp.usage, 'output_tokens') else 0
            
            if attempt > 0:
                print(f"[Claude] SUCCESS on retry {attempt + 1}")
            
            return text, tokens, False, None
            
        except Exception as e:
            error_msg = str(e)
            timeout = "timeout" in error_msg.lower()
            return "[modelul a avut o eroare tehnică și nu a putut răspunde în această rundă]", 0, timeout, error_msg
    
    return "[eroare după retry]", 0, False, "Exhausted retries"


def call_gpt(messages: List[Dict], max_tokens: int) -> Tuple[str, int, bool, str]:
    """Call GPT API with optional θ-Logos system prompt."""
    if not _openai_client:
        return "[API key lipsă]", 0, False, "No API key"
    
    # Inject θ-Logos prompt if enabled
    messages = _inject_theta_prompt(messages, max_tokens)
    
    model_config = config.MODELS["gpt"]
    
    # RETRY LOGIC
    for attempt in range(2):
        try:
            resp = _openai_client.chat.completions.create(
                model=model_config["api_model_name"],
                messages=messages,
                max_completion_tokens=max_tokens,
                temperature=model_config["temperature"],
                timeout=model_config["timeout"]
            )
            
            # DEFENSIVE CHECKS
            if not resp:
                if attempt == 0:
                    print(f"[GPT] Null response, retry {attempt + 1}/2")
                    continue
                return "[răspuns null de la API]", 0, False, "Null response after retry"
            
            if not hasattr(resp, 'choices') or not resp.choices:
                if attempt == 0:
                    print(f"[GPT] No choices, retry {attempt + 1}/2")
                    continue
                return "[răspuns fără choices]", 0, False, "No choices after retry"
            
            if len(resp.choices) == 0:
                if attempt == 0:
                    print(f"[GPT] Empty choices array, retry {attempt + 1}/2")
                    continue
                return "[choices array gol]", 0, False, "Empty choices after retry"
            
            if not hasattr(resp.choices[0], 'message'):
                if attempt == 0:
                    print(f"[GPT] No message, retry {attempt + 1}/2")
                    continue
                return "[choice fără message]", 0, False, "No message after retry"
            
            if not hasattr(resp.choices[0].message, 'content'):
                if attempt == 0:
                    print(f"[GPT] No content, retry {attempt + 1}/2")
                    continue
                return "[message fără content]", 0, False, "No content after retry"
            
            text = resp.choices[0].message.content
            if not text or not text.strip():
                if attempt == 0:
                    print(f"[GPT] Empty text, retry {attempt + 1}/2")
                    continue
                return "[text gol]", 0, False, "Empty text after retry"
            
            text = text.strip()
            
            # SUCCESS
            tokens = 0
            if hasattr(resp, 'usage') and resp.usage:
                tokens = resp.usage.completion_tokens if hasattr(resp.usage, 'completion_tokens') else 0
            
            if attempt > 0:
                print(f"[GPT] SUCCESS on retry {attempt + 1}")
            
            return text, tokens, False, None
            
        except Exception as e:
            error_msg = str(e)
            timeout = "timeout" in error_msg.lower()
            return "[modelul a avut o eroare tehnică și nu a putut răspunde în această rundă]", 0, timeout, error_msg
    
    return "[eroare după retry]", 0, False, "Exhausted retries"


def call_gemini(messages: List[Dict], max_tokens: int) -> Tuple[str, int, bool, str]:
    """Call Gemini API with optional θ-Logos system prompt."""
    if not _gemini_model:
        return "[API key lipsă]", 0, False, "No API key"
    
    # Inject θ-Logos prompt if enabled
    messages = _inject_theta_prompt(messages, max_tokens)
    
    model_config = config.MODELS["gemini"]
    
    # RETRY LOGIC
    for attempt in range(2):
        try:
            prompt = _convert_to_gemini_format(messages)
            
            resp = _gemini_model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": max_tokens,
                    "temperature": model_config["temperature"],
                }
            )
            
            # DEFENSIVE CHECKS
            if not resp:
                if attempt == 0:
                    print(f"[Gemini] Null response, retry {attempt + 1}/2")
                    continue
                return "[răspuns null de la API]", 0, False, "Null response after retry"
            
            if not hasattr(resp, 'candidates') or not resp.candidates:
                if attempt == 0:
                    print(f"[Gemini] No candidates, retry {attempt + 1}/2")
                    continue
                return "[blocat de safety]", 0, False, "No candidates after retry"
            
            candidate = resp.candidates[0]
            
            if not hasattr(candidate, 'content'):
                if attempt == 0:
                    print(f"[Gemini] No content attribute, retry {attempt + 1}/2")
                    continue
                return "[content lipsă]", 0, False, "No content after retry"
            
            if not hasattr(candidate.content, 'parts'):
                if attempt == 0:
                    print(f"[Gemini] No parts attribute, retry {attempt + 1}/2")
                    continue
                return "[parts attribute lipsă]", 0, False, "No parts attribute after retry"
            
            if not candidate.content.parts or len(candidate.content.parts) == 0:
                if attempt == 0:
                    print(f"[Gemini] Empty parts list, retry {attempt + 1}/2")
                    continue
                return "[parts gol]", 0, False, "Empty parts after retry"
            
            first_part = candidate.content.parts[0]
            text = first_part.text if hasattr(first_part, 'text') and first_part.text else None
            
            if not text or not text.strip():
                if attempt == 0:
                    print(f"[Gemini] Empty text, retry {attempt + 1}/2")
                    continue
                return "[text gol]", 0, False, "Empty text after retry"
            
            text = text.strip()
            
            # SUCCESS
            tokens = len(text.split())
            
            if attempt > 0:
                print(f"[Gemini] SUCCESS on retry {attempt + 1}")
            
            return text, tokens, False, None
            
        except Exception as e:
            error_msg = str(e)
            timeout = "timeout" in error_msg.lower() or "deadline" in error_msg.lower()
            return "[modelul a avut o eroare tehnică și nu a putut răspunde în această rundă]", 0, timeout, error_msg
    
    return "[eroare după retry]", 0, False, "Exhausted retries"


def call_grok(messages: List[Dict], max_tokens: int) -> Tuple[str, int, bool, str]:
    """Call Grok API with optional θ-Logos system prompt."""
    if not config.GROK_API_KEY:
        return "[API key lipsă]", 0, False, "No API key"
    
    # Inject θ-Logos prompt if enabled
    messages = _inject_theta_prompt(messages, max_tokens)
    
    model_config = config.MODELS["grok"]
    
    # RETRY LOGIC
    for attempt in range(2):
        try:
            headers = {
                "Authorization": f"Bearer {config.GROK_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": model_config["api_model_name"],
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": model_config["temperature"],
            }
            
            with httpx.Client(timeout=model_config["timeout"]) as client:
                resp = client.post(
                    "https://api.x.ai/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                
                if resp.status_code == 200:
                    data = resp.json()
                    
                    # DEFENSIVE CHECKS
                    if not data.get("choices"):
                        if attempt == 0:
                            print(f"[Grok] No choices, retry {attempt + 1}/2")
                            continue
                        return "[răspuns fără choices]", 0, False, "No choices after retry"
                    
                    if len(data["choices"]) == 0:
                        if attempt == 0:
                            print(f"[Grok] Empty choices array, retry {attempt + 1}/2")
                            continue
                        return "[choices array gol]", 0, False, "Empty choices after retry"
                    
                    if not data["choices"][0].get("message"):
                        if attempt == 0:
                            print(f"[Grok] No message, retry {attempt + 1}/2")
                            continue
                        return "[choice fără message]", 0, False, "No message after retry"
                    
                    if not data["choices"][0]["message"].get("content"):
                        if attempt == 0:
                            print(f"[Grok] No content, retry {attempt + 1}/2")
                            continue
                        return "[message fără content]", 0, False, "No content after retry"
                    
                    text = data["choices"][0]["message"]["content"].strip()
                    
                    if not text:
                        if attempt == 0:
                            print(f"[Grok] Empty text, retry {attempt + 1}/2")
                            continue
                        return "[text gol]", 0, False, "Empty text after retry"
                    
                    # SUCCESS
                    tokens = data.get("usage", {}).get("completion_tokens", 0)
                    
                    if attempt > 0:
                        print(f"[Grok] SUCCESS on retry {attempt + 1}")
                    
                    return text, tokens, False, None
                else:
                    return "[modelul a avut o eroare tehnică și nu a putut răspunde în această rundă]", 0, False, f"HTTP {resp.status_code}"
                    
        except httpx.TimeoutException as e:
            return "[modelul a avut o eroare tehnică și nu a putut răspunde în această rundă]", 0, True, str(e)
        except Exception as e:
            return "[modelul a avut o eroare tehnică și nu a putut răspunde în această rundă]", 0, False, str(e)
    
    return "[eroare după retry]", 0, False, "Exhausted retries"
