
def lookup_lid(lid):
    from handler import is_lemma, is_lexeme
    if (is_lemma(lid)):
        from lemma import function
    elif (is_lexeme(lid)):
        from lexeme import function
    else:
        function = None
        ret = []
    if function is not None:
        (result, result_code) = function('json', lid)
        ret = cjson.decode(utf8.d(result))
    return ret

def md1(sense_id):
    xs = []
    sib = []
    res = lookup_lid(sense_id)
    if res == []:
        return []
    if res['fm'] != 'PRIM..1':
        sib = lookup_lid(utf8.e(res['fm']))['mf']
        xs = [res['fm']]
    md1 = xs + sib + res['mf']
#    wf = []
#    for s in md1:
#        wf = wf + wordforms(utf8.e(s))
    return list(set(md1))

