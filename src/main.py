from utils.my_yacc import parse_input
if __name__ == "__main__":
    while True:
        try:
            s = input('input: ')
        except EOFError:
            break
        if not s:
            continue
        parse_input(s)