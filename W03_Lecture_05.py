import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 05 · Lorentz factor, photons, relativistic dynamics", css_file="phy309.css")


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
    header("Lecture 05", "Week 03", "Lecture 05 · Lorentz factor, photons, relativistic dynamics")
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, HALF, ORANGE, RED, arrow, blank, np):
    # v = Gamma (u + nu): the particle sigma and the photon xi decomposed along u and S_p^u
    fig_decomp, _ax = blank(HALF, 3.2, (-1.4, 2.0), (-1.0, 1.9))
    _b = 0.5
    _G = 1 / np.sqrt(1 - _b**2)
    _ax.plot([-1.6, 1.8], [-1.6, 1.8], color=GREY, lw=0.8)
    _ax.plot([-1.6, 1.4], [1.6, -1.4], color=GREY, lw=0.8)
    _ax.plot([-1.3, 1.9], [0, 0], color=GREY, lw=1.0)
    _ax.text(1.9, -0.08, r"$S_p^u$", color=GREY, fontsize=12, ha="right", va="top")
    _s = np.linspace(-0.9, 1.7, 80)
    _ax.plot(0.1 * np.sin(2 * _s), _s, color=BLUE)
    _ax.plot(_b * _s + 0.1 * _s**2, _s, color=RED)
    _ax.text(-0.3, 1.6, r"$\gamma$", color=BLUE, fontsize=12)
    _ax.text(1.25, 1.5, r"$\sigma$", color=RED, fontsize=12)
    _ax.text(1.75, 1.55, r"$\xi$", color=ORANGE, fontsize=12)
    arrow(_ax, (0, 0), (0, 1), BLUE)
    _ax.text(-0.08, 0.55, "$u$", color=BLUE, fontsize=13, ha="right")
    arrow(_ax, (0, 0), (_G * _b, _G), RED)
    _ax.text(_G * _b / 2 + 0.08, _G / 2, "$v$", color=RED, fontsize=13)
    arrow(_ax, (0, 1), (_b, 1), GREEN)
    _ax.text(_b / 2, 1.06, r"$\nu(\gamma, \sigma)$", color=GREEN, fontsize=10, ha="center", va="bottom")
    arrow(_ax, (0, 0), (1.5, 1.5), ORANGE)
    _ax.plot([-0.9, 1.75], [-0.9, 1.75], color=ORANGE)
    _ax.text(1.3, 1.05, "$w$", color=ORANGE, fontsize=13)
    arrow(_ax, (0, 1), (1, 1), GREEN)
    _ax.text(0.8, 0.94, r"$\nu(\gamma, \xi)$", color=GREEN, fontsize=10, ha="center", va="top")
    _ax.plot(0, 0, "o", color="black", ms=4)
    _ax.text(0.1, -0.25, "$p$", fontsize=12)
    _ = None  # no cell output: the figures are returned, not displayed here
    return (fig_decomp,)


