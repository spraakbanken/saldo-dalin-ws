# -*- coding: utf-8 -*-

import utf8
import socket
import saldo_util
import pos_list
import cjson
from mod_python import apache
from mod_python import util 

host = "localhost"
sem_port = 8091
size = 2048 

def function(format):
    result = ''
    result_code=apache.OK
    if format == 'xml':
         xs = cjson.decode(utf8.d(pos_list.pos))
         result = xmlize(xs)
    elif format == 'json':
        result = pos_list.pos
    elif format == 'html':
        xs = cjson.decode(utf8.d(pos_list.pos))
        result = htmlize(xs)
    return (result,result_code)

def xmlize(xs):
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<result>\n'
    for x in xs:
        xml += '<pos>' + x + '</pos>\n'
    xml += '</result>\n'
    return utf8.e(xml)

def htmlize(xs):
    content =  ' <center>'
    content += ', '.join([utf8.e(x) for x in xs])
    content += '</center>\n'
    html = saldo_util.html_document("pos",content,bar=False)
    return html
