class EvalError(Exception):
    pass

class Evaluator:
    def __init__(self):
        self.global_env = {}
        self.env_stack = [self.global_env]
        
    def evaluate(self, node):
        method_name = f'eval_{node.node_type.name.lower()}'
        method = getattr(self, method_name, self.generic_eval)
        return method(node)
    
    def generic_eval(self, node):
        raise EvalError(f"No eval_{node.node_type.name.lower()} method")
    
    def current_env(self):
        return self.env_stack[-1]

    def push_env(self):
        self.env_stack.append({})
    
    def pop_env(self):
        self.env_stack.pop()
        
    def eval_program(self, node):
        result = None
        for stmt in node.children:
            result = self.evaluate(stmt)
        return result
    
    def eval_number(self, node):
        return node.leaf
    
    def eval_bool_val(self, node):
        return node.leaf == '#t'
    
    def eval_num_op(self, node):
        operator = node.leaf
        operands = [self.evaluate(child) for child in node.children]
        if operator == '+':
            return sum(operands)
        elif operator == '-':
            if len(operands) == 1:
                return -operands[0]
            return operands[0] - operands[1]
        elif operator == '*':
            result = 1
            for op in operands:
                result *= op
            return result
        elif operator == '/':
            if len(operands) != 2:
                raise EvalError("Division requires exactly two operands")
            if operands[1] == 0:
                raise EvalError("Division by zero")
            return operands[0] / operands[1]
        elif operator == '%':
            if len(operands) != 2:
                raise EvalError("Modulus requires exactly two operands")
            return operands[0] % operands[1]
        elif operator == '>':
            if len(operands) != 2:
                raise EvalError("Greater-than operator requires exactly two operands")
            return operands[0] > operands[1]
        elif operator == '<':
            if len(operands) != 2:
                raise EvalError("Less-than operator requires exactly two operands")
            return operands[0] < operands[1]
        elif operator == '=':
            if len(operands) < 2:
                raise EvalError("Equality operator requires at least two operands")
            first = operands[0]
            return all(op == first for op in operands[1:])
        else:
            raise EvalError(f"Unknown operator '{operator}'")
    
    def eval_print(self, node):
        expr = self.evaluate(node.children[0])
        if node.leaf == 'PRINT_NUM':
            print(int(expr))
        elif node.leaf == 'PRINT_BOOL':
            print('#t' if expr else '#f')
        else:
            raise EvalError(f"Unknown print type '{node.leaf}'")
        return None 