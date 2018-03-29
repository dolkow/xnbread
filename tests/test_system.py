#!/usr/bin/env python3
#coding=utf8

from unittest import TestCase
from .util import mktest, decode

from xnbread.exceptions import XnbInvalidPayload, XnbUnknownType
from xnbread.readers import ObjectFactory

class NullableBoolTests(TestCase):
	readers = ['NullableReader`1[[System.Boolean]]']
	test_nullable_bool_true = mktest(b'\x01\x01\x01', True)
	test_nullable_bool_false = mktest(b'\x01\x01\x00', False)
	test_nullable_bool_null = mktest(b'\x01\x00', None)

	def test_type_count_lo(self):
		with self.assertRaises(XnbUnknownType):
			ObjectFactory(None, ['Microsoft.Xna.Framework.Content.NullableReader`0[]'])

	def test_type_count_hi(self):
		with self.assertRaises(XnbUnknownType):
			ObjectFactory(None, ['Microsoft.Xna.Framework.Content.NullableReader`2[[System.Byte],[System.Byte]]'])
			print(of.readers)

class ArrayTests(TestCase):
	readers = [
		'ArrayReader`1[[System.String]]',
		'StringReader',
		'ArrayReader`1[[System.UInt16]]',
		'ArrayReader`1[[System.Object]]',
		'UInt16Reader'
	]
	intdata = b'\x03\x04\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08'
	strdata = b'\x01\x03\x00\x00\x00\x02\x05Hello\x02\x05cruel\x02\x06world!'
	mixdata = b'\x04\x03\x00\x00\x00\x02\x05Hello\x05\x01\x80\x02\x06world!'
	test_int_elems = mktest(intdata, [513, 1027, 1541, 2055])
	test_str_elems = mktest(strdata, ['Hello', 'cruel', 'world!'])
	test_mix_elems = mktest(mixdata, ['Hello', 32769, 'world!'])

	def test_type_count_lo(self):
		with self.assertRaises(XnbUnknownType):
			ObjectFactory(None, ['Microsoft.Xna.Framework.Content.ArrayReader`0[]'])

	def test_type_count_hi(self):
		with self.assertRaises(XnbUnknownType):
			ObjectFactory(None, ['Microsoft.Xna.Framework.Content.ArrayReader`2[[System.Byte],[System.Byte]]'])

class ListTests(TestCase):
	readers = [
		'ListReader`1[[System.UInt16]]',
		'StringReader',
		'ListReader`1[[System.String]]',
		'ArrayReader`1[[System.Object]]',
		'Int16Reader'
	]
	intdata = b'\x01\x04\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08'
	strdata = b'\x03\x03\x00\x00\x00\x02\x05Hello\x02\x05cruel\x02\x06world!'
	mixdata = b'\x04\x03\x00\x00\x00\x02\x05Hello\x05\x01\x80\x02\x06world!'
	test_int_elems = mktest(intdata, [513, 1027, 1541, 2055])
	test_str_elems = mktest(strdata, ['Hello', 'cruel', 'world!'])
	test_mix_elems = mktest(mixdata, ['Hello', -32767, 'world!'])

	def test_type_count_lo(self):
		with self.assertRaises(XnbUnknownType):
			ObjectFactory(None, ['Microsoft.Xna.Framework.Content.ListReader`0[]'])

	def test_type_count_hi(self):
		with self.assertRaises(XnbUnknownType):
			ObjectFactory(None, ['Microsoft.Xna.Framework.Content.ListReader`2[[System.Byte],[System.Byte]]'])

