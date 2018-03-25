#!/usr/bin/env python3
#coding=utf8

from xnbread.readers import *
from xnbread.readers.factory import ByteStream, ObjectFactory

import io

from unittest import TestCase

class PrimitiveReaders(TestCase):
	def setUp(self):
		bytes = b'\x05\xe6\xbc\xa2\xc3\xa5'
		self.factory = ObjectFactory(ByteStream(bytes), [])


	def test_boolean(self):
		factory = ObjectFactory(ByteStream(b'\x01'), [])
		self.assertEqual(True, boolean(factory))

	def test_u8(self):
		self.assertEqual(5, byte(self.factory))

	def test_u32(self):
		self.assertEqual(0xa2bce605, u32(self.factory))

	def test_i32(self):
		self.assertEqual(0xa2bce605 - 0x100000000, i32(self.factory))


	def test_single(self):
		self.assertEqual(-5.120104475866963e-18, single(self.factory))


	def test_char(self):
		self.assertEqual('\x05', char(self.factory))

	def test_str(self):
		self.assertEqual('漢å', string(self.factory))
