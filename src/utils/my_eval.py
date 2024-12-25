class EvalError(Exception):
    pass
class Function:
    def __init__(self, param_names, body, env):
        self.param_names = param_names
        self.body = body
        self.env = env

class AstNode:
    def accept(self, visitor: 'Visitor'):
        method_name = 'visit_' + self.__class__.__name__.lower() + '_node'
        visit = getattr(visitor, method_name)
        return visit(self)
    
class Program(AstNode):
    def __init__(self, stmts: list[AstNode]):
        self.stmts = stmts
        
class Number(AstNode):
    def __init__(self, value: int):
        self.value = value
        
class Boolean(AstNode):
    def __init__(self, value: bool):
        self.value = value
        
class Print(AstNode):
    def __init__(self, exp: AstNode, print_type: str):
        self.exp = exp
        self.print_type = print_type

class NumOp(AstNode):
    def __init__(self, operator, operands):
        self.operator = operator
        self.operands = operands

class LogicalOp(AstNode):
    def __init__(self, operator, operands):
        self.operator = operator
        self.operands = operands
        
class IfExp(AstNode):
    def __init__(self, condition, true_branch, false_branch):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch
        
class Visitor:
    def visit_program_node(self, node: Program):
        stmts: list[AstNode] = node.stmts
        result = None
        for stmt in stmts:
            result = stmt.accept(self)
        return result
    
    def visit_number_node(self, node: Number):
        return node.value
    
    def visit_boolean_node(self, node: Boolean):
        return node.value
    
    def visit_print_node(self, node: Print):
        exp = node.exp.accept(self)
        print_type = node.print_type
        if(print_type == 'PRINT_NUM'):
            print(int(exp))
        elif(print_type == 'PRINT_BOOL'):
            symbol = '#t' if exp else '#f'
            print(symbol)
    
    def visit_numop_node(self, node: NumOp):
        operator = node.operator
        operands = [operand.accept(self) for operand in node.operands]
        for operand in operands:
            if isinstance(operand, bool):
                raise EvalError('Type error!')
        if operator == '+':
            return self._add(operands)
        elif operator == '-':
            return self._sub(operands)
        elif operator == '*':
            return self._mut(operands)
        elif operator == '/':
            return self._divide(operands)
        elif operator == '%':
            return self._mod(operands)
        elif operator == '>':
            return self._greater_than(operands)
        elif operator == '<':
            return self._less_than(operands)
        elif operator == '=':
            return self._equal(operands)
        else:
            raise EvalError(f"Unknown operator '{operator}'")
    
    def visit_logicalop_node(self, node: LogicalOp):
        operator = node.operator
        if operator == 'and':
            operands: list[AstNode] = node.operands
            for operand in operands:
                result = operand.accept(self)
                if not result:
                    return False
            return True
        elif operator == 'or':
            operands: list[AstNode] =  node.operands
            for operand in operands:
                result = operand.accept(self)
                if result:
                    return True
            return False
        elif operator == 'not':
            operand: AstNode =  node.operands[0]
            if len(node.operands) != 1:
                raise EvalError("'not' operator requires exactly one operand")
            return not operand.accept(self)
        else:
            raise EvalError(f"Unknown logical operator '{operator}'")
    
    def visit_ifexp_node(self, node: IfExp):
        condition: AstNode = node.condition
        true_branch: AstNode = node.true_branch
        false_branch: AstNode = node.false_branch
        if(condition.accept(self)):
            return true_branch.accept(self)
        return false_branch.accept(self)
    
    def _add(self, operands):
        return sum(operands)
    
    def _sub(self, operands):
        if len(operands) == 1:
            return -operands[0]
        return operands[0] - operands[1]
    
    def _mut(self, operands):
        result = 1
        for op in operands:
            result *= op
        return result
    
    def _divide(self, operands):
        if len(operands) != 2:
            raise EvalError("Division requires exactly two operands")
        if operands[1] == 0:
            raise EvalError("Division by zero")
        return int(operands[0] / operands[1])
    
    def _mod(self, operands):
        if len(operands) != 2:
            raise EvalError("Modulus requires exactly two operands")
        return operands[0] % operands[1]
    
    def _greater_than(self, operands):
        if len(operands) != 2:
            raise EvalError("Greater-than operator requires exactly two operands")
        return operands[0] > operands[1]
    
    def _less_than(self, operands):
        if len(operands) != 2:
            raise EvalError("Less-than operator requires exactly two operands")
        return operands[0] < operands[1]
    
    def _equal(self, operands):
        if len(operands) < 2:
            raise EvalError("Equality operator requires at least two operands")
        first = operands[0]
        return all(op == first for op in operands[1:])
    
    # @staticmethod
    # def generic_visit(node: AstNode):
    #     raise EvalError(f"No visit_{node.__class__.__name__.lower()}_node method")
    
# class Evaluator:
#     def __init__(self):
#         self.global_env = {}
#         self.env_stack = [self.global_env]
        
    
#     def evaluate(self, node):
#         method_name = f'eval_{node.node_type.name.lower()}'
#         method = getattr(self, method_name, self.generic_eval)
#         return method(node)
    
