from lattice2d.client import ClientCore
from lattice2d.config import Config
from config import CONFIG

Config(CONFIG)
client = ClientCore()
client.run()
