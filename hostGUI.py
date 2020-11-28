import sys
import os
from tkinter import *
import subprocess
import runpy
from threading import Thread
sys.path.append('..')
#from server import server



# REQUIRE PYTHON 3
def requireVersion():
    if (sys.version_info[0] != 3):
        print("This script requires Python version 3.x")
        sys.exit(1)

def runServer():
    requireVersion()
    runpy.run_module(mod_name = 'server')


class hostGUI:
    def __init__(self):
        self.top = Tk()
        self.top.title("GV-Napster Host")

        self.connectionLabelFrame = LabelFrame(self.top, text = "Connection")
        self.connectionLabelFrame.pack(fill="both", expand="yes")
        self.searchLabelFrame = LabelFrame(self.top, text = "Search")
        self.searchLabelFrame.pack(fill="both", expand="yes")
        self.FTPLabelFrame = LabelFrame(self.top, text = "FTP")
        self.FTPLabelFrame.pack(fill="both", expand="yes")

        self.left = Label(self.connectionLabelFrame, text="Inside the LabelFrame")
        self.left.pack()

        self.left = Label(self.searchLabelFrame, text="Inside the LabelFrame")
        self.left.pack()

        self.left = Label(self.FTPLabelFrame, text="Inside the LabelFrame")
        self.left.pack()


def main():
    gui = hostGUI()
    gui.top.mainloop()

if __name__ == '__main__':
    Thread(target = runServer).start()
    Thread(target = main).start()