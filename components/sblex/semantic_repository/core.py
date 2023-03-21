import abc
import logging
from typing import Any

from sblex.predicates import is_lemma, is_lexeme

logger = logging.getLogger(__name__)


class SemanticRepository(abc.ABC):
    @abc.abstractmethod
    def get_lemma(self, lid: str) -> dict[str, Any]:
        """Get lemma with given `lid`.

        Raises
        ------
        SemanticRepositoryError
            custom error
        """
        ...

    @abc.abstractmethod
    def get_lexeme(self, lid: str) -> dict[str, Any]:
        """Get lexeme with given `lid`.

        Raises
        ------
        SemanticRepositoryError
            custom error
        """
        ...

    def get_by_lid(self, lid: str) -> dict[str, Any]:
        if is_lemma(lid):
            logger.debug("calling SemanticRepository.get_lemma for '%s'", lid)
            return self.get_lemma(lid)
        elif is_lexeme(lid):
            logger.debug("calling SemanticRepository.get_lexeme for '%s'", lid)
            return self.get_lexeme(lid)
        else:
            return {}

    def md1(self, sense_id):
        xs = []
        sib = []
        res = self.get_by_lid(sense_id)
        if res == []:
            return []
        if res["fm"] != "PRIM..1":
            sib = self.get_by_lid(res["fm"])["mf"]
            xs = [res["fm"]]
        md1 = xs + sib + res["mf"]
        #    wf = []
        #    for s in md1:
        #        wf = wf + wordforms(utf8.e(s))
        return list(set(md1))


class SemanticRepositoryError(Exception):
    """Raised when the SemanticRepository fails."""


class LemmaNotFound(SemanticRepositoryError, KeyError):
    """Raised when a Lemma is not found."""


class LexemeNotFound(SemanticRepositoryError, KeyError):
    """Raised when a Lexeme is not found."""
