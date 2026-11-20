import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 • Lecture 08 • Charts on the sphere, smooth maps, tangent vectors", css_file="phy309.css")


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
    header("Lecture 08", "Week 04", "Lecture 08 • Charts on the sphere, smooth maps, tangent vectors")
    return


@app.cell(hide_code=True)
def _(fig_angles, mo):
    mo.vstack([mo.md(r"""
    ## Last time

    - a manifold is a set of points $M \ni p$ with a collection of charts $\mathcal{A} \ni \varphi_\alpha : U_\alpha \subseteq M \longrightarrow V_\alpha \subseteq \mathbb{R}^m$: the $U_\alpha$ cover $M$, the $V_\alpha$ and $\varphi_\alpha(U_\alpha \cap U_\beta)$ are open, the $\varphi_\alpha$ are bijections and the changes of chart $\varphi_\beta \circ \varphi_\alpha^{-1}$ are smooth with smooth inverse

    **In this lecture:** the atlas of the sphere in full, smooth maps between manifolds, and tangent vectors

    **References:** Schutz 6.1; Carroll 2.2–2.3; Sasane 1.3, 2.1

    ## II.3 &nbsp; Charts on the sphere, smooth maps, tangent vectors

    ### Charts on the sphere

    **Example.** &nbsp; $\mathbb{S}^2 = \{\, (x, y, z) \in \mathbb{R}^3 \mid x^2 + y^2 + z^2 = 1 \,\}$

    Choose $n = (0, 0, 1)$. Define $\varphi_n : U_n \longrightarrow V_n$ via &nbsp; <span class="nw">$U_n = \mathbb{S}^2 - \{n\}$, &nbsp; $V_n = \mathbb{R}^2$</span>

    <span class="chain">$\displaystyle \varphi_n(x, y, z) = (u, v) = \left( \frac{x}{1 - z},\ \frac{y}{1 - z} \right)$ $\displaystyle \qquad \big( z\, (u, v, 0) = (u - x, v - y, 0) \big)$ $\displaystyle \Longrightarrow \quad \varphi_n^{-1}(u, v) = \left( \frac{2u}{1 + u^2 + v^2},\ \frac{2v}{1 + u^2 + v^2},\ \frac{-1 + u^2 + v^2}{1 + u^2 + v^2} \right)$</span>

    Similarly, choose $s = (0, 0, -1)$. Define $\varphi_s : U_s \longrightarrow V_s$ via &nbsp; <span class="nw">$U_s = \mathbb{S}^2 - \{s\}$, &nbsp; $V_s = \mathbb{R}^2$,</span>

    <span class="chain">$\displaystyle \varphi_s(x, y, z) = (\tilde{u}, \tilde{v}) = \left( \frac{x}{1 + z},\ \frac{y}{1 + z} \right)$ $\displaystyle \Longrightarrow \quad \varphi_s^{-1}(\tilde{u}, \tilde{v}) = \left( \frac{2\tilde{u}}{1 + \tilde{u}^2 + \tilde{v}^2},\ \frac{2\tilde{v}}{1 + \tilde{u}^2 + \tilde{v}^2},\ \frac{1 - \tilde{u}^2 - \tilde{v}^2}{1 + \tilde{u}^2 + \tilde{v}^2} \right)$</span>

    - $U_n \cup U_s = (\mathbb{S}^2 - \{n\}) \cup (\mathbb{S}^2 - \{s\}) = \mathbb{S}^2$
    - $V_n = \mathbb{R}^2$, $V_s = \mathbb{R}^2$ open
    - $\varphi_n : U_n \longrightarrow V_n$, &nbsp; $\varphi_s : U_s \longrightarrow V_s$ bijective
    - $\varphi_n(U_n \cap U_s)$ and $\varphi_s(U_n \cap U_s)$ are open!

        $$
        \begin{aligned}
        \varphi_n(U_n \cap U_s) &= \varphi_n(\mathbb{S}^2 - \{n, s\}) = \mathbb{R}^2 - \{(0, 0)\} \\[4pt]
        \varphi_s(U_n \cap U_s) &= \varphi_s(\mathbb{S}^2 - \{n, s\}) = \mathbb{R}^2 - \{(0, 0)\}
        \end{aligned}
        $$
    - $\varphi_s \circ \varphi_n^{-1}$:

        $$
        \begin{aligned}
        \varphi_s \circ \varphi_n^{-1}(u, v) &= \varphi_s\!\left( \frac{2u}{1 + u^2 + v^2},\ \frac{2v}{1 + u^2 + v^2},\ \frac{-1 + u^2 + v^2}{1 + u^2 + v^2} \right) \\[8pt]
        &= \left( \frac{2u}{2 (u^2 + v^2)},\ \frac{2v}{2 (u^2 + v^2)} \right) \\[8pt]
        &= \left( \frac{u}{u^2 + v^2},\ \frac{v}{u^2 + v^2} \right) = (\tilde{u}, \tilde{v})
        \end{aligned}
        $$

    $\leadsto$ &nbsp; diffeomorphism $\mathbb{R}^2 - \{(0, 0)\} \longrightarrow \mathbb{R}^2 - \{(0, 0)\}$. &nbsp; We can differentiate it infinitely many times; it is invertible $(\varphi_s \circ \varphi_n^{-1})^{-1} = \varphi_n \circ \varphi_s^{-1}$ and the inverse is also infinitely differentiable

    $$
    \varphi_n \circ \varphi_s^{-1}(\tilde{u}, \tilde{v}) = \left( \frac{\tilde{u}}{\tilde{u}^2 + \tilde{v}^2},\ \frac{\tilde{v}}{\tilde{u}^2 + \tilde{v}^2} \right)
    $$

    $\therefore$ &nbsp; $\mathbb{S}^2$ with $\mathcal{A} = \{\varphi_n, \varphi_s\}$ is a 2-manifold

    **Remark.** There are many more charts $\varphi : U \subseteq \mathbb{S}^2 \longrightarrow V \subseteq \mathbb{R}^2$ which are “compatible” with $\varphi_n$ and $\varphi_s$ in the sense

    $$
    \varphi_\alpha \circ \varphi^{-1} : \varphi(U \cap U_\alpha) \longrightarrow \varphi_\alpha(U \cap U_\alpha) \quad \text{is a diffeo for } \alpha = n, s
    $$

    - choose any $q \in \mathbb{S}^2$ and define

        $$
        \varphi_q : \mathbb{S}^2 - \{q\} \longrightarrow \mathbb{R}^2 \approx (q - o)^\perp \subseteq \mathbb{R}^3
        $$

        the stereographic projection based at $q$
    - choose any $q \in \mathbb{S}^2$ ($= n$) and $e_1 \in (n - o)^\perp$, &nbsp; $e_2 = (n - o) \times e_1$, &nbsp; and remove the half meridian

        $$
        C = \{\, p \in \mathbb{S}^2 \mid \langle p - o, e_2 \rangle = 0,\ \langle p - o, e_1 \rangle \geq 0 \,\} \ni n, s
        $$

        define

    $$
    \phi : \mathbb{S}^2 - C \longrightarrow (0, \pi), \qquad \theta : \mathbb{S}^2 - C \longrightarrow (0, 2\pi)
    $$

    <span class="chain">$\displaystyle \cos\phi(p) = \langle p - o,\ n - o \rangle,$ $\displaystyle \quad \cos\theta(p) = \frac{\langle p - o,\ e_1 \rangle}{\sin\phi(p)},$ $\displaystyle \quad \sin\theta(p) = \frac{\langle p - o,\ e_2 \rangle}{\sin\phi(p)}$ $\displaystyle \qquad \theta \leadsto \text{oriented angle}$</span>

    the polar and azimuthal angles, giving

    $$
    \psi : \mathbb{S}^2 - C \longrightarrow (0, \pi) \times (0, 2\pi) \subset \mathbb{R}^2
    $$
    """), fig_angles, mo.md(r"""

    $$
    \begin{aligned}
    \psi^{-1}(\phi, \theta) &= (\sin\phi \cos\theta,\ \sin\phi \sin\theta,\ \cos\phi) = (x, y, z) \\[8pt]
    &= \left( \frac{2u}{1 + u^2 + v^2},\ \frac{2v}{1 + u^2 + v^2},\ \frac{-1 + u^2 + v^2}{1 + u^2 + v^2} \right) = \varphi_n^{-1}(u, v) \\[8pt]
    \Longrightarrow \quad (u, v) &= \varphi_n \circ \psi^{-1}(\phi, \theta) = \left( \cot\frac{\phi}{2} \cos\theta,\ \cot\frac{\phi}{2} \sin\theta \right)
    \end{aligned}
    $$

    diffeo from $(0, \pi) \times (0, 2\pi)$ to $\mathbb{R}^2 - \{\, \lambda e_1,\ \lambda \geq 0 \,\}$

    $\therefore$ &nbsp; $\mathbb{S}^2$ with $\mathcal{A} = \{\varphi_n, \varphi_s, \varphi_q, \psi\}$ is also a 2-manifold &nbsp;$\leadsto$&nbsp; we assume $\mathcal{A}$ contains all possible compatible charts (maximal atlas)
    """)])
    return


