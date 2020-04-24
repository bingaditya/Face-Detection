import tkinter as tk
from time import sleep
from PIL import Image, ImageTk
from itertools import count
from tkinter.ttk import *
import numpy as np
import cv2

class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):         #checks im is instance of string class bcoz im is a gif
            im = Image.open(im)         #it will open the image and specifies the location and set some info properties
        self.loc = 0                    #initializing the loc variable
        self.frames = []                #frame array
        try:
            for i in count(1):          
                self.frames.append(ImageTk.PhotoImage(im.copy()))   #it append image frame by frame in the array of frame
                im.seek(i)  # seeks ie attempt to find 1 to the given sequence if beyond the sequence the EOFerror
        except EOFError:
            pass           #is used when a statement is required syntatically but we dont want any code

        try:
            self.delay = im.info['duration']    #time to display current frame of the gif in milisecond
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()


    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)
def face():
    cap=cv2.VideoCapture(0)
    m=0
    face_cascade=cv2.CascadeClassifier('C:\Python37\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
    while(True):
        
        #eye_cascade=cv2.CascadeClassifier('C:\Python37\Lib\site-packages\cv2\data\haarcascade_eye.xml')
        #ret,frame=cap.read()
        (_, im) = cap.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x,y,w,h) in faces:
            
            img = cv2.rectangle(im,(x,y),(x+w,y+h),(255,0,0),2)
            #roi_gray = gray[y:y+h, x:x+w]
            #roi_color = img[y:y+h, x:x+w]
            #eyes = eye_cascade.detectMultiScale(roi_gray)
            #for (ex,ey,ew,eh) in eyes:
                #cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            cv2.imshow('frame',im)
            key=cv2.waitKey(1)
            if key == 27:
                m=1
                break
        if m==1:
            break


    cap.release()
    cv2.destroyAllWindows()

def eye():
    cap=cv2.VideoCapture(0)
    m=0
    while(True):
        face_cascade=cv2.CascadeClassifier('C:\Python37\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
        eye_cascade=cv2.CascadeClassifier('C:\Python37\Lib\site-packages\cv2\data\haarcascade_eye.xml')
        ret,frame=cap.read()
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            img = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                cv2.imshow('frame',frame)
                key=cv2.waitKey(10)
                if key ==27:
                    m=1
                    #cv2.destroyAllWindows()
                    break
            if m==1:
                break
        if m==1:
            break
    cap.release()
    cv2.destroyAllWindows()
    
    
def create_window():
    root.destroy()
    window=tk.Tk()
    window.geometry("500x500")
    window.configure(bg='gray')
    lb1=tk.Label(window,text="CLICK BUTTON FOR FACE DETCETION",bg='green')
    lb1.configure(font=('Courier',10,'bold'))
    lb1.place(x=20,y=50)
    lb2=tk.Label(window,text="CLICK BUTTON FOR EYE DETCETION",bg='red')
    lb2.configure(font=('Courier',10,'bold'))
    lb2.place(x=20,y=100)
   # lb1.pack()
    btn=tk.Button(window,text="FACE DETECTION",command=face)
    btn2=tk.Button(window,text="EYE DETECTION",command=eye)
    btn.place(x=300,y=50)
    
    btn2.place(x=300,y=100)
    #btn.pack(fill=tk.X,side=tk.LEFT)
    window.mainloop()
    

root = tk.Tk()
#img3=tk.PhotoImage(file='backgr.png')
root.configure(bg='gray')
img2=tk.PhotoImage(file='ppg.png')
lb2=ImageLabel(root,image=img2,height='60')
lb2.pack(fill=tk.X ,padx=30)
lbl = ImageLabel(root)
lbl.pack()
lbl.load('faced.gif')
img=tk.PhotoImage(file='butt1.png')
btn= tk.Button(root,width='800',bg='green',image=img,compound=tk.LEFT,command=create_window)
root.after(5000, btn.pack)

root.mainloop()
