from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from threading import Thread
import csv
import sys

# REQUIRE PYTHON 3
def requireVersion():
    if (sys.version_info[0] != 3):
        print("This script requires Python version 3.x")
        sys.exit(1)


'''
HOSTS ACCESS EACH OTHER, BUT ONLY FOR DOWNLOADS, THIS SERVER IS ONLY THE MIDDLEMAN FOR P2P FILESHARING. IE, THIS SERVER ONLY MAINTAINS A DB OF FILENAMES AND DESCRIPTIONS, BUT
DOES NOT DO ANY MORE THAN TELL THE HOST WHAT FILES ARE AND WHERE TO FIND THEM (ON WHICH HOST)
'''


'''
Add handlers for addUser and removeUser to log users as they come and go 
'''
proto_cmds = FTPHandler.proto_cmds.copy()
proto_cmds.update(
    {'SITE ADDUSER': dict(perm='', auth=True, arg=True,
      help='Syntax: SITE <SP> ADDUSER <USERNAME>')}
)

class CustomizedFTPHandler(FTPHandler):
    proto_cmds = proto_cmds

    def ftp_SITE_ADDUSER(self, username):
        # add a user
        self.authorizer.add_user(username, '', '.', perm='r')
        print("User [" + username + "] added")
        self.respond("100: Added" + username + "as a user.")


# The port the FTP server will listen on.
# This must be greater than 1023 unless you run this script as root.
FTP_PORT = 2121

'''
NOT WORRIED ABOUT AUTHENTICATING THIS SERVER, DOESN'T SEEM MAJOR IN THE SCOPE OF THE PROJECT.
IT'S JUST A CENTRAL "WHO HAS WHAT" SO. 
'''

# The name of the FTP user that can log in.
FTP_USER = "user"

# The FTP user's password.
FTP_PASSWORD = ""

# The directory the FTP user will have full read/write access to.
# This directory holds the file that operates as the filename directory/database, ie
# what files are, and where they are. 
FTP_DIRECTORY = "."


'''
CONNECTION DATA:
WE CAN KEEP A PRE-BUILT LIST OF FILES/DESCRIPTIONS, BUT THAT REQUIRES LOGGING IN THE
IMPORTED DATASET WHICH HOSTS ARE LOGGED IN/CAN BE DOWNLOADED FROM
'''

'''
TO DO: FILE CONTAINING FILENAMES AND DESCRIPTIONS
'''

# Load the .csv file containing file names and descriptions
files = {}
i = 0
with open('files.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        print(row) # print the array at that row
        #print(row[0]) # print filename of that row
        #print(row[0],row[1],row[2],) # print filename, description, and path of row
        files[i] = row
        i = i + 1

print("Current Number of Files: " + str(i))
#print(files)
#print(readCSV)

'''
TO DO: A TABLE MAPPING FILENAMES TO HOSTS
'''


def main():

    requireVersion()

    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions.
    authorizer.add_user(FTP_USER, FTP_PASSWORD, FTP_DIRECTORY, perm='r')

    handler = CustomizedFTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Optionally specify range of ports to use for passive connections.
    #handler.passive_ports = range(60000, 65535)

    address = ('', FTP_PORT)
    server = FTPServer(address, handler)

    server.max_cons = 256
    server.max_cons_per_ip = 5

    # ASCII art by some guy named 'das'
    print('''

457 PURPLE TEAM GV-NAPSTER SERVER
---------------------------------
 ___________________________    -
|[]                        []|  -
|[]                        []|  -
|                            |  -
|            . .             |  -
|          `    _`           |  -
|         `  ()|_|`          |  -
|         `       `          |  -
|          ` . . `           |  -
|      ________________      |  -
|     |          ____  |     |  -
|     |         |    | |     |  -
|     |         |    | |     |  -
|     |         |    | |     |  -
|()   |         |_  _| |   ()|  -
|)    |           --   |    (|  -
|_____|[]______________|\___/   -
                                -
---------------------------------

Logging users...

    ''')

    server.serve_forever()


if __name__ == '__main__':
    main()
