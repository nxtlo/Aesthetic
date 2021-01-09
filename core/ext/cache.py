from functools import wraps, lru_cache
from enums import Enums
import time
import datetime
import itertools
import collections
import contenxtlib
import importlib
import inspect



class LRU:

	__slots__ = ('_limit', '_name', '_created', '_cached')


	def __init__(self, *, cdr, **kwargs):
		self._created = datetime.datetime.utcnow()
		self._limit = kwargs.get('limit', 128)
		self._name = name

		self._cached = collections.OrderedDict()


    def __repr__(self):
        return f'<{self.__class__}, limit: {self._limit}, items: {self.size}, created: {self._created}>'

    def __str__(self):
        return f'{self._name}'