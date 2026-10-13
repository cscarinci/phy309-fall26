import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 02 · Galilean geometry", css_file="phy309.css")


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
    header("Lecture 02", "Week 01", "Lecture 02 · Galilean geometry")
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, LIGHT, ORANGE, RED, arrow, blank, np):
    # Static sketches from the handwritten notes (time runs upwards, one spatial direction drawn)

    # Inertial frame: e0 future unit vector, e_i, e_j spatial orthonormal, coordinates of p
    fig_frame, _ax = blank(3.4, 3.0, (-1.4, 2.6), (-1.1, 2.3))
    _f = lambda x, y, z: (y - 0.5 * x, z - 0.45 * x)
    for _tip, _name, _col, _off in (((2.0, 0, 0), r"$\vec{e}_i$", "black", (2, -14)), ((0, 2.2, 0), r"$\vec{e}_j$", "black", (4, -4)), ((0, 0, 2.0), r"$\vec{e}_0$", "black", (6, -4))):
        arrow(_ax, (0, 0), _f(*_tip), _col)
        _ax.annotate(_name, _f(*_tip), textcoords="offset points", xytext=_off, color=_col, fontsize=13)
    _p = (1.0, 1.4, 1.5)
    for _a, _b in (((1.0, 0, 0), (1.0, 1.4, 0)), ((0, 1.4, 0), (1.0, 1.4, 0)), ((1.0, 1.4, 0), _p), ((0, 0, 1.5), _p)):
        _ax.plot(*zip(_f(*_a), _f(*_b)), "--", color=GREEN, lw=1.0)
    arrow(_ax, (0, 0), _f(*_p), BLUE)
    _ax.plot(*_f(*_p), "o", color="black", ms=4)
    _ax.annotate("$p$", _f(*_p), textcoords="offset points", xytext=(6, 2), fontsize=13)
    _ax.plot(0, 0, "o", color="black", ms=4)
    _ax.annotate("$o$", (0, 0), textcoords="offset points", xytext=(-14, -2), fontsize=13)
    for _q, _n, _off in (((1.0, 0, 0), "$x^i$", (-20, 2)), ((0, 1.4, 0), "$x^j$", (-4, 6)), ((0, 0, 1.5), "$t$", (-14, -2))):
        _ax.annotate(_n, _f(*_q), textcoords="offset points", xytext=_off, color=GREEN, fontsize=12)

    # Relative velocity of gamma_2 with respect to gamma_1
    fig_relvel, _ax = blank(3.2, 2.6, (-1.6, 2.2), (-1.0, 1.9))
    _s = np.linspace(-1.0, 1.5, 100)
    _ax.plot(-0.4 * _s - 0.25 * _s**2, _s, color=BLUE)
    _ax.plot(0.8 * _s + 0.2 * _s**2, _s, color=RED)
    _ax.text(-0.95, 1.55, r"$\gamma_1$", color=BLUE, fontsize=13)
    _ax.text(1.55, 1.55, r"$\gamma_2$", color=RED, fontsize=13)
    arrow(_ax, (0, 0), (-0.4, 1.0), BLUE)
    _ax.text(-0.5, 0.5, r"$\gamma_1'$", color=BLUE, fontsize=13, ha="right")
    arrow(_ax, (0, 0), (0.8, 1.0), RED)
    _ax.text(1.0, 0.65, r"$\gamma_2'$", color=RED, fontsize=13)
    arrow(_ax, (-0.4, 1.0), (0.8, 1.0), GREEN)
    _ax.text(0.2, 1.12, r"$\vec{v}(\gamma_1, \gamma_2)$", color=GREEN, fontsize=12, ha="center", va="bottom")
    _ax.plot(0, 0, "o", color="black", ms=4)

    # Newtonian gravity: sigma straight, gamma attracted; both events in the slice S_gamma(t)
    fig_gravity, _ax = blank(3.8, 2.8, (-2.3, 2.5), (-1.6, 1.9))
    _s = np.linspace(-1.5, 1.6, 120)
    _ax.plot([0, 0], [-1.5, 1.7], color="black")
    _ax.plot(1.1 - 0.35 * _s**2, _s, color=BLUE)
    _ax.fill([-2.2, 1.6, 2.4, -1.4], [-0.45, -0.45, 0.45, 0.45], color=LIGHT, alpha=0.6, lw=0)
    _ax.plot([-2.2, 1.6, 2.4, -1.4, -2.2], [-0.45, -0.45, 0.45, 0.45, -0.45], color=GREY, lw=1.0)
    arrow(_ax, (1.1, 0), (0.15, 0), GREEN)
    _ax.plot([0, 1.1], [0, 0], "o", color="black", ms=4)
    _ax.text(-0.15, 0.1, r"$\sigma(t)$", fontsize=12, ha="right")
    _ax.text(1.2, 0.1, r"$\gamma(t)$", color=BLUE, fontsize=12)
    _ax.text(-0.12, 1.5, r"$\sigma$", fontsize=13, ha="right")
    _ax.text(0.65, -1.35, r"$\gamma$", color=BLUE, fontsize=13)
    _ax.text(1.0, -0.75, r"$S_{\gamma(t)}$", color=GREY, fontsize=12)

    # Velocity addition for three particles through one event
    fig_addition, _ax = blank(3.2, 2.8, (-1.3, 2.3), (-0.9, 1.9))
    _s = np.linspace(-0.8, 1.5, 100)
    _ax.plot(-0.3 * _s - 0.15 * _s**2, _s, color=BLUE)
    _ax.plot(0.4 * _s + 0.1 * _s**2, _s, color=RED)
    _ax.plot(1.2 * _s, _s, color=ORANGE)
    _ax.text(-0.85, 1.55, r"$\gamma$", color=BLUE, fontsize=13)
    _ax.text(0.95, 1.55, r"$\sigma$", color=RED, fontsize=13)
    _ax.text(1.95, 1.4, r"$\xi$", color=ORANGE, fontsize=13)
    arrow(_ax, (0, 0), (-0.3, 1.0), BLUE)
    arrow(_ax, (0, 0), (0.4, 1.0), RED)
    arrow(_ax, (0, 0), (1.2, 1.0), ORANGE)
    _bb = dict(boxstyle="round,pad=0.1", facecolor="white", edgecolor="none", alpha=0.9)
    arrow(_ax, (-0.3, 1.0), (0.4, 1.0), GREEN)
    arrow(_ax, (0.4, 1.0), (1.2, 1.0), GREEN)
    arrow(_ax, (-0.3, 1.45), (1.2, 1.45), GREEN)
    _ax.text(0.05, 1.07, r"$\vec{v}(\gamma, \sigma)$", color=GREEN, fontsize=11, ha="center", va="bottom", bbox=_bb)
    _ax.text(0.8, 1.07, r"$\vec{v}(\sigma, \xi)$", color=GREEN, fontsize=11, ha="center", va="bottom", bbox=_bb)
    _ax.text(0.45, 1.53, r"$\vec{v}(\gamma, \xi)$", color=GREEN, fontsize=11, ha="center", va="bottom", bbox=_bb)
    _ax.plot(0, 0, "o", color="black", ms=4)
    _ = None  # no cell output: the figures are returned, not displayed here

    return fig_addition, fig_frame, fig_gravity, fig_relvel


