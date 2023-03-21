from sblex.fm.morphology import Morphology
from sblex.trie.trie import Trie


def test_morphology_exists() -> None:
    _morpholoy = Morphology(Trie({}))
