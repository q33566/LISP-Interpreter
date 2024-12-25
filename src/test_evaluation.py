import pytest
from pathlib import Path
from utils.my_yacc import parse_input
test_case_input = list(Path('../public_test_data/in').iterdir())
@pytest.mark.parametrize("input_text, expected_output", [
    ("(+)", 'syntax error'),
])
def test_case_01_1(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    
    
@pytest.mark.parametrize("input_text, expected_output", [
    ("(+ (* 5 2) -)", 'syntax error'),
])
def test_case_01_2(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    
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
    ('''(print-num
  ((fun (a b) (+ a b)) 4 5))''', '9'),
])
def test_case_07_1(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    

@pytest.mark.parametrize("input_text, expected_output", [
    ('(define x 0)', ''),
    ('''(print-num
  ((fun (x y z) (+ x (* y z))) 10 20 30))''', '610'),
    ('(print-num x)', '0')
])
def test_case_07_2(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    
@pytest.mark.parametrize("input_text, expected_output", [
    ('''(define foo
  (fun (a b c) (+ a b (* b c))))''', ''),
    ('(print-num (foo 10 9 8))', '91')
])
def test_case_08_1(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    
@pytest.mark.parametrize("input_text, expected_output", [
    ('(define bar (fun (x) (+ x 1)))', ''),
    ('(define bar-z (fun () 2))', ''),
    ('(print-num (bar (bar-z)))', '3')
])
def test_case_08_1(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    
@pytest.mark.parametrize("input_text, expected_output", [
    ('''(define fact
  (fun (n) (if (< n 3) n
               (* n (fact (- n 1))))))''', ''),
    ('(print-num (fact 2))', '2'),
    ('(print-num (fact 3))', '6'),
    ('(print-num (fact 4))', '24'),
    ('(print-num (fact 10))', '3628800'),
    ('''(define fib (fun (x)
  (if (< x 2) x (+
                 (fib (- x 1))
                 (fib (- x 2))))))''', ''),
    ('(print-num (fib 1))', '1'),
    ('(print-num (fib 3))', '2'),
    ('(print-num (fib 5))', '5'),
    ('(print-num (fib 10))', '55'),
    ('(print-num (fib 20))', '6765'),
])
def test_case_b1_1(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    
@pytest.mark.parametrize("input_text, expected_output", [
    ('''(define min
  (fun (a b)
    (if (< a b) a b)))''', ''),
    ('''(define max
  (fun (a b)
    (if (> a b) a b)))''', ''),
    ('''(define gcd
  (fun (a b)
    (if (= 0 (mod (max a b) (min a b)))
        (min a b)
        (gcd (min a b) (mod (max a b) (min a b))))))''', ''),
    ('(print-num (gcd 100 88))', '4'),
    ('(print-num (gcd 1234 5678))', '2'),
    ('(print-num (gcd 81 54))', '27'),
])
def test_case_b1_2(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    
@pytest.mark.parametrize("input_text, expected_output", [
    ('(+ 1 2 3 (or #t #f))', 'Type error!'),
])
def test_case_b2_1(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    

@pytest.mark.parametrize("input_text, expected_output", [
    ('(+ 1 2 3 (or #t #f))', 'Type error!'),
])
def test_case_b2_1(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    
@pytest.mark.parametrize("input_text, expected_output", [
    ('''(define f
  (fun (x)
    (if (> x 10) 10 (= x 5))))''', ''),
    ('(print-num (* 2 (f 4)))', 'Type error!'),
])
def test_case_b2_2(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    
@pytest.mark.parametrize("input_text, expected_output", [
    ('''(define dist-square
  (fun (x y)
    (define square (fun (x) (* x x)))
    (+ (square x) (square y))))''', ''),
    ('(print-num (dist-square 3 4))', '25'),
])
def test_case_b3_1(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    

@pytest.mark.parametrize("input_text, expected_output", [
    ('''(define diff
  (fun (a b)
    (define abs
      (fun (a)
        (if (< a 0) (- 0 a) a)))
    (abs (- a b))))''', ''),
    ('(print-num (diff 1 10))', '9'),
    ('(print-num (diff 10 2))', '8'),
])
def test_case_b3_2(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    
@pytest.mark.parametrize("input_text, expected_output", [
    ('''(define add-x
  (fun (x) (fun (y) (+ x y))))''', ''),
    ('(define z (add-x 10))', ''),
    ('(print-num (z 1))', '11'),
])
def test_case_b4_1(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"
    
@pytest.mark.parametrize("input_text, expected_output", [
    ('''(define foo
  (fun (f x) (f x)))''', ''),
    ('''(print-num
  (foo (fun (x) (- x 1)) 10))''', '9'),
])
def test_case_b4_2(input_text, expected_output, capsys):
    parse_input(input_text)
    captured = capsys.readouterr()
    assert captured.out.strip() == str(expected_output), f"Expected printed output {expected_output}, but got {captured.out.strip()}"