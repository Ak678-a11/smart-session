def compute_confusion_score(
    face_count: int,
    gaze_direction: str,
    brow_furrow: bool,
    smiling: bool,
    head_tilt: bool
):
    """
    Returns:
    confusion_score (0.0 – 1.0)
    """

    score = 0.0

    # Proctoring failures
    if face_count == 0:
        score += 0.4
    elif face_count > 1:
        score += 0.5

    # Attention loss
    if gaze_direction in ["left", "right", "up", "down"]:
        score += 0.2

    # Facial cues
    if brow_furrow:
        score += 0.2

    if not smiling:
        score += 0.1

    if head_tilt:
        score += 0.1

    return min(score, 1.0)