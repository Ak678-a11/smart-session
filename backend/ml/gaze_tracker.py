import dlib

detector = dlib.get_frontal_face_detector()

def detect_gaze_and_faces(gray_frame):
    faces = detector(gray_frame)

    if len(faces) == 0:
        return 0, "no_face"

    if len(faces) > 1:
        return len(faces), "multiple_faces"

    face = faces[0]

    h, w = gray_frame.shape
    cx = (face.left() + face.right()) // 2
    cy = (face.top() + face.bottom()) // 2

    dx = cx - w // 2
    dy = cy - h // 2

    if dx > 40:
        gaze = "right"
    elif dx < -40:
        gaze = "left"
    elif dy > 40:
        gaze = "down"
    elif dy < -40:
        gaze = "up"
    else:
        gaze = "center"

    return 1, gaze