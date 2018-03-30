#!/usr/bin/env python3
#coding=utf8

import re
import struct

from collections import namedtuple
from functools import partial
from inspect import signature
from io import StringIO

from ..exceptions import XnbUnknownType, XnbConfigError

from ..util import TODO, log, dumphex

GENERIC_READER_PTN = re.compile(r'([^[`]+)(?:`(\d+)\[(.*)\])?$')
PLAIN_TYPE_PTN = re.compile(r'([^,]+)(?:, ([^,]+), Version=([0-9.]+), Culture=([^,]+), PublicKeyToken=((?:null)|(?:[a-f0-9]+)))?$')


READER_TO_TYPE = {} # reader name without generic args -> DataType object
NAME_TO_TYPE = {} # type name without generic args -> DataType

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

	def read_byte(self):
		val = self.data[self.pos]
		self.pos += 1
		return val

	def read_u32(self):
		val, = struct.unpack('<I', self.data[self.pos:self.pos+4])
		self.pos += 4
		return val

	def read_char(self):
		lenbits = self.data[self.pos] & 0xf0
		if lenbits >= 0xf0:
			nbytes = 4
		elif lenbits >= 0xe0:
			nbytes = 3
		elif lenbits >= 0xc0:
			nbytes = 2
		else:
			nbytes = 1
		out = str(self.data[self.pos:self.pos+nbytes], 'utf-8')
		self.pos += nbytes
		assert len(out) == 1
		return out

	def read_string(self):
		nbytes = self.read_7bitint()
		binary = self.data[self.pos:self.pos+nbytes]
		self.pos += nbytes
		return str(binary, 'utf-8')

	def read_bytes(self, nbytes):
		out = self.data[self.pos:self.pos+nbytes]
		self.pos += nbytes
		return out

DataType = namedtuple('DataType', 'readfunc isvaluetype')

def fallbackread(kind, name, factory):
	msg = StringIO()
	print('%s "%s" does not exist' % (kind, name), file=msg)
	print('upcoming data:', file=msg)
	dumphex(factory.stream.data[factory.stream.pos:factory.stream.pos+128], msg)
	raise XnbUnknownType(msg.getvalue())

class ObjectFactory(object):
	def __init__(self, stream, reader_names):
		self.stream = stream
		self.readers = [reader_from_mangled(n) for n in reader_names]
		if any(s is None for s in self.readers):
			raise XnbReadError('at least one reader is None')

	def read(self, dtype=None):
		if dtype is not None:
			if callable(dtype):
				return dtype(self)
			else:
				if type(dtype) is not DataType:
					raise XnbReadError('%s is not a DataType' % str(dtype))
				if dtype.isvaluetype:
					return dtype.readfunc(self)
		typeid = self.stream.read_7bitint()
		if typeid == 0:
			return None
		if typeid > len(self.readers):
			raise XnbUnknownType('typeid %d is larger than the number of readers (%d)' % (typeid, len(self.readers)))
		reader = self.readers[typeid - 1]
		return reader(self)

def add_reader(func, readername, typename=None, isvaluetype=False):
	if not callable(func):
		raise XnbConfigError('%s is not callable' % repr(func))
	dtype = DataType(func, isvaluetype)
	if type(readername) is not str:
		raise XnbConfigError('reader name %s is not a string' % repr(readername))
	if readername in READER_TO_TYPE:
		raise XnbConfigError('duplicate reader name %s' % readername)
	READER_TO_TYPE[readername] = dtype
	if typename is not None:
		if type(typename) is not str:
			raise XnbConfigError('type name %s is not a string' % repr(typename))
		if typename in NAME_TO_TYPE:
			raise XnbConfigError('duplicate type name %s' % typename)
		NAME_TO_TYPE[typename] = dtype

def reader_from_mangled(mangled_name):
	match = GENERIC_READER_PTN.match(mangled_name)
	if not match:
		raise XnbUnknownType('reader does not match mangled pattern: %s' % mangled_name)
	name, nparams, paramstr = match.groups()
	tparams = []
	if nparams is None:
		match = PLAIN_TYPE_PTN.match(mangled_name)
		if not match:
			raise XnbUnknownType('reader does not match plain pattern: %s' % mangled_name)
		name = match.group(1)
		nparams = 0
	else:
		# TODO: multi-level nesting like ListReader`1[Nullable[Boolean]] will probably fail.
		nparams = int(nparams)
		if len(paramstr) < 2:
			raise XnbUnknownType('Unreasonably short param str: %s' % paramstr)
		depth = 1
		start = 1
		end = 1
		while end < len(paramstr):
			if paramstr[end] == '[':
				depth += 1
			elif paramstr[end] == ']':
				depth -= 1
				if depth == 0:
					if paramstr[start - 1] != '[':
						raise XnbUnknownType('Expected a starting bracket at %d in %s' % (start-1, paramstr))
					if start > 1 and paramstr[start - 2] != ',':
						raise XnbUnknownType('Expected a comma at %d in %s' % (start-2, paramstr))
					tparams.append(paramstr[start:end])
					start = end + 3
			end += 1
		if depth != 0:
			raise XnbUnknownType('Unbalanced nesting in %s' % paramstr)
		if start != len(paramstr) + 2:
			raise XnbUnknownType('Unused chars at end of %s' % paramstr)
	if nparams != len(tparams):
		raise XnbUnknownType('Declared %d type parameters, but found %d' % (nparams, len(tparams)))
	dtype = READER_TO_TYPE.get(name)
	if dtype is None:
		return partial(fallbackread, 'reader', name)
	sig = signature(dtype.readfunc)
	if len(sig.parameters) != nparams + 1:
		fmt = 'readfunc %s has %d type parameters, but "%s" contains %d'
		args = (str(dtype.readfunc), len(sig.parameters)-1, mangled_name, nparams)
		raise XnbUnknownType(fmt % args)
	if len(sig.parameters) == 1:
		return dtype.readfunc
	else:
		tparams = [type_from_mangled(t) for t in tparams]
		assert not any(t is None for t in tparams)
		return partial(dtype.readfunc, *tparams)

def type_from_mangled(mangled_name):
	match = PLAIN_TYPE_PTN.match(mangled_name)
	# TODO: more tests for the unmatched case?
	if not match:
		raise XnbUnknownType('type does not match plain pattern: %s' % mangled_name)
	name = match.group(1)
	if name.endswith('[]'):
		# TODO: reuse DataType instance per array type?
		ttype = type_from_mangled(name[:-2])
		atype = NAME_TO_TYPE['[]']
		return DataType(partial(atype.readfunc, ttype), atype.isvaluetype)
	dtype = NAME_TO_TYPE.get(name)
	if dtype is None:
		return DataType(partial(fallbackread, 'type', name), True)
	return dtype
