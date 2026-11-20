import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 • Lecture 02 • Galilean geometry", css_file="phy309.css")


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
def _(GREY, LIGHT, np, patch):
    # ---- 3D figures of this lecture: coordinates (x^1, x^2, time) -------
    K = "#000000"
    O3 = (0.0, 0.0, 0.0)

    def flat_plane(corners, fill=LIGHT, edge=GREY, alpha=0.6, lw=1.0):
        """A flat parallelogram (surface, cut fine so that arrows lying in it sort right) and its edge (a closed line)."""
        c = np.array(corners + [corners[0]], float)
        return patch(corners, fill, alpha, n=24), (c[:, 0], c[:, 1], c[:, 2], edge, lw)

    def curve(v, k, s):
        """The curve s -> s v + s^2 k (v, k in (x^1, x^2, time))."""
        c = s[:, None] * np.asarray(v, float) + (s**2)[:, None] * np.asarray(k, float)
        return c[:, 0], c[:, 1], c[:, 2]

    return K, O3, curve, flat_plane


@app.cell(hide_code=True)
def _(header):
    header("Lecture 02", "Week 01", "Lecture 02 • Galilean geometry")
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, arrow, blank):
    # Static sketches from the handwritten notes (time runs upwards, one spatial direction drawn)

    # Inertial frame: e0 future unit vector, e_i, e_j spatial orthonormal, coordinates of p
    fig_frame, _ax = blank(3.4, 3.0, (-1.4, 2.6), (-1.1, 2.3))
    _f = lambda x, y, z: (y - 0.5 * x, z - 0.45 * x)
    for _tip, _name, _col, _off in (((2.0, 0, 0), r"$\vec{e}_i$", "black", (2, -14)), ((0, 2.2, 0), r"$\vec{e}_j$", "black", (4, -4)), ((0, 0, 2.0), r"$\vec{e}_0$", "black", (6, -4))):
        arrow(_ax, (0, 0), _f(*_tip), _col)
        _ax.annotate(_name, _f(*_tip), textcoords="offset points", xytext=_off, color=_col, fontsize=13)
    _p = (1.0, 1.4, 1.5)
    for _a, _b in (((1.0, 0, 0), (1.0, 1.4, 0)), ((0, 1.4, 0), (1.0, 1.4, 0)), ((1.0, 1.4, 0), _p), ((0, 0, 1.5), _p)):
        _ax.plot(*zip(_f(*_a), _f(*_b)), "--", color=GREEN, lw=1.0)
    arrow(_ax, (0, 0), _f(*_p), BLUE)
    _ax.plot(*_f(*_p), "o", color="black", ms=4)
    _ax.annotate("$p$", _f(*_p), textcoords="offset points", xytext=(6, 2), fontsize=13)
    _ax.plot(0, 0, "o", color="black", ms=4)
    _ax.annotate("$o$", (0, 0), textcoords="offset points", xytext=(-14, -2), fontsize=13)
    for _q, _n, _off in (((1.0, 0, 0), "$x^i$", (-20, 2)), ((0, 1.4, 0), "$x^j$", (-4, 6)), ((0, 0, 1.5), "$t$", (-14, -2))):
        _ax.annotate(_n, _f(*_q), textcoords="offset points", xytext=_off, color=GREEN, fontsize=12)

    _ = None  # no cell output: the figures are returned, not displayed here

    return (fig_frame,)


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, K, flat_plane, np, panel, turntable):
    # Newtonian gravity: sigma at rest (the vertical line), gamma on a circular orbit around it (a helix, speed
    # 0.85 < 1, so steeper than 45 degrees); the slice S_gamma(t) through gamma(t) and the force arrow from
    # gamma(t) to sigma(t) in it, stopping just short of sigma(t)
    _t = np.linspace(-1.0, 1.45, 170)  # below the slice only as much as above it
    _c = (0.85 * np.sin(_t), 0.85 * np.cos(_t), _t)
    _g0, _tip = (0.0, 0.85, 0.0), (0.0, 0.1, 0.0)
    _corners = [(1.4, -1.4, 0.0), (1.4, 1.4, 0.0), (-1.4, 1.4, 0.0), (-1.4, -1.4, 0.0)]  # wide enough that its back edge stays off the name gamma(t)
    _sf, _ln = flat_plane(_corners)
    fig_gravity = turntable(
        -30,
        22,
        "the particles gamma (an orbit, a helix) and sigma (at rest), the simultaneity slice through gamma(t), and the force arrow from gamma(t) to sigma(t) in it",
        [
            panel(
                1.0,
                surfaces=[_sf],
                lines=[_ln, ([0.0, 0.0], [0.0, 0.0], [-1.1, 1.65], K, 1.6), (*_c, BLUE, 1.6)],
                arrows=[(_g0, _tip, GREEN)],
                points=[((0.0, 0.0, 0.0), K, 3.4), (_g0, K, 3.4)],
                texts=[
                    ((0.0, 0.0, 0.0), r"\sigma(t)", K, 180, 7),
                    (_g0, r"\gamma(t)", K, 10, 7),
                    ((0.0, 0.0, 1.65), r"\sigma", K, 90, 4),
                    ((_c[0][-1], _c[1][-1], _c[2][-1]), r"\gamma", BLUE, 0, 6),
                    (_corners[0], r"S_{\gamma(t)}", GREY, -150, 8),
                ],
            )
        ],
        height=380,
        width=460,
        bias=0.12,
    )
    return (fig_gravity,)


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, K, O3, RED, curve, flat_plane, np, panel, turntable):
    # Relative velocity of gamma_2 with respect to gamma_1: both velocities, v twice, the plane ker(tau) through the event
    _g1, _g2 = np.array([0.1, -0.5, 1.0]), np.array([-0.25, 0.75, 1.0])
    _s = np.linspace(-0.35, 0.8, 50)  # short below the event; above it, up to just below the tips
    _c1 = curve(_g1, (0.05, -0.18, 0), _s)
    _c2 = curve(_g2, (-0.06, 0.15, 0), _s)
    _right = np.array([-np.sin(np.radians(-30)), np.cos(np.radians(-30)), 0.0])  # to the right on the screen, in the first view
    # each name beside the top end of its curve, on the outer side in the first view
    _e1 = np.array(curve(_g1, (0.05, -0.18, 0), np.array([0.5]))).ravel() - 0.1 * _right
    _e2 = np.array(curve(_g2, (-0.06, 0.15, 0), np.array([0.5]))).ravel() + 0.1 * _right
    _v = _g2 - _g1
    _gap = 0.03 / np.linalg.norm(_v)  # a small gap at both ends of the relative velocity, clear of the heads of the velocities
    _sf, _ln = flat_plane([(0.8, -1.1, 0.0), (0.8, 1.6, 0.0), (-0.8, 1.6, 0.0), (-0.8, -1.1, 0.0)])
    fig_relvel = turntable(
        -30,
        22,
        "two particles through one event, their velocities and the relative velocity",
        [
            panel(
                1.0,
                surfaces=[_sf],
                lines=[(*_c1, BLUE, 1.6), (*_c2, RED, 1.6), _ln],
                arrows=[(O3, tuple(_g1), K), (O3, tuple(_g2), K), (tuple(_g1 + _gap * _v), tuple(_g2 - _gap * _v), GREEN), (O3, tuple(_v), GREEN)],
                points=[(O3, K, 3.4)],
                texts=[
                    (tuple(_e1), r"\gamma_1", BLUE, None, 0),
                    (tuple(_e2), r"\gamma_2", RED, None, 0),
                    (tuple(0.82 * _g1), r"\gamma_1'", K, 0, 8),
                    (tuple(0.82 * _g2), r"\gamma_2'", K, 180, 8),
                    (tuple(1.04 * _v), r"\vec{v}(\gamma_1, \gamma_2)", GREEN, -45, 9),
                    ((0.8, -1.1, 0.0), r"\ker(\tau)", GREY, -150, 8),
                ],
            )
        ],
        height=360,
        width=460,
        bias=0.12,
    )
    return (fig_relvel,)


