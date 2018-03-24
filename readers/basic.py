#!/usr/bin/env python3
#coding=utf8

from . import add_reader

from struct import unpack as _unpack

def _boolean(factory):
	v = factory.stream.read_byte()
	assert v in (0,1)
	return (v == 1)
add_reader(_boolean, 'Microsoft.Xna.Framework.Content.BooleanReader', 'System.Boolean', True)


def _i32(factory):
	return _unpack('<i', factory.stream.read_bytes(4))[0]
add_reader(_i32, 'Microsoft.Xna.Framework.Content.Int32Reader', 'System.Int32', True)


def _u32(factory):
	return _unpack('<I', factory.stream.read_bytes(4))[0]
add_reader(_u32, 'Microsoft.Xna.Framework.Content.UInt32Reader', 'System.UInt32', True)


def _single(factory):
	return _unpack('<f', factory.stream.read_bytes(4))[0]
add_reader(_single, 'Microsoft.Xna.Framework.Content.SingleReader', 'System.Single', True)


def _byte(factory):
	return factory.stream.read_byte()
add_reader(_byte, 'Microsoft.Xna.Framework.Content.ByteReader', 'System.Byte', True)

def _char(factory):
	return factory.stream.read_char()
add_reader(_char, 'Microsoft.Xna.Framework.Content.CharReader', 'System.Char', True)


def _read_str(factory):
	return factory.stream.read_string()
add_reader(_read_str, 'Microsoft.Xna.Framework.Content.StringReader', 'System.String')
