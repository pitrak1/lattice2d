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
			print_green(print_value)
		elif log_level == LOG_LEVEL_MEDIUM:
			print_purple(print_value)
		elif log_level == LOG_LEVEL_LOW:
			print_red(print_value)
		elif log_level == LOG_LEVEL_INTERNAL_HIGH:
			print_cyan(print_value)
		else:
			print_yellow(print_value)


def print_red(skk): print("\033[91m {}\033[00m".format(skk))


def print_green(skk): print("\033[92m {}\033[00m".format(skk))


def print_yellow(skk): print("\033[93m {}\033[00m".format(skk))


def print_purple(skk): print("\033[95m {}\033[00m".format(skk))


def print_cyan(skk): print("\033[96m {}\033[00m".format(skk))


def print_grey(skk): print("\033[97m {}\033[00m".format(skk))


def print_black(skk): print("\033[98m {}\033[00m".format(skk))
