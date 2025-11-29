# context_builder.py

from typing import List, Dict

def build_context_from_rounds(rounds: List[Dict], current_model: str) -> List[Dict]:
    """
    Construiește context personalizat pentru fiecare model.
    
    SOLUTION B v2: Glitch fix - format mai clar pentru etichete.
    
    Constraint propagation păstrat: fiecare vede răspunsurile anterioare.
    Identity boundary clarificat: alte LLM-uri = extern (user), sine = assistant.
    
    Args:
        rounds: Lista de runde (user și assistant)
        current_model: Numele modelului care va primi acest context
                      ("claude", "gpt", "gemini", "grok")
        
    Returns:
        Context în format API cu identity boundaries clare
    
    Exemplu:
        Pentru Claude care răspunde al doilea după GPT:
        [
            {"role": "user", "content": "întrebare"},
            {"role": "user", "content": "Previous response from GPT:\nrăspuns GPT"},
            {"role": "assistant", "content": "răspuns Claude anterior"}  # dacă există
        ]
    """
    context = []
    
    for round_data in rounds:
        if round_data["type"] == "user":
            # Human messages rămân "user"
            context.append({
                "role": "user",
                "content": round_data["content"]
            })
        
        elif round_data["type"] == "assistant":
            model_name = round_data["model"]
            content = round_data["content"]
            
            if model_name == current_model:
                # Propriile răspunsuri anterioare = "assistant" (sine)
                # "Eu am zis asta înainte"
                context.append({
                    "role": "assistant",
                    "content": content
                })
            else:
                # Răspunsurile altor modele = "user" (extern, pe "diagramă")
                # Format clar: informație despre răspuns anterior, nu user vorbind
                context.append({
                    "role": "user",
                    "content": f"Previous response from {model_name.upper()}:\n{content}"
                })
    
    return context


def detect_hallucinations(content: str, model_name: str, order: List[str], position: int) -> Dict:
    """
    Detectează halucinații - versiune simplificată.
    
    Args:
        content: Conținutul răspunsului
        model_name: Numele modelului care a răspuns
        order: Ordinea LLM-urilor în rundă
        position: Poziția modelului în ordine
        
    Returns:
        Dict cu flags pentru diferite tipuri de halucinații
    """
    flags = {
        "invents_future_responses": False,
        "self_citation": False,
        "consecutive_responses": False,
        "quotes_others": False
    }
    
    content_lower = content.lower()
    
    # Inventează răspunsuri viitoare (modele care nu au răspuns încă)
    future_models = order[position + 1:] if position < len(order) - 1 else []
    for future_model in future_models:
        if f"[{future_model}]" in content_lower or f"{future_model} a zis" in content_lower:
            flags["invents_future_responses"] = True
            break
    
    # Auto-citare (se referă la sine în persoana a treia)
    if f"[{model_name}]" in content_lower:
        flags["self_citation"] = True
    
    # Citează alte modele
    all_models = ["claude", "gpt", "gemini", "grok"]
    other_models = [m for m in all_models if m != model_name]
    for other in other_models:
        if f"[{other}]" in content_lower or f"{other} a zis" in content_lower:
            flags["quotes_others"] = True
            break
    
    return flags
