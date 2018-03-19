#!/usr/bin/env python3
#coding=utf8

import struct

from collections import namedtuple

def TODO(msg = "Not implemented yet."):
	assert 0, msg

def _dumphexline(line):
	fmt = ' '.join(['%02x'] * len(line))
	args = tuple(int(c) for c in line)
	print(fmt % args)

def dumphex(s):
	pos = 0
	end = len(s)
	while pos < end:
		_dumphexline(s[pos:pos+16])
		pos += 16

def define_tuple(name, fmt, expected_size, fields):
	tup = namedtuple(name, fields)
	tup.format = fmt
	tup.size = expected_size
	assert struct.calcsize(fmt) == expected_size
	return tup

def clamp(v, lo, hi):
	return max(lo, min(hi, v))
