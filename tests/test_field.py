import numpy as np
import pytest

import galscal


@pytest.mark.parametrize("vec_1, vec_2, answer", [
    ([1., 2., 4.], [0.0, 1., 2., -2., 2.], '-0.75 + 0.25 \U0001D44B'),
    ([1., 1., 2.], [0., -.5, 1.], '-0.5 + -1.0 \U0001D44B'),
    ([1., 0., 0., 0., 2.], [0., -.5, 1., 1., 1., 1., 1., ], '-0.5 + -1.0 \U0001D44B + 0.5 \U0001D44B\u00B2 + 1.0 \U0001D44B\u00B3'),
])
def test_reduces(vec_1, vec_2, answer):
  poly_1 = galscal.Polynomial(np.array(vec_1))
  poly_2 = galscal.Polynomial(np.array(vec_2))

  reduced_poly = poly_1.reduces(poly_2).formal()
  
  assert reduced_poly == answer



@pytest.mark.parametrize("vec_1, vec_2", [
    ([1., 2., 4.], [0.0, 1., 2., -2., 2.]),
    ([1., 1., 2.], [0., -.5, 1.]),
    ([1., 0., 0., 0., 2.], [0., -.5, 1., 1., 1., 1., 1., ]),
])
def test_reduced_by(vec_1, vec_2):
  poly_1 = galscal.Polynomial(np.array(vec_1))
  poly_2 = galscal.Polynomial(np.array(vec_2))

  reduced_poly_A = poly_1.reduces(poly_2).formal()
  reduce_poly_B = poly_2.reduced_by(poly_1).formal()

  assert reduced_poly_A == reduce_poly_B



@pytest.mark.parametrize("vec_1, answer", [
    ([1., 0., 1.], [complex(0., 1.), complex(0., -1.)]),
    ([-4., 0., 1.], [complex(2., 0.), complex(-2., 0.)]),
    ([2., -2., 1.], [complex(1., 1.), complex(1., -1.)]),
    ([-1., 0., 0., 0., 1.], [complex(1., 0.), complex(0., 1.), complex(-1., 0.), complex(0., -1.)]),
])
def test_roots(vec_1, answer):
  poly_1 = galscal.Polynomial(np.array(vec_1))

  poly_roots = poly_1.roots()
  poly_roots = [round(num.real, 2) + round(num.imag, 2) * 1j for num in poly_roots]

  assert set(poly_roots) == set(answer)