@app.cell(hide_code=True)
def _(BLUE, GREEN, K, O3, ORANGE, RED, curve, np, panel, turntable):
    # Velocity addition for three particles through one event: spatial speeds below 1, so every curve is steeper
    # than 45 degrees; the curves end below the tips, as on the page; the three relative velocities form a triangle,
    # the two summands in green, their sum in purple; each relative velocity leaves a small gap at both ends,
    # so that it does not touch the heads of the velocities; every label sits in space beside its own object
    # (no offset on the screen), so that it stays there when the figure is turned
    _vel = {"g": np.array([0.2, -0.6, 1.0]), "s": np.array([-0.5, 0.15, 1.0]), "x": np.array([0.45, 0.4, 1.0])}
    _bend = {"g": (0.05, -0.1, 0), "s": (-0.08, 0.1, 0), "x": (0.1, 0.06, 0)}
    _col = {"g": BLUE, "s": RED, "x": ORANGE}
    _nm = {"g": r"\gamma", "s": r"\sigma", "x": r"\xi"}
    _PURPLE = "#7a5c8f"
    _s = np.linspace(-0.35, 0.8, 50)  # short below the event; above it, up to just below the tips
    _mid = sum(_vel.values()) / 3  # the centre of the triangle of the tips
    _AZ = -30
    _right = np.array([-np.sin(np.radians(_AZ)), np.cos(np.radians(_AZ)), 0.0])  # to the right on the screen, in the first view
    _side = {"g": -1, "s": -1, "x": 1}  # each velocity's label on the outer side of its arrow in the first view
    _nside = {"g": -1, "s": 1, "x": 1}  # each name beside the top end of its curve, where there is room in the first view
    _lines, _texts = [], []
    for _k in "gsx":
        _c = curve(_vel[_k], _bend[_k], _s)
        _lines.append((*_c, _col[_k], 1.6))
        _texts.append((tuple(np.array(curve(_vel[_k], _bend[_k], np.array([0.5]))).ravel() + 0.1 * _nside[_k] * _right), _nm[_k], _col[_k], None, 0))

    def _short(a, b, gap=0.03):
        _t = gap / np.linalg.norm(b - a)
        return (tuple(a + _t * (b - a)), tuple(a + (1 - _t) * (b - a)))

    _arrows = [(O3, tuple(_vel[_q]), K) for _q in "gsx"]
    _arrows += [(*_short(_vel["g"], _vel["s"]), GREEN), (*_short(_vel["s"], _vel["x"]), GREEN), (*_short(_vel["g"], _vel["x"]), _PURPLE)]
    _texts += [
        (tuple(0.8 * _vel["g"] + 0.09 * _side["g"] * _right), r"\gamma'", K, None, 0),
        (tuple(0.8 * _vel["s"] + 0.09 * _side["s"] * _right), r"\sigma'", K, None, 0),
        (tuple(0.8 * _vel["x"] + 0.09 * _side["x"] * _right), r"\xi'", K, None, 0),
    ]
    for _a, _b, _tex, _c in (("g", "s", r"\vec{v}(\gamma, \sigma)", GREEN), ("s", "x", r"\vec{v}(\sigma, \xi)", GREEN), ("g", "x", r"\vec{v}(\gamma, \xi)", _PURPLE)):
        _m = (_vel[_a] + _vel[_b]) / 2
        _d = _m - _mid  # from the centre of the triangle out through the middle of the edge
        _texts.append((tuple(_m + 0.13 * _d / np.linalg.norm(_d)), _tex, _c, None, 0))
    fig_addition = turntable(
        _AZ,
        25,
        "three particles through one event, their velocities and the three relative velocities forming a triangle",
        [panel(1.0, surfaces=[], lines=_lines, arrows=_arrows, points=[(O3, K, 3.4)], texts=_texts)],
        height=300,
        width=460,
        bias=0.12,
    )
    return (fig_addition,)


