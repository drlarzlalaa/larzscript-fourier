#!/bin/sh
# A tone halfway between bins reads about 0.64 with a rectangular window (theory: 3.9 dB scalloping loss)
# and about 0.85 with a Hann window (1.4 dB).
$LZ leakage
$LZ leakage --n=128 --freq=10.5