@app.cell(hide_code=True)
def _(corollary, definition, fig_decomp, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    - particles in Minkowski spacetime: $\gamma : \mathbb{R} \longrightarrow \mathbb{M}^4$ with $\gamma'(t)$ timelike and future oriented, parameterized by proper time, $\lVert \gamma'(t) \rVert^2 = -1$
    - inertial particles maximize proper time (reversed triangle inequality); relative velocity $\nu(u, v) = v / (-\eta(u, v)) - u \in u^\perp$ with $\lVert \nu \rVert^2 < 1$, and $= 1$ for photons

    **Today:** the Lorentz factor, photons as limits of particles, and relativistic dynamics

    ## I.5 &nbsp; Lorentz factor, photons, relativistic dynamics

    ### Lorentz factor
    """
            ),
            definition(
                r"""
    Given a particle $\gamma : \mathbb{R} \longrightarrow \mathbb{M}^4$ we call

    - $u(t) = \gamma'(t)$ &nbsp; the **4-velocity** of $\gamma$ at $\gamma(t)$ &nbsp; (assumed $\lVert u(t) \rVert^2 = -1$)
    - $S_{\gamma(t)}^{u(t)} = \gamma(t) + u(t)^\perp$ &nbsp; the **space of simultaneity** of $\gamma$ at $\gamma(t)$
    """,
                "4-velocity",
            ),
            theorem(
                r"""
    Given two particles $\gamma, \sigma$, with $\gamma(t) = \sigma(s) = p$, &nbsp; $\gamma'(t) = u(t)$, $\sigma'(s) = v(s)$

    the 4-velocity of $\sigma$ at $p$ decomposes uniquely as

    $$
    \begin{aligned}
    v &= \underbrace{-\eta(u, v)\, u}_{\text{parallel to } u} + \underbrace{\big( v + \eta(u, v)\, u \big)}_{\text{orthogonal to } u} \\[4pt]
    &= \underbrace{\Gamma(\gamma, \sigma)}_{\text{Lorentz factor of } \sigma \text{ relative } \gamma} \big( u + \underbrace{\nu(\gamma, \sigma)}_{\text{velocity of } \sigma \text{ relative } \gamma} \big) \qquad (\text{at } p)
    \end{aligned}
    $$

    $$
    \leadsto \quad \begin{cases} \Gamma(\gamma, \sigma) = -\eta(u, v) > 0 \\[4pt] \nu(\gamma, \sigma) = \dfrac{v}{\Gamma(\gamma, \sigma)} - u \in u^\perp \end{cases} \qquad (\text{at } p)
    $$
    """,
                "Lorentz factor and relative velocity",
            ),
            fig_decomp,
            mo.md(
                r"""
    **Example.** Suppose $\gamma(t) = p + tu$, $\sigma(s) = p + sv$ are inertial particles (straight lines)

    Choose $o = p \in \mathbb{M}^4$ origin event and $e_0 = u \in \mathbb{V}$, $e_i \in u^\perp \subset \mathbb{V}$ inertial frame

    $$
    \Longrightarrow \quad \gamma(t) = \begin{bmatrix} t \\ 0 \\ 0 \\ 0 \end{bmatrix}, \qquad \sigma(s) = \begin{bmatrix} s v^0 \\ s v^1 \\ s v^2 \\ s v^3 \end{bmatrix}
    $$

    $$
    \Gamma(\gamma, \sigma) = -\eta(u, v) = -(-1) v^0 = v^0 > 0
    $$

    $$
    \nu(\gamma, \sigma) = \frac{1}{v^0} \begin{bmatrix} v^0 \\ v^1 \\ v^2 \\ v^3 \end{bmatrix} - \begin{bmatrix} 1 \\ 0 \\ 0 \\ 0 \end{bmatrix} = \frac{1}{v^0} \begin{bmatrix} 0 \\ v^1 \\ v^2 \\ v^3 \end{bmatrix} \in u^\perp
    \qquad \left( \frac{\text{displacement along } u^\perp}{\text{displacement along } u} \right)
    $$
    """
            ),
            theorem(
                r"""
    For any two particles $\gamma, \sigma$

    $$
    \begin{aligned}
    \lVert \nu(\gamma, \sigma) \rVert^2 &= \frac{\lVert v \rVert^2}{\Gamma(\gamma, \sigma)^2} + 2 \underbrace{\frac{\Gamma(\gamma, \sigma)}{\Gamma(\gamma, \sigma)}}_{=\, 1} + \underbrace{\lVert u \rVert^2}_{=\, -1} \\[4pt]
    &= 1 + \frac{\lVert v \rVert^2}{\Gamma(\gamma, \sigma)^2} < 1
    \end{aligned}
    $$
    """,
                "Bounded relative speed",
            ),
            mo.md(r"Speed of $\sigma$ relative to $\gamma$ is *bounded above* (universal maximum relative speed limit)"),
            corollary(
                r"""
    For any two particles $\gamma, \sigma$

    $$
    \Gamma(\gamma, \sigma) = \frac{1}{\sqrt{1 - \lVert \nu(\gamma, \sigma) \rVert^2}} \geq 1 \qquad (\text{at } p = \gamma(t) = \sigma(s))
    $$
    """,
                "Lorentz factor from the relative speed",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    speed = mo.ui.slider(0, 0.99, 0.01, value=0.6, label=r"$\lVert \nu(\gamma, \sigma) \rVert$", show_value=True)
    mass = mo.ui.slider(0.5, 5, 0.5, value=1, label="$m$", show_value=True)
    return mass, speed


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, RED, mass, math, mo, np, speed):
    _b, _m = speed.value, mass.value
    _G = 1 / math.sqrt(1 - _b**2)
    _x = np.linspace(0, 0.99, 300)
    _fig = Figure(figsize=(FULL, 3.2), layout="constrained")
    _ax = _fig.subplots()
    _ax.plot(_x, 1 / np.sqrt(1 - _x**2), color=BLUE, label=r"$\Gamma$")
    _ax.plot(_x, 1 + 0.5 * _x**2, "--", color=RED, label=r"$1 + \frac{1}{2} \|\nu\|^2$")
    _ax.plot(_b, _G, "o", color=BLUE, ms=6)
    _ax.set_xlim(0, 1)
    _ax.set_ylim(0.9, max(4, 1.15 * _G))
    _ax.set_xlabel(r"$\|\nu\|$")
    _ax.legend(frameon=False, fontsize=11)
    for _s in ("top", "right"):
        _ax.spines[_s].set_visible(False)

    _table = "\n".join(
        [
            "| | | |",
            "|:--|--:|--:|",
            "| | relativistic | Newtonian limit |",
            rf"| $\Gamma = 1 / \sqrt{{1 - \lVert \nu \rVert^2}}$ | ${_G:.4f}$ | $1 + \tfrac{{1}}{{2}} \lVert \nu \rVert^2 = {1 + 0.5 * _b**2:.4f}$ |",
            rf"| $\varepsilon = m \Gamma$ | ${_m * _G:.4f}$ | $m + \tfrac{{1}}{{2}} m \lVert \nu \rVert^2 = {_m * (1 + 0.5 * _b**2):.4f}$ |",
            rf"| $\lVert \pi \rVert = m \Gamma \lVert \nu \rVert$ | ${_m * _G * _b:.4f}$ | $m \lVert \nu \rVert = {_m * _b:.4f}$ |",
        ]
    )
    lorentz_panel = mo.vstack([mo.hstack([speed, mass], justify="start", gap=3, wrap=True), mo.md(_table), _fig])
    return (lorentz_panel,)


@app.cell(hide_code=True)
def _(corollary, definition, lorentz_panel, mo, theorem):
    mo.vstack(
        [
            mo.md(r"### Photons"),
            definition(
                r"""
    A **photon** in $\mathbb{M}^4$ is a future oriented lightlike line &nbsp; $\xi(s) = p + sw$ &nbsp; ($\lVert w \rVert^2 = 0$, in the future cone)
    """,
                "Photon",
            ),
            theorem(
                r"""
    Given a particle $\gamma$ and a photon $\xi$ &nbsp; $\big( p = \gamma(t) = \xi(s)$, $\gamma'(t) = u(t)$, $\xi'(s) = w(s) \big)$

    $$
    \begin{aligned}
    w &= \underbrace{-\eta(u, w)\, u}_{\text{parallel}} + \underbrace{\big( w + \eta(u, w)\, u \big)}_{\text{orthogonal}} \\
    &= -\eta(u, w) \big( u + \nu(\gamma, \xi) \big)
    \end{aligned}
    $$
    """,
                "Decomposition of a photon",
            ),
            corollary(
                r"""
    $$
    \lVert \nu(\gamma, \xi) \rVert^2 = \underbrace{\frac{\lVert w \rVert^2}{\eta(u, w)^2}}_{=\, 0} + 2 \underbrace{\frac{\eta(u, w)}{\eta(u, w)}}_{=\, 1} + \underbrace{\lVert u \rVert^2}_{=\, -1} = 1
    $$
    """,
                "Photons move at the maximal speed",
            ),
            mo.md(
                r"""
    - photons achieve the maximum speed relative to any particle!
    - Maxwell's electromagnetic waves evolve along *photons* in Minkowski spacetime (particles of light, with $c = 1$)

    ### 4-momentum, energy and spatial momentum
    """
            ),
            definition(
                r"""
    If a particle $\sigma(s)$ has mass $m > 0$ its **4-momentum** at $\sigma(s)$ is

    $$
    P(s) = m\, \sigma'(s) = m\, v(s)
    $$
    """,
                "4-momentum",
            ),
            mo.md(
                r"""
    Given another particle $\gamma(t)$, the 4-momentum of $\sigma$ at an event $\sigma(s) = \gamma(t)$

    $$
    \begin{aligned}
    P &= \underbrace{m\, \Gamma(\gamma, \sigma)}_{\text{energy of } \sigma \text{ relative to } \gamma}\, u + \underbrace{m\, \Gamma(\gamma, \sigma)\, \nu(\gamma, \sigma)}_{\text{spatial momentum of } \sigma \text{ relative to } \gamma} \\[4pt]
    &= \varepsilon(\gamma, \sigma)\, u + \underbrace{\pi(\gamma, \sigma)}_{\in\, u^\perp}
    \qquad \Longrightarrow \quad \begin{cases} \varepsilon = -\eta(P, u) \\ \pi = P - \varepsilon u \end{cases}
    \end{aligned}
    $$
    """
            ),
            corollary(
                r"""
    $$
    \lVert P \rVert^2 = m^2 \lVert v \rVert^2 = \varepsilon(\gamma, \sigma)^2 \lVert u \rVert^2 + \lVert \pi(\gamma, \sigma) \rVert^2
    \qquad \Longrightarrow \quad \varepsilon(\gamma, \sigma)^2 = m^2 + \lVert \pi(\gamma, \sigma) \rVert^2
    $$

    $$
    \left( \begin{array}{c} \text{energy of } \sigma \\ \text{measured by } \gamma \end{array} \right)^{\!2} = \big( \text{mass of } \sigma \big)^2 + \left( \begin{array}{c} \text{spatial momentum} \\ \text{of } \sigma \text{ measured by } \gamma \end{array} \right)^{\!2}
    $$
    """,
                "Energy–momentum relation",
            ),
            mo.md(
                r"""
    **Example.** For small relative speeds $\lVert \nu(\gamma, \sigma) \rVert^2 \ll 1$

    $$
    \varepsilon = \sqrt{m^2 + \lVert \pi \rVert^2} = m \sqrt{1 + \frac{\lVert \nu \rVert^2}{1 - \lVert \nu \rVert^2}} \approx \underbrace{m + \frac{1}{2} m \lVert \nu \rVert^2}_{\text{Newtonian limit}} + O(\lVert \nu \rVert^4)
    $$

    $$
    \pi = m \Gamma \nu = m\, \frac{\nu}{\sqrt{1 - \lVert \nu \rVert^2}} \approx \underbrace{m \nu}_{\text{Newtonian limit}} + O(\lVert \nu \rVert^3)
    $$

    For $\nu(\gamma, \sigma) = 0$ &nbsp; $\Longrightarrow$ &nbsp; $\varepsilon = m c^2$ (with $c = 1$)!
    """
            ),
            lorentz_panel,
            mo.md(r"### 4-acceleration and 4-force"),
            definition(
                r"""
    The **4-acceleration** of a particle $\sigma : \mathbb{R} \longrightarrow \mathbb{M}^4$ &nbsp; ($\lVert \sigma'(s) \rVert^2 = -1$) at $p = \sigma(s)$ is

    $$
    A(s) = \frac{d}{ds} v(s) = \sigma''(s)
    $$

    The **4-force** acting on $\sigma$ at $p = \sigma(s)$ is

    $$
    F(s) = \frac{d}{ds} P(s) = m A(s)
    $$
    """,
                "4-acceleration and 4-force",
            ),
            mo.md(
                r"""
    A relativistic model in $\mathbb{M}^4$ is the prescription of a 4-force $F(s) = \mathcal{F}(\sigma(s), \sigma'(s))$ along a particle $\sigma : \mathbb{R} \longrightarrow \mathbb{M}^4$ for some rule

    $$
    \mathcal{F} : \mathbb{M}^4 \times \mathbb{V} \longrightarrow \mathbb{V}
    $$

    e.g. Maxwell: $\mathcal{F}(p, v) = q\, \mathbf{F}(p)\, v$ with $\mathbf{F}(p) : \mathbb{V} \longrightarrow \mathbb{V}$ anti-symmetric &nbsp; ($\eta(\mathbf{F} x, y) = -\eta(x, \mathbf{F} y)$) &nbsp; + Maxwell's equations

    $$
    \begin{aligned}
    \Longrightarrow \quad \sigma''(s) &= \frac{q}{m}\, \mathbf{F}(\sigma(s))\, \sigma'(s) \\
    &= \frac{q}{m}\, \Gamma(\gamma, \sigma) \Big( \eta\big( E(\gamma), \nu(\gamma, \sigma) \big)\, u + E(\gamma) + \nu(\gamma, \sigma) \times B(\gamma) \Big)
    \end{aligned}
    $$

    with respect to any other particle $\gamma$

    ## Summary

    - the 4-velocity of $\sigma$ decomposes along any observer $\gamma$ as $v = \Gamma (u + \nu)$ with Lorentz factor $\Gamma = -\eta(u, v) = 1 / \sqrt{1 - \lVert \nu \rVert^2}$
    - photons decompose the same way with $\lVert \nu \rVert = 1$: the maximal speed, for every observer
    - 4-momentum $P = m v = \varepsilon u + \pi$ gives energy $\varepsilon = m\Gamma$ and spatial momentum $\pi = m\Gamma\nu$ measured by $\gamma$, with $\varepsilon^2 = m^2 + \lVert \pi \rVert^2$ and the Newtonian limit $\varepsilon \approx m + \tfrac{1}{2} m \lVert \nu \rVert^2$
    - dynamics: $m \sigma'' = F(\sigma, \sigma')$, a second order ODE in $\mathbb{M}^4$; Maxwell gives $F = q\, \mathbf{F}(\sigma)\, \sigma'$

    **Next:** gravity, and why it cannot be one more force rule on an affine spacetime
    """
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
