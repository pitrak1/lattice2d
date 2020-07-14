from config import CONFIG
from lattice2d.server.server_core import ServerCore

server = ServerCore(CONFIG)
server.run()