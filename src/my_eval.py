from my_ast import AstNode
class EvalError(Exception):
    pass
class Function:
    def __init__(self, param_names, body, env):
        self.param_names = param_names
        self.body = body
        self.env = env
        
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
    
    @property
    def current_env(self):
        return self.env_stack[-1]

    def push_env(self, new_env=None):
        if new_env is None:
            new_env = {}
        self.env_stack.append(new_env)
    
    def pop_env(self):
        self.env_stack.pop()
        
    def eval_program(self, node):
        result = None
        for stmt in node.children:
            result = self.evaluate(stmt)
        return result
    
    def eval_define(self, node: AstNode):
        variable_node: AstNode = node.children[0]
        value_node: AstNode = node.children[1]
        variable_value = self.evaluate(value_node)
        self.current_env[variable_node.leaf] = variable_value
        return variable_value
    
    def eval_variable(self, node: AstNode):
        var_name = node.leaf
        for environment in reversed(self.env_stack):
            if var_name in environment:
                return environment[var_name]
        raise EvalError(f"Undefined variable '{var_name}'")
    
    def eval_number(self, node: AstNode):
        return int(node.leaf)
    
    def eval_bool_val(self, node: AstNode):
        return node.leaf
    
    def eval_num_op(self, node):
        operator = node.leaf
        operands = [self.evaluate(child) for child in node.children]
        for operand in operands:
            if isinstance(operand, bool):
                raise EvalError('Type error!')
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
            return int(operands[0] / operands[1])
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
    def eval_logical_op(self, node: AstNode):
        operator = node.leaf
        if operator == 'and':
            children: list[AstNode] = node.children
            for child in children:
                result = self.evaluate(child)
                if not result:
                    return False
            return True
        elif operator == 'or':
            children: list[AstNode] =  node.children
            for child in children:
                result = self.evaluate(child)
                if result:
                    return True
            return False
        elif operator == 'not':
            child: AstNode =  node.children[0]
            if len(node.children) != 1:
                raise EvalError("'not' operator requires exactly one operand")
            return not self.evaluate(child)
        else:
            raise EvalError(f"Unknown logical operator '{operator}'")
    
    
    def eval_if_exp(self, node: AstNode):
        condition: AstNode = node.children[0]
        true_branch: AstNode = node.children[1]
        false_branch: AstNode = node.children[2]
        
        
        if(self.evaluate(condition)):
            return self.evaluate(true_branch)
        else:
            return self.evaluate(false_branch)
    
    def eval_print(self, node):
        expr = self.evaluate(node.children[0])
        if node.leaf == 'PRINT_NUM':
            # if(isinstance(expr, bool)):
            #     raise EvalError('Type error!')
            print(int(expr))
        elif node.leaf == 'PRINT_BOOL':
            # if(isinstance(expr, int)):
            #     raise EvalError('Type error!')
            print('#t' if expr else '#f')
        else:
            raise EvalError(f"Unknown print type '{node.leaf}'")
        return None 
    
    def eval_fun(self, node:AstNode):
        # fun_ids: AstNode = node.children[0]
        fun_ids: list  = node.children[0]
        fun_body = node.children[1]
        param_names = fun_ids
        return Function(body=fun_body, param_names=param_names, env=self.current_env.copy())

    def eval_fun_call(self, node:AstNode):
        fun = self.evaluate(node.children[0])
        if not isinstance(fun, Function):
            raise EvalError(f"'{fun}' is not a function")
        args = [self.evaluate(arg) for arg in node.children[1:]]
        
        if len(args) != len(fun.param_names):
            raise EvalError(f"Function expected {len(fun.param_names)} arguments, got {len(args)}")
        
        new_env = fun.env.copy()
        for param, arg in zip(fun.param_names, args):
            new_env[param] = arg
        
        self.push_env(new_env)
        for param, arg in zip(fun.param_names, args):
            self.current_env[param] = arg
        try:
            result = self.evaluate(fun.body)
        finally:
            self.pop_env()
        return result
            