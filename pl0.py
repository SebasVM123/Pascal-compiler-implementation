# pl0.py
'''
usage: pl0.py [-h] [-d] [-o OUT] [-l] [-D] [-p] [-I] [--sym] [-S] [-R] input

Compiler for PL0

positional arguments:
  input              PL0 program file to compile

optional arguments:
  -h, --help         show this help message and exit
  -l, --lex          Store output of lexer
  -a, --ast          Generate AST graph as txt format
  -I, --ir           Dump the generated Intermediate representation
  -s, --sym          Dump the symbol table
'''
from contextlib import redirect_stdout
from context import Context
from rich import print

import argparse


def parse_args():
    cli = argparse.ArgumentParser(
        prog='pl0.py',
        description='Compiler for PL0 programs')

    cli.add_argument(
        '-v', '--version',
        action='version',
        version='0.1')

    file_group = cli.add_argument_group('Formatting options')

    file_group.add_argument(
        'input',
        type=str,
        nargs='?',
        help='PL0 program file to compile')

    mutex = file_group.add_mutually_exclusive_group()

    mutex.add_argument(
        '-l', '--lex',
        action='store_true',
        default=False,
        help='Store output of lexer')

    mutex.add_argument(
        '-a', '--ast',
        action='store_true',
        default=False,
        help='Generate AST graph as txt format')

    mutex.add_argument(
        '-s', '--sym',
        action='store_true',
        help='Dump the symbol table')

    return cli.parse_args()


if __name__ == '__main__':

    args = parse_args()
    context = Context()

    if args.input:
        file_name = args.input

        with open(file_name, encoding='utf-8') as file:
            source = file.read()

        if args.lex:
            file_lex = file_name.split('.')[0] + '.lex'
            print(f'[green]print lexer: {file_lex}[/green]')

            with open(file_lex, 'w', encoding='utf-8') as f:
                with redirect_stdout(f):
                    errors = context.print_lexer(source)
                if errors:
                    print(f'[red]Warning: there are {len(errors)} errors: ')
                    for error in errors:
                        print(f'[red]{error}[/red]')

        elif args.ast:
            file_ast = file_name.split('.')[0] + '.ast'
            print(f'[green]print AST: {file_ast}[/green]')

            with open(file_ast, 'w', encoding='utf-8') as f:
                with redirect_stdout(f):
                    errors = context.print_AST(source)

                if context.have_errors:
                    if errors:
                        print(f'[red]Warning: not possible to dump AST because there are {len(errors)} errors: ')
                        for error in errors:
                            print(f'[red]{error}[/red]')
                    else:
                        print(f'[red]File is empty[/red]')

        elif args.sym:
            file_sym = file_name.split('.')[0] + '.sym'
            print(f'[green]print AST: {file_sym}[/green]')

            with open(file_sym, 'w', encoding='utf-8') as f:
                with redirect_stdout(f):
                    errors = context.print_symtab(source)

            if errors:
                print(f'[red]Warning: there are {len(errors)} errors: ')
                for error in errors:
                    print(f'[red]{error}[/red]')
