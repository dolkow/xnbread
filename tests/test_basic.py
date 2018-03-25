#!/usr/bin/env python3
#coding=utf8

from unittest import TestCase
from .util import decode

def mktest(data, expected):
	def decodetest(tcase):
		out = decode(tcase.readers, data)
		tcase.assertEqual(out, expected)
	return decodetest


class NullTests(TestCase):
	def test_null(self):
		self.assertIsNone(decode(['StringReader'], b'\x00'))


class ReaderVariations(TestCase):
	def test_no_readers(self):
		self.assertIsNone(decode([], b'\x00'))

	def test_extra_reader_1(self):
		self.assertEqual(decode(['ByteReader', 'CharReader'], b'\x01A'), 65)

	def test_extra_reader_2(self):
		self.assertEqual(decode(['CharReader', 'ByteReader'], b'\x02A'), 65)


class ByteTests(TestCase):
	readers = ['ByteReader']
	test_byte_a   = mktest(b'\x01A', 65)
	test_byte_b   = mktest(b'\x01B', 66)
	test_byte_min = mktest(b'\x01\x00', 0)
	test_byte_max = mktest(b'\x01\xff', 255)


class SByteTests(TestCase):
	readers = ['SByteReader']
	test_sbyte_min  = mktest(b'\x01\x80', -128)
	test_sbyte_max  = mktest(b'\x01\x7f', 127)
	test_sbyte_neg1 = mktest(b'\x01\xff', -1)
	test_sbyte_73   = mktest(b'\x01\x49', 73)


class Int16Tests(TestCase):
	readers = ['Int16Reader']
	test_i16_min  = mktest(b'\x01\x00\x80', -32768)
	test_i16_max  = mktest(b'\x01\xff\x7f', 32767)
	test_i16_neg1 = mktest(b'\x01\xff\xff', -1)
	test_i16_val  = mktest(b'\x01\x02\x03', 0x302)


class UInt16Tests(TestCase):
	readers = ['UInt16Reader']
	test_u16_min = mktest(b'\x01\x00\x00', 0)
	test_u16_max = mktest(b'\x01\xff\xff', 65535)
	test_u16_mid = mktest(b'\x01\x00\x80', 32768)
	test_u16_val = mktest(b'\x01\x02\x03', 0x302)


class Int32Tests(TestCase):
	readers = ['Int32Reader']
	test_i32_min  = mktest(b'\x01\x00\x00\x00\x80', -1 << 31)
	test_i32_max  = mktest(b'\x01\xff\xff\xff\x7f', (1 << 31) - 1)
	test_i32_neg1 = mktest(b'\x01\xff\xff\xff\xff', -1)
	test_i32_val  = mktest(b'\x01\x02\x03\x04\x05', 0x5040302)


class UInt32Tests(TestCase):
	readers = ['UInt32Reader']
	test_u32_min = mktest(b'\x01\x00\x00\x00\x00', 0)
	test_u32_max = mktest(b'\x01\xff\xff\xff\xff', (1 << 32) - 1)
	test_u32_mid = mktest(b'\x01\x00\x00\x00\x80', 1 << 31)
	test_u32_val = mktest(b'\x01\x02\x03\x04\x05', 0x05040302)


class Int64Tests(TestCase):
	readers = ['Int64Reader']
	test_i64_min  = mktest(b'\x01\x00\x00\x00\x00\x00\x00\x00\x80', -1 << 63)
	test_i64_max  = mktest(b'\x01\xff\xff\xff\xff\xff\xff\xff\x7f', (1 << 63) - 1)
	test_i64_neg1 = mktest(b'\x01\xff\xff\xff\xff\xff\xff\xff\xff', -1)
	test_i64_val  = mktest(b'\x01\x02\x03\x04\x05\x06\x07\x08\x09', 0x0908070605040302)


class UInt64Tests(TestCase):
	readers = ['UInt64Reader']
	test_u64_min = mktest(b'\x01\x00\x00\x00\x00\x00\x00\x00\x00', 0)
	test_u64_max = mktest(b'\x01\xff\xff\xff\xff\xff\xff\xff\xff', (1 << 64) - 1)
	test_u64_mid = mktest(b'\x01\x00\x00\x00\x00\x00\x00\x00\x80', 1 << 63)
	test_u64_val = mktest(b'\x01\x02\x03\x04\x05\x06\x07\x08\x09', 0x0908070605040302)


class SingleTests(TestCase):
	readers = ['SingleReader']
	test_single_one = mktest(b'\x01\x00\x00\x80\x3f', 1.0)
	test_single_neg = mktest(b'\x01\x00\x00\x80\xbf', -1.0)


class DoubleTests(TestCase):
	readers = ['DoubleReader']
	test_double_one = mktest(b'\x01\x00\x00\x00\x00\x00\x00\xf0\x3f', 1.0)
	test_double_neg = mktest(b'\x01\x00\x00\x00\x00\x00\x00\xf0\xbf', -1.0)


class BooleanTests(TestCase):
	readers = ['BooleanReader']
	test_bool_false = mktest(b'\x01\x00', False)
	test_bool_true  = mktest(b'\x01\x01', True)


class CharTests(TestCase):
	readers = ['CharReader']
	test_charA       = mktest(b'\x01A', 'A')
	test_charAt      = mktest(b'\x01@', '@')
	test_charSwedish = mktest(b'\x01' + bytes('Ö', 'utf8'), 'Ö')
	test_charKanji   = mktest(b'\x01' + bytes('漢', 'utf8'), '漢')
	test_charEmoji   = mktest(b'\x01' + bytes('🤔', 'utf8'), '🤔')


class StringTests(TestCase):
	readers = ['StringReader']
	longstr = 'Ett två tre fyra fem sex sju åtta nio tio elva tolv tretton fjorton femton sexton sjutton arton nitton tjugo tjugoett tjugotvå'
	test_stringEmpty = mktest(b'\x01\x00', '')
	test_stringHello = mktest(b'\x01\x0cHello world!', 'Hello world!')
	test_stringLong  = mktest(b'\x01\x81\x01' + bytes(longstr, 'utf8'), longstr)
	test_stringKanji = mktest(b'\x01\x06' + bytes('漢字', 'utf8'), '漢字')



