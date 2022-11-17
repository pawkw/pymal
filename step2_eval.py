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
    if not ast.isCollection():
        return eval_ast(ast, env)

    if ast.isEmpty():
        return ast

    if ast.isType('hashmap') or ast.isType('vector'):
        return eval_ast(ast, env)
        
    # Apply
    new_ast = eval_ast(ast, env)
    function = new_ast.data[0]
    params = new_ast.data[1:]

    ## Special forms

    ## User functions

    ## Builtins
    return function.data(params)

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

    
    