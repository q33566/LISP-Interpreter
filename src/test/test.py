import pytest
from pathlib import Path
from utils.my_yacc import parse_input
from utils.my_visitor import Visitor

INPUT_DIR = Path('../../public_test_data/in')
OUTPUT_DIR = Path('../../public_test_data/out')

test_case_inputs: list[Path] = sorted(INPUT_DIR.glob('*'))
test_case_outputs: list[Path] = sorted(OUTPUT_DIR.glob('*'))

test_cases = [(test_case_in.read_text(encoding='utf-8'), test_case_out.read_text(encoding='utf-8')) 
              for test_case_in, test_case_out in zip(test_case_inputs, test_case_outputs)]

@pytest.mark.parametrize("input_text, expected_output", test_cases)
def test_my_test(input_text, expected_output, capsys):
    parse_input(input_text, visitor=Visitor())
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"