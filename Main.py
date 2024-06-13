from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
import matplotlib.pyplot as plt
import numpy as np
from tkinter import ttk
from tkinter import filedialog
import os
import cv2
import timeit
import multiprocessing

main = Tk()
main.title("Green: Green Approximate Computing for Next Generation Sustainability")
main.geometry("1300x1200")

global filename, normal_times, onx_times, text


def uploadImages(): 
    global filename # Access the global variable 'filename'
    filename = filedialog.askdirectory(initialdir=".")# Open a file dialog to select a directory
    text.delete('1.0', END)  # Delete any existing text in the text widget
    text.insert(END, filename + " loaded\n\n")  # Insert a message indicating the selected directory was loaded
    size = len(os.listdir(filename)) # Get the number of files in the selected directory
    text.insert(END,f"Total images to process = {size}\n")# Insert the total number of files message to the text widget

def normalProcess(num_iterations=1):
    global filename, normal_times
    text.delete('1.0', END)
    normal_times = []  # List to store processing times for each iteration

    for _ in range(num_iterations):
        start = timeit.default_timer()
        for root, dirs, directory in os.walk(filename):
            for j in range(len(directory)):
                for k in range(0, 5):
                    name = directory[j]
                    img = cv2.imread(root + "/" + directory[j])
                    resized_image = cv2.resize(img, (100, 100))
        end = timeit.default_timer()
        processing_time = end - start
        normal_times.append(processing_time)  # Store processing time for this iteration

    text.insert(END, f"Processing times for each iteration (Normal Process):\n")
    for i, time in enumerate(normal_times):
        text.insert(END, f"Iteration {i + 1} processing time: {time:.4f} seconds\n")

    plotLinearGraph(normal_times, "Normal Process")



def resize_image(image):
     resized_image = cv2.resize(image, (100, 100))
     return resized_image

def batchProcessing():
       global filename
       pool = multiprocessing.Pool(1)
       resized_images = pool.map(resize_image, [cv2.imread("testImages1/"+image_path) for image_path in os.listdir(filename)])


def ONXProcess(num_iterations=1):
    global filename, onx_times
    text.delete('1.0', END)
    onx_times = []  # List to store processing times for each iteration
    
    for _ in range(num_iterations):
        start = timeit.default_timer()
        batchProcessing()
        end = timeit.default_timer()
        processing_time = end - start
        onx_times.append(processing_time)  # Store processing time for this iteration
    
    text.insert(END, f"Processing times for each iteration (ONX Process):\n")
    for i, time in enumerate(onx_times):
        text.insert(END, f"Iteration {i + 1} processing time: {time:.4f} seconds\n")

    plotLinearGraph(onx_times, "ONX Process")

def plotLinearGraph(times, technique):
    plt.figure(figsize=(8, 6))
   # plt.plot( normal_times, marker='o', linestyle='-', color='b', label='Normal Process')
    plt.plot(range(1, len(times) + 1), times, marker='o', linestyle='-', color='b')
    plt.xlabel("Iteration")
    plt.ylabel("Processing Time (seconds)")
    plt.title(f"{technique} Linear Processing Time")
    plt.grid(True)
    plt.show()

def plotComparisonGraph():
    global normal_times, onx_times
    plt.figure(figsize=(8, 6))
    plt.plot(range(1, len(normal_times) + 1), normal_times, marker='o', linestyle='-', color='b', label='Normal Process')
    plt.plot(range(1, len(onx_times) + 1), onx_times, marker='o', linestyle='-', color='r', label='ONX Process')
    plt.xlabel("Iteration")
    plt.ylabel("Processing Time (seconds)")
    plt.title("Comparison of Normal Process vs ONX Process")
    plt.legend()
    plt.grid(True)
    plt.show()

def close():
    main.destroy()

def gui():
    global main, text
    font = ('times', 15, 'bold')
    title = Label(main, text='Green: Green Approximate Computing for Next Generation Sustainability')
    title.config(bg='darkviolet', fg='gold')  
    title.config(font=font)           
    title.config(height=3, width=120)       
    title.place(x=0,y=5)

    font1 = ('times', 13, 'bold')
    ff = ('times', 12, 'bold')

    uploadButton = Button(main, text="Upload Image Data", command=uploadImages)
    uploadButton.place(x=20,y=100)
    uploadButton.config(font=ff)

    normalButton = Button(main, text="Image Processing using Normal Technique", command=lambda: normalProcess(3))
    normalButton.place(x=20,y=150)
    normalButton.config(font=ff)

    onxButton = Button(main, text="Image Processing using ONX Batch", command=lambda: ONXProcess(3))
    onxButton.place(x=20,y=200)
    onxButton.config(font=ff)

    graphButton = Button(main, text="Comparison Graph", command=plotComparisonGraph)
    graphButton.place(x=20,y=250)
    graphButton.config(font=ff)

    closeButton = Button(main, text="Exit", command=close)
    closeButton.place(x=20,y=300)
    closeButton.config(font=ff)

    font1 = ('times', 12, 'bold')
    text=Text(main,height=30,width=110)
    scroll=Scrollbar(text)
    text.configure(yscrollcommand=scroll.set)
    text.place(x=360,y=100)
    text.config(font=font1)

    main.config(bg='forestgreen')
    main.mainloop()

if __name__ == "__main__":
    gui()
