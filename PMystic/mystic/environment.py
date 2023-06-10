from runtime_error import RTE


class Environment:
    def __init__(self, enclosing=None):
        self.__values = {}
        self.__enclosing = enclosing

    def get(self, name):
        if name.lexeme in self.__values:
            return self.__values[name.lexeme]

        if self.__enclosing is not None:
            return self.__enclosing.get(name)

        raise RTE(name, f"Undefined variable '{name.lexeme}'.")

    def __assign(self, name, value):
        if name.lexeme in self.__values:
            self.__values[name.lexeme] = value
            return

        if self.__enclosing is not None:
            self.__enclosing.assign(name, value)
            return

        raise RTE(name, f"Undefined variable '{name.lexeme}'.")

    def define(self, name, value):
        self.__values[name] = value
