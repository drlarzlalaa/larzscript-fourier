#!/usr/bin/env python3
"""Independent Python reference for fourier.lz (provenance and cross-check).

A deliberately naive O(N^2) DFT using math.sin / math.cos (fourier.lz uses an FFT and its own series).

    python3 tools/reference.py spectrum 64 sin:5:1,sin:12:0.5,dc:0.25
    python3 tools/reference.py leakage 64 5.5
    python3 tools/reference.py parseval 64 1
"""
import math, sys

M, MUL = 2147483647, 48271

def dft(x):
    n = len(x)
    out = []
    for k in range(n):
        re = sum(x[t] * math.cos(2 * math.pi * k * t / n) for t in range(n))
        im = -sum(x[t] * math.sin(2 * math.pi * k * t / n) for t in range(n))
        out.append((re, im))
    return out

def wave(n, spec):
    x = [0.0] * n
    for part in spec.split(","):
        f = part.split(":")
        if f[0] == "dc":
            for t in range(n): x[t] += float(f[1])
        else:
            amp = float(f[2]); ph = math.radians(float(f[3])) if len(f) > 3 else 0.0
            for t in range(n): x[t] += amp * math.sin(2 * math.pi * float(f[1]) * t / n + ph)
    return x

def spectrum(n, spec):
    X = dft(wave(n, spec))
    for k in range(n // 2 + 1):
        mag = math.hypot(*X[k]) / n * (1 if k in (0, n // 2) else 2)
        if mag >= 0.001: print(k, "%.6g" % mag)

def leakage(n, freq):
    x = [math.sin(2 * math.pi * freq * t / n) for t in range(n)]
    hann = [0.5 - 0.5 * math.cos(2 * math.pi * t / n) for t in range(n)]
    Xr = dft(x); Xh = dft([a * b for a, b in zip(x, hann)])
    for k in range(int(freq) - 2, int(freq) + 4):
        print(k, "%.4f %.4f" % (2 * math.hypot(*Xr[k]) / n, 2 * math.hypot(*Xh[k]) / sum(hann)))

def parseval(n, seed):
    s = seed % M or 1; x = []
    for _ in range(n):
        s = (MUL * s) % M; x.append(s / M - 0.5)
    X = dft(x)
    left = sum(v * v for v in x); right = sum(a * a + b * b for a, b in X) / n
    print("%.6g %.6g %.3g" % (left, right, abs(left - right) / left))

if __name__ == "__main__":
    c = sys.argv[1]
    if c == "spectrum": spectrum(int(sys.argv[2]), sys.argv[3])
    elif c == "leakage": leakage(int(sys.argv[2]), float(sys.argv[3]))
    else: parseval(int(sys.argv[2]), int(sys.argv[3]))
