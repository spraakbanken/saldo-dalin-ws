import sblex


class Lexeme(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
        
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(examples=["vanlig..1"])
        
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("string required")
            
        if not sblex.is_lexeme(v):
            raise ValueError("invalid lexeme format")
            
        return cls(v)
        
    def __repr__(self) -> str:
        return f"Lexeme({super().__repr__()})"
