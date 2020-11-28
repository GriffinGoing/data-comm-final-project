import sys
import os
import tkinter
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
        self.top = tkinter.Tk()
        self.top.title("GV-Napster Host")


def main():
    gui = hostGUI()
    gui.top.mainloop()

if __name__ == '__main__':
    Thread(target = runServer).start()
    Thread(target = main).start()