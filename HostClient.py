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
        self.ftp.connect(URI, int(PORT))
        self.ftp.login(user=USERNAME, passwd="")

