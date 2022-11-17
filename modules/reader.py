import re
from modules.maltypes import MalType
from typing import List
from modules.malerror import MalError

class Reader:
    pattern = re.compile(r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)""");

    def __init__(self, in_str) -> None:
        self.tokens = self.tokenize(in_str)
        self.current=self.next()

    def tokenize(self, in_str: str) -> iter:
        for token in re.finditer(self.pattern, in_str):
            yield token[1].strip()

    def next(self) -> str:
        self.current = next(self.tokens, None)
        return self.current

    def peek(self) -> str:
        return self.current


def read_str(in_str: str) -> MalType:
    reader = Reader(in_str)
    return read_form(reader)


def read_form(reader: Reader) -> MalType:
    if reader.peek() is None:
        raise MalError("unbalanced")
    if reader.peek() == "(":
        return MalType.list(read_list(reader, ")"))
    if reader.peek() == "[":
        return MalType.vector(read_list(reader, "]"))
    if reader.peek() == "{":
        return MalType.hashmap(read_list(reader, "}"))
    
    # Do quote, unquote, etc. here.

    return read_atom(reader)


def read_list(reader: Reader, delim: str) -> List:
    result = []
    token = ""
    while True:
        token = reader.next()
        if token in [")", "]", "}"]:
            break
        result.append(read_form(reader))
    if token != delim:
        raise MalError(f"unbalanced")
    return result


def read_atom(reader: Reader):
    string = reader.peek()
    if string.isnumeric():
        return MalType.integer(int(string))
    
    if string[0] == '"':
        if len(string) > 1 and string[-1] == '"':
            return MalType.string(process_string(string[1:]))
        raise MalError("unbalanced")

    if string[0] == ':':
        return MalType.hashkey(string[1:])

    if string == 'true':
        return MalType.true()

    if string == 'nil':
        return MalType.nil()

    if string == 'false':
        return MalType.false()

    if string[0] == ';':
        return MalType.comment(string)

    return MalType.symbol(string)


def process_string(string: str) -> str:
    result = ""
    process = string
    while process:
        if process[0] == '\\':
            if process[1] == '\\':
                result += '\\'
                process = process[2:]
                continue
            if process[1] == 'n':
                result += '\n'
                process = process[2:]
                continue
            if process[1] == '"':
                result += '"'
                process = process[2:]
                continue
        if process[0] == '"':
            break
        result += process[0]
        process = process[1:]
    if process != '"':
        raise MalError("unbalanced")
    return result