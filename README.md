### 🚀 How This Program Works
![alt text](image.png)
1. Use `my_lex.py` to perform lexical analysis.
2. Use `my_yacc.py` to construct the AST. The definition of an AST node can be found in `my_ast.py` 
3. Use `Visotor` class to iterate throuth each node in AST and perform the correspoding action. (see `my_visitor.py` for more details.)


### 🛠️ How to Run the Main Program
1. Install [uv](https://github.com/astral-sh/uv) as the package manager:  
   ```bash
   pip install uv
   ```

2. Navigate to the `src` directory:  
   ```bash
   cd src
   ```

3. Execute the main program:  
   ```bash
   uv run python main.py
   ```

   During execution, the terminal will prompt for input:
   ```bash
   input:
   ```

   For example, given the following input:
   ```bash
   input: (print-num (mod 10 4))
   ```

   The output will be:
   ```bash
   2
   ```
1. To run with an input file, specify the file path:  
   ```bash
   uv run python main.py example.lsp
   ```

### 🧪 How to Run Test Cases

1. Navigate to the `test` directory:  
   ```bash
   cd test
   ```

2. Run the test script using `pytest`:  
   ```bash
   uv run pytest test.py
   ```


*To add custom test cases:*

- Place the input and output files in the `public_test_data` directory.
- Ensure that each input file has a corresponding output file with the same filename (e.g., test1.input and test1.output).

### 🌐 Environment
- python 3.11
- Windows 11


### 📝 Completed Features
- [x] Syntax Validation
- [x] Print
- [x] Logical Operations
- [x] if Expression
- [x] Variable Definition
- [x] Function
- [x] Named Function
- [x] Recursion
- [x] Type Checking
- [x] Nested Function
- [x] First-class Function