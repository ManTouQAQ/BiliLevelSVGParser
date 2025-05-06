from lexer import Token, TokenType


class ASTNode:
    pass


class StatementNode(ASTNode):
    pass


class ExpressionNode(ASTNode):
    pass


class VariableDeclarationNode(StatementNode):
    def __init__(self, name, expr: ExpressionNode):
        self.name = name
        self.expr = expr

    def __repr__(self):
        return f"(var {self.name} = {repr(self.expr)})"


class LiteralExpressionNode(ExpressionNode):
    def __init__(self, value: object):
        self.value = value

    def __repr__(self):
        return f"{repr(self.value)}"


class VariableExpressionNode(ExpressionNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class ArrayExpressionNode(ExpressionNode):
    def __init__(self, fields: list[ExpressionNode]):
        self.fields = fields

    def __repr__(self):
        fields_repr = ", ".join(repr(field) for field in self.fields)
        return f"([{fields_repr}])"


class UnaryExpressionNode(ExpressionNode):
    def __init__(self, op: TokenType, expr: ExpressionNode):
        self.op = op
        self.expr = expr

    def __repr__(self):
        return f"({self.op.name} {repr(self.expr)})"


class StructExpressionNode(ExpressionNode):
    def __init__(self, fields: dict[str, ExpressionNode]):
        self.fields = fields

    def __repr__(self):
        fields_repr = ", ".join(f"{k}: {repr(v)}" for k, v in self.fields.items())
        return f"{{{fields_repr}}}"


class FunctionCallNode(ExpressionNode):
    def __init__(self, name, args: list[ExpressionNode]):
        self.name = name
        self.args = args

    def __repr__(self):
        args_repr = ", ".join(repr(arg) for arg in self.args)
        return f"{self.name}({args_repr})"


class Parser:
    def __init__(self, tokens: list[Token]):
        self.statements = []
        self.tokens = tokens
        self.position = 0

    def _peek(self):
        return self.tokens[self.position]

    def _advance(self):
        if self._is_at_end():
            raise Exception("Can't advance at end")

        self.position += 1

    def _consume(self, expected_type):
        token = self._peek()
        if token.token_type != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got {token.token_type}")
        self._advance()
        return token

    def _match(self, expected_type):
        if self._peek().token_type != expected_type:
            return False
        self._advance()
        return True

    def _is_at_end(self):
        return self.position >= len(self.tokens) or self.tokens[self.position].token_type == TokenType.EOF

    def parse(self):
        self.statements.clear()

        while not self._is_at_end():
            self._parse_statement()

        return self.statements

    def _parse_statement(self):
        if self._match(TokenType.CONST_VAR):
            self._parse_decl_variable()
            return

        raise Exception("Unknown statement")

    def _parse_decl_variable(self):
        while True:
            name = self._consume(TokenType.IDENTIFIER)
            self._consume(TokenType.EQUAL)

            self.statements.append(VariableDeclarationNode(name, self._parse_expression()))

            if self._match(TokenType.COMMA):
                continue
            self._consume(TokenType.SEMICOLON)
            break

    def _parse_expression(self):
        # 没有必要添加其他的表达式解析, (人话: 懒)
        return self._parse_unary()

    def _parse_unary(self):
        if self._peek().token_type == TokenType.MINUS:
            token = self._peek()
            self._advance()
            right = self._parse_unary()
            return UnaryExpressionNode(token.token_type, right)

        return self._parse_call()

    def _parse_call(self):
        expr = self._parse_primary()

        while True:
            if self._match(TokenType.LPAREN):
                args = []
                if self._peek().token_type != TokenType.RPAREN:
                    while True:
                        args.append(self._parse_expression())
                        if self._match(TokenType.COMMA):
                            continue
                        break

                self._consume(TokenType.RPAREN)
                expr = FunctionCallNode(expr, args)
            else:
                break

        return expr

    def _parse_primary(self):
        if self._peek().token_type == TokenType.LITERAL:
            token = self._consume(TokenType.LITERAL)
            return LiteralExpressionNode(token.value)

        if self._peek().token_type == TokenType.IDENTIFIER:
            token = self._consume(TokenType.IDENTIFIER)
            return VariableExpressionNode(token.value)

        if self._match(TokenType.LBRACKET):
            return self._parse_array()

        if self._match(TokenType.LBRACE):
            return self._parse_struct()

        raise Exception(f"Unknown expression type {self._peek().token_type}")

    def _parse_array(self):
        fields = []
        while not self._match(TokenType.RBRACKET):
            fields.append(self._parse_expression())

            if not self._match(TokenType.COMMA):
                self._consume(TokenType.RBRACKET)
                break

        return ArrayExpressionNode(fields)

    def _parse_struct(self):
        fields = {}
        while not self._match(TokenType.RBRACE):
            key = self._peek().value
            self._advance()
            self._consume(TokenType.COLON)
            value = self._parse_expression()
            fields[key] = value
            if not self._match(TokenType.COMMA):
                self._consume(TokenType.RBRACE)
                break

        return StructExpressionNode(fields)
