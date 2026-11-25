import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 1 · Euclidean geometry", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import sys

    import marimo as mo
    import numpy as np

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return lk, mo, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(1, "Euclidean geometry")
    return


@app.cell(hide_code=True)
def _(lk, np):
    # Helpers of this lecture: the six sketches, in the shared sketch style (lk.sk)
    sk = lk.sk
    K = "#000000"

    def displacement_sketch():
        # axiom (i): the vector u = q - p from p to q
        fig, ax = sk.sketch((-0.6, 3.0), (-0.6, 1.1))
        sk.maps(ax, (0, 0), (2.0, 0.6), color=lk.GREEN)
        sk.dot(ax, (0, 0), r"$p$", at=(-0.12, 0.0), ha="right", va="center")
        sk.dot(ax, (2.0, 0.6), r"$q$", at=(0.12, 0.0), ha="left", va="center")
        sk.label(ax, (1.15, 0.12), r"$\vec u=q-p$", lk.GREEN, ha="left", va="top")
        return fig

    def congruent_sketch():
        # axiom (ii): v at p and its congruent copy v' at q
        fig, ax = sk.sketch((-0.6, 3.0), (-0.4, 1.9))
        ax.plot([0, 2.0], [0, 0.4], "--", color=lk.GREY, lw=1.0)
        sk.maps(ax, (0, 0), (0.3, 1.1), color=lk.GREEN)
        sk.maps(ax, (2.0, 0.4), (2.3, 1.5), color=lk.GREEN)
        sk.dot(ax, (0, 0), r"$p$", at=(-0.12, 0.0), ha="right", va="center")
        sk.dot(ax, (2.0, 0.4), r"$q$", at=(0.12, -0.05), ha="left", va="center")
        sk.label(ax, (1.3, 1.45), r"$\vec v=\vec v\,'$", lk.GREEN, va="bottom")
        return fig

    def addition_sketch():
        # u from p to q, v at p, v' at q ending at r, and u + v from p to r
        fig, ax = sk.sketch((-0.6, 3.0), (-0.6, 2.0))
        p, q, r = (0, 0), (1.9, 0.4), (2.3, 1.5)
        sk.maps(ax, p, q, color=lk.BLUE)
        sk.maps(ax, p, (0.4, 1.1), color=lk.RED)
        sk.maps(ax, q, r, color=lk.RED)
        sk.maps(ax, p, r, color=lk.GREEN)
        sk.label(ax, (1.0, 0.1), r"$\vec u$", lk.BLUE, va="top")
        sk.label(ax, (0.12, 0.6), r"$\vec v$", lk.RED, ha="right")
        sk.label(ax, (2.2, 0.85), r"$\vec v\,'$", lk.RED, ha="left")
        sk.label(ax, (1.0, 0.95), r"$\vec u+\vec v$", lk.GREEN, ha="right", va="bottom")
        sk.dot(ax, p, r"$p$", at=(-0.12, 0.0), ha="right", va="center")
        sk.dot(ax, q, r"$q$", at=(0.12, -0.05), ha="left", va="center")
        sk.dot(ax, r, r"$r$", at=(0.1, 0.05), ha="left", va="bottom")
        return fig

    def stretch_sketch():
        # v, pi v and -v on one line; the parallelogram of u and v with its diagonal u + v
        fig, ax = sk.sketch((-1.4, 6.6), (-0.95, 1.9))
        sk.maps(ax, (0, 0), (1.15, 1.53), color=lk.GREEN)
        sk.maps(ax, (0, 0), (-0.5, -0.67), color=lk.ORANGE)
        sk.maps(ax, (0, 0), (0.45, 0.6), color=lk.RED)
        sk.dot(ax, (0, 0))
        sk.label(ax, (0.12, 0.42), r"$\vec v$", lk.RED, ha="right", va="bottom")
        sk.label(ax, (1.25, 1.35), r"$\pi\vec v$", lk.GREEN, ha="left")
        sk.label(ax, (-0.35, -0.8), r"$-\vec v$", lk.ORANGE, ha="left", va="top")
        o = np.array([3.0, -0.3])
        u, v = np.array([2.6, 0.0]), np.array([0.5, 1.4])
        for a, b, c in ((o, o + u, lk.BLUE), (o, o + v, lk.RED), (o + v, o + u + v, lk.BLUE), (o + u, o + u + v, lk.RED), (o, o + u + v, lk.GREEN)):
            sk.maps(ax, tuple(a), tuple(b), color=c)
        sk.dot(ax, tuple(o))
        sk.label(ax, tuple(o + 0.5 * u + (0, -0.15)), r"$\vec u$", lk.BLUE, va="top")
        sk.label(ax, tuple(o + 0.5 * v + (-0.12, 0)), r"$\vec v$", lk.RED, ha="right")
        sk.label(ax, tuple(o + 0.38 * (u + v) + (0.15, -0.1)), r"$\vec u+\vec v$", lk.GREEN, ha="left", va="top")
        return fig

    def measures_sketch():
        # a distance, an angle, a triangle area and a tetrahedron volume, side by side
        fig, ax = sk.sketch((-0.3, 11.0), (-0.8, 1.6))
        # distance
        sk.maps(ax, (0, 0), (2.0, 0.5), color=lk.GREEN)
        sk.dot(ax, (0, 0))
        ax.plot([0.08, 2.03], [-0.25, 0.24], color=lk.GREEN, lw=0.9)
        for x, y in ((0.08, -0.25), (2.03, 0.24)):
            ax.plot([x + 0.03, x - 0.03], [y - 0.12, y + 0.12], color=lk.GREEN, lw=0.9)
        sk.label(ax, (1.1, -0.2), r"$d$", lk.GREEN, va="top")
        # angle
        o = np.array([3.0, 0.0])
        sk.maps(ax, tuple(o), tuple(o + (2.0, 0.2)), color=lk.BLUE)
        sk.maps(ax, tuple(o), tuple(o + (0.8, 1.3)), color=lk.RED)
        t = np.radians(np.linspace(6, 58, 30))
        ax.plot(o[0] + 0.6 * np.cos(t), o[1] + 0.6 * np.sin(t), color=lk.GREEN, lw=1.0)
        sk.label(ax, tuple(o + (0.72, 0.38)), r"$\theta$", lk.GREEN, ha="left")
        sk.dot(ax, tuple(o))
        # area
        o = np.array([6.0, 0.0])
        ax.fill(o[0] + np.array([0, 2.0, 0.6]), o[1] + np.array([0, 0.3, 1.4]), color=lk.GREEN, alpha=0.2, lw=0)
        ax.plot(o[0] + np.array([2.0, 0.6]), o[1] + np.array([0.3, 1.4]), "--", color=lk.GREY, lw=1.0)
        sk.maps(ax, tuple(o), tuple(o + (2.0, 0.3)), color=lk.BLUE)
        sk.maps(ax, tuple(o), tuple(o + (0.6, 1.4)), color=lk.RED)
        sk.label(ax, tuple(o + (1.45, 1.0)), r"$A$", lk.GREEN, ha="left")
        sk.dot(ax, tuple(o))
        # volume
        o = np.array([9.0, 0.0])
        u, w, z = np.array((1.7, -0.15)), np.array((0.7, 0.45)), np.array((0.15, 1.1))
        for a, b in ((u, w), (w, z), (z, u)):
            ax.plot(o[0] + np.array([a[0], b[0]]), o[1] + np.array([a[1], b[1]]), "--", color=lk.GREY, lw=1.0)
        for tip, c in ((u, lk.BLUE), (w, lk.RED), (z, lk.ORANGE)):
            sk.maps(ax, tuple(o), tuple(o + tip), color=c)
        sk.label(ax, tuple(o + (1.15, 0.7)), r"$V$", ha="left")
        sk.dot(ax, tuple(o))
        return fig

    def coordinates_sketch():
        # origin o, the orthonormal basis e1, e2, e3, an event p, p - o and the coordinates x, y, z
        fig, ax = sk.sketch((-1.5, 2.9), (-1.3, 2.4))

        def f(x, y, z):
            return (y - 0.5 * x, z - 0.45 * x)

        for tip, name, at in (((2.0, 0, 0), r"$\vec e_1$", dict(ha="right", va="top")), ((0, 2.4, 0), r"$\vec e_2$", dict(ha="left", va="center")), ((0, 0, 2.0), r"$\vec e_3$", dict(va="bottom"))):
            sk.maps(ax, (0, 0), f(*tip), color=K)
            sk.label(ax, f(*[1.06 * c for c in tip]), name, **at)
        p = (1.2, 1.8, 1.5)
        for a, b in (((1.2, 0, 0), (1.2, 1.8, 0)), ((0, 1.8, 0), (1.2, 1.8, 0)), ((1.2, 1.8, 0), p), ((0, 0, 1.5), p)):
            ax.plot(*zip(f(*a), f(*b)), "--", color=lk.GREEN, lw=1.0)
        sk.maps(ax, (0, 0), f(*p), color=lk.RED)
        sk.label(ax, (0.3, 0.62), r"$p-o$", lk.RED, ha="right", va="bottom")
        sk.dot(ax, f(*p), r"$p$", at=(0.12, 0.05), ha="left", va="bottom")
        sk.dot(ax, (0, 0), r"$o$", at=(-0.12, 0.06), ha="right", va="bottom")
        sk.label(ax, (-0.72, -0.48), r"$x$", lk.GREEN, ha="right", va="bottom")
        sk.label(ax, f(0, 1.8, 0.12), r"$y$", lk.GREEN, va="bottom")
        sk.label(ax, f(0, -0.12, 1.5), r"$z$", lk.GREEN, ha="right", va="center")
        return fig

    return addition_sketch, congruent_sketch, coordinates_sketch, displacement_sketch, measures_sketch, stretch_sketch


