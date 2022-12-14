# -*- coding: utf-8 -*-

import utf8
import urllib
import saldo_util
import socket
import cjson
from mod_python import apache
from mod_python import util 

host = "localhost"
sem_port = 8091
size = 2048 

def function(format,segment):
      try:
        segment=segment.strip()
        if segment == '' and format == 'html':
             return (saldo_util.html_document('SALDO','<center><p>Mata in en ordform.</p></center>'),apache.OK)
        result=''
        lemmas = set([(x['id'],x['gf'],x['p']) for x in saldo_util.lookup_ff(segment) if not(x['msd'] in ['ci','cm','c'] or x['pos'][-1] == 'h')])
        list=[]
        for (lem,gf,p) in lemmas:
            lemma  = utf8.e(lem)
            lexemes =  saldo_util.lookup_lid(lemma)['l']
            for lex in lexemes:
                lexeme = utf8.e(lex)
                lexdata =  saldo_util.lookup_lid(lexeme)
                try:
                      list.append('{"id":"%s","fm":"%s","fp":"%s","l":"%s","gf":"%s","p":"%s"}' %(lex,lexdata['fm'],lexdata['fp'],lem,gf,p))
                except:
                      raise Exception, utf8.e(lex)
        list.sort()
        result=utf8.e('[' + ',\n '.join(list) + ']')
        if format=='xml':
            result=xmlize(segment,result)
        elif format=='html':
            result=htmlize(segment,result)
        result_code=apache.OK
      except:
              result_code=apache.HTTP_SERVICE_UNAVAILABLE
      return (result,result_code)

def xmlize(segment,s):
    j = cjson.decode(utf8.d(s))
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<result>\n'
    for x in j:
            xml+='<a><id>%s</id><fm>%s</fm><fp>%s</fp><l>%s</l><gf>%s</gf><p>%s</p></a>'%(x['id'],x['fm'],x['fp'],x['l'],x['gf'],x['p'])
    xml += '</result>\n'
    return utf8.e(xml)

def htmlize(segment,s):
    j = cjson.decode(utf8.d(s))
    content = '<center><h1>' + segment + '</h1><p>'  + saldo_util.sms_ref(segment,'sammansättningsanalys') + '</p>'
    content += '<table border="1">'
    if (j == []):
            content += '<tr><td>ordet saknas i lexikonet.</td></tr>'
    else:
      for json in j:
            content += '<tr><td>' + saldo_util.lexeme_ref(utf8.e(json['id']))
            content += '</td><td>' 
            content += saldo_util.lexeme_ref(utf8.e(json['fm']))
            if (json['fp']) != 'PRIM..1':
           #content += '</td><td><b>far: </b>' 
                  content += ' + ' + saldo_util.lexeme_ref(utf8.e(json['fp']))
            content += '</td><td>' 
            content += saldo_util.gen_ref(utf8.e(json['p']),utf8.e(json['gf']),saldo_util.lemma_ref(utf8.e(json['l']))) 
            content += '</td>'
            content += '<td>' + saldo_util.korpus_ref([json['l']],'korpus') +'</td>'
    content += '</tr></table></center>'
    html = saldo_util.html_document(segment,content)
    return html
