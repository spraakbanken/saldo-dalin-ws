from sblex.fm.morphology import Morphology


def test_morphology_exists() -> None:
    morphology = Morphology("assets/testing/dalin.lex")
    morphology.build()

    assert morphology.lookup("1 kol") is None
