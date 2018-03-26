#!/usr/bin/env python3
#coding=utf8

import struct

from collections import namedtuple
from sys import stderr

def log(*args):
	print(*args, file=stderr)

def TODO(msg = "Not implemented yet."):
	raise NotImplementedError(msg)

def dumphex(s, out=stderr):
	assert type(s) in (bytes, bytearray, memoryview)
	if type(s) is memoryview:
		assert type(s.obj) in (bytes, bytearray)
	pos = 0
	end = len(s)

	def mkfmt(length):
		return ' '.join(['%02x'] * length)
	fmt8 = mkfmt(8)

	def mkhex(data):
		fmt = fmt8 if len(data) == 8 else mkfmt(len(data))
		args = tuple(int(c) for c in data)
		return fmt % args

	def bytefmt(b):
		if 32 <= b < 127:
			return chr(b)
		elif b == ord('\t'):
			return '␉'
		elif b == ord('\n'):
			return '␊'
		elif b == ord('\r'):
			return '␍'
		elif b == ord('\0'):
			return '␀'
		return '·'

	def mkstr(data):
		return ''.join(map(bytefmt, data))

	while pos < end:
		raw = mkstr(s[pos:pos+16])
		hex1 = mkhex(s[pos:pos+8])
		hex2 = mkhex(s[pos+8:pos+16]) if pos + 8 < end else ''
		print('%6x: %-23s  %-23s | %s' % (pos, hex1, hex2, raw), file=out)
		pos += 16

def define_tuple(name, fmt, expected_size, fields):
	tup = namedtuple(name, fields)
	tup.format = fmt
	tup.size = expected_size
	assert struct.calcsize(fmt) == expected_size
	return tup

def clamp(v, lo, hi):
	return max(lo, min(hi, v))
