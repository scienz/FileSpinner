# File created on 8:20 pm. 10/11/2018
# Author: Xinchen Zhang

import subprocess
import re
from ftplib import FTP

class FTPProtocol:
    def __init__(self):
        self.ftp= FTP()
        self.status= 'WAITING'
  
    def initialize(self, host_addr: str, user= 'anonymous', passwd= ''):
        try:       
            self.ftp.connect(host_addr, timeout= 3)
            self.ftp.login(user, passwd)
            
        except:
            self._fail()

        else:
            self._success()

        finally:
            return self.status

    def disconnect(self):
        self.ftp.quit()

    def download(self, file: str):
        def _save_file(data):
            f= open(file, 'wb')
            f.write(data)
        
        self.ftp.retrbinary('RETR '+ file, _save_file)

    def get_file_list(self, file_name= ''):
        def _return_data(data):
            self.file_list.append(data)
            
        try:
            self.file_list= list()
            self.ftp.retrlines('NLST '+ file_name, _return_data)
            return self.file_list
        
        except:
            self._fail()

        else:
            self._success()
        

    def get_status(self) -> str:
        return self.status

    def get_dir(self)-> str:
        return self.ftp.pwd()

    def is_file(self, _str)-> bool:
        pattern= re.compile('[.]')
        m= pattern.search(_str)

        if m!= None:
            return True
        else:
            return False

    def open_file(self, path):
        self._download_file(path)
        subprocess.run(path.split('/')[-1], shell= True)
    

    #Private functions

    def _success(self):
        self.status= 'SUCCESS'

    def _fail(self):
        self.status= 'FAIL'

    def _download_file(self, path):
        self.ftp.retrbinary(
            'RETR '+ path, open(path.split('/')[-1], 'wb').write)

class FoundLANIPAddrs:
    def get_selfIP(self)-> str:
        addrs= list()
        
        shell_output= self._get_shell_output()
        pattern= re.compile('(192[.]168[.]1[.])([1-9])([0-9])?')

        for line in shell_output.splitlines():
            m= pattern.search(line)

            if m!= None:
                addrs.append(m.group())
        
        return addrs[0]

    def _get_shell_output(self)-> str:
        self.popen= subprocess.Popen('ipconfig', shell= True, \
                                     stdout= subprocess.PIPE, stdin= subprocess.PIPE)
        out, err= self.popen.communicate()
        return out.decode(encoding= 'utf-8')


if __name__== '__main__':
    ftp= FTPProtocol()
    ftp.initialize('192.168.1.12')
    list= ftp.get_file_list()
    print(list)
    



    

    
        
