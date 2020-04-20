LOG_LEVEL = 2

LOG_LEVEL_NETWORK = 0
LOG_LEVEL_COMMAND = 1
LOG_LEVEL_DEBUG = 2

def log(value, log_level=LOG_LEVEL_NETWORK, data=None):
	if log_level <= LOG_LEVEL:
		print_value = ''
		for i in range(log_level):
			print_value += '\t'
		print_value += value
		if data:
			print_value += '{ '
			for key, value in data.items():
				print_value += f'{key}: {value}, '
			print_value = print_value[:-2]
			print_value += ' }'
		if log_level == LOG_LEVEL_NETWORK:
			prGreen(print_value)
		elif log_level == LOG_LEVEL_COMMAND:
			prPurple(print_value)
		else:
			prRed(print_value)

def prRed(skk): print("\033[91m {}\033[00m" .format(skk)) 
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk)) 
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk)) 
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk)) 
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk)) 
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk)) 
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk)) 
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk)) 