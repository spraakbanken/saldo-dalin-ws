import logging

from sblex.application.queries import FullformLexQuery
from sblex.application.services import LookupService

logger = logging.getLogger(__name__)


class LookupFullformLexQuery(FullformLexQuery):
    def __init__(self, lookup_service: LookupService) -> None:
        self.lookup_service = lookup_service

    def query(self, segment: str) -> list[dict]:
        result = []
        lemmas = {
            (x["id"], x["gf"], x["p"])
            for x in self.lookup_service.lookup_ff(segment)
            if x["msd"] not in ["ci", "cm", "c"] and x["pos"][-1] != "h"
        }

        for lem, gf, p in lemmas:
            logger.info("calling lookup_lid for '%s'", lem)
            lexemes = self.lookup_service.lookup_lid(lem)["l"]
            for lex in lexemes:
                lexdata = self.lookup_service.lookup_lid(lex)
                try:
                    result.append(
                        {
                            "id": lex,
                            "fm": lexdata["fm"],
                            "fp": lexdata["fp"],
                            "l": lem,
                            "gf": gf,
                            "p": p,
                        }
                    )
                except:
                    raise Exception(lex)
        result.sort()
        return result
