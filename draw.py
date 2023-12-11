import cv2

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