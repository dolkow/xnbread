#!/usr/bin/env python3
#coding=utf8

from . import add_reader

from struct import unpack as _unpack

def boolean(factory):
	v = factory.stream.read_byte()
	assert v in (0,1)
	return (v == 1)
add_reader(boolean, 'Microsoft.Xna.Framework.Content.BooleanReader', 'System.Boolean', True)


def i32(factory):
	return _unpack('<i', factory.stream.read_bytes(4))[0]
add_reader(i32, 'Microsoft.Xna.Framework.Content.Int32Reader', 'System.Int32', True)


def u32(factory):
	return _unpack('<I', factory.stream.read_bytes(4))[0]
add_reader(u32, 'Microsoft.Xna.Framework.Content.UInt32Reader', 'System.UInt32', True)


def single(factory):
	return _unpack('<f', factory.stream.read_bytes(4))[0]
add_reader(single, 'Microsoft.Xna.Framework.Content.SingleReader', 'System.Single', True)


def byte(factory):
	return factory.stream.read_byte()
add_reader(byte, 'Microsoft.Xna.Framework.Content.ByteReader', 'System.Byte', True)

def char(factory):
	return factory.stream.read_char()
add_reader(char, 'Microsoft.Xna.Framework.Content.CharReader', 'System.Char', True)


def string(factory):
	return factory.stream.read_string()
add_reader(string, 'Microsoft.Xna.Framework.Content.StringReader', 'System.String')
