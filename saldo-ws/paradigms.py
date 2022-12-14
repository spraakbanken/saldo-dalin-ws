# -*- coding: utf-8 -*-

import utf8
import os
import codecs
from mod_python import apache
from mod_python import util 
import popen2
import cjson
import saldo_util

def function(format,s):
                result=''
        #try:
		if s == '' and format == 'html':
			return (saldo_util.html_pdocument('SALDO','<center><p>Mata in kommaseparerade ordformer, där första ordet är en grundform försedd med ordklass.</p><p>Exempel: <a href="http://spraakbanken.gu.se/ws/saldo-ws/para/html/man%3Ann%2C%20m%C3%A4n">man:nn, män</a></p></center>'),apache.OK)
		xs=[x.strip() for x in s.split(',') if len(x) > 0]
		if (xs[0].find(':') == -1 and format =='html'):
			return (saldo_util.html_pdocument('SALDO','<center><p>Grundformen måste förses med ordklass (grundform:ordklass).</p></center>'),apache.OK)
		n  = xs[0].find(':')
		w1 = xs[0][0:n].strip()
		w  = w1.decode('UTF-8')
		w2 = xs[0][n+1:].strip()
		xs[0] = '%s:%s'% (w1,w2)
		words = ",".join(xs)
		saldo = 'export LC_ALL="sv_SE.UTF-8";/home/markus/fm/sblex/bin/saldo -f'
                fin, fout = popen2.popen2(saldo)
                fout.write(words)
                fout.close()
		result = ''
                for line in fin.readlines():
                        result+=line
		if(result.strip()==''):
			result='[]'
		j=cjson.decode(utf8.d(result))
		if format=='html':
			result = htmlize(j,w,s)
		if format=='json':
			result = result
		elif format == 'xml':
			result=xmlize(j).encode('UTF-8')
		result_code = apache.OK
#        except:
                #result_code = apache.HTTP_NOT_FOUND
		return (result,result_code)

def xmlize(j):
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<paradigms>\n'
    xml += "".join(['<p>' + x + '</p>' for x in j])
    xml += '</paradigms>\n'
    return xml

def htmlize(j,w,s):
    if (j == []):
            content = '<center><p><b>Hittade inga paradigm.</b></p></center>'
            return saldo_util.html_pdocument('SALDO',content,s)
    content = '<center><table border="1">'
    for p in j:
            content+='<tr><td><i>%s</i></td></tr>' % (saldo_util.gen_ref(utf8.e(p),utf8.e(w), utf8.e(p)))
    content+='</table></center>'
    return saldo_util.html_pdocument('SALDO',content,s)
