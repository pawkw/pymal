from modules.maltypes import MalType
from typing import List

def pr_str(ast: MalType, print_readably: bool = True) -> str:
    # print(f"reader::pr_str ast type = {ast.type}")
    if not ast.isCollection() and not ast.isType('string'):
        if ast.isType('hashkey'):
            return ':' + ast.data
        if ast.isType('atom'):
            return "(atom "+pr_str(ast.data)+")"
        if ast.isType('builtin'):
            return "<Built in function>"
        if ast.isType('special'):
            return "<Built in special form>"
        if ast.isType('function'):
            return "<User defined in function>"
        if ast.isType('macro'):
            return "<Macro function>"
        return str(ast.data)
    if ast.isType('string'):
        return process_string(ast.data, print_readably)
    if ast.isType('list'):
        return "(" + get_list(ast.data, print_readably) + ")"
    if ast.isType('vector'):
        return "[" + get_list(ast.data, print_readably) + "]"
    if ast.isType('hashmap'):
        result = []
        keys = ast.data.keys()
        vals = ast.data.values()
        for key, val in zip(keys, vals):
            result.append('"'+key[1:]+'"')
            result.append(pr_str(val, print_readably))
        return "{" + " ".join(result) + "}"


def get_list(items: List, print_readably: bool) -> List:
    result = []
    for item in items:
        # I really dislike this ideosyncratic representation of keywords.
        if item.isType('hashkey'):
            result.append('"'+key[1:]+'"')
        else:
            result.append(pr_str(item, print_readably))
    return " ".join(result)


def process_string(string: str, print_readably: bool) -> str:
    # print(f"printer::process_string string = '{string}' print_readably = {print_readably}")
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
    