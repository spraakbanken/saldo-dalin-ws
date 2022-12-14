# -*- mode: python; coding: utf-8 -*-
# $Id: index.wsgi 65360 2013-01-16 16:55:42Z cjs $

# WSGI-wrapper för saldo-ws

import os, sys
# FIXA: Fult som fan. Kanske ok i egen WSGI-server?
if os.path.dirname(__file__) not in sys.path:
   sys.path.insert(0, os.path.dirname(__file__))

from handler import handler

print('loading application ...')

def application(environ, start_response):
   print('environ = %s' % environ)
   req = SaldoRequest(environ)
   status = handler(req)
   start_response(status, req.getHeaders())
   return [req.getOutput()]

class SaldoRequest:
   def __init__(self, environ):
      self.output = []
      self.headers_out = {}
      self.environ = environ

   def getOutput(self):
      return ''.join(self.output)

   def getHeaders(self):
      if (hasattr(self, 'content_type')):
         self.headers_out['Content-Type'] = self.content_type
      return [(k, self.headers_out[k]) for k in self.headers_out]

   def write(self, str):
      self.output.append(str)

   def send_http_header(self):
      pass
