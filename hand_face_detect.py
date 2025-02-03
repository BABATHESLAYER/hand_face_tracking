import cv2
import numpy
import mediapipe as mp
mp_drawing_styles = mp.solutions.drawing_styles


# Initialize Mediapipe solutions
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh
hands = mp_hands.Hands()
face_mesh = mp_face_mesh.FaceMesh()
mp_drawing = mp.solutions.drawing_utils

# Define drawing specifications for hands (darker color and thicker lines)
hand_landmark_style = mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=5, circle_radius=2)
hand_connection_style = mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=5, circle_radius=2)

# Start capturing video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the image color space from BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame for hand tracking
    hand_results = hands.process(frame_rgb)

    # Process the frame for face mesh
    face_results = face_mesh.process(frame_rgb)

    # Convert back the image color space from RGB to BGR
    frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

    # Draw hand landmarks with the defined drawing specifications
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                landmark_drawing_spec=hand_landmark_style,
                connection_drawing_spec=hand_connection_style
            )

    # Draw face mesh landmarks
    if face_results.multi_face_landmarks:
        for face_landmarks in face_results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                frame, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=1)
                # connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style()
            )

    # Display the output
    cv2.imshow('Hand Tracking and Face Mesh', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()