import pytest
from pathlib import Path
from my_yacc import parse_input
test_case_input = list(Path('../public_test_data/in').iterdir())

def test_case_01_1():
    result = parse_input(test_case_input[0].read_text())
    assert result == 'syntax error'
    
def test_case_01_2():
    result = parse_input(test_case_input[1].read_text())
    assert result == 'syntax error'
    
@pytest.mark.parametrize("input_text, expected_output", [
    ("(print-num 1)", 1),
    ("(print-num 2)", 2),
    ("(print-num 3)", 3),
    ("(print-num 4)", 4),
])
def test_case_02_1(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    
@pytest.mark.parametrize("input_text, expected_output", [
    ("(print-num 0)", 0),
    ("(print-num -123)", -123),
    ("(print-num 456)", 456),
])
def test_case_02_2(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    
@pytest.mark.parametrize("input_text, expected_output", [
    ("(+ 1 2 3)", ""),
    ("(* 4 5 6)", ""),
    ("(print-num (+ 1 (+ 2 3 4) (* 4 5 6) (/ 8 3) (mod 10 3)))", 133),
    ("(print-num (mod 10 4))", 2),
    ("(print-num (- (+ 1 2) 4))", -1),
    ("(print-num -256)", -256),
])
def test_case_03_1(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    
@pytest.mark.parametrize("input_text, expected_output", [
    ("(print-num (mod 10 (+ 1 2)))", 1),
    ("(print-num (* (/ 1 2) 4))", 0),
    ("""
    (print-num (- (+ 1 2 3 (- 4 5) 6 (/ 7 8) (mod 9 10))
                  11))
    """, 9),
])
def test_case_03_2(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    
    
@pytest.mark.parametrize("input_text, expected_output", [
    ("(print-bool #t)", '#t'),
    ("(print-bool #f)", '#f'),
    ("(print-bool (and #t #f))", '#f'),
    ("(print-bool (and #t #t))", '#t'),
    ("(print-bool (or #t #f))", '#t'),
    ("(print-bool (or #f #f))", '#f'),
    ("(print-bool (not #t))", '#f'),
    ("(print-bool (not #f))", '#t'),
])
def test_case_04_1(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    
@pytest.mark.parametrize("input_text, expected_output", [
    ("(print-bool (or #t #t #f))", '#t'),
    ("(print-bool (or #f (and #f #t) (not #f)))", '#t'),
    ("(print-bool (and #t (not #f) (or #f #t) (and #t (not #t))))", '#f'),
])
def test_case_04_2(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    
    
@pytest.mark.parametrize("input_text, expected_output", [
    ("(print-num (if #t 1 2))", '1'),
    ("(print-num (if #f 1 2))", '2'),
])
def test_case_05_1(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    
    
@pytest.mark.parametrize("input_text, expected_output", [
    ("(print-num (if (< 1 2) (+ 1 2 3) (* 1 2 3 4 5)))", '6'),
    ('''(print-num (if (= 9 (* 2 5))
               0
               (if #t 1 2)))''', '1'),
])
def test_case_05_2(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    
    
@pytest.mark.parametrize("input_text, expected_output", [
    ('(define x 1)', ''),
    ('(print-num x)', '1'),
    ('(define y (+ 1 2 3))', ''),
    ('(print-num y)', '6'),
])
def test_case_06_1(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    
    
@pytest.mark.parametrize("input_text, expected_output", [
    ('(define a (* 1 2 3 4))', ''),
    ('(define b (+ 10 -5 -2 -1))', ''),
    ('(print-num (+ a b))', '26'),
])
def test_case_06_2(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    
@pytest.mark.parametrize("input_text, expected_output", [
    ('''(print-num
  ((fun (x) (+ x 1)) 3))''', '4'),
#     ('''(print-num
#   ((fun (a b) (+ a b)) 4 5))''', '9'),
])
def test_case_07_1(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"