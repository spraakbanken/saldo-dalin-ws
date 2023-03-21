import csv
import logging
import random
from pathlib import Path
from typing import Any

from sblex.semantic_repository import SemanticRepository, SemanticRepositoryError
from sblex.semantic_repository.core import LemmaNotFound

logger = logging.getLogger(__name__)


class MemSemanticRepository(SemanticRepository):
    def __init__(
        self,
        *,
        lex_map: dict[str, dict[str, Any]],
        lem_map: dict[str, dict[str, Any]],
        path_map: dict[str, list[str]],
    ):
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

            final_lem_map = {}
            for lem, values in lem_map.items():
                (s, p, gf) = values
                final_lem_map[lem] = {"l": sorted(s), "p": p, "gf": gf}
            final_lex_map = {}
            for lex, values in lex_map.items():
                (m, f, mchildren, pchildren, lemmas) = values
                final_lex_map[lex] = {
                    "lex": lex,
                    "fm": m,
                    "fp": f,
                    "mf": sorted(mchildren),
                    "pf": sorted(pchildren),
                    "l": lemmas,
                    "path": path_map[lex],
                    "ppath": father_path(f, path_map),
                }
                #  % (l,m,f,pr_set(mchildren),pr_set(pchildren),pr_set(lemmas),pr_list(path_map[l]),father_path(f))
        return cls(lex_map=final_lex_map, lem_map=final_lem_map, path_map=path_map)

    def get_lemma(self, lemma: str) -> dict[str, Any]:
        try:
            return self._lem_map[lemma]
        except KeyError as exc:
            raise LemmaNotFound(lemma) from exc

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
            return []


def father_path(fathers, path_map: dict[str, Any]) -> list:
    result = []
    for s in fathers.split(" "):
        if s != "PRIM..1" and s != "":
            result.append(path_map[s])
    return result


class UnknownCommand(Exception):
    """Raised when process is getting an unknown command."""
