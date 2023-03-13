
class Trie:
    def __init__(self):
        self.trie     = {0:({},[])} 
        self.state    = 0 # state counter
        self.count    = 0 # number of insertions

    def insert(self,word,decoration):
        self.count += 1
        st = 0 # traversal state
        for i in range(len(word)):
            try:
                st = self.trie[st][0][word[i]]
            except:
                self.complete(st,word[i:],decoration)
                return
        self.trie[st][1].append(decoration)

    # create a new branch
    def complete(self,st,word,decoration):
        for c in word:
            self.state += 1
            self.trie[st][0][c]   = self.state
            self.trie[self.state] = ({},[])
            st                    = self.state            
        self.trie[st][1].append(decoration)

    def lookup(self,word,start_state=0):
        st = start_state # traversal state 
        for c in word:
            try:
                st =self.trie[st][0][c]
            except:
                return ''
        return self.trie[st][1]

    def continuation(self,state):
        return list(self.trie[state][0].keys())

    def number_of_insertions(self):
        return self.count

    def precompute(self):
        for i in range(0,self.state+1):
            tr  = self.trie[i][0]
            dec = self.trie[i][1]
            ys  = [x.encode('UTF-8') for x in dec]
            cont = ("".join(self.continuation(i))).encode('UTF-8')            
            self.trie[i] = (tr,'{\n"a":[%s],\n"c":"%s"}' % (wrap(",\n".join(ys)), cont))

def wrap(s):
    if(len(s) > 0) : return '\n'+s+'\n'
    else           : return s
