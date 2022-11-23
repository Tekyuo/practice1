from tkinter import messagebox as mb
import os
import json
import docx
from keras_preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
import shutil
import threading
from tkinter import *
from tkinter import filedialog
from keras.models import load_model
from keras.engine.base_layer_v1 import *
check_pin = False
language = "eng"
IMG_SIZE = 160 # All images will be resized to 160x160

def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


def classificate_texts(input,output):
    for folder in ["Books","Labs"]:
        dir = os.path.join(output,folder)
        if not os.path.exists(dir):
            os.mkdir(dir)
    infoLabel["text"] = "info: " + "Loading model "
    text_model = load_model('best_model_gru.h5')
    num_words = 1000
    # Максимальная длина новости
    max_news_len = 50
    # Количество классов новостей
    nb_classes = 2
    tokenizer = ""
    infoLabel["text"] = "info: " + "Loading tokenizer "
    with open('tokenizer.json') as f:
        data = json.load(f)
        tokenizer = tokenizer_from_json(data)
    infoLabel["text"] = "info: " + "Loading input files "
    i=1
    for file in input:
        file_name, file_extension = os.path.splitext(file)
        if(file_extension==".docx"):
            infoLabel["text"] = "info: " + "File: " + str(i)
            i = i + 1
            text = getText(file)
            sequences = tokenizer.texts_to_sequences([text])
            x_predict = pad_sequences(sequences, maxlen=max_news_len)
            prediction = text_model.predict(np.array(x_predict))
            if abs(prediction[0][0]) >= 0.5:
                shutil.copy(file, os.path.join(output, "Books"))
            elif prediction[0][0] < 0.5:
                shutil.copy(file, os.path.join(output, "Labs"))
    classify_button["state"] = "normal"
    infoLabel["text"] = "info: " + "Done "
    mb.showinfo('confirmation', "Классификация завершена")

# open file function
def open_file():
    files = [listbox_widget.get(i) for i in listbox_widget.curselection()]
    print(files)
    for file in files:
        path = os.path.join(CurFolder["text"], file)
        try:
            os.startfile(path)
        except:
            mb.showinfo('confirmation', "Файл " + file + " не получилось запустить")


# copy file function
def copy_file():
    destination1 = filedialog.askdirectory(title="Укажите папку в которую нужно скопировать файлы")
    files = [listbox_widget.get(i) for i in listbox_widget.curselection()]
    print(files)
    for file in files:
        path = os.path.join(CurFolder["text"], file)
        try:
            shutil.copy(path, destination1)
        except:
            mb.showinfo('confirmation', "Файл " + file + " не получилось скопировать")

    mb.showinfo('confirmation', "Копирование завершено !")


# delete file function
def delete_file():
    files = [listbox_widget.get(i) for i in listbox_widget.curselection()]
    print(files)
    for file in files:
        path = os.path.join(CurFolder["text"], file)
        try:
            os.remove(path)
        except:
            mb.showinfo('confirmation', "Файл " + file + " не получилось удалить")

    mb.showinfo('confirmation', "Удаление завершено !")
    folderList = CurFolder["text"]
    sortlist = sorted(os.listdir(folderList))
    listbox_widget.delete(0, END)
    for i in range(len(sortlist)):
        listbox_widget.insert(END, sortlist[i])
    CurFolder["text"] = folderList


# move file function
def move_file():
    destination1 = filedialog.askdirectory(title="Укажите папку в которую нужно переместить файлы")
    files = [listbox_widget.get(i) for i in listbox_widget.curselection()]
    print(files)
    for file in files:
        path = os.path.join(CurFolder["text"], file)
        try:
            shutil.move(path, destination1)
        except:
            mb.showinfo('confirmation', "Файл " + file + " не получилось переместить")

    mb.showinfo('confirmation', "перемещение завершено !")
    folderList = CurFolder["text"]
    sortlist = sorted(os.listdir(folderList))
    listbox_widget.delete(0, END)
    for i in range(len(sortlist)):
        listbox_widget.insert(END, sortlist[i])
    CurFolder["text"] = folderList


# function to list all the files in folder
def list_files():
    folderList = filedialog.askdirectory()
    sortlist = sorted(os.listdir(folderList))
    listbox_widget.delete(0, END)
    for i in range(len(sortlist)):
        listbox_widget.insert(END, sortlist[i])
    CurFolder["text"] = folderList


#NN classificator
def classify_files():
    OUTPUT_FOLDER = filedialog.askdirectory(title="Укажите папку где будет сохранен результат")
    INPUT_FILES = []
    files = [listbox_widget.get(i) for i in listbox_widget.curselection()]
    print(files)
    for file in files:
        path = os.path.join(CurFolder["text"], file)
        INPUT_FILES.append(path)
    if INPUT_FILES != [] and OUTPUT_FOLDER != "":
        process = threading.Thread(target=classificate_texts, args=[INPUT_FILES, OUTPUT_FOLDER])
        process.start()
        classify_button["state"] = "disabled"
    else:
        infoLabel["text"] = "info: " + "no directory selected"

def ConvertToNN(p):
    pass

root = Tk()
root.title("Smart_file_manager")
LeftFrame = Frame(root)
LeftFrame.grid(row = 0,column = 0)
RightFrame = Frame(root)
RightFrame.grid(row = 0,column = 1)

# creating label and buttons to perform operations
Label(LeftFrame, text="File Manager", font=("Helvetica", 16), fg="blue").pack()
Button(LeftFrame, text = "Запустить выделенные файлы", command = open_file).pack()
Button(LeftFrame, text = "Скопировать выделенные файлы", command = copy_file).pack()
Button(LeftFrame, text = "Удалить выделенные файлы", command = delete_file).pack()
Button(LeftFrame, text = "Переместить выделенные файлы", command = move_file).pack()
Button(LeftFrame, text = "Выбрать новую директорию для работы", command = list_files).pack()
classify_button = Button(LeftFrame, text = "Запуск классификации по выделенным файлам", command = classify_files)
classify_button.pack()
infoLabel = Label(LeftFrame, text="Info:", font=("Helvetica", 9))
infoLabel.pack()

CurFolder = Label(RightFrame, text="", font=("Helvetica", 7))
CurFolder.pack()
listbox_widget = Listbox(RightFrame,width=120,height=40,selectmode=EXTENDED)
listbox_widget.pack()
root.iconbitmap('icon.ico')
root.mainloop()