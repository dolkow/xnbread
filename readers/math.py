#!/usr/bin/env python3
#coding=utf8

from . import add_reader
from .basic import _i32, _single

from collections import namedtuple as _nt

Vector3 = _nt('Vector3', 'x y z')
def _vector3(factory):
	return Vector3(_single(factory), _single(factory), _single(factory))
add_reader(_vector3, 'Microsoft.Xna.Framework.Content.Vector3Reader', 'Microsoft.Xna.Framework.Vector3', True)

Rectangle = _nt('Rectangle', 'x y w h')
def _rectangle(factory):
	return Rectangle(_i32(factory), _i32(factory), _i32(factory), _i32(factory))
add_reader(_rectangle, 'Microsoft.Xna.Framework.Content.RectangleReader', 'Microsoft.Xna.Framework.Rectangle', True)
