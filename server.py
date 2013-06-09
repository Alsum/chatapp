#!usr/bin/env python 
 
import socket 
import threading 
 
 
class ChatServer(object): 
 
    def __init__(self, port): 
 
        self.port=port 
        addr=('', self.port) 
        self._bufsize=2048 
 
        self.listener=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IP version 4, STREAM socket (TCP)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Quick restart server. 
        self.listener.bind(addr) 
        self.alSocks=[] 
	self.listeningHandler() #Start listening... 
 
 
 
 
    def listeningHandler(self): 
        self.listener.listen(5) 
        print "Server started.." 
	try:
		while True: 
		    clientSocket, clientAddr=self.listener.accept() 
		    #Handle the client in a new thread... 
		    self.tHandleClient=threading.Thread(target=self.clientHandler, args=[clientSocket]) 
		    self.tHandleClient.start() 
	except KeyboardInterrupt:
		print "server closed" 
 
    def clientHandler(self, clientSocket): 
 
        self.alSocks += [clientSocket] 
        print "connection from: ", clientSocket.getpeername() 
        self._bufsize=2048 
        try: 
            while True: 
 
                data=clientSocket.recv(self._bufsize) 
                if not data: 
                    break  
                self.serverToAll(clientSocket, data) 
 
        except Exception: 
            print clientSocket.getpeername(), " closed..." 
        finally: 
            self.alSocks.remove(clientSocket) 
            clientSocket.close() 
 
    def serverToAll(self, currentClient, data): 
        try: 
            for sock in self.alSocks: 
                if not sock == currentClient: 
                    sock.send(data) 
                else: 
                    pass 
        except Exception, e: 
            print e 
 
 
if __name__=="__main__": 
 
    chatServer=ChatServer(8030)  
