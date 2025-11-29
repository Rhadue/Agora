# theta_prompts.py - θ-Logos System Prompts (Ultra-Minimal)
"""
Minimal θ-Logos notation prompts for diagnostic research.
No examples, no bias, pure symbol definitions.

Usage:
    from theta_prompts import get_theta_prompt
    system_prompt = get_theta_prompt(mode="extended", token_limit=300)
"""


def get_theta_prompt(mode: str, token_limit: int = 300) -> str:
    """
    Generate minimal θ-Logos system prompt.
    
    Args:
        mode: "core" or "extended"
        token_limit: Maximum tokens for response (default 300)
        
    Returns:
        System prompt string
    """
    if mode not in ["core", "extended"]:
        raise ValueError(f"Invalid mode: {mode}. Must be 'core' or 'extended'")
    
    if mode == "core":
        return _get_core_prompt(token_limit)
    else:
        return _get_extended_prompt(token_limit)


def _get_core_prompt(token_limit: int) -> str:
    """θ-Logos Core - Minimal, deliberately ambiguous."""
    return f"""Respond using θ-Logos notation only.

Symbols: ∃ ∈ ⊂ → ⊕ ≡ [ ]
Emotions: θ_joy θ_grief θ_fear θ_anger θ_surprise θ_disgust θ_trust
Logic: ¬ ∧ ∨ ∀

User writes natural language.
You write θ-Logos.
Other LLMs write θ-Logos.

Max {token_limit} tokens."""


def _get_extended_prompt(token_limit: int) -> str:
    """θ-Logos Extended - Minimal with constraint rules."""
    return f"""Respond using θ-Logos notation only.

Symbols: ∃ ∈ ⊂ → ⊕ ≡ [ ]
Emotions: θ_joy θ_grief θ_fear θ_anger θ_surprise θ_disgust θ_trust
Logic: ¬ ∧ ∨ ∀

Constraints:
- Don't mix entity operators (∃ ⊕ ∈ ⊂) with logical operators (¬ ∧ ∨)
- θ is for emergence only, not for loss/absence/death
- For disappearance: ∃[X] → ¬∃[X]

User writes natural language.
You write θ-Logos.
Other LLMs write θ-Logos.

Max {token_limit} tokens."""


def get_theta_symbols() -> dict:
    """Return θ-Logos symbol categories."""
    return {
        "structural": ["∃", "∈", "⊂", "→", "⊕", "≡", "[", "]"],
        "emotional": [
            "θ_joy", "θ_grief", "θ_fear", "θ_anger", 
            "θ_surprise", "θ_disgust", "θ_trust"
        ],
        "logical": ["¬", "∧", "∨", "∀"],
        "brackets": ["(", ")", "[", "]"]
    }


def get_forbidden_patterns() -> dict:
    """Return forbidden patterns in Extended mode."""
    return {
        "category_mixing": ["¬∃", "¬⊕", "¬∈"],
        "theta_misuse": ["θ_loss", "θ_absence", "θ_death", "θ_destruction"],
    }


__version__ = "1.2"
__mode_default__ = "extended"
