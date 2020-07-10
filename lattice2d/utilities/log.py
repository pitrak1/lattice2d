from lattice2d.config import Config

LOG_LEVEL_HIGH = 0
LOG_LEVEL_MEDIUM = 1
LOG_LEVEL_LOW = 2
LOG_LEVEL_INTERNAL_HIGH = 3
LOG_LEVEL_INTERNAL_LOW = 4

def log(value, log_level):
	if log_level <= Config()['log_level']:
		print_value = ''
		for i in range(log_level):
			print_value += '\t'
		print_value += value

		if log_level == LOG_LEVEL_HIGH:
			prGreen(print_value)
		elif log_level == LOG_LEVEL_MEDIUM:
			prPurple(print_value)
		elif log_level == LOG_LEVEL_LOW:
			prRed(print_value)
		elif log_level == LOG_LEVEL_INTERNAL_HIGH:
			prCyan(print_value)
		else:
			prYellow(print_value)

def prRed(skk): print("\033[91m {}\033[00m" .format(skk)) 
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk)) 
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk)) 
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk)) 
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk)) 
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk)) 
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk)) 
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk)) 