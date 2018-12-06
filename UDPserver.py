import socket
import threading
import logging
class Server:
    def __init__(self,ip='127.0.0.1',port=699):
        self.ip=ip
        self.port=port
        self.sock=socket.socket(type=socket.SOCK_DGRAM)
        self.sock.bind((self.ip,self.port))
        self.client=set()
        self.event=threading.Event()
    def start(self):
        threading.Thread(target=self.__recv).start()
    def stop(self):
        self.event.set()
        self.sock.close()
    def __recv(self):
        while not self.event.is_set():
            data,ipinfo=self.sock.recvfrom(1024)
            self.client.add(ipinfo)
            print(data,ipinfo)
            if data==b'quit':
                self.client.remove(ipinfo)
            self.send(data)
    def send(self,data):
        for client in self.client:
            # data = data.encode()
            self.sock.sendto(data,client)
if __name__=='__main__':
    server = Server()
    server.start()
    while True:
        cmd=input('>>>')
        if cmd =='stop':
            server.stop()
            break
        cmd = cmd.encode()
        server.send(cmd)