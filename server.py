import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from threading import Thread

    
authorizer = DummyAuthorizer()   
authorizer.add_user('SMartBird', '12345', '.', perm='elradfmwM')
authorizer.add_anonymous(os.getcwd())
   
handler = FTPHandler
handler.authorizer = authorizer
handler.banner = "Local Server is Ready now."
   
address = ('127.0.0.1', 21)

server = FTPServer(address, handler)    
server.max_cons = 256
server.max_cons_per_ip = 5  
server.serve_forever()


