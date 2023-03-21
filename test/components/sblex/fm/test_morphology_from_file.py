from json_streams import jsonlib

from sblex.fm.morphology import MemMorphology


def test_morphology_exists() -> None:
    morphology = MemMorphology.from_path("assets/testing/dalin.lex")

    result = morphology.lookup_from_bytes("0 öka".encode("utf-8"))
    morph = jsonlib.loads(result)
    expected = {
        "a": [
            {
                "gf": "öka",
                "id": "dalinm--öka..vb.2",
                "is": [],
                "msd": "-",
                "p": "vb",
                "pos": "vb",
            },
            {
                "gf": "öka",
                "id": "dalinm--öka..vb.1",
                "is": [],
                "msd": "-",
                "p": "vb",
                "pos": "vb",
            },
        ],
        "c": "",
    }
    assert morph == expected
