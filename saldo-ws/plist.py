# -*- coding: utf-8 -*-

import utf8
import socket
import saldo_util
import paradigms_list
import cjson
from mod_python import apache
from mod_python import util

host = "localhost"
sem_port = 8091
size = 2048


def function(format):
    result = ""
    result_code = apache.OK
    if format == "xml":
        xs = cjson.decode(utf8.d(paradigms_list.paradigms))
        result = xmlize(xs)
    elif format == "json":
        result = paradigms_list.paradigms
    elif format == "html":
        xs = cjson.decode(utf8.d(paradigms_list.paradigms))
        result = htmlize(xs)
    return (result, result_code)


def xmlize(xs):
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += "<result>\n"
    for x in xs:
        xml += "<p>" + x + "</p>\n"
    xml += "</result>\n"
    return utf8.e(xml)


def htmlize(xs):
    content = " <center>"
    content += ", ".join([utf8.e(x) for x in xs])
    content += "</center>\n"
    html = saldo_util.html_document("paradigm", content, bar=False)
    return html
