#!/usr/bin/env python3
#coding=utf8

from . import add_reader

from struct import unpack as _unpack

def boolean(factory):
	v = factory.stream.read_byte()
	assert v in (0,1)
	return (v == 1)
add_reader(boolean, 'Microsoft.Xna.Framework.Content.BooleanReader', 'System.Boolean', True)


def i16(factory):
	return _unpack('<h', factory.stream.read_bytes(2))[0]
add_reader(i16, 'Microsoft.Xna.Framework.Content.Int16Reader', 'System.Int16', True)

def u16(factory):
	return _unpack('<H', factory.stream.read_bytes(2))[0]
add_reader(u16, 'Microsoft.Xna.Framework.Content.UInt16Reader', 'System.UInt16', True)


def i32(factory):
	return _unpack('<i', factory.stream.read_bytes(4))[0]
add_reader(i32, 'Microsoft.Xna.Framework.Content.Int32Reader', 'System.Int32', True)

def u32(factory):
	return _unpack('<I', factory.stream.read_bytes(4))[0]
add_reader(u32, 'Microsoft.Xna.Framework.Content.UInt32Reader', 'System.UInt32', True)


def i64(factory):
	return _unpack('<q', factory.stream.read_bytes(8))[0]
add_reader(i64, 'Microsoft.Xna.Framework.Content.Int64Reader', 'System.Int64', True)

def u64(factory):
	return _unpack('<Q', factory.stream.read_bytes(8))[0]
add_reader(u64, 'Microsoft.Xna.Framework.Content.UInt64Reader', 'System.UInt64', True)


def single(factory):
	return _unpack('<f', factory.stream.read_bytes(4))[0]
add_reader(single, 'Microsoft.Xna.Framework.Content.SingleReader', 'System.Single', True)

def double(factory):
	return _unpack('<d', factory.stream.read_bytes(8))[0]
add_reader(double, 'Microsoft.Xna.Framework.Content.DoubleReader', 'System.Double', True)

def byte(factory):
	return factory.stream.read_byte()
add_reader(byte, 'Microsoft.Xna.Framework.Content.ByteReader', 'System.Byte', True)

def sbyte(factory):
	return _unpack('<b', factory.stream.read_bytes(1))[0]
add_reader(sbyte, 'Microsoft.Xna.Framework.Content.SByteReader', 'System.SByte', True)


def char(factory):
	return factory.stream.read_char()
add_reader(char, 'Microsoft.Xna.Framework.Content.CharReader', 'System.Char', True)


def string(factory):
	return factory.stream.read_string()
add_reader(string, 'Microsoft.Xna.Framework.Content.StringReader', 'System.String')


def obj(factory):
	return factory.read()
add_reader(obj, 'Microsoft.Xna.Framework.Content.ObjectReader', 'System.Object')
