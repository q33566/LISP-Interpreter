### 🚀 How This Program Works
![alt text](image.png)
1. Use `my_lex.py` to perform lexical analysis.
2. Use `my_yacc.py` to construct the AST. The definition of an AST node can be found in `my_ast.py` 
3. Use `Visotor` class to iterate throuth each node in AST and perform the correspoding action. (see `my_visitor.py` for more details.)


### 🛠️ How to Run the Main Program
1. `pip install -r requirements.txt`
2. `cd src`
3. `py main.py`

You can also provide an input file to main.py.

    $ py main.py example.lsp

### 🧪 How to Run Test Cases
1. `pip install -r requirements.txt`
2. `cd src`
3. `cd test`
4. `pytest test.py`


*To add custom test cases:*

- Place the input and output files in the `public_test_data` directory.
- Ensure that each input file has a corresponding output file with the same filename (e.g., test1.input and test1.output).

### 🌐 Environment
- python 3.10.11
- Windows 11