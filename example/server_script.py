from config import CONFIG
from lattice2d.config import Config
from lattice2d.server.server_core import ServerCore
from lattice2d.utilities.log import log

Config(CONFIG)
server = ServerCore()
server.run()
