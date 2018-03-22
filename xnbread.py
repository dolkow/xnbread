#!/usr/bin/env python3
#coding=utf8

from factory import ObjectFactory
from util import TODO, define_tuple, dumphex, log
import struct

KNOWN_FLAGS = 0x81
FLAG_BIT_HIDEF      = 0x01
FLAG_BIT_COMPRESSED = 0x80

Header = define_tuple('Header', '<3scBBI', 10,
		'magic target version flags fsize')

class ByteStream(object):
	def __init__(self, content):
		self.pos = 0
		self.data = content
		assert type(content) in (bytes, bytearray, memoryview)
		if type(content) is memoryview:
			assert type(content.obj) in (bytes, bytearray)

	def read_7bitint(self):
		res = 0
		byte = 0x80
		start = self.pos
		while byte & 0x80:
			byte = self.data[self.pos]
			res |= (byte & 0x7f) << (7 * (self.pos-start))
			self.pos += 1
		return res

	def read_u32(self):
		val, = struct.unpack('<I', self.data[self.pos:self.pos+4])
		self.pos += 4
		return val

	def read_string(self):
		nbytes = self.read_7bitint()
		binary = self.data[self.pos:self.pos+nbytes]
		self.pos += nbytes
		return str(binary, 'utf-8')


def read_payload(f):
	header = Header._make(struct.unpack(Header.format, f.read(Header.size)))
	assert header.magic == b'XNB'
	assert header.target in b'wmx'
	assert header.version == 5
	assert header.flags & KNOWN_FLAGS == header.flags
	if header.flags & FLAG_BIT_COMPRESSED:
		import lzx
		dsize, = struct.unpack('<I', f.read(4))
		csize = header.fsize - Header.size - 4
		data = f.read(csize)
		assert len(data) == csize
		data = lzx.decompress(data, csize, dsize)
		assert len(data) == dsize
	else:
		csize = header.fsize - Header.size
		data = f.read(csize)
		assert len(data) == csize
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

if __name__ == '__main__':
	import sys
	raw = False
	for filename in sys.argv[1:]:
		if filename == '-r':
			raw = True
			continue
		with open(filename, 'rb') as f:
			data = read_payload(f)
			if raw:
				sys.stdout.buffer.write(data)
				continue
			else:
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
