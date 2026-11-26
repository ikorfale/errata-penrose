#!/usr/bin/env python3
"""Penrose rhombus tilings from de Bruijn's pentagrid, with exact checks.
Every pair of grid lines from families r<s meets once -> one rhombus whose corners are integer 5-vectors K;
a corner's position is sum_j K_j e_j. Checks: (1) each interior edge is shared by exactly two rhombi,
(2) vertex index sum(K) takes exactly 4 values when sum(gamma)=0 (Penrose) and 5 otherwise,
(3) thick/thin -> golden ratio. Usage: pentagrid.py N gamma0..gamma4"""
import math, sys, json, collections
def tiling(N, gam):
    e = [(math.cos(2*math.pi*j/5), math.sin(2*math.pi*j/5)) for j in range(5)]
    tiles = []
    for r in range(5):
        for s in range(r+1, 5):
            det = e[r][0]*e[s][1] - e[r][1]*e[s][0]
            for kr in range(-N, N+1):
                for ks in range(-N, N+1):
                    a, b = kr - gam[r], ks - gam[s]
                    z = ((a*e[s][1] - b*e[r][1])/det, (b*e[r][0] - a*e[s][0])/det)
                    K = [math.floor(z[0]*e[j][0] + z[1]*e[j][1] + gam[j]) for j in range(5)]
                    corners = []
                    for dr, ds in ((-1, -1), (0, -1), (0, 0), (-1, 0)):
                        k = K[:]; k[r] = kr + dr; k[s] = ks + ds; corners.append(tuple(k))
                    kind = 'thick' if (s - r) in (1, 4) else 'thin'
                    tiles.append((kind, corners, z))
    return tiles, e
def pos(k, e): return (sum(k[j]*e[j][0] for j in range(5)), sum(k[j]*e[j][1] for j in range(5)))
def checks(N, gam, R=None):
    tiles, e = tiling(N, gam)
    R = R or 0.45*N   # pentagrid region where all lines are present: keep well inside
    inner = [t for t in tiles if math.hypot(*t[2]) < R]
    edges = collections.Counter()
    for _, c, _ in tiles:
        for i in range(4):
            edges[tuple(sorted((c[i], c[(i+1) % 4])))] += 1
    bad = 0; interior = 0
    for (p, q), m in edges.items():
        P, Q = pos(p, e), pos(q, e)
        if math.hypot(*P) < 0.8*R*2.5 and math.hypot(*Q) < 0.8*R*2.5:   # rhombus positions scale ~2.5x grid
            interior += 1; bad += (m != 2)
    idx = collections.Counter(sum(k) for _, c, z in inner for k in c)
    thick = sum(t[0] == 'thick' for t in inner); thin = len(inner) - thick
    return dict(N=N, gamma=gam, tiles=len(inner), thick=thick, thin=thin, ratio=thick/max(thin, 1),
                interior_edges=interior, edges_not_shared_by_two=bad, vertex_index_values=sorted(idx)), tiles, e
if __name__ == '__main__':
    N = int(sys.argv[1]); gam = [float(x) for x in sys.argv[2:7]]
    print(json.dumps(checks(N, gam)[0]))
