import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 • Lecture 14 • Metrics", css_file="phy309.css")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    # ---- Building blocks shared by all lectures -------------------------
    BLUE = "#3f5f8f"

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

    return BLUE, definition, header, theorem


@app.cell(hide_code=True)
def _():
    import math

    import numpy as np

    # the course palette (figures only); BLUE is the one of the building blocks
    GREY, LIGHT, ORANGE = "#9a9a9a", "#e3ebf4", "#b9853f"
    return GREY, LIGHT, ORANGE, math, np


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
def _(GREY, LIGHT, np, sheet):
    # the unit sphere (z up) in one flat colour, see-through, and its edge as seen from the current view
    def sphere_flat():
        a, b = np.meshgrid(np.linspace(0, np.pi, 37), np.linspace(0, 2 * np.pi, 73), indexing="ij")
        return sheet(np.sin(a) * np.cos(b), np.sin(a) * np.sin(b), np.cos(a), flat=LIGHT, alpha=0.5)

    SPHERE_OUTLINE = ("sphere", (0, 0, 0), 1.0, GREY, 1.2)

    def first_view(az, el):
        """The directions of R^3 that are right and up on the screen in the first view (az, el in degrees)."""
        a, e = np.radians(az), np.radians(el)
        return np.array([-np.sin(a), np.cos(a), 0.0]), np.array([-np.sin(e) * np.cos(a), -np.sin(e) * np.sin(a), np.cos(e)])

    def name_at(point, dx, dy, tex, colour, axes, sc, h=20):
        """A name whose middle sits dx, dy pixels from the 3D point `point` in the first view (the offset turns with the
        figure). The kit puts a name of direction 90 with its bottom edge at its anchor, so the anchor is half the name's
        height lower; so a name never changes its alignment as a slider moves it."""
        right, up = axes
        return (tuple(np.asarray(point, float) + (dx * right + (dy - h / 2) * up) / sc), tex, colour, 90, 0)

    def beyond(tail, tip, gap, axes):
        """The offset (dx, dy), of length `gap` pixels, that continues the arrow from `tail` to `tip` on the screen of the first view."""
        d = np.asarray(tip, float) - np.asarray(tail, float)
        v = np.array([d @ axes[0], d @ axes[1]])
        return gap * v / (np.hypot(*v) or 1.0)

    def pins(up, top, bottom):
        """Two names without text above and below everything in the first view, so the frame keeps its height."""
        return [(tuple(top * up), "", "#000000", 0, 0), (tuple(-bottom * up), "", "#000000", 0, 0)]

    return SPHERE_OUTLINE, beyond, first_view, name_at, pins, sphere_flat


