# Import Library
import cv2
import mediapipe as mp
from scipy.spatial import distance
from pygame import mixer as pymixer
import paremeter as pm
import time
import tkinter as tk
import PIL.Image, PIL.ImageTk

class draw:
    def __init__(self):
        pass

    def draw_facial_landmark(self,face,facial_landmark,width,height,frame):
        for i in face:
            x = int(facial_landmark.landmark[i].x * width)
            y = int(facial_landmark.landmark[i].y * height)
            circle = cv2.circle(frame, (x,y),1, (255,0,0), -1)
        return

    def draw_text(self,input_text,frame, position_text, bg_text_color, text_color):
        cv2.putText(frame, f"{input_text}", position_text,
                                cv2.FONT_HERSHEY_SIMPLEX, 1, bg_text_color, 12)
        cv2.putText(frame, f"{input_text}", position_text,
                                cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 5)


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
            

class capture_video:
    def __init__(self, window):
        # Choose Camera
        self.cap = cv2.VideoCapture(0)
        # Load Alarm .wav
        pymixer.init()
        pymixer.music.load(pm.alarm)

        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh()
        
        self.cal = calculation()


    def start_capture(self):
        # while True:
        self.ret, self.frame = self.cap.read()
        self.height, self.width, _ = self.frame.shape
        frameRGB = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        result = self.face_mesh.process(frameRGB)

        self.cal.calculating(result,self.width,self.height,self.frame)
            

class Menu(capture_video):
    def Menu(self, window):
        self.window = window
        self.window.title(pm.title)

        # Create a canvas that can fit the video source
        self.canvas = tk.Canvas(window, width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        # Button to start/stop the video
        self.btn_snapshot = tk.Button(window, text="Exit to Menu", width=50, command=None)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)


        self.delay = 10  
        self.update()

        self.window.mainloop()

    def update(self):
        # # Get a frame from the video source
        # ret, frame = self.cap.read()
        self.start_capture()
        if self.ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    app = Menu(root).Menu(root)
