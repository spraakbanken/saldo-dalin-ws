from sblex import predicates


class Lexeme(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            examples=["rnd", "lexeme..1"]
        )

    @classmethod
    def validate(cls, value):
        if not isinstance(value,str):
            raise TypeError("string required")
        if not predicates.is_lexeme(value):
            raise ValueError("invalid lexeme format")
        return cls(value)

    def __repr__(self):
        return f"Lexeme({super().__repr__()}"
