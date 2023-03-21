import abc


class FullformLexQuery(abc.ABC):
    @abc.abstractmethod
    def query(self, segment: str) -> list[dict]:
        ...
