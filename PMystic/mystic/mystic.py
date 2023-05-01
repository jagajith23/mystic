import sys
from scanner import Scanner
from mystic_parser import MysticParser
from ast_printer import AstPrinter
from token_type import *
from token import Token


class Mystic:
    def __init__(self):
        self.__had_error = False

    def __run_file(self, path: str) -> None:
        with open(path, "rb") as file:
            bytes = file.read()
            self.__run(bytes.decode())
            if self.__had_error:
                sys.exit(65)

    def __run_prompt(self) -> None:
        while True:
            try:
                line = input(">>> ")
                self.__run(line)
                self.__had_error = False
            except KeyboardInterrupt:
                print("Exiting...")
                break
            except EOFError:
                break

    def __run(self, source: str):
        scanner = Scanner(source, self)
        tokens = scanner.scan_tokens()

        parser = MysticParser(tokens, self)
        expression = parser.parse()

        if self.__had_error:
            return

        print(AstPrinter().print(expression))

    def __report(self, line: int, where: str, message: str):
        print("[line " + str(line) + "] Error" + where + ": " + message)
        self.__had_error = True

    def error(self, line: int, message: str):
        self.__report(line, "", message)

    def error_at(self, token: Token, message: str):
        if token.token_type == TokenType.EOF:
            self.__report(token.line, " at end", message)
        else:
            self.__report(token.line, " at '" + token.lexeme + "'", message)

    def main(self):
        args = sys.argv

        if len(args) > 2:
            print("Usage: python mystic.py [filename]")
            sys.exit(64)
        elif len(args) == 2:
            self.__run_file(args[1])
        else:
            self.__run_prompt()


mystic = Mystic()

if __name__ == "__main__":
    mystic.main()
