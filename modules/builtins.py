from typing import List
from modules.maltypes import MalType
from functools import reduce
from modules.printer import pr_str
from modules.reader import read_str
from modules.malerror import MalError

# '+': MalType.function(lambda args: reduce(lambda x, y: MalType.integer(x.data + y.data), args), builtin=True),

builtins = {
    '+': MalType.builtin(
        lambda args: reduce(lambda x, y: MalType.integer(x.data + y.data), args)
    ),
    '-': MalType.builtin(
        lambda args: reduce(lambda x, y: MalType.integer(x.data - y.data), args)
    ),
    '*': MalType.builtin(
        lambda args: reduce(lambda x, y: MalType.integer(x.data * y.data), args)
    ),
    '/': MalType.builtin(
        lambda args: reduce(lambda x, y: MalType.integer(x.data // y.data), args)
    ),
    '%': MalType.builtin(
        lambda args: reduce(lambda x, y: MalType.integer(x.data % y.data), args)
    ),
    'neg': MalType.builtin(
        lambda arg: MalType.integer(-arg[0].data)
    ),
    'prn': MalType.builtin(
        lambda args: prn(args)
    ),
    'str': MalType.builtin(
        lambda args: make_str(args)
    ),
    'pr-str': MalType.builtin(
        lambda args: prstr(args)
    ),
    'println': MalType.builtin(
        lambda args: println(args)
    ),
    'list': MalType.builtin(
        lambda args: MalType.list(args)
    ),
    'list?': MalType.builtin(
        lambda args: MalType.true() if args[0].isType('list') else MalType.false()
    ),
    'vec': MalType.builtin(
        lambda args: MalType.vector(args[0].data)
    ),
    'vector?': MalType.builtin(
        lambda args: MalType.true() if args[0].isType('vector') else MalType.false()
    ),
    'hashmap?': MalType.builtin(
        lambda args: MalType.true() if args[0].isType('hashmap') else MalType.false()
    ),
    'empty?': MalType.builtin(
        lambda args: MalType.true() if args[0].isEmpty() else MalType.false()
    ),
    'count': MalType.builtin(
        lambda args: MalType.integer(len(args[0].data)) if args[0].type in ['list', 'vector', 'hashmap'] else MalType.integer(0)
    ),
    '=': MalType.builtin(
        lambda args: equate(args)
    ),
    '>': MalType.builtin(
        lambda args: MalType.true() if args[0].data > args[1].data else MalType.false()
    ),
    '<': MalType.builtin(
        lambda args: MalType.true() if args[0].data < args[1].data else MalType.false()
    ),
    '>=': MalType.builtin(
        lambda args: MalType.true() if args[0].data >= args[1].data else MalType.false()
    ),
    '<=': MalType.builtin(
        lambda args: MalType.true() if args[0].data <= args[1].data else MalType.false()
    ),
    'not': MalType.builtin(
        lambda args: MalType.true() if args[0].type in ['nil', 'false'] else MalType.false()
    ),
    'read-string': MalType.builtin(
        lambda args: read_str(args[0].data)
    ),
    'slurp': MalType.builtin(
        lambda args: slurp(args[0].data)
    ),
    'atom': MalType.builtin(
        lambda args: MalType.atom(args[0])
    ),
    'atom?': MalType.builtin(
        lambda args: MalType.true() if args[0].isType('atom') else MalType.false()
    ),
    'deref': MalType.builtin(
        lambda args: args[0].data
    ),
    'reset!': MalType.builtin(
        lambda args: reset(args[0], args[1])
    ),
    'cons': MalType.builtin(
        lambda args: MalType.list([args[0]]+args[1].data)
    ),
    'concat': MalType.builtin(
        lambda args: concat(args)
    ),
    'nth': MalType.builtin(
        lambda args: nth(args)
    ),
    'first': MalType.builtin(
        lambda args: MalType.nil() if args[0].isType('nil') or args[0].isEmpty() else args[0].data[0]
    ),
    'rest': MalType.builtin(
        lambda args: MalType.list([]) if args[0].isType('nil') or len(args[0].data) < 2 else MalType.list(args[0].data[1:])
    ),
    'nil?': MalType.builtin(
        lambda args: MalType.true() if args[0].isType('nil') else MalType.false()
    ),
    'true?': MalType.builtin(
        lambda args: MalType.true() if args[0].isType('true') else MalType.false()
    ),
    'false?': MalType.builtin(
        lambda args: MalType.true() if args[0].isType('false') else MalType.false()
    ),
    'symbol?': MalType.builtin(
        lambda args: MalType.true() if args[0].isType('symbol') else MalType.false()
    ),
    'keyword?': MalType.builtin(
        lambda args: MalType.true() if args[0].isType('hashkey') else MalType.false()
    ),
    'sequential?': MalType.builtin(
        lambda args: MalType.true() if args[0].type in ['list', 'vector'] else MalType.false()
    ),
    'map?': MalType.builtin(
        lambda args: MalType.true() if args[0].isType('hashmap') else MalType.false()
    ),
    'symbol': MalType.builtin(
        lambda args: MalType.symbol(str(args[0].data))
    ),
    'keyword': MalType.builtin(
        lambda args: MalType.hashkey(str(args[0].data))
    ),
    'vector': MalType.builtin(
        lambda args: MalType.vector([*args])
    ),
    'hash-map': MalType.builtin(
        lambda args: make_hashmap(args)
    ),
    'apply': MalType.builtin(
        lambda args: mal_apply(args)
    ),
    'map': MalType.builtin(
        lambda args: mal_map(args)
    ),
    'throw': MalType.builtin(
        lambda args: throw(args)
    ),
    'assoc': MalType.builtin(
        lambda args: assoc(args)
    ),
    'dissoc': MalType.builtin(
        lambda args: dissoc(args)
    ),
    'get': MalType.builtin(
        lambda args: get(args)
    ),
    'contains?': MalType.builtin(
        lambda args: MalType.true() if '\u029E' + args[1].data in args[0].data else MalType.false()
    ),
    'keys': MalType.builtin(
        lambda args: MalType.list([MalType.hashkey(x[1:]) for x in args[0].data.keys()])
    ),
    'vals': MalType.builtin(
        lambda args: MalType.list([x for x in args[0].data.values()])
    ),
    'def!': MalType.special('def!'),
    'let*': MalType.special('let*'),
    'prn-env': MalType.special('prn-env'),
    'do': MalType.special('do'),
    'if': MalType.special('if'),
    'fn*': MalType.special('fn*'),
    'swap!': MalType.special('swap!'),
    'quote': MalType.special('quote'),
    'quasiquote': MalType.special('quasiquote'),
    'unquote': MalType.special('unquote'),
    'splice-unquote': MalType.special('splice-unquote'),
    'quasiquoteexpand': MalType.special('quasiquoteexpand'),
    'defmacro!': MalType.special('defmacro!'),
    'macroexpand': MalType.special('macroexpand'),
    'try*': MalType.special('try*'),
    'catch*': MalType.special('catch*'),
}


def get(args: List) -> MalType:
    map_one = args[0]
    key = '\u029E' + args[1].data
    if key in map_one.data:
        return map_one.data[key]
    return MalType.nil()


def dissoc(args: List) -> MalType:
    map_one = args[0].data.copy()
    keys = args[1:]
    for raw_key in keys:
        key = '\u029E' + raw_key.data
        if key in map_one:
            del map_one[key]
    return MalType.hashmap(map_one)


def assoc(args: List) -> MalType:
    map_one = args[0].data.copy()
    map_two = make_hashmap(args[1:])
    map_one.update(map_two.data)
    return MalType.hashmap(map_one)


def throw(args: List) -> None:
    raise MalError(pr_str(args[0]))


def mal_map(args: List) -> MalType:
    result = []
    function = args[0]
    if not args[1].type in ['list', 'vector']:
        raise MalError(f"Can not map to type {args[1].type}.")

    for item in args[1].data:
        result.append(function.data([item]))
    return MalType.list(result)


def mal_apply(args: List) -> MalType:
    function = args[0]
    last = args[-1]
    extras = [] if len(args) < 3 else args[1:-1]
    if not last.type in ['list', 'vector']:
        raise MalError(f"Can not apply to type {last.type}.")

    params = extras + last.data
    return function.data(params)


def nth(args: List) -> MalType:
    if args[0].type not in ['vector', 'list']:
        raise MalError("nth only works with lists and vectors.")

    index = args[1].data
    if index > len(args[0].data):
        raise MalError(f"Index {index} out of range.")
    return args[0].data[index]


def prn(args: List) -> MalType:
    result = prstr(args)
    print(result.data)
    return MalType.nil()


def make_str(args: List) -> MalType:
    result = []
    for item in args:
        result.append(pr_str(item, print_readably=False))
    return MalType.string("".join(result))


def make_hashmap(args: List) -> MalType:
    keys = args[::2]
    vals = args[1::2]
    if len(keys) != len(vals):
        raise MalError("Unbalanced")

    result = {}
    for raw_key, val in zip(keys, vals):
        key = '\u029E' + raw_key.data
        result[key] = val
    return MalType.hashmap(result)


def prstr(args: List) -> MalType:
    result = []
    for item in args:
        result.append(pr_str(item))
    return MalType.string(" ".join(result))

def println(args: List) -> MalType:
    result = []
    for item in args:
        result.append(pr_str(item, print_readably=False))
    print(" ".join(result))
    return MalType.nil()


def equate(args: List) -> MalType:
    x = args[0]
    y = args[1]
    
    if not (x.isCollection() and y.isCollection()):
        return MalType.true() if x.data == y.data and x.type == y.type else MalType.false()

    if len(x.data) != len(y.data):
        return MalType.false()

    for index in range(len(x.data)):
        # print(f"builtins::equate x.data = {x.data[index].data} y.data = {y.data[index].data}")
        if x.data[index].isCollection() and y.data[index].isCollection():
            if equate([x.data[index], y.data[index]]).isType('false'):
                return MalType.false()
        elif x.data[index].data != y.data[index].data:
            return MalType.false()
    
    # print("builtins::equate returning true")
    return MalType.true()


def slurp(file_name: str) -> MalType:
    try:
        with open(file_name, 'r') as f:
            result = f.readlines()
            return MalType.string(" ".join(result))
    except FileNotFoundError:
        raise MalError(f"Could not open file '{file_name}'.")

def reset(atom: MalType, value: MalType) -> MalType:
    if not atom.isType('atom'):
        raise MalError('Can not reset a non-atom.')
    atom.data = value
    return atom.data

def concat(args: List) -> MalType:
    result = []
    for item in args:
        result.extend(item.data)
    return MalType.list(result)
    