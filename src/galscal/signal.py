"""
Collects Signal class, representing signals Ae^(omega rt)
"""

import math
import numpy as np
from scipy.io.wavfile import write

import galscal

class Signal():
  """
  Class representing a signal of the form A e^(omega rt), for fixed positive
  real numbers A and r, and for fixed complex number omega.

  Attributes:
    Signal.log_amplitude : the real part of omega
    Signal.frequency : the imaginary part of omega
    Signal.abs_amp : A
    Signal.abs_logamp : log A
    Signal.abs_rate : r
    Signal.max_val : The maximum possible value that can be represented by a
      16-bit signed integer

  """
  def __init__(self, omega, absolute_amplitude=1., absolute_rate=1.):
    assert isinstance(omega, complex)
    self.root = omega

    self.log_amplitude = omega.real
    self.frequency = omega.imag/(2*np.pi)

    self.abs_amp = absolute_amplitude
    self.abs_logamp = np.log(self.abs_amp)
    self.abs_rate = absolute_rate

    self.max_val = np.iinfo(np.int16).max

  
  def eval_at(self, t):
    """
    Evaluate signal
    """
    arg = complex(
      self.abs_logamp + self.log_amplitude,
      2*np.pi*self.frequency * self.abs_rate * t,
    )
    output = np.exp(arg)

    return output


  def save_wav(self,
    save_path : str,
    time_interval : tuple[float, float],
    samples_per_second : int=44100,
  ) -> None:
    """
    Save the signal as a WAV file over a given time interval
    """
    start_time = time_interval[0]
    end_time =  time_interval[1]
    duration = end_time - start_time
    sample_count = math.floor(samples_per_second * duration)

    T = np.linspace(start_time, end_time, sample_count)

    signal_values_list = [self.eval_at(t) for t in T]
    signal_values = np.array(signal_values_list)
    # signal_values = self.eval_at(T)

    normed_values = signal_values / np.max(np.abs(signal_values))
    max_adjusted_values = normed_values * self.max_val
    
    values_to_write = np.int16(max_adjusted_values.real)
    write(save_path, samples_per_second, values_to_write)



class GalSignal(Signal):
  """
  Class representing a version of the same signal object represented by the
  class Signal, except that this version retains information about the underlying
  field extension in order to track Galois actions on the signal object.

  Attributes:
    GalSignal.element = element_poly
    GalSignal.field = field_ext_poly
    GalSignal.log_amplitude : the real part of omega
    GalSignal.frequency : the imaginary part of omega
    GalSignal.abs_amp : A
    GalSignal.abs_logamp : log A
    GalSignal.abs_rate : r
    GalSignal.max_val : The maximum possible value that can be represented by a
      16-bit signed integer

  """
  def __init__(self, 
    element_poly : galscal.Polynomial,
    field_ext_poly,
    absolute_amplitude=1.,
    absolute_rate=1.,
  ):
    self.min_arg_root = complex(field_ext_poly.min_arg_root())

    reduced_element_poly = element_poly.reduced_by(field_ext_poly)

    omega = reduced_element_poly.eval_at(self.min_arg_root)
    super().__init__(
      omega, 
      absolute_amplitude=absolute_amplitude, 
      absolute_rate=absolute_rate,
    )

    self.element = element_poly
    self.field = field_ext_poly