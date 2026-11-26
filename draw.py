#!/usr/bin/env python3
"""SVG drawings: a Penrose tiling (generic gamma, sum 0) and a singular grid (gamma=0) with its broken edges in red."""
import math, collections
from pentagrid import tiling, pos
def svg(gam, N, Rpos, fn, title, mark_bad=False):
    tiles, e = tiling(N, gam)
    S = 900; sc = S/(2*Rpos)
    cnt = collections.Counter()
    for _, c, _ in tiles:
        for i in range(4): cnt[tuple(sorted((c[i], c[(i+1) % 4])))] += 1
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S+40}" width="{S}" height="{S+40}">',
           f'<rect width="100%" height="100%" fill="#f7f4ec"/>', f'<title>{title}</title>',
           f'<clipPath id="c"><circle cx="{S/2}" cy="{S/2}" r="{S/2-6}"/></clipPath><g clip-path="url(#c)">']
    for kind, c, z in tiles:
        P = [pos(k, e) for k in c]
        if min(math.hypot(*p) for p in P) > Rpos*1.05: continue
        pts = " ".join(f"{S/2+x*sc:.1f},{S/2-y*sc:.1f}" for x, y in P)
        fill = '#1f3a5f' if kind == 'thick' else '#d9a441'
        out.append(f'<polygon points="{pts}" fill="{fill}" fill-opacity="0.9" stroke="#f7f4ec" stroke-width="1"/>')
    if mark_bad:
        for (p, q), m in cnt.items():
            if m != 2:
                (x1, y1), (x2, y2) = pos(p, e), pos(q, e)
                if max(math.hypot(x1, y1), math.hypot(x2, y2)) < Rpos*0.8:
                    out.append(f'<line x1="{S/2+x1*sc:.1f}" y1="{S/2-y1*sc:.1f}" x2="{S/2+x2*sc:.1f}" y2="{S/2-y2*sc:.1f}" stroke="#c0392b" stroke-width="4"/>')
    out.append('</g>')
    out.append(f'<text x="{S/2}" y="{S+28}" font-family="Georgia,serif" font-size="20" text-anchor="middle" fill="#222">{title}</text></svg>')
    open(fn, 'w').write("\n".join(out))
svg([0.11, 0.23, -0.07, 0.31, -0.58], 16, 14, 'penrose.svg', 'Penrose rhombus tiling from a pentagrid, gamma sum 0 (thick navy, thin ochre)')
svg([0, 0, 0, 0, 0], 16, 14, 'singular.svg', 'Singular grid, gamma = 0: red edges are not shared by exactly two tiles', True)
