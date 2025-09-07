from typing import List, Tuple

# Define symptom categories and their base scores
SYMPTOM_SEVERITY = {
    "critical": {"shortness of breath": 8, "chest pain": 7, "severe pain": 7, "difficulty breathing": 8, "unconsciousness": 10, "sudden weakness": 7},
    "urgent": {"fever": 4, "persistent cough": 3, "abdominal pain": 5, "headache with fever": 5, "vomiting": 3, "diarrhea": 3, "dizziness": 4},
    "stable": {"headache": 2, "nausea": 2, "mild pain": 2, "sore throat": 1, "runny nose": 1}
}

def get_triage_score(symptoms: List[str], age: int) -> int:
    """
    Calculates a triage score based on symptoms and age.
    Higher score means higher severity.
    """
    score = 0
    normalized_symptoms = [s.lower().strip() for s in symptoms]

    # Age-based scoring (adjusted for more impact)
    if age < 1: # Infants
        score += 5
    elif age < 18: # Children/Adolescents
        score += 2
    elif age >= 65: # Elderly
        score += 4
    
    # Symptom-based scoring with weights
    for category, symptom_map in SYMPTOM_SEVERITY.items():
        for known_symptom, base_score in symptom_map.items():
            if known_symptom in normalized_symptoms:
                score += base_score

    # Rule-based combinations (examples - expand as needed)
    if "chest pain" in normalized_symptoms and "shortness of breath" in normalized_symptoms:
        score += 5 # Significantly increase score for combination
    if "fever" in normalized_symptoms and "headache" in normalized_symptoms:
        score += 2
    if "severe pain" in normalized_symptoms and (age < 5 or age > 75):
        score += 3 # Vulnerable age groups with severe pain

    # Ensure score doesn't go below zero
    return max(0, score)

def get_severity_level(score: int) -> str:
    """
    Determines severity level based on triage score.
    """
    if score >= 7:
        return "Critical"
    elif score >= 4:
        return "Urgent"
    else:
        return "Stable"

def get_estimated_wait_time(severity_level: str, current_queue_length: int) -> int:
    """
    Estimates wait time in minutes based on severity and queue length.
    This is a simplified model.
    """
    base_wait_time = 10 # minutes per patient if queue is empty

    if severity_level == "Critical":
        return 5 + (current_queue_length * 2) # Critical patients get priority
    elif severity_level == "Urgent":
        return 15 + (current_queue_length * 5)
    else: # Stable
        return 30 + (current_queue_length * 10)
