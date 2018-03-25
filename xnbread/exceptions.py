#!/usr/bin/env python3
#coding=utf8

class XnbReadError(Exception):
	''' base exception type for xnbread '''

class XnbInvalidPayload(XnbReadError):
	''' the payload we're trying to decode is invalid in some way '''
