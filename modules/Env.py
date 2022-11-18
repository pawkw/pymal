from modules.maltypes import MalType
from typing import Any
from modules.malerror import MalError

class Env:
    def __init__(self, parent: "Env", binds = None, exprs = None) -> None:
        self.data = {}
        self.parent = parent
        
        if binds:
            for index in range(len(binds)):
                if binds[index].data == "&":
                    self.set(binds[index+1].data, MalType.list(exprs[index:]))
                    break
                self.set(binds[index].data, exprs[index])

    def set(self, key: MalType, value: Any) -> None:
        self.data[key] = value

    def find(self, key: MalType) -> "Env":
        if key in self.data:
            return self

        if self.parent is None:
            return None

        return self.parent.find(key)

    def get(self, key: MalType):
        # print(f'Env::get {key.type} {key.data}')
        result = self.find(key.data)
        if result is None:
            raise MalError(f"{key.data} not found.")
        return result.data[key.data]

    def root(self) -> "Env":
        if self.parent is None:
            return self
        return self.root()