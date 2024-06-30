from SymbolTable import SymbolTableDict

class MyParser:
    """
    语法分析器识别文法：
    <prog> → program <id>; <block>
    <block> → [<vardecl>][<array>][<proc>]<body>
    <vardecl> → var [<intvar>|<floatvar>];
    <intvar> → int <id>
    <floatvar> → float <id>
    <array> → arr [<intarr>|<floatarr>];
    <intarr> → int <id>[<integer>{,<integer>}]
    <floatarr> → float <id>[<integer>{,<integer>}]
    <proc> → procedure [int|float] <id>([<vardecl>{,<vardecl>}][<arrptt>{,<arrptt>}]);<block>{;<proc>}
    <arrptt> → arr [<intvar>|<floatvar>];
    <body> → begin <statement>{;<statement>}end
    <statement> → <id>{[<integer>{,<integer>}]} := [<exp> | call <id>([<exp>{,<exp>}])] 
                |if <lexp> then <statement>[else <statement>]
                |while <lexp> do <statement>
                |<body>
                |read (<id>{,<id>})
                |write (<exp>{,<exp>})
                |return [<id>|<exp>]
    <lexp> → <exp> <lop> <exp>|odd <exp>
    <exp> → [+|-]<term>{<aop><term>}
    <term> → <factor>{<mop><factor>}
    <factor>→<id>|<integer>|(<exp>)
    <lop> → =|<>|<|<=|>|>=
    <aop> → +|-
    <mop> → *|/
    <id> → l{l|d} (注:l 表示字母)
    <integer> → d{d}
    """
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.current_token = None
        self.tables = SymbolTableDict()
        self.next_token()
        self.is_ptt = False
        self.table_stack = []
        self.size = 0
        self.size_stack = []

    def next_token(self):
        try:
            self.current = next(self.tokens)
            self.current_token = self.current[0]
            # print(f"Current token: {self.current}")
        except StopIteration:
            self.current_token = None

    def match(self, expected_token):
        if self.current_token == expected_token:
            if self.current_token == "<id>":
                self.current_id = self.current[1]
            self.next_token()
        else:
            raise SyntaxError(f"Expect '{expected_token}' but got '{self.current_token}'.")

    def program(self):
        self.match("program")
        self.tables.add_table(self.current[1])
        self.table_stack.append(self.tables.get_table(self.current[1]))
        self.current_table = self.table_stack[-1]
        self.match("<id>")
        self.match(";")
        self.block()

    def block(self):
        while self.current_token == "var":
            self.vardecl()
        while self.current_token == "arr":
            self.array()
        while self.current_token == "procedure":
            self.proc()
        self.body()

    def vardecl(self):
        self.match("var")
        if self.current_token == "int":
            self.intvar()
        if self.current_token == "float":
            self.floatvar()
        if self.current_token == ";":
            self.match(";")

    def intvar(self):
        self.match("int")
        self.size += 4
        self.current_table.add_symbol(name = self.current[1], type = "int", offset = self.size)
        self.match("<id>")
    
    def floatvar(self):
        self.match("float")
        self.size += 8
        self.current_table.add_symbol(name = self.current[1], type = "float", offset = self.size)
        self.match("<id>")

    def array(self):
        self.match("arr")
        if self.current_token == "int":
            self.intarr()
        if self.current_token == "float":
            self.floatarr()
        self.match(";")

    def intarr(self):
        self.match("int")
        name = self.current[1]
        self.current_table.add_symbol(name = name, type = "array", base = 0, etype = "int")
        self.match("<id>")
        self.match("[")
        size = int(self.current[1])
        self.match("<integer>")
        while self.current_token == ",":
            self.match(",")
            size *= int(self.current[1])
            self.match("<integer>")
        self.match("]")
        self.size += size * 4
        self.current_table.set_attribute(name = name, attribute = 'base', value = self.size)
    
    def floatarr(self):
        self.match("float")
        name = self.current[1]
        self.current_table.add_symbol(name = name, type = "array", base = 0, etype = "float")
        self.match("<id>")
        self.match("[")
        size = int(self.current[1])
        self.match("<integer>")
        while self.current_token == ",":
            self.match(",")
            size *= int(self.current[1])
            self.match("<integer>")
        self.match("]")
        self.size += size * 8
        self.current_table.set_attribute(name = name, attribute = 'base', value = self.size)

    def proc(self):
        self.match("procedure")
        if self.current_token == "int":
            self.match("int")
            rtype = "int"
        if self.current_token == "float":
            self.match("float")
            rtype = "float"
        self.size += 8
        self.current_table.add_symbol(name = self.current[1], type = "proc", offset = self.size)
        self.tables.add_table(self.current[1])
        self.table_stack.append(self.tables.get_table(self.current[1]))
        self.size_stack.append(self.size)
        self.size = 0
        self.current_table = self.table_stack[-1]
        name = self.table_stack[-2].symbol_table['name']
        self.current_table.symbol_table['outer'] = f'{name}@table'
        self.current_table.symbol_table['rtype'] = rtype
        self.match("<id>")
        arglist = []
        self.match("(")
        while self.current_token != ")":
            if self.current_token == "var":
                self.vardecl()
                arglist.append(self.current_id)
            if self.current_token == "arr":
                self.arrptt()
                arglist.append(self.current_id)
            if self.current_token == ",":
                self.match(",")
        self.match(")")
        self.match(";")
        self.current_table.symbol_table['argc'] = len(arglist)
        self.current_table.symbol_table['arglist'] = tuple(arglist)
        self.block()
        if self.current_token == ";":
            self.proc()
    
    def arrptt(self):
        self.match("arr")
        if self.current_token == "int":
            self.intvar()
            self.current_table.set_attribute(name = self.current_id, attribute = 'type', value = 'arrptt')
        if self.current_token == "float":
            self.floatvar()
            self.current_table.set_attribute(name = self.current_id, attribute = 'type', value = 'arrptt')
            self.size -= 4
            self.current_table.set_attribute(name = self.current_id, attribute = 'offset', value = self.size)
 
    def body(self):
        self.match("begin")
        self.statement()
        self.match(";")
        while self.current_token != "end":
            self.statement()
            self.match(";")
        self.match("end")
        self.table_stack.pop()
        if self.table_stack:
            self.current_table = self.table_stack[-1]
        if self.size_stack:
            self.size = self.size_stack[-1]
            self.size_stack.pop()

    def statement(self):
        if self.current_token == "<id>":
            self.match("<id>")
            if self.current_token == "[":
                self.match("[")
                self.match("<integer>")
                while self.current_token == ",":
                    self.match(",")
                    self.match("<integer>")
                self.match("]")
            self.match(":=")
            if self.current_token == "call":
                self.match("call")
                self.match("<id>")
                self.match("(")
                if self.current_token != ")":
                    self.exp()
                    while self.current_token == ",":
                        self.match(",")
                        self.exp()
                self.match(")")
            else:
                self.exp()
        elif self.current_token == "if":
            self.match("if")
            self.lexp()
            self.match("then")
            self.statement()
            if self.current_token == "else":
                self.match("else")
                self.statement()
        elif self.current_token == "while":
            self.match("while")
            self.lexp()
            self.match("do")
            self.statement()
        # elif self.current_token == "call":
        #     self.match("call")
        #     self.match("<id>")
        #     self.match("(")
        #     if self.current_token != ")":
        #         self.exp()
        #         while self.current_token == ",":
        #             self.match(",")
        #             self.exp()
        #     self.match(")")
        elif self.current_token == "begin":
            self.body()
        elif self.current_token == "read":
            self.match("read")
            self.match("(")
            self.match("<id>")
            while self.current_token == ",":
                self.match(",")
                self.match("<id>")
            self.match(")")
        elif self.current_token == "write":
            self.match("write")
            self.match("(")
            self.exp()
            while self.current_token == ",":
                self.match(",")
                self.exp()
            self.match(")")
        elif self.current_token == "return":
            self.match("return")
            if self.current_token == "<id>":
                self.match("<id>")
            else:
                self.exp()

    def lexp(self):
        if self.current_token == "odd":
            self.match("odd")
            self.exp()
        else:
            self.exp()
            self.match("<lop>")
            self.exp()

    def exp(self):
        if self.current_token in ["+", "-"]:
            self.match(self.current_token)
        self.term()
        while self.current_token in ["+", "-"]:
            self.match(self.current_token)
            self.term()

    def term(self):
        self.factor()
        while self.current_token in ["*", "/"]:
            self.match(self.current_token)
            self.factor()

    def factor(self):
        if self.current_token == "<id>":
            self.match("<id>")
        elif self.current_token == "<integer>":
            self.match("<integer>")
        elif self.current_token == "(":
            self.match("(")
            self.exp()
            self.match(")")
        else:
            raise SyntaxError("Expected identifier, integer, or '('.")

    def parse(self):
        self.program()
        if self.current_token is not None:
            raise SyntaxError("Unexpected tokens after end of program.")
        for _, table in self.tables.symbol_tables.items():
            last_key = list(table.symbol_table)[-1]
            if last_key != 'code':
                if 'offset' in table.symbol_table[last_key]:
                    table.symbol_table['width'] = table.symbol_table[last_key]['offset']
                elif 'base' in table[last_key]:
                    table.symbol_table['width'] = table.symbol_table[last_key]['base']

