from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import gensim
from PIL import ImageTk, Image
import io
import os
from google.cloud import vision
from google.cloud.vision_v1 import types
import nltk
nltk.download('stopwords')
from nltk.tokenize import word_tokenize, sent_tokenize
import re
import string
from nltk.corpus import stopwords
import numpy as np
from nltk.probability import FreqDist
import math
from gensim.models.doc2vec import TaggedDocument


def process(f):
    r = open(f).read()
    tokens = word_tokenize(r)
    words = [w.lower() for w in tokens]

    porter = nltk.PorterStemmer()
    stemmed_tokens = [porter.stem(t) for t in words]

    stop_words = set(stopwords.words('english'))
    filtered_tokens = [w for w in stemmed_tokens if not w in stop_words]

    count = nltk.defaultdict(int)
    for word in filtered_tokens:
        count[word] += 1
    print(count)
    return count


def cos_sim(a, b):
    dot_product = np. dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)


def getSimilarity(dict1, dict2):
    all_words_list = []
    for key in dict1:
        all_words_list.append(key)
    for key in dict2:
        all_words_list.append(key)
    all_words_list_size = len(all_words_list)

    v1 = np.zeros(all_words_list_size, dtype=np.int)
    v2 = np.zeros(all_words_list_size, dtype=np.int)
    i = 0
    for (key) in all_words_list:
        v1[i] = dict1.get(key,0)
        v2[i] = dict2.get(key,0)
        i = i + 1
   # print(v1)
   # print(v2)
    return cos_sim(v1, v2)


def checkSim(docfile, ansfile):
    a = process(docfile)
    b = process(ansfile)
    return getSimilarity(a, b) * 100

def create():
    global f
    global path
    parentdir = "D:\\python\\"
    os.chdir(parentdir)
    name = txtName.get()
    if name == " ":
        messagebox.showwarning("Error", "Please enter a valid file name")
    else:
        name += ".txt"
        if os.path.isfile(os.path.join(parentdir,name)):
            res = messagebox.askyesno("Info", "Such a filename already exists.Do you wish to continue?")
            if res:
                path = parentdir + name
                f = open(name, 'a')
                txtName.configure(state="disabled")
                btnCreate.configure(state="disabled")
            else:
                txtName.delete(0, 'end')
        else:
            path = parentdir + name
            f = open(name, 'a')
            messagebox.showinfo("Info", "File created successfully")
            txtName.configure(state="disabled")
            btnCreate.configure(state="disabled")


def uploadDoc():
    global docfile
    top.filename = filedialog.askopenfilename(initialdir="D:\\python", title=" Select a File", filetypes=(("Text Files", "*.txt"),))
    x = StringVar()
    x.set(top.filename)
    txtDoc.configure(text=x)
    docfile = top.filename


def uploadKey():
    global keyfile
    top.filename = filedialog.askopenfilename(initialdir="D:\\python", title=" Select a File", filetypes=(("Text Files", "*.txt"),))
    x = StringVar()
    x.set(top.filename)
    txtKey.configure(text=x)
    keyfile = top.filename


def uploadAns():
    global ansfile
    top.filename = filedialog.askopenfilename(initialdir="D:\\python", title=" Select a File", filetypes=(("Text Files", "*.txt"),))
    x = StringVar()
    x.set(top.filename)
    txtAnsKey.configure(text=x)
    ansfile = top.filename


def checkKey(docfile, keyfile):
    global keycount
    doc_key = []
    df = open(docfile, "r")
    for line in df:
        doc_key.extend(line.split())

    key_file = []
    kf = open(keyfile, "r")
    for line in kf:
        key_file.extend(line.split())

    keycount = len(key_file)
    c = 0
    i = 0
    j = 0
    for i in range(len(doc_key)):
        j = 0
        for j in range(len(key_file)):
            if str(doc_key[i]).casefold() == str(key_file[j]).casefold():
                c = c + 1
                del(key_file[j])
                break
            else:
                j += 1
        if len(key_file) == 0:
            break
        else:
            i += 1
    return c


