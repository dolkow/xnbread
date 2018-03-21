#!/usr/bin/env python3
#coding=utf8

# based on format description at https://msdn.microsoft.com/en-us/library/bb417343.aspx#lzxintro
# with some quirks help from https://github.com/kyz/libmspack/blob/master/libmspack/mspack/lzxd.c

import struct

from util import TODO, clamp, dumphex

# block types:
VERBATIM     = 1
ALIGNED      = 2
UNCOMPRESSED = 3

# misc
WINDOW_BITS = 16 # XXX valid for .xnb lzx data; may vary in others!
WINDOW_SIZE = 1 << WINDOW_BITS
NUM_POSITION_SLOTS = WINDOW_BITS * 2 # this will be wrong for winbits 20 and 21
MIN_MATCH = 2
MAX_MATCH = 257
NUM_CHARS = 256
NUM_PRIMARY_LENGTHS = 7
EXTRA_BITS = [clamp(i // 2 - 1, 0, 17) for i in range(50)]
BASE_POSITION = [sum(1 << x for x in EXTRA_BITS[:i]) for i in range(50)]

# pre-tree
PRETREE_SIZE = 20
PRETREE_TABLE_BITS = 8
# main tree
MAIN_SIZE = NUM_CHARS + NUM_POSITION_SLOTS * 8
MAIN_TABLE_BITS = 15
# secondary tree (a.k.a. "length tree"; a difficult name to use); beta for short
BETA_SIZE = 249
BETA_TABLE_BITS = 15
# aligned tree
ALIGNED_SIZE = 8
ALIGNED_TABLE_BITS = 8


class BitStream(object):
	''' the LZX format bit stream puts bits in 16-bit entities, with
	    little-endian byte order '''
	def __init__(self, bytes):
		self.bytes = bytes
		self.nextbyte = 0
		self.cache = 0 # essentially a queue of unused bits
		self.avail = 0 # bits in cache

	def peek(self, bits):
		while self.avail < bits and self.nextbyte < len(self.bytes):
			self.avail += 16
			self.cache <<= 16
			self.cache |= self.bytes[self.nextbyte]
			self.cache |= self.bytes[self.nextbyte+1] << 8
			self.nextbyte += 2
		if self.avail >= bits:
			return self.cache >> (self.avail - bits)
		else:
			return self.cache << (bits - self.avail) # zero-pad

	def take(self, bits):
		if bits > self.avail:
			raise Exception('taking %d bits from only %d' % (bits, self.avail))
		self.avail -= bits
		self.cache &= (1 << self.avail) - 1

	def read(self, bits):
		val = self.peek(bits)
		self.take(bits)
		return val

class LookupTable(object):
	def __init__(self, nbits, symbol_lengths):
		self.nbits = nbits
		self.table = table = (1 << nbits) * [None]
		self.symbol_lengths = symbol_lengths

		assert all(length <= nbits for length in symbol_lengths)
		assert all(length >= 0 for length in symbol_lengths)

		next = (1 << nbits) - 1
		nsyms = len(symbol_lengths)
		for bits in range(nbits, 0, -1):
			for val in range(nsyms-1, -1, -1):
				if symbol_lengths[val] == bits:
					nslots = 1 << (nbits - bits)
					for x in range(nslots):
						table[next-x] = val
					next -= nslots
		if False:
			for peeked, val in enumerate(table):
				print('LUT {:06b}'.format(peeked), val, symbol_lengths[val])
		assert next == -1
		assert not any(x is None for x in table), 'empty lookup table slot'
		populated = set(i for i, v in enumerate(symbol_lengths) if v > 0)
		assert populated == set(self.table)

	def read_from(self, bitstream):
		peeked = bitstream.peek(self.nbits)
		val = self.table[peeked]
		bitstream.take(self.symbol_lengths[val])
		return val

def decompress_block(cbuf, dbuf):
	first_block = True # TODO: take as param
	main_lengths = memoryview(bytearray(MAIN_SIZE)) # TODO: take as param / store state?
	beta_lengths = memoryview(bytearray(BETA_SIZE)) # TODO: take as param / store state?
	cbuf = BitStream(cbuf)
	dpos = 0
	lru = [1, 1, 1]

	if first_block:
		transformed = cbuf.read(1)
		if transformed:
			TODO("intel call instruction transform not supported")
	while dpos < len(dbuf):
		# TODO: "after each 32768th uncompressed byte is represented, the output bit buffer is byte aligned on a 16-bit boundary by outputting 0-15 zero bits"
		# TODO: block remaining bytes?
		blocktype = cbuf.read(3)
		blocksize = cbuf.read(24) # uncompressed size of this block
		if blocktype in (VERBATIM, ALIGNED):
			if blocktype == ALIGNED:
				align_lengths = [cbuf.read(3) for i in range(8)]
				aligntree = LookupTable(ALIGNED_TABLE_BITS, align_lengths)
			update_lengths(cbuf, main_lengths[:NUM_CHARS])
			update_lengths(cbuf, main_lengths[NUM_CHARS:])
			maintree = LookupTable(MAIN_TABLE_BITS, main_lengths)
			update_lengths(cbuf, beta_lengths)
			betatree = LookupTable(BETA_TABLE_BITS, beta_lengths)
		else:
			TODO("no implementation for block type %d" % blocktype)
		while blocksize > 0:
			print(dpos, blocksize, cbuf.nextbyte, len(cbuf.bytes))
			val = maintree.read_from(cbuf)
			if val < NUM_CHARS:
				dbuf[dpos] = val
				dpos += 1
				blocksize -= 1
				continue
			match_length = (val - NUM_CHARS) & NUM_PRIMARY_LENGTHS
			if match_length == NUM_PRIMARY_LENGTHS:
				match_length += MIN_MATCH + betatree.read_from(cbuf)
			else:
				match_length += MIN_MATCH
			position_slot = (val - NUM_CHARS) >> 3
			if position_slot <= 2:
				match_offset = lru[position_slot]
				lru[position_slot] = lru[0]
				lru[0] = match_offset
			else:
				extra = EXTRA_BITS[position_slot]
				if blocktype == VERBATIM:
					if extra > 0:
						verbatim_bits = cbuf.read(extra)
					else:
						verbatim_bits = 0
					formatted_offset = BASE_POSITION[position_slot] + verbatim_bits
				elif blocktype == ALIGNED:
					if extra > 3:
						verbatim_bits = cbuf.read(extra - 3) << 3
						aligned_bits = aligntree.read_from(cbuf)
					elif extra == 3:
						verbatim_bits = aligntree.read_from(cbuf)
						aligned_bits = 0
					elif extra > 0:
						verbatim_bits = cbuf.read(extra)
						aligned_bits = 0
					else:
						verbatim_bits = 0
						aligned_bits = 0
					formatted_offset = BASE_POSITION[position_slot] + verbatim_bits + aligned_bits
				else:
					TODO()
				match_offset = formatted_offset - 2
				lru[2] = lru[1]
				lru[1] = lru[0]
				lru[0] = match_offset
			# now, copy!
			for i in range(match_length):
				dbuf[dpos + i] = dbuf[dpos + i - match_offset]
			dpos += match_length
			blocksize -= match_length

def update_lengths(bitstream, lengths):
	pretree = LookupTable(PRETREE_TABLE_BITS,
	                      [bitstream.read(4) for i in range(PRETREE_SIZE)])
	repeats_left = 0
	for x in range(len(lengths)):
		if repeats_left > 0:
			lengths[x] = lengths[x-1]
			repeats_left -= 1
			continue
		code = pretree.read_from(bitstream)
		if code == 17:
			repeats_left = 3 + bitstream.read(4)
			lengths[x] = 0
		elif code == 18:
			repeats_left = 19 + bitstream.read(5)
			lengths[x] = 0
		else:
			if code == 19:
				repeats_left = 3 + bitstream.read(1)
				code = pretree.read_from(bitstream)
			lengths[x] = (lengths[x] - code) % 17
	if False:
		for i,v in enumerate(lengths):
			if v != 0:
				print('update_lengths %3d => %2d' % (i, v))
	return lengths

def decompress(cdata, inputsize, outputsize):
	cdata = memoryview(cdata)
	ddata = memoryview(bytearray(outputsize))
	cpos = 0
	dpos = 0
	assert len(cdata) == inputsize
	while dpos < outputsize and cpos < inputsize:
		if cdata[cpos] == 0xff:
			fsize, bsize = struct.unpack('>HH', cdata[cpos+1:cpos+5])
			cpos += 5
		else:
			fsize = 1 << 15
			bsize, = struct.unpack('>H', cdata[cpos:cpos+2])
			cpos += 2
		assert fsize > 0
		assert bsize > 0

		decompress_block(cdata[cpos:cpos+bsize], ddata[dpos:dpos+fsize])

		cpos += bsize
		dpos += fsize
	assert dpos == outputsize
	return ddata
