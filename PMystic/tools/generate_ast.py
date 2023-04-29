import sys


class GenerateAst:
    def __init__(self, output_dir: str):
        self.__output_dir = output_dir
        self.define_ast(
            "Expr",
            [
                "Binary: Expr left, Token operator, Expr right",
                "Grouping: Expr expression",
                "Literal: object value",
                "Unary: Token operator, Expr right",
            ],
        )

    def define_ast(self, base_name: str, types: list):
        path = self.__output_dir + "/" + base_name.lower() + ".py"
        writer = open(path, "w")
        writer.write("class " + base_name + ":\n")
        self.define_vistior(writer, base_name, types)
        writer.write("    def __init__(self):\n")

        for type in types:
            class_name = type.split(":")[0].strip()
            writer.write(
                "        self." + class_name.lower() + " = self." + class_name + "\n"
            )
        writer.write("\n")

        for type in types:
            class_name = type.split(":")[0].strip()
            fields = type.split(":")[1].strip()
            self.define_type(writer, base_name, class_name, fields)

    def define_type(self, writer, base_name, class_name, field_list):
        writer.write("    class " + class_name + ":\n")
        fields = field_list.split(", ")
        writer.write("        def __init__(self, ")

        for field in fields:
            type = field.split(" ")[0].strip()
            name = field.split(" ")[1].strip()
            writer.write(name + ": " + type + ", ")

        writer.write("):\n")

        for field in fields:
            name = field.split(" ")[1].strip()
            writer.write("            self." + name + " = " + name + "\n")

        writer.write("\n")

        writer.write("        def accept(self, visitor):\n")
        writer.write(
            "            return visitor.visit_"
            + class_name.lower()
            + "_"
            + base_name.lower()
            + "(self)\n\n"
        )

    def define_vistior(self, writer, base_name, types):
        writer.write("    class Visitor:\n")
        for type in types:
            type_name = type.split(":")[0].strip()
            writer.write(
                "        def visit_"
                + type_name.lower()
                + "_"
                + base_name.lower()
                + "(self, "
                + base_name.lower()
                + ": "
                + type_name
                + "):\n"
            )
            writer.write("            pass\n")


output_dir = sys.argv[1]
GenerateAst(output_dir)
