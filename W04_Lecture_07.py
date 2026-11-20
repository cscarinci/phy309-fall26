import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 • Lecture 07 • Manifolds", css_file="phy309.css")


@app.cell(hide_code=True)
def _():
    import math

    import marimo as mo
    import matplotlib
    import numpy as np
    from matplotlib.figure import Figure
    from matplotlib.patches import Arc

    # Figures use the same Computer Modern typeface as the text
    matplotlib.rcParams.update({"font.size": 14, "font.family": "serif", "font.serif": ["cmr10", "DejaVu Serif"], "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True, "axes.unicode_minus": False})

    return Arc, Figure, math, mo, np


@app.cell(hide_code=True)
def _(mo):
    # ---- Building blocks shared by all lectures -------------------------
    # Palette with fixed roles (figures only; text carries no colour):
    #   BLUE   the primary object (the particle, the point, the chosen vector)
    #   RED    the second object it is compared with
    #   GREEN  a derived quantity (velocity, relative velocity, tangent vector)
    #   ORANGE a third series, only when three are needed
    #   GREY   reference geometry (equator, light cone, inertial comparison)
    #   LIGHT  fills and grids
    BLUE, RED, GREEN, ORANGE, GREY, LIGHT = "#3f5f8f", "#a8554c", "#4f7f5c", "#b9853f", "#9a9a9a", "#e3ebf4"
    # Figure widths: FULL spans the page, HALF sits beside text or in a pair
    FULL, HALF = 7.4, 3.6

    def header(document, date, running=""):
        """Course header, as on the exercise sheets and exams."""
        return mo.Html(
            f"""
    <div class="bs-head">
      <div class="bs-running">PHY309 &bull; {running}</div>
      <div class="bs-title">Differential Geometry<br>and General Relativity</div>
      <div class="bs-inst">Daegu Gyeongbuk Institute of Science and Technology<br>School of Undergraduate Studies</div>
      <div class="bs-meta">
        <b>Document</b><span>{document}</span><b>Course</b><span>PHY309</span>
        <b>Week</b><span>{date.removeprefix('Week ')}</span><b>Instructor</b><span>Professor Scarinci</span>
      </div>
    </div>
    """
        )

    def _statement(label, title, body):
        head = f"**{label}" + (f" ({title})" if title else "") + ".**"
        return mo.md(head + "\n\n" + body).style({"border-left": f"2px solid {BLUE}", "padding-left": "1rem"})

    def definition(body, title=""):
        return _statement("Definition", title, body)

    def theorem(body, title=""):
        return _statement("Theorem", title, body)

    def proposition(body, title=""):
        return _statement("Proposition", title, body)

    def corollary(body, title=""):
        return _statement("Corollary", title, body)

    def postulate(body, title=""):
        return _statement("Postulate", title, body)

    def note(body):
        """Editorial note of the notebook (not part of the lecture)."""
        return mo.md("**Note.** " + body.strip())

    def arrow(ax, tail, tip, color, label=None, at_tip=False, lw=1.4, **kw):
        """Draw the vector from `tail` to `tip` on a 2D axis, labelled at its middle or its tip.
        The head is small and open, sized from the line width (3 x long, 1.3 x wide, in points), so arrows look alike across lectures."""
        ax.annotate(
            "",
            xy=tip,
            xytext=tail,
            arrowprops={"arrowstyle": f"->,head_length={3 * lw:g},head_width={1.3 * lw:g}", "mutation_scale": 1, "color": color, "lw": lw, "shrinkA": 0, "shrinkB": 0, **kw},
        )
        if label:
            pos = tip if at_tip else ((tail[0] + tip[0]) / 2, (tail[1] + tip[1]) / 2)
            ax.annotate(label, pos, textcoords="offset points", xytext=(6, 6), color=color, fontsize=13)

    def plane(ax, lim):
        """Style a 2D axis as a coordinate plane with range [-lim, lim]."""
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.axhline(0, color="black", lw=0.8)
        ax.axvline(0, color="black", lw=0.8)
        ax.grid(True, color=LIGHT, lw=0.6)
        ax.set_axisbelow(True)

    def blank(w, h, xlim, ylim):
        """A figure with one bare axis (no frame) for sketches."""
        from matplotlib.figure import Figure as _Figure

        fig = _Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def blob(cx, cy, rx, ry, wobble=0.07, seed=0, n=400):
        """Closed organic curve around (cx, cy): an ellipse with a few low harmonics."""
        import numpy as _np

        rng = _np.random.default_rng(seed)
        t = _np.linspace(0, 2 * _np.pi, n)
        r = 1 + sum(wobble / k * rng.uniform(0.4, 1.0) * _np.cos(k * t + rng.uniform(0, 2 * _np.pi)) for k in (2, 3, 4, 5))
        return cx + rx * r * _np.cos(t), cy + ry * r * _np.sin(t)

    def table(rows):
        """Fixed-label readout table: rows are (label, value) pairs of markdown strings."""
        _md = mo.md("\n".join(["| | |", "|:--|:--|"] + [f"| {k} | {v} |" for k, v in rows]))
        return mo.Html(f'<div class="readout">{_md.text}</div>')

    return BLUE, FULL, GREEN, GREY, HALF, LIGHT, ORANGE, RED, arrow, blank, blob, corollary, definition, header, note, plane, postulate, proposition, table, theorem


@app.cell(hide_code=True)
def _(arrow):
    def cross_axes(ax, xlim, ylim, xlabel=None, ylabel=None):
        """A bare pair of coordinate axes through the origin."""
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        arrow(ax, (xlim[0], 0), (xlim[1], 0), "black", lw=0.9)
        arrow(ax, (0, ylim[0]), (0, ylim[1]), "black", lw=0.9)
        if xlabel:
            ax.annotate(xlabel, (xlim[1], 0), textcoords="offset points", xytext=(-12, -18), fontsize=13)
        if ylabel:
            ax.annotate(ylabel, (0, ylim[1]), textcoords="offset points", xytext=(8, -10), fontsize=13)

    return (cross_axes,)


@app.cell(hide_code=True)
def _(mo, np):
    # ---- Interactive 3D figures ------------------------------------------
    # Drawn in the browser on canvases, in the style of the static figures: orthographic views of
    # R^3 = R^2 x R (x^1 towards the viewer, x^2 to the right, y up), surfaces drawn back to front.
    # Dragging turns the view at a fixed scale (all panels of a figure together) and a double click restores
    # it; a figure redrawn by a slider keeps its view. Names sit beside their objects (`texts`), never in a
    # legend box. Typesetting is done by KaTeX.
    import html as _html
    import json as _json

    _PAGE = r"""<!doctype html><html><head><meta charset="utf-8">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" onload="window.typeset && typeset()"></script>
    <style>
      html, body { margin: 0; padding: 0; background: transparent; overflow: hidden;
                   font-family: KaTeX_Main, "Latin Modern Roman", Georgia, serif; }
      #o { display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 4px 16px; }
      #g { position: relative; flex: 1 1 300px; min-width: 240px; max-width: __MAXW__px; display: grid;
           grid-template-columns: repeat(__COLS__, minmax(0, 1fr)); gap: 6px 14px; touch-action: none; cursor: grab;
           user-select: none; -webkit-user-select: none; }
      @media (max-width: 520px) { #g { grid-template-columns: minmax(0, 1fr); } }
      #g.drag { cursor: grabbing; }
      .p { position: relative; }
      .p canvas { display: block; width: 100%; }
      .cap { text-align: center; font-size: 14px; }
      .lab { position: absolute; left: 0; top: 0; white-space: nowrap; line-height: 1.1; pointer-events: none; font-size: 15px; }
      .katex { font-size: 1em; }
      #lg { flex: 0 0 auto; border: 1px solid #c8c8c8; border-radius: 4px; padding: 4px 10px; background: #fff; font-size: 14px; }
      #lg:empty { display: none; }
      .it { display: flex; align-items: center; gap: 8px; margin: 4px 0; white-space: nowrap; }
      .it svg { flex: 0 0 24px; }
      #hint { position: absolute; right: 0; bottom: 0; color: #888; opacity: 0.7; font: 15px Georgia, serif; }
    </style></head><body>
    <div id="o"><div id="g" role="img" aria-label="__ALT__"><div id="hint">&#10227;</div></div><div id="lg"></div></div>
    <script>
    (function () {
      const S = __SCENE__;
      const RAD = Math.PI / 180, L = [0.3, -0.4, 0.87];
      const lit = [247, 251, 255], dark = [201, 223, 244], lit2 = [219, 235, 251], dark2 = [163, 194, 230];
      const rgb = (a, b, k) => "rgb(" + [0, 1, 2].map((i) => Math.round(a[i] + (b[i] - a[i]) * k)).join(",") + ")";
      const texs = [];
      const tex = (el, t) => { el.dataset.tex = t; el.textContent = t.replace(/\\[a-z]+\{?|[{}$^_]/gi, ""); texs.push(el); };
      const dot3 = (u, p) => u[0] * p[0] + u[1] * p[1] + u[2] * p[2];

      class Scene {
        constructor(spec, host) {
          const ys = (this.ys = spec.ys);
          this.box = document.createElement("div");
          this.box.className = "p";
          this.cv = document.createElement("canvas");
          this.box.appendChild(this.cv);
          this.g = this.cv.getContext("2d");
          host.appendChild(this.box);
          if (spec.caption) {
            const c = document.createElement("div");
            c.className = "cap";
            tex(c, spec.caption);
            this.box.appendChild(c);
          }
          const pts = (this.pts = []), quads = (this.quads = []), segs = (this.segs = []);
          this.dots = []; this.heads = []; this.labs = []; this.outl = spec.outlines || [];
          const add = (x, y, z) => (pts.push(x, y, z), pts.length / 3 - 1);
          const eq = [];  // faces of the surfaces drawn with an edge
          for (const s of spec.surfaces) {
            const base = pts.length / 3, n = s.n, m = s.m, id = (i, j) => base + i * m + j;
            for (const v of s.v) pts.push(v);
            const P = (k) => [pts[3 * k], pts[3 * k + 1], pts[3 * k + 2]];
            const inTint = (x1, x2) => s.tint && x1 > s.tint[0] && x1 <= s.tint[1] && x2 > s.tint[2] && x2 <= s.tint[3];
            const sLit = s.tone ? s.tone.map((c) => Math.round(0.06 * c + 0.94 * 255)) : lit;
            const sDark = s.tone ? s.tone.map((c) => Math.round(0.3 * c + 0.7 * 255)) : dark;
            for (let i = 0; i < n - 1; i++) for (let j = 0; j < m - 1; j++) {
              const q = [id(i, j), id(i + 1, j), id(i + 1, j + 1), id(i, j + 1)];
              const v = q.map(P);
              if (v.some((p) => p.some(isNaN))) continue;
              if (s.edge) eq.push([q, s.edge]);
              const deep = inTint((v[0][0] + v[2][0]) / 2, (v[0][1] + v[2][1]) / 2);
              let col = s.flat;
              if (!col) {
                const a = [0, 1, 2].map((t) => v[2][t] - v[0][t]), b = [0, 1, 2].map((t) => v[3][t] - v[1][t]);
                const nn = [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
                const len = Math.hypot(...nn) || 1;
                const k = Math.min(1, Math.abs((nn[0] * L[0] + nn[1] * L[1] + nn[2] * L[2]) / len) / 1.0034);
                col = deep ? rgb(dark2, lit2, k) : rgb(sDark, sLit, k);
              }
              quads.push([q, col, deep ? 1 : s.alpha]);
            }
            for (const [axis, every, c, lw] of s.wire || []) {
              const rows = axis === 0 ? n : m, cols = axis === 0 ? m : n;
              for (let r = 0; r < rows; r++) {
                if (r % every !== 0 && r !== rows - 1) continue;
                for (let t = 0; t < cols - 1; t++) {
                  const a = axis === 0 ? id(r, t) : id(t, r), b = axis === 0 ? id(r, t + 1) : id(t + 1, r);
                  const pa = P(a), pb = P(b);
                  if (pa.concat(pb).some(isNaN)) continue;
                  if (s.clear && inTint((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2)) continue;
                  segs.push({ a, b, c, lw, line: null });
                }
              }
            }
          }
          // edges of the surfaces drawn with an edge, keyed by their end points, so that faces sharing an edge
          // across a seam or between two sheets are found; an edge with one face only is a boundary
          const ekey = (k) => pts[3 * k].toFixed(3) + "," + pts[3 * k + 1].toFixed(3) + "," + pts[3 * k + 2].toFixed(3);
          const emap = new Map();
          for (const [q, ed] of eq) for (let t = 0; t < 4; t++) {
            const ka = ekey(q[t]), kb = ekey(q[(t + 1) % 4]);
            if (ka === kb) continue;
            const key = ka < kb ? ka + "|" + kb : kb + "|" + ka;
            if (!emap.has(key)) emap.set(key, { a: q[t], b: q[(t + 1) % 4], f: [], c: ed[0], w: ed[1] });
            emap.get(key).f.push(q);
          }
          this.sil = [...emap.values()];
          this.lines = spec.lines.map((ln) => {
            const idx = [];
            for (let k = 0; k < ln.p.length; k += 3) idx.push(add(ln.p[k], ln.p[k + 1], ln.p[k + 2]));
            const line = { idx, dash: ln.d, cum: new Float64Array(idx.length) };
            for (let k = 0; k < idx.length - 1; k++)
              if (![ln.p[3 * k], ln.p[3 * k + 3]].some(isNaN)) segs.push({ a: idx[k], b: idx[k + 1], c: ln.c, lw: ln.w, line, k, e: ln.e || 0 });
            return line;
          });
          for (const d of spec.points) this.dots.push({ i: add(...d.p), c: d.c, r: d.r, h: d.h });
          for (const h of spec.heads) this.heads.push({ i: add(...h.p), j: add(...h.q), c: h.c, w: h.w });
          // the centre of the scene and the radius of a ball holding it, heights at their drawing scale
          let src = pts;
          if (spec.box) {
            src = [];
            for (const p of [0, 1]) for (const q of [0, 1]) for (const t of [0, 1]) src.push(spec.box[0][p], spec.box[1][q], spec.box[2][t]);
          }
          const lo = [Infinity, Infinity, Infinity], hi = [-Infinity, -Infinity, -Infinity];
          for (let k = 0; k < src.length; k++) {
            const t = k % 3, v = src[k] * (t === 2 ? ys : 1);
            if (!isNaN(v)) { lo[t] = Math.min(lo[t], v); hi[t] = Math.max(hi[t], v); }
          }
          const C = [0, 1, 2].map((t) => (lo[t] + hi[t]) / 2);
          let R = 0;
          for (let k = 0; k < src.length; k += 3) {
            const d = Math.hypot(src[k] - C[0], src[k + 1] - C[1], src[k + 2] * ys - C[2]);
            if (!isNaN(d)) R = Math.max(R, d);
          }
          C[2] /= ys;
          this.C = C;
          this.R = R;
          for (const l of spec.labels) {
            const el = document.createElement("div");
            el.className = "lab";
            el.style.color = l.c;
            tex(el, l.t);
            this.box.appendChild(el);
            this.labs.push({ el, i: add(...l.p), a: l.a === null ? null : l.a * RAD, r: l.r });  // direction null: centred on its point
          }
          // the first view's height range about C (screen up), so that the frame fits that view
          const fa = S.az * RAD, fe = S.el * RAD, fu = [-Math.sin(fe) * Math.cos(fa), -Math.sin(fe) * Math.sin(fa), Math.cos(fe) * ys];
          this.vlo = Infinity; this.vhi = -Infinity;
          for (let k = 0; k < pts.length; k += 3) {
            const v = fu[0] * (pts[k] - C[0]) + fu[1] * (pts[k + 1] - C[1]) + fu[2] * (pts[k + 2] - C[2]);
            if (!isNaN(v)) { this.vlo = Math.min(this.vlo, v); this.vhi = Math.max(this.vhi, v); }
          }
          const M = pts.length / 3;
          this.X = new Float64Array(M); this.Y = new Float64Array(M); this.Z = new Float64Array(M);
        }

        size(W, H, R) {
          this.W = W; this.H = H;
          this.sc = 0.94 * W / (2 * R);
          const dpr = window.devicePixelRatio || 1;
          this.cv.width = Math.round(W * dpr);
          this.cv.height = Math.round(H * dpr);
          this.cv.style.height = H + "px";
          this.g.setTransform(dpr, 0, 0, dpr, 0, 0);
        }

        draw(az, el) {
          const { g, pts, X, Y, Z, W, H, sc, ys } = this;
          if (!W) return;
          const a = az * RAD, e = el * RAD;
          const r = [-Math.sin(a), Math.cos(a), 0];
          const u = [-Math.sin(e) * Math.cos(a), -Math.sin(e) * Math.sin(a), Math.cos(e) * ys];
          const d = [Math.cos(e) * Math.cos(a), Math.cos(e) * Math.sin(a), Math.sin(e) * ys];
          const tx = W / 2 - dot3(r, this.C) * sc, ty = 28 + (dot3(u, this.C) + this.vhi) * sc;
          for (let k = 0; k < X.length; k++) {
            const x = pts[3 * k], y = pts[3 * k + 1], z = pts[3 * k + 2];
            X[k] = (x * r[0] + y * r[1] + z * r[2]) * sc + tx;
            Y[k] = ty - (x * u[0] + y * u[1] + z * u[2]) * sc;
            Z[k] = x * d[0] + y * d[1] + z * d[2];
          }
          for (const ln of this.lines) {  // screen length along each line, so that dashes run on across segments
            ln.cum[0] = 0;
            for (let k = 1; k < ln.idx.length; k++) {
              const p = ln.idx[k - 1], q = ln.idx[k];
              ln.cum[k] = ln.cum[k - 1] + (isNaN(X[p] + X[q]) ? 0 : Math.hypot(X[q] - X[p], Y[q] - Y[p]));
            }
          }
          const items = [], bias = S.bias;
          for (const q of this.quads) items.push([(Z[q[0][0]] + Z[q[0][1]] + Z[q[0][2]] + Z[q[0][3]]) / 4, 0, q]);
          for (const s of this.segs) items.push([(Z[s.a] + Z[s.b]) / 2 + bias + (s.e || 0), 1, s]);
          for (const h of this.heads) items.push([Z[h.i] + bias, 2, h]);
          for (const p of this.dots) items.push([Z[p.i] + 2 * bias, 3, p]);
          // outlines of round surfaces as seen from this view: a sphere's rim circle, a vertical cylinder's two side lines,
          // a vertical double cone's side lines (slope 1); each cut into short segments drawn among the other items
          const P = (p) => [(p[0] * r[0] + p[1] * r[1] + p[2] * r[2]) * sc + tx, ty - (p[0] * u[0] + p[1] * u[1] + p[2] * u[2]) * sc, p[0] * d[0] + p[1] * d[1] + p[2] * d[2]];
          const R3 = [-Math.sin(a), Math.cos(a), 0], U3 = [-Math.sin(e) * Math.cos(a), -Math.sin(e) * Math.sin(a), Math.cos(e)];
          const edge = (A, B, o, lift) => {
            for (let k = 0; k < 16; k++) {
              const s0 = k / 16, s1 = (k + 1) / 16, p0 = P(A.map((v, i) => v + (B[i] - v) * s0)), p1 = P(A.map((v, i) => v + (B[i] - v) * s1));
              items.push([(p0[2] + p1[2]) / 2 + bias + lift, 4, [p0[0], p0[1], p1[0], p1[1], o.c, o.w]]);
            }
          };
          for (const o of this.outl) {
            if (o.k === "sphere") {
              const c = o.p, z = P(c)[2] + o.r + bias;
              for (let k = 0; k < 96; k++) {
                const t0 = (k / 96) * 2 * Math.PI, t1 = ((k + 1) / 96) * 2 * Math.PI;
                const p0 = P(c.map((v, i) => v + o.r * (Math.cos(t0) * R3[i] + Math.sin(t0) * U3[i]))), p1 = P(c.map((v, i) => v + o.r * (Math.cos(t1) * R3[i] + Math.sin(t1) * U3[i])));
                items.push([z, 4, [p0[0], p0[1], p1[0], p1[1], o.c, o.w]]);
              }
            } else if (o.k === "cylinder") {
              for (const sg of [-1, 1]) {
                const x = o.p[0] + sg * o.r * R3[0], y = o.p[1] + sg * o.r * R3[1];
                edge([x, y, o.z[0]], [x, y, o.z[1]], o, 0.02);
              }
            } else if (o.k === "cone") {
              const te = Math.tan(e);
              for (const [up, cs] of [[1, te], [-1, -te]]) {
                if (Math.abs(cs) >= 1) continue;
                for (const sg of [-1, 1]) {
                  const al = a + sg * Math.acos(cs);
                  edge(o.p, [o.p[0] + o.h * Math.cos(al), o.p[1] + o.h * Math.sin(al), o.p[2] + up * o.h], o, 0.02);
                }
              }
            }
          }
          // the edges of those surfaces on their outline in this view: between a face turned towards the viewer
          // and one turned away (opposite orientation on screen), and every boundary edge
          const face = (q) => (X[q[2]] - X[q[0]]) * (Y[q[3]] - Y[q[1]]) - (Y[q[2]] - Y[q[0]]) * (X[q[3]] - X[q[1]]);
          for (const s of this.sil)
            if (s.f.length === 1 || face(s.f[0]) * face(s.f[1]) < 0) items.push([(Z[s.a] + Z[s.b]) / 2 + bias, 4, [X[s.a], Y[s.a], X[s.b], Y[s.b], s.c, s.w]]);
          items.sort((p, q) => p[0] - q[0]);
          g.clearRect(0, 0, W, H);
          g.lineJoin = "round";
          for (const [, kind, o] of items) {
            if (kind === 0) {
              const q = o[0];
              g.beginPath();
              g.moveTo(X[q[0]], Y[q[0]]);
              for (let t = 1; t < 4; t++) g.lineTo(X[q[t]], Y[q[t]]);
              g.closePath();
              g.fillStyle = g.strokeStyle = o[1];
              g.globalAlpha = o[2];
              g.fill();
              if (o[2] === 1) { g.lineWidth = 0.6; g.setLineDash([]); g.stroke(); }
              g.globalAlpha = 1;
            } else if (kind === 1) {
              g.beginPath();
              g.moveTo(X[o.a], Y[o.a]);
              g.lineTo(X[o.b], Y[o.b]);
              g.strokeStyle = o.c;
              g.lineWidth = o.lw;
              const dash = o.line && o.line.dash;
              g.lineCap = dash ? "butt" : "round";
              g.setLineDash(dash || []);
              g.lineDashOffset = dash ? -o.line.cum[o.k] : 0;
              g.stroke();
            } else if (kind === 2) {
              let vx = X[o.i] - X[o.j], vy = Y[o.i] - Y[o.j];
              const len = Math.hypot(vx, vy) || 1;
              vx /= len; vy /= len;
              // an open head, as in the flat figures (matplotlib "->"): 3 x the stroke width long, 1.3 x wide on each side, in points
              const pt = 4 / 3, hl = 3 * o.w * pt, hw = 1.3 * o.w * pt, bx = X[o.i] - hl * vx, by = Y[o.i] - hl * vy;
              g.beginPath();
              g.moveTo(bx - hw * vy, by + hw * vx);
              g.lineTo(X[o.i], Y[o.i]);
              g.lineTo(bx + hw * vy, by - hw * vx);
              g.strokeStyle = o.c;
              g.lineWidth = o.w;
              g.setLineDash([]);
              g.lineCap = "round";
              g.stroke();
            } else if (kind === 4) {
              g.beginPath();
              g.moveTo(o[0], o[1]);
              g.lineTo(o[2], o[3]);
              g.strokeStyle = o[4];
              g.lineWidth = o[5];
              g.lineCap = "round";
              g.setLineDash([]);
              g.stroke();
            } else {
              g.beginPath();
              g.arc(X[o.i], Y[o.i], o.r, 0, 2 * Math.PI);
              g.setLineDash([]);
              g.fillStyle = o.h ? "#fff" : o.c;
              g.fill();
              g.strokeStyle = o.h ? o.c : "#fff";
              g.lineWidth = o.h ? 1.5 : 1;
              g.stroke();
            }
          }
          for (const l of this.labs) {  // beside its point, on the side given by its direction
            const c = l.a === null ? 0 : Math.cos(l.a), s = l.a === null ? 0 : Math.sin(l.a);
            const hx = c > 0.35 ? 0 : c < -0.35 ? -100 : -50, vy = s > 0.35 ? -100 : s < -0.35 ? 0 : -50;
            l.el.style.transform = `translate(${X[l.i] + l.r * c}px, ${Y[l.i] - l.r * s}px) translate(${hx}%, ${vy}%)`;
          }
        }
      }

      const grid = document.getElementById("g"), out = document.getElementById("o");
      const scenes = S.panels.map((p) => new Scene(p, grid));
      const Rmax = Math.max(...scenes.map((s) => s.R));
      const lg = document.getElementById("lg");
      for (const e of S.legend) {
        const it = document.createElement("div"), t = document.createElement("span");
        it.className = "it";
        const dash = e.d ? ` stroke-dasharray="${e.d.join(" ")}"` : "";
        it.innerHTML = {
          dot: `<svg width="24" height="14"><circle cx="12" cy="7" r="4.2" fill="${e.c}"/></svg>`,
          ring: `<svg width="24" height="14"><circle cx="12" cy="7" r="3.8" fill="#fff" stroke="${e.c}" stroke-width="1.5"/></svg>`,
          line: `<svg width="24" height="14"><line x1="1" y1="7" x2="23" y2="7" stroke="${e.c}" stroke-width="${e.w || 2}"${dash}/></svg>`,
          area: `<svg width="24" height="14"><rect x="2" y="1.5" width="20" height="11" fill="${e.c}" fill-opacity="${e.o || 1}" stroke="${e.e || e.c}" stroke-width="1.2"/></svg>`,
        }[e.k];
        tex(t, e.t);
        it.appendChild(t);
        lg.appendChild(it);
      }

      // the view, shared by all panels and kept by the page when a slider redraws the figure
      let store = {};
      try { store = window.parent.__phy3d || (window.parent.__phy3d = {}); } catch (e) {}
      let view = S.key && store[S.key] ? { ...store[S.key] } : { az: S.az, el: S.el };
      const keep = () => { if (S.key) store[S.key] = { ...view }; };

      function fit() {  // square-ish canvases holding their balls, so that the scale never changes while turning
        for (const s of scenes) {
          const W = s.box.clientWidth;
          s.size(W, Math.ceil((s.vhi - s.vlo) * 0.94 * W / (2 * (S.shared ? Rmax : s.R))) + 56, S.shared ? Rmax : s.R);
        }
        if (window.frameElement) window.frameElement.style.height = out.offsetHeight + "px";
      }
      const draw = () => { for (const s of scenes) s.draw(view.az, view.el); };
      window.typeset = () => {
        for (const el of texs) try { katex.render(el.dataset.tex, el, { throwOnError: false }); } catch (e) {}
        fit();
        draw();
      };

      let pending = false;
      const redraw = () => { if (!pending) { pending = true; requestAnimationFrame(() => { pending = false; draw(); }); } };
      let grab = null;
      grid.addEventListener("pointerdown", (e) => { grab = { x: e.clientX, y: e.clientY, ...view }; grid.setPointerCapture(e.pointerId); grid.classList.add("drag"); });
      grid.addEventListener("pointermove", (e) => {
        if (!grab) return;
        view = { az: grab.az - (e.clientX - grab.x) * 0.45, el: Math.max(-89, Math.min(89, grab.el + (e.clientY - grab.y) * 0.45)) };
        keep();
        redraw();
      });
      const drop = () => { grab = null; grid.classList.remove("drag"); };
      grid.addEventListener("pointerup", drop);
      grid.addEventListener("pointercancel", drop);
      grid.addEventListener("dblclick", () => { view = { az: S.az, el: S.el }; if (S.key) delete store[S.key]; redraw(); });
      new ResizeObserver(() => { fit(); draw(); }).observe(out);
      if (window.katex) window.typeset();
    })();
    </script></body></html>"""

    def _flat(*xyz):
        return np.round(np.stack(np.broadcast_arrays(*(np.asarray(v, dtype=float) for v in xyz)), -1).ravel(), 3).tolist()

    def sheet(x1, x2, y, wire=(), tint=None, clear=False, flat=None, alpha=1.0, tone=None, edge=None):
        """A surface through the grid points (x1, x2, y) (2D arrays). `wire` lists grid lines to draw, as
        (axis, every, colour, width): every `every`-th row (axis 0) or column (axis 1), and the last one.
        Faces whose centre lies in tint = (x^1 lo, x^1 hi, x^2 lo, x^2 hi) (lo excluded) take deeper tones and
        stay opaque, without wire there when `clear`; the other faces have the opacity `alpha`.
        `flat` is one colour instead of the shading, and `tone` (a colour such as RED) shades the surface in
        light tones of that colour instead of the light blue ones. `edge` = (colour, width) draws the outline of
        the surface as seen from the current view: its silhouette, the rims of its holes and its boundary; sheets
        that share edges (two halves of one surface) must be oriented alike for their common edges to show."""
        n, m = np.shape(x1)
        rgb = [int(tone[k : k + 2], 16) for k in (1, 3, 5)] if tone else None
        return {"n": n, "m": m, "v": _flat(x1, x2, y), "wire": [list(t) for t in wire], "tint": tint, "clear": clear, "flat": flat, "alpha": alpha, "tone": rgb, "edge": list(edge) if edge else None}

    def patch(corners, colour, alpha=1.0, n=6):
        """The flat parallelogram (or quadrilateral) with the four `corners` (in order), one colour, opacity `alpha`;
        cut into n x n faces, so that it is drawn in the right order among other surfaces."""
        c = [np.asarray(q, float) for q in corners]
        s, t = np.meshgrid(np.linspace(0, 1, n + 1), np.linspace(0, 1, n + 1), indexing="ij")
        p = (1 - s)[..., None] * (1 - t)[..., None] * c[0] + s[..., None] * (1 - t)[..., None] * c[1] + (s * t)[..., None] * c[2] + ((1 - s) * t)[..., None] * c[3]
        return sheet(p[..., 0], p[..., 1], p[..., 2], flat=colour, alpha=alpha)

    def panel(ys, surfaces=(), lines=(), points=(), axes=(), arrows=(), arcs=(), texts=(), caption=None, box=None, outlines=()):
        """One drawing of a 3D figure, with heights at the scale `ys`.
        lines: (x1, x2, y, colour, width[, dash, depth offset]); points: ((x^1, x^2, y), colour[, radius, hollow]);
        axes: (tail, tip, TeX label, direction of the label in degrees), drawn black;
        arrows: (tail, tip, colour[, width, dash]), vectors with a head in their colour;
        arcs: (x1, x2, y, colour[, width]), curves ending in a head, such as a turning arrow;
        texts: ((x^1, x^2, y), TeX, colour, direction[, distance]), names beside their objects and short
        labels such as tick values; caption: TeX below the drawing;
        box: ((x^1 lo, hi), (x^2 lo, hi), (y lo, hi)) to size the drawing by, instead of its own points;
        outlines: the edge of a round surface as seen from the current view, redrawn as the figure turns (ys = 1):
        ("sphere", centre, radius, colour, width), ("cylinder", (x^1, x^2) of the vertical axis, radius, (y lo, y hi), colour, width),
        ("cone", vertex, height, colour, width) for the vertical double cone of slope 1."""
        p = {"ys": ys, "surfaces": list(surfaces), "lines": [], "points": [], "heads": [], "labels": [], "caption": caption, "box": box, "outlines": []}
        for o in outlines:
            if o[0] == "sphere":
                p["outlines"].append({"k": "sphere", "p": [float(c) for c in o[1]], "r": float(o[2]), "c": o[3], "w": o[4]})
            elif o[0] == "cylinder":
                p["outlines"].append({"k": "cylinder", "p": [float(c) for c in o[1]], "r": float(o[2]), "z": [float(c) for c in o[3]], "c": o[4], "w": o[5]})
            else:
                p["outlines"].append({"k": "cone", "p": [float(c) for c in o[1]], "h": float(o[2]), "c": o[3], "w": o[4]})
        for ln in lines:
            p["lines"].append({"p": _flat(*ln[:3]), "c": ln[3], "w": ln[4], "d": ln[5] if len(ln) > 5 else None, "e": ln[6] if len(ln) > 6 else 0})
        for tail, tip, label, d in axes:
            a, b = np.asarray(tail, float), np.asarray(tip, float)
            seg = a + np.linspace(0, 0.96, 60)[:, None] * (b - a)
            p["lines"].append({"p": _flat(*seg.T), "c": "#000000", "w": 1.1, "d": None})
            p["heads"].append({"p": b.tolist(), "q": (a + 0.9 * (b - a)).tolist(), "c": "#000000", "w": 1.1})
            p["labels"].append({"p": b.tolist(), "t": label, "c": "#000000", "a": d, "r": 5})
        for q in points:
            p["points"].append({"p": [float(c) for c in q[0]], "c": q[1], "r": q[2] if len(q) > 2 else 4.0, "h": bool(q[3]) if len(q) > 3 else False})
        for ar in arrows:
            a, b = np.asarray(ar[0], float), np.asarray(ar[1], float)
            seg = a + np.linspace(0, 1, 40)[:, None] * (b - a)
            p["lines"].append({"p": _flat(*seg.T), "c": ar[2], "w": ar[3] if len(ar) > 3 else 1.8, "d": ar[4] if len(ar) > 4 else None, "e": 0})
            p["heads"].append({"p": b.tolist(), "q": (a + 0.9 * (b - a)).tolist(), "c": ar[2], "w": ar[3] if len(ar) > 3 else 1.8})
        for arc in arcs:
            c = np.stack(np.broadcast_arrays(*(np.asarray(v, dtype=float) for v in arc[:3])), -1)
            p["lines"].append({"p": _flat(*c[:-1].T), "c": arc[3], "w": arc[4] if len(arc) > 4 else 1.8, "d": None, "e": 0})
            p["heads"].append({"p": c[-1].tolist(), "q": c[max(0, len(c) - 4)].tolist(), "c": arc[3], "w": arc[4] if len(arc) > 4 else 1.8})
        for tx in texts:
            p["labels"].append({"p": [float(c) for c in tx[0]], "t": tx[1], "c": tx[2], "a": tx[3], "r": tx[4] if len(tx) > 4 else 5})
        return p

    def turntable(az, el, alt, panels, legend=(), height=360, width=None, cols=1, key=None, shared=True, bias=0.03):
        """An interactive 3D figure of one or more `panels` (made by panel(), in `cols` columns), first seen
        from azimuth `az` and elevation `el` (degrees); each drawing at most `height` pixels high, all together
        at most `width` wide, with an optional legend box beside them (not used: names sit beside their objects). `key` names the view
        so that it survives a redraw; with `shared`, all panels have one scale.
        legend: (kind, colour, TeX[, line width / edge colour, dash / opacity]) with kind "dot", "ring", "line" or "area"."""
        scene = {"az": az, "el": el, "h": height, "bias": bias, "panels": list(panels), "legend": [], "key": key, "shared": shared}
        for e in legend:
            item = {"k": e[0], "c": e[1], "t": e[2]}
            if len(e) > 3:
                item["e" if e[0] == "area" else "w"] = e[3]
            if len(e) > 4:
                item["o" if e[0] == "area" else "d"] = e[4]
            scene["legend"].append(item)
        page = (_PAGE.replace("__MAXW__", str(width or max(700, cols * height + (cols - 1) * 14))).replace("__COLS__", str(cols))
                .replace("__ALT__", _html.escape(alt)).replace("__SCENE__", _json.dumps(scene, separators=(",", ":"))))
        return mo.Html(f'<iframe srcdoc="{_html.escape(page)}" title="{_html.escape(alt)}" style="display: block; width: 100%; height: {height}px; border: 0;"></iframe>')

    return panel, patch, sheet, turntable


@app.cell(hide_code=True)
def _(BLUE, np, sheet):
    # ---- Sphere figures of this lecture ---------------------------------
    def sphere(alpha=1.0):
        """The unit sphere of R^3 (z up), shaded like the other surfaces, at opacity `alpha`."""
        th, ph = np.meshgrid(np.linspace(0, np.pi, 37), np.linspace(0, 2 * np.pi, 73), indexing="ij")
        return sheet(np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th), alpha=alpha)

    # the sphere's edge as seen from the current view, for the panel's outlines
    SPHERE_EDGE = ("sphere", (0, 0, 0), 1.0, BLUE, 1.2)

    return SPHERE_EDGE, sphere


@app.cell(hide_code=True)
def _(header):
    header("Lecture 07", "Week 04", "Lecture 07 • Manifolds")
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, arrow, fig_congruence, fig_surfaces, mo, np):
    _fig = Figure(figsize=(5.6, 2.2), layout="constrained")
    _l, _r = _fig.subplots(1, 2)
    for _ax in (_l, _r):
        _ax.set_xlim(-1.6, 1.6)
        _ax.set_ylim(-0.4, 2.1)
        _ax.axis("off")
    for _x in (-0.6, 0.6):
        _l.plot([_x, _x], [0, 2], color=BLUE)
        arrow(_l, (_x, 0), (_x, 0.9), GREEN)
        _l.plot(_x, 0, "o", color="black", ms=4)
    _l.text(-0.9, 0.5, "$v$", color=GREEN, fontsize=13)
    _l.text(0.7, 0.5, "$v' = v$", color=GREEN, fontsize=13)
    _l.text(-0.7, -0.35, "$p$", fontsize=13)
    _l.text(0.5, -0.35, "$q$", fontsize=13)
    _s = np.linspace(0, 1.7, 100)  # the histories end before they reach the source
    _r.plot([0, 0], [-0.2, 2.1], color="black")
    for _sgn in (-1, 1):
        _r.plot(_sgn * 0.6 * (1 - (_s / 2.05) ** 2), _s, color=BLUE)
        arrow(_r, (_sgn * 0.6, 0), (_sgn * 0.6, 0.9), GREEN)
        _r.plot(_sgn * 0.6, 0, "o", color="black", ms=4)
    _r.text(-0.9, 0.5, "$v$", color=GREEN, fontsize=13)
    _r.text(0.7, 0.5, "$v'$", color=GREEN, fontsize=13)
    _r.text(-0.7, -0.35, "$p$", fontsize=13)
    _r.text(0.5, -0.35, "$q$", fontsize=13)
    _r.text(0.1, 1.95, "source of gravity", color="black", fontsize=11)

    mo.vstack(
        [
            mo.md(
                r"""
    ## So far

    - geometry = *affine space* + additional structure &nbsp;$\leadsto$&nbsp; no origins or frames, just congruence <span class="nw">$\Longrightarrow$ straight lines</span> <span class="nw">$\Longrightarrow$ parallel lines</span>
    - gravity defines free-falling particles: a notion of “straight lines” incompatible with parallelism (tidal effects), hence with congruence
    """
            ),
            _fig,
            mo.md(
                r"""
    **In this lecture:** generalize geometry so that it does *not need congruence* &nbsp;$\leadsto$&nbsp; drop the affine structure!

    **References:** Schutz 6.1; Carroll 2.2; Sasane 1.1–1.3

    ## II.2 &nbsp; Manifolds

    ### Charts and atlases

    differential geometry = *manifolds* + additional structure

    Manifolds &nbsp;$\leadsto$&nbsp; generalized spaces with points, but no displacement vectors, which look like $\mathbb{R}^m$, but only locally

    In $\mathbb{R}^m$ we have a preferred point $o$ and a preferred basis of vectors $e_i$

    $$
    o = \begin{bmatrix} 0 \\ 0 \\ \vdots \\ 0 \end{bmatrix}, \qquad e_i = \begin{bmatrix} 0 \\ \vdots \\ 1 \\ \vdots \\ 0 \end{bmatrix}
    $$

    In $\mathbb{A}^m$ each choice of $(o, e_i) \in \mathbb{A}^m \times \mathbb{V}^m$ defines

    $$
    \varphi_{(o, e_i)} : \mathbb{A}^m \longrightarrow \mathbb{R}^m, \qquad p = \underbrace{o + x^i e_i}_{\mathclap{\footnotesize \begin{matrix} \text{using} \\ - : \mathbb{A} \times \mathbb{A} \to \mathbb{V} \end{matrix}}} \longmapsto \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^m \end{bmatrix}
    $$

    Importantly $\varphi_{(o, e_i)} : \mathbb{A}^m \longrightarrow \mathbb{R}^m$ is a global bijection

    For $\varphi_{(o, e_i)}$, $\varphi_{(\tilde{o}, \tilde{e}_i)}$ two such charts

    <span class="chain">$\displaystyle \varphi_{(\tilde{o}, \tilde{e}_i)} \circ \varphi_{(o, e_i)}^{-1} : \mathbb{R}^m \overset{\sim}{\longrightarrow} \mathbb{R}^m, \qquad$ $\displaystyle \begin{bmatrix} x^1 \\ \vdots \\ x^m \end{bmatrix} \longmapsto \begin{bmatrix} \tilde{x}^1 \\ \vdots \\ \tilde{x}^m \end{bmatrix} = \begin{bmatrix} A^1{}_1 & \cdots & A^1{}_m \\ \vdots & & \vdots \\ A^m{}_1 & \cdots & A^m{}_m \end{bmatrix} \begin{bmatrix} x^1 \\ \vdots \\ x^m \end{bmatrix} + \begin{bmatrix} b^1 \\ \vdots \\ b^m \end{bmatrix}$</span>

    change of coordinates = linear transformation + constant translation

    In a manifold $M^m$ we will keep the ability of producing coordinate charts

    $$
    \varphi_\alpha : U_\alpha \subseteq M^m \longrightarrow V_\alpha \subseteq \mathbb{R}^m
    $$

    - now only local bijections
    - for $\varphi_\alpha$ and $\varphi_\beta$: &nbsp; $\varphi_\beta \circ \varphi_\alpha^{-1} : V_\alpha \subseteq \mathbb{R}^m \overset{\sim}{\longrightarrow} V_\beta \subseteq \mathbb{R}^m$ &nbsp; (bijective at least in some subset of $V_\alpha$)

    **Example.** 2-sphere $\mathbb{S}^2$, &nbsp; 2-torus $\mathbb{T}^2$, &nbsp; genus 2 surface $\Sigma_2$
    """
            ),
            fig_surfaces,
            mo.md(r"""What does congruence mean on the sphere?"""),
            fig_congruence,
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, ORANGE, RED, SPHERE_EDGE, math, np, panel, sheet, sphere, turntable):
    # Surfaces of genus 0, 1, 2
    _t = np.linspace(0, 2 * np.pi, 241)
    _u, _w = np.meshgrid(np.linspace(0, 2 * np.pi, 61), np.linspace(0, 2 * np.pi, 31), indexing="ij")
    _torus = sheet((1.0 + 0.42 * np.cos(_w)) * np.cos(_u), (1.0 + 0.42 * np.cos(_w)) * np.sin(_u), 0.42 * np.sin(_w), edge=(BLUE, 1.2))
    # genus 2: two tori smoothly joined, side by side on the screen, as z^2 = -S(a, b) with a along the screen
    # and b across it; the grid points just outside the region S < 0 are moved onto its rim S = 0
    _az = math.radians(-30)
    _ea, _eb = np.array([-math.sin(_az), math.cos(_az)]), np.array([math.cos(_az), math.sin(_az)])

    def _S(a, b):
        s1 = (np.hypot(a + 0.95, b) - 0.62) ** 2 - 0.09
        s2 = (np.hypot(a - 0.95, b) - 0.62) ** 2 - 0.09
        return -0.18 * np.logaddexp(-s1 / 0.18, -s2 / 0.18)

    _a, _b = np.meshgrid(np.linspace(-2.0, 2.0, 101), np.linspace(-1.0, 1.0, 51), indexing="ij")
    _in = _S(_a, _b) < 0
    _rim = np.zeros_like(_in)
    for _di in (-1, 0, 1):
        for _dj in (-1, 0, 1):
            _rim |= np.roll(np.roll(_in, _di, 0), _dj, 1)
    _rim &= ~_in
    _ra, _rb = _a[_rim], _b[_rim]
    for _ in range(12):  # Newton steps onto S = 0
        _ga = (_S(_ra + 1e-5, _rb) - _S(_ra - 1e-5, _rb)) / 2e-5
        _gb = (_S(_ra, _rb + 1e-5) - _S(_ra, _rb - 1e-5)) / 2e-5
        _k = _S(_ra, _rb) / (_ga**2 + _gb**2)
        _ra, _rb = _ra - _k * _ga, _rb - _k * _gb
    _a[_rim], _b[_rim] = _ra, _rb
    _z = np.where(_in, np.sqrt(np.maximum(-_S(_a, _b), 0.0)), np.where(_rim, 0.0, np.nan))
    _x, _y = _a * _ea[0] + _b * _eb[0], _a * _ea[1] + _b * _eb[1]
    fig_surfaces = turntable(
        -30,
        45,
        "the sphere, the torus and the genus 2 surface",
        [
            panel(1.0, surfaces=[sphere()], outlines=[SPHERE_EDGE], lines=[(np.cos(_t), np.sin(_t), 0 * _t, "#000000", 1.0)], caption=r"\mathbb{S}^2"),
            panel(1.0, surfaces=[_torus], caption=r"\mathbb{T}^2"),
            panel(1.0, surfaces=[sheet(_x, _y, _z, edge=(BLUE, 1.2)), sheet(_x[:, ::-1], _y[:, ::-1], -_z[:, ::-1], edge=(BLUE, 1.2))], caption=r"\Sigma_2"),
        ],
        height=220,
        cols=3,
        shared=False,
        bias=0.12,  # the equator lies on the sphere: draw it in front of the faces around it
    )
    # congruence on the sphere: vectors copied along the equator, then carried up to the pole
    _al = math.asin(0.6)  # longitudes of p and q
    _la = np.linspace(0, np.pi / 2, 61)

    def _meridian(lon):
        return np.cos(_la) * math.cos(lon), np.cos(_la) * math.sin(lon), np.sin(_la)

    _p, _q, _r = (math.cos(_al), -math.sin(_al), 0.0), (math.cos(_al), math.sin(_al), 0.0), (0.0, 0.0, 1.0)
    _v, _vq = (-math.cos(_al), math.sin(_al), 0.0), (-math.cos(_al), -math.sin(_al), 0.0)  # v and v' at r, along the meridians of p and q
    def _m(lon, lt):
        return (math.cos(lt) * math.cos(lon), math.cos(lt) * math.sin(lon), math.sin(lt))

    def _tn(lon, lt):  # the northward unit tangent of the meridian
        return (-math.sin(lt) * math.cos(lon), -math.sin(lt) * math.sin(lon), math.cos(lt))

    fig_congruence = turntable(
        0,
        24,
        "the sphere with vectors v copied along the equator from p to q, and the vectors v and v' carried up the meridians of p and q to the pole r",
        [
            panel(
                1.0,
                surfaces=[sphere()],
                outlines=[SPHERE_EDGE],
                lines=[(np.cos(_t), np.sin(_t), 0 * _t, "#000000", 1.0)]
                + [(*_meridian(-_al), BLUE, 1.6), (*_meridian(_al), RED, 1.6)],
                arrows=[((math.cos(_l), math.sin(_l), 0.0), (math.cos(_l), math.sin(_l), 0.4), GREEN) for _l in np.linspace(-_al, _al, 6)]
                + [(_r, tuple(0.55 * np.array(_v) + _r), GREEN), (_r, tuple(0.55 * np.array(_vq) + _r), ORANGE)]
                + [(_m(_lon, _lt), tuple(np.array(_m(_lon, _lt)) + 0.4 * np.array(_tn(_lon, _lt))), _c) for _lon, _c in ((-_al, GREEN), (_al, ORANGE)) for _lt in [0.85]],
                points=[(_p, "#000000", 3.4), (_q, "#000000", 3.4), (_r, "#000000", 3.4)],
                texts=[
                    (_p, "p", "#000000", -100),
                    (_q, "q", "#000000", -80),
                    (_r, "r", "#000000", -90, 8),
                    ((_p[0], _p[1], 0.2), "v", GREEN, 180, 8),
                    ((_q[0], _q[1], 0.2), "v", GREEN, 0, 8),
                    (tuple(0.55 * np.array(_v) + _r), "v", GREEN, 0, 8),
                    (tuple(0.55 * np.array(_vq) + _r), "v'", ORANGE, 180, 8),
                ],
            )
        ],
        height=320,
        width=320,  # as wide as high: the picture scales with its width
        bias=0.12,
    )
    return fig_congruence, fig_surfaces


@app.cell(hide_code=True)
def _(BLUE, LIGHT, RED, arrow, blank, blob, definition, fig_stereo, mo, np):
    # two charts on M: the pages V_alpha, V_beta, each cut by the image of the edge of the other chart's domain
    from matplotlib.path import Path as _Path

    def _inside(curve, X, Y):
        return _Path(np.column_stack(curve)).contains_points(np.column_stack([X.ravel(), Y.ravel()])).reshape(X.shape)

    _fig, _ax = blank(5.6, 3.9, (-0.1, 10.1), (-0.4, 6.7))
    _ax.plot(*blob(5.0, 4.45, 2.25, 1.95, wobble=0.09, seed=3), color="black", lw=1.4)
    _ax.text(2.95, 6.15, "$M$", fontsize=14)
    _Ua, _Ub = blob(4.62, 4.45, 1.12, 0.95, seed=1, wobble=0.03), blob(5.38, 4.4, 1.12, 1.0, seed=2, wobble=0.03)
    _X, _Y = np.meshgrid(np.linspace(2.8, 7.2, 500), np.linspace(2.6, 6.6, 500))
    _ax.contourf(_X, _Y, (_inside(_Ua, _X, _Y) & _inside(_Ub, _X, _Y)).astype(float), levels=[0.5, 1.5], colors=[LIGHT])
    _ax.plot(*_Ua, color=RED, lw=1.4)
    _ax.plot(*_Ub, color=BLUE, lw=1.4)
    _ax.text(3.85, 5.6, r"$U_\alpha$", color=RED, fontsize=13, ha="center")
    _ax.text(6.15, 5.6, r"$U_\beta$", color=BLUE, fontsize=13, ha="center")
    _ax.text(5.0, 4.42, r"$U_\alpha \cap U_\beta$", fontsize=11, ha="center", va="center")
    _w, _h, _y0 = 2.8, 2.0, 0.3
    _s = np.linspace(0, 1, 120)
    for _x0, _frame, _cut, _side, _name, _img in (
        (0.05, RED, BLUE, 1, r"$V_\alpha \subseteq \mathbb{R}^2$", r"$\varphi_\alpha(U_\alpha \cap U_\beta)$"),
        (7.15, BLUE, RED, -1, r"$V_\beta \subseteq \mathbb{R}^2$", r"$\varphi_\beta(U_\alpha \cap U_\beta)$"),
    ):
        _base = _x0 + 0.95 if _side == 1 else _x0 + _w - 0.95
        _xc = _base - _side * 0.3 * np.sin(np.pi * _s)  # an arc, bulging away from the filled side
        _edge = _x0 + _w if _side == 1 else _x0
        _ax.fill(np.r_[_xc, [_edge, _edge]], np.r_[_y0 + _h * _s, [_y0 + _h, _y0]], color=LIGHT, lw=0)
        _ax.plot(_xc, _y0 + _h * _s, color=_cut, lw=1.4)
        _ax.plot([_x0, _x0 + _w, _x0 + _w, _x0, _x0], [_y0, _y0, _y0 + _h, _y0 + _h, _y0], color=_frame, lw=1.4)
        _ax.text(_x0 + _w / 2, _y0 - 0.2, _name, color=_frame, fontsize=13, ha="center", va="top")
        _ax.text((_base - _side * 0.3 + _edge) / 2, _y0 + _h / 2, _img, fontsize=11, ha="center", va="center")
    # the arrows touch no outline
    arrow(_ax, (2.55, 3.75), (1.4, 2.6), RED, connectionstyle="arc3,rad=0.25")
    _ax.text(1.55, 3.45, r"$\varphi_\alpha$", color=RED, fontsize=13, ha="right")
    arrow(_ax, (7.45, 3.75), (8.6, 2.6), BLUE, connectionstyle="arc3,rad=-0.25")
    _ax.text(8.45, 3.45, r"$\varphi_\beta$", color=BLUE, fontsize=13)
    arrow(_ax, (3.1, 1.3), (6.9, 1.3), "black")
    _ax.text(5.05, 1.1, r"$\varphi_\beta \circ \varphi_\alpha^{-1}$", fontsize=13, ha="center", va="top")

    mo.vstack(
        [
            definition(
                r"""
    A **$m$-dimensional manifold** ($m$-manifold) is a set of points $M^m \ni p$, with a collection of charts $\mathcal{A} \ni \varphi_\alpha$

    $$
    \varphi_\alpha : U_\alpha \subseteq M \longrightarrow V_\alpha \subseteq \mathbb{R}^m
    $$

    where

    - $U_\alpha$ *cover* $M$ &nbsp; $\left( \bigcup_\alpha U_\alpha = M \right)$
    - $V_\alpha$ are *open sets* of $\mathbb{R}^m$ &nbsp; (given by union of open balls in $\mathbb{R}^m$)
    - $\varphi_\alpha : U_\alpha \overset{\sim}{\longrightarrow} V_\alpha$ are *bijections* &nbsp; (each $U_\alpha$ “looks like” $V_\alpha = \varphi_\alpha(U_\alpha)$ <span class="nw">via $\varphi_\alpha$)</span>
    - $\varphi_\alpha(U_\alpha \cap U_\beta) \subseteq V_\alpha$, &nbsp; $\varphi_\beta(U_\alpha \cap U_\beta) \subseteq V_\beta$ are also open
    - $\varphi_\beta \circ \varphi_\alpha^{-1}$ are $\underbrace{\textit{diffeomorphisms}}_{\footnotesize \mathclap{\begin{matrix} \text{smooth bijections} \\ \text{with smooth inverse} \end{matrix}}\rule[-0.35em]{0pt}{0pt}}$

        $$
        \varphi_\beta \circ \varphi_\alpha^{-1} : \smash[b]{\underbrace{\varphi_\alpha(U_\alpha \cap U_\beta)}_{\footnotesize \subseteq \mathbb{R}^m}} \overset{\sim}{\longrightarrow} \smash[b]{\underbrace{\varphi_\beta(U_\alpha \cap U_\beta)}_{\footnotesize \subseteq \mathbb{R}^m}}
        $$
    """,
                "Manifold",
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $\mathbb{S}^2 = \{\, (x^1, x^2, x^3) \in \mathbb{R}^3 \mid$ $(x^1)^2 + (x^2)^2 + (x^3)^2 = 1 \,\}$ &nbsp; (Earth)

    $V_\alpha \subseteq \mathbb{R}^2$ = “page $\alpha$ of a geographical atlas”, &nbsp; $V_\beta \subseteq \mathbb{R}^2$ = “page $\beta$”
    """
            ),
            _fig,
            mo.md(
                r"""
    **Remark.** $\varphi_\beta \circ \varphi_\alpha^{-1}$ diffeomorphism &nbsp; <span class="nw">$\Longrightarrow$ &nbsp; we can</span> do calculus on each $U_\alpha \subseteq M$ using usual calculus on $V_\alpha \subseteq \mathbb{R}^m$ and every result agrees on $U_\alpha \cap U_\beta$

    ### Topology

    **Remark.** Collection of all open sets defines a topology on $\mathbb{R}^m$ <span class="nw">$\leadsto$ &nbsp; study</span> properties of $\mathbb{R}^m$ invariant under continuous deformations

    $\varphi_\alpha : U_\alpha \longrightarrow V_\alpha$ bijection, $V_\alpha$ open, $\varphi_\alpha(U_\alpha \cap U_\beta)$ open &nbsp; <span class="nw">$\Longrightarrow$ &nbsp; defines</span> a topology on $M$ with open sets $\varphi_\alpha^{-1}(V_\alpha \cap W) \subseteq M$, for $W \subseteq \mathbb{R}^m$ open, and their unions

    **Remark.** We need to require a few *technical conditions* (Hausdorff + second countable) on this topology, but it will not be too important.

    ### Smooth functions
    """
            ),
            definition(
                r"""
    Given an $m$-manifold $M$, $\mathcal{A} = \{\, \varphi_\alpha : U_\alpha \longrightarrow V_\alpha \subseteq \mathbb{R}^m \,\}$, a function $f : M \longrightarrow \mathbb{R}$ is called **smooth** if, for every chart $\varphi_\alpha \in \mathcal{A}$, the composition

    $$
    \underbrace{f \circ \varphi_\alpha^{-1}}_{\footnotesize \mathclap{\begin{matrix} \text{usual scalar} \\ \text{function in } \mathbb{R}^m \end{matrix}}} : V_\alpha \subseteq \mathbb{R}^m \longrightarrow \mathbb{R}
    $$

    is smooth
    """,
                "Smooth function",
            ),
            mo.md(
                r"""
    $\Longrightarrow$ &nbsp; we know how to calculate derivatives with respect to coordinates in $V_\alpha$

    Let's simplify notation a bit here: &nbsp; $\varphi_\alpha : U_\alpha \longrightarrow V_\alpha$ <span class="nw">$\leadsto$ &nbsp; $\varphi : U \longrightarrow V \subseteq \mathbb{R}^m \ni x$</span>

    $$
    \frac{\partial}{\partial x^\mu} (f \circ \varphi^{-1})(x) = \lim_{h \to 0} \frac{(f \circ \varphi^{-1})(x + h e_\mu) - (f \circ \varphi^{-1})(x)}{h}
    $$

    $$
    \begin{aligned}
    D_x (f \circ \varphi^{-1})(v) &= \lim_{h \to 0} \frac{(f \circ \varphi^{-1})(x + h v) - (f \circ \varphi^{-1})(x)}{h} \\[8pt]
    &= v^\mu\, \frac{\partial}{\partial x^\mu} (f \circ \varphi^{-1})(x)
    \end{aligned}
    $$

    $\Longrightarrow$ &nbsp; given two charts $\varphi : U \longrightarrow V \subseteq \mathbb{R}^m \ni x$, &nbsp; $\tilde{\varphi} : \tilde{U} \longrightarrow \tilde{V} \subseteq \mathbb{R}^m \ni \tilde{x}$

    $$
    \left. \begin{aligned} f \circ \varphi^{-1} &: V \longrightarrow \mathbb{R} \\ f \circ \tilde{\varphi}^{-1} &: \tilde{V} \longrightarrow \mathbb{R} \end{aligned} \right\} \quad \text{representations of } f \text{ in each chart}
    $$

    are related via

    <span class="chain">$\displaystyle (f \circ \varphi^{-1})(x) = (f \circ \tilde{\varphi}^{-1}) \circ \underbrace{(\tilde{\varphi} \circ \varphi^{-1})(x)}_{\footnotesize \tilde{x}(x)} \qquad \text{on } \varphi(U \cap \tilde{U}) \subseteq V$</span>

    $$
    \begin{aligned}
    \Longrightarrow \quad \frac{\partial}{\partial x^\mu} (f \circ \varphi^{-1})(x) &= \frac{\partial}{\partial \tilde{x}^\nu} (f \circ \tilde{\varphi}^{-1})(\tilde{x}(x))\, \frac{\partial \tilde{x}^\nu}{\partial x^\mu}(x) \\[8pt]
    &= \underbrace{\frac{\partial \tilde{x}^\nu}{\partial x^\mu}(x)}_{\mathclap{\footnotesize \begin{matrix} \text{Jacobian matrix of the} \\ \text{change of coordinates} \end{matrix}}} \frac{\partial}{\partial \tilde{x}^\nu} (f \circ \tilde{\varphi}^{-1})(\tilde{x}(x))
    \end{aligned}
    $$

    ($\tilde{x} = \tilde{\varphi} \circ \varphi^{-1}(x)$ <span class="nw">$\leadsto$ &nbsp; smooth</span> by the diffeo assumption!)

    $\therefore$ &nbsp; the notion of smoothness for $f : M \longrightarrow \mathbb{R}$ via charts is well-defined because changes of charts are always smooth!

    ### Stereographic charts on the sphere

    **Example.** &nbsp; $\mathbb{S}^2 = \{\, (x, y, z) \in \mathbb{R}^3 \mid x^2 + y^2 + z^2 = 1 \,\}$

    Choose a point $n = (0, 0, 1)$ (north pole). Define $\varphi_n : \mathbb{S}^2 - \{n\} \longrightarrow \mathbb{R}^2$ via stereographic projection

    $$
    \varphi_n(x, y, z) = (u, v) = \left( \frac{x}{1 - z},\ \frac{y}{1 - z} \right)
    $$
    """
            ),
            fig_stereo,
            mo.md(
                r"""
    By triangle similarity:

    <span class="chain">$\displaystyle z \begin{bmatrix} u \\ v \\ 0 \end{bmatrix} = \begin{bmatrix} u - x \\ v - y \\ 0 \end{bmatrix}$ $\displaystyle \Longrightarrow \quad (1 - z)\, u = x, \quad (1 - z)\, v = y$</span>

    $\Longrightarrow$ &nbsp; $\varphi_n$ is a bijection from $U_n = \mathbb{S}^2 - \{n\}$ to $V_n = \mathbb{R}^2$

    Choose $s = (0, 0, -1)$ (south pole)

    <span class="chain">$\displaystyle \varphi_s : \underbrace{\mathbb{S}^2 - \{s\}}_{\footnotesize U_s} \longrightarrow \underbrace{\mathbb{R}^2}_{\footnotesize V_s}, \qquad$ $\displaystyle (x, y, z) \longmapsto \varphi_s(x, y, z) = (\tilde{u}, \tilde{v}) = \left( \frac{x}{1 + z},\ \frac{y}{1 + z} \right)$</span>

    is also a bijection

    - $U_n \cup U_s = (\mathbb{S}^2 - \{n\}) \cup (\mathbb{S}^2 - \{s\}) = \mathbb{S}^2$
    - $V_n, V_s$ are open, &nbsp; $\varphi_n(U_n \cap U_s) = \mathbb{R}^2 - \{(0, 0)\}$, &nbsp; $\varphi_s(U_s \cap U_n) = \mathbb{R}^2 - \{(0, 0)\}$ are open
    - $\varphi_s \circ \varphi_n^{-1} : \mathbb{R}^2 - \{(0, 0)\} \longrightarrow \mathbb{R}^2 - \{(0, 0)\}$ is smooth with smooth inverse!

    $$
    \varphi_s \circ \varphi_n^{-1}(u, v) = \left( \frac{u}{u^2 + v^2},\ \frac{v}{u^2 + v^2} \right) = (\tilde{u}, \tilde{v})
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, GREY, RED, SPHERE_EDGE, math, np, panel, patch, sphere, turntable):
    # the line through n and p meets the plane z = 0 at (u, v, 0); the line through s and p at (u~, v~, 0)
    _ph, _th = math.radians(60), math.radians(30)
    _P = np.array([math.sin(_ph) * math.cos(_th), math.sin(_ph) * math.sin(_th), math.cos(_ph)])
    _n, _s, _o = np.array([0.0, 0.0, 1.0]), np.array([0.0, 0.0, -1.0]), np.zeros(3)
    _F = np.array([_P[0], _P[1], 0.0])
    _Un = np.array([_P[0] / (1 - _P[2]), _P[1] / (1 - _P[2]), 0.0])
    _Us = np.array([_P[0] / (1 + _P[2]), _P[1] / (1 + _P[2]), 0.0])
    _plane = [(-1.25, -1.25, 0), (1.75, -1.25, 0), (1.75, 1.25, 0), (-1.25, 1.25, 0)]
    _edge = np.array(_plane + _plane[:1])
    _k = np.linspace(0, 1, 40)[:, None]

    def _seg(a, b):
        return tuple((a + _k * (b - a)).T)

    fig_stereo = turntable(
        -30,
        18,
        "the unit sphere and the plane z = 0, with the line through n and p meeting the plane at (u, v, 0) and the line through s and p meeting it at (u~, v~, 0)",
        [
            panel(
                1.0,
                surfaces=[sphere(alpha=0.45), patch(_plane, "#e8e8e8", 0.6, n=16)],
                outlines=[SPHERE_EDGE],
                lines=[
                    (*_edge.T, GREY, 1.2),
                    (np.cos(np.linspace(0, 2 * np.pi, 121)), np.sin(np.linspace(0, 2 * np.pi, 121)), np.zeros(121), "#000000", 1.0),
                    (*_seg(_n, _o), "#000000", 1.0, [2, 3]),
                    (*_seg(_P, _F), "#000000", 1.0, [2, 3]),
                    (*_seg(_o, _Un), GREY, 1.0, [4, 3]),
                    (*_seg(_n, _Un), BLUE, 1.8),
                    (*_seg(_s, _P), RED, 1.8),
                ],
                points=[(tuple(_n), "#000000", 3.4), (tuple(_s), "#000000", 3.4), (tuple(_o), "#000000", 2.6), (tuple(_P), "#000000", 3.4), (tuple(_F), "#000000", 2.6), (tuple(_Un), BLUE, 4.0), (tuple(_Us), RED, 4.0)],
                texts=[
                    (tuple(_n), "n = (0, 0, 1)", "#000000", 90),
                    (tuple(_o), "(0, 0, 0)", "#000000", 150, 8),
                    (tuple(_P), "p = (x, y, z)", "#000000", 30, 12),
                    (tuple(_F), "(x, y, 0)", "#000000", -90, 12),
                    (tuple(_Un), "(u, v, 0)", "#000000", -60, 14),
                    (tuple(_Us), r"(\tilde{u}, \tilde{v}, 0)", "#000000", -130, 8),
                    (tuple((_P + _Un) / 2), r"\begin{matrix} \text{line through } n \text{ and } p \\ \text{in } \mathbb{R}^3 \end{matrix}", "#000000", 45, 16),
                ],
            )
        ],
        height=420,
        bias=0.12,
    )
    return (fig_stereo,)


@app.cell(hide_code=True)
def _(mo):
    lat = mo.ui.slider(-45, 45, 1, value=35, label="latitude of $p$", show_value=False)
    return (lat,)


@app.cell(hide_code=True)
def _(BLUE, GREY, RED, blank, lat, math, mo, np):
    _a = math.radians(lat.value)
    _x, _z = math.cos(_a), math.sin(_a)
    _u, _ut = _x / (1 - _z), _x / (1 + _z)
    _t = math.radians(180 + lat.value / 2 - max(-5, min(25, 20 + 3 * lat.value)))  # direction of the name of p

    _R = 2.8  # holds the projected points for every latitude of the slider (u <= 2.41 at 45 degrees)
    _fig, _ax = blank(3.4, 2.7, (-1.3, _R), (-1.5, 1.6))
    _th = np.linspace(0, 2 * np.pi, 200)
    _ax.plot(np.cos(_th), np.sin(_th), color=GREY)
    _ax.plot([-1.3, _R], [0, 0], color="black")
    _ax.plot([0, _x, _u], [1, _z, 0], color=BLUE)  # ray from n through p to phi_n(p)
    _ax.plot([0, _x, _ut], [-1, _z, 0], color=RED)  # ray from s through p to phi_s(p)
    for _pt, _name, _col, _off in (((0, 1), "$n$", "black", (-14, 4)), ((0, -1), "$s$", "black", (-14, -12)), ((_x, _z), "$p$", "black", (18 * math.cos(_t), 18 * math.sin(_t)))):
        _ax.plot(*_pt, "o", color=_col, ms=5)
        _ax.annotate(_name, _pt, textcoords="offset points", xytext=_off, color=_col, fontsize=14, **({"ha": "center", "va": "center"} if _name == "$p$" else {}))
    _ax.plot(_u, 0, "o", color=BLUE, ms=5)
    _ax.annotate(r"$u$", (_u, 0), textcoords="offset points", xytext=(4, 5), ha="left", va="bottom", fontsize=13)
    _ax.plot(_ut, 0, "o", color=RED, ms=5)
    _ax.annotate(r"$\tilde{u}$", (_ut, 0), textcoords="offset points", xytext=(4, -5), ha="left", va="top", fontsize=13)
    mo.vstack([mo.hstack([lat], justify="start"), _fig])
    return


if __name__ == "__main__":
    app.run()
