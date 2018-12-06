import socket
import threading
import logging
class Custom:
    def __init__(self,ip='127.0.0.1',port=699):
        self.ip=ip
        self.port=port
        self.sock=socket.socket(type=socket.SOCK_DGRAM)
        self.event=threading.Event()
    def start(self):
        self.send('reg')
        threading.Thread(target=self.__recv).start()
    def stop(self):
        self.event.set()
        self.sock.close()
    def __recv(self):
        while not self.event.is_set():
            data=self.sock.recv(1024)
            print(data)
    def send(self,cmd):
        cmd=cmd.encode()
        self.sock.sendto(cmd,(self.ip,self.port))
if __name__=='__main__':
    custom = Custom()
    custom.start()
    while True:
        cmd=input('>>>')
        if cmd =='stop':
            custom.stop()
            break
            
        custom.send(cmd)