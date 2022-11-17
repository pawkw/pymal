from modules.maltypes import MalType
from typing import List

def pr_str(ast: MalType, print_readably: bool = True) -> str:
    # print(f"reader::pr_str ast type = {ast.type}")
    if not ast.isCollection() and not ast.isType('string'):
        if ast.isType('hashkey'):
            return ":" + ast.data
        return str(ast.data)
    if ast.isType('string'):
        return process_string(ast.data, print_readably)
    if ast.isType('list'):
        return "(" + " ".join(get_list(ast.data)) + ")"
    if ast.isType('vector'):
        return "[" + " ".join(get_list(ast.data)) + "]"
    if ast.isType('hashmap'):
        return "{" + " ".join(get_list(ast.data)) + "}"


def get_list(items: List) -> List:
    result = []
    for item in items:
        result.append(pr_str(item))
    return result


def process_string(string: str, print_readably: bool) -> str:
    if not print_readably:
        return string

    result = ""
    for char in string:
        if char == '"':
            result += '\\"'
            continue
        if char == '\\':
            result += "\\\\"
            continue
        if char == '\n':
            result += '\\n'
            continue
        result += char
    return '"' + result + '"'
    