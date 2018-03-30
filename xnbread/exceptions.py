#!/usr/bin/env python3
#coding=utf8

class XnbReadError(Exception):
	''' base exception type for xnbread '''

class XnbInvalidHeader(XnbReadError):
	''' the file data we're trying to decode had an unexpected header '''

class XnbInvalidPayload(XnbReadError):
	''' the payload we're trying to decode is invalid in some way '''

class XnbUnknownType(XnbReadError):
	''' tried to read a type we don't know about '''

class XnbConfigError(XnbReadError):
	''' tried set up xnbread in some weird way '''
