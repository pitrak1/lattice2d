import threading

class ThreadedSync():
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