def check():
    if docfile == " " or keyfile == " " or ansfile == " ":
        messagebox.showerror("Error", "Kindly check all the documents are uploaded.")
    elif path == " ":
        messagebox.showerror("Error", "Please select a file to upload the marks to")
    elif txtAnsMark.get() == " " or txtKeyMark.get() == " ":
        messagebox.showwarning("Error", "Enter the marks")
    else:
        key = checkKey(docfile, keyfile)
        km = int(txtKeyMark.get())
        keymark = key * km/keycount
        print("Key count-> ", keycount)

        n = checkSim(docfile, ansfile)
        n = round(n)
        print(n)
        print("keymark",keymark)
        if int(txtAnsMark.get()) > 2:
            if n > 90:
                ansmark = int(txtAnsMark.get())
            elif n > 75:
                ansmark = float(txtAnsMark.get()) - 0.5
            elif n > 65:
                ansmark = float(txtAnsMark.get()) - 1.0
            elif n > 50:
                ansmark = float(txtAnsMark.get()) / 2.0
            elif n > 40:
                ansmark = float(txtAnsMark.get()) - 2.0
            else:
                ansmark = 0
        else:

            if n > 50:
                ansmark = float(txtAnsMark.get())
            elif n > 40:
                ansmark = float(txtAnsMark.get()) - 1.0
            else:
                ansmark = 0
        print("ansmark=",ansmark)
        totalmark = keymark + ansmark

        file = open(path, "r+")
        text = file.read()
        if os.path.basename(docfile) in text:
            messagebox.showwarning("SAE", "Mark already uploaded")
        else:
            file = open(path, "a+")
            file.write(os.path.basename(docfile) + ": " + str(totalmark) + "\n")
            file.close()
            messagebox.showinfo("SAE", "Mark uploaded successfully")


def finish():
    txtName.configure(state="normal")
    txtName.delete(0, 'end')
    btnCreate.configure(state='normal')
    txtDoc.configure(state="normal")
    txtKey.configure(state="normal")
    txtAnsKey.configure(state="normal")
    txtDoc.delete(0, 'end')
    txtKey.delete(0, 'end')
    txtAnsKey.delete(0, 'end')
    txtDoc.configure(state="disabled")
    txtKey.configure(state="disabled")
    txtAnsKey.configure(state="disabled")
    txtAnsMark.delete(0, 'end')
    txtKeyMark.delete(0, 'end')


top = Tk()
top.geometry("635x498+354+127")
top.minsize(120, 1)
top.maxsize(1362, 741)
top.resizable(1, 1)
top.title("SAE-Evaluation")
top.configure(background="#d9d9d9")
top.configure(highlightbackground="#d9d9d9")
top.configure(highlightcolor="black")

lblDoc = Label(top)
lblDoc.place(relx=0.046, rely=0.261, height=34, width=71)
lblDoc.configure(activebackground="#f9f9f9")
lblDoc.configure(activeforeground="black")
lblDoc.configure(anchor='w')
lblDoc.configure(background="#d9d9d9")
lblDoc.configure(disabledforeground="#a3a3a3")
lblDoc.configure(foreground="#000000")
lblDoc.configure(highlightbackground="#d9d9d9")
lblDoc.configure(highlightcolor="black")
lblDoc.configure(justify='left')
lblDoc.configure(text='''Select file:''')

txtDoc = Entry(top)
txtDoc.place(relx=0.216, rely=0.261, height=30, relwidth=0.431)
txtDoc.configure(background="white")
txtDoc.configure(disabledforeground="#a3a3a3")
txtDoc.configure(font="TkFixedFont")
txtDoc.configure(foreground="#000000")
txtDoc.configure(highlightbackground="#d9d9d9")
txtDoc.configure(highlightcolor="black")
txtDoc.configure(insertbackground="black")
txtDoc.configure(selectbackground="#c4c4c4")
txtDoc.configure(selectforeground="black")
txtDoc.configure(state='disabled')

btnUploadDoc = Button(top)
btnUploadDoc.place(relx=0.66, rely=0.261, height=34, width=107)
btnUploadDoc.configure(activebackground="#ececec")
btnUploadDoc.configure(activeforeground="#000000")
btnUploadDoc.configure(background="#d9d9d9")
btnUploadDoc.configure(disabledforeground="#a3a3a3")
btnUploadDoc.configure(foreground="#000000")
btnUploadDoc.configure(highlightbackground="#d9d9d9")
btnUploadDoc.configure(highlightcolor="black")
btnUploadDoc.configure(pady="0")
btnUploadDoc.configure(text='''Upload''')
btnUploadDoc.configure(command=uploadDoc)


