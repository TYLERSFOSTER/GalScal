import numpy as np
import pytest

import galscal

@pytest.mark.parametrize("omega, answer", [
    (complex(1., 0.), 1.),
])
def test_Signal(omega, answer):
  signal = galscal.Signal(omega)

  assert signal.root == omega


@pytest.mark.parametrize("element_vec, field_vec, answer", [
    (np.array([1., 1., 1., 1.]), np.array([1., 0., 0., 0., 1.]), 1.),
])
def test_GalSignal(element_vec, field_vec, answer):
  element_poly = galscal.Polynomial(element_vec)
  field_poly = galscal.Polynomial(field_vec)


  alpha = complex(field_poly.roots()[0])
  print('ALPHA:', alpha)
  assert isinstance(alpha, complex)
  omega = element_poly.eval_at(alpha)
  print(omega)

  signal = galscal.GalSignal(element_poly, field_poly)

  assert True