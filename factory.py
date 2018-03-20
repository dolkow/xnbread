#!/usr/bin/env python3
#coding=utf8

import re

from functools import partial
from inspect import signature
from util import TODO

MANGLED_PTN = re.compile('([^[`]+)(?:`(\d+)\[(.*)\])?')
READER_REGISTRY = {} # reader name without generic args -> reader function

class ObjectFactory(object):
	def __init__(self, stream, reader_names):
		self.stream = stream
		self.reader_names = reader_names

	def read(self):
		typeid = self.stream.read_7bitint()
		if typeid == 0:
			return None
		reader = reader_by_name(self.reader_names[typeid - 1])
		return reader(self)


def add_reader(func, readername):
	READER_REGISTRY[readername] = func

def reader_by_name(mangled_name):
	match = MANGLED_PTN.match(mangled_name)
	assert match, 'reader does not match mangled pattern: %s' % mangled_name
	name, nparams, params = match.groups()
	reader = READER_REGISTRY.get(name)
	if reader is None:
		raise NotImplementedException('reader does not exist: %s' % name)
	return reader

def read_dict(factory):
	out = dict()
	count = factory.stream.read_u32()
	for i in range(count):
		key = factory.read()
		val = factory.read()
		out[key] = val
	return out
add_reader(read_dict, 'Microsoft.Xna.Framework.Content.DictionaryReader')

def read_str(factory):
	return factory.stream.read_string()
add_reader(read_str, 'Microsoft.Xna.Framework.Content.StringReader')
