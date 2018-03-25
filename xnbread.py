#!/usr/bin/env python3
#coding=utf8

from xnbread import dump

if __name__ == '__main__':
	import sys
	raw = False
	for filename in sys.argv[1:]:
		if filename == '-r':
			raw = True
			continue
		with open(filename, 'rb') as f:
			dump(f, raw)
