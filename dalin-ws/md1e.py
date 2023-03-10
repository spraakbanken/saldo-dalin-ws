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


def function(format, lexeme):
    result = ""
    result_code = apache.OK
    xs = []
    #    try:
    xs = saldo_util.md1e(lexeme)
    #    except:
    #        result_code=apache.HTTP_SERVICE_UNAVAILABLE
    if format == "xml":
        result = xmlize(xs)
    elif format == "json":
        result = jsonize(xs)
    elif format == "html":
        result = htmlize(lexeme, xs)
    return (result, result_code)


def xmlize(xs):
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += "<result>\n"
    for x in xs:
        xml += " <e>"
        xml += "  <eid>" + x + "</eid>"
        xml += (
            "  <forms>\n"
            + "".join(
                [
                    "   <form>" + w + "</form>\n"
                    for w in saldo_util.generate_wordforms(x)
                ]
            )
            + "  </forms>\n"
        )
        xml += " </e>\n"
    xml += "</result>\n"
    return utf8.e(xml)


def jsonize(xs):
    return utf8.e("[" + ",".join(['"' + x + '"' for x in xs]) + "]")


def htmlize(lid, xs):
    content = " <center>"
    content += ", ".join([saldo_util.lemma_href(utf8.e(x)) for x in xs])
    content += "</center>\n"
    html = saldo_util.html_document(lid, content, bar=False)
    return html
