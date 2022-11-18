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
    print(f"EVAL: {pr_str(ast)}")
    while True:
        if not ast.isCollection():
            return eval_ast(ast, env)

        if ast.isEmpty():
            return ast

        if ast.isType('hashmap') or ast.isType('vector'):
            return eval_ast(ast, env)

        # Apply
        function = EVAL(ast.data[0], env)
        params = ast.data[1:]

        ## Special forms
        if function.isType('special'):
            function = function.data

            if function == "def!":
                env.set(params[0].data, EVAL(params[1], env))
                return env.get(params[0])
            
            if function == "let*":
                args = params[0]
                keys = args.data[::2]
                vals = args.data[1::2]
                newEnv = Env(env)
                for key, val in zip(keys, vals):
                    newEnv.set(key.data, EVAL(val, newEnv))
                # Discard newEnv after let*
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

        params = eval_ast(MalType.list(params), env)
        
        ## User functions
        if function.isType('function'):
            ast = function.body
            env = Env(function.env, binds=function.params, exprs=params.data)
            continue

        ## Builtins
        if function.isType('builtin'):
            return function.data(params.data)
        
        raise MalError(f"Can not evaluate {ast}.")

def eval_ast(ast: MalType, env: Env) -> MalType:
    if ast.isType('symbol'):
        return env.get(ast)

    if ast.isCollection():
        result_type = ast.type
        result = MalType(result_type, [])
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
        lambda args: EVAL(args, repl_env)
    ))
    EVAL(read_str('(def! load-file (fn* (f) (eval (read-string (str "(do " (slurp f) "\nnil)")))))'), repl_env)

    try:
        readline.read_history_file("history.txt")
    except FileNotFoundError:
        print("Line history will be saved in history.txt.")

    readline.set_history_length(100)
    while True:
        try:
            in_str = input("user> ")
            print(rep(in_str, repl_env))
        except EOFError:
            print("\nExiting.")
            exit(0)
        except MalError as e:
            print(e)
        except Exception as error:
            print("".join(traceback.format_exception(*sys.exc_info())))

    
    