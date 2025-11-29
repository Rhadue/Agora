# dice_roller.py - STABLE MODULE

import random
from typing import List, Optional

class DiceRoller:
    """Generează ordine aleatorie pentru LLM-uri, evitând repetiții consecutive."""
    
    def __init__(self):
        self.last_order: Optional[List[str]] = None
    
    def roll(self, available_models: List[str]) -> List[str]:
        """
        Generează o ordine aleatorie diferită de ultima.
        
        Args:
            available_models: Lista modelelor active
            
        Returns:
            Listă cu modele în ordine aleatorie
        """
        if len(available_models) == 0:
            return []
        
        if len(available_models) == 1:
            return available_models
        
        max_attempts = 100
        for _ in range(max_attempts):
            new_order = random.sample(available_models, len(available_models))
            if new_order != self.last_order:
                self.last_order = new_order
                return new_order
        
        # Fallback: inversează ultima ordine
        fallback = list(reversed(self.last_order)) if self.last_order else available_models
        self.last_order = fallback
        return fallback
    
    def get_last_order(self) -> Optional[List[str]]:
        """Returnează ultima ordine generată."""
        return self.last_order