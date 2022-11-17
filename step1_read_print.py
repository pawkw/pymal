import os, readline, atexit

def READ(in_str: str) -> str:
    return in_str

def EVAL(in_str: str) -> str:
    return in_str

def PRINT(in_str: str) -> str:
    return in_str

def rep(in_str: str) -> str:
    PRINT(EVAL(READ(in_str)))
    return in_str

if __name__ == "__main__":
    atexit.register(readline.write_history_file, "history.txt")
    try:
        readline.read_history_file("history.txt")
        readline.set_history_length(100)
        while True:
            in_str = input("user> ")
            print(rep(in_str))
    
    except FileNotFoundError:
        print("Line history will be saved in history.txt.")
    except EOFError:
        print("\nExiting.")
        exit(0)


