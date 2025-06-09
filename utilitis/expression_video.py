import cv2
import mediapipe as mp

# Inisialisasi mediapipe face mesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

# Inisialisasi webcam
cap = cv2.VideoCapture(1)

with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(img_rgb)

        if result.multi_face_landmarks:
            for face_landmarks in result.multi_face_landmarks:
                # Gambar landmark wajah
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_styles.get_default_face_mesh_tesselation_style())

                # Deteksi ekspresi sederhana
                h, w, _ = frame.shape
                lm = face_landmarks.landmark

                top_lip = lm[13]
                bottom_lip = lm[14]
                left_lip = lm[61]
                right_lip = lm[291]

                vertical_mouth = abs(top_lip.y - bottom_lip.y)
                horizontal_mouth = abs(left_lip.x - right_lip.x)

                expression = "Neutral"
                color = (0, 255, 255)

                if vertical_mouth > 0.05 and horizontal_mouth > 0.15:
                    expression = "Surprised"
                    color = (255, 0, 0)
                elif vertical_mouth > 0.03:
                    expression = "Open Mouth"
                    color = (0, 0, 255)
                elif horizontal_mouth > 0.12:
                    expression = "Smile"
                    color = (0, 255, 0)

                # Tampilkan teks ekspresi
                x = int(lm[10].x * w)
                y = int(lm[10].y * h) - 30
                cv2.putText(frame, expression, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        cv2.imshow("Expression & Landmark Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
