tanglenum
=========

[![License:MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This Python program is used to enumerate planar Tangles as described
in the paper [Enumeration of planar
Tangles](https://arxiv.org/abs/1906.01541) by Douglas A. Torrance.


Requirements
------------
* [NetworkX](https://networkx.github.io/)


Usage
-----
To generate lists of the dual graphs of all fixed, one-sided, and free
Tangles of size up to *P*, run

    import tanglenum
    tanglenum.generate_tangles(P)

Files
-----

* `enumeration_of_planar_tangles.py` - Script which generates the
  numbers used in the paper
* `enumeration_of_planar_tangles.txt` - Output of the above script
* `tanglenum.py` - Main algorithm
