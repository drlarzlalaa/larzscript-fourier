# larzscript-fourier

The fast Fourier transform, and what it can and cannot tell you about a signal, written entirely in [Larzscript](https://github.com/larz-scripter/larzscript). `fourier.lz` is one file. Any signal of N samples is a sum of sine waves; the Fourier transform finds how much of each frequency is present. It is behind audio equalisers, radio, image compression and vibration analysis, and the FFT is the trick that made it cheap enough to use everywhere.

```
$ larzscript fourier.lz spectrum
64 samples
| Bin | Frequency (cycles per window) | Amplitude |
|-----|-------------------------------|-----------|
| 0   | 0                             | 0.25      |
| 5   | 5                             | 1         |
| 12  | 12                            | 0.5       |

$ larzscript fourier.lz leakage
64 samples of a sine of amplitude 1 at 5.5 cycles per window
| Bin | Rectangular window | Hann window |
|-----|--------------------|-------------|
| 3   | 0.1619             | 0.02478     |
| 4   | 0.2429             | 0.1701      |
| 5   | 0.6641             | 0.8486      |
| 6   | 0.6118             | 0.849       |
| 7   | 0.1896             | 0.1696      |
| 8   | 0.1067             | 0.02412     |

$ larzscript fourier.lz compare
64 samples
largest difference between the FFT and the DFT: < 1e-12 (rounding error)
| Method                    | Complex multiplications |
|---------------------------|-------------------------|
| DFT (from the definition) | 4096                    |
| FFT (radix-2)             | 192                     |

The FFT does 21 times fewer multiplications at this size, and the gap widens as N grows.
```

- **`spectrum`** builds a signal from components you describe (`sin:FREQ:AMPLITUDE[:PHASE]`, `dc:LEVEL`) and reads them back. A tone that fits a whole number of cycles in the window appears in exactly one bin at its true amplitude; the DC offset is bin 0. (Bin numbers are cycles per window: with N samples taken over T seconds, bin k is k/T Hz.)
- **`leakage`** is the practical lesson. A tone that does *not* fit a whole number of cycles (here 5.5) has no bin of its own, so its energy smears across many, and every reading is too small - about 0.64 instead of 1 with the plain (rectangular) window, the well-known "scalloping loss" of 3.9 dB for a tone halfway between bins. A **Hann window** tapers the ends of the sample and gives 0.849 in both neighbouring bins (a loss of only 1.4 dB) with far less smearing into distant bins (0.025 at bin 3 instead of 0.16), at the cost of a broader peak.
- **`parseval`** checks Parseval's theorem: total energy is the same computed from the samples or from the spectrum (5.20593 both ways).
- **`compare`** shows why the FFT matters: the same answer as the textbook DFT for 21 times fewer multiplications at N = 64, and 64 times fewer at N = 256.

## Does it check out?

- **The program is right.** `tools/reference.py` is an independent Python implementation using a naive O(N^2) DFT and `math.sin` / `math.cos` (Larzscript has no trigonometry built in, so `fourier.lz` writes its own `sin` and `cos` as series and uses an FFT). Every spectrum, all the leakage columns for two window sizes and two tone frequencies, and the Parseval energies matched it before the tests were written.
- **The theory is honoured.** Parseval's theorem holds to rounding error (about 1e-15 relative); the FFT and the DFT agree to rounding error; the rectangular and Hann readings for a half-bin tone average 0.64 and 0.85, as scalloping-loss theory predicts. Differences between two neighbouring bins (0.6641 and 0.6118 here) are real: the tone's mirror image at negative frequency interferes with it, and the effect shrinks the farther the tone sits from zero frequency: the two readings differ by 0.052 for a tone at bin 5.5 but by only 0.028 for one at bin 10.5 (`leakage --n=128 --freq=10.5`), and changing the window length alone does not remove it.

## Install

You need the [Larzscript](https://github.com/larz-scripter/larzscript) interpreter and the `cli`, `args` and `table` packages:

```
curl -fsSL https://raw.githubusercontent.com/larz-scripter/larzscript/main/install.sh | sh
larzscript pkg install cli
larzscript pkg install args
larzscript pkg install table
```

## Commands

| Command | What it does |
|---|---|
| `spectrum [--n=64] [--wave=sin:5:1,sin:12:0.5,dc:0.25]` | The amplitude at each frequency bin of a signal you describe (bins with at least 0.001 shown). |
| `leakage [--n=64] [--freq=5.5]` | A sine between bins, read with a rectangular and a Hann window. |
| `parseval [--n=64] [--seed=1]` | Energy in time against energy in frequency for seeded random samples. |
| `compare [--n=64]` | The DFT and FFT results and their multiplication counts. |

`--n` must be a power of two from 2 to 1024. Frequencies must be below N/2 (the Nyquist limit); a real tone above it would alias, appearing at a false lower frequency.

## Limits

- **Synthetic signals only.** There is no file or audio input; you describe the signal on the command line.
- **Power-of-two sizes.** The FFT is a plain radix-2 one; other lengths would need zero-padding or a different algorithm.
- **Amplitude only.** Phase is not reported, and only the positive-frequency half of the spectrum is shown (the other half mirrors it for real signals).
- **Windowing is a trade-off,** not a fix: a window reduces leakage but widens every peak and slightly changes amplitudes; the Hann figures here are normalised by the window's average.
- **Small values are hidden.** Bins under 0.001 are not printed, which also hides the rounding noise (around 1e-16) in bins that are exactly zero.

## Tests

```
sh tests/run_tests.sh
```

Set `LZ="larzscript /path/to/fourier.lz"` to test another copy. CI runs the same suite on every push.

## Licence

MIT (`LICENSE`).
