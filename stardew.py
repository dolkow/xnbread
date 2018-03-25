#!/usr/bin/env python3
#coding=utf8

# this file contains non-standard types found in Stardew Valley's XNB files.

import xnbread

from xnbread.readers import *
from xnbread.readers.basic import _read_str, _u32

def _bmxml(factory):
	# TODO: parse this xml? Nahhh.
	return _read_str(factory)
add_reader(_bmxml, 'BmFont.XmlSourceReader')

def _xtile(factory):
	nbytes = _u32(factory)
	return factory.stream.read_bytes(nbytes).tobytes()
add_reader(_xtile, 'xTile.Pipeline.TideReader')


if __name__ == '__main__':
	import sys
	for filename in sys.argv[1:]:
		with open(filename, 'rb') as f:
			xnbread.dump(f)
