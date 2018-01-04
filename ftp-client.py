from ftplib import FTP

ftp = FTP('')
ftp.connect('localhost',1026)
ftp.login()
ftp.cwd('') # Colocar o diretório aqui
ftp.retrlines('LIST')


def listFile():
    files = []
    try:
        files = ftp.nlst()
    except (ftplib.error_perm, resp):
        if str(resp) == "550 No files found":
            print ("No files in this directory")
        else:
            raise

    for f in files:
        print (f)

def grabFile():
    filename = 'testfile.txt' 
    localfile = open(filename, 'wb')
    ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
    ftp.quit()
    localfile.close()


def placeFile():
    filename = 'testfile.txt'
    ftp.storbinary('STOR '+filename, open(filename, 'rb'))
    ftp.quit()

def changeDirectory(directory):
    ftp.cwd(directory)
    ftp.retrlines('LIST')
