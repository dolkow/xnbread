#!/usr/bin/env python3
#coding=utf8

from . import add_reader
from .basic import _u32, _boolean

def _nullable(ttype, factory):
	hasobj = _boolean(factory)
	if hasobj:
		return factory.read(ttype)
	return None
add_reader(_nullable, 'Microsoft.Xna.Framework.Content.NullableReader', 'System.Nullable', True)

def _fixedarray(ttype, count, factory):
	out = count * [None]
	for i in range(count):
		out[i] = factory.read(ttype)
	return out

def _list(ttype, factory):
	count = _u32(factory)
	return _fixedarray(ttype, count, factory)

add_reader(_list, 'Microsoft.Xna.Framework.Content.ArrayReader', '[]') # not _fixedarray
add_reader(_list, 'Microsoft.Xna.Framework.Content.ListReader', 'System.Collections.Generic.List')

def _read_dict(ktype, vtype, factory):
	out = dict()
	count = factory.stream.read_u32()
	for i in range(count):
		key = factory.read(ktype)
		val = factory.read(vtype)
		out[key] = val
	return out
add_reader(_read_dict, 'Microsoft.Xna.Framework.Content.DictionaryReader', 'System.Collections.Generic.Dictionary')

