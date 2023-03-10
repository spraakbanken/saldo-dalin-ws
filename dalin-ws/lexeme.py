# -*- coding: utf-8 -*-

import utf8
import socket
import saldo_util
import cjson
from mod_python import apache
from mod_python import util

host = "localhost"
sem_port = 8093
size = 2048


def function(format, lexeme):
    result = ""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, sem_port))
        s.send("lex " + lexeme)
        buff = ""
        while True:
            buff = s.recv(size)
            if len(buff) == 0:
                break
            result += buff
        s.close()
        result_code = apache.OK
    except:
        result_code = apache.HTTP_SERVICE_UNAVAILABLE
    if format == "xml":
        result = xmlize(result)
    elif format == "html":
        result = htmlize(lexeme, result)
    return (result, result_code)


def xmlize(s):
    j = cjson.decode(utf8.d(s))
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += "<result>\n"
    for l in j:
        xml += "<l>%s</l>" % l
    xml += "</result>\n"
    return utf8.e(xml)


def htmlize(lexeme, s):
    j = cjson.decode(utf8.d(s))
    if j == []:
        result = '<center><p>"%s" saknas.</p></center>' % (lexem)
    else:
        result = '<center><table border="1">'
        for l in j:
            result += "<tr><td>%s</td></tr>" % saldo_util.lemma_hrefx(l.encode("UTF-8"))
        result += "</table></center>"
    return saldo_util.html_document(lexeme, result)
