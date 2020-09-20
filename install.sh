#!/bin/sh
python3 setup.py sdist
pip3 install --user dist/lattice2d-1.0.0.tar.gz