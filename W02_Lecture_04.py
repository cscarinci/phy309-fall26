import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 04 · Proper time, reversed inequalities, relative velocity", css_file="phy309.css")


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
    header("Lecture 04", "Week 02", "Lecture 04 · Proper time, reversed inequalities, relative velocity")
    return


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, RED, arrow, np):
    # Curved path versus straight chord: longest proper time in M4, shortest length in E3
    fig_compare = Figure(figsize=(FULL, 3.4), layout="constrained")
    _m, _e = fig_compare.subplots(1, 2)
    for _ax in (_m, _e):
        _ax.set_aspect("equal")
        _ax.axis("off")
    _s = np.linspace(0, 2.2, 100)
    _m.plot(0.55 * np.sin(np.pi * _s / 2.2), _s, color=BLUE)
    arrow(_m, (0, 0), (0, 2.2), RED)
    _m.plot([0, 0], [0, 2.2], "o", color="black", ms=4)
    _m.text(-0.1, -0.05, r"$\gamma(t_1) = p$", fontsize=11, ha="right", va="top")
    _m.text(-0.1, 2.25, r"$\gamma(t_2) = q$", fontsize=11, ha="right", va="bottom")
    _m.text(-0.12, 1.1, r"$q - p$", color=RED, fontsize=11, ha="right")
    _m.text(0.62, 1.1, r"$\gamma$", color=BLUE, fontsize=12)
    _m.text(-1.3, 2.55, r"$\mathbb{M}^4$", fontsize=13)
    _m.set_xlim(-1.4, 1.2)
    _m.set_ylim(-0.5, 2.9)
    _x = np.linspace(0, 2.2, 100)
    _e.plot(_x, 0.55 * np.sin(np.pi * _x / 2.2), color=BLUE)
    arrow(_e, (0, 0), (2.2, 0), RED)
    _e.plot([0, 2.2], [0, 0], "o", color="black", ms=4)
    _e.text(0, -0.15, r"$\gamma(t_1) = p$", fontsize=11, ha="center", va="top")
    _e.text(2.2, -0.15, r"$\gamma(t_2) = q$", fontsize=11, ha="center", va="top")
    _e.text(1.1, -0.12, r"$q - p$", color=RED, fontsize=11, ha="center", va="top")
    _e.text(1.1, 0.62, r"$\gamma$", color=BLUE, fontsize=12, ha="center")
    _e.text(-0.3, 1.0, r"$\mathbb{E}^3$", fontsize=13)
    _e.set_xlim(-0.4, 2.6)
    _e.set_ylim(-0.7, 1.3)
    _ = None  # no cell output: the figures are returned, not displayed here
    return (fig_compare,)


