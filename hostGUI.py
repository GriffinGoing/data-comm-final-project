import sys
import os
from tkinter import *
import tkinter.font as tkFont
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
    #runpy.run_module(mod_name = 'server')
    os.system("gnome-terminal -x python server.py")

class hostGUI:
    def __init__(self):
        self.top = Tk()
        self.top.title("GV-Napster Host")

        self.fontStyle = tkFont.Font(root=self.top, family="Helvetica", size=20)

        self.font = tkFont.Font(family="Helvetica",size=12)

        self.top.option_add("*Font", self.font)



        self.connectionLabelFrame = LabelFrame(self.top, text = "Connection")
        self.connectionLabelFrame.pack(fill="both", expand="yes")
        self.searchLabelFrame = LabelFrame(self.top, text = "Search")
        self.searchLabelFrame.pack(fill="both", expand="yes")
        self.FTPLabelFrame = LabelFrame(self.top, text = "FTP")
        self.FTPLabelFrame.pack(fill="both", expand="yes")

        self.connectionInputs = Frame(self.connectionLabelFrame)


        self.serverHostnameLabel = Label(self.connectionInputs, text="Server Hostname:")
        self.serverHostnameLabel.grid(row=0, column=0)
        self.serverHostnameText = Entry(self.connectionInputs)
        self.serverHostnameText.grid(row=0, column=1)

        self.usernameLabel = Label(self.connectionInputs, text="Username:")
        self.usernameLabel.grid(row=1, column=0)
        self.userNameText = Entry(self.connectionInputs)
        self.userNameText.grid(row=1, column=1)

        self.portLabel = Label(self.connectionInputs, text="Port:")
        self.portLabel.grid(row=0, column=3)
        self.portText = Entry(self.connectionInputs)
        self.portText.grid(row=0, column=4)

        self.hostnameLabel = Label(self.connectionInputs, text="Hostname:")
        self.hostnameLabel.grid(row=1, column=3)
        self.hostnameText = Entry(self.connectionInputs)
        self.hostnameText.grid(row=1, column=4)

        self.speedFrame = Frame(self.connectionLabelFrame)
        self.speedLabel = Label(self.speedFrame, text="Speed:")
        self.speedSelection = StringVar(self.top)
        self.speedChoices = { 'Ethernet'}
        self.speedMenu = OptionMenu(self.speedFrame, self.speedSelection, *self.speedChoices)

        self.connectButton = Button(self.connectionLabelFrame, text="Connect")

        # to be deleted later, just placeholders
        self.left = Label(self.searchLabelFrame, text="Inside the LabelFrame")
        self.left.pack()

        self.left = Label(self.FTPLabelFrame, text="Inside the LabelFrame")
        self.left.pack()

        '''
        pack all frames in proper order (top to bottom)
        '''
        self.connectionInputs.pack()
        self.speedLabel.pack(side=LEFT)
        self.speedMenu.pack(side=RIGHT)
        self.speedFrame.pack()
        self.connectButton.pack(side=BOTTOM)


def main():
    gui = hostGUI()
    gui.top.mainloop()

if __name__ == '__main__':
    Thread(target = runServer).start()
    Thread(target = main).start()