class DictionaryTests(TestCase):
	def test_dict_uint_int(self):
		readers = ['DictionaryReader`2[[System.UInt16],[System.Int16]]']
		data = b'\x01\x03\x00\x00\x00\x37\x13\x39\x05\x00\x80\x80\x80\xff\xff\xff\xff'
		out = decode(readers, data)
		self.assertIsInstance(out, dict)
		self.assertEqual(len(out), 3)
		self.assertIn(4919, out)
		self.assertIn(32768, out)
		self.assertIn(65535, out)
		self.assertEqual(out[4919], 1337)
		self.assertEqual(out[32768], -32640)
		self.assertEqual(out[65535], -1)

	def test_dict_uint_str(self):
		readers = ['StringReader', 'DictionaryReader`2[[System.UInt16],[System.String]]']
		data = b'\x02\x02\x00\x00\x00\x00\x10\x01\x05Hello\x02\x10\x01\x07Goodbye'
		out = decode(readers, data)
		self.assertIsInstance(out, dict)
		self.assertEqual(len(out), 2)
		self.assertIn(4096, out)
		self.assertIn(4098, out)
		self.assertEqual(out[4096], 'Hello')
		self.assertEqual(out[4098], 'Goodbye')

	def test_dict_str_uint(self):
		readers = ['StringReader', 'DictionaryReader`2[[System.String],[System.UInt32]]']
		data = b'\x02\x02\x00\x00\x00\x01\x02AB\x10\x20\x30\x40\x01\x03CDE\x50\x60\x70\x80'
		out = decode(readers, data)
		self.assertIsInstance(out, dict)
		self.assertEqual(len(out), 2)
		self.assertIn('AB', out)
		self.assertIn('CDE', out)
		self.assertEqual(out['AB'], 0x40302010)
		self.assertEqual(out['CDE'], 0x80706050)

	def test_dict_str_str(self):
		readers = ['DictionaryReader`2[[System.String],[System.String]]', 'StringReader']
		data = (b'\x01\x03\x00\x00\x00' +
		        b'\x02\x02aa\x02\x02\xc3\xa5' +
		        b'\x02\x02ae\x02\x02\xc3\xa4' +
		        b'\x02\x02oe\x02\x02\xc3\xb6')
		out = decode(readers, data)
		self.assertIsInstance(out, dict)
		self.assertEqual(len(out), 3)
		self.assertIn('aa', out)
		self.assertIn('ae', out)
		self.assertIn('oe', out)
		self.assertEqual(out['aa'], 'å')
		self.assertEqual(out['ae'], 'ä')
		self.assertEqual(out['oe'], 'ö')

	def test_dict_str_mix(self):
		readers = ['DictionaryReader`2[[System.String],[System.Object]]', 'StringReader', 'UInt32Reader']
		data = (b'\x01\x03\x00\x00\x00' +
		        b'\x02\x02aa\x03\x00\x00\x00\x80' +
		        b'\x02\x03abc\x02\x03xyz' +
		        b'\x02\x03def\x03\x01\x00\x00\x80')
		out = decode(readers, data)
		self.assertIsInstance(out, dict)
		self.assertEqual(len(out), 3)
		self.assertIn('aa', out)
		self.assertIn('abc', out)
		self.assertIn('def', out)
		self.assertEqual(out['aa'], 1<<31)
		self.assertEqual(out['abc'], 'xyz')
		self.assertEqual(out['def'], 0x80000001)

	def test_dict_mix_mix(self):
		readers = ['DictionaryReader`2[[System.Object],[System.Object]]', 'StringReader', 'UInt32Reader']
		data = (b'\x01\x04\x00\x00\x00' +
		        b'\x03\x0a\x00\x00\x00\x03\x0b\x0c\x0d\x0e' +
		        b'\x02\x02xy\x03\xff\xff\x00\x00' +
		        b'\x02\x03xyz\x02\x06coords' +
		        b'\x03\x01\x00\x00\x80\x02\x02hi')
		out = decode(readers, data)
		self.assertIsInstance(out, dict)
		self.assertEqual(len(out), 4)
		self.assertIn('xy', out)
		self.assertIn('xyz', out)
		self.assertIn(10, out)
		self.assertIn(0x80000001, out)
		self.assertEqual(out['xy'], 65535)
		self.assertEqual(out['xyz'], 'coords')
		self.assertEqual(out[10], 0x0e0d0c0b)
		self.assertEqual(out[0x80000001], 'hi')

	def test_dict_duplicate_key(self):
		readers = ['DictionaryReader`2[[System.String],[System.UInt16]]', 'StringReader']
		data = b'\x01\x02\x00\x00\x00\x02\x02hi\x03\x01\x02\x02hi\x01\x02'
		with self.assertRaises(XnbInvalidPayload):
			decode(readers, data)

	def test_type_count_lo(self):
		with self.assertRaises(XnbUnknownType):
			ObjectFactory(None, ['Microsoft.Xna.Framework.Content.DictionaryReader`1[[System.Byte]]'])

	def test_type_count_hi(self):
		with self.assertRaises(XnbUnknownType):
			ObjectFactory(None, ['Microsoft.Xna.Framework.Content.DictionaryReader`3[[System.Byte],[System.Byte],[System.Byte]]'])
