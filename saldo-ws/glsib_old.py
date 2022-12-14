# -*- coding: utf-8 -*-

import utf8
import socket
import saldo_util
import cjson
from mod_python import apache
from mod_python import util 

host = "localhost"
sem_port = 8091
size = 2048 

def function(format,lemma):
    result = ''
    result_code=apache.OK
    xs = []
    try:
        xs=saldo_util.glsib(lemma)
        result = jsonize(xs)
    except:
        result_code=apache.HTTP_SERVICE_UNAVAILABLE
    return (result,result_code)

def jsonize(xss):
    result= []
    for (s,xs) in xss:
        result.append(
            ('{"sense":"%s","rel":[' % s) + 
            ",".join(['"' + x + '"' for x in xs]) + 
            ']}')
    return utf8.e('[' + ", ".join(result) + ']')
