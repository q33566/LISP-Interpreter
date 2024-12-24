from enum import Enum,  auto
from typing import Optional, List

class NodeType(Enum):
    PROGRAM = auto()
    STMT_LIST = auto()
    DEFINE = auto()
    FUN = auto()
    FUN_IDS = auto()
    FUN_CALL = auto()
    IF = auto()
    PRINT = auto()
    NUM_OP = auto()
    LOGICAL_OP = auto()
    VARIABLE = auto()
    NUMBER = auto()
    BOOL_VAL = auto()

class Node:
    def __init__(self, node_type: NodeType, children: list = [], leaf = None, type_info = None):
        self.node_type = node_type
        self.children = children
        self.leaf = leaf
        self.type_info = type_info
    
    def __repr__(self):
        return f"Node(node_type={self.node_type}, leaf={self.leaf}, children={self.children}, type_info={self.type_info})"
    