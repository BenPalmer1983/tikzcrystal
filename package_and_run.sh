#!/bin/bash
python3 pack/pack.py tikzcrystal.py
cd example && python3 ../tikzcrystal.py input.in

