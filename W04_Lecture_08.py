import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 08 · Charts on the sphere, smooth maps, tangent vectors", css_file="phy309.css")


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
    BLUE, RED, GREEN, ORANGE, GREY, LIGHT = "#1b458f", "#b3261e", "#2e7d32", "#e65100", "#888888", "#cfe3f5"
    # Figure widths: FULL spans the page, HALF sits beside text or in a pair
    FULL, HALF = 7.4, 3.6

    def header(document, date, running=""):
        """Course header, as on the exercise sheets and exams."""
        return mo.Html(
            f"""
    <div class="bs-head">
      <div class="bs-running">PHY309 &bull; {running}</div>
      <div class="bs-title">Differential Geometry and General Relativity</div>
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
        One head size and one line weight for every figure, so arrows look alike across lectures."""
        ax.annotate(
            "",
            xy=tip,
            xytext=tail,
            arrowprops={"arrowstyle": "-|>,head_width=0.15,head_length=0.35", "color": color, "lw": lw, "shrinkA": 0, "shrinkB": 0, **kw},
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
        return mo.md("\n".join(["| | |", "|:--|--:|"] + [f"| {k} | {v} |" for k, v in rows]))

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
def _(header):
    header("Lecture 08", "Week 04", "Lecture 08 · Charts on the sphere, smooth maps, tangent vectors")
    return


@app.cell(hide_code=True)
def _(fig_angles, mo):
    mo.vstack([mo.md(r"""
    ## Last time

    - a manifold is a set of points $M \ni p$ with charts $\varphi_\alpha : U_\alpha \subseteq M \longrightarrow V_\alpha \subseteq \mathbb{R}^m$: the $U_\alpha$ cover $M$, the $V_\alpha$ and $\varphi_\alpha(U_\alpha \cap U_\beta)$ are open, the $\varphi_\alpha$ are bijections and the changes of chart $\varphi_\beta \circ \varphi_\alpha^{-1}$ are smooth with smooth inverse
    - a function $f : M \longrightarrow \mathbb{R}$ is smooth if $f \circ \varphi_\alpha^{-1}$ is smooth for every chart; the sphere with its two stereographic charts is a 2-manifold

    **In this lecture:** the atlas of the sphere in full, smooth maps between manifolds, and tangent vectors

    ## II.3 &nbsp; Charts on the sphere, smooth maps, tangent vectors

    ### Charts on the sphere

    **Example.** &nbsp; $\mathbb{S}^2 = \{\, (x, y, z) \in \mathbb{R}^3 \mid x^2 + y^2 + z^2 = 1 \,\}$

    Choose $n = (0, 0, 1)$. Define $\varphi_n : U_n \longrightarrow V_n$ via &nbsp; $U_n = \mathbb{S}^2 - \{n\}$, &nbsp; $V_n = \mathbb{R}^2$

    $$
    \varphi_n(x, y, z) = (u, v) = \left( \frac{x}{1 - z},\ \frac{y}{1 - z} \right) \qquad \big( z\, (u, v, 0) = (u - x, v - y, 0) \big)
    $$

    $$
    \Longrightarrow \qquad \varphi_n^{-1}(u, v) = \left( \frac{2u}{1 + u^2 + v^2},\ \frac{2v}{1 + u^2 + v^2},\ \frac{-1 + u^2 + v^2}{1 + u^2 + v^2} \right)
    $$

    Similarly, choose $s = (0, 0, -1)$. Define $\varphi_s : U_s \longrightarrow V_s$ via &nbsp; $U_s = \mathbb{S}^2 - \{s\}$, &nbsp; $V_s = \mathbb{R}^2$,

    $$
    \varphi_s(x, y, z) = (\tilde{u}, \tilde{v}) = \left( \frac{x}{1 + z},\ \frac{y}{1 + z} \right)
    \qquad \Longrightarrow \qquad \varphi_s^{-1}(\tilde{u}, \tilde{v}) = \left( \frac{2\tilde{u}}{1 + \tilde{u}^2 + \tilde{v}^2},\ \frac{2\tilde{v}}{1 + \tilde{u}^2 + \tilde{v}^2},\ \frac{1 - \tilde{u}^2 - \tilde{v}^2}{1 + \tilde{u}^2 + \tilde{v}^2} \right)
    $$

    - $U_n \cup U_s = (\mathbb{S}^2 - \{n\}) \cup (\mathbb{S}^2 - \{s\}) = \mathbb{S}^2$
    - $V_n = \mathbb{R}^2$, $V_s = \mathbb{R}^2$ open
    - $\varphi_n : U_n \longrightarrow V_n$, &nbsp; $\varphi_s : U_s \longrightarrow V_s$ bijective
    - $\varphi_n(U_n \cap U_s) = \varphi_n(\mathbb{S}^2 - \{n, s\}) = \mathbb{R}^2 - \{(0, 0)\}$ and $\varphi_s(U_n \cap U_s) = \varphi_s(\mathbb{S}^2 - \{n, s\}) = \mathbb{R}^2 - \{(0, 0)\}$ are open!
    - $\varphi_s \circ \varphi_n^{-1}$:

    $$
    \begin{aligned}
    \varphi_s \circ \varphi_n^{-1}(u, v) &= \varphi_s\!\left( \frac{2u}{1 + u^2 + v^2},\ \frac{2v}{1 + u^2 + v^2},\ \frac{-1 + u^2 + v^2}{1 + u^2 + v^2} \right) \\[4pt]
    &= \left( \frac{2u}{2 (u^2 + v^2)},\ \frac{2v}{2 (u^2 + v^2)} \right) \\[4pt]
    &= \left( \frac{u}{u^2 + v^2},\ \frac{v}{u^2 + v^2} \right) = (\tilde{u}, \tilde{v})
    \end{aligned}
    $$

    $\leadsto$ &nbsp; diffeomorphism $\mathbb{R}^2 - \{(0, 0)\} \longrightarrow \mathbb{R}^2 - \{(0, 0)\}$

    We can differentiate it infinitely many times; it is invertible $(\varphi_s \circ \varphi_n^{-1})^{-1} = \varphi_n \circ \varphi_s^{-1}$ and inverse is also infinitely differentiable

    $$
    \varphi_n \circ \varphi_s^{-1}(\tilde{u}, \tilde{v}) = \left( \frac{\tilde{u}}{\tilde{u}^2 + \tilde{v}^2},\ \frac{\tilde{v}}{\tilde{u}^2 + \tilde{v}^2} \right)
    $$

    $\therefore$ &nbsp; $\mathbb{S}^2$ with $\mathcal{A} = \{\varphi_n, \varphi_s\}$ is a 2-manifold

    **Remark.** There are many more charts $\varphi : U \subseteq \mathbb{S}^2 \longrightarrow V \subseteq \mathbb{R}^2$ which are “compatible” with $\varphi_n$ and $\varphi_s$ in the sense

    $$
    \varphi_\alpha \circ \varphi^{-1} : \varphi(U \cap U_\alpha) \longrightarrow \varphi_\alpha(U \cap U_\alpha) \quad \text{is a diffeo for } \alpha = n, s
    $$

    - choose any $q \in \mathbb{S}^2$ and define $\varphi_q : \mathbb{S}^2 - \{q\} \longrightarrow \mathbb{R}^2 \approx (q - o)^\perp \subseteq \mathbb{R}^3$ the stereographic projection based at $q$
    - choose any $q \in \mathbb{S}^2$ ($= n$) and $e_1 \in (n - o)^\perp$, &nbsp; $e_2 = (n - o) \times e_1$, &nbsp; and remove the half meridian $C = \{\, p \in \mathbb{S}^2 \mid \langle p - o, e_2 \rangle = 0,\ \langle p - o, e_1 \rangle \geq 0 \,\} \ni n, s$; define

    $$
    \phi : \mathbb{S}^2 - C \longrightarrow (0, \pi), \qquad \theta : \mathbb{S}^2 - C \longrightarrow (0, 2\pi)
    $$

    $$
    \cos\phi(p) = \langle p - o,\ n - o \rangle, \qquad \cos\theta(p) = \frac{\langle p - o,\ e_1 \rangle}{\sin\phi(p)}, \quad \sin\theta(p) = \frac{\langle p - o,\ e_2 \rangle}{\sin\phi(p)} \qquad (\theta: \text{oriented angle})
    $$

    the polar and azimuthal angles, giving

    $$
    \psi : \mathbb{S}^2 - C \longrightarrow (0, \pi) \times (0, 2\pi) \subset \mathbb{R}^2
    $$
    """), fig_angles, mo.md(r"""

    $$
    \begin{aligned}
    \psi^{-1}(\phi, \theta) &= (\sin\phi \cos\theta,\ \sin\phi \sin\theta,\ \cos\phi) = (x, y, z) \\
    &= \left( \frac{2u}{1 + u^2 + v^2},\ \frac{2v}{1 + u^2 + v^2},\ \frac{-1 + u^2 + v^2}{1 + u^2 + v^2} \right) = \varphi_n^{-1}(u, v)
    \end{aligned}
    $$

    $$
    \Longrightarrow \qquad (u, v) = \varphi_n \circ \psi^{-1}(\phi, \theta) = \left( \cot\tfrac{\phi}{2} \cos\theta,\ \cot\tfrac{\phi}{2} \sin\theta \right)
    $$

    diffeo from $(0, \pi) \times (0, 2\pi)$ to $\mathbb{R}^2 - \{\, \lambda e_1,\ \lambda \geq 0 \,\}$

    $\therefore$ &nbsp; $\mathbb{S}^2$ with $\mathcal{A} = \{\varphi_n, \varphi_s, \varphi_q, \psi\}$ is also a 2-manifold &nbsp; (we assume $\mathcal{A}$ contains all possible compatible charts: maximal atlas)
    """)])
    return


@app.cell(hide_code=True)
def _(BLUE, FULL, GREEN, GREY, HALF, LIGHT, RED, arrow, blank, blob, math, np, plane):
    # Polar angle phi from n and azimuthal angle theta from e_1, drawn in perspective
    _az, _el = math.radians(-30), math.radians(20)

    def _pr(x, y, z):
        X = -x * math.sin(_az) + y * math.cos(_az)
        Y = z * math.cos(_el) - (x * math.cos(_az) + y * math.sin(_az)) * math.sin(_el)
        D = (x * math.cos(_az) + y * math.sin(_az)) * math.cos(_el) + z * math.sin(_el)
        return X, Y, D

    def _curve(ax, x, y, z, color, lw=1.0, ls="-"):
        X, Y, D = _pr(x, y, z)
        ax.plot(np.where(D >= 0, X, np.nan), np.where(D >= 0, Y, np.nan), color=color, lw=lw, ls=ls)
        ax.plot(np.where(D < 0, X, np.nan), np.where(D < 0, Y, np.nan), color=color, lw=0.7 * lw, ls=(0, (3, 3)))

    fig_angles, _ax = blank(HALF, 3.2, (-1.45, 1.45), (-1.45, 1.45))
    _t = np.linspace(0, 2 * np.pi, 300)
    _ax.plot(np.cos(_t), np.sin(_t), color="black")
    _curve(_ax, np.cos(_t), np.sin(_t), 0 * _t, GREY)
    _ph, _th = math.radians(50), math.radians(40)
    _P = (math.sin(_ph) * math.cos(_th), math.sin(_ph) * math.sin(_th), math.cos(_ph))
    _F = (_P[0], _P[1], 0.0)  # foot of p on the equatorial plane
    _N, _S, _O = _pr(0, 0, 1), _pr(0, 0, -1), _pr(0, 0, 0)
    _ax.plot([_S[0], _N[0]], [_S[1], _N[1]], color="black", lw=0.9, zorder=2)
    for _Q, _lab, _dx, _dy in ((_N, "$n$", 0.08, 0.04), (_S, "$s$", 0.08, -0.2)):
        _ax.plot(*_Q[:2], "o", color="black", ms=4, zorder=4)
        _ax.text(_Q[0] + _dx, _Q[1] + _dy, _lab, fontsize=12)
    _ax.plot(*_O[:2], "o", color="black", ms=3, zorder=4)
    _ax.text(_O[0] - 0.1, _O[1] - 0.16, "$o$", fontsize=11, ha="right")
    arrow(_ax, _O[:2], _pr(*_P)[:2], BLUE)
    _ax.plot(*_pr(*_P)[:2], "o", color=BLUE, ms=4, zorder=4)
    _ax.text(_pr(*_P)[0] + 0.05, _pr(*_P)[1] + 0.12, "$p$", color=BLUE, fontsize=12, bbox=dict(boxstyle="round,pad=0.1", facecolor="white", edgecolor="none", alpha=0.85))
    _ax.plot([_pr(*_P)[0], _pr(*_F)[0]], [_pr(*_P)[1], _pr(*_F)[1]], "--", color=BLUE, lw=0.9)
    _ax.plot([_O[0], _pr(*_F)[0]], [_O[1], _pr(*_F)[1]], "--", color=BLUE, lw=0.9)
    arrow(_ax, _O[:2], _pr(1.0, 0, 0)[:2], "black")
    _ax.text(_pr(1.0, 0, 0)[0] - 0.02, _pr(1.0, 0, 0)[1] - 0.2, "$e_1$", fontsize=12, ha="center")
    _a = np.linspace(0, _ph, 60)  # arc for phi, in the plane of n, o and p
    _X, _Y, _ = _pr(0.4 * np.sin(_a) * math.cos(_th), 0.4 * np.sin(_a) * math.sin(_th), 0.4 * np.cos(_a))
    _ax.plot(_X, _Y, color=GREEN)
    _ax.text(_pr(0.5 * math.sin(_ph / 2) * math.cos(_th), 0.5 * math.sin(_ph / 2) * math.sin(_th), 0.5 * math.cos(_ph / 2))[0] + 0.02, _pr(0, 0, 0.5)[1] - 0.05, r"$\phi$", color=GREEN, fontsize=12)
    _a = np.linspace(0, _th, 60)  # arc for theta, in the equatorial plane from e_1
    _X, _Y, _ = _pr(0.45 * np.cos(_a), 0.45 * np.sin(_a), 0 * _a)
    _ax.plot(_X, _Y, color=GREEN)
    _m = _pr(0.6 * math.cos(_th / 2), 0.6 * math.sin(_th / 2), 0)
    _ax.text(_m[0] + 0.1, _m[1] - 0.06, r"$\theta$", color=GREEN, fontsize=12)
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
    _bb = dict(boxstyle="round,pad=0.1", facecolor="white", edgecolor="none", alpha=0.85)
    _ax.text(1.15, 3.85, "$U$", color=RED, fontsize=12, ha="center", bbox=_bb)
    _ax.text(2.62, 3.05, "$f^{-1}(A)$", color=BLUE, fontsize=11, ha="center", bbox=_bb)
    _ax.text(7.3, 3.25, "$f(U)$", color=RED, fontsize=11, ha="center", bbox=_bb)
    _ax.text(8.75, 3.85, "$A$", color=BLUE, fontsize=12, ha="center", bbox=_bb)
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
    arrow(_ax, (2.8, 0.9), (6.8, 0.9), "black", lw=1.0)
    _ax.text(4.8, 1.05, r"$\psi \circ f \circ \varphi^{-1}$", fontsize=12, ha="center", va="bottom")
    _ax.text(2.7, 1.75, r"$\varphi(U \cap f^{-1}(A))$", color=GREY, fontsize=11, ha="center")
    _ax.text(7.4, 1.75, r"$\psi(f(U) \cap A)$", color=GREY, fontsize=11, ha="center")
    _ = None  # no cell output: the figures are returned, not displayed here
    return fig_angles, fig_smooth


@app.cell(hide_code=True)
def _(mo):
    s_phi = mo.ui.slider(5, 175, 1, value=60, label=r"$\phi$ (degrees)", show_value=True)
    s_theta = mo.ui.slider(1, 359, 1, value=40, label=r"$\theta$ (degrees)", show_value=True)
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
        (_axes[1], (_u, _v), r"$\varphi_n(p) = (u, v)$", max(2.0, 1.2 * _r)),
        (_axes[2], (_ut, _vt), r"$\varphi_s(p) = (\tilde{u}, \tilde{v})$", max(2.0, 1.2 / _r)),
    ):
        _ax.set_title(_title, fontsize=12)
        if _lim is None:
            _ax.set_xlim(0, 180)
            _ax.set_ylim(0, 360)
            _ax.set_xlabel(r"$\phi$")
            _ax.set_ylabel(r"$\theta$", rotation=0, labelpad=12)
            _ax.set_xticks([0, 90, 180])
            _ax.set_yticks([0, 180, 360])
        else:
            _ax.set_xlim(-_lim, _lim)
            _ax.set_ylim(-_lim, _lim)
            _ax.set_aspect("equal")
            _ax.axhline(0, color="black", lw=0.6)
            _ax.axvline(0, color="black", lw=0.6)
            _ax.plot(np.cos(_a), np.sin(_a), color=GREY, lw=0.8)
            _ax.set_xticks([-round(_lim, 1), 0, round(_lim, 1)])
            _ax.set_yticks([-round(_lim, 1), 0, round(_lim, 1)])
            for _axis in (_ax.xaxis, _ax.yaxis):
                _axis.set_major_formatter(lambda _t, _i: f"${_t:.1f}$")
        _ax.plot(*_pt, "o", color=BLUE, ms=6)
    # the curve of constant phi in the three charts
    _axes[1].plot(_r * np.cos(_a), _r * np.sin(_a), color=GREEN, lw=1.0)
    _axes[2].plot(np.cos(_a) / _r, np.sin(_a) / _r, color=GREEN, lw=1.0)
    _axes[0].plot([s_phi.value, s_phi.value], [0, 360], color=GREEN, lw=1.0)
    _axes[1].text(0.06, 1.04, "equator", color=GREY, fontsize=10, ha="left", va="bottom")
    _axes[1].text(0.76 * max(_r, 0.5), -0.76 * max(_r, 0.5), r"$\phi$ = const", color=GREEN, fontsize=10, ha="left", va="top")

    _table = "\n".join(
        [
            "| | |",
            "|:--|--:|",
            rf"| $p = \psi^{{-1}}(\phi, \theta) = (\sin\phi \cos\theta,\ \sin\phi \sin\theta,\ \cos\phi)$ | $({_x:.3f},\ {_y:.3f},\ {_z:.3f})$ |",
            rf"| $\varphi_n(p) = \left( \cot\tfrac{{\phi}}{{2}} \cos\theta,\ \cot\tfrac{{\phi}}{{2}} \sin\theta \right)$ | $({_u:.3f},\ {_v:.3f})$ |",
            rf"| $\varphi_s(p) = \left( \dfrac{{u}}{{u^2 + v^2}},\ \dfrac{{v}}{{u^2 + v^2}} \right)$ | $({_ut:.3f},\ {_vt:.3f})$ |",
        ]
    )
    mo.vstack([mo.hstack([s_phi, s_theta], justify="start", gap=3, wrap=True), mo.md(_table), _fig])
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
    \psi \circ f \circ \varphi^{-1} : \underbrace{\varphi(U \cap f^{-1}(A))}_{\subseteq\, \mathbb{R}^m} \longrightarrow \underbrace{\psi(f(U) \cap A)}_{\subseteq\, \mathbb{R}^n}
    $$

    is smooth (or differentiable) (or continuous) (or any adjective)
    """,
                "Smooth map",
            ),
            fig_smooth,
            mo.md(
                r"""
    ### Tangent vectors

    To define the notion of derivatives of smooth functions, we need a notion of “directions” on manifolds &nbsp; $\leadsto$ &nbsp; tangent vectors

    On affine spaces $(\mathbb{A}, \mathbb{V}, -)$, $(\mathbb{B}, \mathbb{W}, -)$, given $p \in \mathbb{A}$ and $v \in \mathbb{V}$ and $f : \mathbb{A} \longrightarrow \mathbb{B}$ &nbsp; $\leadsto$ &nbsp; derivative of $f$ at $p$ in the direction of $v$

    $$
    \begin{aligned}
    Df_p(v) &= \lim_{t \to 0} \frac{f(p + tv) - f(p)}{t} && (\text{using affine structure}) \\[4pt]
    &= \lim_{t \to 0} \frac{f(\gamma(t)) - f(p)}{t} && (\text{using curves on } \mathbb{A})
    \end{aligned}
    $$

    for *any* curve $\gamma : \mathbb{R} \longrightarrow \mathbb{A}$ such that $\begin{cases} \gamma(0) = p \in \mathbb{A} \\ \gamma'(0) = v \in \mathbb{V} \end{cases}$ &nbsp; $\left( \gamma'(0) = \displaystyle\lim_{s \to 0} \frac{\gamma(s) - \gamma(0)}{s} \right)$
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
    v_p = [\gamma]_p = \left\{\, \sigma : \mathbb{R} \longrightarrow M \;\middle|\; \sigma(0) = \gamma(0) = p \ \text{ and } \ (\varphi \circ \sigma)'(0) = (\varphi \circ \gamma)'(0) \,\right\}
    $$

    (for any chart $\varphi : U \subseteq M \longrightarrow V \subseteq \mathbb{R}^m$ with $p \in U$)
    """,
                "Tangent vector",
            ),
            mo.md(
                r"""
    In other words, two smooth paths $\gamma, \sigma$ are considered equivalent if in a chart $\varphi$

    $$
    \begin{cases}
    (\varphi \circ \gamma)(0) = (\varphi \circ \sigma)(0) & \leadsto \qquad \gamma(0) = \sigma(0) = p \\
    (\varphi \circ \gamma)'(0) = (\varphi \circ \sigma)'(0) & \leadsto \qquad \text{“} \gamma'(0) = \sigma'(0) = v \text{”}
    \end{cases}
    $$

    **Remark.** If $\gamma \sim \sigma$ with respect to one chart then $\gamma \sim \sigma$ with respect to any other

    $$
    \psi \circ \gamma(t) = \underbrace{\psi \circ \varphi^{-1}}_{\text{change of coordinates}} \circ\, \varphi \circ \gamma(t)
    \qquad \Longrightarrow \qquad (\psi \circ \gamma)'(t) = \underbrace{D(\psi \circ \varphi^{-1})_{\varphi \circ \gamma(t)}}_{\text{Jacobian matrix}} \big( (\varphi \circ \gamma)'(t) \big)
    $$

    $\Longrightarrow$ &nbsp; $[\gamma]_p$ is defined independently of the choice of charts
    """
            ),
            definition(
                r"""
    We denote by

    $$
    T_p M = \text{set of tangent vectors to } M \text{ at } p = \textbf{Tangent space} \text{ to } M \text{ at } p
    $$
    """,
                "Tangent space",
            ),
            mo.md(
                r"""
    ## Summary

    - the sphere carries many compatible charts: the two stereographic projections, projections from any point, and the spherical angles $\psi = (\phi, \theta)$ on the sphere minus a half meridian; a manifold comes with its maximal atlas
    - a map $f : M \longrightarrow N$ is smooth when every local representation $\psi \circ f \circ \varphi^{-1}$ is smooth
    - without displacement vectors, a tangent vector at $p$ is an equivalence class $[\gamma]$ of paths through $p$ with the same velocity in a chart (hence in every chart); $T_p M$ is the set of these classes

    **Next:** the derivative $Df_p : T_p M \longrightarrow T_{f(p)} N$ of a smooth map
    """
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
