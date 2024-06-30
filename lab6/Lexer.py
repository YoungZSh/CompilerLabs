import re

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.token_types = [
            ('program', r'program'),
            ('procedure', r'procedure'),
            ('var', r'var'),
            ('const', r'const'),
            ('begin', r'begin'),
            ('end', r'end'),
            ('if', r'if'),
            ('then', r'then'),
            ('else', r'else'),
            ('while', r'while'),
            ('do', r'do'),
            ('odd', r'odd'),
            ('call', r'call'),
            ('read', r'read'),
            ('write', r'write'),
            ('int', r'int'),
            ('float', r'float'),
            ('arr', r'arr'),
            ('return', r'return'),
            (';', r';'),
            (',', r','),
            (':=', r':='),
            ('=', r'='),
            ('<>', r'<>'),
            ('<', r'<'),
            ('<=', r'<='),
            ('>', r'>'),
            ('>=', r'>='),
            ('(', r'\('),
            (')', r'\)'),
            ('[', r'\['),
            (']', r'\]'),
            ('+', r'\+'),
            ('-', r'-'),
            ('*', r'\*'),
            ('/', r'/'),
            ('<id>', r'[a-zA-Z][a-zA-Z0-9|_]*'),  # identifier
            ('<integer>', r'\d+'),  # integer
        ]
        self.tokens = []

    def lex(self):
        while self.pos < len(self.text):
            matched = False
            if re.match(r'\s', self.text[self.pos]):
                self.pos += 1
                continue
            for token_type, pattern in self.token_types:
                regex = re.compile(pattern)
                match = regex.match(self.text, self.pos)
                if match:
                    value = match.group(0)
                    self.tokens.append((token_type, value))
                    self.pos = match.end()
                    matched = True
                    break
            if not matched:
                raise SyntaxError(f"Unexpected character '{self.text[self.pos]}' at position {self.pos}.")
        return self.tokens

