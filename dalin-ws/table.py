# -*- coding: utf-8 -*-

import utf8
import os
import codecs
from mod_python import apache
from mod_python import util
import popen2
import cjson
import saldo_util


def function(format, paradigm, word):
    result = ""
    try:
        dalin = 'export LC_ALL="sv_SE.UTF-8";/home/markus/fm/sblex/bin/dalin -i'
        input = paradigm + ' "' + word + '";'
        fin, fout = popen2.popen2(dalin)
        fout.write(input)
        fout.close()
        for line in fin.readlines():
            result += line
        if result.strip() == "":
            result = "[]"
        j = cjson.decode(utf8.d(result))
        if format == "html":
            result = htmlize(paradigm, word, j)
        elif format == "json":
            result = "[\n"
            result += ",\n".join(
                [
                    '{"form":"%s","gf":"%s","pos":"%s","is":[%s],"msd":"%s","p":"%s"}'
                    % (
                        x["word"],
                        x["head"],
                        x["pos"],
                        ", ".join(['"%s"' % (i) for i in x["inhs"]]),
                        x["param"],
                        utf8.d(paradigm),
                    )
                    for x in j
                ]
            )
            result += "\n]"
        elif format == "xml":
            result = xmlize(paradigm, j)
        result_code = apache.OK
    except:
        result_code = apache.HTTP_SERVICE_UNAVAILABLE
    return (utf8.e(result), result_code)


def xmlize(paradigm, j):
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += "<result>\n"
    xml += "<table>\n"
    xml += "\n".join(
        [
            "<w><form>%s</form><gf>%s</gf><pos>%s</pos><is>%s</is><msd>%s</msd><p>%s</p></w>"
            % (
                x["word"],
                x["head"],
                x["pos"],
                " ".join(x["inhs"]),
                x["param"],
                utf8.d(paradigm),
            )
            for x in j
        ]
    )
    xml += "</table>\n"
    xml += "</result>\n"
    return xml


def htmlize(paradigm, word, j):
    if j == []:
        content = (
            "<center><p><b>paradigm " + utf8.d(paradigm) + " finns ej.</b></p></center>"
        )
        return saldo_util.html_document(
            utf8.d(paradigm) + ' "' + utf8.d(word) + '"', content
        )
    content = '<center><table border="1"><tr><td><b>%s</b></td><td>%s</td></tr>' % (
        "word class",
        j[0]["pos"],
    )
    if len(j[0]["inhs"]) > 0:
        content += "<tr><td><b>%s</b></td><td>%s</td></tr>" % (
            "inherent feature(s)",
            ", ".join(j[0]["inhs"]),
        )
    content += '<tr><th colspan="2"><b>inflection table</b></tr>'
    data = group_msd(j)
    prev = ""
    for x in j:
        msd = x["param"]
        if msd != prev:
            data[msd].reverse()
            content += "<tr><td><i>%s</i></td><td>%s</td></tr>" % (
                msd,
                "/".join(data[msd]),
            )
            prev = msd
    content += "</table></center>"
    return saldo_util.html_document(
        j[0]["p"] + ' "' + j[0]["head"] + '"', content, bar=False
    )


def group_msd(j):
    dict = {}
    for x in j:
        msd = x["param"]
        wf = x["word"]
        if msd in dict:
            dict[msd].append(wf)
        else:
            dict[msd] = [wf]
    return dict
