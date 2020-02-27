#!/bin/bash
thisdir=$(pwd)
echo $thisdir
cd ../../
tikzdir=$(pwd)
echo $tikzdir
./package.sh
cd $thisdir
python3 $tikzdir/tikzcrystal.py input.in

