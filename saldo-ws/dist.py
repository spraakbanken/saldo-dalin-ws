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

def function(format,senses):
    result = ''
    result_code=apache.OK
    xs = []
    try:
        xs = saldo_util.distances(senses.split(' '))
    except:
        result_code=apache.HTTP_SERVICE_UNAVAILABLE
    if format == 'xml':
        result = xmlize(xs)
    elif format == 'json':
        result = jsonize(xs)
    elif format == 'html':
        result = htmlize(senses,xs)
    return (result,result_code)

def xmlize(xs):
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<result>\n'
    for (d,s1,s2) in xs:
        xml += '<dist><l>' + s1 + '</l><l>'+s2+'</l><d>' + str(d) + '</d></dist>\n'
    xml += '</result>\n'
    return xml

def jsonize(xs):
    dstrs = []
    for (d,s1,s2) in xs:
        dstrs.append(' ["' + s1 + '", "' + s2 +'", '+ str(d) + ']')
    return '[\n' + ",\n".join(dstrs) + '\n]'

def htmlize(lid,xs):
    content =  ' <center><table border="1">'
    col = 0
    for (d,s1,s2) in xs:
        content += '<tr><td>' + saldo_util.lexeme_ref(s1) + '</td><td>' + saldo_util.lexeme_ref(s2) + '</td><td style="text-align:right;">' + str(d)+ '</tr>'
    content += '</table></center>\n'
    html = saldo_util.html_document(lid,content,bar=False)
    return html
