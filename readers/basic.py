#!/usr/bin/env python3
#coding=utf8

from . import add_reader

def _read_dict(factory):
	out = dict()
	count = factory.stream.read_u32()
	for i in range(count):
		key = factory.read()
		val = factory.read()
		out[key] = val
	return out
add_reader(_read_dict, 'Microsoft.Xna.Framework.Content.DictionaryReader')

def _read_str(factory):
	return factory.stream.read_string()
add_reader(_read_str, 'Microsoft.Xna.Framework.Content.StringReader')
