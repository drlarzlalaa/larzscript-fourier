#!/bin/sh
$LZ spectrum --n=100
$LZ spectrum --n=2048
$LZ spectrum --n=abc
$LZ spectrum --wave=sin:40:1
$LZ spectrum --wave=sin:0:1
$LZ spectrum --wave=triangle:5:1
$LZ spectrum --wave=sin:5
$LZ spectrum --wave=dc
$LZ spectrum --wave=sin:x:1
$LZ leakage --freq=2
$LZ leakage --freq=31
$LZ parseval --n=1
