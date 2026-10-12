import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 10 · Derivations", css_file="phy309.css")


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
        <b>Date</b><span>{date}</span><b>Instructor</b><span>Professor Scarinci</span>
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
    header("Lecture 10", "Week 06", "Lecture 10 · Derivations")
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, GREY, ORANGE, RED, arrow, blob, np):
    # Paths through p with the same velocity, seen on M and in a chart
    fig_paths = Figure(figsize=(5.4, 4.2), layout="constrained")
    _ax = fig_paths.subplots()
    _ax.set_aspect("equal")
    _ax.axis("off")
    _t = np.linspace(0, 2 * np.pi, 300)
    _ax.plot(*blob(3.2, 3.0, 2.05, 1.3, wobble=0.1, seed=8), color="black")
    _ax.text(1.4, 4.1, "$M$", fontsize=13)
    _ax.plot(*blob(3.2, 3.05, 0.8, 0.62, wobble=0.06, seed=9), color=GREY)
    _ax.text(2.45, 3.65, "$U$", color=GREY, fontsize=11)
    _s = np.linspace(-0.6, 0.6, 80)
    _P = (3.2, 3.05)
    for _col, _k in ((BLUE, 0.0), (RED, 0.9), (ORANGE, -0.9)):
        _ax.plot(_P[0] + _s, _P[1] + 0.25 * _s - _k * _s**2, color=_col)
    arrow(_ax, _P, (_P[0] + 0.55, _P[1] + 0.14), GREEN)
    _ax.text(_P[0] + 0.9, _P[1] + 0.42, r"$v_p = [\gamma]$", color=GREEN, fontsize=11, bbox=dict(boxstyle="round,pad=0.1", facecolor="white", edgecolor="none", alpha=0.85))
    _ax.plot(*_P, "o", color="black", ms=4)
    _ax.text(_P[0] - 0.08, _P[1] - 0.28, "$p$", fontsize=12, ha="right")
    # the real line on the left and the three paths as maps from it
    arrow(_ax, (-0.5, 1.6), (0.9, 1.6), "black", lw=1.0)
    _ax.plot(0.2, 1.6, "o", color="black", ms=3.5)
    _ax.text(0.2, 1.4, "$0$", fontsize=10, ha="center", va="top")
    _ax.text(0.95, 1.45, r"$\mathbb{R}$", fontsize=11)
    for _col, _dy, _name in ((BLUE, 0.5, r"$\gamma$"), (RED, 0.25, r"$\tilde{\gamma}$"), (ORANGE, 0.0, r"$\hat{\gamma}$")):
        arrow(_ax, (0.3, 1.9 + _dy), (1.3, 2.3 + _dy), _col, lw=1.0, connectionstyle="arc3,rad=-0.3")
        _ax.text(0.2, 1.9 + _dy, _name, color=_col, fontsize=11, ha="right", va="center")
    # chart box below
    _B = (4.2, 0.2)
    _ax.plot([_B[0], _B[0] + 1.9, _B[0] + 1.9, _B[0], _B[0]], [_B[1], _B[1], _B[1] + 1.6, _B[1] + 1.6, _B[1]], color=GREY)
    _ax.text(_B[0] + 1.95, _B[1] + 0.05, r"$\varphi(U) \subseteq \mathbb{R}^m$", color=GREY, fontsize=10)
    _Q = (_B[0] + 0.9, _B[1] + 0.8)
    for _col, _k in ((BLUE, 0.0), (RED, 1.2), (ORANGE, -1.2)):
        _ax.plot(_Q[0] + _s, _Q[1] + 0.3 * _s - _k * _s**2, color=_col)
    arrow(_ax, _Q, (_Q[0] + 0.6, _Q[1] + 0.18), GREEN)
    _ax.text(_Q[0] + 0.65, _Q[1] + 0.3, r"$(\varphi \circ \gamma)'(0)$", color=GREEN, fontsize=10)
    _ax.plot(*_Q, "o", color="black", ms=4)
    _ax.text(_Q[0] - 0.05, _Q[1] - 0.5, r"$\varphi(p)$", fontsize=10, ha="center", va="top", bbox=dict(boxstyle="round,pad=0.1", facecolor="white", edgecolor="none", alpha=0.85))
    arrow(_ax, (3.9, 2.3), (4.6, 1.85), "black", connectionstyle="arc3,rad=-0.3")
    _ax.text(4.45, 2.35, r"$\varphi$", fontsize=12)
    _ax.set_xlim(-0.7, 7.2)
    _ax.set_ylim(-0.1, 4.6)
    _ = None  # no cell output: the figures are returned, not displayed here
    return (fig_paths,)


