import pytest
from pathlib import Path
from parser import parse_input
test_case_input = list(Path('../public_test_data').iterdir())

def test_case_0():
    result = parse_input(test_case_input[0].read_text())
    assert result == 'syntax error'