from mystic_callable import MysticCallable
from environment import Environment
from mystic_return import Return


class MysticFunction(MysticCallable):
    def __init__(self, declaration, closure):
        self.__declaration = declaration
        self.__closure = closure

    def arity(self):
        return len(self.__declaration.params)

    def call(self, interpreter, arguments):
        env = Environment(self.__closure)
        for i in range(self.arity()):
            env.define(self.__declaration.params[i].lexeme, arguments[i])

        try:
            interpreter._execute_block(self.__declaration.body, env)
        except Return as return_value:
            return return_value.value
        return None

    def __str__(self):
        return f"<fn {self.__declaration.name.lexeme}>"
