%{
#include <stdio.h>
#include <stdlib.h>
#include "parser.tab.h"
%}

%%
[0-9]+"."[0-9]+([eE][+-]?[0-9]+)?    { yylval.num = atof(yytext); return NUM; }
[0-9]+([eE][+-]?[0-9]+)?            { yylval.num = atof(yytext); return NUM; }
"+"               { return PLUS; }
"-"               { return MINUS; }
"*"               { return MUL; }
"/"               { return DIV; }
"("               { return LPAREN; }
")"               { return RPAREN; }
[ \t]             ;  // Skip whitespace
\n                { return '\n'; }
.                 { printf("Unknown character %c\n", *yytext); return UNKNOWN; }

%%

int yywrap() {
    return 1;
}