@app.cell(hide_code=True)
def _(corollary, definition, fig_compare, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    - Minkowski spacetime $\mathbb{M}^4 = (\mathbb{A}^4, \mathbb{V}^4, -)$ with $\eta$ symmetric, bilinear, of signature $(3, 1)$; non-zero vectors are timelike ($\lVert u \rVert^2 < 0$), spacelike ($> 0$) or lightlike ($= 0$)
    - causal structure: $q$ in the future / past of $p$ if $q - p$ is timelike in the future / past cone; $p, q$ spacelike separated otherwise; no absolute simultaneity
    - proper time $\mathrm{time}(p, q) = \sqrt{-\lVert q - p \rVert^2}$ and proper distance $\mathrm{dist}(p, q) = \sqrt{\lVert q - p \rVert^2}$; particles are future oriented timelike curves

    **In this lecture:** proper time along a particle, the reversed inequalities behind the twin paradox, and relative velocity in coordinates

    ## I.4 &nbsp; Proper time, reversed inequalities, relative velocity

    ### Proper time length

    At every event in the history of a particle its tangent 4-vector is inside the upper light cone &nbsp; $\Longrightarrow$ &nbsp; $\gamma(t_2) - \gamma(t_1)$ is also inside the upper cone $\forall\, t_2 > t_1$
    """
            ),
            theorem(
                r"""
    Every particle in $\mathbb{M}^4$ can be parameterized by a “proper time length parameter” $t$ such that $\lVert \gamma'(t) \rVert^2 = -1$
    """,
                "Proper time parameterization",
            ),
            mo.md(
                r"""
    Recall, in $\mathbb{G}^4$, particles were parameterized by “absolute time” if $\tau(\gamma'(t)) = 1$

    $$
    \Longrightarrow \qquad \mathrm{time}(\gamma(t_1), \gamma(t_2)) = \int_{t_1}^{t_2} \tau(\gamma'(t))\, dt = t_2 - t_1 = \tau(\gamma(t_2) - \gamma(t_1)) \qquad (\text{for any particle})
    $$
    """
            ),
            definition(
                r"""
    The **proper time length** of a particle $\gamma : \mathbb{R} \longrightarrow \mathbb{M}^4$ is

    $$
    \mathrm{time}_\gamma(\gamma(t_1), \gamma(t_2)) = \int_{t_1}^{t_2} \sqrt{-\lVert \gamma'(t) \rVert^2}\, dt
    \underbrace{= t_2 - t_1}_{\text{proper time parameterization}} \leq \sqrt{-\lVert \gamma(t_2) - \gamma(t_1) \rVert^2}
    $$

    (equal only if $\gamma$ is an inertial particle)
    """,
                "Proper time length",
            ),
            mo.md(
                r"""
    $$
    \mathbb{M}^4: \quad \underbrace{\sqrt{-\lVert q - p \rVert^2}}_{\text{proper time from } p \text{ to } q} \geq \underbrace{\mathrm{time}_\gamma(p, q)}_{\text{proper time length of } \gamma}
    \qquad \qquad
    \mathbb{E}^3: \quad \underbrace{\mathrm{length}_\gamma(p, q)}_{\int_{t_1}^{t_2} \sqrt{\lVert \gamma'(t) \rVert^2}\, dt} \geq \underbrace{\sqrt{\lVert q - p \rVert^2}}_{\text{distance from } p \text{ to } q}
    $$

    """
            ),
            fig_compare,
            mo.md(
                r"""
    Like length, proper time length depends on each particle &nbsp; $\Longrightarrow$ &nbsp; each particle has its own proper time length parameterization (its own clock!)

    ### Reversed inequalities
    """
            ),
            theorem(
                r"""
    If $u, v \in \mathbb{V}$ are timelike future oriented

    $$
    \begin{aligned}
    \eta(u, v)^2 &\geq \lVert u \rVert^2 \lVert v \rVert^2 \\[4pt]
    \sqrt{-\lVert u + v \rVert^2} &\geq \sqrt{-\lVert u \rVert^2} + \sqrt{-\lVert v \rVert^2}
    \end{aligned}
    $$

    with “$=$” if and only if $u, v$ are proportional
    """,
                "Reversed Cauchy–Schwarz and triangle inequalities",
            ),
            mo.md(
                r"""
    Recall in $\mathbb{E}^3$: &nbsp; $\langle u, v \rangle^2 \leq \lVert u \rVert^2 \lVert v \rVert^2$, &nbsp; $\lVert u + v \rVert \leq \lVert u \rVert + \lVert v \rVert$

    **Proof.** Given $u, v$ future oriented timelike vectors

    **1.** $\eta(u, v) < 0$

    Choose $e_\mu = e_0, e_i$ inertial frame

    $$
    \Longrightarrow \qquad \begin{cases} u = u^0 e_0 + u^i e_i & \text{with } u^0 > 0 \\ v = v^0 e_0 + v^i e_i & \text{with } v^0 > 0 \end{cases}
    $$

    $$
    \begin{aligned}
    \lVert u \rVert^2 = -(u^0)^2 + \delta_{ij} u^i u^j < 0 \qquad & \Longrightarrow \qquad \sqrt{\delta_{ij} u^i u^j} < u^0 \qquad \left( \sqrt{\delta_{ij} u^i u^j} = \sqrt{(u^1)^2 + (u^2)^2 + (u^3)^2} \right) \\
    \lVert v \rVert^2 = -(v^0)^2 + \delta_{ij} v^i v^j < 0 \qquad & \Longrightarrow \qquad \sqrt{\delta_{ij} v^i v^j} < v^0
    \end{aligned}
    $$

    $$
    \begin{aligned}
    \text{Euclidean Cauchy–Schwarz} \qquad & \Longrightarrow \qquad \delta_{ij} u^i v^j \leq \sqrt{\delta_{k\ell} u^k u^\ell}\, \sqrt{\delta_{mn} v^m v^n} < u^0 v^0 \\[4pt]
    & \Longrightarrow \qquad -u^0 v^0 + \delta_{ij} u^i v^j < 0
    \end{aligned}
    $$

    **2.** Consider $\eta(u + tv, u + tv) = \lVert u \rVert^2 + 2t\, \eta(u, v) + t^2 \lVert v \rVert^2$

    (quadratic polynomial with negative leading coefficient &nbsp; $\Longrightarrow$ &nbsp; achieves a maximum at $t = -\dfrac{\eta(u, v)}{\lVert v \rVert^2}$)

    Let $w = u - \dfrac{\eta(u, v)}{\lVert v \rVert^2}\, v$

    $$
    \Longrightarrow \qquad \eta(v, w) = \eta(v, u) - \eta(u, v) \frac{\lVert v \rVert^2}{\lVert v \rVert^2} = 0
    $$

    $$
    \Longrightarrow \qquad w \in v^\perp \ \ (v \text{ timelike}) \qquad \Longrightarrow \qquad 0 \leq \underbrace{\lVert w \rVert^2}_{\text{spacelike}} = \lVert u \rVert^2 - \frac{2\, \eta(u, v)^2}{\lVert v \rVert^2} + \frac{\eta(u, v)^2}{\lVert v \rVert^2}
    $$

    $$
    \Longrightarrow \qquad \lVert u \rVert^2 \geq \frac{\eta(u, v)^2}{\lVert v \rVert^2} \quad (\lVert v \rVert^2: \text{negative})
    \qquad \Longrightarrow \qquad \lVert u \rVert^2 \lVert v \rVert^2 \leq \eta(u, v)^2 \qquad \text{reversed Cauchy–Schwarz}
    $$

    $$
    \Longrightarrow \qquad \underbrace{-\eta(u, v)}_{+\text{ve}} \geq \underbrace{\sqrt{-\lVert u \rVert^2}}_{+\text{ve}}\, \underbrace{\sqrt{-\lVert v \rVert^2}}_{+\text{ve}}
    $$

    **3.** $u + v$ is timelike

    **4.**

    $$
    \begin{aligned}
    -\lVert u + v \rVert^2 &= -\lVert u \rVert^2 - 2\, \eta(u, v) - \lVert v \rVert^2 \\
    &\geq -\lVert u \rVert^2 + 2 \sqrt{-\lVert u \rVert^2} \sqrt{-\lVert v \rVert^2} - \lVert v \rVert^2 = \left( \sqrt{-\lVert u \rVert^2} + \sqrt{-\lVert v \rVert^2} \right)^{\!2} \qquad \square
    \end{aligned}
    $$

    """
            ),
            corollary(
                r"""
    $$
    \sqrt{-\lVert \gamma(t_2) - \gamma(t_1) \rVert^2} \int_{t_1}^{t_2} \sqrt{-\lVert \gamma'(t) \rVert^2}\, dt \ \leq \ \int_{t_1}^{t_2} -\eta\big( \gamma(t_2) - \gamma(t_1),\ \gamma'(t) \big)\, dt = \left( \sqrt{-\lVert \gamma(t_2) - \gamma(t_1) \rVert^2} \right)^{\!2}
    $$

    (“$=$” if and only if $\gamma$ is inertial)
    """,
                "Inertial particles maximize proper time",
            ),
            mo.md(
                r"""
    ### Twin paradox

    **Example** (Twin paradox). Twin A stays on Earth, twin B visits a nearby star. Twin B returns and finds twin A is older

    $p = (0, 0)$, &nbsp; $r = (5, 4)$, &nbsp; $q = (10, 0)$; &nbsp; $s$ simultaneous to $r$ with respect to $q - p$ (A's point of view)

    $$
    \underbrace{\sqrt{-\underbrace{\lVert q - p \rVert^2}_{-100}}}_{\mathrm{time}_A(p, q) \,=\, 10} \ \geq \ \underbrace{\sqrt{-\underbrace{\lVert r - p \rVert^2}_{-25 + 16}}}_{\mathrm{time}_B(p, r) \,=\, 3} + \underbrace{\sqrt{-\underbrace{\lVert q - r \rVert^2}_{-25 + 16}}}_{\mathrm{time}_B(r, q) \,=\, 3}
    $$

    A waits 10 years for B's return; &nbsp; B takes 3 years to reach the star; &nbsp; B takes another 3 years to return

    $$
    \leadsto \qquad \sqrt{\frac{-\lVert s - p \rVert^2}{-\lVert r - p \rVert^2}} = \frac{5}{3} \quad \text{is called the time dilation factor between A and B}
    $$

    $$
    \left( \Gamma = \frac{1}{\sqrt{1 - \lVert \nu \rVert^2}} = \frac{1}{\sqrt{1 - (4/5)^2}} = \frac{5}{3} \right)
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    star = mo.ui.slider(0, 4.9, 0.1, value=4, label="distance to the star (spatial coordinate of $r$)", show_value=True)
    return (star,)


@app.cell(hide_code=True)
def _(BLUE, GREY, RED, arrow, blank, math, mo, star):
    _x = star.value
    _leg = math.sqrt(25 - _x**2)
    _fig, _ax = blank(4.0, 4.6, (-2.2, 6.6), (-0.9, 10.9))
    _ax.plot([0, 5], [0, 5], color=GREY, lw=0.8)  # light cone of p
    _ax.plot([0, 5], [10, 5], color=GREY, lw=0.8)  # light cone of q
    _ax.plot([-1.5, 6], [5, 5], "--", color=GREY, lw=1.0)
    arrow(_ax, (0, 0), (0, 10), BLUE)
    arrow(_ax, (0, 0), (_x, 5), RED)
    arrow(_ax, (_x, 5), (0, 10), RED)
    _ax.text(-0.3, 7.5, "A", color=BLUE, fontsize=12, ha="right")
    _ax.text(_x / 2 + 0.3, 2.3, "B", color=RED, fontsize=12)
    for _pt, _name, _off in (((0, 0), "$p = (0, 0)$", (8, -10)), ((0, 10), "$q = (10, 0)$", (8, 2)), ((_x, 5), f"$r = (5, {_x:g})$", (8, 6)), ((0, 5), "$s$", (-16, 4))):
        _ax.plot(*_pt, "o", color="black", ms=4)
        _ax.annotate(_name, _pt, textcoords="offset points", xytext=_off, fontsize=12, bbox=dict(boxstyle="round,pad=0.08", facecolor="white", edgecolor="none"), zorder=8)

    _table = "\n".join(
        [
            "| | |",
            "|:--|--:|",
            r"| $\mathrm{time}_A(p, q) = \sqrt{-\lVert q - p \rVert^2}$ | $10$ |",
            rf"| $\mathrm{{time}}_B(p, r) + \mathrm{{time}}_B(r, q) = 2 \sqrt{{25 - {_x:g}^2}}$ | ${2 * _leg:.2f}$ |",
            rf"| $\Gamma = 1 / \sqrt{{1 - ({_x:g}/5)^2}}$ | ${5 / _leg:.3f}$ |",
        ]
    )
    mo.vstack([mo.hstack([star], justify="start"), mo.md(_table), _fig])
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"### Relative velocity"),
            definition(
                r"""
    Given a particle $\gamma : \mathbb{R} \longrightarrow \mathbb{M}^4$ &nbsp; ($\lVert \gamma'(t) \rVert^2 = -1$)

    $$
    S_{\gamma(t)} = \gamma(t) + \gamma'(t)^\perp = \text{space of simultaneous events to } \gamma(t) \text{ relative to } \gamma'(t)
    $$
    """,
                "Space of simultaneity",
            ),
            mo.md(
                r"""
    (in $\mathbb{G}^4$: &nbsp; $S_{\gamma(t)} = \gamma(t) + \ker(\tau)$, independent from $\gamma$)

    Given two particles $\gamma, \sigma$ &nbsp; $\big( \lVert \gamma'(t) \rVert^2 = -1$, $\lVert \sigma'(s) \rVert^2 = -1$; &nbsp; $\gamma(0) = \sigma(0) = p$, $\gamma'(0) = u$, $\sigma'(0) = v \big)$

    The velocity of $\sigma$ relative to $\gamma$ at $p$ is the spacelike vector orthogonal to $u = \gamma'(0)$

    $$
    \nu(u, v) = \frac{v}{-\eta(u, v)} - u \in u^\perp \qquad (\text{depends on } u \text{ and } v)
    $$

    For the twins: &nbsp; $u = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \ v = \begin{bmatrix} 5/3 \\ 4/3 \end{bmatrix}$ &nbsp; $\Longrightarrow$ &nbsp; $\eta(u, v) = -5/3$ &nbsp; $\Longrightarrow$ &nbsp; $\nu = \begin{bmatrix} 0 \\ 4/5 \end{bmatrix}$ &nbsp; $\Longrightarrow$ &nbsp; $\lVert \nu \rVert^2 = \tfrac{16}{25}$

    In $\mathbb{G}^4$: &nbsp; $\nu(u, v) = v - u \in \ker \tau$ &nbsp; (the same subspace for every $u$, unlike $u^\perp$ &nbsp; $\Longrightarrow$ &nbsp; simple formula for the addition of relative velocities &nbsp; $\Longrightarrow$ &nbsp; broke Maxwell)

    $$
    \Longrightarrow \qquad \lVert \nu(u, v) \rVert^2 = \frac{\lVert v \rVert^2}{\eta(u, v)^2} + \lVert u \rVert^2 + 2\, \frac{\eta(u, v)}{\eta(u, v)} = 1 + \frac{\lVert v \rVert^2}{\eta(u, v)^2} < 1
    $$

    Relative speeds are bounded above (by 1)
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    beta = mo.ui.slider(-0.95, 0.95, 0.05, value=0.6, label="$\\beta = v^1 / v^0$", show_value=True)
    return (beta,)


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, ORANGE, RED, arrow, beta, blank, math, mo):
    _b = beta.value
    _g = 1 / math.sqrt(1 - _b**2)
    _v = (_g * _b, _g)  # (space, time), normalized: -t^2 + x^2 = -1

    _L = max(1.7, 1.2 * _v[1])  # axes grow with v: the unit vector is never rescaled
    _fig, _ax = blank(4.6, 4.2, (-_L, _L), (-_L, _L))
    _ax.plot([-_L, _L], [-_L, _L], color=GREY, lw=0.8)
    _ax.plot([-_L, _L], [_L, -_L], color=GREY, lw=0.8)
    _ax.plot([-_L, _L], [0, 0], color=BLUE, lw=1.0)
    _ax.text(_L * 0.98, -0.12 * _L, r"$p + u^\perp = S_p^u$", color=BLUE, fontsize=12, ha="right")
    _ax.plot([-_L, _L], [-_L * _b, _L * _b], color=RED, lw=1.0)
    _ax.annotate(r"$p + v^\perp = S_p^v$", (-_L * 0.95, -_L * 0.95 * _b), textcoords="offset points", xytext=(0, -16 if _b >= 0 else 8), color=RED, fontsize=12)
    arrow(_ax, (0, 0), (0, 1), BLUE)
    _ax.annotate("$u$", (0, 0.5), textcoords="offset points", xytext=(-16, -4), color=BLUE, fontsize=16)
    arrow(_ax, (0, 0), _v, RED)
    _ax.annotate("$v$", (_v[0] / 2, _v[1] / 2), textcoords="offset points", xytext=(8, -8) if _b >= 0 else (-18, -8), color=RED, fontsize=16)
    # nu(u, v) = v / (-eta) - u: from the tip of u along S_p^u;  nu(v, u) = u / (-eta) - v: from the tip of v along S_p^v
    arrow(_ax, (0, 1), (_b, 1), GREEN)
    _ax.annotate(r"$\nu(u, v)$", (_b / 2, 1), textcoords="offset points", xytext=(0, 6), color=GREEN, fontsize=12, ha="center", va="bottom")
    arrow(_ax, _v, (0, 1 / _g), ORANGE)
    _ax.annotate(r"$\nu(v, u)$", _v, textcoords="offset points", xytext=(8, 0) if _b >= 0 else (-8, 0), color=ORANGE, fontsize=12, ha="left" if _b >= 0 else "right", va="center", bbox=dict(boxstyle="round,pad=0.08", facecolor="white", edgecolor="none"), zorder=8)
    _ax.plot(0, 0, "o", color="black", ms=4)
    _ax.text(0.1, -0.3, "$p$", fontsize=13)

    _table = "\n".join(
        [
            "| | |",
            "|:--|--:|",
            r"| $u$ | $(1,\ 0)$ |",
            rf"| $v = \Gamma\, (1,\ \beta)$ | $({_g:.3f},\ {_g * _b:.3f})$ |",
            rf"| $\eta(u, v)$ | ${-_g:.3f}$ |",
            rf"| $\nu(u, v)$ | $(0,\ {_b:g})$ |",
            rf"| $\lVert \nu(u, v) \rVert^2$ | ${_b**2:.3f}$ |",
        ]
    )
    mo.vstack([mo.hstack([beta], justify="start"), mo.md(_table), _fig])
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"### Photons and Maxwell's equations"),
            definition(
                r"""
    A **photon** in $\mathbb{M}^4$ is a future oriented lightlike line &nbsp; $\xi(s) = p + s w$ &nbsp; ($\lVert w \rVert^2 = 0$ in the future cone)
    """,
                "Photon",
            ),
            mo.md(
                r"""
    The relative velocity of a photon relative to a particle $\gamma$ as above is

    $$
    \nu(u, w) = \frac{w}{-\eta(u, w)} - u \in u^\perp
    $$

    $$
    \Longrightarrow \qquad \lVert \nu(u, w) \rVert^2 = \underbrace{\frac{\lVert w \rVert^2}{\eta(u, w)^2}}_{=\, 0} + \lVert u \rVert^2 + 2\, \frac{\eta(u, w)}{\eta(u, w)} = 1\,!
    $$

    - photons *achieve the maximal relative velocity* with respect to every other particle!
    - Minkowski geometry is not incompatible with Maxwell's electrodynamics (at least in principle)

    **Remark.** Maxwell's equations

    $$
    \begin{gathered}
    \begin{cases}
    \underbrace{\partial_i B^i}_{\nabla \cdot B} = 0, \qquad \underbrace{\epsilon^{ijk} \partial_j E_k}_{\nabla \times E} + \partial_0 B^i = 0 \\[10pt]
    \partial_i E^i = \rho, \qquad \epsilon^{ijk} \partial_j B_k - \partial_0 E^i = J^i
    \end{cases} \\[8pt]
    \text{not invariant under change of Galilean inertial frames… (Galilean transformations)}
    \end{gathered}
    $$

    have a very “simple” formulation in Minkowski spacetime

    $$
    \begin{cases} \partial_\mu \tilde{F}^{\mu\nu} = 0 \\ \partial_\mu F^{\mu\nu} = J^\nu \end{cases}
    \qquad \text{invariant under change of Minkowski inertial frame! (Poincaré transformations)}
    $$

    $$
    F^{\mu\nu} = \begin{bmatrix} 0 & -E^1 & -E^2 & -E^3 \\ E^1 & 0 & -B^3 & B^2 \\ E^2 & B^3 & 0 & -B^1 \\ E^3 & -B^2 & B^1 & 0 \end{bmatrix}, \qquad
    \tilde{F}^{\mu\nu} = \begin{bmatrix} 0 & -B^1 & -B^2 & -B^3 \\ B^1 & 0 & E^3 & -E^2 \\ B^2 & -E^3 & 0 & E^1 \\ B^3 & E^2 & -E^1 & 0 \end{bmatrix}, \qquad
    J^\mu = \begin{bmatrix} \rho \\ J^i \end{bmatrix}
    $$

    ## Summary

    - proper time length $\int \sqrt{-\lVert \gamma' \rVert^2}\, dt$ is the clock carried by each particle; it is *longest* along the inertial particle (reversed triangle inequality), which is the twin paradox
    - the relative velocity $\nu(u, v) = v / (-\eta(u, v)) - u \in u^\perp$ has $\lVert \nu \rVert^2 = 1 - 1 / \eta(u, v)^2 < 1$, and $= 1$ exactly for photons, for every observer
    - Maxwell's equations take the frame-independent form $\partial_\mu F^{\mu\nu} = J^\nu$, $\partial_\mu \tilde{F}^{\mu\nu} = 0$ in Minkowski spacetime

    **Next:** the Lorentz factor, photons as limits of particles, and relativistic dynamics (4-momentum, energy, 4-force)
    """
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