@app.cell(hide_code=True)
def _(header):
    header("Lecture 14", "Week 9", "Lecture 14 • Metrics")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    Smooth vector fields

    $$
    \left.
    \begin{aligned}
    X : p \in M &\longrightarrow X_p \in T_pM \\[4pt]
    X : C^\infty(M, \mathbb{R}) &\longrightarrow C^\infty(M, \mathbb{R}) \\
    f &\longmapsto X(f) \quad \text{linear + Leibniz}
    \end{aligned}
    \ \right\}
    \ \begin{gathered} \text{smooth vector fields} \\ X \in \Gamma(TM) \end{gathered}
    $$

    <span class="chain">$\displaystyle \overset{\varphi}{\leadsto} \quad X = \underbrace{X^i\vphantom{\big|_p}}_{\footnotesize \mathclap{\begin{matrix} \text{components} \\ \text{of } X \end{matrix}}}\, \partial_i \quad \text{where} \quad X^i = \underbrace{X(x^i)\vphantom{\big|_p}}_{\footnotesize \mathclap{\begin{matrix} \text{derivative of local} \\ \text{coordinates} \end{matrix}}} : U \to \mathbb{R} \quad \text{and} \quad \underbrace{\partial_i\big|_p\vphantom{\big|_p}}_{\footnotesize \mathclap{\begin{matrix} \text{coord basis} \\ \text{of } T_pM \end{matrix}}} \in T_pM$</span>

    <span class="chain">$\displaystyle \overset{\tilde\varphi}{\leadsto} \quad X = \tilde X^j\, \tilde\partial_j \quad \text{are related via} \quad \underbrace{\frac{\partial \tilde x^j}{\partial x^i}}_{\footnotesize \mathclap{\begin{matrix} \text{the Jacobian matrix of} \\ \text{the change of coordinates} \end{matrix}}}$</span>

    If &nbsp; $p = \varphi^{-1}(x^i e_i) = \tilde\varphi^{-1}(\tilde x^j e_j)$

    $$
    \begin{aligned}
    \Longrightarrow \quad & \tilde x^j(x^i e_i)\, e_j = \tilde\varphi \circ \varphi^{-1}(x^i e_i) \\[12pt]
    \Longrightarrow \quad & \partial_i = \frac{\partial \tilde x^j}{\partial x^i}\, \tilde\partial_j \qquad (i \text{ free, } j \text{ summed over}) \\[12pt]
    & \tilde X^j = \frac{\partial \tilde x^j}{\partial x^i}\, X^i \qquad (j \text{ free, } i \text{ summed over})
    \end{aligned}
    $$

    Coordinates and their indices must remain coherent on both sides of the equations!

    $$
    \leadsto \quad
    \begin{bmatrix} \tilde X^1 \\ \vdots \\ \tilde X^m \end{bmatrix}
    =
    \begin{bmatrix}
    \dfrac{\partial \tilde x^1}{\partial x^1} & \cdots & \dfrac{\partial \tilde x^1}{\partial x^m} \\
    \vdots & \ddots & \vdots \\
    \dfrac{\partial \tilde x^m}{\partial x^1} & \cdots & \dfrac{\partial \tilde x^m}{\partial x^m}
    \end{bmatrix}
    \begin{bmatrix} X^1 \\ \vdots \\ X^m \end{bmatrix}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A path $\gamma(t) \in M$ is an integral curve of a smooth vector field $X \in \Gamma(TM)$ if

    $$
    \begin{aligned}
    & \gamma'(t) = X_{\gamma(t)} \in T_{\gamma(t)}M \\[12pt]
    & \quad \begin{aligned}
    \Longleftrightarrow \quad & \frac{d}{dt}\, f \circ \gamma(t) = X_{\gamma(t)}(f) \quad \forall\, f \in C^\infty(M, \mathbb{R}) \\[12pt]
    \overset{\varphi}{\Longleftrightarrow} \quad & \frac{d}{dt}\, x^i(t) = X^i(t) \quad \text{where} \quad \gamma(t) = \varphi^{-1}\big(x^i(t)\, e_i\big) \qquad X_{\gamma(t)} = X^i(t)\, \partial_i\big|_{\gamma(t)} \\[8pt]
    & \begin{array}{l} (\text{1st order system of ODEs} \\ \quad \text{for components of path}) \end{array} \quad \leadsto \quad \begin{cases} \dfrac{d}{dt}\, x^1(t) = X^1(t) \\ \qquad \vdots \\ \dfrac{d}{dt}\, x^m(t) = X^m(t) \end{cases}
    \end{aligned}
    \end{aligned}
    $$

    $\leadsto$ &nbsp; in affine spaces we could put the “same” vector at different points in space

    &emsp; $\Longrightarrow$ &nbsp; we have special vector fields on affine spaces (constant vector fields)

    &emsp; $\Longrightarrow$ &nbsp; we have special integral curves (straight lines) which later became important physically (inertial particles)

    $\leadsto$ &nbsp; on manifolds, in order to obtain special vector fields, and their special integral curves, we will need <u>more structure</u>! &nbsp; <span class="nw">$\leadsto$ &nbsp; connections</span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **In this lecture:** metrics

    (will give us connections later)

    All elementary interactions in the standard model of particle physics are given by types of connections $\leadsto$ gravity as well!

    **References:** <span style="white-space: nowrap">Schutz 5.2, 6.2;</span> <span style="white-space: nowrap">Carroll 2.5;</span> <span style="white-space: nowrap">Sasane 5.1–5.2</span>

    ## III.1 &nbsp; Metrics

    **Recall.**

    <span class="chain">$\displaystyle \mathbb{E}^3 = \big( (\mathbb{A}^3, \mathbb{V}^3, -),\ \langle \cdot, \cdot \rangle \big)$</span>

    <span class="chain">$\displaystyle \langle \cdot, \cdot \rangle : \mathbb{V}^3 \times \mathbb{V}^3 \longrightarrow \mathbb{R}$ $\displaystyle \quad \begin{array}{l} (\text{symmetric bilinear} \\ \quad \text{positive definite}) \end{array}$</span>

    <span class="chain">$\displaystyle \mathbb{M}^{3,1} = \big( (\mathbb{A}^4, \mathbb{V}^4, -),\ \eta(\cdot, \cdot) \big)$</span>

    <span class="chain">$\displaystyle \eta(\cdot, \cdot) : \mathbb{V}^4 \times \mathbb{V}^4 \longrightarrow \mathbb{R}$ $\displaystyle \quad \begin{array}{l} (\text{symmetric bilinear} \\ \quad \text{of signature } (3, 1)) \end{array}$</span>

    signature $(3, 1)$ &nbsp;$\leadsto$&nbsp; restriction to orthogonal complement of timelike vector is Euclidean
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(
        r"""
    A metric on a manifold $M$ is an assignment

    $$
    g : p \in M \longmapsto g_p(\cdot, \cdot) : T_pM \times T_pM \longrightarrow \mathbb{R}
    $$

    of an inner-product on each tangent space

    <span class="chain">$\displaystyle \bullet \quad \text{if } g_p \text{ is } \underbrace{\text{Euclidean}}_{\footnotesize \mathclap{\text{positive definite}}} \text{ for every } p \in M$ $\displaystyle \quad \leadsto \quad g \text{ is called a Riemannian metric}$</span>

    <span class="chain">$\displaystyle \bullet \quad \text{if } g_p \text{ is } \underbrace{\text{Minkowski}}_{\footnotesize \mathclap{\text{signature } (m - 1, 1)}} \text{ for every } p \in M$ $\displaystyle \quad \leadsto \quad g \text{ is called a Lorentzian metric}$</span>
    """,
        "Metric",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In a chart &nbsp; $\varphi : U \subseteq M \to \mathbb{R}^m$

    $$
    \begin{aligned}
    p &= \varphi^{-1}(x^i e_i) \in M \\[4pt]
    X_p &\overset{\varphi}{=} X^i(p)\, \partial_i\big|_p \in T_pM \\[4pt]
    Y_p &\overset{\varphi}{=} Y^j(p)\, \partial_j\big|_p \in T_pM
    \end{aligned}
    $$

    $$
    \begin{aligned}
    \Longrightarrow \quad & g_p(X_p, Y_p) \overset{\varphi}{=} g_p\big( X^i(p)\, \partial_i\big|_p,\ Y^j(p)\, \partial_j\big|_p \big) \\[8pt]
    & \quad = X^i(p)\, g_p\big( \partial_i\big|_p, \partial_j\big|_p \big)\, Y^j(p) = X^i(p)\, \underbrace{g_{ij}(p)}_{\footnotesize \mathclap{\begin{matrix} \text{components} \\ \text{of } g_p \end{matrix}}}\, Y^j(p) \\[22pt]
    & \quad = \big[ X^1(p) \ \cdots \ X^m(p) \big]
    \begin{bmatrix} g_{11}(p) & \cdots & g_{1m}(p) \\ \vdots & \ddots & \vdots \\ g_{m1}(p) & \cdots & g_{mm}(p) \end{bmatrix}
    \begin{bmatrix} Y^1(p) \\ \vdots \\ Y^m(p) \end{bmatrix} \\[8pt]
    & \quad = [X^i(p)]^T\, [g_{ij}(p)]\, [Y^j(p)]
    \end{aligned}
    $$

    <span class="chain">$\displaystyle g \text{ metric on } M \ \ \overset{\varphi}{\leftrightsquigarrow} \ \ \underbrace{g_{ij}}_{\footnotesize \mathclap{\begin{matrix} \text{components} \\ \text{of } g \end{matrix}}} : U \subseteq M \to \mathbb{R}$ $\displaystyle \quad \overset{\tilde\varphi}{\leftrightsquigarrow} \ \ \tilde g_{kl} : \tilde U \subseteq M \to \mathbb{R}$</span>

    $$
    \begin{aligned}
    g_p(X_p, Y_p) &\overset{\varphi}{=} [X^i(p)]^T\, [g_{ij}(p)]\, [Y^j(p)] \\[8pt]
    &\overset{\tilde\varphi}{=} [\tilde X^k(p)]^T\, [\tilde g_{kl}(p)]\, [\tilde Y^l(p)] \\[8pt]
    &= [X^i(p)]^T \Big[ \frac{\partial \tilde x^k}{\partial x^i}(p) \Big]^T [\tilde g_{kl}(p)] \Big[ \frac{\partial \tilde x^l}{\partial x^j}(p) \Big] [Y^j(p)]
    \end{aligned}
    $$

    <span class="chain">$\displaystyle \Longrightarrow \quad \boxed{\ g_{ij} = \frac{\partial \tilde x^k}{\partial x^i}\, \tilde g_{kl}\, \frac{\partial \tilde x^l}{\partial x^j} \quad \text{on } U \cap \tilde U \ }$ $\displaystyle \quad \begin{array}{l} (\text{transformation of components} \\ \quad \text{of } g \text{ under change of charts}) \end{array}$</span>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** &nbsp; Euclidean plane $\mathbb{E}^2$

    Choose &nbsp; $o \in \mathbb{E}^2$, &nbsp; $e_1, e_2 \in \mathbb{V}^2$ &nbsp; orthonormal
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, GREY, ORANGE, mo):
    # ---- Figure: the point p in both charts of the plane (the PDF's sketch) ----
    def _name(x, y, tex, colour="#000"):
        return f'<text x="{x}" y="{y}" fill="{colour}" font-family="KaTeX_Math" font-style="italic" font-size="19">{tex}</text>'

    _sub = '<tspan font-family="KaTeX_Main" font-style="normal" font-size="13" dy="4">{}</tspan>'

    mo.Html(f"""
    <div style="text-align: center; margin: 0.4rem 0;">
    <svg viewBox="0 0 400 250" style="display: block; margin: 0 auto; width: 400px; max-width: 100%;" role="img"
         aria-label="the plane with origin o, the orthonormal vectors e1 and e2 along the axes, and a point p, at x and y along the axes, at distance r from o and at angle theta from the first axis">
      <line x1="25" y1="200" x2="372" y2="200" stroke="#000" stroke-width="1.1"/><polygon points="380,200 370,196 370,204" fill="#000"/>
      <line x1="70" y1="238" x2="70" y2="22" stroke="#000" stroke-width="1.1"/><polygon points="70,14 66,24 74,24" fill="#000"/>
      <line x1="245" y1="62" x2="245" y2="200" stroke="{GREY}" stroke-width="1.2" stroke-dasharray="5 4"/>
      <line x1="245" y1="62" x2="70" y2="62" stroke="{GREY}" stroke-width="1.2" stroke-dasharray="5 4"/>
      <path d="M 112 200 A 42 42 0 0 0 103.0 173.9" fill="none" stroke="{GREY}" stroke-width="1.2"/>
      <line x1="70" y1="200" x2="239.5" y2="66.4" stroke="{BLUE}" stroke-width="2"/><polygon points="245,62 233.5,65.9 238.4,72.2" fill="{BLUE}"/>
      <line x1="70" y1="200" x2="136" y2="200" stroke="{ORANGE}" stroke-width="2"/><polygon points="146,200 135,195.5 135,204.5" fill="{ORANGE}"/>
      <line x1="70" y1="200" x2="70" y2="134" stroke="{ORANGE}" stroke-width="2"/><polygon points="70,124 65.5,135 74.5,135" fill="{ORANGE}"/>
      <circle cx="245" cy="62" r="4" fill="#000"/><circle cx="70" cy="200" r="3.6" fill="#000"/>
      {_name(52, 222, "o")}
      {_name(122, 226, "e" + _sub.format(1), ORANGE)}
      {_name(42, 150, "e" + _sub.format(2), ORANGE)}
      {_name(240, 224, "x")}
      {_name(48, 68, "y")}
      {_name(254, 56, "p")}
      {_name(140, 112, "r", BLUE)}
      {_name(120, 188, "θ")}
    </svg>
    </div>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <span class="chain">$\displaystyle p = o + x\, e_1 + y\, e_2 = o + r\cos\theta\, e_1 + r\sin\theta\, e_2$ $\displaystyle \quad (x = x^1, \ \ y = x^2, \ \ r = \tilde x^1, \ \ \theta = \tilde x^2)$</span>

    $$
    \begin{aligned}
    X_p &= X^1 \frac{\partial}{\partial x} + X^2 \frac{\partial}{\partial y} = \tilde X^1 \frac{\partial}{\partial r} + \tilde X^2 \frac{\partial}{\partial \theta} \\[10pt]
    &= \tilde X^1 \Big( \frac{\partial x}{\partial r} \frac{\partial}{\partial x} + \frac{\partial y}{\partial r} \frac{\partial}{\partial y} \Big) + \tilde X^2 \Big( \frac{\partial x}{\partial \theta} \frac{\partial}{\partial x} + \frac{\partial y}{\partial \theta} \frac{\partial}{\partial y} \Big) \\[10pt]
    &= \big( \cos\theta\, \tilde X^1 - r\sin\theta\, \tilde X^2 \big) \frac{\partial}{\partial x} + \big( \sin\theta\, \tilde X^1 + r\cos\theta\, \tilde X^2 \big) \frac{\partial}{\partial y}
    \end{aligned}
    $$

    $$
    \Longrightarrow \quad
    \begin{bmatrix} X^1 \\ X^2 \end{bmatrix}
    =
    \begin{bmatrix} \cos\theta & -r\sin\theta \\ \sin\theta & r\cos\theta \end{bmatrix}
    \begin{bmatrix} \tilde X^1 \\ \tilde X^2 \end{bmatrix}
    $$

    $$
    \begin{aligned}
    & g_p(X_p, Y_p) = X^1 Y^1 + X^2 Y^2 = [X^1 \ X^2] \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} Y^1 \\ Y^2 \end{bmatrix} \qquad \Big( \begin{bmatrix} g_{11} & g_{12} \\ g_{21} & g_{22} \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \Big) \\[10pt]
    & \quad = [\tilde X^1 \ \tilde X^2]
    \begin{bmatrix} \cos\theta & \sin\theta \\ -r\sin\theta & r\cos\theta \end{bmatrix}
    \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}
    \begin{bmatrix} \cos\theta & -r\sin\theta \\ \sin\theta & r\cos\theta \end{bmatrix}
    \begin{bmatrix} \tilde Y^1 \\ \tilde Y^2 \end{bmatrix} \\[10pt]
    & \quad = [\tilde X^1 \ \tilde X^2] \begin{bmatrix} 1 & 0 \\ 0 & r^2 \end{bmatrix} \begin{bmatrix} \tilde Y^1 \\ \tilde Y^2 \end{bmatrix} = \tilde X^1 \tilde Y^1 + r^2\, \tilde X^2 \tilde Y^2 \qquad \Big( \begin{bmatrix} \tilde g_{11} & \tilde g_{12} \\ \tilde g_{21} & \tilde g_{22} \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 0 & r^2 \end{bmatrix} \Big)
    \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    polar_r = mo.ui.slider(1.0, 2.0, 0.1, value=1.5, label=r"$r$", show_value=True)
    return (polar_r,)


@app.cell(hide_code=True)
def _(BLUE, GREY, ORANGE, math, mo, polar_r):
    # ---- Figure: the coordinate vectors of the polar chart at p, for theta fixed ----
    _U, _TH, _OX, _OY = 70, math.radians(30), 50, 305   # pixels per unit, theta, the origin in the picture
    _c, _s, _r = math.cos(_TH), math.sin(_TH), polar_r.value

    def _at(x, y):
        return _OX + _U * x, _OY - _U * y

    def _arrow(a, b, colour, w=2.0):
        (x0, y0), (x1, y1) = _at(*a), _at(*b)
        L = math.hypot(x1 - x0, y1 - y0)
        ux, uy = (x1 - x0) / L, (y1 - y0) / L
        bx, by = x1 - 10 * ux, y1 - 10 * uy
        return (
            f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{colour}" stroke-width="{w}"/>'
            f'<polygon points="{x1:.1f},{y1:.1f} {bx - 4.5 * uy:.1f},{by + 4.5 * ux:.1f} {bx + 4.5 * uy:.1f},{by - 4.5 * ux:.1f}" fill="{colour}"/>'
        )

    def _name(x, y, tex, colour="#000", anchor="start"):
        return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" fill="{colour}" font-family="KaTeX_Math" font-style="italic" font-size="19">{tex}</text>'

    def _ddx(x, y, letter):
        # the fraction d/d(letter), with its left end at x and its bar at height y
        return (
            f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x + 22:.1f}" y2="{y:.1f}" stroke="{ORANGE}" stroke-width="1"/>'
            f'<text x="{x + 11:.1f}" y="{y - 5:.1f}" text-anchor="middle" fill="{ORANGE}" font-family="KaTeX_Main" font-size="16">∂</text>'
            f'<text x="{x + 11:.1f}" y="{y + 16:.1f}" text-anchor="middle" fill="{ORANGE}" font-family="KaTeX_Math" font-style="italic" font-size="16"><tspan font-family="KaTeX_Main" font-style="normal">∂</tspan>{letter}</text>'
        )

    _p = (_r * _c, _r * _s)
    _dr = (_p[0] + _c, _p[1] + _s)
    _dth = (_p[0] - _r * _s, _p[1] + _r * _c)
    _px, _py = _at(*_p)
    _rx, _ry = _at(*_dr)
    _tx, _ty = _at(*_dth)
    _mx, _my = _at(_p[0] / 2 - 0.2 * _s, _p[1] / 2 + 0.2 * _c)
    _ax0, _ay0 = _at(0.34 * math.cos(_TH), 0.34 * math.sin(_TH))

    mo.vstack(
        [
            polar_r,
            mo.Html(f"""
    <div style="text-align: center;">
    <svg viewBox="0 36 305 309" style="display: block; margin: 0 auto; width: 305px; max-width: 100%;" role="img"
         aria-label="the point p at distance r from o, with the coordinate vectors d/dr, of length 1 along the ray, and d/dtheta, perpendicular to it and of length r">
      <line x1="20" y1="{_OY}" x2="288" y2="{_OY}" stroke="#000" stroke-width="1.1"/><polygon points="296,{_OY} 286,{_OY - 4} 286,{_OY + 4}" fill="#000"/>
      <line x1="{_OX}" y1="335" x2="{_OX}" y2="52" stroke="#000" stroke-width="1.1"/><polygon points="{_OX},44 {_OX - 4},54 {_OX + 4},54" fill="#000"/>
      <path d="M {_OX + 0.34 * _U:.1f} {_OY} A {0.34 * _U:.1f} {0.34 * _U:.1f} 0 0 0 {_ax0:.1f} {_ay0:.1f}" fill="none" stroke="{GREY}" stroke-width="1.2"/>
      <line x1="{_OX}" y1="{_OY}" x2="{_px:.1f}" y2="{_py:.1f}" stroke="{BLUE}" stroke-width="1.6"/>
      {_arrow(_p, _dr, ORANGE)}
      {_arrow(_p, _dth, ORANGE)}
      <circle cx="{_px:.1f}" cy="{_py:.1f}" r="4" fill="#000"/><circle cx="{_OX}" cy="{_OY}" r="3.6" fill="#000"/>
      {_name(_OX - 18, _OY + 22, "o")}
      {_name(_OX + 42, _OY - 6, "θ")}
      {_name(_mx, _my + 6, "r", BLUE, "middle")}
      {_name(_px + 10, _py + 21, "p")}
      {_ddx(_rx + 8, _ry + 2, "r")}
      {_ddx(_tx - 11, _ty - 26, "θ")}
    </svg>
    </div>
    """),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** &nbsp; $\mathbb{S}^2 = \{ (x, y, z) \in \mathbb{R}^3 \mid x^2 + y^2 + z^2 = 1 \}$

    $$
    \begin{aligned}
    (x, y, z) &\overset{\footnotesize \varphi_n}{=} \Big( \frac{2u}{1 + u^2 + v^2},\ \frac{2v}{1 + u^2 + v^2},\ \frac{-1 + u^2 + v^2}{1 + u^2 + v^2} \Big) \\[8pt]
    &\overset{\footnotesize \psi}{=} \big( \sin\phi\cos\theta,\ \sin\phi\sin\theta,\ \cos\phi \big)
    \end{aligned}
    $$

    $$
    \Longrightarrow \quad (u, v) = \big( \cot(\phi/2)\cos\theta,\ \cot(\phi/2)\sin\theta \big)
    $$

    $$
    X_p \overset{\footnotesize \varphi_n}{=} X^u \frac{\partial}{\partial u} + X^v \frac{\partial}{\partial v} \overset{\footnotesize \psi}{=} X^\phi \frac{\partial}{\partial \phi} + X^\theta \frac{\partial}{\partial \theta}
    $$

    $$
    \Longrightarrow \quad
    \begin{bmatrix} X^u \\ X^v \end{bmatrix}
    =
    \frac{-1}{2\sin(\phi/2)^2}
    \begin{bmatrix} \cos\theta & \sin\phi\sin\theta \\ \sin\theta & -\sin\phi\cos\theta \end{bmatrix}
    \begin{bmatrix} X^\phi \\ X^\theta \end{bmatrix}
    $$

    $$
    \begin{aligned}
    g(X, Y) &\overset{\footnotesize \varphi_n}{=} \frac{4}{(1 + u^2 + v^2)^2} \big( X^u Y^u + X^v Y^v \big) \\[10pt]
    &\overset{\footnotesize \psi}{=} X^\phi Y^\phi + (\sin\phi)^2\, X^\theta Y^\theta \qquad (\text{round metric on } \mathbb{S}^2) \\[10pt]
    &\overset{\footnotesize \varphi_s}{=} \frac{4}{(1 + \tilde u^2 + \tilde v^2)^2} \big( X^{\tilde u} Y^{\tilde u} + X^{\tilde v} Y^{\tilde v} \big)
    \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(
        r"""
    Given a Riemannian metric $g$ on $M$ and given $\gamma : [a, b] \to M$ a path segment on $M$

    $$
    \mathrm{length}_g(\gamma) = \int_a^b \sqrt{g_{\gamma(t)}\big(\gamma'(t), \gamma'(t)\big)}\, dt
    $$
    """,
        "Length",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** &nbsp; $\gamma : [0, 2\pi] \longrightarrow \mathbb{S}^2$, &nbsp; $t \longmapsto \big( \sin(\phi_0)\cos(t),\ \sin(\phi_0)\sin(t),\ \cos(\phi_0) \big)$
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, GREY, SPHERE_OUTLINE, np, panel, sphere_flat, turntable):
    # ---- Figure: the path gamma on the sphere (the PDF's sketch) ------------
    _phi0 = 1.0
    _t = np.linspace(0, 2 * np.pi, 241)
    turntable(
        20,
        18,
        "the sphere with the points n and s, and the circle gamma at height z = cos(phi_0)",
        [
            panel(
                1.0,
                surfaces=[sphere_flat()],
                outlines=[SPHERE_OUTLINE],
                lines=[
                    ([0, 0], [0, 0], [-1, 1], GREY, 1.1),
                    (np.sin(_phi0) * np.cos(_t), np.sin(_phi0) * np.sin(_t), np.cos(_phi0) * np.ones_like(_t), BLUE, 2.4),
                    ([0, 0], [0, 0], [-0.001, 0.001], "#000000", 6.0, None, 1.2),  # the centre: a dot of the kit would lie under the see-through sphere
                ],
                points=[((0, 0, 1), "#000000", 3.6), ((0, 0, -1), "#000000", 3.6), ((0, 0, np.cos(_phi0)), "#000000", 2.6)],
                axes=[((0, 0, 0), (1.4, 0, 0), "x", 208), ((0, 0, 0), (0, 1.4, 0), "y", -8), ((0, 0, 0), (0, 0, 1.4), "z", 90)],
                texts=[
                    ((0, 0, 1), "n", "#000000", 180, 8),  # left of n, clear of the z axis
                    ((0, 0, -1), "s", "#000000", -90, 7),
                    # on the axis, 131 px to the right: 10 px past the sphere's edge (its radius is about 121 px at width 380 with this box)
                    ((0, 0, np.cos(_phi0)), r"z = \cos(\phi_0)", "#000000", 0, 131),
                ],
                box=((-0.85, 0.85), (-0.85, 0.85), (-0.85, 0.85)),
            )
        ],
        height=300,
        width=380,
        key="L14-latitude",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <span class="chain">$\displaystyle \varphi_n \quad \begin{bmatrix} u(t) \\ v(t) \end{bmatrix} = \begin{bmatrix} \cot(\phi_0/2)\cos(t) \\ \cot(\phi_0/2)\sin(t) \end{bmatrix} = \cot(\phi_0/2) \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix}$ $\displaystyle \qquad \begin{bmatrix} u'(t) \\ v'(t) \end{bmatrix} = \cot(\phi_0/2) \begin{bmatrix} -\sin(t) \\ \cos(t) \end{bmatrix}$</span>

    <span class="chain">$\displaystyle \psi \quad \begin{bmatrix} \phi(t) \\ \theta(t) \end{bmatrix} = \begin{bmatrix} \phi_0 \\ t \end{bmatrix}, \quad \begin{bmatrix} \phi'(t) \\ \theta'(t) \end{bmatrix} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$</span>

    $$
    \begin{aligned}
    g_{\gamma(t)}\big(\gamma'(t), \gamma'(t)\big) &= \frac{4}{\big(1 + u(t)^2 + v(t)^2\big)^2} \big( u'(t)^2 + v'(t)^2 \big) \\[10pt]
    &= \frac{4}{\big(1 + \cot(\phi_0/2)^2\big)^2}\, \cot(\phi_0/2)^2 = \sin(\phi_0)^2 \\[10pt]
    &= \phi'(t)^2 + \sin(\phi(t))^2\, \theta'(t)^2
    \end{aligned}
    $$

    $$
    \Longrightarrow \quad \mathrm{length}_g(\gamma) = \int_0^{2\pi} \sqrt{\sin(\phi_0)^2}\, dt = 2\pi\sin(\phi_0)
    $$
    """)
    return


if __name__ == "__main__":
    app.run()
