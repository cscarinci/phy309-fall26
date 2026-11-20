import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 • Lecture 19 • Connections on manifolds", css_file="phy309.css")


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
    GREY, LIGHT, ORANGE, RED = "#9a9a9a", "#e3ebf4", "#b9853f", "#a8554c"
    return GREY, LIGHT, ORANGE, RED, np


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
    header("Lecture 19", "Week 11", "Lecture 19 • Connections on manifolds")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    Covariant derivatives on manifolds

    $$
    \begin{gathered}
    \gamma(t) \overset{\varphi}{=} \varphi^{-1}\big(x^k(t)\, e_k\big) \overset{\tilde\varphi}{=} \tilde\varphi^{-1}\big(\tilde x^l(t)\, e_l\big) \\[6pt]
    X_{\gamma(t)} \overset{\varphi}{=} X^k(t)\, \partial_k\big|_{\gamma(t)} \overset{\tilde\varphi}{=} \tilde X^l(t)\, \tilde\partial_l\big|_{\gamma(t)}
    \end{gathered}
    $$

    $$
    \begin{aligned}
    \leadsto \quad \frac{D}{dt} X_{\gamma(t)} &\overset{\varphi}{=} \Big( \dot X^k(t) + \dot x^i(t)\, X^j(t)\, \Gamma^k_{ij}(t) \Big)\, \partial_k\big|_{\gamma(t)} \\[8pt]
    &\overset{\tilde\varphi}{=} \Big( \dot{\tilde X}{}^l(t) + \dot{\tilde x}{}^m(t)\, \tilde X^n(t)\, \tilde\Gamma^l_{mn}(t) \Big)\, \tilde\partial_l\big|_{\gamma(t)}
    \end{aligned}
    $$

    $$
    \begin{aligned}
    \Longleftrightarrow \quad \tilde x &= \tilde\varphi \circ \varphi^{-1}(x) & \qquad \dot{\tilde x}{}^l &= \frac{\partial \tilde x^l}{\partial x^k}\, \dot x^k \\[14pt]
    \tilde X^l &= \frac{\partial \tilde x^l}{\partial x^k}\, X^k & \qquad \dot{\tilde X}{}^l &= \frac{\partial \tilde x^l}{\partial x^k}\, \dot X^k + \underbrace{\frac{\partial^2 \tilde x^l}{\partial x^i \partial x^j}\, X^i \dot x^j}_{\footnotesize \text{non-tensorial}} \\[14pt]
    \tilde\partial_l &= \frac{\partial x^k}{\partial \tilde x^l}\, \partial_k & \qquad \Gamma^k_{ij} &= \frac{\partial x^k}{\partial \tilde x^l}\, \tilde\Gamma^l_{mn}\, \frac{\partial \tilde x^m}{\partial x^i}\, \frac{\partial \tilde x^n}{\partial x^j} + \underbrace{\frac{\partial x^k}{\partial \tilde x^l}\, \frac{\partial^2 \tilde x^l}{\partial x^i \partial x^j}}_{\footnotesize \text{non-tensorial}}
    \end{aligned}
    $$

    $\Longrightarrow$ &nbsp; Christoffel symbols are not components of tensors on $M$!

    **In this lecture:** connections on manifolds

    **References:** <span style="white-space: nowrap">Schutz 5.4, 6.3–6.4;</span> <span style="white-space: nowrap">Carroll 3.2–3.4;</span> <span style="white-space: nowrap">Sasane 6.1–6.4, 7.1–7.2, 8.1–8.3</span>

    ## IV.2 &nbsp; Connections on manifolds
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            definition(
                r"""
    A connection on $M$ is an operator

    <span class="chain">$\displaystyle \begin{aligned} \nabla : \Gamma(TM) \times \Gamma(TM) &\longrightarrow \Gamma(TM) \\ (X, Y) &\longmapsto \nabla_X Y \end{aligned}$ $\displaystyle \begin{aligned} & \\ & \quad \begin{array}{l} (\text{derivative of } Y \text{ in} \\ \quad \text{the direction of } X) \end{array} \end{aligned}$</span>

    satisfying:

    $$
    \begin{alignedat}{3} \text{i)} \quad & \nabla_{fX + gY} Z = f\, \nabla_X Z + g\, \nabla_Y Z & \quad & \forall\, X, Y, Z \in \Gamma(TM),\ \forall\, f, g \in C^\infty(M, \mathbb{R}) & \quad & (C^\infty(M, \mathbb{R})\text{-linearity}) \\[10pt] \text{ii)} \quad & \nabla_X (aY + bZ) = a\, \nabla_X Y + b\, \nabla_X Z & \quad & \forall\, X, Y, Z \in \Gamma(TM),\ \forall\, a, b \in \mathbb{R} & \quad & (\mathbb{R}\text{-linearity}) \\[10pt] \text{iii)} \quad & \nabla_X (fY) = X(f)\, Y + f\, \nabla_X Y & \quad & \forall\, X, Y \in \Gamma(TM),\ \forall\, f \in C^\infty(M, \mathbb{R}) & \quad & (\text{Leibniz rule}) \end{alignedat}
    $$
    """,
                "Connection",
            ),
            mo.md(
                r"""
    $X \overset{\varphi}{=} X^i\, \partial_i$, &nbsp; $Y \overset{\varphi}{=} Y^j\, \partial_j$

    $$
    \begin{aligned}
    \Longrightarrow \quad \nabla_X Y &\overset{\varphi}{=} (\nabla_X Y)^k\, \partial_k \\[8pt]
    &= \nabla_{X^i \partial_i} (Y^j\, \partial_j) = X^i\, \nabla_{\partial_i} (Y^j\, \partial_j) = (X^i\, \partial_i Y^j)\, \partial_j + X^i Y^j\, \nabla_{\partial_i} \partial_j
    \end{aligned}
    $$
    <span class="chain" style="text-align: left">$\displaystyle \Longrightarrow \quad \nabla_{\partial_i} \partial_j = \Gamma^k_{ij}\, \partial_k$ $\displaystyle \quad (C^\infty(M, \mathbb{R})\text{-linear combination of coordinate basis vector fields})$</span>

    Under a change of charts &nbsp; $\partial_i = \dfrac{\partial \tilde x^k}{\partial x^i}\, \tilde\partial_k$

    $$
    \begin{aligned}
    \Longrightarrow \quad & \nabla_{\partial_i} \partial_j = \nabla_{\frac{\partial \tilde x^k}{\partial x^i} \tilde\partial_k} \Big( \frac{\partial \tilde x^l}{\partial x^j}\, \tilde\partial_l \Big) \\[14pt]
    \Longrightarrow \quad & \Gamma^k_{ij} = \frac{\partial x^k}{\partial \tilde x^l}\, \tilde\Gamma^l_{mn}\, \frac{\partial \tilde x^m}{\partial x^i}\, \frac{\partial \tilde x^n}{\partial x^j} + \frac{\partial x^k}{\partial \tilde x^l}\, \frac{\partial^2 \tilde x^l}{\partial x^i \partial x^j} \ !
    \end{aligned}
    $$

    $\leadsto$ &nbsp; Christoffel symbols are components of connections on manifolds!

    **Remark.** Connections define covariant derivatives along paths.

    For $X \in \Gamma(TM)$ along a path $\gamma(t)$: &nbsp; $\dfrac{D}{dt} X_{\gamma(t)} = \nabla_{\gamma'(t)} X$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            theorem(
                r"""
    Given a metric field $g \in \Gamma(TM^0_2)$, there exists a unique connection <span style="white-space: nowrap">$\nabla : \Gamma(TM) \times \Gamma(TM) \longrightarrow \Gamma(TM)$</span> such that

    <span class="chain" style="text-align: left">$\displaystyle \bullet \quad X\big(g(Y, Z)\big) = g(\nabla_X Y, Z) + g(Y, \nabla_X Z) \kern 0.43em$ $\displaystyle \quad \leadsto \quad \nabla \text{ is “compatible with } g \text{”}$</span>
    <span class="chain" style="text-align: left">$\displaystyle \bullet \quad (\nabla_X Y - \nabla_Y X)\, f = X(Y(f)) - Y(X(f))$ $\displaystyle \quad \leadsto \quad \nabla \text{ is “torsion-free”}$</span>

    $\forall\, X, Y, Z \in \Gamma(TM)$, &nbsp; $\forall\, f \in C^\infty(M, \mathbb{R})$.
    """,
                "Levi-Civita connection",
            ),
            mo.md(
                r"""
    **Proof.** In a chart, take $X = \partial_i$, $Y = \partial_j$, $Z = \partial_k$

    <span class="chain" style="text-align: left">$\displaystyle \bullet \quad \partial_i g_{jk} = g(\Gamma^l_{ij}\, \partial_l, \partial_k) + g(\partial_j, \Gamma^l_{ik}\, \partial_l) = g_{lk}\, \Gamma^l_{ij} + g_{jl}\, \Gamma^l_{ik}$ $\displaystyle \quad \leadsto \quad (i, j, k) + (j, i, k) - (k, i, j) \quad \times\, g^{kl}$</span>
    <span class="chain" style="text-align: left">$\displaystyle \bullet \quad (\Gamma^k_{ij} - \Gamma^k_{ji})\, \partial_k f = \partial_i (\partial_j f) - \partial_j (\partial_i f) = 0 \iff \Gamma^k_{ij} = \Gamma^k_{ji}$</span>

    $$
    \Longrightarrow \quad \Gamma^k_{ij} = \frac{1}{2}\, g^{kl} \big( \partial_i g_{lj} + \partial_j g_{il} - \partial_l g_{ij} \big) \tag*{$\square$}
    $$

    **Example.** &nbsp; $M = \mathbb{S}^2$

    $$
    \begin{aligned}
    & \begin{aligned}
    g_{\mathbb{S}^2} &\overset{\psi}{=} d\phi \otimes d\phi + (\sin\phi)^2\, d\theta \otimes d\theta = \begin{bmatrix} 1 & 0 \\ 0 & (\sin\phi)^2 \end{bmatrix} \\[14pt]
    g^{-1}_{\mathbb{S}^2} &\overset{\psi}{=} \partial_\phi \otimes \partial_\phi + (\sin\phi)^{-2}\, \partial_\theta \otimes \partial_\theta = \begin{bmatrix} 1 & 0 \\ 0 & (\sin\phi)^{-2} \end{bmatrix}
    \end{aligned} \\[14pt]
    & \quad \begin{aligned}
    \Longrightarrow \quad \Gamma^\phi_{ij} &= \frac{1}{2}\, g^{\phi\phi} \big( \partial_i g_{\phi j} + \partial_j g_{i\phi} - \partial_\phi g_{ij} \big) = \begin{bmatrix} 0 & 0 \\ 0 & -\sin\phi\cos\phi \end{bmatrix} \\[14pt]
    \Longrightarrow \quad \Gamma^\theta_{ij} &= \frac{1}{2}\, g^{\theta\theta} \big( \partial_i g_{\theta j} + \partial_j g_{i\theta} - \partial_\theta g_{ij} \big) = \begin{bmatrix} 0 & \cot\phi \\ \cot\phi & 0 \end{bmatrix}
    \end{aligned}
    \end{aligned}
    $$

    $$
    \leadsto \ \ \nabla_{\partial_\phi} \partial_\phi = 0, \ \ \nabla_{\partial_\theta} \partial_\theta = -\sin\phi\cos\phi\, \partial_\phi, \ \ \nabla_{\partial_\phi} \partial_\theta = \nabla_{\partial_\theta} \partial_\phi = \cot\phi\, \partial_\theta
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            definition(
                r"""
    Given a path $\gamma$ on $M$, its acceleration is the vector field along $\gamma$ given by

    $$
    \begin{aligned}
    A_{\gamma(t)} &= \frac{D}{dt} \gamma'(t) \\[8pt]
    &= \nabla_{\gamma'(t)} X \\[8pt]
    &\overset{\varphi}{=} \Big( \ddot x^k(t) + \dot x^i(t)\, \dot x^j(t)\, \Gamma^k_{ij}(t) \Big)\, \partial_k\big|_{\gamma(t)} \qquad \begin{array}{l} (\text{where } \gamma \text{ is an integral} \\ \quad \text{curve of } X \in \Gamma(TM)) \end{array}
    \end{aligned}
    $$

    A geodesic is a path with zero acceleration

    $$
    \frac{D}{dt} \gamma'(t) = 0 \quad \overset{\varphi}{\Longleftrightarrow} \quad \ddot x^k + \dot x^i \dot x^j\, \Gamma^k_{ij} = 0 \quad \forall\, k
    $$

    $\leadsto$ &nbsp; non-linear 2nd order system of ODEs
    """,
                "Acceleration, geodesic",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, np):
    fig_a_phi = mo.ui.slider(steps=[round(float(k * np.pi / 36), 2) for k in range(3, 34)], value=0.79, label=r"$\phi_0$", show_value=False)
    return (fig_a_phi,)


@app.cell(hide_code=True)
def _(AZ_B, BLUE, BOTTOM_B, BOX_B, EL_B, HEIGHT_B, ORANGE, RED, SC_B, SPHERE_OUTLINE, TOP_B, T_B, WIDTH_B, beyond, fig_a_phi, first_view, mo, name_at, np, panel, pins, sphere_flat, turntable):
    # ---- Widget: the latitude gamma(t) = (phi_0, t), an integral curve of d_theta, and its acceleration ----
    # A = nabla_{d_theta} d_theta = -sin(phi_0) cos(phi_0) d_phi, with d_phi = (cos phi cos theta, cos phi sin theta, -sin phi) in R^3
    _ph = fig_a_phi.value
    _th = np.radians(AZ_B + 25)                       # the point shown: on the front of the sphere, between the x and y axes
    _axes = first_view(AZ_B, EL_B)
    _s = np.linspace(0, 2 * np.pi, 181)
    _p = np.array([np.sin(_ph) * np.cos(_th), np.sin(_ph) * np.sin(_th), np.cos(_ph)])
    _dphi = np.array([np.cos(_ph) * np.cos(_th), np.cos(_ph) * np.sin(_th), -np.sin(_ph)])
    _v = np.sin(_ph) * np.array([-np.sin(_th), np.cos(_th), 0.0])
    _A = -np.sin(_ph) * np.cos(_ph) * _dphi
    _zero = abs(np.cos(_ph)) < 0.01                   # the equator
    _arrows = [(_p, _p + _v, ORANGE, 1.8)]
    if not _zero:
        _arrows.append((_p, _p + _A, RED, 2.2))
    # the name of A sits past its tip and to the right, clear of the z axis; at the equator, below the point
    _d = np.array([34.0, -20.0]) if _zero else beyond(_p, _p + _A, 30, _axes) + np.array([20.0, 0.0])
    if not _zero and _ph < np.pi / 2:
        _d[0] = max(_d[0], 36 - (_p + _A) @ _axes[0] * SC_B)
    if _ph > 2.6:                                     # near the south pole the arrow is seen end-on: its name goes below the sphere
        _d[1] = min(_d[1], -172 - (_p + _A) @ _axes[1] * SC_B)
    # the name of gamma' sits above its tip; where that would meet the end of the y axis and its name, it goes above or below them
    _h = (_p + _v) @ _axes[1] * SC_B
    _y = _h + 12
    if -62 < _y < -14:
        _y = -14 if _y > -38 else -62
    _texts = [
        name_at(_p + _v, 30, _y - _h, r"\gamma'(t)", ORANGE, _axes, SC_B),
        name_at(_p if _zero else _p + _A, *_d, r"A_{\gamma(t)} = 0" if _zero else r"A_{\gamma(t)}", RED, _axes, SC_B),
    ] + pins(_axes[1], TOP_B, BOTTOM_B)
    _fig = turntable(
        AZ_B,
        EL_B,
        "the latitude of the sphere at the chosen phi_0, the point gamma(t) on it, its velocity gamma'(t) along the latitude, and its acceleration, tangent to the sphere along the meridian",
        [
            panel(
                1.0,
                surfaces=[sphere_flat()],
                outlines=[SPHERE_OUTLINE],
                lines=[(np.sin(_ph) * np.cos(_s), np.sin(_ph) * np.sin(_s), np.cos(_ph) * np.ones_like(_s), BLUE, 2.2)],
                points=[((0, 0, 0), "#000000", 2.6), (tuple(_p), "#000000", 3.6)],
                axes=[((0, 0, 0), (T_B, 0, 0), "x", 208), ((0, 0, 0), (0, T_B, 0), "y", -8), ((0, 0, 0), (0, 0, T_B), "z", 90)],
                arrows=_arrows,
                texts=_texts,
                box=BOX_B,
            )
        ],
        height=HEIGHT_B,
        width=WIDTH_B,
        key="L19-latitude",
        apart=True,
    )
    mo.vstack([mo.hstack([fig_a_phi], justify="start"), _fig])
    return


@app.cell(hide_code=True)
def _(HEIGHT_B, frame):
    frame("L19-latitude", HEIGHT_B)
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    $\leadsto$ &nbsp; they form a special family of paths on Riemannian / Lorentzian manifolds<br>
    Lorentzian &nbsp; $\leadsto$ &nbsp; particles / photons (if timelike / lightlike)
    """
            ),
            theorem(
                r"""
    If $\gamma$ is a geodesic then

    $$
    g_{\gamma(t)}\big(\gamma'(t), \gamma'(t)\big) = \text{constant along } \gamma
    $$
    """
            ),
            mo.md(
                r"""
    **Proof.** For any $X_{\gamma(t)}$, $Y_{\gamma(t)}$ vector fields along $\gamma(t)$

    $$
    g_{\gamma(t)}\big(X_{\gamma(t)}, Y_{\gamma(t)}\big) \overset{\varphi}{=} g_{ij}(t)\, X^i(t)\, Y^j(t)
    $$

    $$
    \begin{aligned}
    \Longrightarrow \, & \frac{d}{dt} \big( g_{\gamma(t)}(X_{\gamma(t)}, Y_{\gamma(t)}) \big) \overset{\varphi}{=} \partial_k g_{ij}\, X^i Y^j \dot x^k + g_{ij} \dot X^i Y^j + g_{ij} X^i \dot Y^j \\[6pt]
    & \qquad = g_{ij} \big( \dot X^i + \Gamma^i_{kl} \dot x^k X^l \big) Y^j + g_{ij} X^i \big( \dot Y^j + \Gamma^j_{kl} \dot x^k Y^l \big) \\[6pt]
    & \qquad = g_{\gamma(t)}\Big( \frac{D}{dt} X_{\gamma(t)}, Y_{\gamma(t)} \Big) + g_{\gamma(t)}\Big( X_{\gamma(t)}, \frac{D}{dt} Y_{\gamma(t)} \Big) \\[16pt]
    \Longrightarrow \, & \frac{d}{dt}\, g_{\gamma(t)}\big(\gamma'(t), \gamma'(t)\big) = 2\, g_{\gamma(t)}\Big( \frac{D}{dt} \gamma'(t), \gamma'(t) \Big) = 0
    \end{aligned}
    $$
    <span style="float: right; margin-top: -4.3em">$\square$</span>
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** &nbsp; $M = \mathbb{S}^2$, &nbsp; $\gamma(t) \overset{\psi}{=} (\phi(t), \theta(t))$ geodesic

    $$
    \begin{aligned}
    &\Longleftrightarrow \ \begin{cases} \ddot\theta + \Gamma^\theta_{ij}\, \dot x^i \dot x^j = 0 \\[4pt] \ddot\phi + \Gamma^\phi_{ij}\, \dot x^i \dot x^j = 0 \end{cases}
    \quad \Longleftrightarrow \quad \begin{cases} \ddot\theta + 2\cot\phi\, \dot\phi\, \dot\theta = 0 \\[4pt] \ddot\phi - \sin\phi\cos\phi\, (\dot\theta)^2 = 0 \end{cases} \\[18pt]
    &\Longleftrightarrow \ \begin{cases} \dfrac{d}{dt} \big( \dot\theta (\sin\phi)^2 \big) = 0 & \leadsto \ \dot\theta\, (\sin\phi)^2 = L \\[12pt] \dfrac{d}{dt} \Big( \dot\phi^2 + \dfrac{L^2}{(\sin\phi)^2} \Big) = 0 & \leadsto \ \dot\phi^2 + \dfrac{L^2}{(\sin\phi)^2} = \underset{\mathclap{\textstyle g_{\mathbb{S}^2}(\gamma', \gamma')}}{\underset{\textstyle \|}{\rule[-3pt]{0pt}{0pt}k}} \end{cases}
    \end{aligned}
    $$

    Note $\gamma'(t) = (\dot\phi(t), \dot\theta(t))$

    $$
    \Longrightarrow \quad g_{\mathbb{S}^2}(\gamma', \gamma') = \dot\phi^2 + (\sin\phi)^2\, \dot\theta^2 = k
    $$

    $$
    \begin{aligned}
    \text{For } L = 0 \quad &\Longrightarrow \quad \theta = \theta_0 \qquad \phi = \sqrt{k}\, t + \phi_0 \quad (\text{meridians}) \\[14pt]
    \text{For } L \neq 0 \quad &\Longrightarrow \quad \cot\phi = \frac{\sqrt{k - L^2}}{L} \cos(\theta - \theta_0) \enspace (\text{implicit solution}) \\[14pt]
    &\Longleftrightarrow \quad \underbrace{z = \frac{\sqrt{k - L^2}}{L} \big( \cos\theta_0\, x + \sin\theta_0\, y \big)}_{\footnotesize \text{plane through the origin}}
    \end{aligned}
    $$

    $\therefore$ &nbsp; the geodesics on $(\mathbb{S}^2, g_{\mathbb{S}^2})$ are the great circles of $\mathbb{S}^2$!
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, GREY, ORANGE, SPHERE_OUTLINE, beyond, first_view, name_at, np, panel, pins, sphere_flat):
    # ---- Figure B: the geodesics of the sphere ----------------------------
    AZ_B, EL_B, WIDTH_B = 30, 18, 500
    # the theta_0 of the plane: not a slider, never named in the figure. At az + 120 degrees the circle is an open ellipse
    # at every L (never edge-on in the first view), and the point runs counterclockwise on the screen.
    TH0 = np.radians(AZ_B + 120)
    S_B = 1.1                                         # half the side of the square that outlines the plane
    T_B = 1.65                                        # the length of the x, y, z axes
    BOX_B = ((-0.92, 0.92), (-0.92, 0.92), (-0.92, 0.92))
    SC_B = 0.94 * WIDTH_B / (2 * np.sqrt(3) * 0.92)
    TOP_B = 1.414 + (38 - 10) / SC_B + 0.02          # the highest and lowest name anchors in the first view (gamma'(t) straight up / down)
    BOTTOM_B = 1.414 + (38 + 10) / SC_B + 0.02
    HEIGHT_B = int(np.ceil((TOP_B + BOTTOM_B) * SC_B)) + 56

    def great_circle(L, t):
        """gamma(t) = -cos(t) u + sin(t) v with u, v as in the brief; t may be an array. Returns gamma, gamma', u, v."""
        w = np.sqrt(max(1 - L * L, 0.0))
        c0, s0 = np.cos(TH0), np.sin(TH0)
        u = np.array([-s0, c0, 0.0])
        v = np.array([L * c0, L * s0, w])
        t = np.asarray(t, float)
        g = -np.cos(t)[..., None] * u + np.sin(t)[..., None] * v
        dg = np.sin(t)[..., None] * u + np.cos(t)[..., None] * v
        return g, dg, u, v

    def panel_b(L, t):
        """The sphere, the plane through the origin in outline, the great circle, and the point gamma(t) with gamma'(t)."""
        axes = first_view(AZ_B, EL_B)
        g, dg, u, v = great_circle(L, t)
        tt = np.linspace(0, 2 * np.pi, 241)
        circle, _, _, _ = great_circle(L, tt)
        # the square of the plane, in the basis u, v, which holds for every L (vertical at L = 0, z = 0 at L = 1)
        corners = [S_B * (a * u + b * v) for a, b in [(-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)]]
        edge = np.concatenate([corners[k] + np.linspace(0, 1, 40, endpoint=False)[:, None] * (corners[k + 1] - corners[k]) for k in range(4)] + [corners[0][None, :]])
        tip = g + dg
        # gamma(t) sits inside the ellipse: 0.16 towards the centre (in space, so it stays off its point when the figure turns)
        # and 13 px to the left of the direction of motion on the screen (the motion is counterclockwise)
        mx, my = beyond(g, tip, 13, axes)
        texts = [
            name_at(tip, *beyond(g, tip, 38, axes), r"\gamma'(t)", ORANGE, axes, SC_B),
            name_at((1 - 0.16) * g, -my, mx, r"\gamma(t)", "#000000", axes, SC_B),
        ] + pins(axes[1], TOP_B, BOTTOM_B)
        return panel(
            1.0,
            surfaces=[sphere_flat()],
            outlines=[SPHERE_OUTLINE],
            lines=[(*edge.T, GREY, 1.2), (*circle.T, BLUE, 2.2)],
            points=[((0, 0, 0), "#000000", 2.6), (tuple(g), "#000000", 3.6)],
            axes=[((0, 0, 0), (T_B, 0, 0), "x", 208), ((0, 0, 0), (0, T_B, 0), "y", -8), ((0, 0, 0), (0, 0, T_B), "z", 90)],
            arrows=[(g, tip, ORANGE, 1.8)],
            texts=texts,
            box=BOX_B,
        )

    return AZ_B, BOTTOM_B, BOX_B, EL_B, HEIGHT_B, SC_B, TH0, TOP_B, T_B, WIDTH_B, great_circle, panel_b


