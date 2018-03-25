#!/usr/bin/env python3
#coding=utf8

from . import *

from collections import namedtuple as _nt

Texture2d = _nt('Texture2d', 'format width height miplevels')
def texture2d(factory):
	fmt = u32(factory)
	w = u32(factory)
	h = u32(factory)
	n = u32(factory)
	mips = n * [None]
	for i in range(n):
		dsize = u32(factory)
		mips[i] = factory.stream.read_bytes(dsize)
	return Texture2d(fmt, w, h, mips)
add_reader(texture2d, 'Microsoft.Xna.Framework.Content.Texture2DReader', 'Microsoft.Xna.Framework.Graphics.Texture2D')

Effect = _nt('Effect', 'bytecode')
def effect(factory):
	return Effect(genericlist(byte, factory))
add_reader(effect, 'Microsoft.Xna.Framework.Content.EffectReader', 'Microsoft.Xna.Framework.Graphics.Effect')


SpriteFont = _nt('SpriteFont', 'texture glyphs crop charmap vspace hspace kerning defchar')
def spritefont(factory):
	return SpriteFont(factory.read(), factory.read(),
		factory.read(), factory.read(),
		i32(factory), single(factory),
		factory.read(), nullable(char, factory))
add_reader(spritefont, 'Microsoft.Xna.Framework.Content.SpriteFontReader', 'Microsoft.Xna.Framework.Graphics.SpriteFont')

