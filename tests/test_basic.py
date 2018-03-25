#!/usr/bin/env python3
#coding=utf8

from unittest import TestCase
from .util import decode

class BasicTests(TestCase):

	def test_null(self):
		self.assertIsNone(decode(['StringReader'], b'\x00'))


	def test_no_readers(self):
		self.assertIsNone(decode([], b'\x00'))

	def test_extra_reader_1(self):
		self.assertEqual(decode(['ByteReader', 'CharReader'], b'\x01A'), 65)

	def test_extra_reader_2(self):
		self.assertEqual(decode(['CharReader', 'ByteReader'], b'\x02A'), 65)


	def test_byte_a(self):
		self.assertEqual(decode(['ByteReader'], b'\x01A'), 65)

	def test_byte_b(self):
		self.assertEqual(decode(['ByteReader'], b'\x01B'), 66)

	def test_byte_min(self):
		self.assertEqual(decode(['ByteReader'], b'\x01\x00'), 0)

	def test_byte_max(self):
		self.assertEqual(decode(['ByteReader'], b'\x01\xff'), 255)
