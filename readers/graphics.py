#!/usr/bin/env python3
#coding=utf8

from . import add_reader

from collections import namedtuple as _nt

Texture2d = _nt('Texture2d', 'format width height miplevels')
def _read_texture2d(factory):
	fmt = factory.stream.read_u32()
	w = factory.stream.read_u32()
	h = factory.stream.read_u32()
	n = factory.stream.read_u32()
	mips = n * [None]
	for i in range(n):
		dsize = factory.stream.read_u32()
		mips[i] = factory.stream.read_bytes(dsize)
	return Texture2d(fmt, w, h, mips)
add_reader(_read_texture2d, 'Microsoft.Xna.Framework.Content.Texture2DReader')