@app.cell(hide_code=True)
def _(BLUE, FULL, GREEN, GREY, LIGHT, RED, SPHERE_EDGE, arrow, blank, blob, math, np, panel, patch, sphere, turntable):
    # Polar angle phi from n and azimuthal angle theta from e_1
    _ph, _th = math.radians(50), math.radians(40)
    _P = (math.sin(_ph) * math.cos(_th), math.sin(_ph) * math.sin(_th), math.cos(_ph))
    _F = (_P[0], _P[1], 0.0)  # foot of p on the equatorial plane
    _k = np.linspace(0, 1, 30)
    _a = np.linspace(0, 1, 60)
    _plane = [(-1.25, -1.25, 0), (1.25, -1.25, 0), (1.25, 1.25, 0), (-1.25, 1.25, 0)]
    _edge = np.array(_plane + _plane[:1])
    fig_angles = turntable(
        -30,
        20,
        "the unit sphere and the plane z = 0, with the poles n and s, the centre o, the vector e_1, a point p, and the angles phi from n and theta from e_1",
        [
            panel(
                1.0,
                surfaces=[sphere(alpha=0.45), patch(_plane, "#e8e8e8", 0.6, n=16)],
                outlines=[SPHERE_EDGE],
                lines=[
                    (*_edge.T, GREY, 1.2),
                    (np.cos(np.linspace(0, 2 * np.pi, 121)), np.sin(np.linspace(0, 2 * np.pi, 121)), np.zeros(121), "#000000", 1.0),
                    (0 * _k, 0 * _k, 2 * _k - 1, "#000000", 0.9),
                    (_P[0] + 0 * _k, _P[1] + 0 * _k, _P[2] * (1 - _k), GREY, 1.0, [4, 3]),
                    (_F[0] * _k, _F[1] * _k, 0 * _k, GREY, 1.0, [4, 3]),
                    (0.4 * np.sin(_ph * _a) * math.cos(_th), 0.4 * np.sin(_ph * _a) * math.sin(_th), 0.4 * np.cos(_ph * _a), GREEN, 1.4),
                    (0.45 * np.cos(_th * _a), 0.45 * np.sin(_th * _a), 0 * _a, GREEN, 1.4),
                ],
                arrows=[((0, 0, 0), _P, BLUE), ((0, 0, 0), (1.0, 0, 0), "#000000", 1.4)],
                points=[((0, 0, 1), "#000000", 3.4), ((0, 0, -1), "#000000", 3.4), ((0, 0, 0), "#000000", 2.6), (_P, BLUE, 3.4)],
                texts=[
                    ((0, 0, 1), "n", "#000000", 90),
                    ((0, 0, -1), "s", "#000000", -90),
                    ((0, 0, 0), "o", "#000000", -150, 6),
                    (_P, "p", "#000000", 125, 6),
                    ((1.0, 0, 0), "e_1", "#000000", -90, 8),
                    ((0.4 * math.sin(_ph / 2) * math.cos(_th), 0.4 * math.sin(_ph / 2) * math.sin(_th), 0.4 * math.cos(_ph / 2)), r"\phi", GREEN, 30, 6),
                    ((0.62 * math.cos(_th / 2), 0.62 * math.sin(_th / 2), 0), r"\theta", GREEN, 0, 3),
                ],
            )
        ],
        height=380,
        bias=0.12,
    )
    # Smooth map between manifolds through charts
    fig_smooth, _ax = blank(FULL, 3.1, (-0.2, 10.2), (-0.5, 4.7))
    from matplotlib.path import Path as _Path

    _g = np.linspace(0, 1, 200)
    for _cx, _name, _seed in ((2.0, "$M$", 4), (8.0, "$N$", 5)):
        _ax.plot(*blob(_cx, 3.2, 1.55, 1.05, wobble=0.1, seed=_seed), color="black")
        _ax.text(_cx - 1.95, 4.3, _name, fontsize=13)
        _R, _B = blob(_cx - 0.4, 3.2, 0.68, 0.55, seed=_seed + 10), blob(_cx + 0.5, 3.1, 0.68, 0.6, seed=_seed + 20)
        _X, _Y = np.meshgrid(_cx - 1.5 + 3.0 * _g, 2.2 + 2.0 * _g)
        _pts = np.column_stack([_X.ravel(), _Y.ravel()])
        _in = _Path(np.column_stack(_R)).contains_points(_pts) & _Path(np.column_stack(_B)).contains_points(_pts)
        _ax.contourf(_X, _Y, _in.reshape(_X.shape).astype(float), levels=[0.5, 1.5], colors=[LIGHT], alpha=0.9)
        _ax.plot(*_R, color=RED)
        _ax.plot(*_B, color=BLUE)
    _ax.text(1.3, 3.2, "$U$", color=RED, fontsize=12, ha="center", va="center")
    _ax.text(2.5, 3.95, "$f^{-1}(A)$", color=BLUE, fontsize=11, ha="center", va="center")
    _ax.text(7.3, 3.2, "$f(U)$", color=RED, fontsize=11, ha="center", va="center")
    _ax.text(8.8, 3.1, "$A$", color=BLUE, fontsize=12, ha="center", va="center")
    arrow(_ax, (3.9, 3.3), (6.1, 3.3), "black", connectionstyle="arc3,rad=-0.2")
    _ax.text(5.0, 3.75, "$f$", fontsize=13, ha="center")
    for _x0, _col in ((1.0, RED), (7.0, BLUE)):
        _ax.plot([_x0, _x0 + 1.6, _x0 + 1.6, _x0, _x0], [0.3, 0.3, 1.6, 1.6, 0.3], color=_col)
        _ax.text(_x0 + 0.8, -0.05, r"$\mathbb{R}^m$" if _col == RED else r"$\mathbb{R}^n$", fontsize=12, ha="center", va="top")
    _ax.fill([1.9, 2.6, 2.6, 1.8], [0.3, 0.3, 1.6, 1.6], color=LIGHT, alpha=0.9, lw=0)
    _ax.fill([7.0, 7.7, 7.8, 7.0], [0.3, 0.3, 1.6, 1.6], color=LIGHT, alpha=0.9, lw=0)
    arrow(_ax, (1.3, 2.5), (1.5, 1.7), RED, connectionstyle="arc3,rad=0.3")
    _ax.text(0.7, 2.0, r"$\varphi$", color=RED, fontsize=12)
    arrow(_ax, (8.6, 2.5), (8.4, 1.7), BLUE, connectionstyle="arc3,rad=-0.3")
    _ax.text(9.0, 2.0, r"$\psi$", color=BLUE, fontsize=12)
    arrow(_ax, (2.8, 0.9), (6.8, 0.9), "black")
    _ax.text(4.8, 1.05, r"$\psi \circ f \circ \varphi^{-1}$", fontsize=12, ha="center", va="bottom")
    _ax.text(2.7, 1.75, r"$\varphi(U \cap f^{-1}(A))$", color=GREY, fontsize=11, ha="center")
    _ax.text(7.4, 1.75, r"$\psi(f(U) \cap A)$", color=GREY, fontsize=11, ha="center")
    _ = None  # no cell output: the figures are returned, not displayed here
    return fig_angles, fig_smooth


