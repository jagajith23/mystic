from runtime_error import RTE


class Environment:
    def __init__(self, enclosing=None):
        self.__values = {}
        self.__enclosing = enclosing

    def define(self, name, value):
        self.__values[name] = value

    def get(self, name):
        if name.lexeme in self.__values:
            return self.__values[name.lexeme]

        if self.__enclosing is not None:
            return self.__enclosing.get(name)

        raise RTE(name, f"Undefined variable '{name.lexeme}'.")

    def get_at(self, dist, name):
        return self.__ancestor(dist).__values[name.lexeme]

    def assign(self, name, value):
        if name.lexeme in self.__values:
            self.__values[name.lexeme] = value
            return

        if self.__enclosing is not None:
            self.__enclosing.assign(name, value)
            return

        raise RTE(name, f"Undefined variable '{name.lexeme}'.")

    def assign_at(self, dist, name, value):
        self.__ancestor(dist).__values[name.lexeme] = value

    def __ancestor(self, dist):
        env = self
        for i in range(dist):
            env = env.__enclosing
        return env
