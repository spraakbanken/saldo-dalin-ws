
import sys,random

class Semantics:
    def process(self, command: str, key: str):
        try:
            if(command == 'lem'):
                return lem_map[key]
            elif(command == 'lex'):
                if key == 'rnd':
                    return lex_map[list(lex_map.keys())[random.randint(0, len(lex_map)-1)]]
                else:
                    return lex_map[key]
            elif(command == 'rel'):
                    return relations(key)
            else:
                return '[]'
        except:
            return '[]'

host     = "localhost"
port     = 1
backlog  = 5
size     = 1024
lem_map  = {}
lex_map  = {}
path_map = {}

def json(x):
    return cjson.encode(x).encode('UTF-8')

def build(saldo):
    f = codecs.open(saldo,'r','utf-8')
    for line in f.readlines():
        xs = line.split('\t')
        if len(xs) != 7:
         continue
        (lexeme,mother,father,lemma,gf,pos,p) = line.split('\t')
        # create lemma-lexeme mappings
        if(lemma in lem_map):
            (s,p,gf)=lem_map[lemma]
            s.add(lexeme)
        else:
            lem_map[lemma] = (set([lexeme]),p.strip(),gf)
        # add mother, father and lemma
        if(lexeme in lex_map):
            # we may have added the children already
            (_,_,mf,pf,ls) = lex_map[lexeme]
            ls.add(lemma)
            lex_map[lexeme] = (mother,father,mf,pf,ls)
        else:
            lex_map[lexeme] = (mother,father,set([]),set([]),set([lemma]))

        # add m-children
        if(mother in lex_map):
            (m,f,mf,pf,_) = lex_map[mother]
            mf.add(lexeme)
        else:
            # we don't know the mother and the father yet.
            lex_map[mother] = ('','',set([lexeme]),set([]),set([]))

        # add p-children
        for father_ in father.split():
            if(father_ in lex_map):
                (m,f,mf,pf,_) = lex_map[father_]
                pf.add(lexeme)
            else:
                lex_map[father_] = ('','',set([]),set([lexeme]),set())

    # add path
    for sense in lex_map:
        pth = []
        sns = sense
        while sns not in ['PRIM..1',''] and sns not in pth:
            (primary,_,_,_,_) = lex_map[sns]
            sns = primary
            if sns != 'PRIM..1':
                pth.append(sns)
        path_map[sense] = pth

    for l in list(lem_map.keys()):
        (s,p,gf) = lem_map[l]
        lem_map[l] = ('{"l":%s,"p":"%s","gf":"%s"}' % (pr_set(s),p,gf)).encode('UTF-8')
    for l in list(lex_map.keys()):
        (m,f,mchildren,pchildren,lemmas) = lex_map[l]
        lex_map[l] = ('{\n "lex":"%s",\n "fm":"%s",\n "fp":"%s",\n "mf":%s,\n "pf":%s,\n "l":%s,\n "path":%s,\n "ppath":%s\n}' % (l,m,f,pr_set(mchildren),pr_set(pchildren),pr_set(lemmas),pr_list(path_map[l]),father_path(f))).encode('UTF-8')

def father_path(fathers):
    result = []
    for s in fathers.split(' '):
        if s != 'PRIM..1' and s != '':
            result.append(pr_list(path_map[s]))
    if len(result) > 0:
        return '[\n %s\n]' % (',\n '.join(result))
    else:
        return '[]'



def lemgram(sense):
    return cjson.decode(lex_map[sense].decode('UTF-8'))['l']

def mother(sense):
    return cjson.decode(lex_map[sense].decode('UTF-8'))['fm']

def fm_siblings(sense):
    fm = mother(sense)
    if fm == 'PRIM..1':
        return []
    senses = cjson.decode(lex_map[fm].decode('UTF-8'))['mf']
    return set([l for s in senses for l in lemgram(fm) + lemgram(s)])

def not_comp(lemgram):
    try:
        wc = lemgram.split('.')[2]
        return wc != 'sxc' and wc[-1] != 'h'
    except:
        return False

def relations(key):
    senses = cjson.decode(lem_map[key].decode('UTF-8'))['l']
    result = []
    for (s,ls) in [(s,fm_siblings(s)) for s in senses]:
        if len(ls) > 0:
            result.append(
                ('{"sense":"%s","rel":[' % s) +
                ",".join(['"' + l + '"' for l in ls if l != key and not_comp(l)]) +
                ']}')
    return ('[' + ", ".join(result) + ']').encode('UTF-8')

def pr_set(s):
    xs = list(s)
    xs.sort()
    if(xs == []):
        return '[]'
    else:
        return '["%s"]' % ('","'.join(xs))

def pr_list(xs):
    if(xs == []):
        return '[]'
    else:
        return '["%s"]' % ('","'.join(xs))


