# File created on 10:46 am. 10/12/2018
# Author: Xinchen Zhang

import tkinter
import tkinter.ttk as ttk
from tkinter import messagebox

import protocol
import using_thread


class UserInterface:
    def __init__(self):
        self.connection= Connection()
        self.status= self.connection.get_status()

        #initialize server directory
        self._server_dir= list()

    def run(self):
        # Draw widgets
        self._place_root_window()
        self._draw_notebook()
        self._draw_frame1()
        self._draw_frame2()
        self._draw_statusLabel()

        self.root.mainloop()

    def _place_root_window(self):
        self.root= tkinter.Tk()
        self.root.geometry('300x350-250+50')
        self.root.resizable(0, 0)
        self.root.title('FileSpinner')

        self.root.columnconfigure(0, weight= 1)
        self.root.rowconfigure(0, weight= 1)

    def _draw_notebook(self):
        # Draw the notebook
        self.notebook= ttk.Notebook(self.root)
        
        self.notebook.columnconfigure(0, weight= 1)
         
        self.frame1= ttk.Frame(self.notebook)
        self.frame2= ttk.Frame(self.notebook)
        
        # Expand the widgets in tabs
        self.frame1.columnconfigure(0, weight= 1)

        self.frame2.columnconfigure(1, weight= 1)
        self.frame2.rowconfigure(0, weight= 1)
        
        # Adding tabs to notebook
        self.notebook.add(self.frame1)
        self.notebook.add(self.frame2)

        self.notebook.tab(0, text= 'Connection', sticky= tkinter.W+ tkinter.E+\
                          tkinter.N+ tkinter.S)
        self.notebook.tab(1, text= 'Server file list', sticky= tkinter.W+ \
                          tkinter.E+ tkinter.N+ tkinter.S)
   
        # Position the notebook
        self.notebook.grid(row= 0, sticky= tkinter.W+ tkinter.E+ tkinter.N+\
                           tkinter.S)

    def _draw_frame1(self):
        # First labelFrame
        labelFrame1= ttk.LabelFrame(self.frame1, text=\
                                    'Connect to a local FTP server')
        labelFrame1.grid(row= 0, column= 0, sticky=\
                         tkinter.W+ tkinter.E+ tkinter.S, pady= (10, 0))
        
        # === START Centering the widgets in labelFrame1 === #
        labelFrame1.columnconfigure(0, weight= 1)

        temp_label= tkinter.Label(labelFrame1)
        temp_label.grid()

        # === END === #

        label1= ttk.Label(temp_label, text= 'FTP Server IP:')
        label1.grid(row= 0, column= 0, pady= (10, 0))

        label2= ttk.Label(temp_label, text= '192.168.1.')
        label2.grid(row= 0, column= 1, pady= (10, 0))

        self.entry1_str= tkinter.StringVar()
        entry1= ttk.Entry(temp_label, width= 3, textvariable=\
                          self.entry1_str)
        entry1.grid(row= 0, column= 2, pady= (10, 0))
        
        self.button1_str= tkinter.StringVar()
        button1= ttk.Button(temp_label,textvariable=\
                            self.button1_str, command= self._connect)
        self.button1_str.set('Connect')
        button1.grid(row= 1, column= 0, sticky= tkinter.W+\
                     tkinter.E, columnspan= 3, pady= (10, 10))

        # Second labelFrame
        labelFrame2= ttk.LabelFrame(self.frame1, text=\
                                    'Hosting a FTP server')
        labelFrame2.grid(row= 1, column= 0, sticky=\
                         tkinter.W+ tkinter.E, pady= (10, 0))

        # === START Centering the widgets in labelFrame2 === #
        labelFrame2.columnconfigure(0, weight= 1)

        temp_label2= tkinter.Label(labelFrame2)
        temp_label2.grid()

        # === END === #

        label3= ttk.Label(temp_label2, text= 'Current IP:', width= 10)
        label3.grid(row= 0, column=0, sticky= tkinter.W, pady= (10, 0))

        label4= ttk.Label(temp_label2, text= self.connection.get_self_ip())
        label4.grid(row= 0, column= 1, sticky= tkinter.W, pady= (10, 0))

        label5= ttk.Label(temp_label2, text= '', width= 3)
        label5.grid(row= 0, column= 2, pady= (10, 0))

        button2= ttk.Button(temp_label2, text= 'Start')
        button2.grid(row= 1, column= 0, columnspan= 3, sticky=\
                     tkinter.W+ tkinter.E, pady= (10, 10))

    def _draw_frame2(self):
        self.listbox1= tkinter.Listbox(self.frame2)
        self.listbox1.grid(row= 0, column= 0, columnspan= 2, \
                           sticky= tkinter.W+ tkinter.E+ \
                           tkinter.N+ tkinter.S)
        
        self.listbox1.bind('<Double-Button-1>', self._listbox1_dbclick)

        button1= ttk.Button(self.frame2, text= 'Refresh', command= \
                            lambda: self._insert_file_list(
                                self.connection.get_file_list()))
        button1.grid(row= 1, column= 1, sticky= tkinter.W+ tkinter.E)

        button1= ttk.Button(self.frame2, text= 'Back', command= \
                            self._rollback_file_list)
        button1.grid(row= 1, column= 0, sticky= tkinter.W+ tkinter.E)

 
    def _draw_statusLabel(self):
        self.statusLabel= ttk.Label(self.root, text= '')
        self.statusLabel.grid(row= 3, column= 0, sticky= tkinter.W)

    def _change_button1_textvar(self, status: str):
        if status== 'WAITING':
            self.button1_str.set('Connecting...')
        elif status== 'FAIL':
            self.button1_str.set('Connect')
        elif status== 'SUCCESS':
            self.button1_str.set('Disconnect')

    def _insert_file_list(self, file_list):   
        if self.status!= 'SUCCESS':
            messagebox.showinfo('Error', 'Please connect to a FTP server first')

        else:
            self.listbox1.delete(0, tkinter.END)

            for file in file_list:
                self.listbox1.insert(tkinter.END, file)

    def _rollback_file_list(self):
        # For the file list to go forward, the _listbox1_dbclick event is used
        self._server_dir.pop()

        self._get_into_dir()

    def _get_dir(self)-> str:
        return '/'.join(self._server_dir)

    def _get_into_dir(self):
        _dir= self._get_dir()
        
        file_list= self.connection.get_file_list(_dir)
        self._insert_file_list(file_list)

    def _retrieve_FTPServer_ip(self)-> str:
        user_input= self.entry1_str.get()

        if user_input!= '':
            return '192.168.1.'+ user_input
        
        else:
            messagebox.showinfo(
                'Error', 'Please input a valid ip address')
            return None

    def _connect(self):
        if self.button1_str.get()== 'Connect':
            ip= self._retrieve_FTPServer_ip()

            if ip is not None:
                self.connection.connect(ip)
                self.status= self.connection.get_status()
                self._change_button1_textvar(self.status)
            else:
                messagebox.showinfo(
                    'Error', 'Please input a valid ip address')
        else:
            self.connection.disconnect()
            self.button1_str.set('Connect')
                
    #Events

    def _listbox1_dbclick(self, event):
        select_dir= self.listbox1.get(tkinter.ACTIVE)
        self._server_dir.append(select_dir)

        if self.connection.is_file(select_dir):
            self.connection.open_file(self._get_dir())
            self._server_dir.pop()
        else:
            self._get_into_dir()


