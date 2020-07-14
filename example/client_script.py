from lattice2d.client.client_core import ClientCore
from config import CONFIG

client = ClientCore(CONFIG)
client.run()