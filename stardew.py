#!/usr/bin/env python3
#coding=utf8

# this file contains non-standard types found in Stardew Valley's XNB files.

from readers import *
from readers.basic import _read_str

def _bmxml(factory):
	# TODO: parse this xml? Nahhh.
	return _read_str(factory)
add_reader(_bmxml, 'BmFont.XmlSourceReader')