class Connection:
    def __init__(self):
        self.ftp= protocol.FTPProtocol()
    
    def connect(self, ip):
        '''
        self.ip_thread= using_thread.UsingThread(
            target= self.ftp.initialize, args= (self.server_ip,))

        self.ip_thread.start_thread()
        '''
      
        self.ftp.initialize(ip)

        '''
        self.ip_thread= using_thread.UsingThread()
        self.ip_thread.communicate(
            self.ftp.initialize, self.server_ip, \
            self._change_button1_textvar, None)
        '''
        '''

        self.status= self.ftp.get_status()
        print(self.status)
        self._change_button1_textvar(self.status)
        '''
    def disconnect(self):
        self.ftp.disconnect()

    def get_file_list(self, file_name= ''):
        return self.ftp.get_file_list(file_name)
        
    def get_self_ip(self)-> str:
        ip_getter= protocol.FoundLANIPAddrs()
        self_ip= ip_getter.get_selfIP()

        return self_ip

    def get_status(self)-> str:
        return self.ftp.get_status()

    def get_current_dir(self)-> str:
        return self.ftp.get_dir()

    def is_file(self, _str)-> bool:
        return self.ftp.is_file(_str)

    def open_file(self, path):
        self.ftp.open_file(path)
        
if __name__== '__main__':
    UserInterface().run()