lblKey = Label(top)
lblKey.place(relx=0.046, rely=0.361, height=34, width=132)
lblKey.configure(activebackground="#f9f9f9")
lblKey.configure(activeforeground="black")
lblKey.configure(anchor='w')
lblKey.configure(background="#d9d9d9")
lblKey.configure(disabledforeground="#a3a3a3")
lblKey.configure(foreground="#000000")
lblKey.configure(highlightbackground="#d9d9d9")
lblKey.configure(highlightcolor="black")
lblKey.configure(justify='left')
lblKey.configure(text='''Select keyword file:''')

txtKey = Entry(top)
txtKey.place(relx=0.216, rely=0.361, height=30, relwidth=0.431)
txtKey.configure(background="white")
txtKey.configure(disabledforeground="#a3a3a3")
txtKey.configure(font="TkFixedFont")
txtKey.configure(foreground="#000000")
txtKey.configure(highlightbackground="#d9d9d9")
txtKey.configure(highlightcolor="black")
txtKey.configure(insertbackground="black")
txtKey.configure(selectbackground="#c4c4c4")
txtKey.configure(selectforeground="black")
txtKey.configure(state='disabled')

btnUploadKey = Button(top)
btnUploadKey.place(relx=0.66, rely=0.361, height=34, width=107)
btnUploadKey.configure(activebackground="#ececec")
btnUploadKey.configure(activeforeground="#000000")
btnUploadKey.configure(background="#d9d9d9")
btnUploadKey.configure(disabledforeground="#a3a3a3")
btnUploadKey.configure(foreground="#000000")
btnUploadKey.configure(highlightbackground="#d9d9d9")
btnUploadKey.configure(highlightcolor="black")
btnUploadKey.configure(pady="0")
btnUploadKey.configure(text='''Upload''')
btnUploadKey.configure(command=uploadKey)

lblKeyMark = Label(top)
lblKeyMark.place(relx=0.046, rely=0.602, height=34, width=208)
lblKeyMark.configure(activebackground="#f9f9f9")
lblKeyMark.configure(activeforeground="black")
lblKeyMark.configure(anchor='w')
lblKeyMark.configure(background="#d9d9d9")
lblKeyMark.configure(disabledforeground="#a3a3a3")
lblKeyMark.configure(foreground="#000000")
lblKeyMark.configure(highlightbackground="#d9d9d9")
lblKeyMark.configure(highlightcolor="black")
lblKeyMark.configure(justify='left')
lblKeyMark.configure(text='''Total Marks to be awarded(Keyword):''')

txtKeyMark = Entry(top)
txtKeyMark.place(relx=0.378, rely=0.602, height=30, relwidth=0.054)
txtKeyMark.configure(background="white")
txtKeyMark.configure(disabledforeground="#a3a3a3")
txtKeyMark.configure(font="TkFixedFont")
txtKeyMark.configure(foreground="#000000")
txtKeyMark.configure(highlightbackground="#d9d9d9")
txtKeyMark.configure(highlightcolor="black")
txtKeyMark.configure(insertbackground="black")
txtKeyMark.configure(selectbackground="#c4c4c4")
txtKeyMark.configure(selectforeground="black")

lblAnswer = Label(top)
lblAnswer.place(relx=0.046, rely=0.462, height=34, width=132)
lblAnswer.configure(activebackground="#f9f9f9")
lblAnswer.configure(activeforeground="black")
lblAnswer.configure(anchor='w')
lblAnswer.configure(background="#d9d9d9")
lblAnswer.configure(disabledforeground="#a3a3a3")
lblAnswer.configure(foreground="#000000")
lblAnswer.configure(highlightbackground="#d9d9d9")
lblAnswer.configure(highlightcolor="black")
lblAnswer.configure(justify='left')
lblAnswer.configure(text='''Select Answer key:''')

txtAnsKey = Entry(top)
txtAnsKey.place(relx=0.216, rely=0.462, height=30, relwidth=0.431)
txtAnsKey.configure(background="white")
txtAnsKey.configure(disabledforeground="#a3a3a3")
txtAnsKey.configure(font="TkFixedFont")
txtAnsKey.configure(foreground="#000000")
txtAnsKey.configure(highlightbackground="#d9d9d9")
txtAnsKey.configure(highlightcolor="black")
txtAnsKey.configure(insertbackground="black")
txtAnsKey.configure(selectbackground="#c4c4c4")
txtAnsKey.configure(selectforeground="black")
txtAnsKey.configure(state='disabled')

