#!/usr/bin/env python3
"""Can the statistical checks tell a Penrose tiling from a non-Penrose (generalized, sum gamma not integer) one?
Thick/thin within radius 32 and the index-class counts, for sum gamma = 0 (Penrose) and 0.3, 0.5 (not Penrose)."""
import math, collections
from pentagrid import tiling
phi = (1+5**.5)/2
base = [0.11, 0.23, -0.07, 0.31]
for s in (0.0, 0.3, 0.5):
    g = base + [s - sum(base)]
    tiles, e = tiling(64, g)
    inn = [t for t in tiles if math.hypot(*t[2]) < 32]
    a = sum(t[0] == 'thick' for t in inn); b = len(inn) - a
    V = {k for _, c, z in tiles if math.hypot(*z) < 32 for k in c}
    c = collections.Counter(sum(k) for k in V)
    print(f"sum={s:.1f} thick/thin {a}/{b}={a/b:.4f} (phi {phi:.4f})  index classes {dict(sorted(c.items()))}")
