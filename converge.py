#!/usr/bin/env python3
"""thick/thin inside discs of growing radius (grid units) for 3 Penrose gammas; deviation from the golden ratio."""
import math
from pentagrid import tiling
phi = (1+5**.5)/2
G = [[0.11, 0.23, -0.07, 0.31, -0.58], [0.37, -0.12, 0.05, -0.41, 0.11], [0.2, 0.2, 0.2, 0.2, 0.2]]
print("R  " + "  ".join(f"g{i}: thick/thin  |dev|" for i in range(len(G))))
T = [tiling(64, g)[0] for g in G]
for R in (4, 8, 16, 32):
    row = []
    for tiles in T:
        inn = [t for t in tiles if math.hypot(*t[2]) < R]
        a = sum(t[0] == 'thick' for t in inn); b = len(inn) - a
        row.append(f"{a:5d}/{b:5d}={a/b:.4f} {abs(a/b-phi):.4f}")
    print(f"{R:2d} " + "  ".join(row))
print(f"golden ratio {phi:.4f}")
