"""
Server pra teste, bora mudar depois pro server que Mário quer
"""
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

authorizer = DummyAuthorizer()
authorizer.add_user("Rkanehisa", "123456'", "/home/rkanehisa", perm="elradfmw") #Coloca o diretório aqui
authorizer.add_anonymous("/home/rkanehisa", perm="elradfmw") # E aqui também

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("127.0.0.1", 1026), handler)
server.serve_forever()