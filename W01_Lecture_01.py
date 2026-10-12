import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 01 · Euclidean geometry", css_file="phy309.css")


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
    header("Lecture 01", "Week 01", "Lecture 01 · Euclidean geometry")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Course information": mo.md(r"""
    **PHY309 – Differential Geometry and General Relativity**

    | | |
    |:--|:--|
    | **Instructor** | Prof. Scarinci (cscarinci@dgist.ac.kr) |
    | **Office hours** | Thu 10:45 – 11:45 (E7 L10) |

    ## Course Description

    **DG** = modern mathematical theory of shapes in space and of space itself

    Generalizes Euclidean geometry allowing for “curved” shapes / spaces where different notions of “straight” lines are possible.

    **GR** = modern physical theory of gravitation

    Replaces Newton's theory by describing gravity not as a force acting across space and time, but as a manifestation of the curvature of spacetime.

    > “Spacetime tells matter how to move. Matter tells spacetime how to curve.”

    $$
    \text{Geometry of spacetime} \quad \longleftrightarrow \quad \text{Dynamics of matter}
    $$

    We will develop the mathematical language to understand this statement precisely!

    ## Schedule (tentative)

    | | | | |
    |:--|:--|:--|:--|
    | I | Flat geometry | L01 ~ L05 | Euclidean space and Galilean spacetime; Minkowski spacetime and special relativity |
    | II | Manifolds | L06 ~ L10 | The equivalence principle and local coordinates; Tangent vectors, vector fields and flows |
    | III | Metrics | L11 ~ L14 | The metric field and causality; Spheres, hyperbolic planes, Schwarzschild |
    | | *Midterm Week* | | |
    | IV | Connections | L15 ~ L19 | Covariant derivative and calculus on manifolds; Parallel transport and free falling observers |
    | V | Field equations | L20 ~ L24 | Riemann curvature and its contractions; Einstein equations and the Newtonian limit |
    | VI | Applications | L25 ~ L28 | Collapsing stars and black holes; Cosmology and the fate of the Universe |
    | | *Final Week* | | |

    ## Assessment

    6 take-home assignments with 3 oral defenses (one per pair)

    | | | |
    |:--|:--|:--|
    | A1 | 08.24 – 09.18 | D01 ~ W08 (Midterm Week) |
    | A2 | 09.07 – 10.02 | |
    | A3 | 09.28 – 10.23 | D02 ~ W13 – W14 |
    | A4 | 10.19 – 11.13 | |
    | A5 | 11.09 – 11.27 | D03 ~ W16 (Final Week) |
    | A6 | 11.23 – 12.04 | |

    Oral defense is *pass or fail*.

    ## Grading

    $$
    X = \sum_{i=1}^{6} X_i / 6 \ \in [0, 100], \qquad
    X_i = \begin{cases} \text{score of } A_i & \text{if pass} \\ 0 & \text{if fail} \end{cases}
    $$

    - pass: student must demonstrate the work in the assignment is really their own work
    - fail: student may retake each defense at most once and no more than twice overall

    | Letter | A+ | A0 | A− | B+ | B0 | B− | C+ | C0 | C− | D+ | D0 | D− | F |
    |:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | Minimum score | 97 | 94 | 90 | 85 | 80 | 75 | 70 | 65 | 60 | 57 | 54 | 50 | 0 |

    ## Course Policy

    - Missed deadline without justification $\Longrightarrow$ $A_i = 0$
    - Missed defense without justification $\Longrightarrow$ $A_i + A_{i+1} = 0$
    - Attendance $< 75\%$ without justification $\Longrightarrow$ F
    - Cheating (plagiarism, proxy attendance) $\Longrightarrow$ F

    ## Practicalities

    - Weekly exercises on LMS (ungraded)
    - Diagnostic test + review exercises + W01 already available
    - Solutions released the following week
    - Ask questions in class or during office hours!
    """)})
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, HALF, RED, arrow, blank, mo, theorem):
    def _pt(ax, xy, name, off=(-14, -4)):
        ax.plot(*xy, "o", color="black", ms=4)
        ax.annotate(name, xy, textcoords="offset points", xytext=off, fontsize=13)

    # (i) the displacement vector from p to q
    _f1, _a1 = blank(HALF, 1.6, (-0.4, 2.8), (-0.5, 1.0))
    arrow(_a1, (0, 0), (2, 0.6), GREEN)
    _a1.text(0.9, -0.3, r"$\vec{u} = q - p$", color=GREEN, fontsize=13)
    _pt(_a1, (0, 0), "$p$")
    _pt(_a1, (2, 0.6), "$q$", (6, -4))

    # (ii) a congruent copy of v at q
    _f2, _a2 = blank(HALF, 2.0, (-0.4, 2.9), (-0.3, 1.7))
    _a2.plot([0, 2], [0, 0.4], "--", color=GREY, lw=1.0)
    arrow(_a2, (0, 0), (0.3, 1.1), GREEN)
    arrow(_a2, (2, 0.4), (2.3, 1.5), GREEN)
    _a2.text(0.75, 1.35, r"$\vec{v} = \vec{v}\,'$", color=GREEN, fontsize=13)
    _pt(_a2, (0, 0), "$p$")
    _pt(_a2, (2, 0.4), "$q$", (6, -8))

    # addition of vectors
    _f3, _a3 = blank(HALF, 2.3, (-0.5, 3.0), (-0.4, 1.9))
    arrow(_a3, (0, 0), (1.9, 0.4), GREEN)
    arrow(_a3, (0, 0), (0.4, 1.1), GREEN)
    arrow(_a3, (1.9, 0.4), (2.3, 1.5), GREEN)
    arrow(_a3, (0, 0), (2.3, 1.5), BLUE)
    _a3.text(0.9, 0.05, r"$\vec{u}$", color=GREEN, fontsize=13)
    _a3.text(0.75, 1.0, r"$\vec{u} + \vec{v}$", color=BLUE, fontsize=13)
    _a3.text(2.25, 0.8, r"$\vec{v}\,'$", color=GREEN, fontsize=13)
    _a3.text(-0.15, 0.6, r"$\vec{v}$", color=GREEN, fontsize=13)
    _pt(_a3, (0, 0), "$p$")
    _pt(_a3, (1.9, 0.4), "$q$", (6, -10))
    _pt(_a3, (2.3, 1.5), "$r$", (6, 2))

    # scalar multiples and the parallelogram
    _f4, _a4 = blank(5.6, 2.1, (-1.3, 5.6), (-0.95, 1.85))
    arrow(_a4, (0, 0), (0.45, 0.6), GREEN)
    arrow(_a4, (0, 0), (1.15, 1.53), BLUE)
    arrow(_a4, (0, 0), (-0.5, -0.67), RED)
    _a4.text(0.1, 0.55, r"$\vec{v}$", color=GREEN, fontsize=13)
    _a4.text(1.25, 1.3, r"$\pi \vec{v}$", color=BLUE, fontsize=13)
    _a4.text(-0.45, -0.9, r"$-\vec{v}$", color=RED, fontsize=13)
    _o = (3.0, -0.3)
    for _tail, _tip in (((0, 0), (1.1, 0.35)), ((0, 0), (0.45, 1.0)), ((0.45, 1.0), (1.55, 1.35)), ((1.1, 0.35), (1.55, 1.35))):
        arrow(_a4, (_o[0] + _tail[0], _o[1] + _tail[1]), (_o[0] + _tip[0], _o[1] + _tip[1]), GREEN)
    arrow(_a4, _o, (_o[0] + 1.55, _o[1] + 1.35), BLUE)
    _a4.text(3.6, -0.6, r"$\vec{u}$", color=GREEN, fontsize=13)
    _a4.text(2.9, 0.4, r"$\vec{v}$", color=GREEN, fontsize=13)
    _a4.text(3.55, 0.95, r"$\vec{u} + \vec{v}$", color=BLUE, fontsize=13, rotation=41)

    mo.vstack(
        [
            mo.md(
                r"""
    ## I.1 &nbsp; Euclidean geometry

    **Space** = set of all *locations* (points in space) $= \mathbb{E}^3$

    **Geometry** = study of the fundamental *structure of space* (relations between its points)

    Fundamental assumptions (axioms)

    **(i)** given points $p, q \in \mathbb{E}^3$, there exists a unique “vector” $\vec{u}$ from $p$ to $q$ &nbsp; (here a vector is defined as the “difference” between two points)

    $$
    \vec{u} := q - p \in \mathbb{V}_p \qquad (\text{vectors from } p)
    $$
    """
            ),
            _f1,
            mo.md(
                r"""
    given $p \in \mathbb{E}^3$ and $\vec{u} \in \mathbb{V}_p$, there exists a unique “end point” $q \in \mathbb{E}^3$ such that

    $$
    \vec{u} = q - p \quad \overset{\text{notation}}{\leadsto} \quad q = p + \vec{u}
    $$

    Once we fix $p \in \mathbb{E}^3$, we get a well-defined identification

    $$
    \underbrace{\mathbb{E}^3}_{\text{points}} \cong \underbrace{\mathbb{V}_p^3}_{\text{vectors}}
    $$

    **(ii)** given $p, q \in \mathbb{E}^3$ and $\vec{v} \in \mathbb{V}_p^3$, there exists a unique $\vec{v}\,' \in \mathbb{V}_q$ “congruent” to $\vec{v}$ &nbsp; (intuitively “same size and direction”)

    $$
    \overset{\text{notation}}{\leadsto} \quad \vec{v}\,' = \vec{v} \in \mathbb{V}^3 \qquad (\text{identification between } \mathbb{V}_p^3 \text{ and } \mathbb{V}_q^3)
    $$
    """
            ),
            _f2,
            theorem(
                r"""
    Assumptions (i) and (ii) allow us to define

    $$
    {+} : \mathbb{V}^3 \times \mathbb{V}^3 \longrightarrow \mathbb{V}^3 \qquad \text{addition of vectors}
    $$
    """,
                "Addition of vectors",
            ),
            mo.md(
                r"""
    **Proof.** &nbsp; $\vec{u}, \vec{v} \in \mathbb{V}_p^3$ &nbsp; $\Longrightarrow$ &nbsp; $\vec{u} + \vec{v} := \big( \underbrace{\overbrace{(p + \vec{u})}^{q} + \vec{v}\,'}_{r} \big) - p$ &nbsp; $\square$
    """
            ),
            _f3,
            mo.md(
                r"""
    **Remark.** We need extra assumptions to define

    $$
    \cdot : \mathbb{R} \times \mathbb{V}^3 \longrightarrow \mathbb{V}^3 \qquad \text{scalar multiplication}
    $$

    idea: &nbsp; $a \in \mathbb{R}$, $\vec{u} \in \mathbb{V}^3$

    $$
    \begin{aligned}
    \text{if } \ a = n \in \mathbb{N} \quad &\leadsto \quad n \cdot \vec{u} = \underbrace{\vec{u} + \cdots + \vec{u}}_{n \text{ times}} \\[4pt]
    a = 0 \quad &\leadsto \quad 0 \cdot \vec{u} = \vec{0} \ \text{ such that } \ p + \vec{0} = p \\[4pt]
    a = -1 \quad &\leadsto \quad (-1) \cdot \vec{u} = \vec{v} \ \text{ such that } \ \vec{u} + \vec{v} = \vec{0} \\[4pt]
    a = 1/n \quad &\leadsto \quad \tfrac{1}{n} \cdot \vec{u} = \vec{v} \ \text{ such that } \ \vec{u} = n \cdot \vec{v} \qquad (\text{here we need more than (i) and (ii)})
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
def _(Arc, BLUE, FULL, GREEN, arrow, definition, mo):

    # Marginal sketches of the four measurements: distance, angle, triangle area, tetrahedron volume
    from matplotlib.figure import Figure as _Figure

    _fig = _Figure(figsize=(FULL, 1.9), layout="constrained")
    _d, _t, _a, _v = _fig.subplots(1, 4)
    for _ax in (_d, _t, _a, _v):
        _ax.set_aspect("equal")
        _ax.axis("off")

    _d.plot([0, 2.0], [0, 0.5], "o", color="black", ms=4)
    _d.plot([0, 2.0], [0, 0.5], color=GREEN, lw=1.4)
    _d.plot([0.05, 1.95], [-0.25, 0.25], color=GREEN, lw=0.9)
    for _x, _y in ((0.05, -0.25), (1.95, 0.25)):
        _d.plot([_x + 0.03, _x - 0.03], [_y - 0.12, _y + 0.12], color=GREEN, lw=0.9)
    _d.text(1.0, -0.4, "$d$", color=GREEN, fontsize=13, ha="center", va="top")
    _d.set_xlim(-0.3, 2.3)
    _d.set_ylim(-0.75, 0.8)

    arrow(_t, (0, 0), (2.0, 0.2), GREEN)
    arrow(_t, (0, 0), (0.8, 1.3), GREEN)
    _t.add_patch(Arc((0, 0), 1.2, 1.2, theta1=6, theta2=58, color=BLUE, lw=1.0))
    _t.text(0.72, 0.42, r"$\theta$", color=BLUE, fontsize=13)
    _t.plot(0, 0, "o", color="black", ms=4)
    _t.set_xlim(-0.3, 2.3)
    _t.set_ylim(-0.3, 1.5)

    _a.fill([0, 2.0, 0.6], [0, 0.3, 1.4], color=GREEN, alpha=0.2, lw=0)
    _a.plot([2.0, 0.6], [0.3, 1.4], "--", color=BLUE, lw=1.0)
    arrow(_a, (0, 0), (2.0, 0.3), GREEN)
    arrow(_a, (0, 0), (0.6, 1.4), GREEN)
    _a.text(1.2, 1.1, "$A$", color=GREEN, fontsize=13)
    _a.plot(0, 0, "o", color="black", ms=4)
    _a.set_xlim(-0.3, 2.3)
    _a.set_ylim(-0.3, 1.6)

    _o, _u, _w, _z = (0, 0), (2.0, -0.2), (1.2, 0.7), (0.9, 1.6)
    for _p, _q in ((_u, _w), (_w, _z), (_u, _z)):
        _v.plot([_p[0], _q[0]], [_p[1], _q[1]], "--", color=BLUE, lw=1.0)
    for _tip in (_u, _w, _z):
        arrow(_v, _o, _tip, GREEN)
    _v.text(1.45, 0.95, "$V$", color=GREEN, fontsize=13)
    _v.plot(0, 0, "o", color="black", ms=4)
    _v.set_xlim(-0.3, 2.3)
    _v.set_ylim(-0.5, 1.9)

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

    together with an Euclidean inner product on $\mathbb{V}$

    $$
    \langle\ ,\ \rangle : \mathbb{V} \times \mathbb{V} \longrightarrow \mathbb{R}
    $$
    """,
                "Euclidean space",
            ),
            mo.md(
                r"""
    Every geometric measurement comes from the inner product

    | | |
    |:--|:--|
    | norms | $\lVert \vec{u} \rVert = \sqrt{\langle \vec{u}, \vec{u} \rangle}$ |
    | distances | $d(p, q) = \lVert q - p \rVert$ |
    | angles | $\theta(\vec{u}, \vec{v}) = \arccos\!\left( \dfrac{\langle \vec{u}, \vec{v} \rangle}{\lVert \vec{u} \rVert\, \lVert \vec{v} \rVert} \right)$ |
    | areas (triangle) | $A(\vec{u}, \vec{v}) = \dfrac{1}{2} \left[ \det \begin{pmatrix} \lVert \vec{u} \rVert^2 & \langle \vec{u}, \vec{v} \rangle \\ \langle \vec{u}, \vec{v} \rangle & \lVert \vec{v} \rVert^2 \end{pmatrix} \right]^{1/2}$ |
    | volumes (tetrahedron) | $V(\vec{u}, \vec{v}, \vec{w}) = \dfrac{1}{6} \left[ \det \begin{pmatrix} \lVert \vec{u} \rVert^2 & \langle \vec{u}, \vec{v} \rangle & \langle \vec{u}, \vec{w} \rangle \\ \langle \vec{u}, \vec{v} \rangle & \lVert \vec{v} \rVert^2 & \langle \vec{v}, \vec{w} \rangle \\ \langle \vec{u}, \vec{w} \rangle & \langle \vec{v}, \vec{w} \rangle & \lVert \vec{w} \rVert^2 \end{pmatrix} \right]^{1/2}$ |
    """
            ),
            _fig,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    nu = mo.ui.slider(0.5, 3, 0.1, value=2, label=r"$\lVert \vec{u} \rVert$", show_value=True)
    nv = mo.ui.slider(0.5, 3, 0.1, value=1.5, label=r"$\lVert \vec{v} \rVert$", show_value=True)
    ip = mo.ui.slider(-1, 1, 0.05, value=0.5, label=r"$\langle \vec{u}, \vec{v} \rangle \,/\, \lVert \vec{u} \rVert \lVert \vec{v} \rVert$", show_value=True)
    return ip, nu, nv


@app.cell(hide_code=True)
def _(BLUE, GREEN, arrow, blank, ip, math, mo, nu, nv, table):
    _a, _b, _c = nu.value, nv.value, ip.value
    _g = _a * _b * _c
    _th = math.acos(_c)
    _area = 0.5 * math.sqrt(max(_a**2 * _b**2 - _g**2, 0))  # the max only guards round-off: cos(theta) is in [-1, 1]
    _u, _v = (_a, 0), (_b * math.cos(_th), _b * math.sin(_th))

    _fig, _ax = blank(4.6, 3.0, (-3.3, 3.6), (-0.4, 3.3))
    _ax.fill([0, _u[0], _v[0]], [0, _u[1], _v[1]], color=GREEN, alpha=0.2, lw=0)
    _ax.plot([_u[0], _v[0]], [_u[1], _v[1]], "--", color=BLUE, lw=1.0)
    arrow(_ax, (0, 0), _u, GREEN, r"$\vec{u}$", at_tip=True)
    arrow(_ax, (0, 0), _v, GREEN, r"$\vec{v}$", at_tip=True)

    mo.vstack(
        [
            mo.hstack([nu, nv, ip], justify="start", gap=2, wrap=True),
            table(
                [
                    (r"$\langle \vec{u}, \vec{v} \rangle$", rf"${_g:.3f}$"),
                    (r"$\theta(\vec{u}, \vec{v})$", rf"${_th:.3f} \ \text{{rad}} = {math.degrees(_th):.1f}^\circ$"),
                    (r"$A(\vec{u}, \vec{v})$", rf"${_area:.3f}$"),
                ]
            ),
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
    for _q, _n in (((1.2, 0, 0), "$x$"), ((0, 1.8, 0), "$y$"), ((0, 0, 1.5), "$z$")):
        _ax.annotate(_n, _f(*_q), textcoords="offset points", xytext=(-12, 2), color=GREEN, fontsize=12)

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
    Choosing $o \in \mathbb{E}^3$ (origin) and $\vec{e}_1, \vec{e}_2, \vec{e}_3 \in \mathbb{V}$ such that

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
            mo.md(
                r"""
    ## Summary

    - Euclidean space $\mathbb{E}^3$ = affine space $(\mathbb{A}, \mathbb{V}, -)$ (points and displacements, no origin) + Euclidean inner product on $\mathbb{V}$ (measurements)
    - every length, distance, angle, area and volume is computed from $\langle\ ,\ \rangle$
    - an origin and an orthonormal basis are a *choice*; they identify $\mathbb{E}^3$ with $\mathbb{R}^3$

    **Next:** Galilean spacetime, the geometry behind Newtonian mechanics
    """
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
