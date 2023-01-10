

import logging

from fastapi import FastAPI

from webapp.api import saldo_ws
# from handler import handler

logger = logging.getLogger(__name__)

logger.info('loading application ...')

def create_app():
   app = FastAPI()

   app.include_router(saldo_ws.api)
   return app

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
