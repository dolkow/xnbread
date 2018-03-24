#!/usr/bin/env python3
#coding=utf8

# this file contains non-standard types found in Stardew Valley's XNB files.

from readers import *
from readers.basic import _read_str, _u32

def _bmxml(factory):
	# TODO: parse this xml? Nahhh.
	return _read_str(factory)
add_reader(_bmxml, 'BmFont.XmlSourceReader')

def _xtile(factory):
	nbytes = _u32(factory)
	return factory.stream.read_bytes(nbytes).tobytes()
add_reader(_xtile, 'xTile.Pipeline.TideReader')
