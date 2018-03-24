#!/usr/bin/env python3
#coding=utf8

from . import add_reader

from .basic import _boolean, _char, _i32, _u32, _single
from .system import _nullable

from collections import namedtuple as _nt

Texture2d = _nt('Texture2d', 'format width height miplevels')
def _read_texture2d(factory):
	fmt = _u32(factory)
	w = _u32(factory)
	h = _u32(factory)
	n = _u32(factory)
	mips = n * [None]
	for i in range(n):
		dsize = _u32(factory)
		mips[i] = factory.stream.read_bytes(dsize)
	return Texture2d(fmt, w, h, mips)
add_reader(_read_texture2d, 'Microsoft.Xna.Framework.Content.Texture2DReader', 'Microsoft.Xna.Framework.Graphics.Texture2D')


SpriteFont = _nt('SpriteFont', 'texture glyphs crop charmap vspace hspace kerning defchar')
def _read_spritefont(factory):
	return SpriteFont(factory.read(), factory.read(),
		factory.read(), factory.read(),
		_i32(factory), _single(factory),
		factory.read(), _nullable(_char, factory))
add_reader(_read_spritefont, 'Microsoft.Xna.Framework.Content.SpriteFontReader', 'Microsoft.Xna.Framework.Graphics.SpriteFont')

