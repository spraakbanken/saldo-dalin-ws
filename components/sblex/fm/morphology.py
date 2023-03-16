"""FM morphology."""

import logging
from typing import Any

import json_streams
from json_streams import jsonlib
from sblex.trie import Trie

logger = logging.getLogger(__name__)

class Morphology:
    def __init__(self, trie: Trie) -> None:
        self._trie = trie

    @classmethod
    def from_path(cls, fname: str) -> "Morphology":
        logger.info("building morphology structure... (takes about 1 minute)")
        return cls(trie=Trie.from_iter(json_streams.load_from_file(fname, json_format="jsonl")))

    def lookup(self, s: bytes) -> bytes:
        try:
            res = s.decode("UTF-8").split(" ", 1)
            n = int(res[0])
            word = res[1]
            if r := self._trie.lookup(word, n):
                return r
        except:
            pass
        return b'{"id":"0","a":[],"c":""}'

    def lookup_dict(self, s: str, n: int = 0) -> dict[str, Any]:
        if result := self.trie.lookup_dict(s, n):
            return result
        else:
            return {"id": "0", "a": [], "c": ""}
