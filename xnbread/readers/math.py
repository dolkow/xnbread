#!/usr/bin/env python3
#coding=utf8

from . import *

from collections import namedtuple as _nt

Vector3 = _nt('Vector3', 'x y z')
def vector3(factory):
	return Vector3(single(factory), single(factory), single(factory))
add_reader(vector3, 'Microsoft.Xna.Framework.Content.Vector3Reader', 'Microsoft.Xna.Framework.Vector3', True)

Rectangle = _nt('Rectangle', 'x y w h')
def rectangle(factory):
	return Rectangle(i32(factory), i32(factory), i32(factory), i32(factory))
add_reader(rectangle, 'Microsoft.Xna.Framework.Content.RectangleReader', 'Microsoft.Xna.Framework.Rectangle', True)
