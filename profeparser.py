class Parser(sly.Parser):
    '''
    '''
    debugfile='pl0.txt'

    tokens = Lexer.tokens

    precedence = (
        ('left', OR),
        ('left', AND),
        ('left', EQ, NE),
        ('left', LT, GT, LE, GE),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', NOT, UNARY),
    )

    @_("funclist")
    def program(self, p):
        ...

    @_("function { function }")
    def funclist(self, p):
        ...

    @_("FUN ID parmlist varlist BEGIN stmtlist END")
    def function(self, p):
        ...

    @_("'(' [ parmlistitems ] ')'")
    def parmlist(self, p):
        ...

    @_("parm { ',' parm }")
    def parmlistitems(self, p):
        ...

    @_("ID ':' typename")
    def parm(self, p):
        ...

    @_("INT", "FLOAT")
    def typename(self, p):
        ...

    @_("INT '[' expr ']'", "FLOAT '[' expr ']'")
    def typename(self, p):
        ...

    @_("[ declist ]")
    def varlist(self, p):
        ...

    @_("vardecl ';' { vardecl ';' } ")
    def declist(self, p):
        ...

    @_("parm", "function")
    def vardecl(self, p):
        ...

    @_("stmt { ';' stmt }")
    def stmtlist(self, p):
        ...

    @_("PRINT '(' STRING ')'",
       "WRITE '(' expr ')'",
       "READ '(' location ')'",
       "WHILE relop DO stmt",
       "BREAK",
       "IF relop THEN stmt [ ELSE stmt ]",
       "BEGIN stmtlist END",
       "location ASSIGN expr",
       "RETURN expr",
       "SKIP",
       "ID '(' exprlist ')'")
    def stmt(self, p):
        ...

    @_("ID")
    def location(self, p):
        ...

    @_("ID '[' expr ']'")
    def location(self, p):
        ...

    @_("[ exprlistitems ]")
    def exprlist(self, p):
        ...

    @_("expr { ',' expr }")
    def exprlistitems(self, p):
        ...

    @_("expr '+' expr",
       "expr '-' expr",
       "expr '*' expr",
       "expr '/' expr",
       "'-' expr %prec UNARY",
       "'+' expr %prec UNARY",
       "'(' expr ')'",
       "INUMBER",
       "FNUMBER",
       "ID",
       "ID '[' expr ']'",
       "ID '(' exprlist ')'",
       "INT '(' expr ')'",
       "FLOAT '(' expr ')'")
    def expr(self, p):
        ...
    
    @_("expr LT expr",
       "expr LE expr",
       "expr GT expr",
       "expr GE expr",
       "expr EQ expr",
       "expr NE expr",
       "relop AND relop",
       "relop OR relop",
       "NOT relop")
    def relop(self, p):
        ...
    

txt = 'fun hola(a:int, b:float)'

lex = Lexer()
parser = Parser()
parser.parse(lex.tokenize(txt))