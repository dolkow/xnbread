#!/usr/bin/env python3
#coding=utf8

from unittest import TestCase
from xnbread.readers import add_reader
from xnbread.exceptions import XnbConfigError

class AddReader(TestCase):
	def test_add_int_reader_name(self):
		with self.assertRaises(XnbConfigError):
			add_reader(lambda x: None, 27)

	def test_add_duplicate_reader(self):
		with self.assertRaises(XnbConfigError):
			add_reader(lambda x: None, 'Microsoft.Xna.Framework.Content.StringReader')

	def test_add_int_type_name(self):
		with self.assertRaises(XnbConfigError):
			add_reader(lambda x: None, 'XnbRead.Fake', 38)

	def test_add_duplicate_type(self):
		with self.assertRaises(XnbConfigError):
			add_reader(lambda x: None, 'XnbRead.FakeReader', 'System.String')

	def test_add_nonfunc(self):
		with self.assertRaises(XnbConfigError):
			add_reader('abc', 'XnbRead.FakeReader', 'XnbRead.Fake')
