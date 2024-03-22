import tkinter as tk
import random
from PIL import Image, ImageTk

class TestFrame(object):

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Test frame (Master)')
        self.root.geometry('900x500')
        self.root.configure(background='green')
        self.init_frame()


    def init_frame(self):

        self.main_frame = tk.Frame(self.root,bg='black')
        self.main_frame.pack(pady=20,expand=True)


        #create subframes
        self.top_frame = TopFrame(self)
        self.mid_frame = MidFrame(self)
        self.bottom_frame = BottomFrame(self)
        self.bottom_frame.hide()



class TopFrame(object):

    def __init__(self,master):
        self.init_frame(master)

    def init_frame(self,master):
        self.frame = tk.LabelFrame(master.main_frame,text='',bd=0)
        self.frame.grid(row=0,column=0,padx=20,ipadx=20)
        # self.frame.pack()
        
        self.label = tk.Label(self.frame,text='<top>')
        self.label.pack(pady=20)

class MidFrame(object):

    def __init__(self,master):
        self.master = master
        self.init_frame(master)


    def init_frame(self,master):
        self.frame = tk.LabelFrame(master.main_frame,text='',bd=0)
        self.frame.grid(row=1,column=0,padx=20,ipadx=20)
        # self.frame.pack()
        
        self.label = tk.Label(self.frame,text='')
        self.label.pack(pady=20)

        self.show_bottom_button = tk.Button(self.frame,text='Show bottom frame!',command=self.show_bottom_frame)
        self.show_bottom_button.pack(padx=10,pady=10)

    def show_bottom_frame(self):
        self.master.bottom_frame.init_frame()
        self.show_bottom_button.config(state='disabled')


class BottomFrame(object):

    def __init__(self,master):
        self.master = master
        self.init_frame()
        

    def init_frame(self):
        if not self.isVisible():
            self.frame = tk.LabelFrame(self.master.main_frame,text='',bd=0)
            self.frame.grid(row=2,column=0,padx=20,ipadx=20)
            
            self.label = tk.Label(self.frame,text='')
            self.label.pack(pady=20)

            self.init_button()

    def init_button(self):
        self.button = tk.Button(self.frame,text='hide frame',command = self.hide)
        self.button.pack(padx=10,pady=10)

    def hide(self):
        if self.isVisible():
            self.frame.grid_forget()
            self.master.mid_frame.show_bottom_button.config(state='normal')
        
    def isVisible(self):
        try:
            return len(self.frame.grid_info()) > 0
        except AttributeError:
            return False


if __name__ == '__main__':

    frame = TestFrame()
    frame.root.mainloop()

