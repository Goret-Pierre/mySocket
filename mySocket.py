import socket
from myEventemitter import Eventemmiter
from threading import Thread
import json

class TreadForListenning(Thread):
    def __init__(self,obj,conn):
        Thread.__init__(self)
        self.obj = obj
        self.conn = conn
        self.listenning = True
    def run(self):
        while self.listenning:
            data = ""
            try:
                data = self.conn.recv(1024)
            except ConnectionResetError:
                self.listenning = False
            if data != "":
                self.obj.emit(self.conn,data)
        self.conn.close()
        self.obj.emit(ConnectionResetError,self.conn)
    # def kill(self):
    #     self.listenning = False
    #     print("kill listenner !")

def Mybind(obj,f):
    def _bind(args):
        obj.host = args[0]
        obj.port = args[1]
        obj.socketType = "Server"
        return f(args)
    return _bind

def Mylisten(obj,f):
    def _listen(n = 5,callback = None):
        obj.enable  = True
        f(n) #NB faire gestion d'erreur !!
        if callable(callback):
            callback()
        if hasattr(callback,"__call__"):
            callback
    return _listen


def Myconnect(obj,f,callback = None):
    def _connect(args):
        obj.socketType = "Client"
        f(args) #NB faire gestion d'erreur !!!
        obj.emit("connection",obj)
        if callable(callback):
            callback()
        if hasattr(callback,"__call__"):
            callback
    return _connect

class MySocket(socket.socket,Eventemmiter,Thread):
    """
        Faire des commentaires
    """
    def __init__(self,**kargs):
        """
            Faire des commentaires
        """
        Thread.__init__(self)
        socket.socket.__init__(self,socket.AF_INET, socket.SOCK_STREAM)
        Eventemmiter.__init__(self,**kargs)

        self.host,self.port = kargs.get("host",None),kargs.get("port",None)
        self.socketType = None
        self._threadsList = {}

        self.bind = Mybind(self,self.bind)
        self.listen = Mylisten(self,self.listen)
        self.connect = Myconnect(self,self.connect)
        
        self.on("Error",self._Error)
        self.on("connection",self._NewConnection)
        self.on(ConnectionResetError,self._ConnectionClosed)
    
    def send_data(self,data,conn = None):
        if conn is None: #broadcast
            for key_conn in self._threadsList.keys():
                try:
                    key_conn.sendall(data)
                except ConnectionResetError:
                    key_conn.close()
                    self.emit(ConnectionResetError,key_conn)
        elif conn in self._threadsList.keys():
            try:
                conn.sendall(data)
            except ConnectionResetError:
                conn.close()
                self.emit(ConnectionResetError,conn)
    
    def run(self):
        while self.enable:     
            conn,addr = self.accept()
            self.emit("connection",conn)
        self.close()

    def _Error(self):
        pass
    def _ConnectionClosed(self,conn):
        if conn in self._threadsList:
            del(self._threadsList[conn])
        print(self._threadsList)
            
    def _NewConnection(self,conn):
        newThread = TreadForListenning(self,conn)
        newThread.start()
        self._threadsList[conn] = newThread

if __name__ == "__main__":    
    # SAV
    screen = ""
    import os
    os.system('cls')
    def Startup_Message(obj):
        global screen
        screen += "Le serveur est démarrer sur \"{};{}\" \n".format(obj.host,obj.port)
    s = MySocket()
    s.bind(("localhost",5060))
    @s.on("connection")
    def affiche_receve(conn):
        global screen
        screen += "Un client c'est connecté ! \n"
        os.system('cls')
        print(screen)
        @s.on(conn)
        def test(data):
            # print(data)
            global screen
            screen += data.decode("utf8") + "\n"
            os.system('cls')
            print(screen)
    s.listen(5,Startup_Message(s))
    s.start()
    data = ""
    while data != "STOP":
        os.system('cls')
        print(screen)
        data = input()
        if data !="":
            s.send_data(data.encode("utf8"))
    