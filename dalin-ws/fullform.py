# -*- coding: utf-8 -*-

import utf8
import saldo_util
import socket
import cjson
from mod_python import apache
from mod_python import util 

host = "localhost"
port = 8092
size = 2048

def function(format,segment):
        result=''
     #try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))
        s.send("0 " + segment)
        buff = ''
        while True:
            buff = s.recv(size)
            if(len(buff) == 0): break
            result += buff
        s.close()
        result_code=apache.OK
        if format == 'xml':
            result = xmlize(result)
        elif format == 'html':
            result = htmlize(segment,result)
     #except:
     #    result_code=apache.HTTP_SERVICE_UNAVAILABLE
        return (result,result_code)

def xmlize(s):
    j = cjson.decode(utf8.d(s))
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<result>\n'
    xml += ' <c>' + j['c'] + '</c>\n'
    xml += ' <as>\n'
    for a in j['a']:
        xml += '  <a>\n'
        xml += '   <gf>' + a['gf'] + '</gf>\n'
        xml += '   <id>' + a['id'] + '</id>\n'
        xml += '   <pos>' + a['pos'] + '</pos>\n'
        xml += '   <is>' + (' '.join(a['is'])) + '</is>\n'
        xml += '   <msd>' + a['msd'] + '</msd>\n'
        xml += '   <p>' + a['p'] + '</p>\n'
        xml += '  </a>\n'
    xml += ' </as>\n'
    xml += '</result>\n'
    return utf8.e(xml)

def htmlize(segment,s):
    j = cjson.decode(utf8.d(s))
    # content =  ' <center><p>segment: ' + segment + '</p>\n'
    # content += ' <p>continuations: ' + utf8.e(j['c']) + '</p>\n'
    if segment=='':
         return  saldo_util.html_document(segment,("<center><p>Mata in en ordform.</p></center>"))
    content = ''
    j['a'] = [ a for a in j['a'] if not (a['msd'] in ['c','cm','ci','sms'])]
    if len(j['a']) > 0:
         content += ' <center><table border="1">\n'
         content += '  <tr><th>gf</th><th>id</th><th>pos</th><th>is</th><th>msd</th><th>p</th><th>lexikon</th></tr>\n'
         for a in j['a']:
              content += '  <tr>\n'
              content += '   <td>' + saldo_util.gen_ref(utf8.e(a['p']),utf8.e(a['gf']),utf8.e(a['gf'])) + '</td>\n'
              content += '   <td>' + saldo_util.lemma_hrefx(utf8.e(a['id'])) + '</td>\n'
              content += '   <td>' + utf8.e(a['pos']) + '</td>\n'
              content += '   <td>' + utf8.e((' '.join(a['is']))) + '</td>\n'
              content += '   <td>' + utf8.e(a['msd']) + '</td>\n'
              content += '   <td>' + utf8.e(a['p']) + '</td>\n'
              content += '   <td>' + saldo_util.lid_ref(utf8.e(a['gf']),'Dalin') + '</td>\n'
              content += '  </tr>\n'
         content += ' </table></center>\n'
    else:
         content=("<center><p>'%s' saknas.</p></center>"%(segment))
    html = saldo_util.html_document(segment,content,segment)
    return html
