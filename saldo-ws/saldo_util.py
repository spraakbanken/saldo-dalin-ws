# -*- coding: utf-8 -*-

import utf8
import urllib.request, urllib.parse, urllib.error
import cjson
from mod_python import apache
from mod_python import util 

import sys

def lookup_ff(s):
    from fullform import function
    (result, result_code) = function('json', s)
    return cjson.decode(utf8.d(result))['a']

def lookup_fl(s):
    from fullform_lex import function
    (result, result_code) = function('json', s)
    return cjson.decode(utf8.d(result))

def lookup_table(p,w):
    from table import function
    (result, result_code) = function('json', p, w)
    return cjson.decode(utf8.d(result))

def lemgrams(word):
    return set([j['l'] for j in lookup_fl(word)])

def generate_wordforms(lemma_id):
    r  = lookup_lid(lemma_id)
    return [w['form'] for w in lookup_table(utf8.e(r['p']),utf8.e(r['gf'])) if not (w['msd'] in ['c','ci','cm','sms'])]

def wordforms(sense_id):
    ls = lookup_lid(sense_id)['l']
    ws = []
    for lemma in ls:
        ws = ws + generate_wordforms(utf8.e(lemma))
    return list(set(ws))

def lsib(lemma_id):
    senses  = lookup_lid(lemma_id)['l']
    return [l for s in senses for _s in sib(utf8.e(s)) for l in lookup_lid(utf8.e(_s))['l'] if utf8.d(lemma_id) != l]

def glsib(lemma_id):
    senses  = lookup_lid(lemma_id)['l']
    return [(s,[l for _s in sib(utf8.e(s)) for l in lookup_lid(utf8.e(_s))['l'] if utf8.d(lemma_id) != l]) for s in senses]

def sib(sense_id):
    sib = []
    res = lookup_lid(sense_id)
    if res == []:
        return []
    if res['fm'] != 'PRIM..1':
        sib = lookup_lid(utf8.e(res['fm']))['mf']
    return [s for s in sib if s != utf8.d(sense_id)]

def path(sense_id):
    res = lookup_lid(sense_id)
    result = []
    if res == []: return [] # (-1,[])
    for p in res['ppath']:
        p.insert(0,sense_id)
        result.append((len(p),p))
    pth = res['path']
    pth.insert(0,sense_id)
    result.append((len(pth),pth))
    return result

def compare_paths(l1,p1,l2,p2):
    found = False
    if l1 > l2:
        dist = l1-l2
        paths = list(zip(p1[dist:],p2))
    else:
        dist = l2-l1
        paths = list(zip(p1,p2[dist:]))
    d = 0
    for (s1,s2) in paths:
        if s1 == s2:
            found = True
            if dist == 0:
                dist = d*2
            else:
                dist += d
            break
        d+=1
    if not found:
        dist = l1+l2+101
    return dist

def compute_distance(s1,s2,path_dict):
    p1 = path_dict[s1]
    p2 = path_dict[s2]
    if s1 == 'PRIM..1':
        return (p2[-1][0],s1,s2)
    if s2 == 'PRIM..1':
        return (p1[-1][0],s1,s2)
    dist = min([compare_paths(_l1,_p1,_l2,_p2) for (_l1,_p1) in p1 for (_l2,_p2) in p2])
    return (dist,s1,s2)

def diag(senses):
    hist  = set([])
    pairs = []
    for (s1,s2) in [(s1,s2) for s1 in senses for s2 in senses if s1 != s2]:
        if (s1,s2) not in hist:
            pairs.append((s1,s2))
            hist.add((s1,s2))
            hist.add((s2,s1))
    return pairs

def distances(senses):
    senses = set(senses)
    path_dict={}
    for s in set(senses):
        pth = path(s)
        if len(pth) > 0:
            path_dict[s] = pth
        else:
            senses.remove(s)
    pairs = diag(senses)
    return sorted([compute_distance(s1,s2, path_dict) for (s1,s2) in pairs])
    
def inits(s):
    xs = []
    for i in range(1,len(s)+1):
        xs.append((s[:i],s[i:]))
    return xs

def prlex(lex):
    return "+".join([_prlex(l) for l in lex.split()])

def _prlex(lex):
    try:
        s = lex[:-3]
        if lex[-1] == '1':
            return s
        elif lex[-2] == '.':
            return s+'<sup>'+lex[-1]+'</sup>'
        else:
            return lex 
    except:
        return lex

def lemma(l):
    rl   = l[::-1]
    i    = rl.find('..')
    pos  = rl[:i][::-1]
    word = rl[(i+2):][::-1]
    return (word,pos)


def lemma_ref(lem):
    try:
        s = lem[:-2]
        (w,pos) = lemma(s)
        if lem[-1] == '1':
            return w + ' (' + pos + ')'
        elif lem[-2] == '.':
            return w+'<sup>'+lem[-1]+'</sup> (' + pos + ')'
        else:
            return lex 
    except:
        return lex

def lemma_pref(lem):
    try:
        s = lem[:-2]
        (w,pos) = lemma(s)
        if lem[-1] == '1':
            return pos
        elif lem[-2] == '.':
            return pos
        else:
            return lex 
    except:
        return lex

def lemma_href(lid):
    if lid=='':
        return '*'
    else:
        return '<a href="http://spraakbanken.gu.se/ws/saldo-ws/lid/html/' + urllib.parse.quote(lid) + '">' + lemma_ref(lid) + '</a>'