btnAnsKey = Button(top)
btnAnsKey.place(relx=0.66, rely=0.462, height=34, width=107)
btnAnsKey.configure(activebackground="#ececec")
btnAnsKey.configure(activeforeground="#000000")
btnAnsKey.configure(background="#d9d9d9")
btnAnsKey.configure(disabledforeground="#a3a3a3")
btnAnsKey.configure(foreground="#000000")
btnAnsKey.configure(highlightbackground="#d9d9d9")
btnAnsKey.configure(highlightcolor="black")
btnAnsKey.configure(pady="0")
btnAnsKey.configure(text='''Upload''')
btnAnsKey.configure(command=uploadAns)

lblAnsMark = Label(top)
lblAnsMark.place(relx=0.046, rely=0.683, height=34, width=199)
lblAnsMark.configure(activebackground="#f9f9f9")
lblAnsMark.configure(activeforeground="black")
lblAnsMark.configure(anchor='w')
lblAnsMark.configure(background="#d9d9d9")
lblAnsMark.configure(disabledforeground="#a3a3a3")
lblAnsMark.configure(foreground="#000000")
lblAnsMark.configure(highlightbackground="#d9d9d9")
lblAnsMark.configure(highlightcolor="black")
lblAnsMark.configure(justify='left')
lblAnsMark.configure(text='''Total Marks to be awarded(Answer):''')

txtAnsMark = Entry(top)
txtAnsMark.place(relx=0.378, rely=0.683, height=30, relwidth=0.054)
txtAnsMark.configure(background="white")
txtAnsMark.configure(disabledforeground="#a3a3a3")
txtAnsMark.configure(font="TkFixedFont")
txtAnsMark.configure(foreground="#000000")
txtAnsMark.configure(highlightbackground="#d9d9d9")
txtAnsMark.configure(highlightcolor="black")
txtAnsMark.configure(insertbackground="black")
txtAnsMark.configure(selectbackground="#c4c4c4")
txtAnsMark.configure(selectforeground="black")

lblName = Label(top)
lblName.place(relx=-0.031, rely=0.08, height=31, width=141)
lblName.configure(anchor='e')
lblName.configure(background="#d9d9d9")
lblName.configure(disabledforeground="#a3a3a3")
lblName.configure(foreground="#000000")
lblName.configure(justify='right')
lblName.configure(text='''Enter the Name:''')

txtName = Entry(top)
txtName.place(relx=0.216, rely=0.08, height=30, relwidth=0.29)
txtName.configure(background="white")
txtName.configure(disabledforeground="#a3a3a3")
txtName.configure(font="TkFixedFont")
txtName.configure(foreground="#000000")
txtName.configure(insertbackground="black")

btnCreate = Button(top)
btnCreate.place(relx=0.521, rely=0.08, height=34, width=107)
btnCreate.configure(activebackground="#ececec")
btnCreate.configure(activeforeground="#000000")
btnCreate.configure(background="#d9d9d9")
btnCreate.configure(disabledforeground="#a3a3a3")
btnCreate.configure(foreground="#000000")
btnCreate.configure(highlightbackground="#d9d9d9")
btnCreate.configure(highlightcolor="black")
btnCreate.configure(pady="0")
btnCreate.configure(text='''Create''')
btnCreate.configure(command=create)

btnCheck = Button(top)
btnCheck.place(relx=0.337, rely=0.803, height=34, width=117)
btnCheck.configure(activebackground="#ececec")
btnCheck.configure(activeforeground="#000000")
btnCheck.configure(background="#d9d9d9")
btnCheck.configure(disabledforeground="#a3a3a3")
btnCheck.configure(foreground="#000000")
btnCheck.configure(highlightbackground="#d9d9d9")
btnCheck.configure(highlightcolor="black")
btnCheck.configure(pady="0")
btnCheck.configure(text='''Check Answer''')
btnCheck.configure(command=check)

btnFinish = Button(top)
btnFinish.place(relx=0.661, rely=0.904, height=34, width=107)
btnFinish.configure(activebackground="#ececec")
btnFinish.configure(activeforeground="#000000")
btnFinish.configure(background="#d9d9d9")
btnFinish.configure(disabledforeground="#a3a3a3")
btnFinish.configure(foreground="#000000")
btnFinish.configure(highlightbackground="#d9d9d9")
btnFinish.configure(highlightcolor="black")
btnFinish.configure(pady="0")
btnFinish.configure(text='''Finish''')
btnFinish.configure(command=finish)
top.mainloop()