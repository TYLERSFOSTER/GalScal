import numpy as np
import pytest


import galscal







@pytest.mark.parametrize("omega, answer", [
    (complex(1., 0.), 1.),
])
def test_Transform(omega, answer):
  pass