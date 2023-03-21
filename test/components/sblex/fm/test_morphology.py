from sblex.fm.morphology import MemMorphology
from sblex.trie.trie import Trie


def test_morphology_exists() -> None:
    _morpholoy = MemMorphology(Trie({}))
