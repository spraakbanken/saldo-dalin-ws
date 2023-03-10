import pytest

from sblex.schemas import Lexeme


class TestLexemeSchema:
    def test_non_string_raises_type_error(self):
        with pytest.raises(TypeError):
            Lexeme.validate(3)

    def test_bad_input_raises_value_error(self):
        with pytest.raises(ValueError):
            Lexeme.validate("bad")

    def test_valid_input_succeds(self):
        assert Lexeme.validate("lexeme..1") == "lexeme..1"
