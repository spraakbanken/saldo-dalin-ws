# -*- coding: utf-8 -*-

import utf8
import socket
import saldo_util
import cjson
from mod_python import apache
from mod_python import util
import sblex

host = "localhost"
sem_port = 8091
size = 2048


def function(format, lexeme):
    result = ""
    result_code = apache.OK
    try:
        xs = sblex.sblex(lexeme)
        if format == "xml":
            result = xmlize(xs)
        elif format == "json":
            result = jsonize(xs)
        elif format == "html":
            result = htmlize(lexeme, xs)
        return (result, result_code)
    except:
        return (result, result_code)


def xmlize(xs):
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += "<result>\n"
    for (x, wfs) in xs:
        xml += " <eid>" + x + "</eid>\n"
        xml += (
            "  <forms>\n"
            + "".join(["   <form>" + w + "</form>\n" for w in wfs])
            + "  </forms>\n"
        )
    xml += "</result>\n"
    return utf8.e(xml)


def jsonize(xs):
    return utf8.e("[" + ",".join(['"' + x + '"' for (x, _) in xs]) + "]")


def htmlize(lid, xs):
    content = ' <center><table border="1"><tr><td>'
    col = 0
    for (eid, wfs) in xs:
        ref = utf8.e(saldo_util.lemma_ref(eid))
        content += saldo_util.korpus_wf_ref(wfs, ref) + "</td>"
        col += 1
        if col == 10:
            content += "</tr><tr><td>"
            col = 0
        else:
            content += "<td>"
    content += "</td></tr></table></center>\n"
    html = saldo_util.html_document(lid, content)
    return html


# korpus_ref
