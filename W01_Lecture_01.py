import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 • Lecture 01 • Euclidean geometry", css_file="phy309.css")


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
    BLUE, RED, GREEN, ORANGE, GREY, LIGHT = "#3f5f8f", "#a8554c", "#4f7f5c", "#b9853f", "#9a9a9a", "#e3ebf4"
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
        The head is small and open, sized from the line width (3 x long, 1.3 x wide, in points), so arrows look alike across lectures."""
        ax.annotate(
            "",
            xy=tip,
            xytext=tail,
            arrowprops={"arrowstyle": f"->,head_length={3 * lw:g},head_width={1.3 * lw:g}", "mutation_scale": 1, "color": color, "lw": lw, "shrinkA": 0, "shrinkB": 0, **kw},
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
        _md = mo.md("\n".join(["| | |", "|:--|:--|"] + [f"| {k} | {v} |" for k, v in rows]))
        return mo.Html(f'<div class="readout">{_md.text}</div>')

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
    header("Lecture 01", "Week 01", "Lecture 01 • Euclidean geometry")
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, HALF, ORANGE, RED, arrow, blank, mo, theorem):
    def _pt(ax, xy, name, off=(-14, -4)):
        ax.plot(*xy, "o", color="black", ms=4)
        ax.annotate(name, xy, textcoords="offset points", xytext=off, fontsize=13)

    # (i) the displacement vector from p to q
    _f1, _a1 = blank(HALF, 1.6, (-0.4, 2.8), (-0.5, 1.0))
    arrow(_a1, (0, 0), (2, 0.6), BLUE)
    _a1.text(0.9, -0.3, r"$\vec{u} = q - p$", color=BLUE, fontsize=13)
    _pt(_a1, (0, 0), "$p$")
    _pt(_a1, (2, 0.6), "$q$", (6, -4))

    # (ii) a congruent copy of v at q
    _f2, _a2 = blank(HALF, 2.0, (-0.4, 2.9), (-0.3, 1.7))
    _a2.plot([0, 2], [0, 0.4], "--", color=GREY, lw=1.0)
    arrow(_a2, (0, 0), (0.3, 1.1), RED)
    arrow(_a2, (2, 0.4), (2.3, 1.5), RED)
    _a2.text(0.75, 1.35, r"$\vec{v} = \vec{v}\,'$", color=RED, fontsize=13)
    _pt(_a2, (0, 0), "$p$")
    _pt(_a2, (2, 0.4), "$q$", (6, -8))

    # addition of vectors
    _f3, _a3 = blank(HALF, 2.3, (-0.5, 3.0), (-0.4, 1.9))
    arrow(_a3, (0, 0), (1.9, 0.4), BLUE)
    arrow(_a3, (0, 0), (0.4, 1.1), RED)
    arrow(_a3, (1.9, 0.4), (2.3, 1.5), RED)
    arrow(_a3, (0, 0), (2.3, 1.5), GREEN)
    _a3.text(1.0, -0.3, r"$\vec{u}$", color=BLUE, fontsize=13)
    _a3.text(0.95, 1.05, r"$\vec{u} + \vec{v}$", color=GREEN, fontsize=13)
    _a3.text(2.25, 0.8, r"$\vec{v}\,'$", color=RED, fontsize=13)
    _a3.text(-0.15, 0.6, r"$\vec{v}$", color=RED, fontsize=13)
    _pt(_a3, (0, 0), "$p$")
    _pt(_a3, (1.9, 0.4), "$q$", (6, -10))
    _pt(_a3, (2.3, 1.5), "$r$", (6, 2))

    # scalar multiples and the parallelogram
    _f4, _a4 = blank(5.6, 2.1, (-1.3, 5.6), (-0.95, 1.85))
    arrow(_a4, (0, 0), (1.15, 1.53), GREEN)
    arrow(_a4, (0, 0), (-0.5, -0.67), ORANGE)
    arrow(_a4, (0, 0), (0.45, 0.6), RED)
    _a4.plot(0, 0, "o", color="black", ms=4, zorder=5)
    _a4.text(0.1, 0.55, r"$\vec{v}$", color=RED, fontsize=13)
    _a4.text(1.25, 1.3, r"$\pi \vec{v}$", color=GREEN, fontsize=13)
    _a4.text(-0.45, -0.9, r"$-\vec{v}$", color=ORANGE, fontsize=13)
    _o = (3.0, -0.3)
    for _tail, _tip, _c in (((0, 0), (1.6, 0.0), BLUE), ((0, 0), (0.3, 1.1), RED), ((0.3, 1.1), (1.9, 1.1), BLUE), ((1.6, 0.0), (1.9, 1.1), RED)):
        arrow(_a4, (_o[0] + _tail[0], _o[1] + _tail[1]), (_o[0] + _tip[0], _o[1] + _tip[1]), _c)
    arrow(_a4, _o, (_o[0] + 1.9, _o[1] + 1.1), GREEN)
    _a4.text(3.7, -0.62, r"$\vec{u}$", color=BLUE, fontsize=13)
    _a4.text(2.82, 0.3, r"$\vec{v}$", color=RED, fontsize=13)
    _a4.text(3.5, 0.45, r"$\vec{u} + \vec{v}$", color=GREEN, fontsize=13)

    mo.vstack(
        [
            mo.md(
                r"""
    ## I.1 &nbsp; Euclidean geometry

    **References:** Sasane 5.1

    **Space** = set of all $\underbrace{\textit{locations}}_{\footnotesize \mathclap{\text{points in space}}\rule[-0.35em]{0pt}{0pt}}$ $= \mathbb{E}^3$

    **Geometry** = study of the fundamental $\underbrace{\textit{structure of space}}_{\footnotesize \mathclap{\text{relations between its points}}\rule[-0.35em]{0pt}{0pt}}$

    Fundamental assumptions (axioms)

    **(i)** given points $p, q \in \mathbb{E}^3$, there exists a unique “vector” $\vec{u}$ from $p$ to $q$ &nbsp; (here a vector is defined as the “difference” between two points)

    $$
    \vec{u} := q - p \in \smash[b]{\underbrace{\mathbb{V}_p}_{\footnotesize \mathclap{\text{vectors from } p}}}
    $$
    """
            ),
            _f1,
            mo.md(
                r"""
    given $p \in \mathbb{E}^3$ and $\vec{u} \in \mathbb{V}_p$, there exists a unique “end point” $q \in \mathbb{E}^3$ such that

    $$
    \vec{u} = q - p \qquad \overset{\footnotesize \text{notation}}{\leadsto} \qquad q = p + \vec{u}
    $$

    Once we fix $p \in \mathbb{E}^3$, we get a well-defined identification

    $$
    \smash[b]{\underbrace{\mathbb{E}^3\vphantom{\mathbb{V}_p^3}}_{\footnotesize \text{points}}} \cong \smash[b]{\underbrace{\mathbb{V}_p^3}_{\footnotesize \text{vectors}}}
    $$

    **(ii)** given $p, q \in \mathbb{E}^3$ and $\vec{v} \in \mathbb{V}_p^3$, there exists a unique $\vec{v}\,' \in \mathbb{V}_q$ “congruent” to $\vec{v}$ &nbsp; (intuitively “same size and direction”)

    $$
    \overset{\footnotesize \text{notation}}{\leadsto} \qquad \vec{v}\,' = \vec{v} \in \mathbb{V}^3 \qquad (\text{identification between } \mathbb{V}_p^3 \text{ and } \mathbb{V}_q^3)
    $$
    """
            ),
            _f2,
            theorem(
                r"""
    Assumptions (i) and (ii) allow us to define

    $$
    {+} : \mathbb{V}^3 \times \mathbb{V}^3 \longrightarrow \mathbb{V}^3 \qquad (\text{addition of vectors})
    $$
    """,
                "Addition of vectors",
            ),
            mo.md(
                r"""
    **Proof.**

    <span class="chain">$\displaystyle \vec{u}, \vec{v} \in \mathbb{V}_p^3 \quad \Longrightarrow \quad \vec{u} + \vec{v} := \big( (p + \vec{u}) + \vec{v}\,' \big) - p$ $\displaystyle = (q + \vec{v}\,') - p = r - p$<span class="qed">$\square$</span></span>
    """
            ),
            _f3,
            mo.md(
                r"""
    **Remark.** We need extra assumptions to define

    $$
    \cdot : \mathbb{R} \times \mathbb{V}^3 \longrightarrow \mathbb{V}^3 \qquad (\text{scalar multiplication})
    $$

    idea: &nbsp; $a \in \mathbb{R}$, $\vec{u} \in \mathbb{V}^3$

    $$
    \begin{aligned}
    \text{if } \ a = n \in \mathbb{N} \qquad & \leadsto \qquad n \cdot \vec{u} = \underbrace{\vec{u} + \cdots + \vec{u}}_{\footnotesize n \text{ times}} \\[14pt]
    a = 0 \qquad & \leadsto \qquad 0 \cdot \vec{u} = \vec{0} \ \text{ such that } \ p + \vec{0} = p \\[4pt]
    a = -1 \qquad & \leadsto \qquad (-1) \cdot \vec{u} = \vec{v} \ \text{ such that } \ \vec{u} + \vec{v} = \vec{0} \\[10pt]
    a = 1/n \qquad & \leadsto \qquad \dfrac{1}{n} \cdot \vec{u} = \vec{v} \ \text{ such that } \ \vec{u} = n \cdot \vec{v} \\[4pt]
    & \phantom{\leadsto} \qquad (\text{here we need more than (i) and (ii)})
    \end{aligned}
    $$

    **(iii)** the space $\mathbb{V}^3$ forms a 3-dimensional vector space: &nbsp; $+ : \mathbb{V}^3 \times \mathbb{V}^3 \longrightarrow \mathbb{V}^3$ and $\cdot : \mathbb{R} \times \mathbb{V}^3 \longrightarrow \mathbb{V}^3$ well-defined with

    - associativity
    - commutativity
    - distributivity
    - zero vector
    - negative vectors
    - identity scalar

    The truly new assumptions are that $\cdot : \mathbb{R} \times \mathbb{V}^3 \longrightarrow \mathbb{V}^3$ is well-defined, and commutativity:

    - can stretch vectors by real scalars
    - sum is the diagonal of the parallelogram
    """
            ),
            _f4,
        ]
    )
    return


@app.cell(hide_code=True)
def _(Arc, BLUE, FULL, Figure, GREEN, GREY, ORANGE, RED, arrow, definition, mo, np):

    # Marginal sketches of the four measurements: distance, angle, triangle area, tetrahedron volume
    _fig = Figure(figsize=(FULL, 1.9), layout="constrained")
    _d, _t, _a, _v = _fig.subplots(1, 4)
    for _ax in (_d, _t, _a, _v):
        _ax.set_aspect("equal")
        _ax.axis("off")

    arrow(_d, (0, 0), (2.0, 0.5), GREEN)
    _d.plot(0, 0, "o", color="black", ms=4)
    _d.plot([0.05, 1.95], [-0.25, 0.25], color=GREEN, lw=0.9)
    for _x, _y in ((0.05, -0.25), (1.95, 0.25)):
        _d.plot([_x + 0.03, _x - 0.03], [_y - 0.12, _y + 0.12], color=GREEN, lw=0.9)
    _d.text(1.0, -0.4, "$d$", color=GREEN, fontsize=13, ha="center", va="top")
    _d.set_xlim(-0.3, 2.3)
    _d.set_ylim(-0.75, 0.8)

    arrow(_t, (0, 0), (2.0, 0.2), BLUE)
    arrow(_t, (0, 0), (0.8, 1.3), RED)
    _t.add_patch(Arc((0, 0), 1.2, 1.2, theta1=6, theta2=58, color=GREEN, lw=1.0))
    _t.text(0.72, 0.42, r"$\theta$", color=GREEN, fontsize=13)
    _t.plot(0, 0, "o", color="black", ms=4)
    _t.set_xlim(-0.3, 2.3)
    _t.set_ylim(-0.3, 1.5)

    _a.fill([0, 2.0, 0.6], [0, 0.3, 1.4], color=GREEN, alpha=0.2, lw=0)
    _a.plot([2.0, 0.6], [0.3, 1.4], "--", color=GREY, lw=1.0)
    arrow(_a, (0, 0), (2.0, 0.3), BLUE)
    arrow(_a, (0, 0), (0.6, 1.4), RED)
    _a.text(1.2, 1.1, "$A$", color=GREEN, fontsize=13)
    _a.plot(0, 0, "o", color="black", ms=4)
    _a.set_xlim(-0.3, 2.3)
    _a.set_ylim(-0.3, 1.6)

    _o, _u, _w, _z = np.array((0.0, 0.0)), np.array((1.7, -0.15)), np.array((0.7, 0.45)), np.array((0.15, 1.1))
    for _p, _q in ((_u, _w), (_w, _z), (_z, _u)):
        _v.plot([_p[0], _q[0]], [_p[1], _q[1]], "--", color=GREY, lw=1.0)
    for _tip, _c in ((_u, BLUE), (_w, RED), (_z, ORANGE)):
        arrow(_v, _o, _tip, _c)
    _v.text(1.15, 0.7, "$V$", color="black", fontsize=13)
    _v.plot(0, 0, "o", color="black", ms=4)
    _v.set_xlim(-0.3, 2.3)
    _v.set_ylim(-0.4, 1.5)

    mo.vstack(
        [
            mo.md(
                r"""
    **Remark.** In this construction we emphasize the distinction between points = locations and vectors = displacements &nbsp; (usually confused when studying multivariable calculus in $\mathbb{R}^3$)
    """
            ),
            definition(
                r"""
    An **affine space** is a triple $(\mathbb{A}, \mathbb{V}, -)$

    - $\mathbb{A}$ is a set (of locations)
    - $\mathbb{V}$ is a *vector space* (of displacements) &nbsp; (iii)
    - $- : \mathbb{A} \times \mathbb{A} \longrightarrow \mathbb{V}$, &nbsp; $(q, p) \longmapsto q - p$ &nbsp; is an assignment of a vector to each ordered pair of points

    satisfying:

    - $\forall\, p \in \mathbb{A},\ \forall\, \vec{u} \in \mathbb{V},\ \exists!\, q \in \mathbb{A}$ &nbsp; such that &nbsp; $q - p = \vec{u}$ &nbsp; (i)
    - $\forall\, p, q, r \in \mathbb{A}$, &nbsp; $(q - r) + (r - p) = q - p$ &nbsp; (ii)
    """,
                "Affine space",
            ),
            mo.md(
                r"""
    Affine spaces will give us the simplest mathematical model of spaces / spacetimes, but for now, we only have notions of locations and displacements, not of measurements.

    ### Euclidean inner product

    **(iv)** there exists a function $\langle\ ,\ \rangle : \mathbb{V} \times \mathbb{V} \longrightarrow \mathbb{R}$ such that

    - bilinear: &nbsp; $\langle a\vec{u} + b\vec{v}, \vec{w} \rangle = a \langle \vec{u}, \vec{w} \rangle + b \langle \vec{v}, \vec{w} \rangle$, &nbsp; $\langle \vec{u}, b\vec{v} + c\vec{w} \rangle = b \langle \vec{u}, \vec{v} \rangle + c \langle \vec{u}, \vec{w} \rangle$
    - symmetric: &nbsp; $\langle \vec{u}, \vec{v} \rangle = \langle \vec{v}, \vec{u} \rangle$
    - positive-definite: &nbsp; $\langle \vec{u}, \vec{u} \rangle \geq 0$ with $\langle \vec{u}, \vec{u} \rangle = 0$ if and only if $\vec{u} = \vec{0}$
    """
            ),
            definition(
                r"""
    The **Euclidean space** is a 3-dimensional affine space ($\dim \mathbb{V} = 3$)

    $$
    \mathbb{E}^3 = (\mathbb{A}, \mathbb{V}, -)
    $$

    together with a Euclidean inner product on $\mathbb{V}$

    $$
    \langle\ ,\ \rangle : \mathbb{V} \times \mathbb{V} \longrightarrow \mathbb{R}
    $$
    """,
                "Euclidean space",
            ),
            mo.md("Every geometric measurement comes from the inner product"),
            mo.Html('<div class="readout cases">' + mo.md(
                r"""
    | | |
    |:--|:--|
    | norms | $\lVert \vec{u} \rVert = \sqrt{\langle \vec{u}, \vec{u} \rangle}$ |
    | distances | $d(p, q) = \lVert q - p \rVert$ |
    | angles | $\theta(\vec{u}, \vec{v}) = \arccos\!\left( \dfrac{\langle \vec{u}, \vec{v} \rangle}{\lVert \vec{u} \rVert\, \lVert \vec{v} \rVert} \right)$ |
    | areas (triangle) | $A(\vec{u}, \vec{v}) = \dfrac{1}{2} \left[ \det \begin{pmatrix} \lVert \vec{u} \rVert^2 & \langle \vec{u}, \vec{v} \rangle \\ \langle \vec{u}, \vec{v} \rangle & \lVert \vec{v} \rVert^2 \end{pmatrix} \right]^{1/2}$ |
    | volumes (tetrahedron) | $V(\vec{u}, \vec{v}, \vec{w}) = \dfrac{1}{6} \left[ \det \begin{pmatrix} \lVert \vec{u} \rVert^2 & \langle \vec{u}, \vec{v} \rangle & \langle \vec{u}, \vec{w} \rangle \\ \langle \vec{u}, \vec{v} \rangle & \lVert \vec{v} \rVert^2 & \langle \vec{v}, \vec{w} \rangle \\ \langle \vec{u}, \vec{w} \rangle & \langle \vec{v}, \vec{w} \rangle & \lVert \vec{w} \rVert^2 \end{pmatrix} \right]^{1/2}$ |
    """
            ).text + '</div>'),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, HALF, arrow, blank, mo, theorem):
    _fig, _ax = blank(HALF, 3.0, (-1.3, 2.9), (-1.2, 2.3))
    _f = lambda x, y, z: (y - 0.5 * x, z - 0.45 * x)
    for _tip, _name, _off in (((2.0, 0, 0), r"$\vec{e}_1$", (2, -14)), ((0, 2.4, 0), r"$\vec{e}_2$", (4, -4)), ((0, 0, 2.0), r"$\vec{e}_3$", (6, -4))):
        arrow(_ax, (0, 0), _f(*_tip), "black", lw=1.0)
        _ax.annotate(_name, _f(*_tip), textcoords="offset points", xytext=_off, fontsize=13)
    _p = (1.2, 1.8, 1.5)
    for _a, _b in (((1.2, 0, 0), (1.2, 1.8, 0)), ((0, 1.8, 0), (1.2, 1.8, 0)), ((1.2, 1.8, 0), _p), ((0, 0, 1.5), _p)):
        _ax.plot(*zip(_f(*_a), _f(*_b)), "--", color=GREEN, lw=1.0)
    arrow(_ax, (0, 0), _f(*_p), BLUE)
    _ax.text(0.25, 0.65, "$p - o$", color=BLUE, fontsize=12, rotation=28)
    _ax.plot(*_f(*_p), "o", color="black", ms=4)
    _ax.annotate("$p$", _f(*_p), textcoords="offset points", xytext=(6, 2), fontsize=13)
    _ax.plot(0, 0, "o", color="black", ms=4)
    _ax.annotate("$o$", (0, 0), textcoords="offset points", xytext=(-14, 2), fontsize=13)
    for _q, _n, _off in (((1.2, 0, 0), "$x$", (-12, 2)), ((0, 1.8, 0), "$y$", (-4, 5)), ((0, 0, 1.5), "$z$", (-12, 2))):
        _ax.annotate(_n, _f(*_q), textcoords="offset points", xytext=_off, color=GREEN, fontsize=12)

    mo.vstack(
        [
            mo.md(
                r"""
    ### Cartesian coordinates

    No need to introduce an *origin* or *special coordinate axes*! But we can if we want to (brings us back to $\mathbb{R}^3$)
    """
            ),
            theorem(
                r"""
    Choosing $\underbrace{o}_{\footnotesize \mathclap{\text{origin}}\rule[-0.35em]{0pt}{0pt}} \in \mathbb{E}^3$ and $\vec{e}_1, \vec{e}_2, \vec{e}_3 \in \mathbb{V}$ such that

    $$
    \langle \vec{e}_i, \vec{e}_j \rangle = \delta_{ij} = \begin{cases} 1 & \text{if } i = j \\ 0 & \text{if } i \neq j \end{cases} \qquad (\text{orthonormal basis})
    $$

    we can define Cartesian coordinates

    $$
    x^i : \mathbb{E}^3 \longrightarrow \mathbb{R}, \qquad p \longmapsto x^i(p) = \langle \vec{e}_i, p - o \rangle
    $$

    and identify

    $$
    \mathbb{R}^3 \approx \mathbb{E}^3, \qquad (x, y, z) \longleftrightarrow p = o + x\vec{e}_1 + y\vec{e}_2 + z\vec{e}_3
    $$
    """,
                "Cartesian coordinates",
            ),
            _fig,
        ]
    )
    return


if __name__ == "__main__":
    app.run()
