from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import csv

'''
HOSTS ACCESS EACH OTHER, BUT ONLY FOR DOWNLOADS, THIS SERVER IS ONLY THE MIDDLEMAN FOR P2P FILESHARING. IE, THIS SERVER ONLY MAINTAINS A DB OF FILENAMES AND DESCRIPTIONS, BUT
DOES NOT DO ANY MORE THAN TELL THE HOST WHAT FILES ARE AND WHERE TO FIND THEM (ON WHICH HOST)
'''

# The port the FTP server will listen on.
# This must be greater than 1023 unless you run this script as root.
FTP_PORT = 2121

'''
NOT WORRIED ABOUT AUTHENTICATING THIS SERVER, DOESN'T SEEM MAJOR IN THE SCOPE OF THE PROJECT.
IT'S JUST A CENTRAL "WHO HAS WHAT" SO. 
'''

# The name of the FTP user that can log in.
FTP_USER = "myuser"

# The FTP user's password.
FTP_PASSWORD = "change_this_password"

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
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions.
    authorizer.add_user(FTP_USER, FTP_PASSWORD, FTP_DIRECTORY, perm='elradfmw')

    handler = FTPHandler
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
