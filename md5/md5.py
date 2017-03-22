import hashlib
import urllib2
import requests
import os

url = 'https://notepad-plus-plus.org/repository/7.x/7.3.3/npp.7.3.3.Installer.x64.exe'
compareWithMD5 = '875074bb372eb06cdfe898387febf3d8'
def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()
    
def download1_file(url): #no status bar  
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream = True)
    print r.status_code
    with open (local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)
    return local_filename

def download2_file(url):    #with status bar
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,
    f.close()
    return file_name

print "start"
local_filename = download2_file(url)
print "..."
print "done #1"
print "MD5checking download " ,local_filename
md5sum = md5Checksum(local_filename)
print "MD5 is %s", md5sum
print "done #2"
if compareWithMD5 == md5sum:
    print 'MD5 EQUAL'
else:
    print 'MD5 check FAILED !!!'
try:
    os.remove(local_filename)
except:
    print "no data to delete!"
#print('The MD5 checksum of text.txt is', md5Checksum('1.txt'))
