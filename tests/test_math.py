#!/usr/bin/env python3
#coding=utf8

from unittest import TestCase
from .util import decode

class MathTests(TestCase):
	readers = ['Vector3Reader', 'RectangleReader']

	def test_vector3(self):
		data = b'\x01\x10\x06\x9e\xbf\xca\xc0\x76\x44\x77\x86\x7c\x44'
		vec = decode(self.readers, data)
		self.assertEqual(vec.x, -1.2345600128173828)
		self.assertEqual(vec.y, 987.0123291015625)
		self.assertEqual(vec.z, 1010.1010131835938)

	def test_rectangle(self):
		data = b'\x02\xff\xff\xff\x7f\x00\x00\x00\x00\x00\x00\x00\x01\xfe\xff\xff\x7f'
		rect = decode(self.readers, data)
		self.assertEqual(rect.x, 2147483647)
		self.assertEqual(rect.y, 0)
		self.assertEqual(rect.w, 16777216)
		self.assertEqual(rect.h, 2147483646)

	def test_rectangle_neg(self):
		data = b'\x02\xff\xff\xff\xff\x00\x00\x00\x80\x00\x00\x00\x81\xfe\xff\xff\xff'
		rect = decode(self.readers, data)
		self.assertEqual(rect.x, -1)
		self.assertEqual(rect.y, -2147483648)
		self.assertEqual(rect.w, -2130706432)
		self.assertEqual(rect.h, -2)
