#!/usr/bin/env python3
"""Distinct vertices by index sum(K) inside a disc. Window theory: index classes project to pentagons of side 1 and phi
(small for the outer two classes, large for the inner two), so count(outer)/count(inner) -> 1/phi^2 = 0.3820."""
import math, collections
from pentagrid import tiling, pos
phi = (1+5**.5)/2
for g in ([0.11, 0.23, -0.07, 0.31, -0.58], [0.37, -0.12, 0.05, -0.41, 0.11]):
    tiles, e = tiling(64, g)
    V = {k for _, c, z in tiles if math.hypot(*z) < 32 for k in c}
    c = collections.Counter(sum(k) for k in V); ks = sorted(c)
    print(g, dict(sorted(c.items())), "outer/inner = %.4f/%.4f" % (c[ks[0]]/c[ks[1]], c[ks[3]]/c[ks[2]]), "theory %.4f" % (1/phi**2))
