from config import CONFIG
from lattice2d.config import Config
from lattice2d.server import ServerCore
from lattice2d.utilities import log

Config(CONFIG)
server = ServerCore()
server.run()
