# -*- coding: utf-8 -*-

import utf8
import urllib.request, urllib.parse, urllib.error
import saldo_util
import socket
import cjson
from mod_python import apache
from mod_python import util

host = "localhost"
sem_port = 8091
size = 2048


def function(format, segment):
    try:
        segment = segment.strip()
        if segment == "" and format == "html":
            return (
                saldo_util.html_document(
                    "SALDO", "<center><p>Mata in en ordform.</p></center>"
                ),
                apache.OK,
            )

        if format == "xml":
            result = xmlize(segment, result)
        elif format == "html":
            result = htmlize(segment, result)
        result_code = apache.OK
    except:
        result_code = apache.HTTP_SERVICE_UNAVAILABLE
    return (result, result_code)


def htmlize(segment, s):
    j = cjson.decode(utf8.d(s))
    content = (
        "<center><h1>"
        + segment
        + "</h1><p>"
        + saldo_util.sms_ref(segment, "sammansättningsanalys")
        + "</p>"
    )
    content += '<table border="1">'
    if j == []:
        content += "<tr><td>ordet saknas i lexikonet.</td></tr>"
    else:
        for json in j:
            content += "<tr><td>" + saldo_util.lexeme_ref(utf8.e(json["id"]))
            content += "</td><td>"
            content += saldo_util.lexeme_ref(utf8.e(json["fm"]))
            if (json["fp"]) != "PRIM..1":
                # content += '</td><td><b>far: </b>'
                content += " + " + saldo_util.lexeme_ref(utf8.e(json["fp"]))
            content += "</td><td>"
            content += saldo_util.gen_ref(
                utf8.e(json["p"]),
                utf8.e(json["gf"]),
                saldo_util.lemma_ref(utf8.e(json["l"])),
            )
            content += "</td>"
            content += "<td>" + saldo_util.korpus_ref([json["l"]], "korpus") + "</td>"
    content += "</tr></table></center>"
    html = saldo_util.html_document(segment, content)
    return html
