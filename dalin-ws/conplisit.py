# -*- coding: utf-8 -*-
#!/usr/bin/env python

import urllib.request, urllib.parse, urllib.error
import saldo_util
import urllib.request, urllib.error, urllib.parse
import re
import time
import sblex
from xml.dom.minidom import parseString

lb = 'http://litteraturbanken.se/query/lb-search.xql'

def request(words):
    return '''<search>
  <string-filter>
    <item type="string">%s</item>
  </string-filter>
  <domain-filter>
    <item type="all-titles"/>
  </domain-filter>
  <ne-filter>
    <item type="NUL"/>
  </ne-filter>
</search>''' % ('|'.join(words) + '|').encode('UTF-8')

def init_search(words):
    init_address = lb + '?username=sblex&action=search-init'
    req          = urllib.request.Request(url=init_address,data=request(words))
    req.add_header('Content-Type', 'text/xml')
    content    = urllib.request.urlopen(req).read().decode('UTF-8')
    # the search parameters
    query_id   = re.findall(r'queryid>(.+)</query',content)[0]
    search_ref = re.findall(r'searchref>(.+)</searchref',content)[0]
    titledatacount = re.findall(r'titledatacount>(.+)</titledatacount',content)[0]
    return (query_id,search_ref,titledatacount)

def start_search(query_id):
    go_address= lb + '?action=search-go&queryid=%s&username=sblex' % query_id
    req = urllib.request.Request(url=go_address)
    urllib.request.urlopen(req).read()

def retrieve_data(search_ref,start,end):
    get_result_address= lb + '?action=get-result-set&searchref=%s&username=sblex&resultitem=%d&resultlength=%s' % (search_ref,start,end-start+1)
    req = urllib.request.Request(url=get_result_address)
    return urllib.request.urlopen(req).read()

def waiting_for_data(query_id, count):
    progress_address= lb + '?action=get-progress&queryid=%s&username=sblex' % query_id
    prog_patt = re.compile(r'progress>(.+)</progress')
    t = 1
    while t < 3:
        req      = urllib.request.Request(url=progress_address)
        content  = urllib.request.urlopen(req).read()
        progress = int(prog_patt.findall(content)[0])
        if progress >= count:
            return progress
        time.sleep(0.5)
        t+=1
    return progress

def process_xml(dom):
    result = []
    for node in dom.getElementsByTagName('kwic'):
        item = node.getElementsByTagName('item')[0]
        authorid = item.getAttributeNode('authorid').value
        title = item.getAttributeNode('title').value 
        title_id = item.getAttributeNode('titleid-new').value 
        page_name = item.getAttributeNode('pagename').value
        nodeid = item.getAttributeNode('nodeid').value
        result.append({
                'left':node.getElementsByTagName('left')[0].childNodes[0].data,
                'kw':node.getElementsByTagName('kw')[0].childNodes[0].data,
                'right':node.getElementsByTagName('right')[0].childNodes[0].data,
                'name':title,
                'url': 'http://litteraturbanken.se/#forfattare/%s/titlar/%s/sida/%s/etext?traff=%s' % (authorid,
                                                                                                       title_id,
                                                                                                       page_name,
                                                                                                       nodeid)})
    return result

class LB:

    def __init__(self,words):
        (query_id,search_ref,titledatacount) = init_search(words)
        self.query_id   = query_id
        self.search_ref = search_ref
        self.count      = int(titledatacount)
        start_search(query_id)

    def number_of_hits(self):
        return self.count

    def waiting(self,count):
        return waiting_for_data(self.query_id,min(self.count,count))

    def retrieve(self,start=1,end=20):
        return process_xml(parseString(retrieve_data(self.search_ref,start,end)))

def table(sense, hits=50):
    words = list(set([w for (_,wfs) in sblex.sblex(sense) for w in wfs]))
    req = LB(words)
    result = ''
    result += '<table border="1">'
    number_of_hits = min(req.waiting(hits),hits)
    count = 1
    for hit in req.retrieve(end=number_of_hits):
        if len(hit['name']) > 25:
            name = hit['name'][:20] + '...'
        else:
            name = hit['name']
        result += '<tr><td>%d</td><td>%s</td><td><a href="%s">%s</a></td><td>%s</td><td>%s</td></tr>' % (count,
                                                                                                         hit['left'],
                                                                                                         hit['url'],
                                                                                                         hit['kw'],
                                                                                                         hit['right'],
                                                                                                         name)
        count += 1
    result += '</table>'
    return result