@app.cell(hide_code=True)
def _(fig_paths, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    - Two smooth paths through $p \in M$ have the same velocity if $(\varphi \circ \gamma)'(0) = (\varphi \circ \tilde{\gamma})'(0)$ for some (hence every) chart $\varphi$.
    - The tangent space $T_pM$ is the set of velocity classes $v_p = [\gamma]$ of paths with $\gamma(0) = p$.
    - The derivative of a smooth map $f : M \longrightarrow N$ at $p$ is $Df_p : T_pM \longrightarrow T_{f(p)}N$, $Df_p[\gamma] = [f \circ \gamma]$.
    - For a smooth function $f : M \longrightarrow \mathbb{R}$, the affine structure of $\mathbb{R}$ gives $T_{f(p)}\mathbb{R} \approx \mathbb{R}$ and $Df_p(v_p) = \dfrac{d}{dt}\Big|_{t=0} f \circ \gamma(t)$, the directional derivative of $f$ at $p$ in the direction $v_p$.

    **Today:** tangent vectors as derivations, the vector space structure of $T_pM$, and the coordinate basis $\partial_i|_p$.
    """
            ),
            fig_paths,
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, HALF, RED, mo, np):
    _fig = Figure(figsize=(HALF, 3.0), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_xlim(-1.8, 2.6)
    _ax.set_ylim(-1.7, 1.9)
    _ax.set_aspect("equal")
    _ax.axis("off")
    _ax.plot([-1.7, 2.4], [0, 0], color=GREY, lw=0.8)
    _ax.plot([0, 0], [-1.6, 1.7], color=GREY, lw=0.8)
    _c = np.linspace(0, 2 * np.pi, 200)
    _ax.plot(np.cos(_c), np.sin(_c), color=BLUE)
    _ax.plot([-1.7, 2.4], [0, 0], color=RED)
    _ax.plot(1, 0, "o", color="black", ms=5)
    _ax.text(1.08, -0.38, r"$\varphi_n(p)$", fontsize=13)
    _ax.text(-1.75, 1.25, r"$\varphi_n \circ \gamma(t)$", color=BLUE, fontsize=13)
    _ax.text(1.15, 0.22, r"$\varphi_n \circ \sigma(t)$", color=RED, fontsize=13)
    _ax.text(2.45, -0.08, "$u$", fontsize=13)
    _ax.text(-0.05, 1.72, "$v$", fontsize=13, ha="center")

    mo.vstack(
        [
            mo.md(
                r"""
    ## II.5 &nbsp; Derivations

    ### Directional derivatives

    **Example.** &nbsp; On $\mathbb{S}^2 = \{\, (x, y, z) \in \mathbb{R}^3 \mid x^2 + y^2 + z^2 = 1 \,\}$ take again the height function, the point $p$ and the two paths

    $$
    h : \mathbb{S}^2 \longrightarrow \mathbb{R}, \qquad h(x, y, z) = z, \qquad p = (1, 0, 0), \qquad \gamma(t) = \big( \cos(t),\ \sin(t),\ 0 \big), \qquad \sigma(t) = \big( \cos(t),\ 0,\ \sin(t) \big)
    $$

    In the chart $\varphi_n$ and its inverse (the local coordinate parametrization)

    $$
    \varphi_n(x, y, z) = \left( \frac{x}{1 - z},\ \frac{y}{1 - z} \right), \qquad \varphi_n^{-1}(u, v) = \left( \tfrac{2u}{1 + u^2 + v^2},\ \tfrac{2v}{1 + u^2 + v^2},\ \tfrac{-1 + u^2 + v^2}{1 + u^2 + v^2} \right)
    $$

    the function and the paths have the local coordinate representations

    $$
    h \circ \varphi_n^{-1}(u, v) = \frac{-1 + u^2 + v^2}{1 + u^2 + v^2}, \qquad \varphi_n \circ \gamma(t) = \big( \cos(t),\ \sin(t) \big), \qquad \varphi_n \circ \sigma(t) = \left( \frac{\cos(t)}{1 - \sin(t)},\ 0 \right)
    $$
    """
            ),
            _fig,
            mo.md(
                r"""
    The derivatives are the velocities at $t = 0$ of the functions $h \circ \gamma, h \circ \sigma : \mathbb{R} \longrightarrow \mathbb{R}$

    $$
    \begin{aligned}
    Dh_p[\gamma] = [h \circ \gamma] &= (h \circ \gamma)'(0) = \frac{d}{dt}\bigg|_{t=0} (0) = 0 = \big[ (h \circ \varphi_n^{-1}) \circ (\varphi_n \circ \gamma) \big] \\[4pt]
    Dh_p[\sigma] = [h \circ \sigma] &= (h \circ \sigma)'(0) = \frac{d}{dt}\bigg|_{t=0} \big( \sin(t) \big) = 1 = \big[ (h \circ \varphi_n^{-1}) \circ (\varphi_n \circ \sigma) \big]
    \end{aligned}
    $$

    Here we can skip the coordinate representation only because $h$, $\gamma$ and $\sigma$ are simple; usually the last expression is the one we must compute.

    $\leadsto$ &nbsp; tangent vectors $v_p = [\gamma] \in T_p M$ let us differentiate scalar functions $f : M \longrightarrow \mathbb{R}$

    $$
    Df_p(v_p) \ \text{“}=\text{”}\ \frac{d}{dt}\bigg|_{t=0} (f \circ \gamma)(t)
    $$

    ### Derivations
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            definition(
                r"""
    Let $C^\infty(M, \mathbb{R})$ be the space of smooth functions on $M$. Given $p \in M$, a **derivation** of $M$ at $p$ is a linear functional (a function of functions)

    $$
    X_p : C^\infty(M, \mathbb{R}) \longrightarrow \mathbb{R}
    $$

    satisfying the Leibniz rule (the product rule)

    $$
    X_p(f g) = X_p(f)\, g(p) + f(p)\, X_p(g)
    $$

    The space of derivations of $M$ at $p$, the functionals that behave like derivatives at $p$, is denoted $\mathrm{Der}_p(M)$.
    """,
                "Derivation",
            ),
            theorem(
                r"""
    $$
    \mathrm{Der}_p(M) \approx T_p M
    $$

    Directional derivatives are derivations (they satisfy the Leibniz rule), and every derivation is the directional derivative along some equivalence class of paths.
    """,
                "Derivations are tangent vectors",
            ),
            mo.md(
                r"""
    **Proof.** Given $[\gamma] \in T_p M$, choose any representative $\gamma$. Define

    $$
    X_p(f) = \frac{d}{dt}\bigg|_{t=0} (f \circ \gamma)(t) \in \mathbb{R}
    $$

    $$
    \begin{aligned}
    \Longrightarrow \quad X_p(f \cdot g) &= \frac{d}{dt}\bigg|_{t=0} \big( (f \cdot g) \circ \gamma \big) \\[4pt]
    &= (f \circ \gamma)'(0)\, g(\gamma(0)) + f(\gamma(0))\, (g \circ \gamma)'(0) = X_p(f)\, g(p) + f(p)\, X_p(g)
    \end{aligned}
    $$

    $$
    \therefore \quad X_p \in \mathrm{Der}_p(M)
    $$

    Moreover $X_p$ depends only on $[\gamma]$ and not on the choice of representative $\gamma$: in a chart $\varphi$, writing $f \circ \gamma = (f \circ \varphi^{-1}) \circ (\varphi \circ \gamma)$,

    $$
    \begin{aligned}
    \frac{d}{dt}\bigg|_{t=0} (f \circ \gamma)(t) &= \frac{d}{dt}\bigg|_{t=0} (f \circ \varphi^{-1}) \circ (\varphi \circ \gamma)(t) \\[4pt]
    &= \underbrace{D(f \circ \varphi^{-1})_{\varphi(p)}}_{\text{independent of } \gamma}\ \underbrace{(\varphi \circ \gamma)'(0)}_{\text{same for every } \gamma \text{ in } [\gamma]}
    \end{aligned}
    $$

    Conversely, given $X_p \in \mathrm{Der}_p(M)$ we define $[\gamma] \in T_p M$. Work in a chart $\varphi$ with local coordinate functions $x^i : U \longrightarrow \mathbb{R}$, $\varphi(q) = x^i(q)\, e_i$, so that $x^i \circ \varphi^{-1}(x) = x^i$, and set

    $$
    \Longrightarrow \quad X_p(x^i) = v^i \in \mathbb{R}
    $$

    Define &nbsp; $\gamma(t) = \varphi^{-1}\big( \varphi(p) + t v^i e_i \big) = \varphi^{-1}\big( (x^i(p) + t v^i)\, e_i \big)$

    $$
    \begin{aligned}
    \Longrightarrow \quad \frac{d}{dt}\bigg|_{t=0} (f \circ \gamma)(t) &= \frac{d}{dt}\bigg|_{t=0} (f \circ \varphi^{-1})\big( \varphi(p) + t v^i e_i \big) \\[4pt]
    &= \frac{\partial}{\partial x^i} (f \circ \varphi^{-1})(\varphi(p)) \cdot v^i
    \end{aligned}
    $$

    $$
    \Longrightarrow \quad \frac{d}{dt}\bigg|_{t=0} (x^i \circ \gamma)(t) = \frac{\partial x^i}{\partial x^j}(\varphi(p))\, v^j = v^i = X_p(x^i)
    $$

    To conclude that $X_p(f) = \frac{\partial}{\partial x^i}(f \circ \varphi^{-1})(\varphi(p))\, v^i$ for *every* $f$, two more facts:

    - derivations are local: if $f = 0$ near $p$, write $f = f \chi$ with $\chi$ smooth, $\chi = 1$ where $f \neq 0$ and $\chi(p) = 0$ &nbsp; $\Longrightarrow$ &nbsp; $X_p(f) = X_p(f)\, \chi(p) + f(p)\, X_p(\chi) = 0$. &nbsp; So $X_p(f)$ depends only on $f$ near $p$, and $X_p$ can be applied to the local functions $x^i$.
    - near $p$: &nbsp; $f = f(p) + \big( x^i - x^i(p) \big)\, g_i$ with $g_i$ smooth and $g_i(p) = \frac{\partial}{\partial x^i}(f \circ \varphi^{-1})(\varphi(p))$, namely $g_i(q) = \int_0^1 \partial_i (f \circ \varphi^{-1})\big( \varphi(p) + s (\varphi(q) - \varphi(p)) \big)\, ds$.

    $$
    \Longrightarrow \quad X_p(f) = \underbrace{X_p(f(p))}_{=\,0 \ (\text{Leibniz on } 1 \cdot 1)} + X_p(x^i)\, g_i(p) + \underbrace{\big( x^i(p) - x^i(p) \big)}_{=\,0} X_p(g_i) = v^i\, \frac{\partial}{\partial x^i}(f \circ \varphi^{-1})(\varphi(p))
    $$

    $\Longrightarrow$ &nbsp; $X_p$ is the directional derivative at $p$ in the direction of $[\gamma]$, which we already know is independent of the chart $\varphi$.

    $\therefore$ &nbsp; we have a bijection $T_p M \overset{\sim}{\longrightarrow} \mathrm{Der}_p(M)$ given with respect to a chart $\varphi$ with local coordinate functions $x^i$ by

    $$
    [\gamma] \ \text{ such that } \ (\varphi \circ \gamma)'(0) = v^i e_i \qquad \longleftrightarrow \qquad X_p \ \text{ such that } \ X_p(x^i) = v^i \qquad \square
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Coordinate basis

    **Remark.** $\mathrm{Der}_p(M)$ is naturally a vector space:

    $$
    \text{if } X_p, Y_p \in \mathrm{Der}_p(M),\ \alpha, \beta \in \mathbb{R} \qquad \Longrightarrow \quad \alpha X_p + \beta Y_p \in \mathrm{Der}_p(M)
    $$

    $\Longrightarrow$ &nbsp; the bijection above defines a vector space structure on the tangent space $T_p M$.

    **Remark.** Each choice of local chart defines a basis of $T_p M$. Given $\varphi : U \subseteq M \longrightarrow \varphi(U) \subseteq \mathbb{R}^m$ with $p \in U$, define $\partial_i|_p \in T_p M \approx \mathrm{Der}_p(M)$ by

    $$
    \partial_i|_p = \big[\, t \longmapsto \varphi^{-1}(\varphi(p) + t e_i) \,\big]
    $$

    $$
    \longleftrightarrow \qquad \partial_i|_p (f) = \frac{d}{dt}\bigg|_{t=0} (f \circ \varphi^{-1})(\varphi(p) + t e_i) = \frac{\partial}{\partial x^i}\bigg|_{x = \varphi(p)} (f \circ \varphi^{-1})
    $$

    The $m$ vectors $\partial_1|_p, \dots, \partial_m|_p$ are linearly independent (they map to $e_1, \dots, e_m$ under $[\gamma] \longmapsto (\varphi \circ \gamma)'(0)$), so they form the **coordinate basis** of $T_pM$ associated with the chart $\varphi$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** &nbsp; $\mathbb{S}^2$, &nbsp; $\varphi_n = (u, v) : \mathbb{S}^2 - \{n\} \longrightarrow \mathbb{R}^2$, &nbsp; $p = (1, 0, 0)$

    $$
    \begin{aligned}
    \partial_u|_p &= \big[\, t \longmapsto \varphi_n^{-1}(1 + t,\ 0) \,\big] \\[4pt]
    &= \left[\, t \longmapsto \left( \frac{2(1 + t)}{1 + (1 + t)^2},\ 0,\ \frac{-1 + (1 + t)^2}{1 + (1 + t)^2} \right) \right] = [\sigma]
    \end{aligned}
    $$

    $$
    \partial_u|_p (f) = \frac{\partial}{\partial u}\bigg|_{(u, v) = (1, 0)} (f \circ \varphi_n^{-1})(u, v)
    $$

    $$
    \begin{aligned}
    \partial_u|_p (h) &= \frac{\partial}{\partial u}\bigg|_{(1, 0)} \frac{-1 + u^2 + v^2}{1 + u^2 + v^2} \\[4pt]
    &= \frac{2u (1 + u^2 + v^2) - (-1 + u^2 + v^2)\, 2u}{(1 + u^2 + v^2)^2}\bigg|_{(1, 0)} = \frac{4 - 0}{2^2} = 1
    \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    s_u = mo.ui.slider(-2.0, 2.0, 0.1, value=1.0, label="$u$", show_value=True)
    s_v = mo.ui.slider(-2.0, 2.0, 0.1, value=0.0, label="$v$", show_value=True)
    return s_u, s_v


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREY, RED, arrow, math, mo, np, s_u, s_v, table):
    _az, _el = math.radians(-30), math.radians(16)

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

    _u, _v = s_u.value, s_v.value
    _r = 1 + _u**2 + _v**2
    _p = np.array(_inv(_u, _v))
    # d(phi_n^{-1})/du and /dv as vectors of R^3
    _du = np.array([2 * (1 - _u**2 + _v**2), -4 * _u * _v, 4 * _u]) / _r**2
    _dv = np.array([-4 * _u * _v, 2 * (1 + _u**2 - _v**2), 4 * _v]) / _r**2
    _hu, _hv = 4 * _u / _r**2 + 0.0, 4 * _v / _r**2 + 0.0

    _fig = Figure(figsize=(FULL, 3.7), layout="constrained")
    _ax, _ax2 = _fig.subplots(1, 2, width_ratios=[1.25, 1])
    _ax.set_xlim(-1.45, 1.75)
    _ax.set_ylim(-1.35, 1.45)
    _ax.set_aspect("equal")
    _ax.axis("off")
    _c = np.linspace(0, 2 * np.pi, 400)
    _ax.plot(np.cos(_c), np.sin(_c), color="black")
    _curve(_ax, (np.cos(_c), np.sin(_c), 0 * _c), GREY, lw=1.0)
    _s = np.tan(np.linspace(-1.5, 1.5, 400))
    _curve(_ax, _inv(_u + _s, _v + 0 * _s), BLUE)
    _curve(_ax, _inv(_u + 0 * _s, _v + _s), RED)
    _P = _pr(*_p)
    _front = _P[2] >= 0
    for _d, _col, _lab in ((_du, BLUE, r"$\partial_u|_p$"), (_dv, RED, r"$\partial_v|_p$")):
        _E = _pr(*(_p + 0.8 * _d))
        arrow(_ax, _P[:2], _E[:2], _col, alpha=1.0 if _front else 0.45)
        _dx, _dy = _E[0] - _P[0], _E[1] - _P[1]
        _n = max(math.hypot(_dx, _dy), 1e-6)
        _ax.text(_E[0] + 0.22 * _dx / _n, _E[1] + 0.16 * _dy / _n, _lab, color=_col, fontsize=13, ha="center", va="center")
    _ax.plot(*_P[:2], "o", color="black", ms=5, mfc="black" if _front else "white")
    _N = _pr(0, 0, 1)
    _ax.plot(*_N[:2], "o", color="black", ms=3)
    _ax.text(_N[0] - 0.04, _N[1] + 0.12, "$n$", fontsize=13)
    if not _front:
        _ax.text(0, -1.3, "$p$ on the far side", fontsize=10, ha="center", color=GREY)

    _ax2.set_title(r"$\varphi_n$ : $(u, v)$", fontsize=13)
    _ax2.set_xlim(-3.0, 3.0)
    _ax2.set_ylim(-3.0, 3.0)
    _ax2.set_aspect("equal")
    _ax2.axhline(0, color="black", lw=0.6)
    _ax2.axvline(0, color="black", lw=0.6)
    _ax2.plot(np.cos(_c), np.sin(_c), color=GREY, lw=1.0)
    _ax2.plot([-3.0, 3.0], [_v, _v], color=BLUE)
    _ax2.plot([_u, _u], [-3.0, 3.0], color=RED)
    _ax2.text(0, 1.04, "equator", color=GREY, fontsize=9, ha="center", va="bottom")
    arrow(_ax2, (_u, _v), (_u + 0.8, _v), BLUE)
    arrow(_ax2, (_u, _v), (_u, _v + 0.8), RED)
    _ax2.plot(_u, _v, "o", color="black", ms=5)
    _ax2.set_xticks([-2, 0, 2])
    _ax2.set_yticks([-2, 0, 2])

    _table = table(
        [
            (r"$p = \varphi_n^{-1}(u, v)$", rf"$({_p[0] + 0.0:.3f},\ {_p[1] + 0.0:.3f},\ {_p[2] + 0.0:.3f})$"),
            (r"$\textcolor{#1b458f}{\partial_u\vert_p} (h) = 4u / (1 + u^2 + v^2)^2$", rf"${_hu:.3f}$"),
            (r"$\textcolor{#b3261e}{\partial_v\vert_p} (h) = 4v / (1 + u^2 + v^2)^2$", rf"${_hv:.3f}$"),
        ]
    )
    mo.vstack([mo.hstack([s_u, s_v], justify="start", gap=3, wrap=True), _table, _fig])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - A tangent vector $v_p = [\gamma]$ differentiates functions: $Df_p(v_p) = \dfrac{d}{dt}\Big|_{t=0} f \circ \gamma(t)$.
    - A derivation at $p$ is a linear functional on $C^\infty(M, \mathbb{R})$ satisfying the Leibniz rule; $\mathrm{Der}_p(M) \approx T_pM$.
    - Through this bijection $T_pM$ becomes a vector space.
    - A chart $\varphi$ with coordinates $x^i$ gives the coordinate basis $\partial_i|_p$, acting on functions as the partial derivatives of $f \circ \varphi^{-1}$ at $\varphi(p)$.

    **Next:** vector fields and differential equations on manifolds.
    """)
    return


if __name__ == "__main__":
    app.run()
