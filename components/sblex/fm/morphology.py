"""FM morphology."""

import json_streams
from json_streams import jsonlib

from sblex.trie import trie


class JsonIterator:
    def __init__(self,fname):
        self.f = open(fname,'r',encoding='utf-8')

    def __next__(self):
        s = self.f.readline()
        if(s==''):
            self.f.close()
            raise StopIteration
        j = cjson.decode(s)
        return (j)

    def __iter__(self):
        return self


def cit(xs):
    if(xs==[]) : return ''
    else       : return '"'


class Morphology:
    def __init__(self,fname):
        self.fname = fname
        self.lexicon = JsonIterator(fname)
        self.trie    = trie.Trie()

    def build(self):
        print("building morphology structure... (takes about 1 minute)")
        for j in json_streams.load_from_file(self.fname, json_format="jsonl"):
            w = j['word']
            # a = '{"gf":"%s","id":"%s","pos":"%s","is":[%s],"msd":"%s","p":"%s"}' % (j['head'],j['id'],j['pos'],"%s%s%s" % (cit(j['inhs']),'","'.join(j['inhs']),cit(j['inhs'])),j['param'],j['p'])
            a = {
                "gf":j["head"],
                "id":j["id"],
                "pos":j["pos"],
                "is":j["inhs"],
                "msd":j["param"],
                "p":j["p"]
            }
            # % ("%s%s%s" % (
            #         cit(j['inhs']),
            #         '","'.join(j['inhs']),
            #         cit(j['inhs'])),
            #     j['param'],
            #     j['p'])
            self.trie.insert(w,jsonlib.dumps(a))
        print("number of word forms read: ", end=' ')
        print(self.trie.number_of_insertions())
        print("initiating precomputation...")
        self.trie.precompute()
        print("done")

    def lookup(self,s: bytes) -> bytes:
        try:
            res = s.decode('UTF-8').split(' ',1)
            n   = int(res[0])
            s   = res[1]
            r = self.trie.lookup(s,n)
            if r == b'':
                return b'{"id":"0","a":[],"c":""}'
            else:
                return self.trie.lookup(s,n)
        except:
            return b'{"id":"0","a":[],"c":""}'
