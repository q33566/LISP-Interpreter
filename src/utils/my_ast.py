from enum import Enum,  auto
from typing import Optional, List
from utils.my_eval import Visitor

class NodeType(Enum):
    PROGRAM = auto()
    STMT_LIST = auto()
    DEFINE = auto()
    FUN = auto()
    FUN_IDS = auto()
    FUN_CALL = auto()
    IF_EXP = auto()
    PRINT = auto()
    NUM_OP = auto()
    LOGICAL_OP = auto()
    VARIABLE = auto()
    NUMBER = auto()
    BOOL_VAL = auto()
    FUN_BODY = auto()
