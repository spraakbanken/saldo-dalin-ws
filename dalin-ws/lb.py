# -*- coding: utf-8 -*-

import conplisit
import utf8
import os
import codecs
from mod_python import apache
from mod_python import util
import popen2
import cjson
import saldo_util


def function(format, sense, hits=50):
    if format == "html":
        try:
            content = "<center>" + conplisit.table(sense, hits) + "</center>"
            result = saldo_util.html_document(sense.decode("UTF-8"), content)
            result_code = apache.OK
        except:
            result = saldo_util.html_document(
                sense.decode("UTF-8"), ("<center><p>Ett fel uppstod.</p></center>")
            )
            result_code = apache.OK
    else:
        result = ""
        result_code = apache.HTTP_NOT_FOUND
    return (utf8.e(result), result_code)
