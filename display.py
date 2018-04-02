#!/usr/bin/env python3
#coding=utf8

import xnbread
import os
import PIL.Image
import sys

for path in sys.argv[1:]:
	with open(path, 'rb') as f:
		payload = xnbread.read_payload(f)
		tex = xnbread.decode_payload(payload)
		if not isinstance(tex, xnbread.readers.Texture2d):
			print('%s: Data is %s; need Texture2d' % (path, type(tex)))
			continue
		if tex.format != 0:
			print('%s: buffer format is %d; can only handle plain ARGB (0)' % (path, tex.format))
			continue
		if len(tex.miplevels) != 1:
			print('%s: too many miplevels' % path)
			continue
		img = PIL.Image.frombuffer('RGBA', (tex.width, tex.height), tex.miplevels[0], 'raw', 'RGBA', 0, 1)
		img.show(title=os.path.basename(path))
