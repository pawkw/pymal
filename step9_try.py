import sys, readline, atexit, traceback
from modules.reader import read_str
from modules.printer import pr_str
from modules.malerror import MalError
from modules.builtins import builtins
from modules.maltypes import MalType
from modules.Env import Env
from typing import List, Any


def READ(in_str: str) -> str:
    return read_str(in_str)


def EVAL(ast: MalType, env: Env) -> MalType:
    while True:
        ast = macroexpand(ast, env)
        # print(f"macroexpand returned {pr_str(ast)}")

        if not ast.isCollection():
            return eval_ast(ast, env)

        if ast.isType('hashmap') or ast.isType('vector'):
            return eval_ast(ast, env)

        if ast.isEmpty():
            return ast

        if ast.isType('comment'):
            continue
        
        # Apply
        function = EVAL(ast.data[0], env)
        params = ast.data[1:]

        ## Special forms
        if function.isType('special'):
            function = function.data

            if function == "try*":
                try:
                    return EVAL(params[0], env)
                except Exception as e:
                    params = params[1].data
                    # print(f"exception params is {pr_str(params[2])}")
                    if params[0].data != "catch*":
                        raise MalError("Malformed try statement")
                    error = MalType.string(e.__str__())
                    newEnv = Env(env, binds=[params[1]], exprs=[error])
                    # print_env(newEnv)
                    return EVAL(params[2], newEnv)

            # if function == "throw":
            #     raise MalError(params[0].data)

            if function == "def!":
                env.set(params[0].data, EVAL(params[1], env))
                return env.get(params[0])

            if function == "defmacro!":
                result = EVAL(params[1], env)
                result.type = 'macro'
                env.set(params[0].data, result)
                return env.get(params[0])

            if function == "macroexpand":
                return macroexpand(params[0], env)
            
            if function == "let*":
                args = params[0]
                keys = args.data[::2]
                vals = args.data[1::2]
                newEnv = Env(env)
                for key, val in zip(keys, vals):
                    newEnv.set(key.data, EVAL(val, newEnv))
               
                env = newEnv
                ast = params[1]
                continue

            if function == "prn-env":
                builtin = False
                special = False
                for flag in params:
                    if flag.data == 'builtin':
                        builtin = True
                    if flag.data == 'special':
                        special = True
                print_env(env, builtin=builtin, special=special)
                return MalType.nil()

            if function == "do":
                eval_ast(MalType.list(params[:-1]), env)
                ast = params[-1]
                continue

            if function == "if":
                predicate = EVAL(params[0], env)
                if not predicate.isType('nil') and not predicate.isType('false'):
                    ast = params[1]
                    continue
                if len(params) > 2:
                    ast = params[2]
                    continue
                return MalType.nil()

            if function == "fn*":
                def user_func(args: MalType):
                    new_env = Env(env, binds=params[0].data, exprs=args)
                    return EVAL(params[1], new_env)
                
                result = MalType.function(user_func)
                result.body = params[1]
                result.params = params[0].data
                result.env = env
                return result

            if function == "swap!":
                data = params[2:]
                func = params[1]
                atom = EVAL(params[0], env)
                result = EVAL(MalType.list([func, atom.data, *data]), env)
                env.find(params[0].data).set(params[0].data, MalType.atom(result))
                return result

            if function == "quote":
                return params[0]

            if function == "quasiquoteexpand":
                return quasiquote(params[0])

            if function == "quasiquote":
                ast = quasiquote(params[0])
                continue

        params = eval_ast(MalType.list(params), env)

        ## User functions
        if function.isType('function'):
            ast = function.body
            env = Env(function.env, binds=function.params, exprs=params.data)
            continue

        ## Builtins
        if function.isType('builtin'):
            return function.data(params.data)
        
        raise MalError(f"Can not evaluate {pr_str(ast)}.")