def lemma_phref(lid):
    if lid=='':
        return '*'
    else:
        return '<a href="http://spraakbanken.gu.se/ws/saldo-ws/lid/html/' + urllib.parse.quote(lid) + '">' + lemma_pref(lid) + '</a>'

def lexeme_ref(lids):
    if lids=='':
        return '*'
    else:
        return "+".join(['<a href="http://spraakbanken.gu.se/ws/saldo-ws/lid/html/' + urllib.parse.quote(lid) + '">' + prlex(lid) + '</a>' for lid in lids.split()])

def not_fragment(param):
    for p in param.split(' '):
        if p[0].isdigit(): return False
    return True

def lid_ref(lid):
    if lid=='':
        return '*'
    else:
        return '<a href="http://spraakbanken.gu.se/ws/saldo-ws/lid/html/' + urllib.parse.quote(lid) + '">' + lid + '</a>'

def gen_ref(p,w,l):
    return '<a href="http://spraakbanken.gu.se/ws/saldo-ws/gen/html/%s/%s">%s</a>' %(urllib.parse.quote(p),urllib.parse.quote(w),l)

def graph(s):
    return '<a href="http://spraakbanken.gu.se/ws/saldo-ws/lid/graph/%s"><img src="https://svn.spraakdata.gu.se/repos/sblex/pub/images/prim_graph.png" /></a>' %(s.encode('UTF-8'))

def korpus_ref(lids,name):
    # xs  = set([y for lid in lids for x in generate_wordforms(utf8.e(lid)) for y in x.split(' ')])
    # wfs = '+'.join([urllib.quote(y.encode('UTF-8')) for y in xs])
    try:
        return '<a href="http://spraakbanken.gu.se/korp/#search=lemgram|%s">%s</a>' % (utf8.e(lids[0]),name)
    except:
        return ''

def sms_ref(w,l):
    return '<a href="http://spraakbanken.gu.se/ws/saldo-ws/sms/html/%s">%s</a>' %(urllib.parse.quote(w),l)

def html_table(xss):
    result=''
    if len(xss) > 0:
        result+='<table border="1">\n'
        for xs in xss:
            result+='<tr><td>'
            result+='</td><td>'.join(xs)
            result+='</td></tr>\n'
    return result

def html_document(title,content,input="",bar=True, service='fl'):
    s= """
<html>
 <head>
  <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
  <link rel="shortcut icon" href="https://svn.spraakdata.gu.se/sb-arkiv/pub/images/saldo_icon.png">
  <link rel="stylesheet" type="text/css" href="http://demo.spraakdata.gu.se/markus/saldo.css" />
  <title>%s</title>
 </head>
 <body OnLoad="document.getElementById('input').focus();">
  <center>
   <p>
    <a href="http://spraakbanken.gu.se/saldo"><img src="http://spraakbanken.gu.se/sites/spraakbanken.gu.se/files/img/saldo/saldo.gif" align="top" alt="SALDO" /></a>
   </p>""" % title
    if bar:
        s+="""
   <script>
   function input_handler(e){
    var word = document.getElementById('input').value;
     if(word.length > 0){
      location.href='http://spraakbanken.gu.se/ws/saldo-ws/%s/html/'+encodeURIComponent(word);
     }
   }
   </script>
   <p><a href="https://svn.spraakdata.gu.se/repos/sblex/pub/saldo_instruktion.pdf">dokumentation (pdf)</a></p>
   <p>
   <input type="search" id="input" class="inputclass" value="%s" size="30" placeholder="Skriv in en ordform" results="10" onchange="input_handler(event)">
   <input type="submit" value="skicka" onchange="input_handler(event)"> </p>
  </center>""" % (service,input)
    s +="""
  <div id="output_table">
  %s
  </div>
 </body>
</html>""" % content
    return s

def html_pdocument(title,content,input="",bar=True):
    s = """
<html>
 <head>
  <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
  <link rel="shortcut icon" href="https://svn.spraakdata.gu.se/sb-arkiv/pub/images/saldo_icon.png">
  <link rel="stylesheet" type="text/css" href="http://demo.spraakdata.gu.se/markus/saldo.css" />
  <title>%s</title>
 </head>
 <body OnLoad="document.getElementById('input').focus();">
  <center>
   <p>
    <a href="http://spraakbanken.gu.se/saldo"><img src="http://spraakbanken.gu.se/sites/spraakbanken.gu.se/files/img/saldo/saldo.gif" align="top" alt="SALDO" /></a>
   </p>""" % title
    if bar:
        s +="""
   <script>
   function input_handler(e){
    var word = document.getElementById('input').value;
     if(word.length > 0){
      location.href='http://spraakbanken.gu.se/ws/saldo-ws/para/html/'+encodeURIComponent(word);
     }
   }
   </script>
   <p><a href="https://svn.spraakdata.gu.se/repos/sblex/pub/saldo_instruktion.pdf">dokumentation (pdf)</a></p>
   <p>
   <input type="search" id="input" class="inputclass" value="%s" size="30" placeholder="Skriv in en ordform" results="10" onchange="input_handler(event)"> 
   <input type="submit" value="skicka" onchange="input_handler(event)"> <p/>
   </center>""" % input
    s +="""
  <div id="output_table">
  %s
  </div>
 </body>
</html>""" % content
    return s
