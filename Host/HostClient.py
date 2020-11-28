from ftplib import FTP
import sys

# REQUIRE PYTHON 3
def requireVersion():
    if (sys.version_info[0] != 3):
        print("This script requires Python version 3.x")
        sys.exit(1)

class HostClient:
    def __init__(self):
        self.ftp = FTP('')

    def connect(self, URI, PORT, USERNAME):
        try:
            self.ftp.connect(URI, int(PORT))
        except:
            return(1) # connection refused

        try:
            self.ftp.login(user=USERNAME, passwd="")
        except:
            return(2) # auth failure

        return(0) # all good, connection established


    def fetchFileIndex(self):
        filename = "files.csv"
        localfile = open(filename, 'wb')
        self.ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
        localfile.close()

