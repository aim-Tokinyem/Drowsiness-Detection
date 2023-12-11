from scipy.spatial import distance
import paremeter as pm
import cv2
from pygame import mixer as pymixer
from draw import draw

class calculation():
    def __init__(self):
        self.COUNTER = pm.default_counter
        # 6 Point eyes Facial Landmark
        self.left_index = pm.left_eye_index
        self.right_index = pm.right_index

        self.draw = draw()

    def calculate_EAR(self,eye):
        A = distance.euclidean(eye[1], eye[5])
        B = distance.euclidean(eye[2], eye[4])
        C = distance.euclidean(eye[0], eye[3])
        ear_aspect_ratio = (A+B)/(2.0*C)
        return ear_aspect_ratio

    def get_6_point(self,eye,facial_landmark,width,height,frame):
        eyes = []
        for i in eye:
            x = int(facial_landmark.landmark[i].x * width)
            y = int(facial_landmark.landmark[i].y * height)
            cv2.circle(frame, (x,y),1, (0,0,255), 2)
            eyes.append((x,y))
        return eyes       
        
    def calculating(self,result,width,height,frame):
        if result.multi_face_landmarks:
            for face_no, facial_landmark in enumerate(result.multi_face_landmarks):
                # Draw Facial Landmark
                self.draw.draw_facial_landmark(range(0,468),facial_landmark,width,height,frame)
                    
                # Get 6 point eye in face    
                leftEye = self.get_6_point(self.left_index,facial_landmark,width,height,frame)
                rightEye = self.get_6_point(self.right_index,facial_landmark,width,height,frame)
                    

            # Calculate EAR
            left_ear = self.calculate_EAR(leftEye)
            right_ear = self.calculate_EAR(rightEye)       
            EAR = (left_ear + right_ear)/2
            
            self.draw.draw_text(f"EAR: {EAR:.2f} ", frame, pm.ear_position, pm.ear_bg_text_color, pm.ear_text_color)

            # Droswsiness Detection
            if EAR <= pm.validate_EAR:
                self.COUNTER += 1
                if self.COUNTER >= pm.validate_counter :
                    self.draw.draw_text(f"Drowsiness Detected ", frame, pm.alert_position, pm.alert_bg_text_color, pm.alert_text_color)
                    pymixer.music.play(-1)

            else:
                self.COUNTER = pm.default_counter
                pymixer.music.stop()