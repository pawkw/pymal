import sys, readline, atexit, traceback
from modules.reader import read_str
from modules.printer import pr_str
from modules.malerror import MalError

def READ(in_str: str) -> str:
    return read_str(in_str)

def EVAL(in_str: str) -> str:
    return in_str

def PRINT(in_str: str) -> str:
    return pr_str(in_str)

def rep(in_str: str) -> str:
    return PRINT(EVAL(READ(in_str)))

if __name__ == "__main__":
    atexit.register(readline.write_history_file, "history.txt")
    try:
        readline.read_history_file("history.txt")
    except FileNotFoundError:
        print("Line history will be saved in history.txt.")

    readline.set_history_length(100)
    while True:
        try:
            in_str = input("user> ")
            print(rep(in_str))
        except EOFError:
            print("\nExiting.")
            exit(0)
        except MalError as e:
            print(e)
        except Exception as error:
            print("".join(traceback.format_exception(*sys.exc_info())))

    
    