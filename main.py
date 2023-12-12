# Import Library
import cv2
import parameter as pm
import tkinter as tk
import PIL.Image, PIL.ImageTk
from capture_video import capture_video

class Menu(capture_video):    

    def Menu(self, window):
        self.window = window
        self.window.title(pm.title)

        # Create a canvas that can fit the video source
        self.canvas = tk.Canvas(window, width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        # Button to start/stop the video
        self.btn_snapshot = tk.Button(window, text="Exit", width=50, command=self.stop_program)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

        self.delay = 10  
        self.update()

        self.window.mainloop()

    def update(self):
        # # Get a frame from the video source
        self.start_capture()
        if self.ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    # Function to stop the program
    def stop_program(self):
        root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Menu(root).Menu(root)
