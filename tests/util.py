#!/usr/bin/env python3
#coding=utf8

import io
import struct

import xnbread

def mktest(data, expected):
	def decodetest(tcase):
		out = decode(tcase.readers, data)
		tcase.assertEqual(out, expected)
	return decodetest

def _seven(out, v):
	assert v >= 0
	if v == 0:
		out.append(0)
	while v > 0:
		b = v & 0x7f
		v >>= 7
		if v > 0:
			b |= 0x80
		out.append(b)

def _add_readerdefs(out, readers):
	assert type(readers) in (list, tuple, set)
	# type reader count
	_seven(out, len(readers))
	for r in readers:
		# type reader names: bytecount, bytes
		_seven(out, len(r))
		out.extend(bytes(r, 'utf8'))
		out.extend(struct.pack('<i', 0))

def _header(content_size):
	return struct.pack('<4sBBI', b'XNBw', 5, 1, content_size + 10)

def decode(readers, payload, add_framework=True):
	if add_framework:
		readers = ['Microsoft.Xna.Framework.Content.' + r for r in readers]

	mid = bytearray()
	_add_readerdefs(mid, readers)
	_seven(mid, 0) # add shared resource count

	data = bytearray()
	data.extend(_header(len(mid) + len(payload)))
	data.extend(mid)
	data.extend(payload)

	f = io.BytesIO(data)
	read = xnbread.read_payload(f)
	decoded = xnbread.decode_payload(read)

	return decoded
