import csv
import logging
import random
from pathlib import Path
from typing import Any

from sblex.semantic_repository import SemanticRepository, SemanticRepositoryError

logger = logging.getLogger(__name__)


class MemSemanticRepository(SemanticRepository):
    def __init__(self, *, lex_map, lem_map, path_map):
        self._lex_map = lex_map
        self._lem_map = lem_map
        self._path_map = path_map

    @classmethod
    def from_tsv_path(cls, tsv_path: Path) -> "MemSemanticRepository":
        lem_map: dict[str, tuple[set[str], str, str]] = {}
        lex_map: dict[str, tuple[str, str, set[str], set[str], set[str]]] = {}
        path_map: dict[str, list[str]] = {}
        with open(tsv_path, "r", encoding="utf-8") as f:
            tsv_file = csv.reader(f, delimiter="\t")
            for line in tsv_file:
                if len(line) != 7:
                    logger.warn(
                        "Expected 7 columns, line has %d: '%s' skipping ...",
                        len(line),
                        line,
                    )
                    continue
                (lexeme, mother, father, lemma, gf, pos, p) = line
                # create lemma-lexeme mappings
                if lemma in lem_map:
                    (s, p, gf) = lem_map[lemma]
                    s.add(lexeme)
                else:
                    lem_map[lemma] = ({lexeme}, p.strip(), gf)
                # add mother, father and lemma
                if lexeme in lex_map:
                    # we may have added the children already
                    (_, _, mf, pf, ls) = lex_map[lexeme]
                    ls.add(lemma)
                    lex_map[lexeme] = (mother, father, mf, pf, ls)
                else:
                    lex_map[lexeme] = mother, father, set(), set(), {lemma}

                # add m-children
                if mother in lex_map:
                    (m, f, mf, pf, _) = lex_map[mother]
                    mf.add(lexeme)
                else:
                    # we don't know the mother and the father yet.
                    lex_map[mother] = ("", "", {lexeme}, set(), set())

                # add p-children
                for father_ in father.split():
                    if father_ in lex_map:
                        (m, f, mf, pf, _) = lex_map[father_]
                        pf.add(lexeme)
                    else:
                        lex_map[father_] = ("", "", set(), {lexeme}, set())

            # add path
            for sense in lex_map:
                pth = []
                sns = sense
                while sns not in ["PRIM..1", ""] and sns not in pth:
                    (primary, _, _, _, _) = lex_map[sns]
                    sns = primary
                    if sns != "PRIM..1":
                        pth.append(sns)
                path_map[sense] = pth

            # for l in list(lem_map.keys()):
            #     (s,p,gf) = lem_map[l]
            #     lem_map[l] = ('{"l":%s,"p":"%s","gf":"%s"}' % (pr_set(s),p,gf)).encode('UTF-8')
            # for l in list(lex_map.keys()):
            #     (m,f,mchildren,pchildren,lemmas) = lex_map[l]
            #     lex_map[l] = ('{\n "lex":"%s",\n "fm":"%s",\n "fp":"%s",\n "mf":%s,\n "pf":%s,\n "l":%s,\n "path":%s,\n "ppath":%s\n}' % (l,m,f,pr_set(mchildren),pr_set(pchildren),pr_set(lemmas),pr_list(path_map[l]),father_path(f))).encode('UTF-8')
        return cls(lex_map=lex_map, lem_map=lem_map, path_map=path_map)

    def get_lemma(self, lemma: str) -> dict[str, Any]:
        return self.process("lem", lemma)

    def get_lexeme(self, lexeme: str) -> dict[str, Any]:
        return self.process("lex", lexeme)

    def process(self, command: str, key: str) -> dict[str, Any]:
        try:
            if command == "lem":
                return self._lem_map[key]
            elif command == "lex":
                return (
                    self._lex_map[
                        list(self._lex_map.keys())[
                            random.randint(0, len(self._lex_map) - 1)
                        ]
                    ]
                    if key == "rnd"
                    else self._lex_map[key]
                )

            elif command == "rel":
                return relations(key)
            raise UnknownCommand(command)
        except:
            return "[]"


class UnknownCommand(Exception):
    """Raised when process is getting an unknown command."""
