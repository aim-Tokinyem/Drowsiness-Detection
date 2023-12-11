import tkinter as tk
from subprocess import call
import paremeter as pm
from main import main
import cv2
import PIL.Image, PIL.ImageTk  # These are used to convert OpenCV images to Tkinter-compatible images



# root = Tk()

# class Menu:
#     def click_button(self,numbers):
#         global operator
#         global var
#         self.operator = str(self.operator) + str(numbers)
#         self.var.set(self.operator)
        
#     def label_button(self,label_key,value,row_number,column_number,height_val=2,width_val=35,column_span=2, button_color=None, fg_color=None, theme=None,commands=None):

#         label = Label(label_key, bg=self.bg_color)
#         label.grid(row=row_number, 
#                    column=column_number,
#                    columnspan=column_span)

#         if theme == "Inverse":
#             button_color = button_color or self.green_color
#             fg_color = fg_color or self.dark_color
#         else:
#             button_color = button_color or self.dark_color
#             fg_color = fg_color or self.green_color

#         button = Button(label, text=value, font=(self.font_type, self.font_size),height=height_val, width=width_val,bg=button_color,fg=fg_color,command=commands)
#         button.pack()
#         return


#     def __init__(self,master):

#         self.bg_color = "#4D4D4D"
#         self.dark_color  = "#1d2023"

#         self.font_type = "Helvetica"
#         self.font_size = "16"
#         self.green_color = '#66B933'
        
#         label_key = Label(root, height=15, width=20,bd=10,bg=self.bg_color)
#         label_key.pack(side=LEFT, fill=BOTH, expand=True)
        
#         self.label_button(label_key,'START',0,0, commands=self.trigger_main)       
#         self.label_button(label_key,'EXIT',1,0, theme="Inverse",commands=None)

#     def trigger_main(self):
#         main_instance = main()  # Create an instance of Main class
#         main_instance.run()     # Call the run method of Main class

#     def trigger_kill(self):
#         main_instance = main()  # Create an instance of Main class
#         main_instance.run()     # Call the run method of Main class

class Menu:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.video_source = 0  # Webcam source (default 0, you might need to change it)

        # Open video source (by default this will try to open the webcam)
        self.vid = cv2.VideoCapture(self.video_source)

        # Create a canvas that can fit the video source
        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        # Button to start/stop the video
        self.btn_snapshot = tk.Button(window, text="Snapshot", width=50, command=None)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

        # # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 10  # in milliseconds
        self.update()

        self.window.mainloop()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.read()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)



if __name__ == "__main__":
    root = tk.Tk()
    app = Menu(root, pm.title)