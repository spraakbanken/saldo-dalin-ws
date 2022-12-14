# -*- mode: python; coding: utf-8 -*-
# $Id: util.py 65360 2013-01-16 16:55:42Z cjs $

import cgi

import sys

class FieldStorage(cgi.FieldStorage):
    def __init__(self, req):
        cgi.FieldStorage.__init__(self, environ = req.environ)

    def __getitem__(self, key):
        return cgi.FieldStorage.__getitem__(self, key).value
