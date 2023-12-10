# Import Library
import cv2
import mediapipe as mp
import time
from scipy.spatial import distance
import pygame
import paremeter as pm





def main():
    # Choose Camera
    cap = cv2.VideoCapture(0)

    # Load Alarm .wav
    pygame.mixer.init()
    pygame.mixer.music.load(pm.alarm)

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh()

    COUNTER = 0

    def calculate_EAR(eye):
        A = distance.euclidean(eye[1], eye[5])
        B = distance.euclidean(eye[2], eye[4])
        C = distance.euclidean(eye[0], eye[3])
        ear_aspect_ratio = (A+B)/(2.0*C)
        return ear_aspect_ratio

    def get_6_point(eye):
        eyes = []
        for i in eye:
            x = int(facial_landmark.landmark[i].x * width)
            y = int(facial_landmark.landmark[i].y * height)
            cv2.circle(frame, (x,y),1, (0,0,255), 2)
            eyes.append((x,y))
        return eyes

    def draw_facial_landmark(face):
        for i in face:
            x = int(facial_landmark.landmark[i].x * width)
            y = int(facial_landmark.landmark[i].y * height)
            circle = cv2.circle(frame, (x,y),1, (255,0,0), -1)

    while True:
        _, frame = cap.read()
        height, width, _ = frame.shape
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(frameRGB)
        
        if result.multi_face_landmarks:
            for face_no, facial_landmark in enumerate(result.multi_face_landmarks):
                
                # 6 Point eyes Facial Landmark
                left_index = [362 ,385, 387 ,263, 373, 380]
                right_index = [33, 160, 158, 133, 153, 144]
                
                # Draw Facial Landmark
                draw_facial_landmark(range(0,468))
                    
                # Get 6 point eye in face    
                leftEye = get_6_point(left_index)
                rightEye = get_6_point(right_index)
                    

            # Calculate EAR
            left_ear = calculate_EAR(leftEye)
            right_ear = calculate_EAR(rightEye)       
            EAR = (left_ear + right_ear)/2
            
            # print("EAR Value : ", (EAR))    
            cv2.putText(frame, "EAR: {:.2f}".format(EAR), (450, 400),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 12)
            cv2.putText(frame, "EAR: {:.2f}".format(EAR), (450, 400),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 5)

            # Droswsiness Detection
            if EAR <= 0.23:
                COUNTER += 1
                if COUNTER >= 50 :
                    pygame.mixer.music.play(-1)
                    # print('Mengantuk Terdeteksi')
                    cv2.putText(frame,"Mengantuk Terdeteksi",(200,80),
                                cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),12)
                    cv2.putText(frame,"Mengantuk Terdeteksi",(200,80),
                                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),5)

            else:
                COUNTER = 0
                pygame.mixer.music.stop()    
            
        cv2.imshow('Deteksi Mengantuk', frame)
        
        # Press "Esc" to Close Apllication
        key = cv2.waitKey(1)
        if key == 27:
            pygame.mixer.music.stop()  
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()