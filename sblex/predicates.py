 
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
