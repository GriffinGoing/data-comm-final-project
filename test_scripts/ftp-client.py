from ftplib import FTP
import sys

# REQUIRE PYTHON 3
def requireVersion():
    if (sys.version_info[0] != 3):
        print("This script requires Python version 3.x")
        sys.exit(1)

'''
ACTION PROMPT / MAIN MENU

This method displays the main menu only AFTER the user has made a connection to an FTP server.
Options are presented as numeric input choices, with the user selecting by number. Generally,
more information is needed for the operation and thus a prompt follows. Is called after
an operation, after connection, and if ghe user's input was invalid. 
'''

def mainMenu():
    userChoice = 0
    choices = ['1', '2', '3', '4', '5']
    while (userChoice not in choices):
        # print menu
        print("    MAIN MENU    ")
        print("-----------------")
        print("Enter the number of an action below...")
        print("1. LIST")
        print("2. CWD")
        print("3. UPLOAD")
        print("4. DOWNLOAD")
        print("5. QUIT")

        # get user input
        userChoice = input()

        # validate selection
        if (userChoice not in choices):
            print("That is not a valid choice. Returning to menu...")

    return userChoice

'''
UPLOAD FILE

This is the method for file upload. After being prompted for the name of the
file to upload, it sends the FTP server the necessary data for upload (binary).
'''
def uploadFile(ftp):
    print("Enter the file to upload: ")
    filename = input()
    try:
        ftp.storbinary('STOR ' + filename, open(filename, 'rb'))
    except:
        print("Could not upload file '" + filename + "'. Returning to menu...")

'''
DOWNLOAD FILE

Method for downloading a file. After giving the name of the file to download,
a new file of the same name is opened on the client device, and the file data is
written to that file, which is promptly closed. 
'''
def downloadFile(ftp):
    print("Enter the file to download")
    filename = input()  # replace with your file in the directory ('directory_name')
    try:
        localfile = open(filename, 'wb')
        ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
        localfile.close()
    except:
        print("Could not download file '" + filename + "'. Returning to menu...")


'''
CONNECT PROMPT AND CONNECT

Prompts the user for the URI, PORT, and USERNAME/PASSWORD credentials
for the FTP server to connect to. If the connection fails, program closes.
'''
def connect(ftp):
    print("Enter the URI and PORT to connect to below: ")
    print("URI: ")
    URI = input()
    print("PORT: ")
    try:
        PORT = int(input())
    except:
        print("Invalid Port. Exiting...")
        sys.exit(1)
    print("USERNAME: ")
    USERNAME = input()
    print("PASSWORD: ")
    PASSWORD = input()
    try:
        ftp.connect(URI, PORT)
        ftp.login(user=USERNAME, passwd=PASSWORD)
    except:
        print("Connection failed. Closing...")
        return 0 # return 0 on failure

    return 1 #return 1 if succesful


'''
CWD

Command to change working direcory of the file server. 
If the desired change is not possible, communicates and returns to menu.
'''
def changeWorkingDirectory(ftp):
    print("Enter the directory to change to: ")
    directory = input()
    try:
        ftp.cwd(directory)
    except:
        print("Could not change to directory '" + directory + "'. Returning to menu...")

'''
LIST

Lists the files and directories in the current working directory.
'''
def listFiles(ftp):
    ftp.retrlines('LIST')

'''
MAIN FUNCTION

Contains the composed logic for the script itself, comprised of
above functions and branch logic. 
'''
def main():

    requireVersion()

    ftp = FTP('')

    userChoice = connect(ftp)

    while (userChoice != 5 and userChoice != 0):
      userChoice = int(mainMenu())

      if (userChoice == 1):
        listFiles(ftp)

        # if user indiciates to change the current directory
      elif (userChoice == 2):
        changeWorkingDirectory(ftp)

      elif (userChoice == 3):
        uploadFile(ftp)

      elif (userChoice == 4):
        downloadFile(ftp)

      elif (userChoice == 5):
        ftp.quit()


# execute main when run
if __name__ == "__main__":
    main()
