# -*- coding: utf-8 -*-
#!/usr/bin/env python

from xml.dom.minidom import parseString
import urllib.request, urllib.error, urllib.parse
import saldo_util
import urllib.request, urllib.parse, urllib.error
import re


def sblex(sense):
    senses = "|".join([saldo.encode("UTF-8") for saldo in saldo_util.lookup_md1(sense)])
    sblex_address = "http://demosb.spraakdata.gu.se/ws/lexikon"
    params = {}
    params["lexikon"] = "dalin"
    params["saldo"] = senses
    data = urllib.parse.urlencode(params)
    req = urllib.request.Request(sblex_address, data)
    content = urllib.request.urlopen(req).read()
    dom = parseString(content)
    result = []
    for entry in dom.getElementsByTagName("LexicalEntry"):
        eid = entry.getElementsByTagName("eid")[0].childNodes[0].data
        wfs = set()
        for wf in entry.getElementsByTagName("wf"):
            wfs.add(wf.childNodes[0].data)
        result.append((eid, list(wfs)))
    return result
