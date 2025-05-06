import argparse
from typing import cast
from xml.etree import ElementTree

from lexer import Lexer
from parser import *


def js_code_stmts_to_svg(statements: list[StatementNode]):
    svg_stmt = cast(VariableDeclarationNode, statements[1])
    svg = ElementTree.Element("svg")
    for key, value in cast(StructExpressionNode, svg_stmt.expr).fields.items():
        value = cast(str, cast(LiteralExpressionNode, value).value)
        svg.set(key, value)

    for path_stmt in statements[2:]:
        # noinspection PyBroadException
        try:
            path = ElementTree.Element("path")
            path_props = cast(FunctionCallNode, cast(VariableDeclarationNode, path_stmt).expr).args[1]
            for key, value in cast(StructExpressionNode, path_props).fields.items():
                value = cast(str, cast(LiteralExpressionNode, value).value)
                path.set(key, value)

            svg.append(path)
        except Exception as _:
            break

    return svg


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True, help="Input file")
    parser.add_argument('-o', '--output', type=str, required=True, help="Output file")
    args = parser.parse_args()

    js_code = read_file(args.input)
    lexer = Lexer(js_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    stmts = parser.parse()
    svg = js_code_stmts_to_svg(stmts)
    write_file(args.output, ElementTree.tostring(svg, "unicode"))


def read_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


def write_file(path: str, content: str):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)


if __name__ == "__main__":
    main()
