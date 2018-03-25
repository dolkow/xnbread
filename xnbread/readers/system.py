#!/usr/bin/env python3
#coding=utf8

from . import *
from ..exceptions import XnbInvalidPayload

def nullable(ttype, factory):
	hasobj = boolean(factory)
	if hasobj:
		return factory.read(ttype)
	return None
add_reader(nullable, 'Microsoft.Xna.Framework.Content.NullableReader', 'System.Nullable', True)

def fixedarray(ttype, count, factory):
	out = count * [None]
	for i in range(count):
		out[i] = factory.read(ttype)
	return out

def genericlist(ttype, factory):
	count = u32(factory)
	return fixedarray(ttype, count, factory)

add_reader(genericlist, 'Microsoft.Xna.Framework.Content.ArrayReader', '[]') # not fixedarray
add_reader(genericlist, 'Microsoft.Xna.Framework.Content.ListReader', 'System.Collections.Generic.List')

def dictionary(ktype, vtype, factory):
	out = dict()
	count = factory.stream.read_u32()
	for i in range(count):
		key = factory.read(ktype)
		val = factory.read(vtype)
		if key in out:
			raise XnbInvalidPayload('duplicate key "%s"' % str(key))
		out[key] = val
	return out
add_reader(dictionary, 'Microsoft.Xna.Framework.Content.DictionaryReader', 'System.Collections.Generic.Dictionary')

