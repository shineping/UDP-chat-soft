import  socket
import  time
import threading
import logging
logging.basicConfig(level=logging.INFO)
class ChatServer:
    def __init__(self,ip='127.0.0.1',port=9999):
        self.ipaddr = (ip,port)
        self.sock = socket.socket()
        self.sock.bind(self.ipaddr)
        self.clients = dict()
        self.event = threading.Event()
    def start(self):
        self.sock.listen()
        threading.Thread(target=self.__accept,name='accept').start()
    def stop(self):
        self.event.set()
        time.sleep(3)
        self.sock.close()
    def __accept(self):
        while not self.event.is_set():
            conn,ipinfo = self.sock.accept()
            print(type(ipinfo))
            logging.info(ipinfo)
            self.clients[ipinfo]=conn
            threading.Thread(target=self.__recv,args=(conn,ipinfo)).start()
    def __recv(self,conn:socket.socket,ipinfo):
        while not self.event.is_set():
            try:
                data = conn.recv(1024)
            except Exception as e :
                data = b'quit'
            data = data.decode()
            if data == 'quit':
                self.clients.pop(ipinfo)
                break
            mes = 'ack:{}'.format(data)
            for client in self.clients.values():
                client.send(mes.encode())
e = threading.Event()
def showthread():
    while not e.wait(5):
        print(threading.enumerate())
chat = ChatServer()
chat.start()
threading.Thread(target=showthread,daemon=True).start()
while True:
    cmd = input('>>>')
    if cmd == 'stop':
        chat.stop()
        break