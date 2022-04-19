import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile

from PIL import ImageTk, Image
import io
import os
from google.cloud import vision
from google.cloud.vision_v1 import types
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import re
import string
import cv2
import numpy as np


credential_path = "C:\\Users\\rixen\\PycharmProjects\\wise-coyote-343006-8c099e81f8d2.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
client = vision.ImageAnnotatorClient()


def view():
    btnSave = tk.Button(top)
    btnSave.place(relx=0.4, rely=0.922, height=44, width=137)
    btnSave.configure(activebackground="#ececec")
    btnSave.configure(activeforeground="#000000")
    btnSave.configure(background="#d9d9d9")
    btnSave.configure(disabledforeground="#a3a3a3")
    btnSave.configure(foreground="#000000")
    btnSave.configure(highlightbackground="#d9d9d9")
    btnSave.configure(highlightcolor="black")
    btnSave.configure(pady="0")
    btnSave.configure(text='''Save''')
    btnSave.configure(command=submit)


def detect_text(path):

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.document_text_detection(image=image)
    extracted_keywords = []
    texts = response.text_annotations

    for text in texts:
        extracted_keywords.append(text.description)
    print(extracted_keywords)
    keywords = sent_tokenize(str(extracted_keywords[0]))
    str1 = ""
    for k in keywords:
        if k == "\n":
            str1 += " "
        else:
            str1 += k
    #print(str1)
    top.savefile = filedialog.asksaveasfile(filetypes=(("Text Files", "*.txt"),), defaultextension=("Text Files", "*.txt"))
    f = os.path.basename(top.savefile.name)
    dirname = os.path.dirname(os.path.abspath(top.savefile.name))
    os.chdir(dirname)
    file = open(f, "a")
    try:
        for r in str1:
            file.write(r)
    except:
           messagebox.showwarning("SAE", "Error converting to file")
    messagebox.showinfo("SAE", "Image converted to file successfully")



def upload():
    i = 1
    global img
    global path
    top.filename = filedialog.askopenfilename(initialdir="D:\\python\\", title=" Select a File", filetypes=(("PNG FIles", "*.png"), ("JPEG Files", "*.jpeg"), ("Other Files", "*.jpg")))
    path = top.filename
    x = StringVar()
    x.set(path)
    txtFileName.configure(text=x)
    im = Image.open(top.filename)
    im = im.resize((408, 461), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(im)
    lblImage.configure(image=img)
    result = messagebox.askyesno("Crop Image", "Would you like to crop the image?")
    if result:
        global imCrop
        showCrossHair = False
        image = cv2.imread(top.filename)
        r = cv2.selectROI(image, showCrossHair)
        imCrop = image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
        top.img_name = filedialog.asksaveasfilename(initialdir="D:\\python\\", title="Save file as", filetypes=(("PNG Files", "*.png"), ("JPEG Files", "*.jpg")))
        print(top.img_name)
        cv2.imwrite(top.img_name, imCrop)
        messagebox.showinfo("Info", "Image Saved")
        im = Image.open(top.img_name)
        im = im.resize((408, 461), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(im)
        lblImage.configure(image=img)
        path = top.img_name
    else:
        im = Image.open(top.filename)
        im = im.resize((408, 461), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(im)
        lblImage.configure(image=img)
        path = top.filename
    view()



def submit():
    detect_text(path)



def main():
    global top, txtFileName, lblImage, txtDirName, txtQuestion
    top = Tk()
    top.geometry("600x705+-3+2")
    top.minsize(120, 1)
    top.maxsize(1354, 733)
    top.resizable(1, 1)
    top.title("SAE-Home")
    top.configure(background="#ffffff")
    top.configure(highlightbackground="#d9d9d9")
    top.configure(highlightcolor="black")

    lblFileName = tk.Label(top)
    lblFileName.place(relx=0.037, rely=0.099, height=31, width=90)
    lblFileName.configure(activebackground="#ffffff")
    lblFileName.configure(activeforeground="black")
    lblFileName.configure(anchor='e')
    lblFileName.configure(background="#ffffff")
    lblFileName.configure(disabledforeground="#a3a3a3")
    lblFileName.configure(foreground="#000000")
    lblFileName.configure(highlightbackground="#d9d9d9")
    lblFileName.configure(highlightcolor="black")
    lblFileName.configure(text='''Choose Image:''')

    txtFileName = tk.Entry(top)
    txtFileName.place(relx=0.192, rely=0.099, height=30, relwidth=0.523)
    txtFileName.configure(background="white")
    txtFileName.configure(disabledforeground="#a3a3a3")
    txtFileName.configure(font="TkFixedFont")
    txtFileName.configure(foreground="#000000")
    txtFileName.configure(highlightbackground="#d9d9d9")
    txtFileName.configure(highlightcolor="black")
    txtFileName.configure(insertbackground="black")
    txtFileName.configure(selectbackground="#c4c4c4")
    txtFileName.configure(selectforeground="black")
    txtFileName.configure(state='disabled')

    btnUploadImage = tk.Button(top)
    btnUploadImage.place(relx=0.733, rely=0.099, height=34, width=107)
    btnUploadImage.configure(activebackground="#ececec")
    btnUploadImage.configure(activeforeground="#000000")
    btnUploadImage.configure(background="#d9d9d9")
    btnUploadImage.configure(disabledforeground="#a3a3a3")
    btnUploadImage.configure(foreground="#000000")
    btnUploadImage.configure(highlightbackground="#d9d9d9")
    btnUploadImage.configure(highlightcolor="black")
    btnUploadImage.configure(pady="0")
    btnUploadImage.configure(text='''Upload''')
    btnUploadImage.configure(command=upload)

    lblImage = tk.Label(top)
    lblImage.place(relx=0.15, rely=0.184, height=461, width=408)
    lblImage.configure(activebackground="#f9f9f9")
    lblImage.configure(activeforeground="black")
    lblImage.configure(background="#ffffff")
    lblImage.configure(disabledforeground="#a3a3a3")
    lblImage.configure(foreground="#000000")
    lblImage.configure(highlightbackground="#d9d9d9")
    lblImage.configure(highlightcolor="black")


    top.mainloop()


main()
