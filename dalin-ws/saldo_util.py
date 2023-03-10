# -*- coding: utf-8 -*-

import utf8
import urllib.request, urllib.parse, urllib.error
import cjson
from mod_python import apache
from mod_python import util
from xml.dom.minidom import parseString


def dalin_exist(word):
    url = (
        "http://litteraturbanken.se/query/dalin.xql?word=%s&limit=10"
        % urllib.parse.quote(word)
    )
    s = urllib.request.urlopen(url).read()
    dom = parseString(s)
    return "\n".join(
        [n.toxml() for n in dom.getElementsByTagName("body")[0].childNodes]
    )


def lookup_ff(s):
    url = "http://spraakbanken.gu.se/ws/dalin-ws/ff/json/"
    f = urllib.request.urlopen(url + urllib.parse.quote(s))
    return cjson.decode(utf8.d(f.read()))["a"]


def lookup_fl(s):
    url = "http://spraakbanken.gu.se/ws/dalin-ws/fl/json/"
    f = urllib.request.urlopen(url + urllib.parse.quote(s))
    return cjson.decode(utf8.d(f.read()))


def lookup_saldo_fl(s):
    url = "http://spraakbanken.gu.se/ws/saldo-ws/fl/json/"
    f = urllib.request.urlopen(url + urllib.parse.quote(s))
    return cjson.decode(utf8.d(f.read()))


def lookup_eid(lid):
    url = "http://spraakbanken.gu.se/ws/dalin-ws/eid/json/"
    f = urllib.request.urlopen(url + urllib.parse.quote(lid))
    return cjson.decode(utf8.d(f.read()))


def lookup_lid(lid):
    url = "http://spraakbanken.gu.se/ws/dalin-ws/lid/json/"
    f = urllib.request.urlopen(url + urllib.parse.quote(lid))
    return cjson.decode(utf8.d(f.read()))


def lookup_saldo_lid(lid):
    url = "http://spraakbanken.gu.se/ws/saldo-ws/lid/json/"
    f = urllib.request.urlopen(url + urllib.parse.quote(lid))
    return cjson.decode(utf8.d(f.read()))


def lookup_table(p, w):
    url = "http://spraakbanken.gu.se/ws/dalin-ws/gen/json/"
    f = urllib.request.urlopen(
        url + urllib.parse.quote(p) + "/" + urllib.parse.quote(w)
    )
    return cjson.decode(utf8.d(f.read()))


def generate_wordforms(lemma_id):
    r = lookup_eid(lemma_id)
    return [
        w["form"]
        for w in lookup_table(utf8.e(r["p"]), utf8.e(r["gf"]))
        if not (w["msd"] in ["c", "ci", "cm", "sms"])
    ]


def wordforms(sense_id):
    ls = lookup_eid(sense_id)["l"]
    ws = set([])
    for lemma in ls:
        ws.update(generate_wordforms(utf8.e(lemma)))
    return list(ws)


def lookup_md1(sense_id):
    url = "http://spraakbanken.gu.se/ws/saldo-ws/md1/json/"
    f = urllib.request.urlopen(url + urllib.parse.quote(sense_id))
    return cjson.decode(utf8.d(f.read()))


def md1(sense_id):
    res = lookup_md1(sense_id)
    eids = set([])
    for r in res:
        eids.update(lookup_lid(utf8.e(r)))
    #    wf = []
    #    for eid in eids:
    #        wf = wf + generate_wordforms(utf8.e(eid))
    return list(eids)


def md1_wordforms(sense_id):
    res = lookup_md1(sense_id)
    eids = set([])
    for r in res:
        eids.update(lookup_lid(utf8.e(r)))
    wf = set([])
    for eid in eids:
        wf.update(generate_wordforms(utf8.e(eid)))
    return list(wf)


def inits(s):
    xs = []
    for i in range(1, len(s) + 1):
        xs.append((s[:i], s[i:]))
    return xs


