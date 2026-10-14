import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 12 · Review: calculus on manifolds", css_file="phy309.css")


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
    header("Lecture 12", "Week 07", "Lecture 12 · Review: calculus on manifolds")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    - A vector field $X : p \longmapsto X_p \in T_pM$; in a chart $X = X^i\, \partial_i$ with local components $X^i : U \longrightarrow \mathbb{R}$, and $X$ is smooth if its components are smooth in every chart.
    - A smooth vector field is a linear differential operator $f \longmapsto X(f)$ on $C^\infty(M, \mathbb{R})$ satisfying the Leibniz rule; $\Gamma(TM)$ is the space of smooth vector fields.
    - An integral curve of $X$ satisfies $\gamma'(t) = X_{\gamma(t)}$, a first order system $(x^i \circ \gamma)' = X^i \circ \gamma$ in any chart; through each point passes a unique maximal integral curve.
    - The tangent bundle $TM$ is the collection of all tangent spaces.

    **In this lecture:** a review of calculus on manifolds, from charts to differential equations, with every step carried out on $\mathbb{S}^2$.

    **References:** Schutz 6.1; Carroll 2.2–2.3; Sasane Ch. 1–3
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## II.7 &nbsp; Review: calculus on manifolds

    ### Charts

    A **manifold** is a set of points $p \in M$ with local charts $\varphi : U \subseteq M \longrightarrow V \subseteq \mathbb{R}^m$ such that every change of charts $\tilde{\varphi} \circ \varphi^{-1} : V \longrightarrow \tilde{V}$ is a diffeomorphism (smooth with smooth inverse).

    A chart $\varphi : U \subseteq M \longrightarrow V \subseteq \mathbb{R}^m$ is the same as

    $$
    p \longmapsto \varphi(p) = x^i(p)\, e_i = \begin{bmatrix} x^1(p) \\ \vdots \\ x^m(p) \end{bmatrix}
    $$

    - **local coordinates** $x^i : U \subseteq M \longrightarrow \mathbb{R}$, $p \longmapsto x^i(p)$
    - **local parametrization** $\varphi^{-1} : V \longrightarrow U \subseteq M$, $x \longmapsto \varphi^{-1}(x) = \text{“}p(x)\text{”}$

    The map $\tilde{\varphi} \circ \varphi^{-1} : V \longrightarrow \tilde{V}$ is the change of charts, of coordinates and of parametrizations at once,

    $$
    x \longmapsto \tilde{x} = \underbrace{\tilde{\varphi} \circ \varphi^{-1}(x)}_{\tilde{x}(x)}
    $$

    and it is a diffeomorphism if and only if the Jacobian matrix

    $$
    \frac{\partial \tilde{x}}{\partial x}(x) = \left[ \frac{\partial \tilde{x}^j}{\partial x^i}(x) \right]
    $$

    is invertible and varies smoothly for all $x \in \varphi(U \cap \tilde{U}) \subseteq V$.

    **Example.** &nbsp; On $\mathbb{S}^2$ the two stereographic charts and their parametrizations are

    $$
    \begin{aligned}
    \varphi_n(x, y, z) &= \left( \frac{x}{1 - z},\ \frac{y}{1 - z} \right) = \big( u(x, y, z),\ v(x, y, z) \big) \\[4pt]
    \varphi_n^{-1}(u, v) &= \left( \frac{2u}{1 + u^2 + v^2},\ \frac{2v}{1 + u^2 + v^2},\ \frac{-1 + u^2 + v^2}{1 + u^2 + v^2} \right) = (x, y, z) \\[8pt]
    \varphi_s(x, y, z) &= \left( \frac{x}{1 + z},\ \frac{y}{1 + z} \right) = \big( \tilde{u}(x, y, z),\ \tilde{v}(x, y, z) \big) \\[4pt]
    \varphi_s^{-1}(\tilde{u}, \tilde{v}) &= \left( \frac{2\tilde{u}}{1 + \tilde{u}^2 + \tilde{v}^2},\ \frac{2\tilde{v}}{1 + \tilde{u}^2 + \tilde{v}^2},\ \frac{1 - \tilde{u}^2 - \tilde{v}^2}{1 + \tilde{u}^2 + \tilde{v}^2} \right) = (x, y, z)
    \end{aligned}
    $$

    The change of charts

    $$
    (\tilde{u}, \tilde{v}) = \varphi_s \circ \varphi_n^{-1}(u, v) = \left( \frac{u}{u^2 + v^2},\ \frac{v}{u^2 + v^2} \right)
    $$

    is smooth with smooth inverse for all $(u, v) \neq (0, 0)$, and its Jacobian matrix

    $$
    \frac{\partial (\tilde{u}, \tilde{v})}{\partial (u, v)} = \frac{1}{(u^2 + v^2)^2} \begin{bmatrix} -u^2 + v^2 & -2uv \\ -2uv & u^2 - v^2 \end{bmatrix}
    $$

    is invertible and smooth for all $(u, v) \neq (0, 0)$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Smooth functions

    Which functions are smooth? A function on $M$ is studied through its **local representation** in a chart

    $$
    f : M \longrightarrow \mathbb{R}, \quad p \longmapsto f(p) \qquad \overset{\varphi}{\leadsto} \qquad f \circ \varphi^{-1} : V \subseteq \mathbb{R}^m \longrightarrow \mathbb{R}, \quad x \longmapsto f(\varphi^{-1}(x)) = f(p(x))
    $$

    $$
    f \ \text{smooth} \qquad \Longleftrightarrow \qquad f \circ \varphi^{-1} \ \text{smooth} \quad \forall\ \varphi
    $$

    **Example.** &nbsp; The height function $f : \mathbb{S}^2 \longrightarrow \mathbb{R}$, $(x, y, z) \longmapsto z$, has local representations

    $$
    f \circ \varphi_n^{-1}(u, v) = \frac{-1 + u^2 + v^2}{1 + u^2 + v^2}, \qquad f \circ \varphi_s^{-1}(\tilde{u}, \tilde{v}) = \frac{1 - \tilde{u}^2 - \tilde{v}^2}{1 + \tilde{u}^2 + \tilde{v}^2}
    $$

    smooth for all $(u, v) \in \mathbb{R}^2$ and for all $(\tilde{u}, \tilde{v}) \in \mathbb{R}^2$ &nbsp; $\Longrightarrow$ &nbsp; $f$ is smooth.

    The function $g : \mathbb{S}^2 \longrightarrow \mathbb{R}$, $(x, y, z) \longmapsto y / x$, has local representations

    $$
    g \circ \varphi_n^{-1}(u, v) = \frac{v}{u}, \qquad g \circ \varphi_s^{-1}(\tilde{u}, \tilde{v}) = \frac{\tilde{v}}{\tilde{u}}
    $$

    smooth for all $(u, v)$ with $u \neq 0$ and for all $(\tilde{u}, \tilde{v})$ with $\tilde{u} \neq 0$ &nbsp; $\Longrightarrow$ &nbsp; $g$ is smooth at all $(x, y, z)$ with $x \neq 0$.
    """)
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, GREY, RED, arrow, blob, np):
    # The derivative of f at p computed through a chart
    fig_deriv = Figure(figsize=(5.4, 3.6), layout="constrained")
    _ax = fig_deriv.subplots()
    _ax.set_aspect("equal")
    _ax.axis("off")
    _t = np.linspace(0, 2 * np.pi, 300)
    _ax.plot(*blob(1.6, 3.0, 1.55, 1.15, wobble=0.1, seed=10), color="black")
    _ax.text(0.1, 4.1, "$M$", fontsize=13)
    _ax.plot(*blob(1.6, 3.0, 0.68, 0.56, wobble=0.06, seed=11), color=GREY)
    _ax.text(0.95, 3.6, "$U$", color=GREY, fontsize=11)
    _P = (1.6, 2.95)
    arrow(_ax, _P, (_P[0] + 0.55, _P[1] + 0.3), GREEN)
    _ax.text(_P[0] + 0.05, _P[1] + 0.4, r"$[\gamma] = v^i \partial_i|_p$", color=GREEN, fontsize=9, ha="center", va="center", bbox=dict(boxstyle="round,pad=0.1", facecolor="white", edgecolor="none"))
    _ax.plot(*_P, "o", color="black", ms=4)
    _ax.text(_P[0], _P[1] - 0.12, r"$p = \varphi^{-1}(x)$", fontsize=10, ha="center", va="top")
    _B = (4.6, 2.2)
    _ax.plot([_B[0], _B[0] + 1.8, _B[0] + 1.8, _B[0], _B[0]], [_B[1], _B[1], _B[1] + 1.6, _B[1] + 1.6, _B[1]], color=GREY)
    _ax.text(_B[0] + 0.9, _B[1] + 1.65, "$V$", color=GREY, fontsize=11, ha="center", va="bottom")
    _Q = (_B[0] + 0.8, _B[1] + 0.7)
    arrow(_ax, _Q, (_Q[0] + 0.55, _Q[1] + 0.35), GREEN)
    _ax.text(_Q[0] + 0.6, _Q[1] + 0.4, "$v$", color=GREEN, fontsize=11)
    _ax.plot(*_Q, "o", color="black", ms=4)
    _ax.text(_Q[0], _Q[1] - 0.25, r"$x = \varphi(p)$", fontsize=10, ha="center", va="top")
    arrow(_ax, (3.0, 3.4), (4.5, 3.4), "black", connectionstyle="arc3,rad=-0.25")
    _ax.text(3.75, 3.8, r"$\varphi$", fontsize=12, ha="center")
    # the real line below
    arrow(_ax, (0.6, 0.6), (3.2, 0.6), "black", lw=1.0)
    _ax.text(3.3, 0.5, r"$\mathbb{R}$", fontsize=11)
    _ax.plot(1.6, 0.6, "o", color="black", ms=4)
    _ax.text(1.6, 0.4, r"$f(p) = f \circ \varphi^{-1}(x)$", fontsize=10, ha="center", va="top")
    arrow(_ax, (1.6, 0.6), (2.5, 0.6), GREEN)
    _ax.text(2.1, 0.75, r"$Df(p)[\gamma]$", color=GREEN, fontsize=10, ha="center", va="bottom")
    arrow(_ax, (1.5, 1.85), (1.55, 0.8), BLUE)
    _ax.text(1.3, 1.35, "$f$", color=BLUE, fontsize=12, ha="right")
    arrow(_ax, (4.9, 2.1), (2.95, 0.75), RED, connectionstyle="arc3,rad=-0.15")
    _ax.text(4.0, 1.1, r"$f \circ \varphi^{-1}$", color=RED, fontsize=11)
    _ax.set_xlim(-0.2, 6.8)
    _ax.set_ylim(0, 4.5)
    _ = None  # no cell output: the figure is returned, not displayed here
    return (fig_deriv,)


@app.cell(hide_code=True)
def _(fig_deriv, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ### Derivatives

    How to compute derivatives? If $f : M \longrightarrow \mathbb{R}$ is smooth at $p \in M$, then $f \circ \varphi^{-1} : V \subseteq \mathbb{R}^m \longrightarrow \mathbb{R}$ is smooth at $x = \varphi(p)$, and

    $$
    D(f \circ \varphi^{-1})(x) = \left[ \frac{\partial}{\partial x^i} (f \circ \varphi^{-1})(x) \right] : \mathbb{R}^m \longrightarrow \mathbb{R}
    $$

    defines the first order approximation of $f \circ \varphi^{-1}$ at $x = \varphi(p)$

    $$
    \begin{aligned}
    (f \circ \varphi^{-1})(x + v) &= f \circ \varphi^{-1}(x) + D(f \circ \varphi^{-1})(x)(v) + o(v) \\[4pt]
    &= f \circ \varphi^{-1}(x) + v^i\, \frac{\partial}{\partial x^i} (f \circ \varphi^{-1})(x) + o(v)
    \end{aligned}
    $$

    where $o(v)$ is small compared to $v$. The same number can be read in several ways:

    $$
    \begin{aligned}
    D(f \circ \varphi^{-1})(x)(v) &= v^i\, \frac{\partial}{\partial x^i} (f \circ \varphi^{-1})(x) \\[6pt]
    &= \frac{d}{dt}\bigg|_{t=0} (f \circ \varphi^{-1})(x + tv) \\[6pt]
    &= \frac{d}{dt}\bigg|_{t=0} (f \circ \gamma)(t), \qquad \gamma(t) = \varphi^{-1}(x + tv) \\[6pt]
    &= v^i\, \partial_i|_p f \\[6pt]
    &= Df(p)([\gamma]) = Df(p)(\gamma'(0)), \qquad [\gamma] = v^i\, \partial_i|_p = \gamma'(0)
    \end{aligned}
    $$

    - the second line is the directional derivative of $f \circ \varphi^{-1}$ at $x$ in the direction $v \in \mathbb{R}^m$
    - the third line is the directional derivative of $f$ at $p$ in the direction $[\gamma]$; it depends only on $v$, since $\varphi \circ \gamma(0) = x$ and $(\varphi \circ \gamma)'(0) = v$
    - the fourth line expands $[\gamma]$ in the basis $\partial_i|_p$ of $T_pM = \mathrm{Der}_p(M)$
    """
            ),
            fig_deriv,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** &nbsp; For the height function $f(x, y, z) = z$ on $\mathbb{S}^2$, in the chart $\varphi_n$ with $z(u, v) = f \circ \varphi_n^{-1}(u, v)$

    $$
    \begin{aligned}
    Dz(u, v)(a, b) &= \begin{bmatrix} \dfrac{\partial}{\partial u} z(u, v) & \dfrac{\partial}{\partial v} z(u, v) \end{bmatrix} \begin{bmatrix} a \\ b \end{bmatrix} \\[8pt]
    &= \begin{bmatrix} \dfrac{\partial}{\partial u} \left( \dfrac{-1 + u^2 + v^2}{1 + u^2 + v^2} \right) & \dfrac{\partial}{\partial v} \left( \dfrac{-1 + u^2 + v^2}{1 + u^2 + v^2} \right) \end{bmatrix} \begin{bmatrix} a \\ b \end{bmatrix} \\[8pt]
    &= a\, \frac{\partial}{\partial u} \left( \frac{-1 + u^2 + v^2}{1 + u^2 + v^2} \right) + b\, \frac{\partial}{\partial v} \left( \frac{-1 + u^2 + v^2}{1 + u^2 + v^2} \right) \\[8pt]
    &= \underbrace{a\, \frac{\partial}{\partial u} z(u, v) + b\, \frac{\partial}{\partial v} z(u, v)}_{\frac{\partial}{\partial u},\, \frac{\partial}{\partial v} \text{ basis of derivations of } \mathbb{R}^2 \text{ at } (u, v)} \\[8pt]
    &= \underbrace{a\, \partial_u|_{(x, y, z)} z + b\, \partial_v|_{(x, y, z)} z}_{\partial_u|,\, \partial_v| \text{ basis of derivations of } \mathbb{S}^2 \text{ at } (x, y, z) = \varphi_n^{-1}(u, v)} \\[8pt]
    &= Dz(x, y, z)([\gamma]), \qquad \gamma(t) = \varphi_n^{-1}(u + ta,\ v + tb) = \big( x(t), y(t), z(t) \big) \\[8pt]
    &= \frac{d}{dt}\bigg|_{t=0} z(t) = \frac{d}{dt}\bigg|_{t=0} \frac{-1 + (u + ta)^2 + (v + tb)^2}{1 + (u + ta)^2 + (v + tb)^2}
    \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    s_u = mo.ui.slider(-2.0, 2.0, 0.1, value=1.0, label="$u$", show_value=True)
    s_v = mo.ui.slider(-2.0, 2.0, 0.1, value=0.5, label="$v$", show_value=True)
    s_a = mo.ui.slider(-1.0, 1.0, 0.1, value=1.0, label="$a$", show_value=True)
    s_b = mo.ui.slider(-1.0, 1.0, 0.1, value=0.5, label="$b$", show_value=True)
    return s_a, s_b, s_u, s_v


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, mo, np, s_a, s_b, s_u, s_v, table):
    _u, _v, _a, _b = s_u.value, s_v.value, s_a.value, s_b.value
    _r = 1 + _u**2 + _v**2
    _zu, _zv = 4 * _u / _r**2, 4 * _v / _r**2
    _d = _a * _zu + _b * _zv + 0.0
    _z0 = (_r - 2) / _r
    _t = np.linspace(-1.5, 1.5, 300)
    _q = (_u + _t * _a) ** 2 + (_v + _t * _b) ** 2
    _fig = Figure(figsize=(FULL, 3.2), layout="constrained")
    _ax = _fig.subplots()
    _ax.plot(_t, (_q - 1) / (_q + 1), color=BLUE)
    _ax.plot(_t, _z0 + _d * _t, color=GREEN)
    _ax.plot(0, _z0, "o", color="black", ms=5)
    _ax.set_xlim(-1.5, 1.5)
    _ax.set_ylim(-1.1, 1.1)
    _ax.axhline(0, color="black", lw=0.6)
    _ax.axvline(0, color="black", lw=0.6)
    _ax.set_xlabel("$t$")
    _ax.set_xticks([-1, 0, 1])
    _ax.set_yticks([-1, 0, 1])
    _ax.text(0.03, 0.9, r"$z(t)$ along $\gamma(t) = \varphi_n^{-1}(u + ta,\ v + tb)$", color=BLUE, fontsize=11, transform=_ax.transAxes)
    _ax.text(0.97, 0.06, r"tangent line, slope $Dz(u, v)(a, b)$", color=GREEN, fontsize=11, transform=_ax.transAxes, ha="right")

    mo.vstack(
        [
            mo.hstack([s_u, s_v, s_a, s_b], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\partial z / \partial u = 4u / (1 + u^2 + v^2)^2$", rf"${_zu + 0.0:.3f}$"),
                    (r"$\partial z / \partial v = 4v / (1 + u^2 + v^2)^2$", rf"${_zv + 0.0:.3f}$"),
                    (r"$Dz(u, v)(a, b) = a\, \partial_u z + b\, \partial_v z$", rf"${_d:.3f}$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vector fields

    A tangent vector and a smooth vector field are both linear operators satisfying the Leibniz rule, at a point and on the whole manifold respectively:

    $$
    \begin{aligned}
    \text{tangent vector } [\gamma] = X_p \in T_pM \qquad & \leadsto \qquad X_p : C^\infty(M, \mathbb{R}) \longrightarrow \mathbb{R}, \qquad f \longmapsto X_p(f) \\[6pt]
    \text{smooth vector field } X \in \Gamma(TM) \qquad & \leadsto \qquad X : C^\infty(M, \mathbb{R}) \longrightarrow C^\infty(M, \mathbb{R}), \qquad f \longmapsto X(f)
    \end{aligned}
    $$

    For $X \in \Gamma(TM)$, $f, g \in C^\infty(M, \mathbb{R})$, $a, b \in \mathbb{R}$ and $p \in M$

    $$
    X(af + bg) = a\, X(f) + b\, X(g) \in C^\infty(M, \mathbb{R}), \qquad X(fg) = X(f)\, g + f\, X(g) \in C^\infty(M, \mathbb{R})
    $$

    and $X$ evaluated at $p$ is the tangent vector $X_p \in T_pM$. In a chart $\varphi$, with $\partial_i|_p$ the basis of $T_pM$ and $\partial_i$ the basis of $\Gamma(TM)$ over $U \subseteq M$,

    $$
    X_p = \underbrace{v^i}_{\in\, \mathbb{R}}\, \partial_i|_p \qquad \Longrightarrow \qquad X = \underbrace{X^i}_{\in\, C^\infty(U, \mathbb{R})}\, \partial_i = \underbrace{X^i\, \frac{\partial \tilde{x}^j}{\partial x^i}}_{\tilde{X}^j}\, \tilde{\partial}_j \qquad \text{where } \tilde{x} = \tilde{\varphi} \circ \varphi^{-1}(x)
    $$

    In particular the coordinate basis itself transforms with the Jacobian of the change of coordinates

    $$
    \partial_i = \frac{\partial \tilde{x}^j}{\partial x^i}\, \tilde{\partial}_j
    $$

    **Example.** &nbsp; On $\mathbb{S}^2$, $\partial_u|_{(x, y, z)}, \partial_v|_{(x, y, z)}$ form a basis of $T_{(x, y, z)}\mathbb{S}^2$ for all $(x, y, z) \neq (0, 0, 1)$, and $\partial_{\tilde{u}}|_{(x, y, z)}, \partial_{\tilde{v}}|_{(x, y, z)}$ form a basis for all $(x, y, z) \neq (0, 0, -1)$. For $(x, y, z) \neq (0, 0, \pm 1)$, with $(\tilde{u}, \tilde{v}) = \left( \frac{u}{u^2 + v^2},\ \frac{v}{u^2 + v^2} \right)$,

    $$
    \begin{aligned}
    \partial_u &= \frac{\partial \tilde{u}}{\partial u}\, \partial_{\tilde{u}} + \frac{\partial \tilde{v}}{\partial u}\, \partial_{\tilde{v}} = \frac{-u^2 + v^2}{(u^2 + v^2)^2}\, \partial_{\tilde{u}} - \frac{2uv}{(u^2 + v^2)^2}\, \partial_{\tilde{v}} = \underbrace{-(\tilde{u}^2 - \tilde{v}^2)\, \partial_{\tilde{u}} - 2\tilde{u}\tilde{v}\, \partial_{\tilde{v}}}_{=\,0 \text{ at } (0, 0, 1)} \\[8pt]
    \partial_v &= \frac{\partial \tilde{u}}{\partial v}\, \partial_{\tilde{u}} + \frac{\partial \tilde{v}}{\partial v}\, \partial_{\tilde{v}} = -\frac{2uv}{(u^2 + v^2)^2}\, \partial_{\tilde{u}} + \frac{u^2 - v^2}{(u^2 + v^2)^2}\, \partial_{\tilde{v}} = \underbrace{-2\tilde{u}\tilde{v}\, \partial_{\tilde{u}} + (\tilde{u}^2 - \tilde{v}^2)\, \partial_{\tilde{v}}}_{=\,0 \text{ at } (0, 0, 1)}
    \end{aligned}
    $$

    The right hand sides are well defined at $(0, 0, 1)$, where $(\tilde{u}, \tilde{v}) = (0, 0)$, but there they vanish and do not form a basis. Extending by zero gives smooth vector fields on all of $\mathbb{S}^2$:

    $$
    X = \begin{cases} \partial_u & (x, y, z) \neq (0, 0, 1) \\ 0 & (x, y, z) = (0, 0, 1) \end{cases} \in \Gamma(T\mathbb{S}^2), \qquad
    X = \begin{cases} \partial_{\tilde{v}} & (x, y, z) \neq (0, 0, -1) \\ 0 & (x, y, z) = (0, 0, -1) \end{cases} \in \Gamma(T\mathbb{S}^2)
    $$

    $$
    X = \begin{cases} -v\, \partial_u + u\, \partial_v & (x, y, z) \neq (0, 0, 1) \\ -\tilde{v}\, \partial_{\tilde{u}} + \tilde{u}\, \partial_{\tilde{v}} & (x, y, z) \neq (0, 0, -1) \end{cases} \in \Gamma(T\mathbb{S}^2)
    $$

    where for the last field the components in the two charts agree for $(x, y, z) \neq (0, 0, \pm 1)$ under the change of coordinates.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    d_field = mo.ui.dropdown(
        options=["∂_u", "∂_ṽ", "−v ∂_u + u ∂_v"],
        value="∂_u",
        label="$X$ =",
    )
    return (d_field,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREY, d_field, mo, np, table):
    _g = np.linspace(-2.0, 2.0, 11)
    _A, _B = np.meshgrid(_g, _g)
    if d_field.value == "∂_u":
        _n = (1 + 0 * _A, 0 * _A)
        _s = (-(_A**2 - _B**2), -2 * _A * _B)
        _txt = (r"$(1,\ 0)$", r"$\big( -(\tilde{u}^2 - \tilde{v}^2),\ -2\tilde{u}\tilde{v} \big)$")
    elif d_field.value == "∂_ṽ":
        _n = (-2 * _A * _B, _A**2 - _B**2)
        _s = (0 * _A, 1 + 0 * _A)
        _txt = (r"$(-2uv,\ u^2 - v^2)$", r"$(0,\ 1)$")
    else:
        _n = (-_B, _A)
        _s = (-_B, _A)
        _txt = (r"$(-v,\ u)$", r"$(-\tilde{v},\ \tilde{u})$")

    _fig = Figure(figsize=(FULL, 3.7), layout="constrained")
    _axes = _fig.subplots(1, 2)
    _c = np.linspace(0, 2 * np.pi, 200)
    for _ax, (_P, _Q), _title, _pole in zip(_axes, (_n, _s), (r"$\varphi_n$ : $(u, v)$", r"$\varphi_s$ : $(\tilde{u}, \tilde{v})$"), ("$s$", "$n$")):
        _ax.set_title(_title, fontsize=13)
        _ax.set_xlim(-2.5, 2.5)
        _ax.set_ylim(-2.5, 2.5)
        _ax.set_aspect("equal")
        _ax.axhline(0, color="black", lw=0.5)
        _ax.axvline(0, color="black", lw=0.5)
        _ax.plot(np.cos(_c), np.sin(_c), color=GREY, lw=1.0)
        _ax.text(0.06, 1.04, "equator", color=GREY, fontsize=10, ha="left", va="bottom", bbox=dict(boxstyle="round,pad=0.1", facecolor="white", edgecolor="none"))
        _ax.plot(0, 0, "o", color="black", ms=3)
        _ax.text(0.08, -0.1, _pole, fontsize=11, va="top")  # the pole at the origin of this chart
        _m = max(float(np.max(np.hypot(_P, _Q))), 1e-9)
        _ax.quiver(_A, _B, _P, _Q, color=BLUE, angles="xy", scale_units="xy", scale=_m / 0.34, width=0.006)  # arrows scaled per panel
        _ax.set_xticks([-2, 0, 2])
        _ax.set_yticks([-2, 0, 2])

    mo.vstack(
        [
            mo.hstack([d_field], justify="start"),
            table(
                [
                    (r"$(X^u, X^v)$ components in $\varphi_n$", _txt[0]),
                    (r"$(X^{\tilde{u}}, X^{\tilde{v}})$ components in $\varphi_s$", _txt[1]),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, HALF, RED, arrow, blank, mo, np):
    # a vector field and one of its integral curves
    _fig, _ax = blank(HALF, 2.3, (-0.2, 4.2), (-0.2, 2.4))
    _X, _Y = np.meshgrid(np.linspace(0.2, 3.8, 6), np.linspace(0.1, 2.2, 4))
    _U, _V = 0.45 + 0 * _X, 0.22 * np.cos(1.2 * _X) + 0.05 * _Y
    for _x, _y, _dx, _dy in zip(_X.ravel(), _Y.ravel(), _U.ravel(), _V.ravel()):
        arrow(_ax, (_x, _y), (_x + _dx, _y + _dy), BLUE, lw=0.9)
    _fx = lambda x, y: (0.45, 0.22 * np.cos(1.2 * x) + 0.05 * y)
    _xs, _ys = [0.3], [0.9]
    for _ in range(360):  # integral curve by Euler steps
        _dx, _dy = _fx(_xs[-1], _ys[-1])
        _xs.append(_xs[-1] + 0.01 * _dx * 2.2)
        _ys.append(_ys[-1] + 0.01 * _dy * 2.2)
    _ax.plot(_xs, _ys, color=RED)
    _k = 150
    _x0, _y0 = _xs[_k], _ys[_k]
    _dx, _dy = _fx(_x0, _y0)
    arrow(_ax, (_x0, _y0), (_x0 + 1.4 * _dx, _y0 + 1.4 * _dy), BLUE)
    _ax.plot(_x0, _y0, "o", color="black", ms=4)
    _ax.text(_x0 + 0.05, _y0 - 0.3, r"$\gamma(t)$", fontsize=11)
    _ax.text(_x0 + 0.35, _y0 + 0.28, r"$X_{\gamma(t)}$", color=BLUE, fontsize=11, zorder=8, bbox=dict(boxstyle="round,pad=0.08", facecolor="white", edgecolor="none"))
    mo.vstack(
        [
            mo.md(
                r"""
    ### Differential equations

    Let $X \in \Gamma(TM)$ be a smooth vector field. A smooth path $\gamma : \mathbb{R} \longrightarrow M$ is an **integral curve** of $X$ if

    $$
    \gamma'(t) = X_{\gamma(t)} \qquad \forall\ t \in \mathbb{R}
    $$
    """
            ),
            _fig,
            mo.md(
                r"""
    In a chart $\varphi$, and in another chart $\tilde{\varphi}$, this is a first order system of ordinary differential equations

    $$
    \gamma'(t) = X_{\gamma(t)} \qquad \overset{\varphi}{\Longleftrightarrow} \qquad \frac{d}{dt} x^i(t) = X^i(t) \quad \forall\ t,\ \forall\ i \qquad \overset{\tilde{\varphi}}{\Longleftrightarrow} \qquad \frac{d}{dt} \tilde{x}^i(t) = \tilde{X}^i(t) \quad \forall\ t,\ \forall\ i
    $$

    where

    $$
    \gamma(t) = \varphi^{-1}\big( x^i(t)\, e_i \big) = \tilde{\varphi}^{-1}\big( \tilde{x}^i(t)\, e_i \big), \qquad X_{\gamma(t)} = X^i(t)\, \partial_i|_{\gamma(t)} = \tilde{X}^i(t)\, \tilde{\partial}_i|_{\gamma(t)}
    $$

    The two systems are equivalent: the solution curve on $M$ is the same, only its coordinate expression changes.

    **Example.** &nbsp; For $X = -v\, \partial_u + u\, \partial_v = -\tilde{v}\, \partial_{\tilde{u}} + \tilde{u}\, \partial_{\tilde{v}}$ the integral curves solve, on $\varphi_n(\mathbb{S}^2 - \{(0, 0, 1)\})$,

    $$
    \begin{cases} u'(t) = -v(t) \\ v'(t) = u(t) \end{cases} \qquad \Longrightarrow \qquad \begin{cases} u(t) = u_0 \cos(t) - v_0 \sin(t) \\ v(t) = u_0 \sin(t) + v_0 \cos(t) \end{cases}
    $$

    $$
    \Longrightarrow \qquad \gamma(t) = \varphi_n^{-1}\big( u(t), v(t) \big) = \big( \sin\phi_0 \cos(\theta_0 + t),\ \sin\phi_0 \sin(\theta_0 + t),\ \cos\phi_0 \big)
    $$

    the horizontal latitudes around the $z$-axis, where $(\phi_0, \theta_0)$ are the spherical coordinates of $\gamma(0)$.

    **Example.** &nbsp; For $X = u\, \partial_u + v\, \partial_v = -\tilde{u}\, \partial_{\tilde{u}} - \tilde{v}\, \partial_{\tilde{v}}$ the integral curves solve, on $\varphi_n(\mathbb{S}^2 - \{(0, 0, 1)\})$,

    $$
    \begin{cases} u'(t) = u(t) \\ v'(t) = v(t) \end{cases} \qquad \Longrightarrow \qquad \begin{cases} u(t) = u_0\, e^t \\ v(t) = v_0\, e^t \end{cases}
    $$

    $$
    \Longrightarrow \qquad \gamma(t) = \varphi_n^{-1}\big( u(t), v(t) \big) = \big( \operatorname{sech}(t - t_0) \cos\theta_0,\ \operatorname{sech}(t - t_0) \sin\theta_0,\ \tanh(t - t_0) \big)
    $$

    the vertical meridians from $s$ to $n$, where $e^{-t_0} = \sqrt{u_0^2 + v_0^2}$ and $\theta_0$ is the polar angle of $(u_0, v_0)$.
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    d_ode = mo.ui.dropdown(options=["−v ∂_u + u ∂_v", "u ∂_u + v ∂_v"], value="−v ∂_u + u ∂_v", label="$X$ =")
    s_u0 = mo.ui.slider(-2.0, 2.0, 0.1, value=1.4, label="$u_0$", show_value=True)
    s_v0 = mo.ui.slider(-2.0, 2.0, 0.1, value=0.5, label="$v_0$", show_value=True)
    s_t = mo.ui.slider(-3.0, 3.0, 0.05, value=1.0, label="$t$", show_value=True)
    return d_ode, s_t, s_u0, s_v0


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREY, RED, arrow, d_ode, math, mo, np, s_t, s_u0, s_v0, table):
    _az, _el = math.radians(-30), math.radians(20)

    def _pr(x, y, z):
        X = -x * math.sin(_az) + y * math.cos(_az)
        Y = z * math.cos(_el) - (x * math.cos(_az) + y * math.sin(_az)) * math.sin(_el)
        D = (x * math.cos(_az) + y * math.sin(_az)) * math.cos(_el) + z * math.sin(_el)
        return X, Y, D

    def _inv(u, v):
        r = 1 + u**2 + v**2
        return 2 * u / r, 2 * v / r, (r - 2) / r

    def _curve(ax, xyz, color, lw=1.4):
        X, Y, D = _pr(*xyz)
        ax.plot(np.where(D >= 0, X, np.nan), np.where(D >= 0, Y, np.nan), color=color, lw=lw)
        ax.plot(np.where(D < 0, X, np.nan), np.where(D < 0, Y, np.nan), color=color, lw=0.8, ls=(0, (4, 3)))

    _rot = d_ode.value == "−v ∂_u + u ∂_v"
    _u0, _v0, _t = s_u0.value, s_v0.value, s_t.value
    _s = np.linspace(min(0.0, _t), max(0.0, _t), 200)
    _w = np.linspace(-np.pi, np.pi, 400) if _rot else np.linspace(-3.0, 3.0, 400)  # the whole curve (one period, or the window of t)
    if _rot:
        _sol = lambda s: (_u0 * np.cos(s) - _v0 * np.sin(s), _u0 * np.sin(s) + _v0 * np.cos(s))
        _field = lambda u, v: (-v, u)
        _vec3 = lambda x, y, z: (-y, x, 0 * z)
    else:
        _sol = lambda s: (_u0 * np.exp(s), _v0 * np.exp(s))
        _field = lambda u, v: (u, v)
        _vec3 = lambda x, y, z: (-x * z, -y * z, 1 - z**2)  # u d_u + v d_v in ambient coordinates
    _ut, _vt = (float(a) + 0.0 for a in _sol(_t))
    _us, _vs = _sol(_s)
    _uw, _vw = _sol(_w)
    _c = np.linspace(0, 2 * np.pi, 400)

    _fig = Figure(figsize=(FULL, 3.7), layout="constrained")
    _ax, _ax2 = _fig.subplots(1, 2, width_ratios=[1.2, 1])
    _ax.set_xlim(-1.3, 1.3)
    _ax.set_ylim(-1.3, 1.45)
    _ax.set_aspect("equal")
    _ax.axis("off")
    _ax.plot(np.cos(_c), np.sin(_c), color="black")
    _curve(_ax, (np.cos(_c), np.sin(_c), 0 * _c), GREY, lw=1.0)
    for _z in (-0.75, -0.4, 0.0, 0.4, 0.75):
        _rr = math.sqrt(1 - _z**2)
        for _a in np.linspace(0, 2 * np.pi, 12, endpoint=False):
            _q = (_rr * math.cos(_a), _rr * math.sin(_a), _z)
            _Q = _pr(*_q)
            if _Q[2] > 0.15 and math.hypot(_Q[0] - _pr(0, 0, -1)[0], _Q[1] - _pr(0, 0, -1)[1]) > 0.25:
                _d = _vec3(*_q)
                _E = _pr(_q[0] + 0.22 * _d[0], _q[1] + 0.22 * _d[1], _q[2] + 0.22 * _d[2])
                arrow(_ax, _Q[:2], _E[:2], BLUE, lw=0.9)
    _curve(_ax, _inv(_uw, _vw), RED, lw=0.9)
    _X, _Y, _D = _pr(*_inv(_us, _vs))
    _ax.plot(np.where(_D >= 0, _X, np.nan), np.where(_D >= 0, _Y, np.nan), color=RED)
    for (_uu, _vv), _fc in (((_u0, _v0), "white"), ((_ut, _vt), RED)):
        _Q = _pr(*_inv(_uu, _vv))
        _ax.plot(*_Q[:2], "o", color=RED, mfc=_fc, ms=6, alpha=1.0 if _Q[2] >= 0 else 0.4)
    for _q, _n, _dy in (((0, 0, 1), "$n$", 0.1), ((0, 0, -1), "$s$", -0.25)):
        _Q = _pr(*_q)
        _ax.plot(*_Q[:2], "o", color="black", ms=3, alpha=1.0 if _Q[2] > 0 else 0.4)
        _ax.text(_Q[0] - 0.04, _Q[1] + _dy, _n, fontsize=13)

    _ax2.set_title(r"$\varphi_n$ : $(u, v)$", fontsize=13)
    _ax2.set_xlim(-3, 3)
    _ax2.set_ylim(-3, 3)
    _ax2.set_aspect("equal")
    _ax2.axhline(0, color="black", lw=0.6)
    _ax2.axvline(0, color="black", lw=0.6)
    _g = np.linspace(-2.5, 2.5, 9)
    _U, _V = np.meshgrid(_g, _g)
    _ax2.quiver(_U, _V, *_field(_U, _V), color=BLUE, angles="xy", scale_units="xy", scale=5, width=0.006)
    _ax2.plot(np.cos(_c), np.sin(_c), color=GREY, lw=1.0)
    _ax2.text(0.06, 1.04, "equator", color=GREY, fontsize=10, ha="left", va="bottom", bbox=dict(boxstyle="round,pad=0.1", facecolor="white", edgecolor="none"))
    _ax2.plot(_uw, _vw, color=RED, lw=0.9)
    _ax2.plot(_us, _vs, color=RED)
    _ax2.plot(_u0, _v0, "o", color=RED, mfc="white", ms=6)
    _ax2.annotate(r"$\gamma(0)$", (_u0, _v0), textcoords="offset points", xytext=(6, -12), color=RED, fontsize=10, bbox=dict(boxstyle="round,pad=0.08", facecolor="white", edgecolor="none"), zorder=8)
    _ax2.plot(_ut, _vt, "o", color=RED, ms=6, clip_on=True)
    _ax2.annotate(r"$\gamma(t)$", (_ut, _vt), textcoords="offset points", xytext=(6, 4), color=RED, fontsize=10, annotation_clip=True, bbox=dict(boxstyle="round,pad=0.08", facecolor="white", edgecolor="none"), zorder=8)
    _ax2.set_xticks([-3, 0, 3])
    _ax2.set_yticks([-3, 0, 3])

    _p = _inv(_ut, _vt)
    _lab = r"$(u(t), v(t)) = (u_0 \cos t - v_0 \sin t,\ u_0 \sin t + v_0 \cos t)$" if _rot else r"$(u(t), v(t)) = (u_0\, e^t,\ v_0\, e^t)$"
    mo.vstack(
        [
            mo.hstack([d_ode, s_u0, s_v0, s_t], justify="start", gap=2, wrap=True),
            table(
                [
                    (_lab, rf"$({_ut:.2f},\ {_vt:.2f})$"),
                    (r"$\gamma(t) = \varphi_n^{-1}(u(t), v(t))$", rf"$({_p[0] + 0.0:.3f},\ {_p[1] + 0.0:.3f},\ {_p[2] + 0.0:.3f})$"),
                ]
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - Charts $\varphi : U \longrightarrow V \subseteq \mathbb{R}^m$ give local coordinates $x^i$ and local parametrizations $\varphi^{-1}$; a change of charts is a diffeomorphism, with invertible smooth Jacobian $\partial \tilde{x}^j / \partial x^i$.
    - A function is smooth if its local representations $f \circ \varphi^{-1}$ are smooth; its derivative in the direction $[\gamma] = v^i\, \partial_i|_p$ is

        $$
        v^i\, \partial_i (f \circ \varphi^{-1})(\varphi(p)) = \frac{d}{dt}\Big|_{t=0} f \circ \gamma(t).
        $$
    - A vector field $X = X^i\, \partial_i$ is a derivation on $C^\infty(M, \mathbb{R})$; under a change of coordinates

        $$
        \partial_i = \frac{\partial \tilde{x}^j}{\partial x^i}\, \tilde{\partial}_j \qquad \text{and} \qquad \tilde{X}^j = X^i\, \frac{\partial \tilde{x}^j}{\partial x^i}.
        $$
    - Integral curves $\gamma'(t) = X_{\gamma(t)}$ are the solutions of the first order system $\dot{x}^i = X^i$ in any chart; on $\mathbb{S}^2$ the fields $-v\, \partial_u + u\, \partial_v$ and $u\, \partial_u + v\, \partial_v$ have the latitudes and the meridians as integral curves.

    **Next:** Part III, metrics: measuring lengths and angles on a manifold.
    """)
    return


if __name__ == "__main__":
    app.run()
