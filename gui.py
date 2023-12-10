from tkinter import *
from subprocess import call
import paremeter as pm

root = Tk()

class Menu:
    def click_button(self,numbers):
        global operator
        global var
        self.operator = str(self.operator) + str(numbers)
        self.var.set(self.operator)
        
    def label_button(self,label_key,value,row_number,column_number,height_val=2,width_val=35,column_span=2, button_color=None, fg_color=None, theme=None):

        label = Label(label_key, bg=self.bg_color)
        label.grid(row=row_number, 
                   column=column_number,
                   columnspan=column_span)

        if theme == "Inverse":
            button_color = button_color or self.green_color
            fg_color = fg_color or self.dark_color
        else:
            button_color = button_color or self.dark_color
            fg_color = fg_color or self.green_color

        button = Button(label, text=value, font=(self.font_type, self.font_size),height=height_val, width=width_val,bg=button_color,fg=fg_color)
        button.pack()
        return


    def __init__(self,master):

        self.bg_color = "#4D4D4D"
        self.dark_color  = "#1d2023"

        self.font_type = "Helvetica"
        self.font_size = "16"
        self.green_color = '#66B933'
        
        label_key = Label(root, height=15, width=20,bd=10,bg=self.bg_color)
        label_key.pack(side=LEFT, fill=BOTH, expand=True)
        
        self.label_button(label_key,'START',0,0)       
        self.label_button(label_key,'EXIT',1,0, theme="Inverse")


c = Calculator(root)
root.title(pm.title)
root.mainloop()