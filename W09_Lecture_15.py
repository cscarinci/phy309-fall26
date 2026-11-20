import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 • Lecture 15 • Lorentzian metrics", css_file="phy309.css")


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
    import numpy as np

    # the course palette (figures only); BLUE is the one of the building blocks
    GREY, LIGHT, ORANGE = "#9a9a9a", "#e3ebf4", "#b9853f"
    return GREY, LIGHT, ORANGE, np


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

    def light_cone(t0, x0=0.0, y0=0.0, h=1.0, rim=1.2):
        """The double cone of slope 1 with vertex (x0, y0, t0) and height h on each side, with its two rims; returns the surface and its outline."""
        s, a = np.meshgrid(np.linspace(-h, h, 21), np.linspace(0, 2 * np.pi, 49), indexing="ij")
        return sheet(x0 + np.abs(s) * np.cos(a), y0 + np.abs(s) * np.sin(a), t0 + s, wire=[(0, 20, GREY, rim)], alpha=0.3, tone=GREY), ("cone", (x0, y0, t0), h, GREY, rim)

    return SPHERE_OUTLINE, light_cone, sphere_flat


@app.cell(hide_code=True)
def _(header):
    header("Lecture 15", "Week 9", "Lecture 15 • Lorentzian metrics")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    Metric fields

    $$
    g : p \in M \longmapsto g_p : T_pM \times T_pM \longrightarrow \mathbb{R}
    $$

    assignment of <u>inner-product</u> on each tangent space &nbsp; <span class="nw">$\leadsto$ &nbsp; symmetric, bilinear &emsp; Euclidean or Minkowski</span>

    $\leadsto$ &nbsp; given $X_p, Y_p \in T_pM$, &nbsp; $g_p(X_p, Y_p) \in \mathbb{R}$ is well-defined independent of charts<br>
    but we can always choose charts and work with local coordinates and components

    $$
    g_p(X_p, Y_p) \overset{\varphi}{=} X^i(p)\, g_{ij}(p)\, Y^j(p) \overset{\tilde\varphi}{=} \tilde X^k(p)\, \tilde g_{kl}(p)\, \tilde Y^l(p)
    $$

    $$
    \Longleftrightarrow \quad g_{ij}(p) = \frac{\partial \tilde x^k}{\partial x^i}(p)\, \tilde g_{kl}(p)\, \frac{\partial \tilde x^l}{\partial x^j}(p)
    $$

    **Recall.** &nbsp; $X \in \Gamma(TM)$ smooth vector field

    $$
    \begin{aligned}
    & X : p \in M \longrightarrow X_p \in T_pM \\[6pt]
    & \quad \begin{aligned}
    \leadsto \quad X : C^\infty(M, \mathbb{R}) &\longrightarrow C^\infty(M, \mathbb{R}) \\
    f &\longmapsto X(f) : p \mapsto X_p(f)
    \end{aligned}
    \end{aligned}
    $$

    A smooth metric field $g \in \Gamma(\underbrace{T^*M \otimes T^*M}_{\footnotesize \mathclap{\text{will explain notation later}}\rule[-0.35em]{0pt}{0pt}})$

    $$
    \begin{aligned}
    g : \Gamma(TM) \times \Gamma(TM) &\longrightarrow C^\infty(M, \mathbb{R}) \\
    (X, Y) &\longmapsto g(X, Y) : p \mapsto g_p(X_p, Y_p)
    \end{aligned}
    $$

    $\leadsto$ &nbsp; inner-product of smooth vector fields taking values on smooth functions
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** &nbsp; $\mathbb{S}^2$

    $$
    X \overset{\varphi_n}{=} X^u\, \partial_u + X^v\, \partial_v \overset{\psi}{=} X^\phi\, \partial_\phi + X^\theta\, \partial_\theta \overset{\varphi_s}{=} X^{\tilde u}\, \partial_{\tilde u} + X^{\tilde v}\, \partial_{\tilde v}
    $$

    $$
    \begin{aligned}
    g(X, Y) &\overset{\varphi_n}{=} \frac{4\,(X^u Y^u + X^v Y^v)}{(1 + u^2 + v^2)^2} && (\text{on } \mathbb{S}^2 - \{n\}) \\[10pt]
    &\overset{\psi}{=} X^\phi Y^\phi + (\sin\phi)^2\, X^\theta Y^\theta && (\text{on } \mathbb{S}^2 - \{\text{meridian}\}) \\[10pt]
    &\overset{\varphi_s}{=} \frac{4\,(X^{\tilde u} Y^{\tilde u} + X^{\tilde v} Y^{\tilde v})}{(1 + \tilde u^2 + \tilde v^2)^2} && (\text{on } \mathbb{S}^2 - \{s\})
    \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, GREY, ORANGE, SPHERE_OUTLINE, np, panel, patch, sphere_flat, turntable):
    # ---- Figure: the angles of psi and the projections of phi_n and phi_s (the sketch of p. 2) ---
    _ph, _th = np.radians(40), np.radians(45)
    _P = np.array([np.sin(_ph) * np.cos(_th), np.sin(_ph) * np.sin(_th), np.cos(_ph)])
    _Q = np.array([np.cos(_th), np.sin(_th), 0.0]) / np.tan(_ph / 2)  # (u, v, 0)
    _I = np.array([np.cos(_th), np.sin(_th), 0.0]) * np.tan(_ph / 2)  # (u~, v~, 0)
    _n, _sp, _o = np.array([0.0, 0.0, 1.0]), np.array([0.0, 0.0, -1.0]), np.zeros(3)
    _plane = [(-1.4, -1.4, 0), (2.3, -1.4, 0), (2.3, 2.5, 0), (-1.4, 2.5, 0)]
    _s = np.linspace(0, 1, 40)[:, None]
    _t = np.linspace(0, 1, 30)[:, None]
    _a = np.linspace(0, 1, 40)
    _eq = np.linspace(0, 2 * np.pi, 121)
    _edge = np.array(_plane + _plane[:1])
    _k = np.array([-1.0, 1.0])
    _ar = 0.2  # radius of the arc of theta

    def _dashed(p, q):  # the line from s, dashed, in one piece through its points
        return (*(p + _t * (q - p)).T, BLUE, 2.0, [6, 4], 2.5)

    turntable(
        -10,
        40,
        "the unit sphere with the plane z = 0, the angles phi and theta of a point of the sphere, the line from the top of the sphere n through that point to (u, v, 0), and the dashed line from the bottom of the sphere s to that point, which meets the plane at (u~, v~, 0)",
        [
            panel(
                1.0,
                surfaces=[sphere_flat(), patch(_plane, "#ececec", 0.6, n=16)],
                outlines=[SPHERE_OUTLINE],
                lines=[
                    _dashed(_sp, _P),
                    (*_edge.T, GREY, 1.2),
                    (np.cos(_eq), np.sin(_eq), 0 * _eq, GREY, 1.0),
                    (0 * _k, 0 * _k, _k, GREY, 1.0),
                    (*(_o + _s * (_Q - _o)).T, GREY, 1.0),
                    (*(_n + _s * (_Q - _n)).T, BLUE, 2.0, None, 2.5),
                    (*(_o + _s * (_P - _o)).T, ORANGE, 1.8),
                    (0.3 * np.sin(_ph * _a) * np.cos(_th), 0.3 * np.sin(_ph * _a) * np.sin(_th), 0.3 * np.cos(_ph * _a), ORANGE, 1.4),
                    (_ar * np.cos(_th * _a), _ar * np.sin(_th * _a), 0 * _a, ORANGE, 1.4),
                ],
                points=[(tuple(_sp), "#000000", 3.4), (tuple(_I), BLUE, 4.0, True), (tuple(_n), "#000000", 3.4), (tuple(_P), "#000000", 3.4), (tuple(_Q), BLUE, 4.0), (tuple(_o), "#000000", 2.6)],
                axes=[((0, 0, 0), (0.6, 0, 0), "e_1", 180), ((0, 0, 0), (0, 0.6, 0), "e_2", 90), ((0, 0, 0), (0, 0, 0.6), "e_3", 150)],
                texts=[
                    (tuple(0.5 * np.array([np.sin(_ph / 2) * np.cos(_th), np.sin(_ph / 2) * np.sin(_th), np.cos(_ph / 2)])), r"\phi", ORANGE, 0, 0),
                    ((_ar * np.cos(_th / 2), _ar * np.sin(_th / 2), 0), r"\theta", ORANGE, -60, 5),
                    (tuple(_Q), "(u, v, 0)", "#000000", 30, 7),
                    (tuple(_P), "(x, y, z)", "#000000", 150, 7),
                    (tuple(_n), "n", "#000000", 90, 6),
                    (tuple(_sp), "s", "#000000", -90, 6),
                    (tuple(_I), r"(\tilde u, \tilde v, 0)", "#000000", 20, 16),
                ],
            )
        ],
        height=380,
        bias=0.12,
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    $$
    \begin{aligned}
    \leadsto \quad X &\overset{\varphi_n}{=} \begin{bmatrix} X^u \\ X^v \end{bmatrix} \overset{\psi}{=} \begin{bmatrix} X^\phi \\ X^\theta \end{bmatrix} \\[14pt]
    g &\overset{\varphi_n}{=} \underbrace{\begin{bmatrix} \dfrac{4}{(1 + u^2 + v^2)^2} & 0 \\ 0 & \dfrac{4}{(1 + u^2 + v^2)^2} \end{bmatrix}}_{\footnotesize g(u, v)} \overset{\psi}{=} \underbrace{\begin{bmatrix} 1 & 0 \\ 0 & (\sin\phi)^2 \end{bmatrix}}_{\footnotesize g(\phi, \theta)}
    \end{aligned}
    $$

    $$
    (u, v) = \varphi_n \circ \psi^{-1}(\phi, \theta) = \big( \cot(\phi/2) \cos\theta,\ \cot(\phi/2) \sin\theta \big)
    $$

    $$
    \frac{\partial(u, v)}{\partial(\phi, \theta)} = -\frac{1}{2\,(\sin(\phi/2))^2} \begin{bmatrix} \cos\theta & \sin\phi \sin\theta \\ \sin\theta & -\sin\phi \cos\theta \end{bmatrix}
    $$

    $$
    \Longrightarrow \quad g(\phi, \theta) = \frac{\partial(u, v)}{\partial(\phi, \theta)}^{T} g(u, v)\, \frac{\partial(u, v)}{\partial(\phi, \theta)} \qquad \text{check!}
    $$
    """
            ),
            definition(
                r"""
    Given a Riemannian metric $g$ on $M$ and a path segment $\gamma : [a, b] \to M$

    $$
    \mathrm{length}_g(\gamma) = \int_a^b \sqrt{g_{\gamma(t)}\big(\gamma'(t), \gamma'(t)\big)}\, dt
    $$
    """,
                "Length",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.**

    $$
    \begin{aligned}
    \gamma : [0, 2\pi] &\longrightarrow \mathbb{S}^2 \\
    t &\longmapsto \big( \sin(\phi_0) \cos(t),\ \sin(\phi_0) \sin(t),\ \cos(\phi_0) \big)
    \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, GREY, SPHERE_OUTLINE, np, panel, sphere_flat, turntable):
    # ---- Figure: the latitude z = cos(phi_0) (the sketch of p. 3) ---------------
    _ph = np.radians(50)
    _t = np.linspace(0, 2 * np.pi, 121)
    _k = np.array([-1.0, 1.0])
    turntable(
        20,
        15,
        "the unit sphere with its poles n and s and the circle z = cos(phi_0)",
        [
            panel(
                1.0,
                surfaces=[sphere_flat()],
                outlines=[SPHERE_OUTLINE],
                lines=[(np.sin(_ph) * np.cos(_t), np.sin(_ph) * np.sin(_t), np.cos(_ph) + 0 * _t, BLUE, 2.4), (0 * _k, 0 * _k, _k, GREY, 1.0)],
                points=[((0, 0, 1), "#000000", 3.4), ((0, 0, -1), "#000000", 3.4), ((0, 0, 0), GREY, 2.6), ((0, 0, np.cos(_ph)), BLUE, 2.6)],
                axes=[((0, 0, 0), (1.4, 0, 0), "x", 208), ((0, 0, 0), (0, 1.4, 0), "y", -8), ((0, 0, 0), (0, 0, 1.4), "z", 90)],
                texts=[
                    ((0, 0, 1), "n", "#000000", 180, 8),  # left of n, clear of the z axis
                    ((0, 0, -1), "s", "#000000", -90),
                    ((0, 0, np.cos(_ph)), r"z = \cos(\phi_0)", BLUE, 0, 128),
                ],
                box=((-0.85, 0.85), (-0.85, 0.85), (-0.85, 0.85)),
            )
        ],
        height=300,
        width=380,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    \begin{aligned}
    \varphi_n \quad \begin{bmatrix} u(t) \\ v(t) \end{bmatrix} &= \begin{bmatrix} \cot(\phi_0/2) \cos(t) \\ \cot(\phi_0/2) \sin(t) \end{bmatrix} = \cot(\phi_0/2) \begin{bmatrix} \cos(t) \\ \sin(t) \end{bmatrix} \\[14pt]
    \begin{bmatrix} u'(t) \\ v'(t) \end{bmatrix} &= \cot(\phi_0/2) \begin{bmatrix} -\sin(t) \\ \cos(t) \end{bmatrix} \\[14pt]
    \psi \quad \begin{bmatrix} \phi(t) \\ \theta(t) \end{bmatrix} &= \begin{bmatrix} \phi_0 \\ t \end{bmatrix}, \qquad \begin{bmatrix} \phi'(t) \\ \theta'(t) \end{bmatrix} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}
    \end{aligned}
    $$

    $$
    \begin{aligned}
    g_{\gamma(t)}\big(\gamma'(t), \gamma'(t)\big) &= \frac{4}{(1 + u(t)^2 + v(t)^2)^2} \big( u'(t)^2 + v'(t)^2 \big) \\[10pt]
    &= \frac{4}{(1 + \cot(\phi_0/2)^2)^2}\, \cot(\phi_0/2)^2 = \sin(\phi_0)^2 \\[10pt]
    &= \phi'(t)^2 + \sin(\phi(t))^2\, \theta'(t)^2
    \end{aligned}
    $$

    $$
    \Longrightarrow \quad \mathrm{length}_g(\gamma) = \int_0^{2\pi} \sqrt{\sin(\phi_0)^2}\, dt = 2\pi \sin(\phi_0)
    $$

    **In this lecture:** Lorentzian metrics

    **References:** <span style="white-space: nowrap">Schutz 6.2, 10.2;</span> <span style="white-space: nowrap">Carroll 2.5, 2.7, 5.1;</span> <span style="white-space: nowrap">Sasane 5.1–5.3</span>

    ## III.2 &nbsp; Lorentzian metrics
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            definition(
                r"""
    Given a Lorentzian metric $g$ on $M$, tangent space $T_pM$ decomposes into

    $$
    \begin{alignedat}{2}
    \bullet \ \ & \text{spacelike vectors} \ \ && X_p \in T_pM \text{ such that } g_p(X_p, X_p) > 0 \\[4pt]
    \bullet \ \ & \text{timelike vectors} \ \ && X_p \in T_pM \text{ such that } g_p(X_p, X_p) < 0 \\[4pt]
    \bullet \ \ & \text{lightlike vectors} \ \ && X_p \in T_pM \text{ such that } g_p(X_p, X_p) = 0 \ \ X_p \neq 0
    \end{alignedat}
    $$

    $\leadsto$ &nbsp; all independent of any choice of charts
    """,
                "Spacelike, timelike, lightlike",
            ),
            mo.md(
                r"""
    **Remark.** In $\mathbb{M}^4$, a choice of a single timelike vector $e_0$ is enough to determine the notion of “future” and “past” &nbsp; <span class="nw">(the “upper side” of the lightcone)</span>

    “future” timelike vectors $u$ are those that $\eta(e_0, u) < 0$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    cone_a = mo.ui.slider(0, 180, 5, value=30, label=r"direction of $X$", show_value=False)
    return (cone_a,)


@app.cell(hide_code=True)
def _(BLUE, ORANGE, cone_a, light_cone, mo, np, panel, turntable):
    # ---- Widget: the lightcone with e_0 and a vector X (the sketch of p. 4, where X is the future timelike u) --------
    # X makes the angle a with the t axis in the drawing, on the left of the screen; a = 0..180 turns it from the
    # future cone, through the cone (a = 45), outside it, through the cone again (a = 135), into the past cone
    _s, _o = light_cone(0.0)
    _right = np.array([-np.sin(np.radians(25)), np.cos(np.radians(25)), 0.0])  # right on the screen in the first view
    _a = np.radians(cone_a.value)
    _e0 = 0.26 * _right + np.array([0, 0, 0.62])
    _X = 0.87 * (-np.sin(_a) * _right + np.array([0, 0, np.cos(_a)]))
    _eta = lambda p, q: -p[2] * q[2] + p[0] * q[0] + p[1] * q[1]
    _xx, _ex = _eta(_X, _X), _eta(_e0, _X)
    if abs(_xx) < 1e-9:
        _kind = r"$\eta(X, X) = 0$ &nbsp; and &nbsp; $\eta(e_0, X) " + ("<" if _ex < 0 else ">") + r" 0$ &nbsp; $\Longrightarrow$ &nbsp; $X$ lightlike, " + ("future" if _ex < 0 else "past")
    elif _xx < 0:
        _kind = r"$\eta(X, X) < 0$ &nbsp; and &nbsp; $\eta(e_0, X) " + ("<" if _ex < 0 else ">") + r" 0$ &nbsp; $\Longrightarrow$ &nbsp; $X$ timelike, " + ("future" if _ex < 0 else "past")
    else:
        _kind = r"$\eta(X, X) > 0$ &nbsp; $\Longrightarrow$ &nbsp; $X$ spacelike"
    _fig = turntable(
        25,
        12,
        "the lightcone at a point, with the timelike vector e_0 and a vector X in the chosen direction: inside the upper half of the cone, on it, outside it, or inside its lower half",
        [panel(1.0, surfaces=[_s], outlines=[_o], arrows=[((0, 0, 0), tuple(_e0), ORANGE), ((0, 0, 0), tuple(_X), BLUE)], points=[((0, 0, 0), "#000000", 3.0)], texts=[(tuple(_e0), "e_0", ORANGE, 0), (tuple(_X), "X", BLUE, 180)])],
        height=300,
        width=420,
        key="L15-cone",
        apart=True,
    )
    mo.vstack([mo.hstack([cone_a, mo.md(_kind)], justify="start", gap=2, wrap=True), _fig])
    return


@app.cell(hide_code=True)
def _(frame):
    frame("L15-cone", 300)
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            definition(
                r"""
    For $(M, g)$ Lorentzian manifold, a time orientation is a choice of a <u>globally defined</u> timelike vector field &nbsp; <span class="nw">$\leadsto$ &nbsp; defined at every point</span>

    $$
    T \in \Gamma(TM) \ \text{ such that } \ g(T, T) < 0 \ \text{ everywhere on } M
    $$
    """,
                "Time orientation",
            ),
            mo.md(
                r"""
    $\Longrightarrow$ &nbsp; defines a notion of “future” or of “<u>moving forwards in time</u>” &nbsp; <span class="nw">$\leadsto$ &nbsp; we don't have yet a proper notion of time!</span>
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, GREY, ORANGE, mo, np):
    # ---- Figure: a time orientation on M (the sketch of p. 4): static, a flat drawing with nothing to turn ---------
    def _xy(x, y):
        return x * 112 + 215, 160 - y * 112

    def _path(xs, ys, close=False):
        pts = [_xy(x, y) for x, y in zip(xs, ys)]
        return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + (" Z" if close else "")

    _a = np.linspace(0, 2 * np.pi, 241)
    _r = 1 + 0.08 * np.cos(2 * _a + 1) + 0.06 * np.cos(3 * _a + 2.4) + 0.04 * np.sin(5 * _a)
    _blob = _path(1.4 * _r * np.cos(_a), 1.05 * _r * np.sin(_a), close=True)
    _y = np.linspace(-1.3, 1.3, 100)
    _curves = "".join(f'<path d="{_path(_c - 0.35 * _y - 0.06 * _y**2, _y)}" fill="none" stroke="{BLUE}" stroke-width="1.5"/>' for _c in (-0.9, -0.45, 0.0, 0.45, 0.9))
    _arrows = []
    def _on(c, y):
        return np.array([c - 0.35 * y - 0.06 * y**2, y])

    for _c, _y0, _dy in ((-0.9, -0.3, 0.36), (-0.45, -0.6, 0.36), (-0.45, 0.25, 0.36), (0.0, -0.8, 0.36), (0.0, 0.05, 0.36), (0.45, -0.5, 0.36), (0.45, 0.35, 0.36), (0.9, -0.45, 0.36), (0.9, 0.2, 0.36)):
        _x1, _y1 = _xy(*_on(_c, _y0))
        _x2, _y2 = _xy(*_on(_c, _y0 + _dy))
        _u = np.array([_x2 - _x1, _y2 - _y1]) / np.hypot(_x2 - _x1, _y2 - _y1)
        _b = np.array([_x2, _y2]) - 9 * _u
        _w = 3.4 * np.array([-_u[1], _u[0]])
        _arrows.append(f'<line x1="{_x1:.1f}" y1="{_y1:.1f}" x2="{_b[0]:.1f}" y2="{_b[1]:.1f}" stroke="{ORANGE}" stroke-width="2.2" stroke-linecap="round"/>'
                       f'<polygon points="{_x2:.1f},{_y2:.1f} {_b[0] + _w[0]:.1f},{_b[1] + _w[1]:.1f} {_b[0] - _w[0]:.1f},{_b[1] - _w[1]:.1f}" fill="{ORANGE}"/>')
    mo.Html(f"""
    <svg viewBox="0 0 430 320" role="img" aria-label="a region M filled with curves and with timelike arrows pointing roughly in the same direction" style="display: block; margin: 0 auto; width: 100%; max-width: 430px; height: auto">
      <defs><clipPath id="L15-blob"><path d="{_blob}"/></clipPath></defs>
      <g clip-path="url(#L15-blob)">{_curves}</g>
      {''.join(_arrows)}
      <path d="{_blob}" fill="none" stroke="{GREY}" stroke-width="1.8"/>
      <text x="392" y="48" font-size="21" style="font-family: KaTeX_Math, serif; font-style: italic" text-anchor="middle">M</text>
    </svg>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\leadsto$ &nbsp; some Lorentzian manifolds don't admit time orientation, but we will assume ours do!
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(
        r"""
    A particle in a Lorentzian manifold $(M, g)$ is a path $\gamma : \mathbb{R} \to M$ such that $\gamma'(t)$ is timelike and <u>future oriented</u> for all $t \in \mathbb{R}$ &nbsp; <span class="nw">$\leadsto$ &nbsp; $g_{\gamma(t)}\big(T_{\gamma(t)}, \gamma'(t)\big) < 0$</span>
    """,
        "Particle",
    )
    return


@app.cell(hide_code=True)
def _(BLUE, GREY, ORANGE, light_cone, np, panel, sheet, turntable):
    # ---- Figure: a particle with light cones at three events (the sketch of p. 5) ----------
    _a0 = np.radians(30)
    _right, _deep, _up = np.array([-np.sin(_a0), np.cos(_a0), 0.0]), np.array([np.cos(_a0), np.sin(_a0), 0.0]), np.array([0.0, 0.0, 1.0])

    def _gamma(t):
        t = np.asarray(t, float)
        return (0.6 * (1 + np.tanh((t - 1.2) / 0.8)))[..., None] * _right + (0.15 * (1 - np.cos(0.8 * t)))[..., None] * _deep + t[..., None] * _up

    def _velocity(t):
        return 0.75 / np.cosh((t - 1.2) / 0.8) ** 2 * _right + 0.12 * np.sin(0.8 * t) * _deep + _up

    def _tilted(p, tau, h):
        """The double cone with vertex p, of height h on each side and slope 1 about its axis, the axis leaning by tau to the right of the first view."""
        axis, across = np.cos(tau) * _up + np.sin(tau) * _right, np.cos(tau) * _right - np.sin(tau) * _up
        s, a = np.meshgrid(np.linspace(-h, h, 21), np.linspace(0, 2 * np.pi, 49), indexing="ij")
        q = p + s[..., None] * axis + (np.abs(s) * np.cos(a))[..., None] * across + (np.abs(s) * np.sin(a))[..., None] * _deep
        return sheet(q[..., 0], q[..., 1], q[..., 2], alpha=0.3, tone=GREY, edge=(GREY, 1.0))

    _c = _gamma(np.linspace(-0.3, 3.5, 200))
    _low, _mid, _top = _gamma(0.4), _gamma(1.6), _gamma(2.8)
    _tip = _low + 0.6 * _velocity(0.4)
    _cl, _ct = light_cone(_low[2], _low[0], _low[1], h=0.4, rim=1.0), light_cone(_top[2], _top[0], _top[1], h=0.4, rim=1.0)
    turntable(
        30,
        12,
        "a particle gamma with light cones at three events, the middle cone tilted, and its velocity gamma' at the lowest event",
        [
            panel(
                1.0,
                surfaces=[_cl[0], _tilted(_mid, np.radians(25), 0.4), _ct[0]],
                outlines=[_cl[1], _ct[1]],
                lines=[(*_c.T, BLUE, 1.8)],
                arrows=[(tuple(_low), tuple(_tip), ORANGE)],
                points=[(tuple(_low), BLUE, 3.4)],
                texts=[(tuple(_low), r"\gamma(t)", "#000000", 0, 14), (tuple(_tip), r"\gamma'(t)", ORANGE, 180)],
            )
        ],
        height=380,
        width=460,
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    The proper time length of a <u>particle segment</u> &nbsp; <span class="nw">$\leadsto$ &nbsp; a segment of the particle's history</span>

    $$
    \gamma : [a, b] \to M \ \text{ is } \ \mathrm{time}_g(\gamma) = \underbrace{\int_a^b \sqrt{-g_{\gamma(t)}\big(\gamma'(t), \gamma'(t)\big)}\, dt}_{\footnotesize \mathclap{\begin{matrix} \text{independent of the choice} \\ \text{of parameter } t \end{matrix}}}
    $$

    $\leadsto$ &nbsp; $\gamma(t)$ is said to be parameterized by proper time if

    $$
    \begin{aligned}
    & g_{\gamma(t)}\big(\gamma'(t), \gamma'(t)\big) = -1 \\[10pt]
    & \quad \begin{aligned}
    \Longrightarrow \quad & \mathrm{time}_g(\gamma) = \int_a^b dt = b - a \\[10pt]
    \Longrightarrow \quad & t \text{ is the proper time parameter of } \gamma
    \end{aligned}
    \end{aligned}
    $$
    """
            ),
            definition(
                r"""
    A lightlike particle in $(M, g)$ is a path $\gamma : \mathbb{R} \to M$ such that $\gamma'(t)$ is future oriented lightlike $\forall\, t \in \mathbb{R}$
    """,
                "Lightlike particle",
            ),
            mo.md(
                r"""
    $\leadsto$ &nbsp; lightlike particles have <u>no invariant notion</u> of time! &nbsp; <span class="nw">$\leadsto$ &nbsp; no physical notion</span>

    **Example** (Schwarzschild spacetime) &nbsp; $\leadsto$ &nbsp; geometry of spacetime around a static, spherical star / black hole

    $$
    M = \mathbb{R} \times (r_0, +\infty) \times \mathbb{S}^2
    $$

    $$
    \Phi(t, r, \smash[b]{\underbrace{x, y, z}_{\footnotesize \mathclap{x^2 + y^2 + z^2 = 1}}}) = \big( \overbrace{t,\ r}^{\footnotesize \mathclap{\begin{matrix} \text{identity charts on} \\ \mathbb{R} \text{ and } (r_0, +\infty) \end{matrix}}},\ \smash[b]{\underbrace{\varphi(x, y, z)}_{\footnotesize \mathclap{\text{chart on } \mathbb{S}^2}}} \big)
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, GREY, ORANGE, np, panel, sheet, turntable):
    # ---- Figure: Schwarzschild, the two lines of the sketch of p. 5 drawn as a cylinder -----------
    _s, _a = np.meshgrid(np.linspace(-1.0, 1.6, 14), np.linspace(0, 2 * np.pi, 49), indexing="ij")
    _ang = np.linspace(0, 2 * np.pi, 121)
    _k = np.array([-1.0, 0.0])
    turntable(
        25,
        14,
        "the cylinder r = r_0 with two directions drawn, the outside region M, and the sphere at r = r_0, t = 0",
        [
            panel(
                1.0,
                surfaces=[sheet(np.cos(_a), np.sin(_a), _s, alpha=0.3, tone=BLUE)],
                outlines=[("cylinder", (0, 0), 1.0, (-1.0, 1.6), BLUE, 1.2)],
                lines=[(np.cos(_ang), np.sin(_ang), 0 * _ang, ORANGE, 2.2), (0 * _k, 0 * _k, _k, GREY, 1.1)],
                arrows=[((0, 0, 0), (0, 0, 1.9), GREY, 1.1), ((0, 0, 0), (0, 2.1, 0), GREY, 1.1)],
                texts=[
                    ((0, 0, 1.9), "t", GREY, 90),
                    ((0, 2.1, 0), "r", GREY, 0, 8),
                    ((0, 0, 1.1), r"M = \text{“outside” region}", BLUE, 0, 138),
                    ((0, 0, -0.5), r"\mathbb{S}^2 \text{ at } r = r_0,\ t = 0", ORANGE, 0, 138),
                ],
            )
        ],
        height=340,
        width=560,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    X \overset{\Phi_n}{=} \begin{bmatrix} X^t \\ X^r \\ X^u \\ X^v \end{bmatrix} \overset{\Psi}{=} \begin{bmatrix} X^t \\ X^r \\ X^\phi \\ X^\theta \end{bmatrix}
    $$

    $$
    \begin{aligned}
    g &\overset{\Phi_n}{=} \begin{bmatrix} -(1 - r_0/r) & 0 & 0 & 0 \\[4pt] 0 & (1 - r_0/r)^{-1} & 0 & 0 \\[4pt] 0 & 0 & \dfrac{4 r^2}{(1 + u^2 + v^2)^2} & 0 \\[4pt] 0 & 0 & 0 & \dfrac{4 r^2}{(1 + u^2 + v^2)^2} \end{bmatrix} \\[8pt]
    &\overset{\Psi}{=} \begin{bmatrix} -(1 - r_0/r) & 0 & 0 & 0 \\[4pt] 0 & (1 - r_0/r)^{-1} & 0 & 0 \\[4pt] 0 & 0 & r^2 & 0 \\[4pt] 0 & 0 & 0 & r^2 (\sin\phi)^2 \end{bmatrix}
    \end{aligned}
    $$

    $\leadsto$ &nbsp; static and spherical because it “looks the same” for every “time” and every “angle”
    """)
    return


if __name__ == "__main__":
    app.run()
