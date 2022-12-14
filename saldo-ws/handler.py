# -*- coding: utf-8 -*-

import locale
import datetime
import cjson
import fullform
import fullform_lex
import compound
import lemma
import lexeme
import table
import paradigms
import version
import plist
import pos
import md1
import sib
import lsib
import glsib
import dist
import lem
from mod_python import apache
from mod_python import util 

formats = set(['json','xml','html','protojs','graph'])

# spraakbanken.gu.se/ws/saldo/input={...}

def handler(req):
    # parse input
    cback = ''
    cgi_input = util.FieldStorage(req)
    if cgi_input.has_key("input"):
        input = cgi_input["input"]
    else:
        return apache.HTTP_NOT_FOUND
    try:
        xs = input.split('/')
        (function,format,args) = (xs[0], xs[1], xs[2:])
    except:
        return apache.HTTP_NOT_FOUND
    try:
        (format,cback) = format.split(' ')
        if format != 'json':
            cback = ''
    except:
        pass
    if cgi_input.has_key("callback"):
        cback=cgi_input['callback']
    # valid format? 
    if not (format in formats):
            return apache.HTTP_NOT_FOUND

    if(function=='ff' and len(args) <= 1):
        if len(args) == 0:
            (result,result_code) = fullform.function(format,'')
        else:
            (result,result_code) = fullform.function(format,args[0])

    elif(function=='fl' and len(args) <= 1):
        if len(args) == 0:
            (result,result_code) = fullform_lex.function(format,'')
        else:
            (result,result_code) = fullform_lex.function(format,args[0])

    elif(function=='lid' and len(args) == 1 and is_lemma(args[0])):
        (result,result_code) = lemma.function(format,args[0])

    elif(function=='flem' and len(args) == 1):
         (result,result_code) = lem.function(format,args[0])

    elif(function=='lid' and len(args) == 1 and is_lexeme(args[0])):
        (result,result_code) = lexeme.function(format,args[0])

    elif(function=='sib' and len(args) == 1 and is_lexeme(args[0])):
        (result,result_code) = sib.function(format,args[0])

    elif(function=='rel' and len(args) == 1 and is_lemma(args[0])):
        (result,result_code) = lsib.function(format,args[0])

    elif(function=='grel' and len(args) == 1 and is_lemma(args[0])):
        (result,result_code) = glsib.function(format,args[0])

    elif(function=='md1' and len(args) == 1 and is_lexeme(args[0])):
        (result,result_code) = md1.function(format,args[0])

    elif(function=='dist' and len(args) == 1):
        (result,result_code) = dist.function(format,args[0])

    elif(function=='p' and len(args) == 0):
        (result,result_code) = plist.function(format)

    elif(function=='pos' and len(args) == 0):
        (result,result_code) = pos.function(format)

    elif(function=='gen' and len(args) == 2):
        (result,result_code) = table.function(format,args[0],args[1])

    elif(function=='para' and len(args) <= 1):
        if len(args) == 0:
            (result,result_code) = paradigms.function(format,'')
        else:
            (result,result_code) = paradigms.function(format,args[0])

    elif(function=='sms' and len(args) <= 1):
        (result,result_code) = compound.function(format,args[0])

    elif(function=='version' and len(args) == 0 and format == 'json'):
        result = version.version
        result_code = apache.OK
    else:
        return apache.HTTP_NOT_FOUND

    # write results
    if result_code == apache.OK:
        write_header(format,req)
        if cback == '':
            req.write(result)
        else:
            req.write(cback +'(' + result + ');')
        return apache.OK
    else:
        return result_code

# HTTP header
def write_header(format,req):
    if format=='html':
        write_html_header(req)
    elif format=='graph':
        write_html_header(req)
    elif format=='xml':
        write_xml_header(req)
    else:
        write_text_header(req)

# HTTP text header
def write_text_header(req):
    req.content_type = "text/plain;charset=utf-8"
    req.headers_out['Access-Control-Allow-Origin'] =  '*'
    req.headers_out['Cache-Control'] = 'must-revalidate, max-age:86400, s-maxage:86400'
    req.headers_out['Expires'] = get_expire_time()
    req.send_http_header()

# HTTP html header
def write_html_header(req):
    req.headers_out['Access-Control-Allow-Origin'] =  '*'
    req.headers_out['Cache-Control'] = 'must-revalidate, max-age:86400, s-maxage:86400'
    req.headers_out['Expires'] = get_expire_time()
    req.content_type = "text/html;charset=utf-8"
    req.send_http_header()

def write_xml_header(req):
    req.headers_out['Access-Control-Allow-Origin'] =  '*'
    req.headers_out['Cache-Control'] = 'must-revalidate, max-age:86400, s-maxage:86400'
    req.headers_out['Expires'] = get_expire_time()
    req.content_type = "text/xml;charset=utf-8"
    req.send_http_header()

# cache expire date
def get_expire_time():
    locale.setlocale(locale.LC_TIME, 'en_US')
    return datetime.datetime.utcnow().strftime('%a, %d %b %Y 23:59:59 GMT')
 
def is_lemma(s):
    rs = s[::-1]
    i  = rs.find('.')
    if(i == -1):
        return False
    else:
        return rs[i+1] != '.'

def is_lexeme(s):
    if s == 'rnd':
        return True
    rs = s[::-1]
    i  = rs.find('.')
    if(i == -1):
        return False
    else:
        return rs[i+1] == '.'
