#!/usr/bin/env python3
#coding=utf8

import re
import struct

from functools import partial
from inspect import signature
from util import TODO, log

MANGLED_PTN = re.compile('([^[`]+)(?:`(\d+)\[(.*)\])?')
READER_REGISTRY = {} # reader name without generic args -> reader function

class ByteStream(object):
	def __init__(self, content):
		self.pos = 0
		self.data = content
		assert type(content) in (bytes, bytearray, memoryview)
		if type(content) is memoryview:
			assert type(content.obj) in (bytes, bytearray)

	def read_7bitint(self):
		res = 0
		byte = 0x80
		start = self.pos
		while byte & 0x80:
			byte = self.data[self.pos]
			res |= (byte & 0x7f) << (7 * (self.pos-start))
			self.pos += 1
		return res

	def read_u32(self):
		val, = struct.unpack('<I', self.data[self.pos:self.pos+4])
		self.pos += 4
		return val

	def read_string(self):
		nbytes = self.read_7bitint()
		binary = self.data[self.pos:self.pos+nbytes]
		self.pos += nbytes
		return str(binary, 'utf-8')

	def read_bytes(self, nbytes):
		out = self.data[self.pos:self.pos+nbytes]
		self.pos += nbytes
		return out

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
	if not nparams:
		name, junk = name.split(',', 1)
	reader = READER_REGISTRY.get(name)
	if reader is None:
		raise NotImplementedError('reader does not exist: %s' % name)
	return reader