@app.cell(hide_code=True)
def _(mo):
    s_phi = mo.ui.slider(5, 175, 1, value=60, label=r"$\phi$", show_value=True)
    s_theta = mo.ui.slider(1, 359, 1, value=40, label=r"$\theta$", show_value=True)
    return s_phi, s_theta


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, GREY, math, mo, np, s_phi, s_theta):
    _ph, _th = math.radians(s_phi.value), math.radians(s_theta.value)
    _x, _y, _z = math.sin(_ph) * math.cos(_th), math.sin(_ph) * math.sin(_th), math.cos(_ph)
    _u, _v = _x / (1 - _z), _y / (1 - _z)
    _ut, _vt = _x / (1 + _z), _y / (1 + _z)

    _r = 1 / math.tan(_ph / 2)  # radius of the constant-phi circle in the north chart; 1/r in the south chart
    _fig = Figure(figsize=(FULL, 3.0), layout="constrained")
    _axes = _fig.subplots(1, 3)
    _a = np.linspace(0, 2 * np.pi, 200)
    for _ax, _pt, _title, _lim in (
        (_axes[0], (math.degrees(_ph), math.degrees(_th)), r"$\psi(p) = (\phi, \theta)$", None),
        (_axes[1], (_u, _v), r"$\varphi_n(p) = (u, v)$", max(2.0, 1.3 * _r)),
        (_axes[2], (_ut, _vt), r"$\varphi_s(p) = (\tilde{u}, \tilde{v})$", max(2.0, 1.2 / _r)),
    ):
        _ax.set_title(_title, fontsize=12)
        if _lim is None:
            _ax.set_xlim(0, 180)
            _ax.set_ylim(0, 360)
            _ax.set_xlabel(r"$\phi$")
            _ax.set_ylabel(r"$\theta$", rotation=0, labelpad=12)
            _ax.set_xticks([0, 90, 180], [r"$0\degree$", r"$90\degree$", r"$180\degree$"])
            _ax.set_yticks([0, 180, 360], [r"$0\degree$", r"$180\degree$", r"$360\degree$"])
        else:
            _ax.set_xlim(-_lim, _lim)
            _ax.set_ylim(-_lim, _lim)
            _ax.set_aspect("equal")
            _ax.axhline(0, color="black", lw=0.6)
            _ax.axvline(0, color="black", lw=0.6)
            _ax.plot(np.cos(_a), np.sin(_a), color=GREY, lw=0.8)
            _tk = math.floor(10 * _lim) / 10  # a tick inside the axis
            _ax.set_xticks([-_tk, 0, _tk])
            _ax.set_yticks([-_tk, 0, _tk])
            for _axis in (_ax.xaxis, _ax.yaxis):
                _axis.set_major_formatter(lambda _t, _i: f"${_t:.1f}$")
        _ax.plot(*_pt, "o", color=BLUE, ms=6, clip_on=False, zorder=3)
    # the curve of constant phi in the three charts
    _axes[1].plot(_r * np.cos(_a), _r * np.sin(_a), color=GREEN, lw=1.0)
    _axes[2].plot(np.cos(_a) / _r, np.sin(_a) / _r, color=GREEN, lw=1.0)
    _axes[0].plot([s_phi.value, s_phi.value], [0, 360], color=GREEN, lw=1.0)
    _axes[2].annotate("equator", (0, 1), textcoords="offset points", xytext=(3, 2), color=GREY, fontsize=10, ha="left", va="bottom")  # offset in points: stays next to the circle at any zoom
    if _r > 0.3:  # label the constant-phi circle only when it is visible beyond the point marker
        _axes[1].annotate(r"$\phi$ = const", (0, -_r), textcoords="offset points", xytext=(4, -3), color=GREEN, fontsize=10, ha="left", va="top")

    mo.vstack([mo.hstack([s_phi, s_theta], justify="start", gap=3, wrap=True), _fig])
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, HALF, RED, arrow, blank, definition, fig_smooth, mo, np):
    _fig, _ax = blank(HALF, 2.8, (-1.7, 1.9), (-1.4, 1.5))
    _t = np.linspace(-1.3, 1.3, 100)
    _ax.plot(_t + 0.35 * _t**2, _t - 0.35 * _t**2, color=BLUE)
    _ax.plot(_t - 0.45 * _t**2, _t + 0.45 * _t**2, color=RED)
    _ax.plot(_t, _t, color=GREY)
    arrow(_ax, (0, 0), (0.55, 0.55), GREEN)
    _ax.plot(0, 0, "o", color="black", ms=4)
    _ax.text(0.15, -0.3, "$p$", fontsize=13)
    _ax.text(0.2, 0.75, "$v$", color=GREEN, fontsize=13)
    _ax.text(1.35, 1.2, "$p + tv$", color=GREY, fontsize=12)
    _ax.text(1.5, 0.45, r"$\gamma(t)$", color=BLUE, fontsize=12)
    _ax.text(-0.1, 1.25, r"$\sigma(t)$", color=RED, fontsize=12)

    mo.vstack(
        [
            mo.md(r"### Smooth maps"),
            definition(
                r"""
    Given two manifolds $(M^m, \mathcal{A})$ and $(N^n, \mathcal{B})$ we can define smooth maps from $M$ to $N$ using their charts: $f : M \longrightarrow N$ is called **smooth** (or differentiable) (or continuous) (or any adjective) if for any choices of charts

    $$
    \varphi : U \subseteq M \longrightarrow V \subseteq \mathbb{R}^m, \qquad \psi : A \subseteq N \longrightarrow B \subseteq \mathbb{R}^n
    $$

    the local representation of $f$ in those charts

    $$
    \psi \circ f \circ \varphi^{-1} : \varphi(U \cap f^{-1}(A)) \longrightarrow \psi(f(U) \cap A)
    $$

    ($\varphi(U \cap f^{-1}(A)) \subseteq \mathbb{R}^m$, &nbsp; $\psi(f(U) \cap A) \subseteq \mathbb{R}^n$)

    is smooth (or differentiable) (or continuous) (or any adjective)
    """,
                "Smooth map",
            ),
            fig_smooth,
            mo.md(
                r"""
    ### Tangent vectors

    To define the notion of derivatives of smooth functions, we need a notion of “directions” on manifolds &nbsp; <span class="nw">$\leadsto$ &nbsp; tangent vectors</span>

    On affine spaces $(\mathbb{A}, \mathbb{V}, -)$, $(\mathbb{B}, \mathbb{W}, -)$, given $p \in \mathbb{A}$ and $v \in \mathbb{V}$ and $f : \mathbb{A} \longrightarrow \mathbb{B}$ &nbsp; <span class="nw">$\leadsto$ &nbsp; derivative</span> of $f$ at $p$ in the direction of $v$

    $$
    \begin{aligned}
    Df_p(v) &= \lim_{t \to 0} \frac{f(p + tv) - f(p)}{t} && (\text{using affine structure}) \\[4pt]
    &= \lim_{t \to 0} \frac{f(\gamma(t)) - f(p)}{t} && (\text{using curves on } \mathbb{A})
    \end{aligned}
    $$

    for *any* curve $\gamma : \mathbb{R} \longrightarrow \mathbb{A}$ such that

    $$
    \begin{cases} \gamma(0) = p \in \mathbb{A} \\ \gamma'(0) = v \in \mathbb{V} \end{cases} \qquad \left( \gamma'(0) = \lim_{s \to 0} \frac{\gamma(s) - \gamma(0)}{s} \right)
    $$
    """
            ),
            mo.md(r"From the point of view of $Df_p(v)$ all paths through $p$ with velocity $v$ can be used equivalently"),
            _fig,
            mo.md(
                r"""
    On a manifold $(M, \mathcal{A})$

    - no immediate notion of vectors
    - but we can also consider paths through points
    - we will *define* vectors on $M$ as equivalence classes of paths with “same velocity” in charts
    """
            ),
            definition(
                r"""
    $M$ $m$-manifold, $p \in M$, a **tangent vector** to $M$ at $p$ is an equivalence class of smooth paths on $M$

    $$
    v_p = [\gamma]_p = \left\{\, \sigma : \mathbb{R} \longrightarrow M \mid \begin{matrix} \sigma(0) = \gamma(0) = p \ \text{ and} \\ (\varphi \circ \sigma)'(0) = (\varphi \circ \gamma)'(0) \end{matrix} \,\right\}
    $$

    (for any chart $\varphi : U \subseteq M \longrightarrow V \subseteq \mathbb{R}^m$ with $p \in U$)
    """,
                "Tangent vector",
            ),
            mo.md(
                r"""
    In other words, two smooth paths $\gamma, \sigma$ are considered equivalent if in <span class="nw">a chart $\varphi$</span>

    $$
    \begin{cases}
    (\varphi \circ \gamma)(0) = (\varphi \circ \sigma)(0) & \leadsto \qquad \gamma(0) = \sigma(0) = p \\
    (\varphi \circ \gamma)'(0) = (\varphi \circ \sigma)'(0) & \leadsto \qquad \text{“} \gamma'(0) = \sigma'(0) = v \text{”}
    \end{cases}
    $$

    **Remark.** If $\gamma \sim \sigma$ with respect to one chart then $\gamma \sim \sigma$ with respect to any other

    <span class="chain">$\displaystyle \psi \circ \gamma(t) = \underbrace{\psi \circ \varphi^{-1}}_{\mathclap{\footnotesize \begin{matrix} \text{change of} \\ \text{coordinates} \end{matrix}}} \circ\, \varphi \circ \gamma(t)$ $\displaystyle \Longrightarrow \quad (\psi \circ \gamma)'(t) = \smash[b]{\underbrace{D(\psi \circ \varphi^{-1})_{\varphi \circ \gamma(t)}}_{\footnotesize \text{Jacobian matrix}}} \big( (\varphi \circ \gamma)'(t) \big)$</span>

    $\Longrightarrow$ &nbsp; $[\gamma]_p$ is defined independently of the choice of charts
    """
            ),
            definition(
                r"""
    We denote by

    <span class="chain">$\displaystyle T_p M = \text{set of tangent vectors to } M \text{ at } p$ $\displaystyle = \textbf{Tangent space} \text{ to } M \text{ at } p$</span>
    """,
                "Tangent space",
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
