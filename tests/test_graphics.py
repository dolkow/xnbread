#!/usr/bin/env python3
#coding=utf8

from unittest import TestCase
from .util import decode

class MathTests(TestCase):
	readers = ['Texture2DReader',
	           'EffectReader',
	           'SpriteFontReader',
	           'ArrayReader`1[[System.Byte]]',
	           'NullableReader`1[[System.Char]]',
	           'RectangleReader',
	           'Vector3Reader',
	           'ListReader`1[[Microsoft.Xna.Framework.Rectangle]]',
	           'ListReader`1[[Microsoft.Xna.Framework.Vector3]]',
	           'ListReader`1[[System.Char]]']

	def test_texture2d(self):
		data = (b'\x01\x05\x00\x00\x00' +
		        b'\x80\x00\x00\x00\x40\x00\x00\x00' +
		        b'\x02\x00\x00\x00' +
		        b'\x04\x00\x00\x00\x12\x34\x56\x78' + 
		        b'\x07\x00\x00\x00\x0a\x0b\x0c\x0d\x0e\x0f\x10')
		tex = decode(self.readers, data)
		self.assertEqual(tex.format, 5)
		self.assertEqual(tex.width, 128)
		self.assertEqual(tex.height, 64)
		self.assertEqual(len(tex.miplevels), 2)
		self.assertEqual(len(tex.miplevels[0]), 4)
		self.assertEqual(len(tex.miplevels[1]), 7)
		self.assertEqual(tex.miplevels[0][0], 0x12)
		self.assertEqual(tex.miplevels[0][1], 0x34)
		self.assertEqual(tex.miplevels[0][2], 0x56)
		self.assertEqual(tex.miplevels[0][3], 0x78)
		self.assertEqual(tex.miplevels[1][0], 0xa)
		self.assertEqual(tex.miplevels[1][1], 0xb)
		self.assertEqual(tex.miplevels[1][2], 0xc)
		self.assertEqual(tex.miplevels[1][3], 0xd)
		self.assertEqual(tex.miplevels[1][4], 0xe)
		self.assertEqual(tex.miplevels[1][5], 0xf)
		self.assertEqual(tex.miplevels[1][6], 0x10)

	def test_effect(self):
		data = b'\x02\x05\x00\x00\x00\x40\x42\x45\x49\x4f'
		out = decode(self.readers, data)
		self.assertEqual(len(out.bytecode), 5)
		self.assertEqual(out.bytecode[0], 0x40)
		self.assertEqual(out.bytecode[1], 0x42)
		self.assertEqual(out.bytecode[2], 0x45)
		self.assertEqual(out.bytecode[3], 0x49)
		self.assertEqual(out.bytecode[4], 0x4f)

	def test_spritefont(self):
		data = (b'\x03' +
				# Texture
		        b'\x01\x02\x00\x00\x00' +
		        b'\x20\x00\x00\x00\x00\x01\x00\x00' +
		        b'\x01\x00\x00\x00' +
		        b'\x03\x00\x00\x00\x71\x63\x56' +
		        # List<Rectangle>
		        b'\x08\x01\x00\x00\x00' +
		        b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10' +
		        # List<Rectangle>
		        b'\x08\x01\x00\x00\x00' +
		        b'\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20' +
		        # List<Char>
		        b'\x0a\x01\x00\x00\x00A' +
		        # v/h spacing
		        b'\xff\xff\xff\xff\x00\x00\x80\xbf' +
		        # List<Vector3>
		        b'\x09\x01\x00\x00\x00' +
		        b'\x00\x00\x00\xbf\x00\x00\x80\xbe\x00\x00\x00\xbe' +
		        # Nullable<Char>
		        b'\x00')
		font = decode(self.readers, data)
		self.assertEqual(font.texture.format, 2)
		self.assertEqual(font.texture.width, 32)
		self.assertEqual(font.texture.height, 256)
		self.assertEqual(len(font.texture.miplevels), 1)
		self.assertEqual(len(font.texture.miplevels[0]), 3)
		self.assertEqual(font.texture.miplevels[0], b'\x71\x63\x56')
		self.assertEqual(len(font.glyphs), 1)
		self.assertEqual(font.glyphs[0].x, 0x04030201)
		self.assertEqual(font.glyphs[0].y, 0x08070605)
		self.assertEqual(font.glyphs[0].w, 0x0c0b0a09)
		self.assertEqual(font.glyphs[0].h, 0x100f0e0d)
		self.assertEqual(len(font.crop), 1)
		self.assertEqual(font.crop[0].x, 0x14131211)
		self.assertEqual(font.crop[0].y, 0x18171615)
		self.assertEqual(font.crop[0].w, 0x1c1b1a19)
		self.assertEqual(font.crop[0].h, 0x201f1e1d)
		self.assertEqual(len(font.charmap), 1)
		self.assertEqual(font.charmap[0], 'A')
		self.assertEqual(font.vspace, -1)
		self.assertEqual(font.hspace, -1.0)
		self.assertEqual(len(font.kerning), 1)
		self.assertEqual(font.kerning[0].x, -0.5)
		self.assertEqual(font.kerning[0].y, -0.25)
		self.assertEqual(font.kerning[0].z, -0.125)
		self.assertIsNone(font.defchar)
