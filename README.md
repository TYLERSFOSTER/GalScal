# GalScal

*GalScal* is a Python package that lets users apply natural Galois actions on audio signals via Galois actions on number fields $K$, interpreted as subfields of complex frequency space $\mathbb{C}$.

## Description

*GalScal* provides a class `Signal` that represents an arbitrary complex-valued audio signal $f(t)$ of the form $$f(t)\ \ =\ \ A\ e^{\omega\ \!r\ \!t}$$ for fixed $A,r\in\mathbb{R}_{\ge0}$ and fixed $\omega\in\mathbb{C}$. *GalScal* also provides a class `Polynomial` that can be used to represent elements in finite degree extensions $K/\mathbb{Q}$. Every automorphism $\varphi\in\text{Aut}_{\mathbb{Q}}(K)$ can transform $$A\ e^{\omega\ \!r\ \!t}\ \ \longmapsto\ \ A\ e^{\varphi(\omega)\ \!r\ \!t}$$

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

## Installation

Steps to install your project:

```bash
git clone https://yourproject.git
cd yourproject
pip install -r requirements.txt
