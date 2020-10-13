from config import CONFIG
from lattice2d.server.server_core import ServerCore
from lattice2d.utilities.log import log


server = ServerCore(CONFIG)
server.run()
