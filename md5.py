import hashlib

import requests
import os

# url = 'https://notepad-plus-plus.org/repository/7.x/7.3.3/npp.7.3.3.Installer.x64.exe'
# compareWithMD5 = '875074bb372eb06cdfe898387febf3d8'

# hash_FLAG table:
# MD5 = 0
# SHA1 = 1
# SHA256 = 2
# SHA384 = 3
# SHA512 = 4

class HASH(object):
    def __init__(self):
        self.url = ''
        self.compWithhash = ''
        self.downloaded_file = ''
        self.site_status_code = -1
        self.hash_flag = -6
        self.path2file = os.path.dirname(__file__)

    def __hashChecksum(self, fileName):
        with open(self.path2file + fileName , 'rb') as fh:
            if self.hash_flag == 0:
                m = hashlib.md5()
            elif self.hash_flag == 1:
                m = hashlib.sh1()
            elif self.hash_flag == 2:
                m = hashlib.sha256()
            elif self.hash_flag == 3:
                m = hashlib.sha384()
            elif self.hash_flag == 4:
                m = hashlib.sha512()
            else:
                print "ERROR! wrong hash algorithm!"
            while True:
                data = fh.read(8192)
                if not data:
                    break
                m.update(data)
            return m.hexdigest()

    def __download1_file(self, urls):  # no status bar  (fast)
        local_filename = urls.split('/')[-1]
        print "downloading file ..."
        r = requests.get(urls, stream=True)
        self.site_status_code = r.status_code
        print "site status code ", self.site_status_code
        directory = os.path.dirname(__file__)
        with open(os.path.join(directory + '/md5', local_filename), 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
        self.path2file = directory + '/md5/'
        self.downloaded_file = local_filename
        r.close()
        print "download finished!"

    def download2_file(self, urls):  # with status bar (slow)
        file_name = urls.split('/')[-1]
        u = urllib2.urlopen(urls)
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
            status = status + chr(8) * (len(status) + 1)
            print status,
        f.close()
        return file_name

    def hashFromURL(self, urls):
        if self.hash_flag == -6:
            print "ERROR! no flag set"
            return "ERROR! no flag set"
        try:
            print "starting download..."
            self.__download1_file(urls)
        except:
            print "FEHLER beim Runterladen"
            return "wrong url"
        print "now hashing"
        hashed = self.__hashChecksum(self.downloaded_file)
        try:
            os.remove(self.path2file + self.downloaded_file)
            print "download data deleted"
        except:
            print "no download data to delete!"
        print "hash done! = ", hashed
        return hashed

    #print "welcome to MD5"




# print('The MD5 checksum of text.txt is', md5Checksum('1.txt'))