@app.cell(hide_code=True)
def _(lk):
    # references
    lk.references("Sasane 5.1")
    return


@app.cell(hide_code=True)
def _(lk):
    lk.section("Euclidean geometry")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Euclidean space
    # space and geometry
    lk.prose(
        lk.aside(r"Space $=$ set of all <span class='lk-mark'>locations</span> $=\mathbb E^3$", "locations: points in space"),
        lk.aside(
            r"Geometry $=$ study of the fundamental <span class='lk-mark'>structure of space</span>",
            "structure of space: relations between its points",
        ),
    )
    return


@app.cell(hide_code=True)
def _(displacement_sketch, lk):
    # module: Euclidean space
    # axiom (i): vectors as differences of points
    lk.prose(
        r"**Fundamental assumptions** (axioms)",
        lk.aside(
            r"i) &nbsp; given points $p,q\in\mathbb E^3$, there exists a unique <span class='lk-mark'>“vector” $\vec u$</span> from $p$ to $q$",
            "here a vector is defined as<br>the “difference” between two points",
        ),
        lk.aside(r"$$\vec u:=q-p\in\mk{\mathbb V_p}$$", r"$\mathbb V_p$ = vectors from $p$"),
        lk.figure(displacement_sketch()),
        r"> given $p\in\mathbb E^3$ and $\vec u\in\mathbb V_p$, there exists a unique “end point” $q\in\mathbb E^3$ such that",
        r"$$\vec u=q-p\quad\overset{\text{notation}}{\leadsto}\quad q=p+\vec u$$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Euclidean space
    # points and vectors from p
    lk.prose(
        r"$\leadsto$ &nbsp; once we fix $p\in\mathbb E^3$, we get a well-defined identification",
        r"$$\underbrace{\mathbb E^3\vphantom{\mathbb V_p^3}}_{\text{points}}\cong\underbrace{\mathbb V_p^3}_{\text{vectors}}$$",
    )
    return


@app.cell(hide_code=True)
def _(congruent_sketch, lk):
    # module: Euclidean space
    # axiom (ii): congruent vectors
    lk.prose(
        lk.aside(
            r"ii) &nbsp; given $p,q\in\mathbb E^3$ and $\vec v\in\mathbb V_p^3$, there exists a unique $\vec v\,'\in\mathbb V_q$ <span class='lk-mark'>“congruent”</span> to $\vec v$",
            "intuitively “same size and direction”",
        ),
        lk.aside(
            r"> $\overset{\text{notation}}{\leadsto}$ &nbsp; $\vec v\,'=\vec v\in\mathbb V^3$",
            r"identification between $\mathbb V_p^3$ and $\mathbb V_q^3$",
        ),
        lk.figure(congruent_sketch()),
    )
    return


@app.cell(hide_code=True)
def _(addition_sketch, lk):
    # module: vector space
    # theorem: addition of vectors
    lk.theorem(
        [
            r"Assumptions (i) and (ii) allow us to define",
            r"$$+:\mathbb V^3\times\mathbb V^3\longrightarrow\mathbb V^3\qquad(\text{addition of vectors})$$",
            lk.figure(addition_sketch()),
        ],
        label="thm-addition",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: vector space
    # proof
    lk.proof(
        r"$\vec u,\vec v\in\mathbb V_p^3$ &nbsp; $\Longrightarrow$ &nbsp; $\vec u+\vec v:=\big(\underbrace{\overbrace{(p+\vec u)}^{q}+\vec v\,'}_{r}\big)-p$"
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: vector space
    # remark: scalar multiplication needs more
    lk.remark(
        [
            r"We need extra assumptions to define",
            r"$$\cdot:\mathbb R\times\mathbb V^3\longrightarrow\mathbb V^3\qquad(\text{scalar multiplication})$$",
            r"idea: &nbsp; $a\in\mathbb R$, &nbsp; $\vec u\in\mathbb V^3$",
            lk.aside(
                r"$$\begin{aligned}\text{if }a=n\in\mathbb N\quad&\leadsto\quad n\cdot\vec u=\underbrace{\vec u+\dots+\vec u}_{n\text{ times}}\\[0.3em]a=0\quad&\leadsto\quad0\cdot\vec u=\vec0\ \text{ such that }\ p+\vec0=p\\[0.3em]a=-1\quad&\leadsto\quad(-1)\cdot\vec u=\vec v\ \text{ such that }\ \vec u+\vec v=\vec0\\[0.3em]a=1/n\quad&\leadsto\quad\tfrac1n\cdot\vec u=\vec v\ \text{ such that }\ \mk{\vec u=n\cdot\vec v}\end{aligned}$$",
                "here we need more than (i) and (ii)",
                at=4,
                rows=4,
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk, stretch_sketch):
    # module: vector space
    # axiom (iii): a vector space
    lk.prose(
        r"iii) &nbsp; the space $\mathbb V^3$ forms a 3-dimensional vector space:",
        lk.aside(
            r"> $+:\mathbb V^3\times\mathbb V^3\longrightarrow\mathbb V^3$ &nbsp; and &nbsp; <span class='lk-mark'>$\cdot:\mathbb R\times\mathbb V^3\longrightarrow\mathbb V^3$ well-defined</span> &nbsp; with",
            "the truly new assumptions:<br>– can stretch vectors by real scalars<br>– sum is the diagonal of the parallelogram",
        ),
        r"""
        > > • &nbsp; associativity

        > > • &nbsp; <span class='lk-mark'>commutativity</span>

        > > • &nbsp; distributivity

        > > • &nbsp; zero vector

        > > • &nbsp; negative vectors

        > > • &nbsp; identity scalar
        """,
        lk.figure(stretch_sketch()),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: affine space
    # remark: points and vectors
    lk.remark(
        r"""
        In this construction we emphasize the distinction between

        > points $=$ locations &nbsp; and &nbsp; vectors $=$ displacements

        > $\leadsto$ &nbsp; usually confused when studying multivariable calculus in $\mathbb R^3$ …
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: affine space
    # definition: affine space
    lk.definition(
        r"""
        An **affine space** is a triple $(\mathbb A,\mathbb V,-)$

        > $\mathbb A$ is a set (of locations)

        > $\mathbb V$ is a vector space (of displacements) &nbsp;&nbsp; (iii)

        > $-:\mathbb A\times\mathbb A\longrightarrow\mathbb V$, &nbsp; $(q,p)\longmapsto q-p$ &nbsp; assigns a vector to each ordered pair of points

        satisfying:

        > • &nbsp; $\forall\,p\in\mathbb A$, $\forall\,\vec u\in\mathbb V$, $\exists!\,q\in\mathbb A$ &nbsp; such that &nbsp; $q-p=\vec u$ &nbsp;&nbsp; (i)

        > • &nbsp; $\forall\,p,q,r\in\mathbb A$, &nbsp; $(q-r)+(r-p)=q-p$ &nbsp;&nbsp; (ii)
        """,
        title="Affine space",
        label="def-affine",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: affine space
    # what affine spaces give, and what they don't
    lk.prose(
        r"""
        $\leadsto$ &nbsp; affine spaces will give us the simplest mathematical model of spaces / spacetimes

        $\leadsto$ &nbsp; but for now, we only have locations and displacements, not measurements
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Euclidean inner product
    # axiom (iv): the Euclidean inner product
    lk.prose(
        r"**Euclidean inner product**",
        r"iv) &nbsp; there exists a function &nbsp; $\langle\ ,\ \rangle:\mathbb V\times\mathbb V\longrightarrow\mathbb R$ &nbsp; such that",
        r"$$\begin{array}{ll}\text{bilinear}&\langle a\vec u+b\vec v,\vec w\rangle=a\langle\vec u,\vec w\rangle+b\langle\vec v,\vec w\rangle\\&\langle\vec u,b\vec v+c\vec w\rangle=b\langle\vec u,\vec v\rangle+c\langle\vec u,\vec w\rangle\\[0.5em]\text{symmetric}&\langle\vec u,\vec v\rangle=\langle\vec v,\vec u\rangle\\[0.5em]\text{positive-definite}\quad&\langle\vec u,\vec u\rangle\geq0\ \text{ with }\ \langle\vec u,\vec u\rangle=0\ \text{ iff }\ \vec u=\vec0\end{array}$$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Euclidean inner product
    # definition: Euclidean space
    lk.definition(
        [
            lk.aside(r"The **Euclidean space** is a <span class='lk-mark'>3-dimensional</span> affine space", r"3-dimensional: $\dim\mathbb V=3$"),
            r"$$\mathbb E^3=(\mathbb A,\mathbb V,-)$$",
            r"together with a Euclidean inner product on $\mathbb V$",
            r"$$\langle\ ,\ \rangle:\mathbb V\times\mathbb V\longrightarrow\mathbb R$$",
        ],
        label="def-euclidean",
    )
    return


@app.cell(hide_code=True)
def _(lk, measures_sketch):
    # module: Euclidean inner product
    # measurements
    lk.prose(
        r"$\leadsto$ &nbsp; every geometric measurement comes from the inner product",
        r"$$\begin{array}{ll}\text{norms}&\lVert\vec u\rVert=\sqrt{\langle\vec u,\vec u\rangle}\\[0.5em]\text{distances}&d(p,q)=\lVert q-p\rVert\\[0.5em]\text{angles}&\theta(\vec u,\vec v)=\arccos\Big(\dfrac{\langle\vec u,\vec v\rangle}{\lVert\vec u\rVert\,\lVert\vec v\rVert}\Big)\\[1em]\text{areas}&A(\vec u,\vec v)=\dfrac12\left[\det\begin{pmatrix}\lVert\vec u\rVert^2&\langle\vec u,\vec v\rangle\\\langle\vec u,\vec v\rangle&\lVert\vec v\rVert^2\end{pmatrix}\right]^{1/2}\\[1.2em]\text{volumes}\quad&V(\vec u,\vec v,\vec w)=\dfrac16\left[\det\begin{pmatrix}\lVert\vec u\rVert^2&\langle\vec u,\vec v\rangle&\langle\vec u,\vec w\rangle\\\langle\vec u,\vec v\rangle&\lVert\vec v\rVert^2&\langle\vec v,\vec w\rangle\\\langle\vec u,\vec w\rangle&\langle\vec v,\vec w\rangle&\lVert\vec w\rVert^2\end{pmatrix}\right]^{1/2}\end{array}$$",
        lk.figure(measures_sketch()),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Cartesian coordinates
    # no origin needed
    lk.prose(
        lk.aside(
            r"$\leadsto$ &nbsp; no need to introduce an <span class='lk-mark'>origin</span> or <span class='lk-mark'>special coordinate axes</span>!",
            r"but we can if we want to!<br>$\leadsto$ brings us back to $\mathbb R^3$",
        )
    )
    return


@app.cell(hide_code=True)
def _(coordinates_sketch, lk):
    # module: Cartesian coordinates
    # theorem: Cartesian coordinates
    lk.theorem(
        [
            lk.aside(r"Choosing &nbsp; $\mk{o}\in\mathbb E^3$ &nbsp; and &nbsp; $\vec e_1,\vec e_2,\vec e_3\in\mathbb V$ &nbsp; such that", r"$o$ = origin"),
            lk.aside(
                r"$$\langle\vec e_i,\vec e_j\rangle=\delta_{ij}=\begin{cases}1&\text{if }i=j\\0&\text{if }i\neq j\end{cases}$$",
                "orthonormal basis",
            ),
            r"we can define Cartesian coordinates",
            r"$$x^i:\mathbb E^3\longrightarrow\mathbb R,\qquad p\longmapsto x^i(p)=\langle\vec e_i,p-o\rangle$$",
            r"and identify &nbsp; $\mathbb R^3\approx\mathbb E^3$",
            r"$$(x,y,z)\longleftrightarrow p=o+x\,\vec e_1+y\,\vec e_2+z\,\vec e_3$$",
            lk.figure(coordinates_sketch()),
        ],
        label="thm-euclidean-coordinates",
    )
    return


if __name__ == "__main__":
    app.run()
