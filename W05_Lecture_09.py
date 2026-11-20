import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 • Lecture 09 • The derivative", css_file="phy309.css")


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
      #g { position: relative; flex: 1 1 300px; min-width: 240px; max-width: var(--maxw); display: grid;
           grid-template-columns: repeat(var(--cols), minmax(0, 1fr)); gap: 6px 14px; touch-action: none; cursor: grab;
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
    <div id="o"><div id="g" role="img"><div id="hint">&#10227;</div></div><div id="lg"></div></div>
    <script>
    // the scene is not in this page but in an element of the notebook beside the frame (or, for a figure with a slider,
    // in the slider's cell), which a slider changes: the page then redraws in place and the frame is never rebuilt
    const box = window.frameElement.closest(".bs3d"), P = window.parent.document;
    const find = () => box.querySelector("[data-scene]") || P.querySelector('[data-bs3d="' + window.frameElement.dataset.bs3d + '"]');
    // a picture beside the frame that moves with the same slider: the slider's cell has it hidden (data-pic="key"), and
    // it is copied into its place beside the frame (data-side="key"); later only its data changes, so marimo redraws it in place
    function pic() {
      const k = window.frameElement.dataset.bs3d, a = k && P.querySelector('[data-pic="' + k + '"] > *'),
            b = k && P.querySelector('[data-side="' + k + '"]');
      if (!a || !b) return;
      const c = b.firstElementChild;
      if (!c || c.tagName !== a.tagName) b.replaceChildren(a.cloneNode(true));
      else for (const n of a.getAttributeNames()) if (c.getAttribute(n) !== a.getAttribute(n)) c.setAttribute(n, a.getAttribute(n));
    }
    (function start() { const h = find(); if (h) { pic(); main(h.dataset.scene); } else setTimeout(start, 50); })();
    function main(shown) {
      let S = JSON.parse(shown);
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
            const hx = c > 0.35 ? 0 : c < -0.35 ? -1 : -0.5, vy = s > 0.35 ? -100 : s < -0.35 ? 0 : -50;
            const w = l.el.offsetWidth, x = Math.max(2, Math.min(this.W - w - 2, X[l.i] + l.r * c + hx * w));  // a label near the edge stays inside the frame
            l.el.style.transform = `translate(${x}px, ${Y[l.i] - l.r * s}px) translate(0, ${vy}%)`;
          }
        }
      }

      const grid = document.getElementById("g"), out = document.getElementById("o");
      const lg = document.getElementById("lg");
      let scenes = [], Rmax = 0;
      function build() {  // the drawings and the legend of the scene S
        for (const s of scenes) s.box.remove();
        texs.length = 0;
        lg.replaceChildren();
        grid.style.setProperty("--maxw", S.maxw + "px");
        grid.style.setProperty("--cols", S.cols);
        grid.setAttribute("aria-label", S.alt);
        window.frameElement.title = S.alt;
        scenes = S.panels.map((p) => new Scene(p, grid));
        Rmax = Math.max(...scenes.map((s) => s.R));
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
      }
      build();

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
        document.fonts.ready.then(draw);  // label widths are final only once the formula fonts are in
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
      new MutationObserver(() => {
        pic();
        const h = find();
        if (!h || h.dataset.scene === shown) return;
        shown = h.dataset.scene;
        S = JSON.parse(shown);
        build();
        if (window.katex) window.typeset(); else { fit(); draw(); }
      }).observe(box.querySelector("[data-scene]") ? box : P.body, { subtree: true, childList: true, attributes: true, attributeFilter: ["data-scene"] });
    }
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

    def turntable(az, el, alt, panels, legend=(), height=360, width=None, cols=1, key=None, shared=True, bias=0.03, apart=False):
        """An interactive 3D figure of one or more `panels` (made by panel(), in `cols` columns), first seen
        from azimuth `az` and elevation `el` (degrees); each drawing at most `height` pixels high, all together
        at most `width` wide, with an optional legend box beside them (not used: names sit beside their objects). `key` names the view
        so that it survives a redraw; with `shared`, all panels have one scale.
        legend: (kind, colour, TeX[, line width / edge colour, dash / opacity]) with kind "dot", "ring", "line" or "area".
        apart: only the scene, for a figure with a slider, whose frame, frame(key, height), is shown by the next cell,
        so that moving the slider redraws the figure without rebuilding its frame."""
        scene = {"az": az, "el": el, "h": height, "bias": bias, "panels": list(panels), "legend": [], "key": key, "shared": shared,
                 "maxw": width or max(700, cols * height + (cols - 1) * 14), "cols": cols, "alt": alt}
        for e in legend:
            item = {"k": e[0], "c": e[1], "t": e[2]}
            if len(e) > 3:
                item["e" if e[0] == "area" else "w"] = e[3]
            if len(e) > 4:
                item["o" if e[0] == "area" else "d"] = e[4]
            scene["legend"].append(item)
        data = _html.escape(_json.dumps(scene, separators=(",", ":")))
        if apart:
            return mo.Html(f'<div hidden data-bs3d="{_html.escape(key)}" data-scene="{data}"></div>')
        return mo.Html(f'<div class="bs3d">{_frame(height)}<div hidden data-scene="{data}"></div></div>')

    def _frame(height, key=""):
        return f'<iframe srcdoc="{_html.escape(_PAGE)}" data-bs3d="{_html.escape(key)}" style="display: block; width: 100%; height: {height}px; border: 0;"></iframe>'

    def frame(key, height=360):
        """The frame of the figure turntable(..., key=key, height=height, apart=True) of the cell above."""
        return mo.Html(f'<div class="bs3d">{_frame(height, key)}</div>')

    return frame, panel, patch, sheet, turntable


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
    header("Lecture 09", "Week 05", "Lecture 09 • The derivative")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    - A manifold $(M, \mathcal{A})$: a set of points with an atlas of charts $\varphi : U \subseteq M \longrightarrow \varphi(U) \subseteq \mathbb{R}^m$, $\varphi(p) = x^\mu(p)\, e_\mu$, whose transition maps $\tilde{\varphi} \circ \varphi^{-1}$ are diffeomorphisms.
    - A change of coordinates $x \longmapsto \tilde{x}(x)$ has an invertible Jacobian $\dfrac{\partial \tilde{x}^\mu}{\partial x^\nu}$ on $\varphi(U \cap \tilde{U})$.
    - $f : M \longrightarrow N$ is smooth if every coordinate expression $\psi \circ f \circ \varphi^{-1}$, $x \longmapsto y^\alpha(x)\, e_\alpha$, is smooth.

    **In this lecture:** velocities of paths, the tangent space $T_pM$, and the derivative $Df_p$ of a smooth map.

    **References:** Carroll 2.3; Sasane 2.2–2.5
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## II.4 &nbsp; The derivative

    ### Derivative in affine spaces

    Suppose $M$ and $N$ are affine spaces

    $$
    M = (\mathbb{A}^m, \mathbb{V}^m, -), \qquad N = (\mathbb{B}^n, \mathbb{W}^n, -)
    $$

    Given a map $f : \mathbb{A} \longrightarrow \mathbb{B}$, $x \in \mathbb{A}$ and $v \in \mathbb{V}$, the **directional derivative**

    $$
    Df_x(v) = \lim_{t \to 0} \frac{f(x + tv) - f(x)}{t} \in \mathbb{W}
    $$

    uses the affine structure both on $\mathbb{A}$ (to form $x + tv$) and on $\mathbb{B}$ (to form the difference and the limit). The map $f$ is **differentiable** at $x$ if

    - $Df_x : \mathbb{V} \longrightarrow \mathbb{W}$ is linear, and
    - $\displaystyle \lim_{t \to 0} \frac{f(\gamma(t)) - f(\gamma(0))}{t} = Df_x(v)$

    for every path $\gamma : \mathbb{R} \longrightarrow \mathbb{A}$ with

    $$
    \begin{cases} \gamma(0) = x \\[4pt] \gamma'(0) = \displaystyle \lim_{t \to 0} \frac{\gamma(t) - \gamma(0)}{t} = v \end{cases}
    $$

    This second condition still depends on the affine structures. Now we can compute $Df_x(v)$ as follows: pick a path $\gamma$ with $\gamma(0) = x$ and $\gamma'(0) = v$, consider $\sigma = f \circ \gamma : \mathbb{R} \longrightarrow \mathbb{B}$ and compute

    $$
    \sigma(0) = f(\gamma(0)) = f(x), \qquad \sigma'(0) = Df_{\gamma(0)}(\gamma'(0)) = Df_x(v)
    $$

    $\leadsto$ &nbsp; $f$ maps paths through $x$ to paths through $f(x)$, and $Df_x$ maps velocities at $x$ to velocities at $f(x)$. &nbsp; <span class="nw">$\leadsto$ &nbsp; we</span> can use this observation to generalize the derivative to maps between manifolds.

    ### Same velocity
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            definition(
                r"""
    Let $M$ be an $m$-manifold. Two smooth paths $\gamma, \tilde{\gamma} : \mathbb{R} \longrightarrow M$ with $\gamma(0) = \tilde{\gamma}(0) = p$ have the **same velocity** at $p$ if for some chart $\varphi : U \subseteq M \longrightarrow \varphi(U) \subseteq \mathbb{R}^m$ with $p \in U$

    $$
    (\varphi \circ \gamma)'(0) = (\varphi \circ \tilde{\gamma})'(0) \in \mathbb{R}^m
    $$
    """,
                "Same velocity",
            ),
            mo.md(
                r"""
    **Remark.** If $\gamma, \tilde{\gamma}$ have the same velocity in one chart, they have the same velocity in every chart containing $p$ (the example below shows why).

    **Remark.** The condition $(\varphi \circ \gamma)'(0) = (\varphi \circ \tilde{\gamma})'(0)$ defines an equivalence relation on the smooth paths through $p = \gamma(0) = \tilde{\gamma}(0)$.
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"""### The tangent space"""),
            definition(
                r"""
    Let $M$ be an $m$-manifold and $p \in M$. The **tangent space** of $M$ at $p$ is the set of all equivalence classes of smooth paths through $p$

    $$
    T_p M = \{\, [\gamma] \mid \gamma : \mathbb{R} \longrightarrow M,\ \gamma(0) = p \,\}
    $$

    where $[\gamma]$ is the equivalence class of $\gamma$ (all paths with the same velocity at $p$).
    """,
                "Tangent space",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** &nbsp; $\mathbb{S}^2 = \{\, (x, y, z) \in \mathbb{R}^3 \mid x^2 + y^2 + z^2 = 1 \,\}$

    <span class="chain">$\displaystyle (u, v) = \varphi_n(x, y, z) = \left( \frac{x}{1 - z},\ \frac{y}{1 - z} \right), \qquad (x, y, z) \neq (0, 0, 1)$ $\displaystyle \leadsto \quad \varphi_n^{-1}(u, v) = \left( \frac{2u}{1 + u^2 + v^2},\ \frac{2v}{1 + u^2 + v^2},\ \frac{-1 + u^2 + v^2}{1 + u^2 + v^2} \right)$</span>

    <span class="chain">$\displaystyle (\tilde{u}, \tilde{v}) = \varphi_s(x, y, z) = \left( \frac{x}{1 + z},\ \frac{y}{1 + z} \right), \qquad (x, y, z) \neq (0, 0, -1)$ $\displaystyle \leadsto \quad \varphi_s^{-1}(\tilde{u}, \tilde{v}) = \left( \frac{2\tilde{u}}{1 + \tilde{u}^2 + \tilde{v}^2},\ \frac{2\tilde{v}}{1 + \tilde{u}^2 + \tilde{v}^2},\ \frac{1 - \tilde{u}^2 - \tilde{v}^2}{1 + \tilde{u}^2 + \tilde{v}^2} \right)$</span>

    Given $\gamma : \mathbb{R} \longrightarrow \mathbb{S}^2$, $\gamma(t) = (x(t), y(t), z(t))$, with $\gamma(0) = p \neq n$, the velocity is computed in the chart, not on $\mathbb{S}^2$:

    $$
    \varphi_n \circ \gamma : \mathbb{R} \longrightarrow \mathbb{R}^2, \qquad \varphi_n \circ \gamma(t) = (u(t), v(t))
    $$

    $$
    (\varphi_n \circ \gamma)'(0) = \begin{bmatrix} u'(0) \\ v'(0) \end{bmatrix} = \begin{bmatrix} a \\ b \end{bmatrix} \in \mathbb{R}^2
    $$

    Another path $\tilde{\gamma} : \mathbb{R} \longrightarrow \mathbb{S}^2$ is equivalent to $\gamma$ if

    $$
    \tilde{\gamma}(0) = \gamma(0) = p \qquad \text{and} \qquad (\varphi_n \circ \tilde{\gamma})'(0) = \begin{bmatrix} a \\ b \end{bmatrix} \in \mathbb{R}^2
    $$

    If $(\varphi_n \circ \gamma)'(0) = (\varphi_n \circ \tilde{\gamma})'(0)$, then $(\varphi_s \circ \gamma)'(0) = (\varphi_s \circ \tilde{\gamma})'(0)$:

    $$
    (\tilde{u}(t), \tilde{v}(t)) = \left( \frac{u(t)}{u(t)^2 + v(t)^2},\ \frac{v(t)}{u(t)^2 + v(t)^2} \right)
    $$

    $$
    \begin{bmatrix} \tilde{a} \\ \tilde{b} \end{bmatrix} = \begin{bmatrix} \tilde{u}' \\ \tilde{v}' \end{bmatrix} = \frac{1}{(u^2 + v^2)^2} \underbrace{\begin{bmatrix} v^2 - u^2 & -2uv \\ -2uv & u^2 - v^2 \end{bmatrix}}_{\mathclap{\footnotesize \begin{matrix} \text{only depends on} \\ p = \gamma(0) = \tilde{\gamma}(0) \end{matrix}}} \begin{bmatrix} a \\ b \end{bmatrix}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, ORANGE, SPHERE_EDGE, np, panel, patch, sphere, turntable):
    # a path gamma through p, its images in the charts phi_n and phi_s on the plane z = 0, and their velocities
    _u0, _v0, _a, _b = 1.2, 0.6, 0.6, 0.8
    _t = np.linspace(-0.6, 0.6, 121)
    _u, _v = _u0 + _t * _a - 0.5 * _t**2 * _b, _v0 + _t * _b + 0.5 * _t**2 * _a
    _q, _r2 = _u**2 + _v**2, _u0**2 + _v0**2
    _path = (2 * _u / (1 + _q), 2 * _v / (1 + _q), (_q - 1) / (1 + _q))
    _P = np.array([2 * _u0 / (1 + _r2), 2 * _v0 / (1 + _r2), (_r2 - 1) / (1 + _r2)])
    _Un, _Us = np.array([_u0, _v0, 0.0]), np.array([_u0 / _r2, _v0 / _r2, 0.0])
    _vn = np.array([_a, _b, 0.0])
    _vs = np.array([(_v0**2 - _u0**2) * _a - 2 * _u0 * _v0 * _b, -2 * _u0 * _v0 * _a + (_u0**2 - _v0**2) * _b, 0.0]) / _r2**2
    _n, _s = np.array([0.0, 0.0, 1.0]), np.array([0.0, 0.0, -1.0])
    _plane = [(-1.3, -1.3, 0), (1.9, -1.3, 0), (1.9, 1.6, 0), (-1.3, 1.6, 0)]
    _edge = np.array(_plane + _plane[:1])
    _k = np.linspace(0, 1, 40)[:, None]

    def _seg(a, b):
        return tuple((a + _k * (b - a)).T)

    turntable(
        -60,
        24,
        "the unit sphere and the plane z = 0, with a path through p, its images through the charts phi_n and phi_s, and their velocity vectors",
        [
            panel(
                1.0,
                surfaces=[sphere(alpha=0.45), patch(_plane, "#e8e8e8", 0.6, n=16)],
                outlines=[SPHERE_EDGE],
                lines=[
                    (*_edge.T, GREY, 1.2),
                    (np.cos(np.linspace(0, 2 * np.pi, 121)), np.sin(np.linspace(0, 2 * np.pi, 121)), np.zeros(121), "#000000", 1.0),
                    (*_seg(_n, _Un), GREY, 1.4),
                    (*_seg(_s, _P), GREY, 1.4),
                    (*_path, BLUE, 1.8),
                    (_u, _v, 0 * _t, BLUE, 1.4),
                    (_u / _q, _v / _q, 0 * _t, BLUE, 1.4),
                ],
                arrows=[(tuple(_Un), tuple(_Un + 0.6 * _vn), GREEN), (tuple(_Us), tuple(_Us + 0.6 * _vs), ORANGE)],
                points=[(tuple(_n), "#000000", 3.4), (tuple(_s), "#000000", 3.4), (tuple(_P), "#000000", 3.4), (tuple(_Un), "#000000", 3.4), (tuple(_Us), "#000000", 3.4)],
                texts=[
                    (tuple(_n), "n", "#000000", 90),
                    (tuple(_s), "s", "#000000", -90),
                    (tuple(_P), "p", "#000000", 60, 8),
                    (tuple(_Un + 0.18 * np.array([0.8, -0.6, 0.0])), r"\varphi_n(p)", "#000000", -90, 2),
                    (tuple(_Us), r"\varphi_s(p)", "#000000", 108, 9),
                    (tuple(_Un + 0.6 * _vn), r"(\varphi_n \circ \gamma)'(0) = \begin{bmatrix} a \\ b \end{bmatrix}", GREEN, 80, 56),
                    (tuple(_Us + 0.6 * _vs), r"(\varphi_s \circ \gamma)'(0) = \begin{bmatrix} \tilde{a} \\ \tilde{b} \end{bmatrix}", ORANGE, 180, 6),
                ],
            )
        ],
        height=460,
        bias=0.12,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    s_u = mo.ui.slider(0.9, 2.0, 0.1, value=1.2, label="$u(0)$", show_value=True)
    s_v = mo.ui.slider(-1.0, 1.0, 0.1, value=0.6, label="$v(0)$", show_value=True)
    s_a = mo.ui.slider(-1.0, 1.0, 0.1, value=0.6, label="$a$", show_value=True)
    s_b = mo.ui.slider(-1.0, 1.0, 0.1, value=0.8, label="$b$", show_value=True)
    return s_a, s_b, s_u, s_v


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, GREY, RED, arrow, mo, np, s_a, s_b, s_u, s_v):
    _u, _v, _a, _b = s_u.value, s_v.value, s_a.value, s_b.value
    _r2 = _u**2 + _v**2
    if _r2 == 0:
        _out = mo.md(r"need $(u(0), v(0)) \neq (0, 0)$ &nbsp; ($p = s$ is not in the chart $\varphi_s$)")
    else:
        _ut, _vt = _u / _r2, _v / _r2
        _at = ((_v**2 - _u**2) * _a - 2 * _u * _v * _b) / _r2**2 + 0.0
        _bt = (-2 * _u * _v * _a + (_u**2 - _v**2) * _b) / _r2**2 + 0.0
        _t = np.linspace(-1.0, 1.0, 300)
        # two paths with the same velocity in the chart phi_n
        _g = (_u + _t * _a, _v + _t * _b)
        _h = (_u + _t * _a - 0.5 * _t**2 * _b, _v + _t * _b + 0.5 * _t**2 * _a)

        _Ls = max(1.6, 1.5 * max(abs(_ut), abs(_vt)))  # south panel follows its point
        _k = min(1.0, 0.6 * _Ls / max(np.hypot(_at, _bt), 1e-9))  # one arrow scale for both panels, so the south arrow fits
        _Ls = max(_Ls, 1.15 * max(abs(_ut + _k * _at), abs(_vt + _k * _bt)))
        _Ln = max(1.6, 1.3 * max(np.abs(np.concatenate([*_g, *_h])).max(), abs(_u + _k * _a), abs(_v + _k * _b)))  # north panel fits its paths and arrow
        _fig = Figure(figsize=(5.6, 3.0), layout="constrained")
        _axes = _fig.subplots(1, 2)
        _c = np.linspace(0, 2 * np.pi, 200)
        for _ax, _title, _L in zip(_axes, (r"$\varphi_n = (u, v)$", r"$\varphi_s = (\tilde{u}, \tilde{v})$"), (_Ln, _Ls)):
            _ax.set_title(_title, fontsize=13)
            _ax.set_xlim(-_L, _L)
            _ax.set_ylim(-_L, _L)
            _ax.set_aspect("equal")
            _ax.axhline(0, color="black", lw=0.6)
            _ax.axvline(0, color="black", lw=0.6)
            _ax.plot(np.cos(_c), np.sin(_c), color=GREY, lw=0.8)
            _ax.text(-0.74, -0.74, "equator", color=GREY, fontsize=10, ha="right", va="top")
            _ax.set_xticks([-round(_L, 1), 0, round(_L, 1)])
            _ax.set_yticks([-round(_L, 1), 0, round(_L, 1)])
        for (_pu, _pv), _col, _name in ((_g, BLUE, r"$\gamma$"), (_h, RED, r"$\tilde{\gamma}$")):
            _axes[0].plot(_pu, _pv, color=_col)
            _du, _dv = _pu[-1] - _pu[-2], _pv[-1] - _pv[-2]
            _n = np.hypot(_du, _dv) or 1.0
            _axes[0].annotate(_name, (_pu[-1], _pv[-1]), textcoords="offset points", xytext=(9 * _du / _n, 9 * _dv / _n), ha="center", va="center", color=_col, fontsize=12)
            _q = _pu**2 + _pv**2
            _q = np.where(_q < 1e-6, np.nan, _q)  # the path image passes through infinity where it crosses s
            _axes[1].plot(_pu / _q, _pv / _q, color=_col)
        arrow(_axes[0], (_u, _v), (_u + _k * _a, _v + _k * _b), GREEN)
        arrow(_axes[1], (_ut, _vt), (_ut + _k * _at, _vt + _k * _bt), GREEN)
        if _k < 1:
            for _ax in _axes:
                _ax.text(0.03, 0.03, "arrows drawn at\n" + rf"${_k:.2g}\times$ length", transform=_ax.transAxes, color=GREEN, fontsize=10)
        _axes[0].plot(_u, _v, "o", color="black", ms=5)
        _axes[1].plot(_ut, _vt, "o", color="black", ms=5)
        _out = _fig
    mo.vstack([mo.hstack([s_u, s_v, s_a, s_b], justify="start", gap=2, wrap=True), _out])
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, RED, arrow, blob, definition, mo, np):
    _fig = Figure(figsize=(6.0, 1.8), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-2.9, 10.3)
    _ax.set_ylim(-1.6, 1.8)
    _ax.set_aspect("equal")
    _ax.axis("off")
    _c = np.linspace(0, 2 * np.pi, 200)
    _t = np.linspace(-1.0, 1.0, 100)
    for _x0, _name, _lab in ((0.0, "$M$", "$p$"), (7.2, "$N$", "$f(p)$")):
        _ax.plot(*blob(_x0, 0.0, 2.45 if _x0 == 0 else 2.75, 1.3, wobble=0.1, seed=6 if _x0 == 0 else 7), color="black")
        _ax.plot(_x0 + _t, 0.2 - 0.35 * _t**2, color=BLUE)
        _ax.plot(_x0 + _t, 0.2 - 1.1 * _t**2, color=RED)
        arrow(_ax, (_x0, 0.2), (_x0 + 0.7, 0.2), GREEN)
        _ax.plot(_x0, 0.2, "o", color="black", ms=4.5)
        _ax.text(_x0 - 2.3, 1.3, _name, fontsize=14, ha="right")
        _ax.text(_x0 - 0.1, 0.4, _lab, fontsize=12, ha="right")
    _ax.text(0.1, 0.5, r"$[\gamma] = [\tilde{\gamma}]$", color=GREEN, fontsize=11)
    _ax.text(1.1, -0.25, r"$\gamma$", color=BLUE, fontsize=12)
    _ax.text(0.2, -0.85, r"$\tilde{\gamma}$", color=RED, fontsize=12)
    _ax.text(7.3, 0.5, r"$[f \circ \gamma] = [f \circ \tilde{\gamma}]$", color=GREEN, fontsize=11)
    _ax.text(8.3, -0.25, r"$f \circ \gamma$", color=BLUE, fontsize=12)
    _ax.text(6.9, -0.95, r"$f \circ \tilde{\gamma}$", color=RED, fontsize=12)
    arrow(_ax, (3.0, -0.1), (4.2, -0.1), "black")
    _ax.text(3.6, -0.55, "$f$", fontsize=13, ha="center")
    arrow(_ax, (3.0, 0.9), (4.2, 0.9), GREEN)
    _ax.text(3.6, 1.1, "$Df_p$", fontsize=13, ha="center", color=GREEN)

    mo.vstack(
        [
            mo.md(
                r"""
    **Remark.** Every $\begin{bmatrix} a \\ b \end{bmatrix} \in \mathbb{R}^2$ is the velocity of some path through $p$ in the chart $\varphi_n$:

    <span class="chain">$\displaystyle \gamma(t) = \varphi_n^{-1}\big( u(0) + t a,\ v(0) + t b \big)$ $\displaystyle \Longrightarrow \quad (\varphi_n \circ \gamma)'(0) = \begin{bmatrix} a \\ b \end{bmatrix}$ $\displaystyle \qquad \therefore \quad T_p \mathbb{S}^2 \approx \mathbb{R}^2 \quad \text{as a vector space (later)}$</span>

    ### Derivative of a smooth map
    """
            ),
            definition(
                r"""
    The **derivative** of a smooth map $f : M \longrightarrow N$ at $p \in M$ is the map

    $$
    Df_p : T_p M \longrightarrow T_{f(p)} N, \qquad [\gamma] \longmapsto Df_p[\gamma] = [f \circ \gamma]
    $$

    It maps the velocity $[\gamma]$ at $p$ to the velocity $[f \circ \gamma]$ at $f(p)$.
    """,
                "Derivative",
            ),
            _fig,
            mo.md(
                r"""
    **Remark.** For a smooth function $f : M \longrightarrow \mathbb{R}$, $p \in M$ and $[\gamma] \in T_p M$

    $$
    Df_p[\gamma] = [f \circ \gamma]  \mathrel{\text{“}{=}\text{”}} (f \circ \gamma)'(0)
    $$

    since two functions $h, \tilde{h} : \mathbb{R} \longrightarrow \mathbb{R}$ have the same velocity at $0$ if and only if $h'(0) = \tilde{h}'(0) \in \mathbb{R}$, and the class $[h]$ is identified with that number.
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Example: the height function

    **Example.** &nbsp; On $\mathbb{S}^2 = \{\, (x, y, z) \in \mathbb{R}^3 \mid x^2 + y^2 + z^2 = 1 \,\}$ consider the height function and the point

    $$
    f : \mathbb{S}^2 \longrightarrow \mathbb{R}, \qquad f(x, y, z) = z, \qquad p = (1, 0, 0) \in \mathbb{S}^2
    $$

    and two paths through $p$, the equator $\gamma$ and the meridian $\sigma$

    $$
    \begin{aligned}
    \gamma : \mathbb{R} \longrightarrow \mathbb{S}^2, \qquad \gamma(t) &= \varphi_n^{-1}\big( \cos(t),\ \sin(t) \big) = \big( \cos(t),\ \sin(t),\ 0 \big) \\[6pt]
    \sigma : \mathbb{R} \longrightarrow \mathbb{S}^2, \qquad \sigma(t) &= \varphi_n^{-1}\!\left( \frac{\cos(t)}{1 - \sin(t)},\ 0 \right) = \big( \cos(t),\ 0,\ \sin(t) \big)
    \end{aligned}
    $$

    <span class="chain">$\displaystyle Df_p[\gamma] = [f \circ \gamma] = [\, 0 : \mathbb{R} \to \mathbb{R} \,]$ $\displaystyle  \mathrel{\text{“}{=}\text{”}} \frac{d}{dt}\bigg|_{t=0} f \circ \gamma(t) = 0$</span>

    is the class of the zero function (all functions with zero derivative at $t = 0$), while

    <span class="chain">$\displaystyle Df_p[\sigma] = [f \circ \sigma] = [\, \sin : \mathbb{R} \to \mathbb{R} \,]$ $\displaystyle  \mathrel{\text{“}{=}\text{”}} \frac{d}{dt}\bigg|_{t=0} f \circ \sigma(t)$ $\displaystyle = \frac{d}{dt}\bigg|_{t=0} \sin(t) = 1$</span>

    is the class of functions with derivative $1$ at $t = 0$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    s_t = mo.ui.slider(-1.5, 1.5, 0.05, value=0.5, label="$t$", show_value=False)
    return (s_t,)


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, GREY, HALF, ORANGE, RED, SPHERE_EDGE, math, mo, np, panel, patch, s_t, sphere, turntable):
    _t = s_t.value
    _c = np.linspace(0, 2 * np.pi, 241)
    _plane = [(-1.25, -1.25, 0), (1.25, -1.25, 0), (1.25, 1.25, 0), (-1.25, 1.25, 0)]
    _edge = np.array(_plane + _plane[:1])
    _sph = turntable(
        -30,
        16,
        "the unit sphere and the plane z = 0, with the equator gamma and the meridian sigma through p, their velocity vectors at p, and the points gamma(t) and sigma(t)",
        [
            panel(
                1.0,
                surfaces=[sphere(alpha=0.45), patch(_plane, "#e8e8e8", 0.6, n=16)],
                outlines=[SPHERE_EDGE],
                lines=[(*_edge.T, GREY, 1.2), (np.cos(_c), np.sin(_c), 0 * _c, BLUE, 1.6), (np.cos(_c), 0 * _c, np.sin(_c), RED, 1.6)],
                arrows=[((1, 0, 0), (1, 0.75, 0), GREEN), ((1, 0, 0), (1, 0, 0.75), ORANGE)],
                points=[((1, 0, 0), "#000000", 3.4), ((0, 0, 1), "#000000", 3.4), ((0, 0, -1), "#000000", 3.4), ((0, 0, 0), "#000000", 2.6), ((math.cos(_t), math.sin(_t), 0), BLUE, 5.0), ((math.cos(_t), 0, math.sin(_t)), RED, 5.0)],
                texts=[
                    ((1, 0, 0), "p", "#000000", -60, 8),
                    ((0, 0, 1), "n", "#000000", 90),
                    ((0, 0, -1), "s", "#000000", -90),
                    ((0, 0, 0), "o", "#000000", 150, 6),
                    ((1, 0.75, 0), r"[\gamma]", GREEN, 0, 6),
                    ((1, 0, 0.75), r"[\sigma]", ORANGE, 0, 6),
                    ((math.cos(-2.6), math.sin(-2.6), 0), r"\gamma", BLUE, 90, 6),
                    ((math.cos(2.1), 0, math.sin(2.1)), r"\sigma", RED, 150, 6),
                ],
            )
        ],
        height=380,
        key="phy309-l09-height",
        apart=True,
        bias=0.12,
    )

    _fig = Figure(figsize=(2.8, HALF), layout="constrained")
    _ax2 = _fig.subplots()
    _ax2.set_xlim(-2.25, 2.3)
    _ax2.set_ylim(-1.3, 1.6)
    _ax2.axis("off")
    _ax2.plot([0, 0], [-1.15, 1.15], color="black")
    for _y, _lab in ((1, "$f(n) = 1$"), (-1, "$f(s) = -1$")):
        _ax2.plot(0, _y, "o", color="black", ms=3.5)
        _ax2.text(0.25, _y - 0.05, _lab, fontsize=12)
    _ax2.plot(0, 0, "o", color=BLUE, ms=6)
    _ax2.plot(0, math.sin(_t), "o", color=RED, ms=6)
    _ax2.text(0.25, -0.05, r"$f(\gamma(t)) = 0 \ \ \forall t$", fontsize=12)
    _ax2.text(-0.25, math.sin(_t), r"$f(\sigma(t)) = \sin(t)$", fontsize=12, ha="right", va="center")
    _ax2.text(0, 1.35, r"$\mathbb{R}$", fontsize=13, ha="center")
    _hidden = mo.Html(f'{_sph.text}<div hidden data-pic="phy309-l09-height">{mo.as_html(_fig).text}</div>')

    mo.vstack(
        [
            mo.hstack([s_t], justify="start"),
            _hidden,
        ]
    )
    return


@app.cell(hide_code=True)
def _(frame, mo):
    mo.vstack(
        [
            mo.Html(
                '<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 0.5rem 1rem;">'
                f'<div style="flex: 1.6 1 300px; min-width: 260px;">{frame("phy309-l09-height", 380).text}</div>'
                '<div style="flex: 0 1 auto;" data-side="phy309-l09-height"></div></div>'
            ),
            mo.md(
                r"""
    In the chart $\varphi_n$ the two velocities are

    $$
    (\varphi_n \circ \gamma)'(0) = \begin{bmatrix} 0 \\ 1 \end{bmatrix}, \qquad (\varphi_n \circ \sigma)'(0) = \begin{bmatrix} 1 \\ 0 \end{bmatrix}
    $$

    **Remark.** Using the ambient space $\mathbb{R}^3$

    $$
    [\gamma]  \mathrel{\text{“}{=}\text{”}} \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix}, \qquad [\sigma]  \mathrel{\text{“}{=}\text{”}} \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}
    $$
    """
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