@app.cell(hide_code=True)
def _(mo, np):
    fig_b_L = mo.ui.slider(0, 1, 0.05, value=0.6, label=r"$L$", show_value=True)
    fig_b_t = mo.ui.slider(0, round(2 * np.pi, 2), 0.04, value=1.0, label=r"$t$", show_value=False)
    return fig_b_L, fig_b_t


@app.cell(hide_code=True)
def _(AZ_B, EL_B, HEIGHT_B, WIDTH_B, fig_b_L, fig_b_t, mo, panel_b, turntable):
    _fig = turntable(
        AZ_B,
        EL_B,
        "the geodesics of the sphere: for k = 1 and the chosen L, a great circle, the plane through the origin that contains it, and the point gamma(t) with the velocity gamma'(t), of length 1",
        [panel_b(round(fig_b_L.value, 2), round(fig_b_t.value, 2))],
        height=HEIGHT_B,
        width=WIDTH_B,
        key="L19-geodesics",
        apart=True,
    )
    mo.vstack([mo.hstack([fig_b_L, fig_b_t], justify="start", gap=2, wrap=True), _fig])
    return


@app.cell(hide_code=True)
def _(HEIGHT_B, frame):
    frame("L19-geodesics", HEIGHT_B)
    return


if __name__ == "__main__":
    app.run()
