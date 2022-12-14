# -*- coding: utf-8 -*-

import utf8
import urllib
import saldo_util
import socket
import cjson
from mod_python import apache
from mod_python import util 

host = "localhost"
sem_port = 8093
size = 2048 

def function(format,segment):
        segment=segment.strip()
        if segment == '' and format == 'html':
             return (saldo_util.html_document('Dalin','<center><p>Mata in en ordform.</p></center>'),apache.OK)
        result=''
#      try:
        lemmas = [(x['id'],x['gf'],x['p']) for x in saldo_util.lookup_ff(segment) if not(x['msd'] in ['ci','cm','c'] or x['pos'][-1] == 'h')]

	for sal in saldo_util.lookup_saldo_fl(segment):
		for eid in saldo_util.lookup_lid(utf8.e(sal['id'])):
			res = saldo_util.lookup_eid(utf8.e(eid))
			lemmas.append((eid,res['gf'],res['p']))
	if len(lemmas) > 1:
		segment = utf8.e(lemmas[0][1])

	lemmas = list(set(lemmas))
	lst=[]

	for (lem,gf,p) in lemmas:
		lemma  = utf8.e(lem)
		try:
			lexemes =  saldo_util.lookup_eid(lemma)['l']
			for lex in lexemes:
				lexeme = utf8.e(lex)
				lexdata =  saldo_util.lookup_saldo_lid(lexeme)
				lst.append('{"id":"%s","fm":"%s","fp":"%s","l":"%s","gf":"%s","p":"%s"}' %(lex,lexdata['fm'],lexdata['fp'],lem,gf,p))
		except:
			pass
	lst.sort()
	result=utf8.e('[' + ',\n '.join(lst) + ']')
        if format=='xml':
            result=xmlize(segment,result)
        elif format=='html':
            result=htmlize(segment,result)
        result_code=apache.OK
#      except:
#              result_code=apache.HTTP_SERVICE_UNAVAILABLE
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
    content = '<center>'
    if (j == []):
	    content += '<p>Ingen analys.</p>'
    else:
          content +='<table border="1">'
          for json in j:
                content += '<tr><td>' 
                content += saldo_util.gen_ref(utf8.e(json['p']),utf8.e(json['gf']),utf8.e(json['l'])) 
                content += '</td><td>' + saldo_util.korpus_ref([json['l']],'fullformssökning') + '</td><td><b>saldo:</b> ' 
                content += saldo_util.lexeme_saldo_ref(utf8.e(json['id']))
                content += ' [' + saldo_util.lexeme_saldo_ref(utf8.e(json['fm']))
                if json['fp'] == 'PRIM..1':
                      content += ']' 
                else:
                      content+= '+' + saldo_util.lexeme_saldo_ref(utf8.e(json['fp'])) + ']'
		content += '</td><td>' + saldo_util.md1_ref(utf8.e(json['id'])) + '</td><td>' + saldo_util.lb_ref(utf8.e(json['id'])) + '</td></tr>'
	  content += '</table>'
    try:
    	    s = saldo_util.dalin_exist(segment)
    	    if 'count="0"' not in s:
    		    content += '<br />'
    		    content += '<table border=1 style="width:75%;align:center;">'
    		    content += '<tr><td>' + utf8.e(s) + '</td></tr>'
    		    content += '</table>'
    except:
    	    pass
    content += '</center>'
    html = saldo_util.html_document(segment,content)
    return html
