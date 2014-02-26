#! /usr/bin/env python
# coding: UTF-8
# python2.7
 
from Tkinter import *
import Tkinter as tk
import threading
import time
from socket import *
import sys
 
 
HOST = '127.0.0.1'
PORT = 8808
BUFSIZ = 1024
ADDR = (HOST, PORT)
 
 
class Application(tk.Frame):
 
    def __init__(self, master=None):
 
        tk.Frame.__init__(self, master)
        self.grid()
        self.createFrameTop()
        self.createFrameMiddle()
        self.createFrameButtom()
        self.flag = False
 
    def createFrameTop(self):
 
        self.frmTop = tk.LabelFrame(root, text='Top')
 
        self.chatText   = tk.Text(self.frmTop, height=15, width=80)
        self.chatText.tag_config('blue', foreground='blue', font=('Tempus Sans ITC',15))
        self.chatText.tag_config('red', foreground='red', font=('Tempus Sans ITC',15))
 
        self.chatScl = Scrollbar(self.frmTop)
        self.chatScl['command'] = self.chatText.yview
        self.chatText['yscrollcommand']=self.chatScl.set
 
        self.frmTop.grid(row = 0, column = 0, sticky = 'w'+'e'+'n'+'s')
        self.chatText.grid(row = 0, column = 0, sticky = 'w'+'e'+'n'+'s')
        self.chatScl.grid(row = 0, column = 1, sticky = 'w'+'e'+'n'+'s')
 
    def createFrameMiddle(self):
 
        self.frmMiddle = tk.LabelFrame(root, text='Middle')
 
        self.inputText = tk.Text(self.frmMiddle, height=8, width=80)
        self.inputText.bind("<Return>", self.sendMessage)
 
        self.inputScl = Scrollbar(self.frmMiddle)
        self.inputScl['command'] = self.inputText.yview
        self.inputText['yscrollcommand']=self.inputScl.set
 
        self.frmMiddle.grid(row = 1, column = 0, sticky = 'w'+'e'+'n'+'s')
        self.inputText.grid(row = 0, column = 0, sticky = 'w'+'e'+'n'+'s')
        self.inputScl.grid(row = 0, column = 1, sticky = 'w'+'e'+'n'+'s')
         
 
    def createFrameButtom(self):
 
        self.frmButton = tk.LabelFrame(root, text='Buttom')
 
        self.btnSend = tk.Button(self.frmButton, text='send', width=10, command=self.sendMessage)
        self.btnClose = tk.Button(self.frmButton, text='close', width=10, command=self.Close)
 
        self.frmButton.grid(row = 2, column = 0, ipadx=0, ipady=0, sticky = 'w'+'e'+'n'+'s')
        self.btnSend.grid(row = 0, column = 0, padx=50, pady=0, sticky = 'e')
        self.btnClose.grid(row = 0, column = 1, padx=150, pady=0, sticky = 'e')
 
 
    # btnSend囘調函數
    def sendMessage(self, event=None):
        # 得到用戶在Text中輸入的消息
        message = self.inputText.get('0.0', END)
        message = message.replace('\n','')
 
        # 顯示當前的時間和發送的信息  
        theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        self.chatText.insert(END, '服務器 ' + theTime +' 說：\n') 
        self.chatText.insert(END, '  ' + message + '\n', 'red')
        self.chatText.see(END)
 
        if self.flag == True: 
            # 將消息發送到客戶端 
            self.connection.send(message) 
        else: 
            # Socket連接沒有建立，提示用戶
            self.chatText.insert(END, '您還未與客戶端建立連接，客戶端無法接收您的消息\n', 'red')
 
        # 清空用戶在Text中輸入的信息 
        self.inputText.delete(0.0, END)
 
 
    # btnClose囘調函數
    def Close(self):
        sys.exit()
 
 
    # 接收客戶端數據 
    def receiveMessage(self):
 
        self.ServerSock = socket(AF_INET, SOCK_STREAM)
        self.ServerSock.bind(ADDR)
        self.ServerSock.listen(5)
 
        self.chatText.insert(END, '服務器已經就緒......\n')
        while True:
 
            self.connection,self.address = self.ServerSock.accept()
            self.flag = True
            self.chatText.insert(END, str(self.address)+'服務器端已經與客戶端建立連接......\n')
 
            while True:
                # 接收客戶端發送的消息
                self.clientMsg = str(self.connection.recv(BUFSIZ))
 
                if not self.clientMsg: 
                    continue
 
                elif self.clientMsg == 'Y':
                    self.chatText.insert(END, '服務器端已經與客戶端建立連接......\n')
                    self.connection.send(self.clientMsg)
                 
                # elif self.clientMsg == 'N':
                #     self.chatText.insert(END, '服務器端與客戶端連接失敗......\n')
                #     self.connection.send(bytes(self.clientMsg, 'utf-8'))
         
 
                else: 
                    theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
                    self.chatText.insert(END, '客戶端 ' + theTime +' 說：\n') 
                    self.chatText.insert(END, '  ' + str(self.clientMsg)+'\n', 'blue')
                    self.chatText.see(END)
 
 
    def startNewThread(self): 
        # 啟動一個新線程來接收客戶端的信息
        thread1 = threading.Timer(1, self.receiveMessage)
        thread1.setDaemon(True)
        thread1.start() 
 
 
 
 
if __name__=="__main__":
 
 
    root = tk.Tk()
    root.title("Server")
    root.resizable(False,False)
    app = Application(master=root)
    app.startNewThread()
    app.mainloop()