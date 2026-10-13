import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 09 · The derivative", css_file="phy309.css")


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
    header("Lecture 09", "Week 05", "Lecture 09 · The derivative")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    - A manifold $(M, \mathcal{A})$: a set of points with an atlas of charts $\varphi : U \subseteq M \longrightarrow \varphi(U) \subseteq \mathbb{R}^m$, $\varphi(p) = x^\mu(p)\, e_\mu$, whose transition maps $\tilde{\varphi} \circ \varphi^{-1}$ are diffeomorphisms.
    - A change of coordinates $x \longmapsto \tilde{x}(x)$ has an invertible Jacobian $\dfrac{\partial \tilde{x}^\mu}{\partial x^\nu}$ on $\varphi(U \cap \tilde{U})$.
    - $f : M \longrightarrow N$ is smooth if every coordinate expression $\psi \circ f \circ \varphi^{-1}$, $x \longmapsto y^\alpha(x)\, e_\alpha$, is smooth.

    **In this lecture:** velocities of paths, the tangent space $T_pM$, and the derivative $Df_p$ of a smooth map.
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
    - $\displaystyle \lim_{t \to 0} \frac{f(\gamma(t)) - f(\gamma(0))}{t} = Df_x(v)$ for every path $\gamma : \mathbb{R} \longrightarrow \mathbb{A}$ with $\gamma(0) = x$ and $\gamma'(0) = \displaystyle\lim_{t \to 0} \frac{\gamma(t) - \gamma(0)}{t} = v$.

    This second condition still depends on the affine structures, but it suggests how to compute $Df_x(v)$ without ever forming $x + tv$: pick a path $\gamma$ with $\gamma(0) = x$ and $\gamma'(0) = v$, consider $\sigma = f \circ \gamma : \mathbb{R} \longrightarrow \mathbb{B}$ and compute

    $$
    \sigma(0) = f(\gamma(0)) = f(x), \qquad \sigma'(0) = Df_{\gamma(0)}(\gamma'(0)) = Df_x(v)
    $$

    $\leadsto$ &nbsp; $f$ maps paths through $x$ to paths through $f(x)$, and $Df_x$ maps velocities at $x$ to velocities at $f(x)$. This observation is what generalizes the derivative to maps between manifolds, where there is no affine structure to speak of.

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
    **Remark.** If $\gamma, \tilde{\gamma}$ have the same velocity in one chart, they have the same velocity in every chart containing $p$ (the example below shows why). Having the same velocity is therefore an equivalence relation on the smooth paths through $p$, and $[\gamma]$ denotes the equivalence class of $\gamma$.
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
    T_p M = \left\{\, [\gamma] \;\middle|\; \gamma : \mathbb{R} \longrightarrow M,\ \gamma(0) = p \,\right\}
    $$
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

    $$
    (u, v) = \varphi_n(x, y, z) = \left( \frac{x}{1 - z},\ \frac{y}{1 - z} \right), \qquad (x, y, z) \neq (0, 0, 1)
    $$

    $$
    \leadsto \qquad \varphi_n^{-1}(u, v) = \left( \frac{2u}{1 + u^2 + v^2},\ \frac{2v}{1 + u^2 + v^2},\ \frac{-1 + u^2 + v^2}{1 + u^2 + v^2} \right)
    $$

    $$
    (\tilde{u}, \tilde{v}) = \varphi_s(x, y, z) = \left( \frac{x}{1 + z},\ \frac{y}{1 + z} \right), \qquad (x, y, z) \neq (0, 0, -1)
    $$

    $$
    \leadsto \qquad \varphi_s^{-1}(\tilde{u}, \tilde{v}) = \left( \frac{2\tilde{u}}{1 + \tilde{u}^2 + \tilde{v}^2},\ \frac{2\tilde{v}}{1 + \tilde{u}^2 + \tilde{v}^2},\ \frac{1 - \tilde{u}^2 - \tilde{v}^2}{1 + \tilde{u}^2 + \tilde{v}^2} \right)
    $$

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

    Why is this chart independent? If $(\varphi_n \circ \gamma)'(0) = (\varphi_n \circ \tilde{\gamma})'(0)$, then also $(\varphi_s \circ \gamma)'(0) = (\varphi_s \circ \tilde{\gamma})'(0)$, because in the chart $\varphi_s$

    $$
    (\tilde{u}(t), \tilde{v}(t)) = \left( \frac{u(t)}{u(t)^2 + v(t)^2},\ \frac{v(t)}{u(t)^2 + v(t)^2} \right)
    $$

    $$
    \begin{bmatrix} \tilde{a} \\ \tilde{b} \end{bmatrix} = \begin{bmatrix} \tilde{u}' \\ \tilde{v}' \end{bmatrix} = \underbrace{\frac{1}{(u^2 + v^2)^2} \begin{bmatrix} v^2 - u^2 & -2uv \\ -2uv & u^2 - v^2 \end{bmatrix}}_{\text{depends only on } p = \gamma(0) = \tilde{\gamma}(0)} \begin{bmatrix} a \\ b \end{bmatrix}
    $$

    and the same velocity $(a, b)$ in $\varphi_n$ gives the same velocity $(\tilde{a}, \tilde{b})$ in $\varphi_s$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    s_u = mo.ui.slider(-2.0, 2.0, 0.1, value=1.2, label="$u(0)$", show_value=True)
    s_v = mo.ui.slider(-2.0, 2.0, 0.1, value=0.6, label="$v(0)$", show_value=True)
    s_a = mo.ui.slider(-1.0, 1.0, 0.1, value=0.6, label="$a$", show_value=True)
    s_b = mo.ui.slider(-1.0, 1.0, 0.1, value=0.8, label="$b$", show_value=True)
    return s_a, s_b, s_u, s_v


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, GREY, RED, arrow, mo, np, s_a, s_b, s_u, s_v, table):
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

        _Ls = max(3.0, 1.2 * max(abs(_ut) + abs(_at), abs(_vt) + abs(_bt)))  # south panel follows its point and arrow
        _fig = Figure(figsize=(FULL, 3.9), layout="constrained")
        _axes = _fig.subplots(1, 2)
        _c = np.linspace(0, 2 * np.pi, 200)
        for _ax, _title, _L in zip(_axes, (r"$\varphi_n$ : $(u, v)$", r"$\varphi_s$ : $(\tilde{u}, \tilde{v})$"), (3.0, _Ls)):
            _ax.set_title(_title, fontsize=13)
            _ax.set_xlim(-_L, _L)
            _ax.set_ylim(-_L, _L)
            _ax.set_aspect("equal")
            _ax.axhline(0, color="black", lw=0.6)
            _ax.axvline(0, color="black", lw=0.6)
            _ax.plot(np.cos(_c), np.sin(_c), color=GREY, lw=0.8)
            _ax.text(0.06, 1.04, "equator", color=GREY, fontsize=10, ha="left", va="bottom", bbox=dict(boxstyle="round,pad=0.1", facecolor="white", edgecolor="none"))
            _ax.set_xticks([-round(_L, 1), 0, round(_L, 1)])
            _ax.set_yticks([-round(_L, 1), 0, round(_L, 1)])
        for (_pu, _pv), _col, _name in ((_g, BLUE, r"$\gamma$"), (_h, RED, r"$\tilde{\gamma}$")):
            _axes[0].plot(_pu, _pv, color=_col)
            _axes[0].annotate(_name, (_pu[-1], _pv[-1]), textcoords="offset points", xytext=(4, 4), color=_col, fontsize=12)
            _q = _pu**2 + _pv**2
            _q = np.where(_q < 1e-6, np.nan, _q)  # the path image passes through infinity where it crosses s
            _axes[1].plot(_pu / _q, _pv / _q, color=_col)
        arrow(_axes[0], (_u, _v), (_u + _a, _v + _b), GREEN)
        arrow(_axes[1], (_ut, _vt), (_ut + _at, _vt + _bt), GREEN)
        _axes[0].plot(_u, _v, "o", color="black", ms=5)
        _axes[1].plot(_ut, _vt, "o", color="black", ms=5)
        _out = mo.vstack(
            [
                table(
                    [
                        (r"$\varphi_n(p) = (u(0), v(0))$", rf"$({_u:.2f},\ {_v:.2f})$"),
                        (r"$(a, b) = (\varphi_n \circ \gamma)'(0) = (\varphi_n \circ \tilde{\gamma})'(0)$", rf"$({_a:.2f},\ {_b:.2f})$"),
                        (r"$\varphi_s(p) = (\tilde{u}(0), \tilde{v}(0))$", rf"$({_ut:.2f},\ {_vt:.2f})$"),
                        (r"$(\tilde{a}, \tilde{b}) = (\varphi_s \circ \gamma)'(0) = (\varphi_s \circ \tilde{\gamma})'(0)$", rf"$({_at:.2f},\ {_bt:.2f})$"),
                    ]
                ),
                _fig,
            ]
        )
    mo.vstack([mo.hstack([s_u, s_v, s_a, s_b], justify="start", gap=3, wrap=True), _out])
    return


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, RED, arrow, blob, definition, mo, np):
    _fig = Figure(figsize=(FULL, 2.6), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-2.9, 10.2)
    _ax.set_ylim(-1.6, 1.8)
    _ax.set_aspect("equal")
    _ax.axis("off")
    _c = np.linspace(0, 2 * np.pi, 200)
    _t = np.linspace(-1.0, 1.0, 100)
    for _x0, _name, _lab in ((0.0, "$M$", "$p$"), (7.2, "$N$", "$f(p)$")):
        _ax.plot(*blob(_x0, 0.0, 2.45, 1.3, wobble=0.1, seed=6 if _x0 == 0 else 7), color="black")
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

    $$
    \gamma(t) = \varphi_n^{-1}\big( u(0) + t a,\ v(0) + t b \big) \qquad \Longrightarrow \qquad (\varphi_n \circ \gamma)'(0) = \begin{bmatrix} a \\ b \end{bmatrix}
    $$

    $$
    \therefore \quad T_p \mathbb{S}^2 \approx \mathbb{R}^2
    $$

    The correspondence $[\gamma] \longmapsto (\varphi_n \circ \gamma)'(0)$ is a bijection, and we will later use it to make $T_p\mathbb{S}^2$ a vector space.

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
    Df_p[\gamma] = [f \circ \gamma] \ \text{“}=\text{”}\ (f \circ \gamma)'(0)
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

    $$
    Df_p[\gamma] = [f \circ \gamma] = [\, 0 : \mathbb{R} \to \mathbb{R} \,] \ \text{“}=\text{”}\ \frac{d}{dt}\bigg|_{t=0} f \circ \gamma(t) = 0
    $$

    is the class of the zero function (all functions with zero derivative at $t = 0$), while

    $$
    Df_p[\sigma] = [f \circ \sigma] = [\, \sin : \mathbb{R} \to \mathbb{R} \,] \ \text{“}=\text{”}\ \frac{d}{dt}\bigg|_{t=0} f \circ \sigma(t) = \frac{d}{dt}\bigg|_{t=0} \sin(t) = 1
    $$

    is the class of functions with derivative $1$ at $t = 0$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    s_t = mo.ui.slider(-1.5, 1.5, 0.05, value=0.5, label="$t$", show_value=True)
    return (s_t,)


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, HALF, RED, arrow, math, mo, np, s_t, table):
    _az, _el = math.radians(-30), math.radians(16)

    def _pr(x, y, z):
        X = -x * math.sin(_az) + y * math.cos(_az)
        Y = z * math.cos(_el) - (x * math.cos(_az) + y * math.sin(_az)) * math.sin(_el)
        D = (x * math.cos(_az) + y * math.sin(_az)) * math.cos(_el) + z * math.sin(_el)
        return X, Y, D

    def _curve(ax, x, y, z, color):
        X, Y, D = _pr(x, y, z)
        ax.plot(np.where(D >= 0, X, np.nan), np.where(D >= 0, Y, np.nan), color=color)
        ax.plot(np.where(D < 0, X, np.nan), np.where(D < 0, Y, np.nan), color=color, lw=0.9, ls=(0, (4, 3)))

    _t = s_t.value
    _fig = Figure(figsize=(FULL, HALF), layout="constrained")
    _ax, _ax2 = _fig.subplots(1, 2, width_ratios=[2.4, 1])
    _ax.set_xlim(-1.5, 1.9)
    _ax.set_ylim(-1.3, 1.6)
    _ax.set_aspect("equal")
    _ax.axis("off")
    _c = np.linspace(0, 2 * np.pi, 400)
    _ax.plot(np.cos(_c), np.sin(_c), color="black")
    _curve(_ax, np.cos(_c), np.sin(_c), 0 * _c, BLUE)
    _curve(_ax, np.cos(_c), 0 * _c, np.sin(_c), RED)
    _P = _pr(1, 0, 0)
    arrow(_ax, _P[:2], _pr(1, 0.75, 0)[:2], GREEN)
    arrow(_ax, _P[:2], _pr(1, 0, 0.75)[:2], GREEN)
    _ax.plot(*_P[:2], "o", color="black", ms=4.5)
    _ax.text(_P[0] + 0.08, _P[1] - 0.22, "$p$", fontsize=14)
    for _q, _n, _dy in (((0, 0, 1), "$n$", 0.12), ((0, 0, -1), "$s$", -0.3)):
        _Q = _pr(*_q)
        _ax.plot(*_Q[:2], "o", color="black", ms=3, alpha=1.0 if _Q[2] > 0 else 0.4)
        _ax.text(_Q[0] - 0.04, _Q[1] + _dy, _n, fontsize=13)
    _G = _pr(math.cos(_t), math.sin(_t), 0)
    _S = _pr(math.cos(_t), 0, math.sin(_t))
    _ax.plot(*_G[:2], "o", color=BLUE, ms=6)
    _ax.plot(*_S[:2], "o", color=RED, ms=6)
    _e = _pr(1, 0.75, 0)
    _ax.text(_e[0] + 0.06, _e[1] - 0.04, r"$[\gamma]$", color=GREEN, fontsize=14)
    _e = _pr(1, 0, 0.75)
    _ax.text(_e[0] + 0.07, _e[1] - 0.02, r"$[\sigma]$", color=GREEN, fontsize=14)
    _ax.text(-0.75, -0.48, r"$\gamma$", color=BLUE, fontsize=14)
    _ax.text(0.33, 0.62, r"$\sigma$", color=RED, fontsize=14)

    _ax2.set_xlim(-1.6, 1.9)
    _ax2.set_ylim(-1.3, 1.6)
    _ax2.axis("off")
    _ax2.plot([0, 0], [-1.15, 1.15], color="black")
    for _y, _lab in ((1, "$f(n) = 1$"), (-1, "$f(s) = -1$")):
        _ax2.plot(0, _y, "o", color="black", ms=3.5)
        _ax2.text(0.25, _y - 0.05, _lab, fontsize=13)
    _ax2.plot(0, 0, "o", color=BLUE, ms=6)
    _ax2.plot(0, math.sin(_t), "o", color=RED, ms=6)
    _ax2.text(-0.25, 0, r"$f(\gamma(t))$", color=BLUE, fontsize=11, ha="right", va="center")
    _ax2.text(-0.25, math.sin(_t), r"$f(\sigma(t))$", color=RED, fontsize=11, ha="right", va="center")
    _ax2.text(0, 1.35, r"$\mathbb{R}$", fontsize=13, ha="center")

    _table = table(
        [
            (r"$\gamma(t) = (\cos t,\ \sin t,\ 0)$", rf"$({math.cos(_t):.2f},\ {math.sin(_t):.2f},\ 0)$"),
            (r"$\sigma(t) = (\cos t,\ 0,\ \sin t)$", rf"$({math.cos(_t):.2f},\ 0,\ {math.sin(_t):.2f})$"),
            (r"$f(\gamma(t)) = 0$", "$0$"),
            (r"$f(\sigma(t)) = \sin t$", rf"${math.sin(_t) + 0.0:.2f}$"),
        ]
    )
    mo.vstack(
        [
            mo.hstack([s_t], justify="start"),
            _table,
            _fig,
            mo.md(
                r"""
    In the chart $\varphi_n$ the two velocities are

    $$
    (\varphi_n \circ \gamma)'(0) = \begin{bmatrix} 0 \\ 1 \end{bmatrix}, \qquad (\varphi_n \circ \sigma)'(0) = \begin{bmatrix} 1 \\ 0 \end{bmatrix}
    $$

    **Remark.** Using the ambient space $\mathbb{R}^3$ instead, $[\gamma] \ \text{“}=\text{”} \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix}$ and $[\sigma] \ \text{“}=\text{”} \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}$; the arrows in the sketch are these ambient vectors.
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - Two paths through $p$ have the same velocity if their coordinate expressions in one (hence every) chart have the same derivative at $0$.
    - The tangent space $T_pM$ is the set of velocity classes $[\gamma]$ of smooth paths with $\gamma(0) = p$; a chart identifies it with $\mathbb{R}^m$.
    - The derivative of a smooth map $f : M \longrightarrow N$ at $p$ is $Df_p[\gamma] = [f \circ \gamma]$, from $T_pM$ to $T_{f(p)}N$.
    - For $f : M \longrightarrow \mathbb{R}$ the class $[f \circ \gamma]$ is the number $(f \circ \gamma)'(0)$.

    **Next:** tangent vectors as derivations, and the vector space structure of $T_pM$.
    """)
    return


if __name__ == "__main__":
    app.run()
