import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

class FaceRecognitionAttendance:
    def __init__(self, known_faces_dir):
        self.known_faces_dir = known_faces_dir
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()

    def load_known_faces(self):
        for filename in os.listdir(self.known_faces_dir):
            if filename.endswith((".jpg", ".jpeg", ".png")):
                path = os.path.join(self.known_faces_dir, filename)
                name = os.path.splitext(filename)[0]
                image = face_recognition.load_image_file(path)
                encoding = face_recognition.face_encodings(image)[0]
                self.known_face_encodings.append(encoding)
                self.known_face_names.append(name)
        print(f"Loaded {len(self.known_face_names)} known faces.")

    def recognize_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            face_names.append(name)

        return face_locations, face_names

    def mark_attendance(self, name):
        with open('attendance.csv', 'a+') as f:
            f.seek(0)
            lines = f.readlines()
            recorded_names = [line.split(',')[0] for line in lines]
            
            if name not in recorded_names:
                now = datetime.now()
                date_string = now.strftime('%Y-%m-%d')
                time_string = now.strftime('%H:%M:%S')
                f.write(f'{name},{date_string},{time_string}\n')
                print(f"Marked attendance for {name}")

    def process_frame(self, frame):
        face_locations, face_names = self.recognize_faces(frame)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            if name != "Unknown":
                self.mark_attendance(name)

        return frame

    def run_video_recognition(self):
        video_capture = cv2.VideoCapture(0)

        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            processed_frame = self.process_frame(frame)

            cv2.imshow('Video', processed_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    known_faces_dir = "known_faces"  # Directory containing images of known faces
    face_recognition_system = FaceRecognitionAttendance(known_faces_dir)
    face_recognition_system.run_video_recognition()