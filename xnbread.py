#!/usr/bin/env python3
#coding=utf8

from util import TODO, define_tuple, dumphex
import struct

KNOWN_FLAGS = 0x81
FLAG_BIT_HIDEF      = 0x01
FLAG_BIT_COMPRESSED = 0x80

Header = define_tuple('Header', '<3scBBII', 14,
		'magic target version flags fsize dsize')

if __name__ == '__main__':
	import sys
	for filename in sys.argv[1:]:
		with open(filename, 'rb') as f:
			header = Header._make(struct.unpack(Header.format, f.read(Header.size)))
			data = f.read()
			dumphex(data)
			assert header.magic == b'XNB'
			assert header.target in b'wmx'
			assert header.version == 5
			assert header.fsize == len(data) + Header.size
			assert header.flags & KNOWN_FLAGS == header.flags
			if header.flags & FLAG_BIT_COMPRESSED:
				import lzx
				csize = header.fsize - Header.size
				data = lzx.decompress(data, csize, header.dsize)
			else:
				TODO("uncompressed data not implemented yet")
			print(bytes(data))
