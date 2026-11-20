import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 • Lecture 06 • The equivalence principle", css_file="phy309.css")


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
            const hx = c > 0.35 ? 0 : c < -0.35 ? -100 : -50, vy = s > 0.35 ? -100 : s < -0.35 ? 0 : -50;
            l.el.style.transform = `translate(${X[l.i] + l.r * c}px, ${Y[l.i] - l.r * s}px) translate(${hx}%, ${vy}%)`;
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
def _(header):
    header("Lecture 06", "Week 03", "Lecture 06 • The equivalence principle")
    return


@app.cell(hide_code=True)
def _(definition, mo, postulate, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    - relativistic dynamics: a particle $\sigma : \mathbb{R} \longrightarrow \mathbb{M}^4$ with mass $m > 0$ has 4&#8209;velocity $\sigma'$ and 4&#8209;acceleration $\sigma''$
    - relativistic equations of motion $m\, \sigma'' = \kappa\, F(\sigma, \sigma')$: a second order system of ODEs with coupling constant (charge) $\kappa$ and force rule $F$

    **In this lecture:** universality of free fall, Einstein's equivalence principle, and tidal effects

    **References:** Schutz 5.1; Carroll 2.1, 4.7

    ## II.1 &nbsp; The equivalence principle

    ### Universality of free fall

    **Remark.** For relativistic models of this type (e.g. Maxwell), given two particles $\sigma_1, \sigma_2$ with

    <span class="chain">$\displaystyle \begin{cases} \sigma_1(0) = \sigma_2(0) = p \\ \sigma_1'(0) = \sigma_2'(0) = v \end{cases}$ $\displaystyle \Longrightarrow \quad \sigma_2''(0) - \sigma_1''(0) = \left( \frac{\kappa_2}{m_2} - \frac{\kappa_1}{m_1} \right) F(p, v)$ $\displaystyle \Longrightarrow \quad \text{different histories}$</span>

    For gravity, however, $\underbrace{\textit{“charge”}}_{\footnotesize \mathclap{\begin{matrix} \text{gravitational} \\ \text{mass } \kappa_i \end{matrix}}\rule[-0.35em]{0pt}{0pt}} \textit{ = } \underbrace{\textit{mass}}_{\footnotesize \mathclap{\begin{matrix} \text{inertial} \\ \text{mass } m_i \end{matrix}}\rule[-0.35em]{0pt}{0pt}}$ &nbsp;$\leadsto$&nbsp; weak equivalence principle

    <span class="chain">$\displaystyle \Longrightarrow \quad \sigma_2''(0) - \sigma_1''(0) = \left( \frac{m_2}{m_2} - \frac{m_1}{m_1} \right) G(p, v) = 0$ $\displaystyle \qquad \begin{array}{l} (\text{independent of the specific} \\ \quad \text{model we would use for } G) \end{array}$ <br> $\displaystyle \Longrightarrow \quad \sigma_1(s) = \sigma_2(s) \quad \forall\, s \qquad (\text{by uniqueness of IVPs})$ <br> $\displaystyle \Longrightarrow \quad \text{gravity defines a special family of histories in spacetime!}$</span>
    """
            ),
            definition(
                r"""
    A **free-falling particle** is a particle subject to no non-gravitational forces
    """,
                "Free-falling particle",
            ),
            mo.md(
                r"""
    In principle defined via

    $$
    \begin{cases} \sigma'' = G(\sigma, \sigma') \\ \sigma(0) = p, \ \sigma'(0) = v \end{cases}
    $$

    for the given gravitational force, but *independent* of the particle's “internal structure” &nbsp; (“universality of free fall”)

    ### Einstein's thought experiment

    An observer releases a test particle and observes its evolution

    Consider $\gamma$ (the “observer”) and $\sigma$ (the “test particle”) two particles with

    $$
    \begin{cases} \sigma(0) = \gamma(0) = p \\ \sigma'(0) = \gamma'(0) = v \end{cases}
    $$

    <span class="chain">$\displaystyle \begin{aligned} \text{Suppose} \qquad m_\gamma \gamma'' &= m_\gamma G(\gamma, \gamma') + \ell_\gamma H(\gamma, \gamma') \\ m_\sigma \sigma'' &= m_\sigma G(\sigma, \sigma') + \kappa_\sigma F(\sigma, \sigma') \end{aligned}$</span>

    $$
    \begin{aligned}
    \Longrightarrow \quad a(\gamma, \sigma)(p) &= \sigma''(0) - \gamma''(0) \\[8pt]
    &= \frac{\kappa_\sigma}{m_\sigma} F(p, v) - \frac{\ell_\gamma}{m_\gamma} H(p, v)
    \end{aligned}
    $$

    <span class="chain">$\displaystyle \text{If } \gamma \text{ is free-falling, } H(\gamma, \gamma') = 0$ $\displaystyle \Longrightarrow \quad a(\gamma, \sigma)(p) = \frac{\kappa_\sigma}{m_\sigma} F(p, v)$</span>

    - same as for an inertial observer in $\mathbb{M}^4$
    - we cannot distinguish between free-falling and inertial motion from $\underbrace{\textit{local measurements}}_{\footnotesize \mathclap{\text{instantaneous}}\rule[-0.35em]{0pt}{0pt}}$

    ### Einstein's equivalence principle
    """
            ),
            postulate(
                r"""
    <span class="chain">$\displaystyle \smash[b]{\underbrace{\textit{Physics}}_{\mathclap{\footnotesize \text{local and non-gravitational}}}} \text{ in a free-falling lab}$ $\displaystyle = \text{Physics in an inertial lab}$</span>

    (extending the weak equivalence principle)
    """,
                "Einstein's equivalence principle",
            ),
            mo.md(
                r"""
    **Remark.** Einstein's equivalence principle is a physical postulate, not a mathematical theorem!

    We will take it as a new assumption about the *structure of spacetime*: the “gravitational force” is universal and not locally observable by any free-falling particle, so it cannot be seen as a force acting on particles but as a property of spacetime itself!

    ### Tidal effects

    Consider now neighboring free-falling particles $\gamma, \sigma$

    <span class="chain">$\displaystyle \gamma'' = G(\gamma, \gamma'), \qquad \sigma'' = G(\sigma, \sigma')$ $\displaystyle \quad \text{with } \sigma(0) = \gamma(0) + \delta, \ \ \sigma'(0) = \gamma'(0) = v \ \ \text{and } \delta \in v^\perp$</span>

    $$
    \begin{aligned}
    \Longrightarrow \quad a(\gamma, \sigma)(0) &= G(p + \delta, v) - G(p, v) \\[8pt]
    &= D_1 G(p, v)[\delta] + O(\lVert \delta \rVert^2) = \nu(\gamma, \sigma)'(0) \neq 0 \ \text{ in general}
    \end{aligned}
    $$

    Neighboring particles with zero initial relative velocity may start moving towards or away from each other <span class="nw">$\leadsto$ &nbsp; tidal effects</span>
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(np):
    # ---- Newtonian free fall towards a mass M at rest at the origin (lecture 2), in units with G M = 1 ----
    K = "#000000"

    def fall(q, s):
        """Free fall from rest at the point q = (x^1, x^2), at the times s: the force -(sigma - M) / ||sigma - M||^3 points
        along the ray from M, so the particle stays on that ray, at r = r0 cos^2(eta), s = sqrt(r0^3 / 2) (eta + sin(eta) cos(eta))."""
        q = np.asarray(q, float)
        r0 = float(np.hypot(*q))
        k = np.sqrt(r0**3 / 2)
        s = np.asarray(s, float)
        assert s.max() / k < np.pi / 2  # before it reaches M
        lo, hi = np.zeros_like(s), np.full_like(s, np.pi / 2)
        for _ in range(60):
            mid = (lo + hi) / 2
            big = mid + np.sin(mid) * np.cos(mid) > s / k
            hi, lo = np.where(big, mid, hi), np.where(big, lo, mid)
        r = r0 * np.cos((lo + hi) / 2) ** 2
        return q[0] / r0 * r, q[1] / r0 * r, s

    def base(x1, x2, colour, lines, surfaces, patch):
        """The plane t = 0 over [x1] x [x2], light, with its edge."""
        c = [(x1[0], x2[0], 0.0), (x1[1], x2[0], 0.0), (x1[1], x2[1], 0.0), (x1[0], x2[1], 0.0)]
        surfaces.append(patch(c, colour, 0.45, n=12))
        e = np.array(c + [c[0]])
        lines.append((e[:, 0], e[:, 1], e[:, 2], "#9a9a9a", 0.8))

    return K, base, fall

@app.cell(hide_code=True)
def _(mo):
    fallen = mo.ui.slider(1.0, 4.0, 0.5, value=4.0, label="$t$", show_value=False)
    return (fallen,)

@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, K, LIGHT, RED, base, fall, fallen, mo, np, panel, patch, turntable):
    _T = fallen.value
    _s = np.linspace(0, _T, 121)
    _d = np.array([0.0, 0.8])  # delta, the same for both pairs
    # gamma(0) of each pair: side by side (delta across the direction to M), one above the other (delta along it)
    _starts = [np.array([3.0, -0.4]), np.array([0.0, 2.6])]
    _lines, _surfaces, _arrows, _points, _texts = [], [], [], [], []
    base((-0.9, 3.9), (-0.9, 3.9), LIGHT, _lines, _surfaces, patch)
    _lines.append(((0.0, 0.0), (0.0, 0.0), (0.0, 4.0), K, 1.4))  # M at rest
    _points.append(((0.0, 0.0, 0.0), K, 2.6))
    _texts.append(((0.0, 0.0, 4.0), r"M", K, 90, 5))
    for _g0 in _starts:
        _pair = [(_g0, BLUE, r"\gamma"), (_g0 + _d, RED, r"\sigma")]
        _paths = [fall(_q, _s) for _q, _c, _n in _pair]
        _ends = [np.array([_x1[-1], _x2[-1]]) for _x1, _x2, _t in _paths]
        for _k, ((_q, _c, _n), (_x1, _x2, _t)) in enumerate(zip(_pair, _paths)):
            _lines.append(((_q[0], _q[0]), (_q[1], _q[1]), (0.0, _T), GREY, 1.0, [4, 3]))  # the inertial particle from the same start
            _lines.append((_x1, _x2, _t, _c, 1.8))
            _points += [((_q[0], _q[1], 0.0), _c, 3.0), ((_x1[-1], _x2[-1], _T), _c, 3.0)]
            _out = (_ends[_k] - _ends[1 - _k]) / np.linalg.norm(_ends[_k] - _ends[1 - _k])  # away from the other particle
            _texts.append(((_x1[-1] + 0.3 * _out[0], _x2[-1] + 0.3 * _out[1], _T), _n, _c, 90, 3))
        _arrows.append(((_g0[0], _g0[1], 0.0), (_g0[0] + _d[0], _g0[1] + _d[1], 0.0), GREEN, 1.4))
        _texts.append(((_g0[0] + _d[0] / 2, _g0[1] + _d[1] / 2, 0.0), r"\delta", GREEN, -90, 7))
    _fig = turntable(
        40,
        24,
        "two pairs of particles falling from rest towards the mass M: a pair side by side comes together, a pair one above the other moves apart; the dashed lines are inertial particles from the same starts",
        [panel(0.8, surfaces=_surfaces, lines=_lines, arrows=_arrows, points=_points, texts=_texts, box=((-0.9, 3.9), (-0.9, 3.9), (0.0, 4.0)))],
        height=340,
        width=560,
        key="tide1",
        apart=True,
        bias=0.12,
    )
    mo.vstack([mo.hstack([fallen], justify="start"), _fig])
    return


@app.cell(hide_code=True)
def _(frame):
    frame("tide1", 340)
    return

@app.cell(hide_code=True)
def _(mo, postulate):
    mo.md(r"""
    **Remark.** This is very different from inertial particles!

    For inertial particles $\gamma, \sigma$ in $\mathbb{M}^4$ (also in $\mathbb{G}^4$) with $\sigma(0) = \gamma(0) + \delta$, &nbsp; $\sigma'(0) = \gamma'(0) = v$, &nbsp; $\delta \in v^\perp$ &nbsp; ($\delta \in \ker \tau$)

    $$
    \Longrightarrow \qquad a(\gamma, \sigma)(0) = 0 = \nu(\gamma, \sigma)'(0)
    $$

    Particles that start moving in the same direction remain parallel forever!

    In the presence of gravity, spacetime has a family of preferred particles which describe local physics exactly as inertial particles in $\mathbb{M}^4$, but *it loses the* $\underbrace{\textit{structure of parallelism}}_{\footnotesize \mathclap{\text{the affine structure}}\rule[-0.35em]{0pt}{0pt}}$ *between those particles*!

    In particular, to be able to formulate a relativistic theory of gravity, we will need to reformulate our description of spacetime without using affine spaces. This will lead us to the theory of manifolds!
    """)
    return


if __name__ == "__main__":
    app.run()
