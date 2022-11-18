from modules.maltypes import MalType
from functools import reduce
from modules.printer import pr_str

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
    'list': MalType.builtin(
        lambda args: MalType.list(args)
    ),
    'list?': MalType.builtin(
        lambda args: args[0].isType('list')
    ),
    'vector?': MalType.builtin(
        lambda args: args[0].isType('vector')
    ),
    'hashmap?': MalType.builtin(
        lambda args: args[0].isType('hashmap')
    ),
    'empty?': MalType.builtin(
        lambda args: args[0].isEmpty()
    ),
    'count': MalType.builtin(
        lambda args: len(args[0])
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
    'def!': MalType.special('def!'),
    'let*': MalType.special('let*'),
    'prn-env': MalType.special('prn-env'),
    'do': MalType.special('do'),
    'if': MalType.special('if'),
    'fn*': MalType.special('fn*'),
}


def prn(args: MalType) -> MalType:
    print(pr_str(args[0]))
    return MalType.nil()


def equate(args: MalType) -> MalType:
    x = args[0]
    y = args[1]
    
    if x.type != y.type:
        return MalType.false()
    
    if not x.isCollection():
        return MalType.true() if args[0].data == args[1].data else MalType.false()

    if len(x) != len(y):
        return MalType.false()

    result = MalType.true()
    # for loop
    
    return result

