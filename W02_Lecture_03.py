import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 03 · Minkowski geometry", css_file="phy309.css")


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
            arrowprops={"arrowstyle": "-|>", "color": color, "lw": lw, "mutation_scale": 11, "shrinkA": 0, "shrinkB": 0, **kw},
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

    def table(rows):
        """Fixed-label readout table: rows are (label, value) pairs of markdown strings."""
        return mo.md("\n".join(["| | |", "|:--|--:|"] + [f"| {k} | {v} |" for k, v in rows]))

    return BLUE, FULL, GREEN, GREY, HALF, LIGHT, ORANGE, RED, arrow, blank, corollary, definition, header, note, plane, postulate, proposition, table, theorem


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
    header("Lecture 03", "Week 02", "Lecture 03 · Minkowski geometry")
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    - Galilean spacetime $\mathbb{G}^4 = (\mathbb{A}^4, \mathbb{V}^4, -)$ with universal time $\tau$ and spatial inner product on $\ker \tau$; particles parameterized by absolute time, $\tau(\gamma') = 1$
    - Newton's law $\gamma'' = \vec{F} / m$ with $\vec{F} \in \ker \tau$: inertial motion, uniform acceleration ($\vec{F} = m\vec{g}$) and central motion (conics) all fit
    - Maxwell's equations do not: they single out a speed $c$, but relative velocities add, $\vec{v}(\gamma, \xi) = \vec{v}(\gamma, \sigma) + \vec{v}(\sigma, \xi)$, so a light particle $\xi$ moving with speed $c$ relative to $\gamma$ and to $\sigma$ forces $c = \lVert \vec{v}(\gamma, \sigma) \rVert + c$

    **Today:** a new geometry for spacetime in which the speed of light is the same for every inertial observer

    ## I.3 &nbsp; Minkowski geometry

    Geometry of special relativity
    """
            ),
            definition(
                r"""
    The **Minkowski spacetime** is a 4-dimensional affine space

    $$
    \mathbb{M}^4 = (\mathbb{A}^4, \mathbb{V}^4, -)
    $$

    together with a *Minkowski inner product*

    $$
    \eta : \mathbb{V}^4 \times \mathbb{V}^4 \longrightarrow \mathbb{R} \qquad \text{symmetric, bilinear, signature } (3, 1)
    $$

    (signature $(3, 1)$: replacement for positive definiteness of the Euclidean inner product)
    """,
                "Minkowski spacetime",
            ),
            definition(
                r"""
    A symmetric bilinear function $\eta : \mathbb{V}^4 \times \mathbb{V}^4 \longrightarrow \mathbb{R}$ has **signature $(3, 1)$** if

    - there exists $\vec{u} \in \mathbb{V}^4$ with $\eta(\vec{u}, \vec{u}) < 0$
    - the restriction of $\eta$ to $\vec{u}^\perp = \{\, \vec{v} \in \mathbb{V}^4 \mid \eta(\vec{u}, \vec{v}) = 0 \,\}$ is positive definite
    """,
                "Signature",
            ),
            mo.md(
                r"""
    In $\mathbb{G}^4$, $\ker(\tau)$ had an Euclidean inner product &nbsp; $\Longrightarrow$ &nbsp; we had copies of $\mathbb{E}^3$ through each $p \in \mathbb{G}^4$: &nbsp; $S_p = p + \ker(\tau) \approx \mathbb{E}^3$

    Now, in $\mathbb{M}^4$, $\vec{u}^\perp$ has an Euclidean inner product for each $\vec{u} \in \mathbb{V}^4$ with $\eta(\vec{u}, \vec{u}) = \lVert \vec{u} \rVert^2 < 0$ &nbsp; $\Longrightarrow$ &nbsp; we get copies of $\mathbb{E}^3$ through each $p \in \mathbb{M}^4$, for each such vector $\vec{u} \in \mathbb{V}^4$, $\lVert \vec{u} \rVert^2 < 0$

    $$
    S_p^{\vec{u}} = p + \vec{u}^\perp \approx \mathbb{E}^3
    $$
    """
            ),
            definition(
                r"""
    Non-zero 4-vectors $\vec{u} \in \mathbb{V}^4$ are called

    - **timelike** if $\lVert \vec{u} \rVert^2 < 0$
    - **spacelike** if $\lVert \vec{u} \rVert^2 > 0$
    - **lightlike** if $\lVert \vec{u} \rVert^2 = 0$
    """,
                "Timelike, spacelike, lightlike",
            ),
            mo.md(
                r"""
    ### Inertial frames and the light cone

    Choose $o \in \mathbb{M}^4$, $\vec{e}_0 \in \mathbb{V}^4$ with $\lVert \vec{e}_0 \rVert^2 = -1$, &nbsp; $\vec{e}_1, \vec{e}_2, \vec{e}_3 \in \vec{e}_0^\perp$ with $\eta(\vec{e}_i, \vec{e}_j) = \delta_{ij}$ &nbsp; (inertial frame)

    $$
    \Longrightarrow \quad p = o + p^0 \vec{e}_0 + p^i \vec{e}_i = o + p^\mu \vec{e}_\mu \in \mathbb{M}^4 \qquad \text{Cartesian coordinates}
    $$

    (sum over $i = 1, 2, 3$; &nbsp; sum over $\mu = 0, 1, 2, 3$)

    $$
    \Longrightarrow \quad \vec{u} = u^0 \vec{e}_0 + u^i \vec{e}_i = u^\mu \vec{e}_\mu \in \mathbb{V}^4
    $$

    $$
    \lVert \vec{u} \rVert^2 = \underbrace{-(u^0)^2}_{\text{negative sign (signature } (0, 1))} + \underbrace{(u^1)^2 + (u^2)^2 + (u^3)^2}_{\text{same as Euclidean (signature } (3, 0))}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    c_u0 = mo.ui.slider(-2, 2, 0.1, value=1.6, label="$u^0$", show_value=True)
    c_u1 = mo.ui.slider(-2, 2, 0.1, value=0.6, label="$u^1$", show_value=True)
    return c_u0, c_u1


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, LIGHT, RED, arrow, blank, c_u0, c_u1, mo):
    _u0, _u1 = c_u0.value, c_u1.value
    _n = -(_u0**2) + _u1**2
    if abs(_n) < 1e-9:
        _kind, _col = ("lightlike", GREY) if (_u0, _u1) != (0, 0) else ("zero vector", "black")
    elif _n < 0:
        _kind, _col = "timelike", BLUE
    else:
        _kind, _col = "spacelike", RED

    _fig, _ax = blank(4.6, 4.4, (-2.4, 2.6), (-2.4, 2.6))
    _ax.fill([0, -2.3, 2.3], [0, 2.3, 2.3], color=LIGHT, alpha=0.5, lw=0)
    _ax.fill([0, -2.3, 2.3], [0, -2.3, -2.3], color=LIGHT, alpha=0.5, lw=0)
    arrow(_ax, (-2.4, 0), (2.5, 0), "black", lw=0.9)
    arrow(_ax, (0, -2.4), (0, 2.5), "black", lw=0.9)
    _ax.text(2.35, -0.3, "$u^1$", fontsize=13)
    _ax.text(0.1, 2.35, "$u^0$", fontsize=13)
    _ax.plot([-2.3, 2.3], [-2.3, 2.3], color=GREY)
    _ax.plot([-2.3, 2.3], [2.3, -2.3], color=GREY)
    if _n < 0:
        # u-perp: vectors v with -u0 v0 + u1 v1 = 0
        _k = 2.3 / max(abs(_u0), abs(_u1))
        _ax.plot([-_k * _u0, _k * _u0], [-_k * _u1, _k * _u1], "--", color=GREEN)
        _ax.annotate(r"$\vec{u}^\perp$", (_k * _u0 * (1 if _u0 > 0 else -1), _k * _u1 * (1 if _u0 > 0 else -1)), textcoords="offset points", xytext=(-22, 8), color=GREEN, fontsize=14)
    if (_u0, _u1) != (0, 0):
        arrow(_ax, (0, 0), (_u1, _u0), _col, r"$\vec{u}$", at_tip=True)
    _ax.text(-1.2, 1.9, "timelike", color=BLUE, fontsize=11, ha="center")
    _ax.text(-1.2, -2.05, "timelike", color=BLUE, fontsize=11, ha="center")
    _ax.text(-2.1, 0.5, "spacelike", color=RED, fontsize=11, ha="center")
    _ax.text(2.1, 0.5, "spacelike", color=RED, fontsize=11, ha="center")
    _ax.text(1.75, -2.0, "lightlike", color=GREY, fontsize=11, rotation=-45, ha="center", va="center")

    _table = "\n".join(
        [
            "| | |",
            "|:--|--:|",
            rf"| $\lVert \vec{{u}} \rVert^2 = -(u^0)^2 + (u^1)^2$ | ${_n:.2f}$ |",
            rf"| type | {_kind} |",
        ]
    )
    mo.vstack([mo.hstack([c_u0, c_u1], justify="start", gap=3, wrap=True), mo.md(_table), _fig])
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, LIGHT, RED, arrow, blank, np):
    # Static sketches from the handwritten notes (time runs upwards, one spatial direction drawn)

    # Particle: tangent vectors inside the future light cone at each event
    fig_cones, _ax = blank(2.8, 3.2, (-1.5, 1.7), (-0.6, 3.2))
    _s = np.linspace(-0.5, 3.0, 120)
    _x = 0.35 * np.sin(1.4 * _s)
    _ax.plot(_x, _s, color=BLUE)
    _ax.text(0.5, 3.0, r"$\gamma$", color=BLUE, fontsize=13)
    for _s0, _name in ((0.5, "$s_1$"), (2.0, "$s_2$")):
        _x0 = 0.35 * np.sin(1.4 * _s0)
        _dx = 0.35 * 1.4 * np.cos(1.4 * _s0)
        for _sign in (1, -1):
            _ax.fill([_x0, _x0 - 0.5, _x0 + 0.5], [_s0, _s0 + 0.5 * _sign, _s0 + 0.5 * _sign], color=LIGHT, alpha=0.5, lw=0)
            _ax.plot([_x0 - 0.5, _x0 + 0.5], [_s0 + 0.5 * _sign, _s0 - 0.5 * _sign], color=GREY, lw=1.0)
        _n = (1 + _dx**2) ** 0.5
        arrow(_ax, (_x0, _s0), (_x0 + 0.8 * _dx / _n, _s0 + 0.8 / _n), GREEN)
        _ax.plot(_x0, _s0, "o", color="black", ms=4)
        _ax.text(_x0 + 0.55, _s0 - 0.1, rf"$\gamma({_name[1:-1]})$", fontsize=12)
        _ax.text(_x0 + 0.8 * _dx / _n - 0.1, _s0 + 0.8 / _n + 0.05, rf"$\gamma'({_name[1:-1]})$", color=GREEN, fontsize=12, ha="right")

    # Relative velocity: rescale sigma' to the simultaneity line of gamma, then subtract gamma'
    fig_relvel, _ax = blank(3.4, 3.0, (-1.6, 2.4), (-1.2, 2.2))
    _s = np.linspace(-1.1, 1.9, 120)
    _ax.plot(-0.25 * _s - 0.12 * _s**2, _s, color=BLUE)
    _ax.plot(0.55 * _s + 0.1 * _s**2, _s, color=RED)
    _ax.text(-0.95, 1.75, r"$\gamma$", color=BLUE, fontsize=13)
    _ax.text(1.35, 1.7, r"$\sigma$", color=RED, fontsize=13)
    _g = (-0.25, (1 + 0.25**2) ** 0.5)  # unit timelike: -(t)^2 + x^2 = -1
    _sg = (0.55, (1 + 0.55**2) ** 0.5)
    # (gamma')^perp: -g_t v_t + g_x v_x = 0, i.e. v_t = (g_x / g_t) v_x
    _ax.plot([-1.5, 2.3], [-1.5 * _g[0] / _g[1], 2.3 * _g[0] / _g[1]], color=GREY, lw=1.0)
    _ax.text(2.05, -0.75, r"$(\gamma')^\perp$", color=GREY, fontsize=12, ha="center")
    arrow(_ax, (0, 0), _g, BLUE)
    _ax.text(_g[0] - 0.1, _g[1] + 0.05, r"$\gamma'$", color=BLUE, fontsize=13, ha="right")
    arrow(_ax, (0, 0), _sg, RED)
    _ax.text(_sg[0] + 0.1, _sg[1] + 0.05, r"$\sigma'$", color=RED, fontsize=13)
    # scaled sigma' / (-eta(gamma', sigma')) lands on the line through gamma' parallel to (gamma')^perp
    _eta = -_g[1] * _sg[1] + _g[0] * _sg[0]
    _sc = (_sg[0] / -_eta, _sg[1] / -_eta)
    _ax.plot([0, _sc[0]], [0, _sc[1]], "--", color=RED, lw=1.0)
    arrow(_ax, _g, _sc, GREEN)
    _ax.text((_g[0] + _sc[0]) / 2, (_g[1] + _sc[1]) / 2 + 0.12, r"$\vec{v}(\gamma, \sigma)$", color=GREEN, fontsize=12, ha="center", va="bottom")
    _ax.plot(0, 0, "o", color="black", ms=4)
    _ = None  # no cell output: the figures are returned, not displayed here

    return fig_cones, fig_relvel

