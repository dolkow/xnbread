#!/usr/bin/env python3
#coding=utf8

from io import BytesIO
from unittest import TestCase

from .util import decode, mktest

from xnbread import read_payload
from xnbread.exceptions import XnbInvalidHeader

def mktest(expected, basedata, *replacements):
	data = bytearray(basedata)
	for ix, v in replacements:
		data[ix] = v
	if type(expected) is type:
		def testfunc(self):
			with self.assertRaises(expected):
				read_payload(BytesIO(data))
	else:
		def testfunc(self):
			payload = read_payload(BytesIO(data))
			self.assertEqual(payload, expected)
	return testfunc

class ContainerTests(TestCase):
	valid_data = b'XNBw\x05\x01\x10\x00\x00\x00Hello!'

	test_valid    = mktest(b'Hello!', valid_data)
	test_target_m = mktest(b'Hello!', valid_data, (3, ord('m')))
	test_target_x = mktest(b'Hello!', valid_data, (3, ord('x')))
	test_target_y = mktest(XnbInvalidHeader, valid_data, (3, ord('y')))

	test_wrong_magic   = mktest(XnbInvalidHeader, valid_data, (2, 98))
	test_wrong_version = mktest(XnbInvalidHeader, valid_data, (4, 6))

	test_flag_0   = mktest(b'Hello!',        valid_data, (5,   0))
	test_flag_1   = mktest(b'Hello!',        valid_data, (5,   1))
	test_flag_2   = mktest(XnbInvalidHeader, valid_data, (5,   2))
	test_flag_4   = mktest(XnbInvalidHeader, valid_data, (5,   4))
	test_flag_8   = mktest(XnbInvalidHeader, valid_data, (5,   8))
	test_flag_16  = mktest(XnbInvalidHeader, valid_data, (5,  16))
	test_flag_32  = mktest(XnbInvalidHeader, valid_data, (5,  32))
	test_flag_64  = mktest(XnbInvalidHeader, valid_data, (5,  64))

	test_short_data = mktest(XnbInvalidHeader, valid_data[:-1])