def eval_ast(ast: MalType, env: Env) -> MalType:
    if ast.isType('symbol'):
        return env.get(ast)

    if ast.isCollection():
        if ast.isType('hashmap'):
            return EVAL(MalType.list([
                MalType.symbol('hash-map'),
                *ast.data
            ]), env)

        if ast.isType('vector'):
            return EVAL(MalType.list([
                MalType.symbol('vector'),
                *ast.data
            ]), env)

        result = MalType.list([])
        for item in ast.data:
            result.data.append(EVAL(item, env))
        return result

    return ast


def print_env(env: Env, builtin = False, special = False) -> None:
    for (key, value) in env.data.items():
        if builtin and value.isType('builtin'):
            print(f"Built in function: {key}")
            continue
        if special and value.isType('special'):
            print(f"Special form: {key}")
            continue
        if value.type not in ['builtin', 'special']:
            print(f"{key} = {value.type}: {pr_str(value)}")


def quasiquote(params: MalType) -> MalType:
    if params.type in ['symbol', 'hashmap']:
        return MalType.list([MalType.symbol('quote'), params])
    
    if params.isType('vector'):
        return MalType.list([MalType.symbol('vec'), quasiquote(MalType.list(params.data))])

    if params.isType('list'):
        if params.isEmpty():
            return params
        
        if params.data[0].data == 'unquote':
            # print(f"unquote is {pr_str(params.data[1])}")
            return params.data[1]

        result = []
        params = [item for item in reversed(params.data)]
        while params:
            element = params[0]
            params = params[1:]
                
            if element.isType('list') and not element.isEmpty():
                if element.data[0].data == 'splice-unquote':
                    result = [MalType.symbol('concat'), element.data[1], MalType.list(result)]
                    continue

            result = [MalType.symbol('cons'), quasiquote(element), MalType.list(result)]
        return MalType.list(result)
    return params


def is_macro_call(ast: MalType, env: Env):
    if ast.isType('list') and not ast.isEmpty():
        first = ast.data[0]
        if first.isType('symbol') and env.find(first.data) is not None and env.get(first).isType('macro'):
            return True
    return False


def macroexpand(ast: MalType, env: Env):
    while is_macro_call(ast, env):
        function = env.get(ast.data[0]).data
        params = ast.data[1:]
        ast = function(params)
        # print(f"macroexpand ast is {pr_str(ast)}")
    return ast


def PRINT(ast: MalType) -> str:
    return pr_str(ast)


def rep(in_str: str, env: Env) -> str:
    return PRINT(EVAL(READ(in_str), env))


if __name__ == "__main__":
    atexit.register(readline.write_history_file, "history.txt")

    # Add root environment
    repl_env = Env(None)
    for func in builtins.items():
        repl_env.set(func[0], func[1])
    repl_env.set('eval', MalType.builtin(
        lambda args: EVAL(args[0], repl_env)
    ))
    EVAL(read_str('(def! load-file (fn* (f) (eval (read-string (str "(do " (slurp f) "\nnil)")))))'), repl_env)
    EVAL(read_str("(defmacro! cond (fn* (& xs) (if (> (count xs) 0) (list 'if (first xs) (if (> (count xs) 1) (nth xs 1) (throw \"odd number of forms to cond\")) (cons 'cond (rest (rest xs)))))))"), repl_env)
    
    try:
        readline.read_history_file("history.txt")
    except FileNotFoundError:
        print("Line history will be saved in history.txt.")

    readline.set_history_length(100)

    repl_env.set('*ARGV*', MalType.list([]))

    if len(sys.argv ) > 2:
        result = []
        for item in sys.argv[2:]:
            result.append(read_str(item))
        repl_env.set('*ARGV*', MalType.list(result))

    if len(sys.argv) > 1:
        EVAL(read_str('(load-file "'+sys.argv[1]+'")'), repl_env)

    while True:
        try:
            in_str = input("user> ")
            print(rep(in_str, repl_env))
        except EOFError:
            print("\nExiting.")
            exit(0)
        except MalError as e:
            print(f"Error: {e}")
        except Exception as error:
            print("".join(traceback.format_exception(*sys.exc_info())))

    
    