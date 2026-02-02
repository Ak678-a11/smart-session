import dlib

detector = dlib.get_frontal_face_detector()

def detect_faces(gray_frame):
    faces = detector(gray_frame)
    return len(faces)