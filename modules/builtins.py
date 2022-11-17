from modules.maltypes import MalType as _mt
from functools import reduce

# '+': MalType.function(lambda args: reduce(lambda x, y: MalType.integer(x.data + y.data), args), builtin=True),

builtins = {
    '+': _mt.builtin(
        lambda args: reduce(lambda x, y: _mt.integer(x.data + y.data), args)
    ),
    '-': _mt.builtin(
        lambda args: reduce(lambda x, y: _mt.integer(x.data - y.data), args)
    ),
    '*': _mt.builtin(
        lambda args: reduce(lambda x, y: _mt.integer(x.data * y.data), args)
    ),
    '/': _mt.builtin(
        lambda args: reduce(lambda x, y: _mt.integer(x.data // y.data), args)
    ),
    '%': _mt.builtin(
        lambda args: reduce(lambda x, y: _mt.integer(x.data % y.data), args)
    ),
    'neg': _mt.builtin(
        lambda arg: _mt.integer(-arg[0].data)
    ),
}