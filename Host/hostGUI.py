import sys
import os
import csv
from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
from tkintertable import TableCanvas, TableModel
import subprocess
import runpy
from threading import Thread
sys.path.append('..')
import hostFTPServer
from HostClient import *


# REQUIRE PYTHON 3
def requireVersion():
    if (sys.version_info[0] != 3):
        print("This script requires Python version 3.x")
        sys.exit(1)

def runServer():
    requireVersion()
    '''
    a few different methods to run the subprocess. not worth running it separately,
    hence the basic function call.
    '''
    #runpy.run_module(mod_name = 'server') # this doesn't listen properly, and doesn't offer logging. below works for gnome terms
    #os.system("gnome-terminal -x python server.py")
    #subprocess.run(["python", "server.py"], )
    hostFTPServer.main()


class hostGUI:
    def __init__(self):

        '''
        The host's FTP client instance
        '''
        self.client = HostClient()

        '''
        Assemble the GUI
        '''

        self.top = Tk()
        self.top.title("GV-Napster Host")
        self.top.protocol("WM_DELETE_WINDOW", self.onClose)
        #self.top.geometry("700x1200")

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

        self.connectButton = Button(self.connectionLabelFrame, text="Connect", command=self.connect)

        self.searchKeywordFrame = Frame(self.searchLabelFrame)
        self.keywordLabel = Label(self.searchKeywordFrame, text="Keyword:")
        self.keywordLabel.grid(row=0, column=0)
        self.keywordText = Entry(self.searchKeywordFrame)
        self.keywordText.grid(row=0, column=1)
        self.searchButton = Button(self.searchKeywordFrame, text="Search", command=self.search)
        self.searchButton.grid(row=0, column=2)
        self.updateFileIndexButton = Button(self.searchKeywordFrame, text="Update File Index", command=self.updateFileIndex)
        self.updateFileIndexButton.grid(row=0, column=3)


        # working on a table, just a placeholder
        self.searchFrame = Frame(self.searchLabelFrame)
        self.searchTable = TableCanvas(self.searchFrame)
        self.searchTable.importCSV("files.csv")
        #self.searchTable = Text(self.searchLabelFrame, height=7)

        self.enterCommandFrame = Frame(self.FTPLabelFrame)
        self.enterCommandLabel = Label(self.enterCommandFrame, text="Enter Command:")
        self.enterCommandLabel.grid(row=0, column=0)
        self.enterCommandText = Entry(self.enterCommandFrame)
        self.enterCommandText.grid(row=0, column=1)
        self.enterCommandButton = Button(self.enterCommandFrame, text="Go", command=self.runFTPCommand)
        self.enterCommandButton.grid(row=0, column=2)

        # needs format specifics but will work
        self.commandTextOutput = Text(self.FTPLabelFrame, height=7)

        '''
        pack all frames in proper order (top to bottom)
        '''
        self.connectionInputs.pack()
        self.speedLabel.pack(side=LEFT)
        self.speedMenu.pack(side=RIGHT)
        self.speedFrame.pack()
        self.connectButton.pack(side=BOTTOM)
        self.searchFrame.pack()
        self.searchTable.show()
        self.searchKeywordFrame.pack()
        #self.searchTable.pack()
        self.enterCommandFrame.pack()
        self.commandTextOutput.pack()

    def connect(self):
        serverHostname = self.serverHostnameText.get()
        port = self.portText.get()
        username = self.userNameText.get()
        hostname = self.hostnameText.get()
        #speed = self.speedMenu.get()
        print("Connecting to " + serverHostname + ":" + port + " as " + username + " from " + hostname + " at speed <later>...")
        connectionResult = self.client.connect(serverHostname, port, username)
        if (connectionResult == 1):
            messagebox.showerror(title="Server Connection", message="Connection Refused")
            return
        if (connectionResult == 2):
            messagebox.showerror(title="Server Authentication", message="Authentication Failed")
        else:
            print("Connected...")
            self.updateFileIndex()


    def search(self):
        print("SEARCH FUNCTION CODE STANDIN")

    def runFTPCommand(self):
        print("Run FTP Command stand-in")

    def updateFileIndex(self):
        print("Updating file index...")
        self.client.fetchFileIndex()
        self.searchTable.importCSV("files.csv")
        self.searchTable.redraw()
        print("File index updated...")

    def resetFileIndex(self):
        with open('files.csv', 'w', newline='') as files:
            fieldnames = ['FILENAME', 'DESCRIPTION', 'LOCATION']
            writer = csv.DictWriter(files, fieldnames=fieldnames)

            writer.writeheader()

    def onClose(self):
        print("Resetting file index and quitting...")
        self.resetFileIndex()
        self.top.destroy()
        sys.exit(0)




def main():
    gui = hostGUI()
    gui.top.mainloop()

if __name__ == '__main__':
    try:
        '''
        Start an FTP server on this machine
        Try to get this running as a thread UNDER the GUI itself to give the GUI control over it 
        '''
        # ONLY COMMENTED OUT BECAUSE RUNNING THIS ON THE SAME MACHINE AS THE CENTRAL SERVER IS ASS
        Thread(target = runServer).start()

        '''
        Start the host GUI (and therefore client) on this machine
        '''
        Thread(target = main).start()
    except:
        exit(0)