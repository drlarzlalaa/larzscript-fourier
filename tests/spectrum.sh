#!/bin/sh
# Whole-cycle tones land in exactly one bin, at their true amplitude; dc is bin 0.
$LZ spectrum
$LZ spectrum --n=128 --wave=sin:9:0.75:90,dc:-0.5
$LZ spectrum --n=32 --wave=sin:3:2
