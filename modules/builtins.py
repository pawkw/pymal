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
    'def!': MalType.special('def!'),
    'let*': MalType.special('let*'),
    'prn-env': MalType.special('prn-env'),
    'do': MalType.special('do'),
    'if': MalType.special('if'),
    'fn*': MalType.special('fn*'),
}


def prn(args: MalType) -> MalType:
    result = prstr(args)
    print(result.data)
    return MalType.nil()


def make_str(args: MalType) -> MalType:
    result = []
    for item in args:
        result.append(pr_str(item, print_readably=False))
    return MalType.string("".join(result))


def prstr(args: MalType) -> MalType:
    result = []
    for item in args:
        result.append(pr_str(item))
    return MalType.string(" ".join(result))

def println(args: MalType) -> MalType:
    result = []
    for item in args:
        result.append(pr_str(item, print_readably=False))
    print(" ".join(result))
    return MalType.nil()


def equate(args: MalType) -> MalType:
    x = args[0]
    y = args[1]
    
    if not (x.isCollection() and y.isCollection()):
        return MalType.true() if x.data == y.data else MalType.false()

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
            return MalType.string(f.readlines())
    except:
        raise MalError(f"Could not open file '{file_name}'.")