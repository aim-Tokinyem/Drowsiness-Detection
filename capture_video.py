from pygame import mixer as pymixer
import paremeter as pm
import mediapipe as mp
import cv2
from calculation import calculation

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