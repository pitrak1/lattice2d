class KeyedList(list):
	def __init__(self, iterable=None):
		super().__init__()
		self.__keys = {}
		if isinstance(iterable, KeyedList) or isinstance(iterable, list):
			self.set(iterable)

	def append_with_key(self, x, key):
		assert key not in self.__keys.keys()
		self.__keys[key] = len(self)
		super().append(x)

	def extend(self, iterable):
		assert isinstance(iterable, KeyedList)
		super().extend(iterable)
		self.__keys.update(iterable.__keys)
		return self

	def insert_with_key(self, i, x, key):
		assert key not in self.__keys.keys()
		super().insert(i, x)
		self.__keys[key] = i

	def remove(self, x):
		index = self.index(x)
		super().remove(x)
		removal_key = next(iter(key for key, value in self.__keys.items() if value == index), False)
		if removal_key: del self.__keys[removal_key]

	def remove_with_key(self, key):
		index = self.__keys[key]
		super().pop(index)
		del self.__keys[key]

	def pop(self, i):
		super().pop(i)
		removal_key = next(iter(key for key, value in self.__keys.items() if value == i), False)
		if removal_key: del self.__keys[removal_key]

	def clear(self):
		super().clear()
		self.__keys = {}

	def find(self, key):
		return self[self.__keys[key]]

	def find_by_attribute(self, attribute, value):
		return next(x for x in self if getattr(x, attribute) == value)

	def set(self, iterable):
		if isinstance(iterable, KeyedList):
			self.clear()
			for value in iterable:
				self.append(value)
			self.__keys.update(iterable.__keys)
		elif isinstance(iterable, list):
			self.clear()
			for value in iterable:
				self.append(value)
