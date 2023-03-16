from json_streams import jsonlib
from sblex.fm.morphology import Morphology


def test_morphology_exists() -> None:
    morphology = Morphology("assets/testing/dalin.lex")
    morphology.build()

    result = morphology.lookup("0 öka".encode("utf-8"))
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
