
  
def main(argv):
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} filename")
        exit(1)

    lex = Lexer()
    txt = open('test3/' + argv[1]).read()
    parser = Parser()
    Nodo = parser.parse(lex.tokenize(txt))
    semantico=Checker()
    Tabla= Symtab()
    semantico.visit(Nodo,Tabla)



if __name__ == '__main__':
    from sys import argv
    main(argv)
