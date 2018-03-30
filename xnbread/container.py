#!/usr/bin/env python3
#coding=utf8

from .exceptions import XnbInvalidHeader
from .readers import *
from .util import TODO, define_tuple, dumphex, log
import struct

KNOWN_FLAGS = 0x81
FLAG_BIT_HIDEF      = 0x01
FLAG_BIT_COMPRESSED = 0x80

Header = define_tuple('Header', '<3scBBI', 10,
		'magic target version flags fsize')

def read_payload(f):
	header = Header._make(struct.unpack(Header.format, f.read(Header.size)))
	if header.magic != b'XNB':
		raise XnbInvalidHeader('Magic %s is not XNB' % repr(header.magic))
	if header.target not in b'wmx':
		raise XnbInvalidHeader('Invalid target %s' % repr(header.target))
	if header.version != 5:
		raise XnbInvalidHeader('Invalid version %d' % header.version)
	if header.flags & KNOWN_FLAGS != header.flags:
		raise XnbInvalidHeader('Invalid flags 0x%08x' % header.flags)
	if header.flags & FLAG_BIT_COMPRESSED:
		from . import lzx
		dsize, = struct.unpack('<I', f.read(4))
		csize = header.fsize - Header.size - 4
		data = f.read(csize)
		if len(data) != csize:
			raise XnbInvalidHeader('Declared compressed length %d, but could only read %d' % (csize, len(data)))
		data = lzx.decompress(data, csize, dsize)
		if len(data) != dsize:
			raise XnbInvalidHeader('Declared decompressed length %d, but could only read %d' % (dsize, len(data)))
	else:
		csize = header.fsize - Header.size
		data = f.read(csize)
		if len(data) != csize:
			raise XnbInvalidHeader('Declared data length %d, but could only read %d' % (csize, len(data)))
	return data

def decode_payload(data):
	# now that we have the payload, let's decode it
	stream = ByteStream(data)
	nreaders = stream.read_7bitint()
	reader_names = []
	for i in range(nreaders):
		name = stream.read_string()
		version = stream.read_u32()
		assert version == 0, "never seen a non-zero version before"
		reader_names.append(name)
	factory = ObjectFactory(stream, reader_names)
	nshared = stream.read_7bitint()
	primary = factory.read()
	if nshared != 0:
		TODO("Haven't implemented shared resources yet")
	return primary

def dump(f, raw=False):
	import sys
	data = read_payload(f)
	if raw:
		sys.stdout.buffer.write(data)
		return
	out = decode_payload(data)
	if type(out) is dict:
		for key in out:
			print(key, '==>')
			print(out[key])
			print()
	elif type(out) in (list, tuple):
		for pair in enumerate(out):
			print('%3d: %s' % pair)
	else:
		print(out)

