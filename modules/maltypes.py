from typing import List, Callable


class MalType:
    def __init__(self, type: str, data) -> None:
        self.type = type
        self.data = data

    def isEmpty(self) -> bool:
        if self.isCollection() or self.type == "string":
            return len(self.data) < 1
        raise ValueError(f"{self.type} can not be empty.")

    def isType(self, query: str) -> str:
        return self.type == query

    def isCollection(self) -> bool:
        return self.type in ["hashmap", "vector", "list"]

    def isMacro(self) -> bool:
        return self.type == 'macro'

    @classmethod
    def list(cls, contents: List) -> "MalType":
        return cls("list", contents)

    @classmethod
    def vector(cls, contents: List) -> "MalType":
        return cls("vector", contents)

    @classmethod
    def hashmap(cls, contents: List) -> "MalType":
        return cls("hashmap", contents)

    # Atoms
    @classmethod
    def integer(cls, contents: int) -> "MalType":
        return cls("integer", contents)

    @classmethod
    def symbol(cls, contents: str) -> "MalType":
        return cls("symbol", contents)

    @classmethod
    def string(cls, contents: str) -> "MalType":
        return cls("string", contents)

    @classmethod
    def nil(cls) -> "MalType":
        return cls("nil", 'nil')

    @classmethod
    def true(cls) -> "MalType":
        return cls("true", 'true')

    @classmethod
    def false(cls) -> "MalType":
        return cls("false", 'false')

    @classmethod
    def hashkey(cls, contents: str) -> "MalType":
        return cls("hashkey", contents)

    @classmethod
    def comment(cls, contents: str) -> "MalType":
        return cls("comment", contents)

    @classmethod
    def function(cls, contents: "MalType") -> "MalType":
        return cls("function", contents)

    @classmethod
    def builtin(cls, contents: Callable) -> "MalType":
        return cls("builtin", contents)

    @classmethod
    def special(cls, contents: str) -> "MalType":
        return cls("special", contents)

    @classmethod
    def macro(cls, contents: Callable) -> "MalType":
        return cls("macro", contents)

    @classmethod
    def atom(cls, contents: str) -> "MalType":
        return cls("atom", contents)