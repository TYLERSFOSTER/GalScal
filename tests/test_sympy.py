import sympy
import pytest



X = sympy.symbols('X')



def is_prime(n):
    """
    Check if a number is prime.
    """
    if n <= 1:
        return False

    # Iterate from 2 to the square root of n
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False

    return True



@pytest.mark.parametrize("polynomial, answer",[
    (X**6 - 1, [X - 1, X + 1, X**2 - X + 1, X**2 + X + 1]),
    (X**5 - 1, [X - 1, X**4 + X**3 + X**2 + X + 1]),
    (X**2 + 2*X + 1, [(X + 1)**2]),
])
def test_sympy_factor(polynomial, answer):
  factored_expression = sympy.factor(polynomial)
  factored_expression = factored_expression.as_ordered_factors(order=None)

  assert factored_expression == answer



@pytest.mark.parametrize("polynomial, prime, answer",[
  (X**6 - 1, 2, [(X + 1)**2, (X**2 + X + 1)**2]),
  (X**6 - 1, 3, [(X - 1)**3, (X + 1)**3]),
  (X**6 - 1, 5, [X - 1, X + 1, X**2 - X + 1, X**2 + X + 1]),
  (X**6 - 1, 7, [X - 3, X - 2, X - 1, X + 1, X + 2, X + 3]),
  (X**6 - 1, 11, [X - 1, X + 1, X**2 - X + 1, X**2 + X + 1]),
  (X**6 - 1, 13, [X - 4, X - 3, X - 1, X + 1, X + 3, X + 4]),
  (X**6 - 1, 17, [X - 1, X + 1, X**2 - X + 1, X**2 + X + 1]),
  (X**6 - 1, 19, [X - 8, X - 7, X - 1, X + 1, X + 7, X + 8]),
  (X**6 - 1, 23, [X - 1, X + 1, X**2 - X + 1, X**2 + X + 1]),
  (X**6 - 1, 29, [X - 1, X + 1, X**2 - X + 1, X**2 + X + 1]),
])
def test_sympy_factor_modulus(polynomial, prime, answer):
  factored_expression = sympy.factor(polynomial, modulus=prime)
  factored_expression = factored_expression.as_ordered_factors(order=None)

  assert factored_expression == answer



def test_sympy_factor_modulus_B():
  for p in range(5, 1000):
    if is_prime(p):
      factored_expression = sympy.factor(X**6 - 1, modulus=p)
      factored_expression = factored_expression.as_ordered_factors(order=None)

      if (p-1)%6 == 0:
        assert len(factored_expression) == 6
      else:
         assert len(factored_expression) != 6


  
