from io import TextIOWrapper
import sys
from typing import List

def define_type(f: TextIOWrapper, base_name: str, class_name: str, field_list: str):
    f.write(f"\nclass {class_name}({base_name}):\n")

    #__init__
    f.write(f"\tdef __init__(self, ")
    cnt = 0
    for word in field_list.split(' '):
        f.write(word)
        if cnt % 2 == 0: f.write(': ')
        else: f.write(' ')
        cnt += 1
    f.write("):\n")
    for pair in field_list.split(', '):
        f.write(f"\t\tself.{pair.split(' ')[0]} = {pair.split(' ')[0]}\n")
    
    #Visitor pattern
    f.write(f"\tdef accept(self, visitor: Visitor):\n")
    f.write(f"\t\treturn visitor.visit_{class_name.lower()}_{base_name.lower()}(self)\n")

def define_visitor(f: TextIOWrapper, base_name: str, types: List[str]):
    f.write("class Visitor:\n")
    for type in types:
        typename = type.split(":")[0].strip()
        f.write(f"\tdef visit_{typename.lower()}_{base_name.lower()}({base_name.lower()}: {typename}): pass\n")

def define_ast(output_dir: str, base_name: str, types: List[str]):
    path = output_dir + "/" + base_name.lower() + ".py"
    with open(path, 'w') as f:
        #import token
        f.write("from .tok import Token\n")
        #Visitor interface
        define_visitor(f, base_name, types)

        #Base abstract class
        f.write(f"\nclass {base_name}:\n")
        f.write("\tdef accept(visitor: Visitor): pass\n")

        for type in types:
            class_name = type.split(":")[0].strip()
            fields = type.split(":")[1].strip()
            define_type(f, base_name, class_name, fields)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate_ast <output directory>")
        sys.exit(64)
    output_dir = sys.argv[1]

    define_ast(output_dir, "Expr", [
        "Binary   : left Expr, operator Token, right Expr",
        "Grouping : expression Expr",
        "Literal  : value object",
        "Unary    : operator Token, right Expr"
    ])