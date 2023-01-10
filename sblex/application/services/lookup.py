import abc

from sblex.predicates import is_lemma, is_lexeme


class LookupService(abc.ABC):
    @abc.abstractmethod
    def lookup_lemma(self, lid):
        ...

    @abc.abstractmethod
    def lookup_lexeme(self, lid):
        ...


    def lookup_lid(self, lid):
        if is_lemma(lid):
            ret = self.lookup_lemma(lid)
        elif is_lexeme(lid):
            ret = self.lookup_lexeme(lid)
        else:
            ret = []
        return ret

    def md1(self, sense_id):
        xs = []
        sib = []
        res = self.lookup_lid(sense_id)
        if res == []:
            return []
        if res['fm'] != 'PRIM..1':
            sib = self.lookup_lid(res['fm'])['mf']
            xs = [res['fm']]
        md1 = xs + sib + res['mf']
    #    wf = []
    #    for s in md1:
    #        wf = wf + wordforms(utf8.e(s))
        return list(set(md1))

