import socket

from sblex.lookup import LookupService


class SocketLookupService(LookupService):
    def __init__(self,*, sem_port: int, host: str = "localhost", size: int = 2048):
        self.host = host
        self.sem_port = sem_port
        self._size = size

    def lookup_lemma(self,lemma):
        result=''
        try:
            s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host,self.sem_port))
            s.send("lem "+lemma)
            buff = ''
            while True:
                buff = s.recv(self._size)
                if len(buff) == 0:
                    break
                result += buff
            s.close()
            result_code=apache.OK
            if format == 'xml':
                result = xmlize(result)
            elif format == 'html':
                result = htmlize(lemma,result)
        except:
            result_code=apache.HTTP_SERVICE_UNAVAILABLE
        return (result,result_code)

    def lookup_lexeme(self,lexeme):
        result=''
        try:
            s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host,self.sem_port))
            s.send("lex "+lexeme)
            buff = ''
            while True:
                buff = s.recv(self._size)
                if len(buff) == 0:
                    break
                result += buff
            s.close()
            result_code=apache.OK
        except:
            result_code=apache.HTTP_SERVICE_UNAVAILABLE
            return ('', result_code)
        if format == 'xml':
            result = xmlize(result)
        elif format=='protojs':
            result = protojs(result)
        elif format=='graph':
            result = graph(lexeme,result)
        elif format == 'html':
            result = htmlize(lexeme,result)
        if lexeme == 'rnd' and format == 'json':
            j = cjson.decode(utf8.d(result))
            ws = saldo_util.wordforms(utf8.e(j['lex']))
            j['fs'] = ws
            s = '{\n "lex":"%s",\n "fm":"%s",\n "fp":"%s",\n "mf":%s,\n "pf":%s,\n "l":%s,\n "fs":%s\n}' % (j['lex'],j['fm'],j['fp'],pr_list(j['mf']),pr_list(j['pf']),pr_list(j['l']),pr_list(ws))
            result = utf8.e(s)
        return (result,result_code)