@app.cell(hide_code=True)
def _(definition, fig_cones, fig_relvel, mo, proposition, theorem):
    mo.vstack(
        [
            mo.md(r"### Causal structure and proper time"),
            definition(
                r"""
    - $q$ is in the **future** (past) of $p$ if $q - p$ is timelike in “upper” (“lower”) cone
    - $p, q$ are **spacelike separated** if $q - p$ is spacelike
    """,
                r"Causal structure in $\mathbb{M}^4$",
            ),
            mo.md(r"Not a notion of *simultaneity* (will depend on additional choices)"),
            definition(
                r"""
    Given $p, q \in \mathbb{M}^4$

    - if $q$ is in the future (past) of $p$

        $$
        \mathrm{time}(p, q) = \pm \sqrt{-\lVert q - p \rVert^2} \qquad (\text{proper time from } p \text{ to } q)
        $$

    - if $p, q$ are spacelike separated

        $$
        \mathrm{dist}(p, q) = \sqrt{\lVert q - p \rVert^2} \qquad (\text{proper distance from } p \text{ to } q)
        $$
    """,
                "Proper time and proper distance",
            ),
            definition(
                r"""
    A **particle** in $\mathbb{M}^4$ is a parameterized curve $\gamma : \mathbb{R} \longrightarrow \mathbb{M}^4$ such that $\gamma'(s)$ is timelike and *future oriented* (always pointing to the upper side of the cone)
    """,
                "Particle",
            ),
            fig_cones,
            mo.md(
                r"""
    An inertial particle is a straight future oriented timelike line &nbsp; $\gamma(s) = p + s\vec{u}$, &nbsp; ($\vec{u}$ timelike, $\vec{u}$ future oriented)

    $\Longrightarrow$ &nbsp; simultaneity of events depends on the choice of an *inertial particle* (inertial observer)
    """
            ),
            definition(
                r"""
    Given $p \in \mathbb{M}^4$, and $\vec{u} \in \mathbb{V}^4$ timelike

    $$
    S_p^{\vec{u}} = \{\, q \in \mathbb{M}^4 \mid q - p \in \vec{u}^\perp \,\}
    $$

    is the set of events simultaneous to $p$ relative to the inertial observer $\gamma(s) = p + s\vec{u}$
    """,
                "Relative simultaneity",
            ),
            mo.md(
                r"""
    It will be this relative notion of simultaneity which will allow us to formulate Maxwell's theory consistently with spacetime geometry!
    """
            ),
            proposition(
                r"""
    Every particle $\gamma : \mathbb{R} \longrightarrow \mathbb{M}^4$ can be parameterized by a *“proper time” parameter* $t$ such that $\lVert \gamma'(t) \rVert^2 = -1$
    """,
                "Proper time parameterization",
            ),
            mo.md(
                r"""
    In $\mathbb{G}^4$, “absolute time” was defined such that $\tau(\gamma'(t)) = 1$

    $$
    \leadsto \quad \mathrm{time}(\gamma(t_1), \gamma(t_2)) = \int_{t_1}^{t_2} \tau(\gamma'(t))\, dt = (t_2 - t_1) = \tau(\gamma(t_2) - \gamma(t_1))
    $$
    """
            ),
            definition(
                r"""
    The **proper time** along a particle $\gamma : \mathbb{R} \longrightarrow \mathbb{M}^4$ is

    $$
    \mathrm{time}_\gamma(\gamma(t_1), \gamma(t_2)) = \int_{t_1}^{t_2} \sqrt{-\lVert \gamma'(t) \rVert^2}\, dt
    = t_2 - t_1 \leq \sqrt{-\lVert \gamma(t_2) - \gamma(t_1) \rVert^2}
    $$

    (with equality if and only if $\gamma$ is inertial)
    """,
                "Proper time along a particle",
            ),
            mo.md(r"### Relative velocity"),
            definition(
                r"""
    Given two particles $\gamma, \sigma$ (with $\lVert \gamma' \rVert^2 = \lVert \sigma' \rVert^2 = -1$) the **relative velocity** of $\sigma$ with respect to $\gamma$ is the spacelike vector orthogonal to $\gamma'$

    $$
    \vec{v}(\gamma, \sigma) = \frac{\sigma'}{-\eta(\gamma', \sigma')} - \gamma' \in (\gamma')^\perp
    $$
    """,
                "Relative velocity",
            ),
            fig_relvel,
            theorem(
                r"""
    $$
    \begin{aligned}
    \lVert \vec{v}(\gamma, \sigma) \rVert^2 &= \frac{\lVert \sigma' \rVert^2}{\eta(\gamma', \sigma')^2} + \lVert \gamma' \rVert^2 + \frac{2\, \eta(\gamma', \sigma')}{\eta(\gamma', \sigma')} \\[4pt]
    &= 1 - \left( \frac{1}{\eta(\gamma', \sigma')} \right)^{\!2} < 1
    \end{aligned}
    $$
    """,
                "Bounded relative speed",
            ),
            mo.md(
                r"""
    $\Longrightarrow$ &nbsp; relative velocities in Minkowski spacetime are bounded from above

    - maximal speed = speed of light
    - every inertial observer agrees

    ## Summary

    - Minkowski spacetime $\mathbb{M}^4$ = 4-dimensional affine space + symmetric bilinear $\eta$ of signature $(3, 1)$; vectors are timelike, spacelike or lightlike
    - no absolute simultaneity: each timelike $\vec{u}$ has its own Euclidean slice $S_p^{\vec{u}} = p + \vec{u}^\perp$
    - particles are future-oriented timelike curves, parameterized by proper time; relative velocity lives in $(\gamma')^\perp$ and its speed is always below $1$

    **Next:** the reversed Cauchy–Schwarz and triangle inequalities, the twin paradox and relative velocity in coordinates
    """
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
