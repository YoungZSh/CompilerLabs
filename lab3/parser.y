%{
#include <stdio.h>
#include <stdlib.h>
void yyerror(const char* s);
int yylex();
int yyparse();

#define YYDEBUG 0  // 关闭Bison的内置调试信息

%}

%union {
    double num;
}

%token <num> NUM
%token PLUS MINUS MUL DIV LPAREN RPAREN UNKNOWN

%left PLUS MINUS
%left MUL DIV

%type <num> expr

%%

input: /* empty */
     | input line
     ;

line: expr '\n' { printf("%g\n", $1); }
    | '\n'
    | UNKNOWN '\n' { yyerror("Invalid input, skipping to next line"); yyerrok; yyclearin;return -1; }
    | error '\n' { yyerror("Invalid input, skipping to next line"); yyerrok; yyclearin;return -1; }
    ;

expr: expr PLUS expr    { printf("expr PLUS expr: %g + %g\n", $1, $3); $$ = $1 + $3; }
    | expr MINUS expr   { printf("expr MINUS expr: %g - %g\n", $1, $3); $$ = $1 - $3; }
    | expr MUL expr     { printf("expr MUL expr: %g * %g\n", $1, $3); $$ = $1 * $3; }
    | expr DIV expr     { 
        if ($3 == 0) {
            yyerror("Division by zero, skipping to next line");
            yyerrok;
            yyclearin;
            return -1;
        } else {
            printf("expr DIV expr: %g / %g\n", $1, $3);
            $$ = $1 / $3;
        }
      }
    | LPAREN expr RPAREN { printf("LPAREN expr RPAREN: ( %g )\n", $2); $$ = $2; }
    | NUM                { printf("NUM: %g\n", $1); $$ = $1; }
    | MINUS expr %prec MUL { printf("MINUS expr: - %g\n", $2); $$ = -$2; }
    ;

%%

void yyerror(const char* s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main() {
    printf("Enter expressions: \n");
    while (1) {
        yyparse();
    }
    return 0;
}
