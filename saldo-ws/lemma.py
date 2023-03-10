# -*- coding: utf-8 -*-

import utf8
import saldo_util
import socket
import cjson
import table
from mod_python import apache
from mod_python import util


def xmlize(s):
    j = cjson.decode(utf8.d(s))
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += "<result>\n"
    if not (j == []):
        xml += " <gf>" + j["gf"] + "</gf>\n"
        xml += " <p>" + j["p"] + "</p>\n"
        xml += " <ls>\n"
        for l in j["l"]:
            xml += "   <l>" + l + "</l>\n"
        xml += " </ls>\n"
    xml += "</result>\n"
    return utf8.e(xml)


def htmlize(lid, s):
    j = cjson.decode(utf8.d(s))
    if not (j == []):
        return table.function("html", utf8.e(j["p"]), utf8.e(j["gf"]))[0]
    else:
        content = "<center><p><b>" + lid + " finns ej.</b></p></center>"
        html = saldo_util.html_document(lid, content, bar=False)
        return html
