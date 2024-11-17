import numpy as np

import galscal


class Transform():
  def __init__(self, matrix, field_poly):
    self.field_poly = field_poly

    assert isinstance(field_poly, galscal.Polynomial)
    self.dimension = field_poly.degree + 1
    self.dim = self.dimension

    assert isinstance(matrix, np.ndarray)
    assert matrix.shape == (self.dim, self.dim)
    self.matrix = matrix


  def on_elem(self, element_poly):
    """
    [...]
    """
    assert isinstance(element_poly, galscal.Polynomial)

    element_poly = element_poly.reduced_by(self.field_poly)

    element_vec = element_poly.coeff_vec
    pad_width = self.dim - len(element_vec)
    element_vec = np.pad(element_vec,
                         (0, pad_width),
                         'constant',
                         constant_values=(0.),
                         )
    
    transformed_vec = np.dot(self.matrix, element_vec)
    transformed_coefficients = np.trim_zeros(transformed_vec, 'b')
    transformed_poly = galscal.Polynomial(transformed_coefficients)

    return transformed_poly
  

  def on_galsig(self, galois_signal):
    """
    [...]
    """
    assert isinstance(galois_signal, galscal.GalSignal)
    signal_field_poly = galois_signal.field_poly
    signal_vec = signal_field_poly.coeff_vec
    transform_vec = self.field_poly.coeff_vec
    assert np.array_equal(signal_vec, transform_vec)

    signal_poly = galois_signal.element
    transformed_poly = self.on_elem(signal_poly)

    output_galois_signal = galscal.GalSignal(transformed_poly, self.field_poly)

    return output_galois_signal