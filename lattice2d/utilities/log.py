from lattice2d.config import Config

color_codes = {
	'red': '\033[91m',
	'green': '\033[92m',
	'yellow': '\033[93m',
	'purple': '\033[95m',
	'cyan': '\033[96m',
	'grey': '\033[97m',
	'black': '\033[98m'
}

def log(value, flag):
	config_flags = Config()['logging']
	if flag in config_flags.keys():
		print(f"{color_codes[config_flags[flag]]} {value}\033[00m")
