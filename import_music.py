import tkinter
from tkinter import filedialog

def import_music():
    root = tkinter.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    return folder_path