# exporter.py - Export JSON pentru Diagnoză

import json
from datetime import datetime
from typing import List, Dict

def export_conversation(rounds_data: List[Dict], filename: str = None) -> str:
    """
    Exportă conversația în JSON complet pentru diagnoză.
    
    Args:
        rounds_data: Lista cu date despre fiecare rundă
        filename: Nume fișier (opțional, default: timestamp)
        
    Returns:
        Path către fișierul salvat
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"agora_conversation_{timestamp}.json"
    
    export_data = {
        "conversation_id": datetime.now().isoformat(),
        "export_timestamp": datetime.now().isoformat(),
        "total_rounds": len(rounds_data),
        "rounds": rounds_data
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    return filename

def generate_diagnostic_report(rounds_data: List[Dict]) -> Dict:
    """
    Generează raport diagnostic despre halucinații.
    
    Returns:
        Dict cu statistici despre halucinații
    """
    total_responses = 0
    hallucination_counts = {
        "invents_future_responses": 0,
        "self_citation": 0,
        "consecutive_responses": 0,
        "quotes_others": 0
    }
    
    by_model = {}
    
    for round_data in rounds_data:
        for response in round_data.get("responses", []):
            total_responses += 1
            model = response["model"]
            
            if model not in by_model:
                by_model[model] = {
                    "total_responses": 0,
                    "hallucinations": {k: 0 for k in hallucination_counts.keys()}
                }
            
            by_model[model]["total_responses"] += 1
            
            hallucinations = response.get("hallucination_flags", {})
            for flag, value in hallucinations.items():
                if value:
                    hallucination_counts[flag] += 1
                    by_model[model]["hallucinations"][flag] += 1
    
    return {
        "total_responses": total_responses,
        "total_hallucinations": hallucination_counts,
        "by_model": by_model
    }