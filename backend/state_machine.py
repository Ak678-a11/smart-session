# state_machine.py

def determine_status(confusion_score: float):
    if confusion_score >= 0.7:
        return "CONFUSED"
    elif confusion_score >= 0.4:
        return "UNSURE"
    else:
        return "FOCUSED"