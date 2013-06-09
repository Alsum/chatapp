#!usr/bin/env python 
 
import socket 
import threading 
 
 
class Peer(object): 
 
    def __init__(self, serverAddr=('localhost', 8030), alias="anonymouse"): 
 
                self.serverAddr=serverAddr 
                self.tcpClient=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                self.alias=alias 
                self._bufsize=2048 
                self.tcpClient.connect(self.serverAddr) 
 		self.finised=False
                print "\nConnected to server.." 
              	self.clientToServerHandler() 
 
    def clientToServerHandler(self): 
                print "Start Chattin' \n" 
		serverToClient=threading.Thread(target=self.serverToClientHandler, args=[]) 
		serverToClient.start() #strart a thread for Non blocking receiving
                while True: 
 		    try:
		            data=raw_input('') 
		            msg=alias+": "+data 
		            if not data: 
		                break 
	
		            self.tcpClient.send(msg) 
			
		    except KeyboardInterrupt:
			    self.tcpClient.send("client %s has left the chat" %self.alias)	
			    self.finised=True		
			    self.tcpClient.close()
 
 
    def serverToClientHandler(self): 
 
                while True and not self.finised: 
                    data=self.tcpClient.recv(self._bufsize) 
                    if not data: 
                        break 
                    print data 
		
		print "stop receving data from %s"%self.alias
 
 
if __name__=="__main__": 
 
                alias=raw_input("Alias: ") 
                peer=Peer(alias=alias) 