def prlex(lex):
    try:
        s = lex[:-3]
        if lex[-1] == "1":
            return s
        elif lex[-2] == ".":
            return s + "<sup>" + lex[-1] + "</sup>"
        else:
            return lex
    except:
        return lex


def lemma(l):
    rl = l[::-1]
    i = rl.find("..")
    pos = rl[:i][::-1]
    word = rl[(i + 2) :][::-1]
    return (word, pos)


def lemma_ref(lem):
    try:
        s = lem[:-2]
        (w, pos) = lemma(s)
        if lem[-1] == "1":
            return w
        elif lem[-2] == ".":
            return w + "<sup>" + lem[-1] + "</sup>"
        else:
            return lem
    except:
        return lem


def lemma_pref(lem):
    try:
        s = lem[:-2]
        (w, pos) = lemma(s)
        if lem[-1] == "1":
            return pos
        elif lem[-2] == ".":
            return pos
        else:
            return lex
    except:
        return lex


def lemma_href(lid):
    if lid == "":
        return "*"
    else:
        return (
            '<a href="http://spraakbanken.gu.se/ws/dalin-ws/eid/html/'
            + urllib.parse.quote(lid)
            + '">'
            + lemma_ref(lid)
            + "</a>"
        )


def md1_ref(l):
    if l == "":
        return "*"
    else:
        return (
            '<a href="http://spraakbanken.gu.se/ws/dalin-ws/md1/html/'
            + urllib.parse.quote(l)
            + '">md1</a>'
        )


def lb_ref(l):
    if l == "":
        return "*"
    else:
        return (
            ' <a href="http://spraakbanken.gu.se/ws/dalin-ws/lb/html/250/'
            + urllib.parse.quote(l)
            + '">relaterade ord</a>'
        )


def lemma_hrefx(lid):
    if lid == "":
        return "*"
    else:
        return (
            '<a href="http://spraakbanken.gu.se/ws/dalin-ws/eid/html/'
            + urllib.parse.quote(lid)
            + '">'
            + lid
            + "</a>"
        )


def lemma_phref(lid):
    if lid == "":
        return "*"
    else:
        return (
            '<a href="http://spraakbanken.gu.se/ws/dalin-ws/eid/html/'
            + urllib.parse.quote(lid)
            + '">'
            + lemma_pref(lid)
            + "</a>"
        )


def lexeme_ref(lid):
    if lid == "":
        return "*"
    else:
        return (
            '<a href="http://spraakbanken.gu.se/ws/dalin-ws/lid/html/'
            + urllib.parse.quote(lid)
            + '">'
            + prlex(lid)
            + "</a>"
        )


def lexeme_saldo_ref(lid):
    if lid == "":
        return "*"
    else:
        return (
            '<a href="http://spraakbanken.gu.se/ws/saldo-ws/lid/html/'
            + urllib.parse.quote(lid)
            + '">'
            + prlex(lid)
            + "</a>"
        )


def not_fragment(param):
    for p in param.split(" "):
        if p[0].isdigit():
            return False
    return True


def lid_ref(word, lid):
    if lid == "":
        return "*"
    else:
        return (
            (
                '<a href="http://litteraturbanken.se/query/dalin.xql?word=%s&limit=10">'
                % word
            )
            + lid
            + "</a>"
        )
        # return '<a href="http://spraakbanken.gu.se/ws/dalin-ws/lid/html/' + urllib.quote(lid) + '">' + lid + '</a>'


def gen_ref(p, w, l):
    return '<a href="http://spraakbanken.gu.se/ws/dalin-ws/gen/html/%s/%s">%s</a>' % (
        urllib.parse.quote(p),
        urllib.parse.quote(w),
        l,
    )


def sms_ref(w, l):
    return '<a href="http://spraakbanken.gu.se/ws/dalin-ws/sms/html/%s">%s</a>' % (
        urllib.parse.quote(w),
        l,
    )


