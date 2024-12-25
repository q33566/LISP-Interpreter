from utils.my_yacc import parse_input
from utils.my_visitor import EvalError
import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse and evaluate input file.')
    parser.add_argument('filename', nargs='?', help='Path to the input file (.in)')

    args = parser.parse_args()

    if args.filename:
        try:
            with open(args.filename, 'r') as f:
                content = f.read()
            parse_input(content)
        except FileNotFoundError:
            print(f"Error: File '{args.filename}' not found.")
        except SyntaxError as e:
            print(f"Syntax Error in file '{args.filename}': {e}")
        except EvalError as e:
            print(f"Evaluation Error in file '{args.filename}': {e}")
        except Exception as e:
            print(f"An unexpected error occurred while processing '{args.filename}': {e}")
    else:
        # Interactive mode
        while True:
            try:
                s = input('input: ')
            except EOFError:
                print("\nExiting.")
                break
            if not s.strip():
                continue
            parse_input(s)