@app.cell(hide_code=True)
def _(BLUE, GREY, RED, arrow, blank, definition, mo):
    _fig, _ax = blank(5.0, 2.4, (-0.5, 5.2), (-0.9, 1.7))
    arrow(_ax, (0, 0), (0.5, 1.4), BLUE)
    arrow(_ax, (0, 0), (1.3, 0), GREY)
    arrow(_ax, (0, 0), (0.8, -0.5), RED)
    _ax.text(0.45, 1.5, "future", color=BLUE, fontsize=12, ha="center")
    _ax.text(1.4, -0.05, "spatial / simultaneous", color=GREY, fontsize=12)
    _ax.text(0.85, -0.8, "past", color=RED, fontsize=12, ha="center")
    _ax.text(-0.3, -0.25, "$p$", fontsize=13)
    _ax.plot(0, 0, "o", color="black", ms=4)
    arrow(_ax, (3.4, 0.9), (4.2, 0.9), "black", connectionstyle="arc3,rad=-0.3")
    _ax.text(3.75, 1.2, r"$\tau$", fontsize=13)
    _ax.plot([4.7, 4.7], [-0.8, 1.6], color="black")
    for _y, _col, _name in ((1.4, BLUE, "$> 0$"), (0, GREY, "$0$"), (-0.5, RED, "$< 0$")):
        _ax.plot(4.7, _y, "o", color=_col, ms=4)
        _ax.text(4.85, _y, _name, fontsize=12, va="center")

    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    - Euclidean space $\mathbb{E}^3$ = affine space $(\mathbb{A}, \mathbb{V}, -)$ + Euclidean inner product $\langle\ ,\ \rangle$ <br>$-$ &nbsp;$\leadsto$&nbsp; difference between points = displacement vector, &nbsp; <span class="nw">$\langle\ ,\ \rangle$ &nbsp;$\leadsto$&nbsp; measurements</span>
    - a choice of origin $o \in \mathbb{E}^3$ and orthonormal basis $\vec{e}_1, \vec{e}_2, \vec{e}_3 \in \mathbb{V}$ &nbsp; <span class="nw">$\Longrightarrow$ &nbsp; usual</span> Cartesian coordinates

    **In this lecture:** the same construction for spacetime: Galilean spacetime and Newtonian mechanics

    **References:** Schutz 1.1; Carroll 1.2; Sasane 12.1, 13.1–13.2

    ## I.2 &nbsp; Galilean geometry

    The geometry of spacetime in Newtonian physics

    **Spacetime** = set of all *events* (locations in space + moments in time)

    **Mechanics** = study of the origins of $\underbrace{\textit{motion}}_{\footnotesize \mathclap{\begin{matrix} \text{relations between events} \\ = \text{geometry of spacetime} \end{matrix}}\rule[-0.35em]{0pt}{0pt}}$
    """
            ),
            definition(
                r"""
    The **Galilean spacetime** is a 4-dimensional affine space

    <span class="chain">$\displaystyle \mathbb{G}^4 = (\mathbb{A}, \mathbb{V}, -)$ $\displaystyle \qquad \begin{array}{l} (\text{assumptions (i), (ii), (iii)} \\ \quad \text{as before, with } \dim \mathbb{V} = 4) \end{array}$</span>

    together with $\underbrace{\textit{some extra structure}}_{\footnotesize \mathclap{\text{different assumptions needed}}\rule[-0.35em]{0pt}{0pt}}$
    """,
                "Galilean spacetime",
            ),
            mo.md(
                r"""
    ### The universal time function

    **(iv)** there exists a function $\tau : \mathbb{V} \longrightarrow \mathbb{R}$

    - linear: &nbsp; $\tau(a\vec{u} + b\vec{v}) = a\, \tau(\vec{u}) + b\, \tau(\vec{v})$
    - non-zero: &nbsp; $\exists\, \vec{u} \in \mathbb{V}$ with $\tau(\vec{u}) \neq 0$

    We can define the $\underbrace{\textit{time length}}_{\footnotesize \mathclap{\text{not necessarily positive}}\rule[-0.35em]{0pt}{0pt}}$ of vectors $\tau(\vec{u})$ and the *time distance* between events $t(p, q) = \tau(q - p)$ (from $p$ to $q$)
    """
            ),
            definition(
                r"""
    - $\vec{u}$ **future oriented** if $\tau(\vec{u}) > 0$ &nbsp; <span class="nw">$\leadsto$ &nbsp; $q$ in</span> future of $p$ if $\tau(q - p) > 0$
    - $\vec{u}$ **past oriented** if $\tau(\vec{u}) < 0$ &nbsp; <span class="nw">$\leadsto$ &nbsp; $q$ in</span> past of $p$ if $\tau(q - p) < 0$
    - $\vec{u}$ **spatial** if $\tau(\vec{u}) = 0$ &nbsp; <span class="nw">$\leadsto$ &nbsp; $p$ and</span> $q$ are simultaneous if $\tau(q - p) = 0$
    """,
                r"Basic causal structure in $\mathbb{G}^4$",
            ),
            _fig,
            mo.md(
                r"""
    ### The spatial inner product

    **(iv′)** there is a Euclidean inner-product on $\ker \tau$ &nbsp; ($\dim = 3$!)

    $$
    \langle\ ,\ \rangle : \ker \tau \times \ker \tau \longrightarrow \mathbb{R}
    $$

    We can define spatial length

    $$
    \text{if } \tau(\vec{u}) = 0 \qquad \Longrightarrow \qquad \lVert \vec{u} \rVert = \sqrt{\langle \vec{u}, \vec{u} \rangle}
    $$

    Each set of mutually simultaneous events in $\mathbb{G}^4$ is an identical copy of $\mathbb{E}^3$

    $$
    S_p = \{\, q \in \mathbb{G}^4 \mid \tau(q - p) = 0 \,\} = p + \ker \tau \approx \mathbb{E}^3
    $$
    """
            ),
            definition(
                r"""
    $\mathbb{G}^4 = (\mathbb{A}, \mathbb{V}, -)$ 4-dimensional affine space together with a universal time function $\tau$ and a spatial inner product $\langle\ ,\ \rangle$ on $\ker \tau$
    """,
                "Galilean spacetime",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, fig_frame, fig_relvel, mo, proposition, theorem):
    mo.vstack(
        [
            mo.md(r"### Inertial frames"),
            theorem(
                r"""
    Choosing $\underbrace{o}_{\footnotesize \mathclap{\text{origin}}\rule[-0.35em]{0pt}{0pt}} \in \mathbb{G}^4$ and $\underbrace{\vec{e}_0, \vec{e}_1, \vec{e}_2, \vec{e}_3}_{\footnotesize \mathclap{\text{inertial frame}}\rule[-0.35em]{0pt}{0pt}} \in \mathbb{V}$ such that

    $$
    \begin{aligned}
    & \tau(\vec{e}_0) = 1 && \text{unit future oriented} \\
    & \tau(\vec{e}_i) = 0, \quad i = 1, 2, 3 \\
    & \langle \vec{e}_i, \vec{e}_j \rangle = \delta_{ij} = \begin{cases} 1 & i = j \\ 0 & i \neq j \end{cases} && \text{spatial orthonormal basis}
    \end{aligned}
    $$

    $\Longrightarrow$ &nbsp; Cartesian coordinates $x^\mu : \mathbb{G}^4 \longrightarrow \mathbb{R}$, &nbsp; $\mu = 0, \underbrace{1, 2, 3}_{\footnotesize i\rule[-0.35em]{0pt}{0pt}}$

    $$
    x^0(p) = \tau(p - o), \qquad x^i(p) = \langle \vec{e}_i,\ p - o - x^0(p)\, \vec{e}_0 \rangle
    $$

    $\Longrightarrow$ &nbsp; identification $\mathbb{R}^4 \approx \mathbb{G}^4$

    $$
    (t, x, y, z) \longleftrightarrow p = o + t\vec{e}_0 + x\vec{e}_1 + y\vec{e}_2 + z\vec{e}_3
    $$
    """,
                "Cartesian coordinates",
            ),
            fig_frame,
            mo.md(
                r"""
    $$
    \text{then} \quad \tau(t, x, y, z) = t, \qquad \lVert (0, x, y, z) \rVert = \sqrt{x^2 + y^2 + z^2}
    $$

    ### Kinematics and dynamics
    """
            ),
            definition(
                r"""
    A **particle** in $\mathbb{G}^4$ is a parameterized curve

    $$
    \gamma : \mathbb{R} \longrightarrow \mathbb{G}^4, \qquad s \longmapsto \gamma(s)
    $$

    such that

    $$
    \gamma'(s) = \lim_{\varepsilon \to 0} \frac{\gamma(s + \varepsilon) - \gamma(s)}{\varepsilon} \in \mathbb{V}
    $$

    is future oriented: &nbsp; $\tau(\gamma'(s)) > 0 \quad \forall\, s$ &nbsp; <span class="nw">$\gamma$ &nbsp;$\leadsto$&nbsp; all events</span> in the particle's history!
    """,
                "Particle",
            ),
            mo.md(
                r"""
    We can now study $\underbrace{\text{dynamics}}_{\footnotesize \mathclap{\begin{matrix} \text{change of position} \\ \text{as function of time} \end{matrix}}\rule[-0.35em]{0pt}{0pt}}$ as the slope of a $\underbrace{\textit{curve in spacetime}}_{\footnotesize \mathclap{\text{the history of events}}\rule[-0.35em]{0pt}{0pt}}$

    **Remark.** $\gamma'(s)$ is not the particle's velocity

    - it is a 4-dimensional vector…
    - $s$ in $\gamma(s)$ is not related to physical time (without other assumptions)
    """
            ),
            proposition(
                r"""
    Every particle can be parameterized by an “absolute time” parameter $t$ such that

    $$
    \tau(\gamma(t_2) - \gamma(t_1)) = t_2 - t_1
    $$
    """,
                "Absolute time",
            ),
            mo.md(
                r"""
    **Proof** (idea). Up to solving some ODE we can always change parameterization so that $\tau(\gamma'(t)) = 1$

    $$
    \begin{aligned}
    \Longrightarrow \quad t_2 - t_1 &= \int_{t_1}^{t_2} dt = \int_{t_1}^{t_2} \tau(\gamma'(t))\, dt \\[8pt]
    &= \tau\!\left( \int_{t_1}^{t_2} \gamma'(t)\, dt \right) = \tau(\gamma(t_2) - \gamma(t_1)) \\[8pt]
    &\square
    \end{aligned}
    $$

    We can now measure time. How do we define $\underbrace{\textit{spatial velocity}}_{\footnotesize \mathclap{\begin{matrix} \text{not possible with} \\ \text{a single particle!} \end{matrix}}\rule[-0.35em]{0pt}{0pt}}$?
    """
            ),
            definition(
                r"""
    Given two particles $\gamma_1, \gamma_2$ (with $\tau(\gamma_1') = \tau(\gamma_2') = 1$) the **relative velocity** of $\gamma_2$ with respect to $\gamma_1$ is the spatial vector

    $$
    \vec{v}(\gamma_1, \gamma_2) = \gamma_2' - \gamma_1' \in \ker(\tau)
    $$
    """,
                "Relative velocity",
            ),
            fig_relvel,
            definition(
                r"""
    The $\underbrace{\textbf{absolute acceleration}}_{\footnotesize \mathclap{\begin{matrix} \text{does not require} \\ \text{other reference} \end{matrix}}\rule[-0.35em]{0pt}{0pt}}$ of a particle $\gamma$ &nbsp; ($\tau(\gamma') = 1$) is the spatial vector

    $$
    \vec{a}(\gamma) = \gamma'' \in \ker(\tau) \qquad \left( \tau(\gamma'') = \frac{d}{dt} \tau(\gamma') = 0 \right)
    $$
    """,
                "Absolute acceleration",
            ),
            mo.md(
                r"""
    **Remark** (Newton's first and second laws). In the absence of external forces, a particle's history is a *straight future oriented line*

    $$
    \gamma(t) = p + t\vec{u}, \qquad \tau(\vec{u}) = 1
    $$

    (solution of $\gamma''(t) = \vec{0}$, $\gamma(0) = p$, $\gamma'(0) = \vec{u}$; &nbsp; inertial particle / inertial observer)

    Deviation from inertial motion is determined by

    $$
    \gamma''(t) = \frac{1}{m} \vec{F}(t), \qquad \text{where } m \in \mathbb{R}_+ \ (\text{mass}), \quad \vec{F}(t) \in \ker(\tau) \ (\text{Force})
    $$

    (system of second order ODEs)

    In Cartesian coordinates (choice of origin and inertial frame)

    $$
    \gamma''(t) = \begin{bmatrix} t \\ x(t) \\ y(t) \\ z(t) \end{bmatrix}'' = \begin{bmatrix} 0 \\ x''(t) \\ y''(t) \\ z''(t) \end{bmatrix} = \frac{1}{m} \begin{bmatrix} 0 \\ F^x(t) \\ F^y(t) \\ F^z(t) \end{bmatrix}
    $$

    **Example.** constant force: &nbsp; $\vec{F}(t) = \vec{v} \in \ker(\tau)$ &nbsp; <span class="nw">$\Longrightarrow$ &nbsp; $\gamma(t) = p + t\vec{u} + \dfrac{1}{2m} t^2 \vec{v}$</span>
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    u_x = mo.ui.slider(-1.5, 1.5, 0.1, value=0, label="spatial part of $\\vec{u}$", show_value=False)
    f_m = mo.ui.slider(0, 1.5, 0.05, value=0.75, label="$\\vec{v} / m$", show_value=False)
    return f_m, u_x


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, K, O3, ORANGE, f_m, flat_plane, mo, np, panel, turntable, u_x):
    # u = (spatial part, 0, 1): its spatial part along x^1; v/m = (0, v/m, 0) along x^2
    _u, _a = u_x.value, f_m.value
    _t = np.linspace(-0.4, 1.3, 90)  # only a short way below p
    _x1, _x2 = _u * _t, 0.5 * _a * _t**2
    _sf, _ln = flat_plane([(2.0, -0.6, 0), (2.0, 2.6, 0), (-2.0, 2.6, 0), (-2.0, -0.6, 0)])
    _tl = np.array([-0.65, 1.65])  # the line p + t u, a little beyond the curve at both ends
    _lines = [_ln, (_u * _tl, 0 * _tl, _tl, GREY, 1.2, [5, 4], -0.2), (_x1, _x2, _t, BLUE, 1.6)]
    _arrows = [(O3, (_u, 0.0, 1.0), GREEN)]
    _texts = [
        ((_x1[-1], _x2[-1], 1.3), r"\gamma", BLUE, 90, 4),
        ((_u, 0.0, 1.0), r"\vec{u}", GREEN, 180, 6),
        (O3, "p", K, -135, 6),
        ((2.0, 2.6, 0), r"S_p", GREY, 0, 5),
        ((1.45 * _u, 0.0, 1.45), r"p + t\vec{u}", GREY, 180, 6),
    ]
    if _a > 0:
        _arrows.append((O3, (0.0, _a, 0.0), ORANGE))
        _texts.append(((0.0, _a + 0.08, 0.0), r"\vec{v} / m", ORANGE, -20, 2))
    _fig = turntable(
        -30,
        18,
        "the worldline of a particle under a constant force, with u, v/m, the plane S_p and the line p + t u",
        [panel(1.3, surfaces=[_sf], lines=_lines, arrows=_arrows, points=[(O3, K, 3.4)], texts=_texts, box=((-2.0, 2.0), (-0.6, 1.8), (-0.65, 1.65)))],
        height=400,
        width=460,
        key="force",
        apart=True,
        bias=0.15,
    )

    mo.vstack([mo.hstack([u_x, f_m], justify="start", gap=3, wrap=True), _fig])
    return


@app.cell(hide_code=True)
def _(frame):
    frame("force", 400)
    return


@app.cell(hide_code=True)
def _(fig_addition, fig_gravity, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ### Newtonian gravity and Maxwell's electrodynamics

    Newtonian gravity:

    $$
    \vec{F}(t) = -G m M\, \frac{\gamma(t) - \sigma(t)}{\lVert \gamma(t) - \sigma(t) \rVert^3} \in \ker(\tau) \qquad (\gamma(t), \sigma(t) \text{ simultaneous})
    $$

    $S_{\gamma(t)}$ = space of simultaneity of $\gamma(t)$ $\approx \mathbb{E}^3$
    """
            ),
            fig_gravity,
            mo.md(
                r"""
    Coulomb's law of electrostatics can be written almost identically exchanging masses and charges!

    Maxwell's electrodynamics breaks down: in Cartesian coordinates we want something like

    $$
    \vec{F}(t) = q \left( \vec{E}_{\sigma(t)} + \vec{v}_{\gamma(t)} \times \vec{B}_{\sigma(t)} \right) \qquad (\text{Lorentz force law})
    $$

    - $\vec{E}_{\sigma(t)}$ &nbsp;$\leadsto$&nbsp; electric field generated by $\sigma$, depends on the inertial frame
    - $\vec{v}_{\gamma(t)}$ &nbsp;$\leadsto$&nbsp; velocity of $\gamma$ relative to the inertial frame
    - $\vec{B}_{\sigma(t)}$ &nbsp;$\leadsto$&nbsp; magnetic field generated by $\sigma$, depends on the inertial frame

    with

    <span class="chain">$\displaystyle \begin{aligned} \vec{\nabla} \cdot \vec{E}_{\sigma(t)} &= \frac{\rho_{\sigma(t)}}{\varepsilon_0}, & \qquad \vec{\nabla} \cdot \vec{B}_{\sigma(t)} &= 0 \\[14pt] \vec{\nabla} \times \vec{E}_{\sigma(t)} + \partial_t \vec{B}_{\sigma(t)} &= 0, & \qquad \vec{\nabla} \times \vec{B}_{\sigma(t)} - \frac{1}{c^2} \partial_t \vec{E}_{\sigma(t)} &= \mu_0\, \vec{J}_{\sigma(t)} \end{aligned}$ $\displaystyle \qquad (\text{Maxwell's Equations})$</span>

    (depend on the choice of *inertial frame*: not an intrinsic physical structure)

    **Remark.** In the vacuum, Maxwell implies the wave equation

    <span class="chain">$\displaystyle \begin{cases} \vec{\nabla} \cdot \vec{E} = 0, \quad \vec{\nabla} \times \vec{B} - \dfrac{1}{c^2} \partial_t \vec{E} = 0 \\[10pt] \vec{\nabla} \cdot \vec{B} = 0, \quad \vec{\nabla} \times \vec{E} + \partial_t \vec{B} = 0 \end{cases}$ $\displaystyle \Longrightarrow \quad \begin{cases} \left( \Delta - \dfrac{1}{c^2} \partial_t^2 \right) \vec{E} = 0 \\[10pt] \left( \Delta - \dfrac{1}{c^2} \partial_t^2 \right) \vec{B} = 0 \end{cases}$</span>

    $\Longrightarrow$ &nbsp; electromagnetic “waves” propagate at constant speed $c$ (the speed of light)

    Experimentally $c$ is *independent* of the choice of inertial frames &nbsp; <span class="nw">$\Longrightarrow$ &nbsp; the speed</span> of light relative to any inertial particle is *always constant* &nbsp; (not possible in Galilean spacetime)!
    """
            ),
            theorem(
                r"""
    Given $\gamma, \sigma, \xi$ three particles in $\mathbb{G}^4$

    $$
    \vec{v}(\gamma, \xi) = \vec{v}(\gamma, \sigma) + \vec{v}(\sigma, \xi)
    $$
    """,
                "Addition of relative velocities",
            ),
            fig_addition,
            mo.md(
                r"""
    <span class="chain">$\displaystyle \text{triangle inequality}$ $\displaystyle \Longrightarrow \quad \lVert \vec{v}(\gamma, \xi) \rVert \leq \lVert \vec{v}(\gamma, \sigma) \rVert + \lVert \vec{v}(\sigma, \xi) \rVert$</span>

    with equality if and only if one of the two vectors is a non-negative multiple of the other: &nbsp; <span class="nw">$\vec{v}(\sigma, \xi) = \lambda\, \vec{v}(\gamma, \sigma)$, &nbsp; $\lambda \geq 0$</span>

    $\gamma, \sigma$ are inertial particles and $\xi$ is a light particle moving along same direction &nbsp; <span class="nw">$\Longrightarrow$ &nbsp; $c = \lVert \vec{v}(\gamma, \sigma) \rVert + c$</span>

    Contradiction unless $\gamma, \sigma$ have zero relative velocity
    """
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