def html_table(xss):
    result = ""
    if len(xss) > 0:
        result += '<table border="1">\n'
        for xs in xss:
            result += "<tr><td>"
            result += "</td><td>".join(xs)
            result += "</td></tr>\n"
    return result


def korpus_ref(lids, name):
    xs = [
        y for lid in lids for x in generate_wordforms(utf8.e(lid)) for y in x.split(" ")
    ]  # -- ' '.join( #).encode('UTF-8')
    ys = []
    for x in xs:
        if not (x in ys):
            ys.append(x)
    wfs = "|".join([urllib.parse.quote(y.encode("UTF-8")) for y in ys])
    if wfs == "":
        return ""
    else:
        return (
            '<a href="http://litteraturbanken.se/#sok?forfattare=alla&titel=alla&antal=20&sortering=verk&fras=%s&traffsida=1">%s</a>'
            % (wfs, name)
        )


def korpus_wf_ref(words, name):
    wfs = "|".join([urllib.parse.quote(w.encode("UTF-8")) for w in words])
    if wfs == "":
        return ""
    else:
        return (
            '<a href="http://litteraturbanken.se/#sok?forfattare=alla&titel=alla&antal=20&sortering=verk&fras=%s&traffsida=1">%s</a>'
            % (wfs, name)
        )


def html_document(title, content, input="", service="fl", bar=True):
    s = """
<html>
 <head>
  <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
  <link rel="stylesheet" type="text/css" href="http://demo.spraakdata.gu.se/markus/swefn.css" />
  <title>%s</title>
 </head>
 <body OnLoad="document.getElementById('input').focus();">
  <center>
   <p>
    <a href="http://spraakbanken.gu.se/swe/forskning/swefn/dalin"><img src="http://spraakbanken.gu.se/sites/spraakbanken.gu.se/files/dalin.png" align="top" alt="Dalin" /></a><br />
   </p>""" % (
        title
    )
    if bar:
        s += """
   <script>
   function input_handler(e){
    var word = document.getElementById('input').value;
     if(word.length > 0){
      location.href='http://spraakbanken.gu.se/ws/dalin-ws/%s/html/'+encodeURIComponent(word);
     }
   }
   </script>
   <p>
   <input type="search" id="input" class="inputclass" value="%s" size="30" placeholder="Skriv in en ordform" results="10" onchange="input_handler(event)">
   <input type="submit" value="skicka" onchange="input_handler(event)">
   </p>
  </center>""" % (
            service,
            input,
        )
    s += """
  <div id="output_table">
  %s
  </div>
 </body>
</html>""" % (
        content
    )
    return s


def html_pdocument(title, content, input="", bar=True):
    s = (
        """
<html>
 <head>
  <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
  <link rel="stylesheet" type="text/css" href="http://demo.spraakdata.gu.se/markus/swefn.css" />
  <title>%s</title>
 </head>
 <body OnLoad="document.getElementById('input').focus();">
  <center>
   <p>
    <a href="http://spraakbanken.gu.se/swe/forskning/swefn/dalin"><img src="http://spraakbanken.gu.se/sites/spraakbanken.gu.se/files/dalin.png" align="top" alt="Dalin" /></a>
   </p>"""
        % title
    )
    if bar:
        s += (
            """
   <script>
   function input_handler(e){
    var word = document.getElementById('input').value;
     if(word.length > 0){
      location.href='http://spraakbanken.gu.se/ws/dalin-ws/para/html/'+encodeURIComponent(word);
     }
   }
   </script>
   <p>
   <input type="search" id="input" class="inputclass" value="%s" size="30" placeholder="Skriv in en ordform" results="10" onchange="input_handler(event)">
   <input type="submit" value="skicka" onchange="input_handler(event)">
   </p></center>"""
            % input
        )
    s += (
        """
  <div id="output_table">
  %s
  </div>
 </body>
</html>"""
        % content
    )
    return s