#     def generic_eval(self, node):
#         raise EvalError(f"No eval_{node.node_type.name.lower()} method")
    
#     @property
#     def current_env(self):
#         return self.env_stack[-1]

#     def push_env(self, new_env=None):
#         if new_env is None:
#             new_env = {}
#         self.env_stack.append(new_env)
    
#     def pop_env(self):
#         self.env_stack.pop()
        
#     def eval_program(self, node):
#         result = None
#         for stmt in node.children:
#             result = self.evaluate(stmt)
#         return result
    
#     def eval_define(self, node: AstNode):
#         variable_node: AstNode = node.children[0]
#         value_node: AstNode = node.children[1]
#         variable_value = self.evaluate(value_node)
#         self.current_env[variable_node.leaf] = variable_value
#         return variable_value
    
#     def eval_variable(self, node: AstNode):
#         var_name = node.leaf
#         for environment in reversed(self.env_stack):
#             if var_name in environment:
#                 return environment[var_name]
#         raise EvalError(f"Undefined variable '{var_name}'")
    
#     def eval_number(self, node: AstNode):
#         return int(node.leaf)
    
#     def eval_bool_val(self, node: AstNode):
#         return node.leaf
    
#     def eval_num_op(self, node):
#         operator = node.leaf
#         operands = [self.evaluate(child) for child in node.children]
#         for operand in operands:
#             if isinstance(operand, bool):
#                 raise EvalError('Type error!')
#         if operator == '+':
#             return sum(operands)
#         elif operator == '-':
#             if len(operands) == 1:
#                 return -operands[0]
#             return operands[0] - operands[1]
#         elif operator == '*':
#             result = 1
#             for op in operands:
#                 result *= op
#             return result
#         elif operator == '/':
#             if len(operands) != 2:
#                 raise EvalError("Division requires exactly two operands")
#             if operands[1] == 0:
#                 raise EvalError("Division by zero")
#             return int(operands[0] / operands[1])
#         elif operator == '%':
#             if len(operands) != 2:
#                 raise EvalError("Modulus requires exactly two operands")
#             return operands[0] % operands[1]
#         elif operator == '>':
#             if len(operands) != 2:
#                 raise EvalError("Greater-than operator requires exactly two operands")
#             return operands[0] > operands[1]
#         elif operator == '<':
#             if len(operands) != 2:
#                 raise EvalError("Less-than operator requires exactly two operands")
#             return operands[0] < operands[1]
#         elif operator == '=':
#             if len(operands) < 2:
#                 raise EvalError("Equality operator requires at least two operands")
#             first = operands[0]
#             return all(op == first for op in operands[1:])
#         else:
#             raise EvalError(f"Unknown operator '{operator}'")
#     def eval_logical_op(self, node: AstNode):
#         operator = node.leaf
#         if operator == 'and':
#             children: list[AstNode] = node.children
#             for child in children:
#                 result = self.evaluate(child)
#                 if not result:
#                     return False
#             return True
#         elif operator == 'or':
#             children: list[AstNode] =  node.children
#             for child in children:
#                 result = self.evaluate(child)
#                 if result:
#                     return True
#             return False
#         elif operator == 'not':
#             child: AstNode =  node.children[0]
#             if len(node.children) != 1:
#                 raise EvalError("'not' operator requires exactly one operand")
#             return not self.evaluate(child)
#         else:
#             raise EvalError(f"Unknown logical operator '{operator}'")
    
    
#     def eval_if_exp(self, node: AstNode):
#         condition: AstNode = node.children[0]
#         true_branch: AstNode = node.children[1]
#         false_branch: AstNode = node.children[2]
        
        
#         if(self.evaluate(condition)):
#             return self.evaluate(true_branch)
#         else:
#             return self.evaluate(false_branch)
    
#     def eval_print(self, node):
#         exp = self.evaluate(node.children[0])
#         if node.leaf == 'PRINT_NUM':
#             print(int(exp))
#         elif node.leaf == 'PRINT_BOOL':
#             print('#t' if exp else '#f')
#         else:
#             raise EvalError(f"Unknown print type '{node.leaf}'")
#         return None 
    
#     def eval_fun(self, node:AstNode):
#         # fun_ids: AstNode = node.children[0]
#         fun_ids: list  = node.children[0]
#         fun_body = node.children[1]
#         param_names = fun_ids
#         return Function(body=fun_body, param_names=param_names, env=self.current_env.copy())

#     def eval_fun_call(self, node:AstNode):
#         fun: Function = self.evaluate(node.children[0])
#         if not isinstance(fun, Function):
#             raise EvalError(f"'{fun}' is not a function")
#         args = [self.evaluate(arg) for arg in node.children[1:]]
        
#         if len(args) != len(fun.param_names):
#             raise EvalError(f"Function expected {len(fun.param_names)} arguments, got {len(args)}")
        
#         new_env = fun.env.copy()
#         for param, arg in zip(fun.param_names, args):
#             new_env[param] = arg
        
#         self.push_env(new_env)
#         try:
#             result = self.evaluate(fun.body)
#         finally:
#             self.pop_env()
#         return result
            
#     def eval_fun_body(self, node: AstNode):
#         result = None
#         for child in node.children:
#             result = self.evaluate(child)
#         return result
