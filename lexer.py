from enum import Enum


class TokenType(Enum):
    # keywords
    CONST_VAR = "const"

    IDENTIFIER = "identifier"
    LITERAL = "literal"

    # symbols
    COMMA = ","
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    COLON = ":"
    EQUAL = "="
    MINUS = "-"
    SEMICOLON = ";"
    LBRACKET = "["
    RBRACKET = "]"

    EOF = "eof"


KEYWORDS = {
    "const": TokenType.CONST_VAR,
}


class Token:
    def __init__(self, token_type: TokenType, value=None):
        self.token_type = token_type
        self.value = value

    def __repr__(self):
        if self.value is not None:
            return f"({self.token_type.name}, {repr(self.value)})"
        else:
            return f"({self.token_type.name})"


class Lexer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.position = 0

    def _current_char(self):
        if self.position >= len(self.source):
            return None
        return self.source[self.position]

    def _advance(self):
        self.position += 1

    def tokenize(self):
        tokens = []
        while True:
            token = self._next_token()
            tokens.append(token)
            if token.token_type == TokenType.EOF:
                break
        return tokens

    def _next_token(self):
        current = self._current_char()
        if current is None:
            return Token(TokenType.EOF)

        if current.isspace():
            while True:
                self._advance()
                current = self._current_char()
                if current is None:
                    return Token(TokenType.EOF)
                elif not current.isspace():
                    break

        match current:
            case "{":
                return self._consume_token(TokenType.LBRACE)
            case "}":
                return self._consume_token(TokenType.RBRACE)
            case "(":
                return self._consume_token(TokenType.LPAREN)
            case ")":
                return self._consume_token(TokenType.RPAREN)
            case ":":
                return self._consume_token(TokenType.COLON)
            case ",":
                return self._consume_token(TokenType.COMMA)
            case "=":
                return self._consume_token(TokenType.EQUAL)
            case "-":
                return self._consume_token(TokenType.MINUS)
            case ";":
                return self._consume_token(TokenType.SEMICOLON)
            case "[":
                return self._consume_token(TokenType.LBRACKET)
            case "]":
                return self._consume_token(TokenType.RBRACKET)
            case "\"":
                return self._parse_str()
            case _:
                return self._parse_other()

    def _consume_token(self, token_type):
        self._advance()
        return Token(token_type)

    def _parse_other(self):
        current = self._current_char()
        if current.isnumeric():
            return self._parse_num()
        return self._parse_identifier()

    def _parse_num(self):
        current = self._current_char()
        content = current

        # 目前不需要考虑小数点 owo
        while True:
            self._advance()
            current = self._current_char()
            if current is None or not current.isnumeric():
                break
            content += current

        return Token(TokenType.LITERAL, content)

    def _parse_str(self):
        self._advance()  # skip first "

        current = self._current_char()
        content = current
        while True:
            self._advance()
            current = self._current_char()
            if current is None:
                raise Exception("Unterminated string literal")
            elif current == "\"":
                break
            content += current

        self._advance()  # skip end "
        return Token(TokenType.LITERAL, content)

    def _parse_identifier(self):
        current = self._current_char()
        content = current

        while True:
            self._advance()
            current = self._current_char()
            if current is None:
                break
            elif current.isspace() or not current.isalpha():
                break
            content += current

        return Token(KEYWORDS.get(content, TokenType.IDENTIFIER), content)
