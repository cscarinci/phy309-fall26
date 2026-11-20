import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 • Lecture 11 • Vector fields", css_file="phy309.css")


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
    header("Lecture 11", "Week 06", "Lecture 11 • Vector fields")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    - $T_pM = \{\, [\gamma] \mid \gamma : \mathbb{R} \to M,\ \gamma(0) = p \,\}$ with $\gamma \sim \tilde{\gamma}$ if $(\varphi \circ \gamma)'(0) = (\varphi \circ \tilde{\gamma})'(0)$.
    - $\mathrm{Der}_p(M) = \{\, X_p : C^\infty(M, \mathbb{R}) \to \mathbb{R} \mid$ $\text{linear + Leibniz} \,\}$, with the Leibniz rule $X_p(fg) = X_p(f)\, g(p) + f(p)\, X_p(g)$.
    - $T_pM \simeq \mathrm{Der}_p(M)$: $[\gamma] \longleftrightarrow X_p$ with $X_p(f) = \dfrac{d}{dt}\Big|_{t=0} (f \circ \gamma)(t)$, equivalently $(\varphi \circ \gamma)'(0) = X_p(x^i)\, e_i$. On manifolds, we can also identify velocity vectors with directional derivatives.
    - $T_pM$ is an $m$-dimensional vector space: $[\rho] = a[\gamma] + b[\sigma] \iff Z_p = aX_p + bY_p$. A chart $\varphi$ gives the coordinate basis $\partial_i|_p$, with $\partial_i|_p f = \dfrac{\partial}{\partial x^i}(f \circ \varphi^{-1})\Big|_{\varphi(p)}$, and every $X_p = X^i(p)\, \partial_i|_p$ with $X^i(p) = X_p(x^i)$. Here $\partial_i|_p \longleftrightarrow [t \mapsto \varphi^{-1}(\varphi(p) + t\, e_i)]$, whose velocity with respect to $\varphi$ is $e_i$.
    - On a manifold the tangent space $T_pM$ takes the place of the vector space $\mathbb{V}$ of an affine space, but each point has its own.

    **In this lecture:** vector fields, integral curves and the tangent bundle.

    **References:** Carroll 2.3; Sasane Ch. 3
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"""
    ## II.6 &nbsp; Vector fields
    """),
            definition(
                r"""
    A **vector field** on $M$ is an assignment of a tangent vector (a velocity vector, or equivalently a derivation) to each point $p \in M$

    $$
    X : p \longmapsto X_p \in T_p M = \mathrm{Der}_p(M)
    $$

    With respect to a chart $\varphi : U \subseteq M \longrightarrow \mathbb{R}^m$ with local coordinates $x^i : U \longrightarrow \mathbb{R}$

    $$
    p = \varphi^{-1}(x^i(p)\, e_i), \qquad X_p = X^i(p)\, \partial_i|_p
    $$

    and the **local components** $X^i : U \subseteq M \longrightarrow \mathbb{R}$ of $X$ are functions on $U$. The vector field $X$ is **smooth** if its local components with respect to every chart are smooth.
    """,
                "Vector field",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Example on the sphere

    **Example.** &nbsp; On $\mathbb{S}^2$ with the two stereographic charts

    $$
    \begin{aligned}
    \varphi_n(x, y, z) &= \left( \frac{x}{1 - z},\ \frac{y}{1 - z} \right) = (u, v) \\[14pt]
    \varphi_s(x, y, z) &= \left( \frac{x}{1 + z},\ \frac{y}{1 + z} \right) = (\tilde{u}, \tilde{v})
    \end{aligned}
    $$

    define

    $$
    X : p \longmapsto X_p =
    \begin{cases}
    -v(p)\, \partial_u|_p + u(p)\, \partial_v|_p, & p \neq n \\[4pt]
    -\tilde{v}(p)\, \partial_{\tilde{u}}|_p + \tilde{u}(p)\, \partial_{\tilde{v}}|_p, & p \neq s
    \end{cases}
    $$

    The first expression is not defined at $n$, the second is not defined at $s$, and on the overlap $\mathbb{S}^2 - \{n, s\}$ the two must agree for $X$ to be well defined. Given $f \in C^\infty(\mathbb{S}^2, \mathbb{R})$

    $$
    \begin{aligned}
    X_p(f) &= -v(p)\, \partial_u|_p f + u(p)\, \partial_v|_p f \\[8pt]
    &= -v(p)\, \frac{\partial}{\partial u} (f \circ \varphi_n^{-1})\bigg|_{\varphi_n(p)} + u(p)\, \frac{\partial}{\partial v} (f \circ \varphi_n^{-1})\bigg|_{\varphi_n(p)} \\[8pt]
    &= -\tilde{v}(p)\, \frac{\partial}{\partial \tilde{u}} (f \circ \varphi_s^{-1})\bigg|_{\varphi_s(p)} + \tilde{u}(p)\, \frac{\partial}{\partial \tilde{v}} (f \circ \varphi_s^{-1})\bigg|_{\varphi_s(p)}
    \end{aligned}
    $$

    Do these agree? Yes!

    $$
    \begin{aligned}
    \varphi_s \circ \varphi_n^{-1}(u, v) &= \left( \frac{u}{u^2 + v^2},\ \frac{v}{u^2 + v^2} \right) \\[8pt]
    &= \big( \tilde{u}(u, v),\ \tilde{v}(u, v) \big) \\[8pt]
    \Longrightarrow \quad \frac{\partial}{\partial u} (f \circ \varphi_n^{-1}) &= \frac{\partial}{\partial u} (f \circ \varphi_s^{-1} \circ \varphi_s \circ \varphi_n^{-1}) \\[8pt]
    &= \frac{\partial}{\partial \tilde{u}} (f \circ \varphi_s^{-1})\, \frac{\partial \tilde{u}}{\partial u} + \frac{\partial}{\partial \tilde{v}} (f \circ \varphi_s^{-1})\, \frac{\partial \tilde{v}}{\partial u} \\[8pt]
    &= \frac{-u^2 + v^2}{(u^2 + v^2)^2}\, \frac{\partial}{\partial \tilde{u}} (f \circ \varphi_s^{-1}) + \frac{-2uv}{(u^2 + v^2)^2}\, \frac{\partial}{\partial \tilde{v}} (f \circ \varphi_s^{-1})
    \end{aligned}
    $$

    <span class="chain">$\displaystyle \frac{\partial}{\partial v} (f \circ \varphi_n^{-1})$ $\displaystyle = \frac{-2uv}{(u^2 + v^2)^2}\, \frac{\partial}{\partial \tilde{u}} (f \circ \varphi_s^{-1}) + \frac{u^2 - v^2}{(u^2 + v^2)^2}\, \frac{\partial}{\partial \tilde{v}} (f \circ \varphi_s^{-1})$</span>

    and taking $-v$ times the first plus $u$ times the second gives the coefficients

    $$
    \frac{-v (u^2 + v^2)}{(u^2 + v^2)^2} = -\tilde{v}, \qquad \frac{u (u^2 + v^2)}{(u^2 + v^2)^2} = \tilde{u}
    $$

    so they do agree.

    $$
    \Longrightarrow \qquad X : p \longmapsto X_p =
    \begin{cases}
    -v(p)\, \partial_u|_p + u(p)\, \partial_v|_p, & p \neq n \\[4pt]
    -\tilde{v}(p)\, \partial_{\tilde{u}}|_p + \tilde{u}(p)\, \partial_{\tilde{v}}|_p, & p \neq s
    \end{cases}
    $$

    is well-defined and it is smooth since

    $$
    \begin{aligned}
    X^u &= -v : \mathbb{S}^2 - \{n\} \longrightarrow \mathbb{R} \\
    X^v &= u : \mathbb{S}^2 - \{n\} \longrightarrow \mathbb{R} \\
    X^{\tilde{u}} &= -\tilde{v} : \mathbb{S}^2 - \{s\} \longrightarrow \mathbb{R} \\
    X^{\tilde{v}} &= \tilde{u} : \mathbb{S}^2 - \{s\} \longrightarrow \mathbb{R}
    \end{aligned}
    \qquad \text{are all smooth}
    $$

    What about other charts? In the chart $\psi$ of polar and azimuthal angles, defined on $\mathbb{S}^2$ minus the arc of great circle $x \geq 0$, $y = 0$ from $n$ to $s$,

    <span class="chain">$\displaystyle \psi^{-1} : (0, \pi) \times (0, 2\pi) \longrightarrow \mathbb{S}^2, \qquad$ $\displaystyle \psi^{-1}(\phi, \theta) = (\cos\theta \sin\phi,\ \sin\theta \sin\phi,\ \cos\phi)$</span>

    $$
    \begin{aligned}
    \varphi_n \circ \psi^{-1}(\phi, \theta) &= \left( \cot\dfrac{\phi}{2} \cos\theta,\ \cot\dfrac{\phi}{2} \sin\theta \right) \\[8pt]
    &= \big( u(\phi, \theta),\ v(\phi, \theta) \big) \\[8pt]
    \Longrightarrow \quad X : p \longmapsto X_p &= \partial_\theta|_p
    \end{aligned}
    $$

    with smooth components, because the transition map $\varphi_n \circ \psi^{-1}$ is smooth.

    ### Vector fields as operators

    **Remark.** Given a vector field $X$ and a smooth function $f$ we can define another function $X(f) : M \longrightarrow \mathbb{R}$ via

    $$
    X(f)(p) = X_p(f) \qquad \text{(well defined since } f \text{ is smooth)}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            theorem(
                r"""
    A vector field $X : p \longmapsto X_p \in T_p M$ is smooth if and only if it defines a linear differential operator on $M$

    $$
    X : C^\infty(M, \mathbb{R}) \longrightarrow C^\infty(M, \mathbb{R}), \qquad f \longmapsto X(f) : p \longmapsto X_p(f)
    $$

    In a chart $\varphi : U \subseteq M \longrightarrow \mathbb{R}^m$

    $$
    X(f) \circ \varphi^{-1} = X^i \circ \varphi^{-1}\, \frac{\partial}{\partial x^i} (f \circ \varphi^{-1})
    $$

    which is smooth for every $f$ if and only if every $X^i \circ \varphi^{-1}$ is smooth.
    """,
                "Smooth vector fields are differential operators",
            ),
            definition(
                r"""
    The space of smooth vector fields on $M$ is denoted

    <span class="chain">$\displaystyle \Gamma(TM) = \text{space of smooth vector fields}$ $\displaystyle X : C^\infty(M, \mathbb{R}) \longrightarrow C^\infty(M, \mathbb{R})$</span>

    where $TM$ denotes the “collection” of all tangent spaces of $M$ (the tangent bundle of $M$).
    """,
                "Smooth vector fields",
            ),
            mo.md(
                r"""
    **Remark.** In terms of a chart $\varphi : U \subseteq M \longrightarrow \mathbb{R}^m$

    $$
    X = X^i\, \partial_i
    $$

    where $X^i : U \subseteq M \longrightarrow \mathbb{R}$ are local functions on $U$ and $\partial_i \in \Gamma(TM)|_U$ are local vector fields on $U$.

    The $\partial_i$ form a local basis of vector fields on $U$; they play over $U$ the role of $e_i \in \mathbb{R}^m$.

    ### Integral curves
    """
            ),
            definition(
                r"""
    Given a smooth path $\gamma : \mathbb{R} \longrightarrow M$, a **vector field along** $\gamma$ is an assignment

    $$
    X : t \in \mathbb{R} \longmapsto X_{\gamma(t)} \in T_{\gamma(t)} M
    $$

    of a tangent vector at $\gamma(t)$ for each $t \in \mathbb{R}$.
    """,
                "Vector field along a path",
            ),
            mo.md(
                r"""
    **Example.** The velocity vector field of a smooth path $\gamma : \mathbb{R} \longrightarrow M$ is the assignment $\gamma' : t \in \mathbb{R} \longmapsto \gamma'(t) \in T_{\gamma(t)} M$ such that

    <span class="chain">$\displaystyle \gamma'(t)(f) = (f \circ \gamma)'(t)$ $\displaystyle \leadsto \quad \text{with respect to a chart } \varphi\text{,} \quad \gamma'(t) = (x^i \circ \gamma)'(t)\ \partial_i|_{\gamma(t)}$</span>
    """
            ),
            definition(
                r"""
    Given a smooth vector field $X \in \Gamma(TM)$, a path $\gamma : I \longrightarrow M$, with $I \subseteq \mathbb{R}$ an open interval, is an **integral curve** of $X$ if its velocity equals the vector field along $\gamma$

    $$
    \gamma'(t) = X_{\gamma(t)} \qquad \forall\ t \in I
    $$

    With respect to a chart $\varphi$ this is a first order system of ordinary differential equations

    $$
    (x^i \circ \gamma)'(t) = X^i(\gamma(t))
    $$
    """,
                "Integral curve",
            ),
            theorem(
                r"""
    For each $p \in M$ there exists a unique maximal integral curve $\gamma : I_p \longrightarrow M$ of $X \in \Gamma(TM)$, where $I_p$ is an open interval containing $0$, with the initial condition $\gamma(0) = p$:

    $$
    \begin{cases} \gamma'(t) = X_{\gamma(t)} \\ \gamma(0) = p \end{cases} \quad \text{is a first order initial value problem on } M
    $$
    """,
                "Existence and uniqueness of integral curves",
            ),
            mo.md(
                r"""
    **Remark.** $I_p$ need not be all of $\mathbb{R}$.

    **Example.** &nbsp; On $\mathbb{S}^2$, with

    $$
    X = \begin{cases} -v\, \partial_u + u\, \partial_v & \text{on } \mathbb{S}^2 - \{n\} \\[4pt] -\tilde{v}\, \partial_{\tilde{u}} + \tilde{u}\, \partial_{\tilde{v}} & \text{on } \mathbb{S}^2 - \{s\} \end{cases}
    $$

    a path $\gamma : \mathbb{R} \longrightarrow \mathbb{S}^2$ with $\varphi_n(\gamma(0)) = (u_0, v_0)$ is an integral curve of $X$

    <span class="chain">$\displaystyle \Longleftrightarrow \quad \gamma'(t) = X_{\gamma(t)}$ $\displaystyle \Longleftrightarrow \quad (\varphi_n \circ \gamma)'(t) = X^i(\gamma(t))\, e_i, \quad \begin{bmatrix} u'(t) \\ v'(t) \end{bmatrix} = \begin{bmatrix} -v(t) \\ u(t) \end{bmatrix}$ $\displaystyle \Longleftrightarrow \quad \begin{bmatrix} u(t) \\ v(t) \end{bmatrix} = \begin{bmatrix} u_0 \cos(t) - v_0 \sin(t) \\ u_0 \sin(t) + v_0 \cos(t) \end{bmatrix}$ $\displaystyle \Longleftrightarrow \quad \gamma(t) = \varphi_n^{-1}\!\left( \begin{bmatrix} u_0 \cos(t) - v_0 \sin(t) \\ u_0 \sin(t) + v_0 \cos(t) \end{bmatrix} \right)$</span>
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    s_u0 = mo.ui.slider(-1.5, 1.5, 0.1, value=1.4, label="$u_0$", show_value=False)
    s_v0 = mo.ui.slider(-1.5, 1.5, 0.1, value=0.0, label="$v_0$", show_value=False)
    s_t = mo.ui.slider(0.0, 6.28, 0.02, value=1.0, label="$t$", show_value=False)
    return s_t, s_u0, s_v0


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, RED, SPHERE_EDGE, arrow, math, mo, np, panel, s_t, s_u0, s_v0, sphere, turntable):
    def _inv(u, v):
        r = 1 + u**2 + v**2
        return 2 * u / r, 2 * v / r, (r - 2) / r

    _u0, _v0, _t = s_u0.value, s_v0.value, s_t.value
    _ut = _u0 * math.cos(_t) - _v0 * math.sin(_t) + 0.0
    _vt = _u0 * math.sin(_t) + _v0 * math.cos(_t) + 0.0
    _s = np.linspace(0, _t, 200)
    _us, _vs = _u0 * np.cos(_s) - _v0 * np.sin(_s), _u0 * np.sin(_s) + _v0 * np.cos(_s)
    _c = np.linspace(0, 2 * np.pi, 400)

    # vectors of X on a few latitude circles
    _arrows = []
    for _z in (-0.75, -0.4, 0.0, 0.4, 0.75):
        _rr = math.sqrt(1 - _z**2)
        for _a in np.linspace(0, 2 * np.pi, 12, endpoint=False):
            _q = (_rr * math.cos(_a), _rr * math.sin(_a), _z)
            _arrows.append((_q, (_q[0] - 0.22 * _q[1], _q[1] + 0.22 * _q[0], _z), BLUE, 1.2))
    _sph = turntable(
        -30,
        20,
        "the unit sphere with the vector field X on a few latitudes and the integral curve gamma from gamma(0) to gamma(t)",
        [
            panel(
                1.0,
                surfaces=[sphere()],  # opaque: the vectors on the far side stay hidden
                outlines=[SPHERE_EDGE],
                lines=[
                    (*_inv(_u0 * np.cos(_c) - _v0 * np.sin(_c), _u0 * np.sin(_c) + _v0 * np.cos(_c)), RED, 0.9),
                    (*_inv(_us, _vs), RED, 1.8),
                ],
                arrows=_arrows,
                points=[(_inv(_u0, _v0), RED, 4.0, True), (_inv(_ut, _vt), RED, 4.0), ((0, 0, 1), "#000000", 3.4), ((0, 0, -1), "#000000", 3.4)],
                texts=[((0, 0, 1), "n", "#000000", 90), ((0, 0, -1), "s", "#000000", -90)],
            )
        ],
        height=340,
        width=400,
        key="phy309-l11-curve",
        apart=True,
        bias=0.12,
    )

    from matplotlib.patches import PathPatch as _PathPatch
    from matplotlib.path import Path as _Path
    from matplotlib.textpath import TextPath as _TextPath

    _fig = Figure(figsize=(3.4, 3.4), layout="constrained")
    _ax2 = _fig.subplots()
    _ax2.set_title(r"$\varphi_n = (u, v)$", fontsize=13)
    _ax2.set_xlim(-3, 3)
    _ax2.set_ylim(-3, 3)
    _ax2.set_aspect("equal")
    _ax2.axhline(0, color="black", lw=0.6)
    _ax2.axvline(0, color="black", lw=0.6)
    _g = np.linspace(-2.5, 2.5, 9)
    _U, _V = np.meshgrid(_g, _g)
    for _a0, _b0 in zip(_U.ravel(), _V.ravel()):
        if _a0 or _b0:
            arrow(_ax2, (_a0, _b0), (_a0 - _b0 / 5, _b0 + _a0 / 5), BLUE, lw=1.0)
    _ax2.plot(np.cos(_c), np.sin(_c), color=GREY, lw=1.0)
    # "equator" along the grey circle, between it and the opening orbit (radius 1.4) and its dot, between the field arrows, off the axes
    _tp = _TextPath((0, 0), "equator", size=10 / 33.8)  # 10 pt in data units (about 33.8 pt per unit at this size)
    _ext = _tp.get_extents()
    _ang = math.radians(-135) + (_tp.vertices[:, 0] - (_ext.x0 + _ext.x1) / 2) / 1.17
    _rad = 1.17 + (_ext.y0 + _ext.y1) / 2 - _tp.vertices[:, 1]
    _ax2.add_patch(_PathPatch(_Path(np.c_[_rad * np.cos(_ang), _rad * np.sin(_ang)], _tp.codes), facecolor=GREY, edgecolor="none"))
    _ax2.plot(_u0 * np.cos(_c) - _v0 * np.sin(_c), _u0 * np.sin(_c) + _v0 * np.cos(_c), color=RED, lw=0.9)
    _ax2.plot(_us, _vs, color=RED)
    _ax2.plot(_u0, _v0, "o", color=RED, mfc="white", ms=6)
    _ax2.plot(_ut, _vt, "o", color=RED, ms=6)
    _al = math.atan2(_v0, _u0)
    _w = 1 / math.hypot(1.2, 1)
    for (_px, _py), _an, _sg, _name in (((_u0, _v0), _al, -1, r"$\gamma(0)$"), ((_ut, _vt), _al + _t, 1, r"$\gamma(t)$")):
        # mostly outward from the circle (weight 1.2), a little behind (gamma(0)) or ahead (gamma(t)) along it;
        # the distance in points keeps the name (about 18 x 11 points) clear of its dot, of the circle, and of the other name when the points meet
        _nx, _ny = math.cos(_an), math.sin(_an)
        _dx, _dy = (1.2 * _nx - _sg * _ny) * _w, (1.2 * _ny + _sg * _nx) * _w
        _off = max(9 * abs(_dx) + 5.5 * abs(_dy) + 3, (9 * abs(_nx) + 5.5 * abs(_ny) + 3) / (1.2 * _w), min(11 / (_w * abs(_ny) + 1e-9), 7.5 / (_w * abs(_nx) + 1e-9)))
        _ax2.annotate(_name, (_px, _py), textcoords="offset points", xytext=(_off * _dx, _off * _dy), ha="center", va="center", color="black", fontsize=10, annotation_clip=False, zorder=8).set_in_layout(False)
    _ax2.set_xticks([-3, 0, 3])
    _ax2.set_yticks([-3, 0, 3])

    _hidden = mo.Html(f'{_sph.text}<div hidden data-pic="phy309-l11-curve">{mo.as_html(_fig).text}</div>')
    mo.vstack([mo.hstack([s_u0, s_v0, s_t], justify="start", gap=2, wrap=True), _hidden])
    return


@app.cell(hide_code=True)
def _(frame, mo):
    mo.Html(
        '<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 0.5rem 1rem;">'
        f'<div style="flex: 1.3 1 300px; min-width: 260px;">{frame("phy309-l11-curve", 340).text}</div>'
        '<div style="flex: 0 1 auto;" data-side="phy309-l11-curve"></div></div>'
    )
    return


@app.cell(hide_code=True)
def _(BLUE, ORANGE, RED, definition, math, mo, np, panel, patch, sheet, turntable):
    # A curved surface with three tangent planes
    def _h(x, y):  # height of the surface
        return 0.35 * np.sin(1.1 * x) * np.cos(0.9 * y) + 0.12 * y

    def _dh(x, y):
        return 0.35 * 1.1 * np.cos(1.1 * x) * np.cos(0.9 * y), -0.35 * 0.9 * np.sin(1.1 * x) * np.sin(0.9 * y) + 0.12

    _X, _Y = np.meshgrid(np.linspace(-2.2, 2.2, 43), np.linspace(-2.2, 2.2, 43), indexing="ij")
    _g = np.linspace(-2.2, 2.2, 160)
    _k = -2.2 + 0 * _g
    _lines = [(_g, _k, _h(_g, _k), "#000000", 1.2), (_g, -_k, _h(_g, -_k), "#000000", 1.2), (_k, _g, _h(_k, _g), "#000000", 1.2), (-_k, _g, _h(-_k, _g), "#000000", 1.2)]
    _arrows, _points, _texts = [], [], [((-2.2, -2.2, _h(-2.2, -2.2)), "M", "#000000", -150, 10)]
    _surfaces = [sheet(_X, _Y, _h(_X, _Y), wire=[(0, 7, BLUE, 0.5), (1, 7, BLUE, 0.5)])]
    # names beyond their arrow or past the plane's edge, at (a, b) in the plane's tangent directions, hung towards the given direction
    _spots = {"W_r": (-1.15, 0.4, 180), "Z_q": (0.9, 0.62, 45), r"T_q M": (0.0, 0.8, 90), r"T_r M": (0.75, -0.7, -60), "Y_p": (0.22, 0.4, 0)}
    for (_x, _y), _col, _fill, _name, _tn, _vecs in (
        ((-1.3, -0.2), BLUE, "#dbe8f6", "q", r"T_q M", (((0.3, 0.2), "Z_q"),)),
        ((1.25, -1.0), RED, "#f4d6d4", "p", r"T_p M", (((0.38, -0.12), "X_p"), ((0.1, 0.38), "Y_p"))),
        ((0.5, 1.5), ORANGE, "#fde0c8", "r", r"T_r M", (((-0.5, 0.25), "W_r"),)),
    ):
        _P = np.array([_x, _y, _h(_x, _y)])
        _hx, _hy = _dh(_x, _y)
        _tx, _ty = np.array([1.0, 0.0, _hx]), np.array([0.0, 1.0, _hy])  # tangent directions
        _corners = np.array([_P + s_ * 0.7 * _tx + t_ * 0.55 * _ty for s_, t_ in ((-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1))])
        _surfaces.append(patch(_corners[:4], _fill, 0.6))
        _lines.append((*_corners.T, _col, 1.2, None, 0.6))  # drawn over the nearby faces of the surface
        for (_a, _b), _lab in _vecs:
            _tip = _P + _a * _tx + _b * _ty
            _arrows.append((tuple(_P), tuple(_tip), _col))
            _sp = _spots.get(_lab)
            _texts.append((tuple(_P + _sp[0] * _tx + _sp[1] * _ty), _lab, _col, _sp[2], 0) if _sp else (tuple(_tip), _lab, _col, math.degrees(math.atan2(_b, _a)), 6))
        _points.append((tuple(_P), "#000000", 3.4))
        _sp = _spots.get(_tn)
        _texts += [(tuple(_P), _name, "#000000", -135, 6), (tuple(_P + _sp[0] * _tx + _sp[1] * _ty), _tn, _col, _sp[2], 0) if _sp else (tuple(_corners[0]), _tn, _col, 180, 6)]
    _fig = turntable(
        -35,
        28,
        "a curved surface M with the tangent planes at three points q, p, r and tangent vectors in each",
        [panel(1.0, surfaces=_surfaces, lines=_lines, arrows=_arrows, points=_points, texts=_texts)],
        height=420,
        bias=0.25,  # the points and vectors lie on the surface and on their tangent planes: draw them in front
    )

    mo.vstack(
        [
            mo.md(r"""### The tangent bundle"""),
            definition(
                r"""
    The **tangent bundle** of an $m$-manifold $M$ is

    $$
    \begin{aligned}
    TM &= \text{the collection of all tangent spaces} \\[8pt]
    &\mathrel{\text{“}{=}\text{”}} \bigcup_{p \in M} T_p M = \{\, (p, X_p) \mid p \in M,\ X_p \in T_p M \,\}
    \end{aligned}
    $$

    A tangent vector $X_p$ (an equivalence class of paths with the same velocity at $p$, or a derivation at $p$) always comes with its base point, which is why the notation $X_p$ is preferable to $[\gamma]$.
    """,
                "Tangent bundle",
            ),
            _fig,
        ]
    )
    return


if __name__ == "__main__":
    app.run()
