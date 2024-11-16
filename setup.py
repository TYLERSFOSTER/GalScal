from setuptools import setup, find_packages

setup(
    name="GalScal",
    version="0.1.0",
    author="Tyler Foster",
    author_email="tylerisnotavailable@gmail.com",
    description="Musical scales with Galois actions.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="http://github.com//TYLERSFOSTERe/galscal",
    package_dir={'': 'src'},  # tells distutils packages are under src
    packages=find_packages(where='src'),  # include all packages under src
    install_requires=[
      'numpy>=1.25.1',
      'pytest>=8.3.3',
      'scipy>=1.14.1',
      'setuptools>=68.0.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
