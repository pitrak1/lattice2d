import math
from lattice2d.config import Config
import threading
from collections import deque


def within_circle_bounds(start_position, end_position, radius):
	distance = math.sqrt(((start_position[0] - end_position[0]) ** 2) + ((start_position[1] - end_position[1]) ** 2))
	return distance < radius


def within_rect_bounds(start_position, end_position, dimensions):
	valid_x = start_position[0] - dimensions[0] // 2 < end_position[0] < start_position[0] + dimensions[0] // 2
	valid_y = start_position[1] - dimensions[1] // 2 < end_position[1] < start_position[1] + dimensions[1] // 2
	return valid_x and valid_y


def within_square_bounds(start_position, end_position, width):
	return within_rect_bounds(start_position, end_position, (width, width))


def get_page_info(current_page, page_size, total):
	min_ = current_page * page_size
	max_ = min((current_page + 1) * page_size, total)
	down = (current_page + 1) * page_size < total
	up = current_page != 0
	return [min_, max_, down, up]


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


class ThreadedQueue:
	def __init__(self):
		self.__queue = deque()
		self.__lock = threading.Lock()

	def has_elements(self):
		return len(self.__queue) > 0

	def popleft(self):
		self.__lock.acquire()
		command = self.__queue.popleft()
		self.__lock.release()
		return command

	def append(self, command):
		self.__lock.acquire()
		self.__queue.append(command)
		self.__lock.release()


class ThreadedSync:
	def __init__(self, count_max):
		self.__lock = threading.Lock()
		self.__count = 0
		self.__count_max = count_max

	def count(self):
		if self.done():
			self.__lock.acquire()
			self.__count = self.__count_max
			self.__lock.release()

		self.__lock.acquire()
		self.__count -= 1
		self.__lock.release()

	def done(self):
		return self.__count == 0
