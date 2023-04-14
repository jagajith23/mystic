import sys
import scanner as sc


class Mystic:
    def __init__(self):
        self.__had_error = False

    def run_file(self, path: str) -> None:
        with open(path, "r") as f:
            lines = f.readlines()
        for line in lines:
            self.__run(line)
            if self.__had_error:
                sys.exit(65)

    def run_prompt(self) -> None:
        while True:
            try:
                line = input(">>> ")
                self.__run(line)
                self.__had_error = False
            except EOFError:
                break

    def __run(self, source: str):
        scanner = sc.Scanner(source, self)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

    @staticmethod
    def error(line: int, message: str):
        self.__report(line, "", message)

    def __report(self, line: int, where: str, message: str):
        print("[line " + str(line) + "] Error" + where + ": " + message)
        self.__had_error = True

    # def main():
    #     args = sys.argv

    #     mystic = Mystic()

    #     if len(args) > 2:
    #         print("Usage: python mystic.py [filename]")
    #         sys.exit(64)
    #     elif len(args) == 2:
    #         mystic.run_file(args[1])
    #     else:
    #         mystic.run_prompt()

    # if __name__ == "__main__":
    #     main()


args = sys.argv

mystic = Mystic()

if len(args) > 2:
    print("Usage: python mystic.py [filename]")
    sys.exit(64)
elif len(args) == 2:
    mystic.run_file(args[1])
else:
    mystic.run_prompt()
