from Lexer import Lexer
from MyParser import MyParser

code = """
    program main;
    var int x;
    var float res_D;
    arr int y[10];
    arr float z[10, 10];
    procedure int B(var int n);
        procedure int C(var int n);
            var float num;
            procedure int E(var int n, arr int a);
            var int x;
            begin
                x := n-1;
                return x;
            end
        begin
            x:= n-1;
            return x;
        end
        procedure float D(var int n);
        var int res_C;
        begin
            x:= n-1;
            res_C := call C(x);
            return res_C;
        end
    begin
        x := n-1;
        res_D := call D(x);
        return res_D;
    end

    begin
        x := 5;
        res_B := call B(x);
        write(x);
    end
"""

lexer = Lexer(code)
tokens = lexer.lex()
# for token in tokens:
#     print(token)
parser = MyParser(tokens)
parser.parse()
print(parser.tables)