@app.cell(hide_code=True)
def _(BLUE, GREY, RED, arrow, blank, definition, mo):
    _fig, _ax = blank(5.0, 2.4, (-0.5, 5.2), (-0.9, 1.7))
    arrow(_ax, (0, 0), (0.5, 1.4), BLUE)
    arrow(_ax, (0, 0), (1.3, 0), GREY)
    arrow(_ax, (0, 0), (0.8, -0.5), RED)
    _ax.text(0.45, 1.5, "future", color=BLUE, fontsize=12, ha="center")
    _ax.text(1.4, -0.05, "spatial / simultaneous", color=GREY, fontsize=12)
    _ax.text(0.85, -0.8, "past", color=RED, fontsize=12, ha="center")
    _ax.text(-0.3, -0.25, "$p$", fontsize=13)
    _ax.plot(0, 0, "o", color="black", ms=4)
    arrow(_ax, (3.4, 0.9), (4.2, 0.9), "black", lw=1.0, connectionstyle="arc3,rad=-0.3")
    _ax.text(3.75, 1.2, r"$\tau$", fontsize=13)
    _ax.plot([4.7, 4.7], [-0.8, 1.6], color="black")
    for _y, _col, _name in ((1.4, BLUE, "$> 0$"), (0, GREY, "$0$"), (-0.5, RED, "$< 0$")):
        _ax.plot(4.7, _y, "o", color=_col, ms=4)
        _ax.text(4.85, _y, _name, color=_col, fontsize=12, va="center")

    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    - Euclidean space $\mathbb{E}^3$ = affine space $(\mathbb{A}, \mathbb{V}, -)$ &nbsp; ($-$: difference between points = displacement vector) &nbsp; + Euclidean inner product $\langle\ ,\ \rangle$ &nbsp; (measurements)
    - a choice of origin $o \in \mathbb{E}^3$ and orthonormal basis $\vec{e}_1, \vec{e}_2, \vec{e}_3 \in \mathbb{V}$ &nbsp; $\Longrightarrow$ &nbsp; Cartesian coordinates

    **In this lecture:** the same construction for spacetime: Galilean spacetime and Newtonian mechanics

    ## I.2 &nbsp; Galilean geometry

    The geometry of spacetime in Newtonian physics

    **Spacetime** = set of all *events* (locations in space + moments in time)

    **Mechanics** = study of the origins of *motion* (relations between events = geometry of spacetime)
    """
            ),
            definition(
                r"""
    The **Galilean spacetime** is a 4-dimensional affine space

    $$
    \mathbb{G}^4 = (\mathbb{A}, \mathbb{V}, -) \qquad (\text{assumptions (i), (ii), (iii) as before, with } \dim \mathbb{V} = 4)
    $$

    together with *some extra structure* (different assumptions needed)
    """,
                "Galilean spacetime",
            ),
            mo.md(
                r"""
    ### The universal time function

    **(iv)** there exists a function $\tau : \mathbb{V} \longrightarrow \mathbb{R}$

    - linear: &nbsp; $\tau(a\vec{u} + b\vec{v}) = a\, \tau(\vec{u}) + b\, \tau(\vec{v})$
    - non-zero: &nbsp; $\exists\, \vec{u} \in \mathbb{V}$ with $\tau(\vec{u}) \neq 0$

    We can define the *time length* of vectors $\tau(\vec{u})$ (not necessarily positive) and the *time distance* between events $t(p, q) = \tau(q - p)$ (from $p$ to $q$)
    """
            ),
            definition(
                r"""
    - $\vec{u}$ **future oriented** if $\tau(\vec{u}) > 0$ &nbsp; $\leadsto$ &nbsp; $q$ in future of $p$ if $\tau(q - p) > 0$
    - $\vec{u}$ **past oriented** if $\tau(\vec{u}) < 0$ &nbsp; $\leadsto$ &nbsp; $q$ in past of $p$ if $\tau(q - p) < 0$
    - $\vec{u}$ **spatial** if $\tau(\vec{u}) = 0$ &nbsp; $\leadsto$ &nbsp; $p$ and $q$ are simultaneous if $\tau(q - p) = 0$
    """,
                r"Causal structure in $\mathbb{G}^4$",
            ),
            _fig,
            mo.md(
                r"""
    ### The spatial inner product

    **(iv′)** there is a Euclidean inner-product on $\ker \tau$ &nbsp; ($\dim = 3$!)

    $$
    \langle\ ,\ \rangle : \ker \tau \times \ker \tau \longrightarrow \mathbb{R}
    $$

    We can define spatial length

    $$
    \text{if } \tau(\vec{u}) = 0 \qquad \Longrightarrow \qquad \lVert \vec{u} \rVert = \sqrt{\langle \vec{u}, \vec{u} \rangle}
    $$

    Each set of mutually simultaneous events in $\mathbb{G}^4$ is an identical copy of $\mathbb{E}^3$

    $$
    S_p = \{\, q \in \mathbb{G}^4 \mid \tau(q - p) = 0 \,\} = p + \ker \tau \approx \mathbb{E}^3
    $$
    """
            ),
            definition(
                r"""
    $\mathbb{G}^4 = (\mathbb{A}, \mathbb{V}, -)$ 4-dimensional affine space together with a universal time function $\tau$ and a spatial inner product $\langle\ ,\ \rangle$ on $\ker \tau$
    """,
                "Galilean spacetime",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, fig_frame, fig_relvel, mo, proposition, theorem):
    mo.vstack(
        [
            mo.md(r"### Inertial frames"),
            theorem(
                r"""
    Choosing $o \in \mathbb{G}^4$ (origin) and $\vec{e}_0, \vec{e}_1, \vec{e}_2, \vec{e}_3 \in \mathbb{V}$ (inertial frame) such that

    $$
    \begin{aligned}
    & \tau(\vec{e}_0) = 1 && \text{unit future oriented} \\
    & \tau(\vec{e}_i) = 0, \quad i = 1, 2, 3 \\
    & \langle \vec{e}_i, \vec{e}_j \rangle = \delta_{ij} = \begin{cases} 1 & i = j \\ 0 & i \neq j \end{cases} && \text{spatial orthonormal basis}
    \end{aligned}
    $$

    $\Longrightarrow$ &nbsp; Cartesian coordinates $x^\mu : \mathbb{G}^4 \longrightarrow \mathbb{R}$, &nbsp; $\mu = 0, \underbrace{1, 2, 3}_{i}$

    $$
    x^0(p) = \tau(p - o), \qquad x^i(p) = \langle \vec{e}_i,\ p - o - x^0(p)\, \vec{e}_0 \rangle
    $$

    $\Longrightarrow$ &nbsp; identification $\mathbb{R}^4 \approx \mathbb{G}^4$

    $$
    (t, x, y, z) \longleftrightarrow p = o + t\vec{e}_0 + x\vec{e}_1 + y\vec{e}_2 + z\vec{e}_3
    $$
    """,
                "Cartesian coordinates",
            ),
            fig_frame,
            mo.md(
                r"""
    $$
    \text{then} \quad \tau(t, x, y, z) = t, \qquad \lVert (0, x, y, z) \rVert = \sqrt{x^2 + y^2 + z^2}
    $$

    ### Kinematics and dynamics
    """
            ),
            definition(
                r"""
    A **particle** in $\mathbb{G}^4$ is a parameterized curve

    $$
    \gamma : \mathbb{R} \longrightarrow \mathbb{G}^4, \qquad s \longmapsto \gamma(s)
    $$

    such that &nbsp; $\gamma'(s) = \displaystyle\lim_{\varepsilon \to 0} \frac{\gamma(s + \varepsilon) - \gamma(s)}{\varepsilon} \in \mathbb{V}$ &nbsp; is future oriented: &nbsp; $\tau(\gamma'(s)) > 0 \quad \forall\, s$

    ($\gamma$: all events in the particle's history)
    """,
                "Particle",
            ),
            mo.md(
                r"""
    We can now study dynamics (change of position as function of time) as the shape of a *curve in spacetime* (the history of events)

    **Remark.** $\gamma'(s)$ is not the particle's velocity

    - it is a 4-dimensional vector…
    - $s$ in $\gamma(s)$ is not related to physical time (without other assumptions)
    """
            ),
            proposition(
                r"""
    Every particle can be parameterized by an “absolute time” parameter $t$ such that

    $$
    \tau(\gamma(t_2) - \gamma(t_1)) = t_2 - t_1
    $$
    """,
                "Absolute time",
            ),
            mo.md(
                r"""
    **Proof** (idea). Up to solving some ODE we can always change parameterization so that $\tau(\gamma'(t)) = 1$

    $$
    \begin{aligned}
    \Longrightarrow \qquad t_2 - t_1 = \int_{t_1}^{t_2} dt &= \int_{t_1}^{t_2} \tau(\gamma'(t))\, dt \\
    &= \tau\!\left( \int_{t_1}^{t_2} \gamma'(t)\, dt \right) = \tau(\gamma(t_2) - \gamma(t_1)) \qquad \square
    \end{aligned}
    $$

    We can now measure time. How do we define *spatial velocity*? (not possible with a single particle)
    """
            ),
            definition(
                r"""
    Given two particles $\gamma_1, \gamma_2$ (with $\tau(\gamma_1') = \tau(\gamma_2') = 1$) the **relative velocity** of $\gamma_2$ with respect to $\gamma_1$ is the spatial vector

    $$
    \vec{v}(\gamma_1, \gamma_2) = \gamma_2' - \gamma_1' \in \ker(\tau)
    $$
    """,
                "Relative velocity",
            ),
            fig_relvel,
            definition(
                r"""
    The **absolute acceleration** (does not require other reference) of a particle $\gamma$ &nbsp; ($\tau(\gamma') = 1$) is the spatial vector

    $$
    \vec{a}(\gamma) = \gamma'' \in \ker(\tau) \qquad \left( \tau(\gamma'') = \frac{d}{dt} \tau(\gamma') = 0 \right)
    $$
    """,
                "Absolute acceleration",
            ),
            mo.md(
                r"""
    **Remark** (Newton's first and second laws). In the absence of external forces, a particle's history is a *straight future oriented line*

    $$
    \gamma(t) = p + t\vec{u}, \qquad \tau(\vec{u}) = 1
    $$

    (solution of $\gamma''(t) = \vec{0}$, $\gamma(0) = p$, $\gamma'(0) = \vec{u}$; &nbsp; inertial particle / inertial observer)

    Deviation from inertial motion is determined by

    $$
    \gamma''(t) = \frac{1}{m} \vec{F}(t), \qquad \text{where } m \in \mathbb{R}_+ \ (\text{mass}), \quad \vec{F}(t) \in \ker(\tau) \ (\text{Force})
    $$

    (system of second order ODEs)

    In Cartesian coordinates (choice of origin and inertial frame)

    $$
    \gamma''(t) = \begin{bmatrix} t \\ x(t) \\ y(t) \\ z(t) \end{bmatrix}'' = \begin{bmatrix} 0 \\ x''(t) \\ y''(t) \\ z''(t) \end{bmatrix} = \frac{1}{m} \begin{bmatrix} 0 \\ F^x(t) \\ F^y(t) \\ F^z(t) \end{bmatrix}
    $$

    **Example.** constant force: &nbsp; $\vec{F}(t) = \vec{v} \in \ker(\tau)$

    $$
    \Longrightarrow \qquad \gamma(t) = p + t\vec{u} + \frac{1}{2m} t^2 \vec{v}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    u_x = mo.ui.slider(-1.5, 1.5, 0.1, value=0, label="spatial part of $\\vec{u}$", show_value=True)
    f_m = mo.ui.slider(-3, 3, 0.1, value=1.5, label="$\\vec{v} / m$", show_value=True)
    return f_m, u_x


@app.cell(hide_code=True)
def _(BLUE, FULL, GREEN, GREY, LIGHT, ORANGE, arrow, blank, f_m, mo, np, u_x):
    _u, _a = u_x.value, f_m.value
    _t = np.linspace(-1.6, 1.6, 200)
    _x = _t * _u + 0.5 * _a * _t**2
    _lim = max(3.2, 1.1 * float(np.abs(_x).max()))
    _fig, _ax = blank(FULL, 4.0, (-_lim, _lim), (-2.05, 1.95))
    _ax.set_aspect("auto")
    for _lev in (-1.5, -1, -0.5, 0.5, 1, 1.5):
        _ax.plot([-_lim, _lim], [_lev, _lev], color=LIGHT, lw=0.8)
    _ax.plot([-_lim, _lim], [0, 0], color=GREY, lw=1.0)
    _ax.text(_lim * 0.98, 0.07, "$S_p$", color=GREY, fontsize=12, ha="right")
    _ax.plot(_t * _u, _t, "--", color=GREY)
    _ax.text(-1.6 * _u, -1.64, r"$p + t\vec{u}$", color=GREY, fontsize=12, ha="center", va="top")
    _ax.plot(_x, _t, color=BLUE)
    _ax.text(_x[-1], 1.62, r"$\gamma$", color=BLUE, fontsize=13, ha="center", va="bottom")
    arrow(_ax, (0, 0), (_u * 0.7, 0.7), GREEN, r"$\vec{u}$", at_tip=True)
    if _a != 0:
        arrow(_ax, (0, 0), (_a, 0), ORANGE, r"$\vec{v} / m$", at_tip=True)
    _ax.plot(0, 0, "o", color="black", ms=4)
    _ax.text(-0.3, -0.3, "$p$", fontsize=13, ha="right")
    _ax.text(-_lim * 0.98, 1.6, "time $\\uparrow$", fontsize=11)

    mo.vstack([mo.hstack([u_x, f_m], justify="start", gap=3, wrap=True), _fig])
    return


@app.cell(hide_code=True)
def _(fig_addition, fig_gravity, mo, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ### Newtonian gravity and Maxwell's electrodynamics

    Newtonian gravity:

    $$
    \vec{F}(t) = -G m M\, \frac{\gamma(t) - \sigma(t)}{\lVert \gamma(t) - \sigma(t) \rVert^3} \in \ker(\tau) \qquad (\gamma(t), \sigma(t) \text{ simultaneous})
    $$

    $S_{\gamma(t)}$ = space of simultaneity of $\gamma(t)$ $\approx \mathbb{E}^3$
    """
            ),
            fig_gravity,
            mo.md(
                r"""
    Coulomb's law of electrostatics can be written almost identically exchanging masses and charges!

    Maxwell's electrodynamics breaks down: in Cartesian coordinates we want something like

    $$
    \vec{F}(t) = q \left( \vec{E}_{\sigma(t)} + \vec{v}_{\gamma(t)} \times \vec{B}_{\sigma(t)} \right) \qquad \text{Lorentz force law}
    $$

    - $\vec{E}_{\sigma(t)}$: electric field generated by $\sigma$ (depends on the inertial frame)
    - $\vec{v}_{\gamma(t)}$: velocity of $\gamma$ (relative to the inertial frame)
    - $\vec{B}_{\sigma(t)}$: magnetic field generated by $\sigma$ (depends on the inertial frame)

    with

    $$
    \begin{aligned}
    \vec{\nabla} \cdot \vec{E}_{\sigma(t)} &= \frac{\rho_{\sigma(t)}}{\varepsilon_0}, & \vec{\nabla} \times \vec{B}_{\sigma(t)} - \frac{1}{c^2} \partial_t \vec{E}_{\sigma(t)} &= \mu_0\, \vec{J}_{\sigma(t)} \\[4pt]
    \vec{\nabla} \cdot \vec{B}_{\sigma(t)} &= 0, & \vec{\nabla} \times \vec{E}_{\sigma(t)} + \partial_t \vec{B}_{\sigma(t)} &= 0
    \end{aligned}
    \qquad \text{Maxwell's Equations}
    $$

    (depend on the choice of *inertial frame*: not an intrinsic physical structure)

    **Remark.** In the vacuum, Maxwell implies the wave equation

    $$
    \begin{cases}
    \vec{\nabla} \cdot \vec{E} = 0, \quad \vec{\nabla} \times \vec{B} - \frac{1}{c^2} \partial_t \vec{E} = 0 \\[4pt]
    \vec{\nabla} \cdot \vec{B} = 0, \quad \vec{\nabla} \times \vec{E} + \partial_t \vec{B} = 0
    \end{cases}
    \qquad \Longrightarrow \qquad
    \begin{cases}
    \left( \Delta - \frac{1}{c^2} \partial_t^2 \right) \vec{E} = 0 \\[4pt]
    \left( \Delta - \frac{1}{c^2} \partial_t^2 \right) \vec{B} = 0
    \end{cases}
    $$

    $\Longrightarrow$ &nbsp; electromagnetic “waves” propagate at constant speed $c$ (the speed of light)

    Experimentally $c$ is *independent* of the choice of inertial frames

    $\Longrightarrow$ &nbsp; the speed of light relative to any inertial particle is *always constant* &nbsp; (not possible in Galilean spacetime)!
    """
            ),
            theorem(
                r"""
    Given $\gamma, \sigma, \xi$ three particles in $\mathbb{G}^4$

    $$
    \vec{v}(\gamma, \xi) = \vec{v}(\gamma, \sigma) + \vec{v}(\sigma, \xi)
    $$
    """,
                "Addition of relative velocities",
            ),
            fig_addition,
            mo.md(
                r"""
    $$
    \begin{gathered}
    \text{triangle inequality} \qquad \Longrightarrow \qquad \lVert \vec{v}(\gamma, \xi) \rVert \leq \lVert \vec{v}(\gamma, \sigma) \rVert + \lVert \vec{v}(\sigma, \xi) \rVert \\[4pt]
    \text{with equality if and only if one of the two vectors is a non-negative multiple of the other}
    \end{gathered}
    $$

    $\gamma, \sigma$ are inertial particles and $\xi$ is a light particle moving along same direction

    $$
    \Longrightarrow \qquad c = \lVert \vec{v}(\gamma, \sigma) \rVert + c \qquad \text{contradiction unless } \gamma, \sigma \text{ have zero relative velocity}
    $$

    ## Summary

    - Galilean spacetime $\mathbb{G}^4$ = 4-dimensional affine space + universal time $\tau$ + Euclidean inner product on $\ker \tau$; simultaneity is absolute: $S_p = p + \ker \tau \approx \mathbb{E}^3$
    - particles are future-oriented curves; absolute time parameterizes them; relative velocity and absolute acceleration are spatial vectors
    - Newton's laws are second order ODEs in spacetime; Newtonian gravity fits, Maxwell's electrodynamics does not: relative velocities add, so no speed can be the same for every inertial observer

    **Next:** Minkowski spacetime, a geometry in which the speed of light is the same for every inertial particle
    """
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
