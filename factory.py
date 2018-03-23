#!/usr/bin/env python3
#coding=utf8

import re

from functools import partial
from inspect import signature
from util import TODO, log

MANGLED_PTN = re.compile('([^[`]+)(?:`(\d+)\[(.*)\])?')
READER_REGISTRY = {} # reader name without generic args -> reader function

class FlexibleObject(object):
	pass

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

def read_texture(factory):
	texture = FlexibleObject()
	texture.format = factory.stream.read_u32()
	texture.width = factory.stream.read_u32()
	texture.height = factory.stream.read_u32()
	mips = factory.stream.read_u32()
	texture.miplevels = mips * [None]
	for i in range(mips):
		dsize = factory.stream.read_u32()
		texture.miplevels[i] = factory.stream.read_bytes(dsize)
	return texture
add_reader(read_texture, 'Microsoft.Xna.Framework.Content.Texture2DReader')
