from typing import Any


class Trie:
    def __init__(self):
        self.trie: dict[int, tuple[dict[str, int], list[bytes]]] = {0: ({}, [])}
        self.state = 0  # state counter
        self.count = 0  # number of insertions
        self.trie_precomputed: dict[int, tuple[dict[str, int], bytes]] = {}

    def insert(self, word: str, decoration: bytes):
        self.count += 1
        st = 0  # traversal state
        for i in range(len(word)):
            try:
                st = self.trie[st][0][word[i]]
            except:
                self.complete(st, word[i:], decoration)
                return
        self.trie[st][1].append(decoration)

    # create a new branch
    def complete(self, st: int, word: str, decoration: bytes):
        for c in word:
            self.state += 1
            self.trie[st][0][c] = self.state
            self.trie[self.state] = ({}, [])
            st = self.state
        self.trie[st][1].append(decoration)

    def lookup(self, word: str, start_state=0) -> bytes:
        st = start_state  # traversal state
        for c in word:
            try:
                st = self.trie[st][0][c]
            except:
                return b""
        return self.trie_precomputed[st][1]

    def continuation(self, state: int):
        return list(self.trie[state][0].keys())

    def number_of_insertions(self):
        return self.count

    def precompute(self):
        for i in range(self.state + 1):
            tr = self.trie[i][0]
            dec = self.trie[i][1]
            # ys  = [x.encode('UTF-8') for x in dec]
            ys = [x for x in dec]
            cont = ("".join(self.continuation(i))).encode("UTF-8")
            self.trie_precomputed[i] = (
                tr,
                b'{\n"a":[%s],\n"c":"%s"}' % (wrap(b",\n".join(ys)), cont),
            )

    def lookup_dict(self, word: str, start_state: int = 0) -> dict[str, Any]:
        # traversal state
        st = start_state
        for c in word:
            st = self.trie[st][0][c]
        return self.trie[st][1]


def wrap(s: bytes) -> bytes:
    if len(s) > 0:
        return b"\n" + s + b"\n"
    else:
        return s
