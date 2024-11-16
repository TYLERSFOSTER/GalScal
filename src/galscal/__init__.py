"""
Package initialization for galscal.

This Python package lets users apply natural Galois actions
on audio signals via Galois actions on number fields,
interpreted as subfields of complex frequency space.

Author: Tyler Foster
Email: tylerisnotavailable@gmail.com
License: MIT License
"""

from .field import Polynomial
from .signal import Signal, GalSignal

__all__ = ['Polynomial', 'Signal', 'GalSignal']
