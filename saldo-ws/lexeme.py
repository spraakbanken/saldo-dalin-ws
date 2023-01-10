# -*- coding: utf-8 -*-

import utf8
import socket
import saldo_util
import cjson
from mod_python import apache
from mod_python import util 


def pr_list(xs):
    xs = list(set(xs))
    xs.sort()
    if(xs == []):
        return '[]'
    else:
        return '["%s"]' % ('","'.join(xs))

def protojs(s):
    j = cjson.decode(utf8.d(s))
    return ('var flare = {' + ", ".join(["'"+x+"':'http://spraakbanken.gu.se/ws/saldo-ws/lid/graph/" + x + "'" for x in j['mf']]) +'}').encode('utf-8')

def xmlize(s):
    j = cjson.decode(utf8.d(s))
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<result>\n'
    if (not (j==[])):
        xml += ' <lex>' + j['lex'] + '</lex>\n'
        xml += ' <fm>' + j['fm'] + '</fm>\n'
        xml += ' <fp>' + j['fp'] + '</fp>\n'
        xml += ' <mfs>\n'
        for l in j['mf']:
            xml += '   <mf>' + l + '</mf>\n'
        xml += ' </mfs>\n'
        xml += ' <pfs>\n'
        for l in j['pf']:
            xml += '   <pf>' + l + '</pf>\n'
        xml += ' </pfs>\n'
        xml += ' <ls>\n'
        for l in j['l']:
            xml += '   <l>' + l + '</l>\n'
        xml += ' </ls>\n'
    xml += '</result>\n'
    return utf8.e(xml)

def htmlize(lexeme,s):
    j = cjson.decode(utf8.d(s))
    if(j == []):
        result='<center>%s finns ej.</center>' % lexeme
    else:
        fm       = saldo_util.lexeme_ref(utf8.e(j['fm']))        
        fp       = saldo_util.lexeme_ref(utf8.e(j['fp']))
        pf_len   = len(j['pf'])
        mf_len   = len(j['mf'])
        if pf_len == 0:
            pf_len = ''
        else:
            pf_len = '<br />' + str(pf_len)
        if mf_len == 0:
            mf_len = ''
        else:
            mf_len = '<br />' + str(mf_len)
        fmmf_len = 0
        mf       = sort_children(j['mf'],'p') 
        if(lexeme == 'PRIM..1'):
            pf = '*'
            lem = ''
        else:
            pf = sort_children(j['pf'],'m')
            lem = ", ".join([ saldo_util.lemma_href(utf8.e(l)) for l in j['l']])
        result='''
     <h1>%s</h1>
     <center><table border="1">
     <tr><td style="text-align:center;">⇧[%d]</td><td>%s</td>
    <td style="text-align:center;">↑</td><td>%s</td></tr>
    </table>
      <p>%s<br/>%s <br /> %s</p>
    <table border="1">
    <tr><td style="vertical-align:top;text-align:center;">⇩%s</td><td style="vertical-align:top;">%s</td>
    <td style="vertical-align:top;text-align:center;">↓%s</td><td style="vertical-align:top;">%s</td></tr>
   </table></center>
''' % (saldo_util.prlex(utf8.e(j['lex'])),depth(j['lex'],j['path']),fm,fp,lem, saldo_util.graph(j['lex']),saldo_util.korpus_ref(j['l'],'[korpus]'),mf_len, mf,pf_len,pf)
    return saldo_util.html_document(lexeme,result)

def depth(s,pths):
    if s == 'PRIM..1':
        return 0
    else:
        return len(pths)+1

def sort_children(lexemes,mp):
    if (lexemes == []):
        return '*'
    dict={}
    for l in lexemes:
        if mp == 'p':
            p = saldo_util.lookup_lid(utf8.e(l))['fp']
        else:
            p = saldo_util.lookup_lid(utf8.e(l))['fm']
        if dict.has_key(p):
            dict[p].append(l)
        else:
            dict[p] = [l]
    s='<table>'
    xs = []
    if(dict.has_key('PRIM..1')):
        prim_lexs = dict['PRIM..1']
        del dict['PRIM..1']
        xs = dict.items()
        xs.sort()
        xs.insert(0,('PRIM..1',prim_lexs))
    else:
        xs = dict.items()
        xs.sort()
    for (p,xs) in xs:
          s+= '<tr><td style="vertical-align:middle;">' + saldo_util.prlex(p) + ' </td><td style="vertical-align:middle;">' + (" ".join([utf8.d(saldo_util.lexeme_ref(utf8.e(x))) for x in xs])) + '</td></tr>'
    s+='</table>'
    return utf8.e(s)

def graph(l,s):
    j = cjson.decode(utf8.d(s))
    if(l != 'PRIM..1'):
        fm = "document.location.href = 'http://spraakbanken.gu.se/ws/saldo-ws/lid/graph/%s';" % j['fm']
    else:
        fm = ''
    content = '''
  <div style="width: 500px; height: 500px;">
  <script type="text/javascript" src="https://svn.spraakdata.gu.se/repos/sblex/pub/js/protovis-r3.2.js"></script>
  <script type="text/javascript" src="http://spraakbanken.gu.se/ws/saldo-ws/lid/protojs/%s"></script>
  <script type="text/javascript+protovis">

var vis = new pv.Panel()
   .width(500)
    .height(500);
    
var tree = vis.add(pv.Layout.Tree)
    .nodes(pv.dom(flare).root("%s").nodes())
    .depth(150)
    .breadth(100)
    .orient("radial");

tree.link.add(pv.Line);

tree.node.add(pv.Dot)
    .fillStyle(function(n) n.firstChild ? "#ffffff" : "#ffffff")
    .size(10)
    .event("mouseover", function() this.fillStyle("blue")) 
    .event("mouseout", function() this.fillStyle(undefined))
    .event("click", function(n) {
    if(n.nodeValue != undefined){
    document.location.href = n.nodeValue;
    }
    else{
    %s
    }
    });

tree.label.add(pv.Label)
   .text(function(n) n.nodeName.replace('..1','').replace('..','_'))
   .font("12px 'Arvo', sans-serif")
   .events("all")
   .cursor("hand")
   .event("click", function(n) {
    if(n.nodeValue != undefined){
      document.location.href = n.nodeValue;
      }
    else{
    %s
    } 
    });


vis.render();

    </script>
  </div>''' % (l,l,fm.encode('UTF-8'),fm.encode('UTF-8'))
    html = saldo_util.html_document(l,content,bar=False)
    return html
