"""
Classes for representing a finiely generated number field  
"""
from __future__ import annotations

import cmath
import numpy as np
import copy

import galscal

class Polynomial():
  """
  Class representing a polynomial as a formal object suitable
  for Galois-theoretic usage

  Important: Within the galscal package, this class represents both a formal
  polynomial, and the polynomial representing an element in a field extension.
  The methods `reduces` and `reduce_by` are examples of the latter.

  Attributes:
    Polynomial.coeffs : row vector of coefficients encoding the polynomial
  """
  def __init__(self, coeffs : np.ndarray):
    assert isinstance(coeffs, np.ndarray)
    assert len(coeffs.shape) == 1
    assert coeffs[-1] != 0

    self.degree = coeffs.shape[0] - 1
    self.deg = self.degree

    self.coefficient_vector = coeffs
    self.coeff_vec = self.coefficient_vector
    self.leading_coeffient = self.coeff_vec[-1]

    self.reducing_vector = - self.coefficient_vector[:-1]/self.leading_coeffient

    self.superscript_dict = {
      '0' : '\u2070',
      '1' : '\u2071',
      '2' : '\u00B2',
      '3' : '\u00B3',
      '4' : '\u2074',
      '5' : '\u2075',
      '6' : '\u2076',
      '7' : '\u2077',
      '8' : '\u2078',
      '9' : '\u2079',
    }


  def coeff(self, n : int) -> float:
    """
    Return the coefficient of the degree n term of the polynomial

    Args:
      n : the degree of the term to return coefficient from
    """
    assert isinstance(n, int)

    if n < 0 or n > self.degree:
      coefficient = 0.0
    else:
      coefficient = self.coeff_vec[n]

    return coefficient


  def eval_at(self, x : np.ndarray) -> np.ndarray:
    """
    Evaluate the polynomail at point x

    Args:
      x : an np.ndarray
    """
    power_vec = [x**n for n in range(self.deg + 1)]
    power_vec = np.array(power_vec)

    value = np.dot(self.coeff_vec, power_vec)

    return value
  

  def formal(self, var_symb : str='\U0001D44B') -> None:
    """
    Print the formal polynomial as a string

    Args:
      var_symb : the string to use for polynomial variable when printing
    """
    poly_str = ''
    for k, c in enumerate(self.coeff_vec):
      c = str(c)

      if k == 0:
        char = ''
      elif k == 1:
        char = ' ' + var_symb
      elif k > 1:
        numerals = str(k).split()
        
        exponent = ''
        for entry in numerals:
          exponent += self.superscript_dict[entry]
        char = ' ' + var_symb + exponent
     
      monomial = c + char

      if k == 0:
        poly_str += monomial
      elif k > 0:
        poly_str += ' + ' + monomial

    return poly_str

  
  def reduces(self, polynomial : Polynomial):
    """
    Use the polynomial `self` to reduce a second polynomial

    Args:
      polynomial : a second instance of the galscal.Polynomial class
    """
    assert isinstance(polynomial, Polynomial)

    output_vec = copy.deepcopy(polynomial.coeff_vec)
    deg_to_reduce = copy.deepcopy(polynomial.deg)

    if deg_to_reduce < self.deg:
      output_polynomial = polynomial
    else:
      while deg_to_reduce >= self.deg:
        reducing_term = np.zeros_like(output_vec)
        reducing_term[deg_to_reduce - (self.deg): deg_to_reduce] = self.reducing_vector
        reducing_term = output_vec[deg_to_reduce] * reducing_term

        output_vec += reducing_term
        output_vec[deg_to_reduce] = 0.

        deg_to_reduce -= 1

      output_vec = output_vec[0 : deg_to_reduce + 1]
      output_polynomial = Polynomial(output_vec)

    return output_polynomial
  

  def reduced_by(self, polynomial):
    """
    Use a second polynomial to reduce the polynomial `self`

    Important: This method reverses the roles of `self` and the second polynomial
    in the method `reduces`
    """
    assert isinstance(polynomial, galscal.Polynomial)

    output_polynomial = polynomial.reduces(self)
  
    return output_polynomial
  

  def roots(self):
    """
    Return the roots of the polynomial
    """
    coefficients = np.flip(self.coeff_vec)
    output = np.roots(coefficients)
    output = [complex(entry) for entry in output]

    return output
  

  def min_arg_root(self):
    poly_roots = self.roots()

    complex_args = []
    arg_dict = {}
    for elem in poly_roots:
      elem_arg = cmath.phase(complex(elem))
      elem_arg = elem_arg%(2*np.pi)

      complex_args.append(elem_arg)
      arg_dict.update({elem_arg : elem})
    
    min_arg = min(complex_args)

    output = arg_dict[min_arg]

    return output
  

  def act_by(self, matrix : np.ndarray) -> None:
    """
    Givne a square matrix G, transform Polynomial(P) to Polynomial(G(P))
    """
    assert isinstance(matrix, np.ndarray)
    assert matrix.shape == (self.deg + 1, self.deg + 1)
    
    new_coeff_vec = np.dot(matrix, self.coeff_vec)
    self.__init__(new_coeff_vec)
