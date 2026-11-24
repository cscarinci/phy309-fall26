import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 2 · Galilean geometry", css_file="lecturekit/style.css")


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
    lk.lecture(2, "Galilean geometry")
    return


@app.cell(hide_code=True)
def _(lk, np):
    # Helpers of this lecture: the 2D sketches in the shared sketch style, and the four 3D figures (relative
    # velocity, constant force, Newtonian gravity, addition of relative velocities), coordinates (x^1, x^2, time);
    # gamma red and sigma blue
    sk = lk.sk
    K = "#000000"
    O3 = (0.0, 0.0, 0.0)
    PLUM = "#7d6596"

    def causal_sketch():
        # p with a future, a spatial (simultaneous) and a past vector, and tau taking them to > 0, 0, < 0
        fig, ax = sk.sketch((-0.6, 7.6), (-1.1, 2.0))
        sk.maps(ax, (0, 0), (0.55, 1.45), color=lk.BLUE)
        sk.maps(ax, (0, 0), (1.35, 0), color=lk.GREY)
        sk.maps(ax, (0, 0), (0.85, -0.55), color=lk.RED)
        for q in ((0.55, 1.45), (1.35, 0), (0.85, -0.55)):
            sk.dot(ax, q)
        sk.dot(ax, (0, 0), r"$p$", at=(-0.15, -0.05), ha="right", va="center")
        sk.label(ax, (0.55, 1.62), "future", lk.BLUE, va="bottom")
        sk.label(ax, (1.5, 0.0), "spatial / simultaneous", lk.GREY, ha="left", va="center")
        sk.label(ax, (0.85, -0.72), "past", lk.RED, va="top")
        sk.maps(ax, (5.3, 0.75), (6.2, 0.75), r"$\tau$", bend=-0.3)
        ax.plot([6.85, 6.85], [-0.95, 1.75], color=K, lw=sk.LW)
        for y, c, n in ((1.45, lk.BLUE, r"$>0$"), (0.0, lk.GREY, r"$0$"), (-0.55, lk.RED, r"$<0$")):
            ax.plot(6.85, y, "o", color=c, ms=4)
            sk.label(ax, (7.05, y), n, ha="left", va="center")
        return fig

    def frame_sketch():
        # origin o, the inertial frame e0 (time, up), e_i, e_j, an event p and its coordinates t, x^i, x^j
        fig, ax = sk.sketch((-1.6, 2.8), (-1.3, 2.4))

        def f(x, y, z):
            return (y - 0.5 * x, z - 0.45 * x)

        sk.maps(ax, (0, 0), f(0, 0, 2.0), color=lk.RED)
        sk.maps(ax, (0, 0), f(2.0, 0, 0), color=lk.BLUE)
        sk.maps(ax, (0, 0), f(0, 2.2, 0), color=lk.BLUE)
        sk.label(ax, f(0, 0, 2.12), r"$\vec e_0$", lk.RED, va="bottom")
        sk.label(ax, f(2.12, 0, 0), r"$\vec e_i$", lk.BLUE, ha="right", va="top")
        sk.label(ax, f(0, 2.3, 0), r"$\vec e_j$", lk.BLUE, ha="left", va="center")
        p = (1.0, 1.4, 1.5)
        for a, b in (((1.0, 0, 0), (1.0, 1.4, 0)), ((0, 1.4, 0), (1.0, 1.4, 0)), ((1.0, 1.4, 0), p), ((0, 0, 1.5), p)):
            ax.plot(*zip(f(*a), f(*b)), "--", color=lk.GREEN, lw=1.0)
        sk.maps(ax, (0, 0), f(*p), color=lk.GREEN)
        sk.dot(ax, f(*p), r"$p$", at=(0.12, 0.05), ha="left", va="bottom")
        sk.dot(ax, (0, 0), r"$o$", at=(-0.12, 0.06), ha="right", va="bottom")
        sk.label(ax, (-0.62, -0.38), r"$x^i$", lk.GREEN, ha="right", va="bottom")
        sk.label(ax, f(0, 1.4, 0.12), r"$x^j$", lk.GREEN, va="bottom")
        sk.label(ax, f(0, -0.12, 1.5), r"$t$", lk.GREEN, ha="right", va="center")
        return fig

    def particle_sketch():
        # gamma takes s, s + epsilon on R to events of a curve in G^4, gamma'(s) at gamma(s)
        fig, ax = sk.sketch((-0.4, 7.6), (-0.6, 2.6))
        ax.plot([0.0, 2.6], [0.3, 0.75], color=lk.BLUE, lw=sk.LW)
        sk.label(ax, (-0.1, 0.25), r"$\mathbb{R}$", lk.BLUE, ha="right", va="center")
        sa, sb = np.array([0.7, 0.42]), np.array([1.9, 0.63])
        sk.maps(ax, tuple(sa), (1.4, 0.54), color=lk.RED)
        sk.dot(ax, tuple(sa), r"$s$", at=(-0.05, 0.12), ha="right", va="bottom")
        sk.dot(ax, tuple(sb), r"$s+\varepsilon$", at=(0.08, -0.12), ha="left", va="top")
        sk.label(ax, (1.25, 0.72), r"$\vec e_1$", lk.RED, va="bottom")
        sk.maps(ax, (3.0, 0.9), (3.9, 0.9), r"$\gamma$", bend=-0.3)
        t = np.linspace(0, 1, 121)
        x = 4.4 + 2.4 * t
        y = -0.35 + 0.6 * t + 1.9 * t**2
        ax.plot(x, y, color=lk.BLUE, lw=sk.LW)
        i, j = 50, 86
        d = np.array([2.4, 0.6 + 3.8 * t[i]])
        d = 1.05 * d / np.linalg.norm(d)
        sk.maps(ax, (x[i], y[i]), (x[i] + d[0], y[i] + d[1]), color=lk.RED)
        sk.dot(ax, (x[i], y[i]), r"$\gamma(s)$", at=(0.12, -0.1), ha="left", va="top")
        sk.dot(ax, (x[j], y[j]), r"$\gamma(s+\varepsilon)$", at=(-0.12, 0.08), ha="right", va="bottom")
        sk.label(ax, (x[i] + d[0] + 0.1, y[i] + d[1] - 0.05), r"$\gamma'(s)$", lk.RED, ha="left", va="center")
        sk.label(ax, (7.4, -0.55), r"$\mathbb{G}^4$", ha="right", va="bottom")
        return fig

    def _flat(corners, fill=lk.LIGHT, edge=lk.GREY, alpha=0.6, lw=1.0):
        c = np.array(corners + [corners[0]], float)
        return lk.patch(corners, fill, alpha, n=24), (c[:, 0], c[:, 1], c[:, 2], edge, lw)

    def _curve(v, k, s):
        c = s[:, None] * np.asarray(v, float) + (s**2)[:, None] * np.asarray(k, float)
        return c[:, 0], c[:, 1], c[:, 2]

    def relvel_scene():
        # two particles through one event, their velocities, v(gamma_1, gamma_2) twice, the plane ker(tau)
        g1, g2 = np.array([0.1, -0.5, 1.0]), np.array([-0.25, 0.75, 1.0])
        s = np.linspace(-0.35, 0.8, 50)
        c1, c2 = _curve(g1, (0.05, -0.18, 0), s), _curve(g2, (-0.06, 0.15, 0), s)
        right = np.array([-np.sin(np.radians(-30)), np.cos(np.radians(-30)), 0.0])
        e1 = np.array(_curve(g1, (0.05, -0.18, 0), np.array([0.5]))).ravel() - 0.1 * right
        e2 = np.array(_curve(g2, (-0.06, 0.15, 0), np.array([0.5]))).ravel() + 0.1 * right
        v = g2 - g1
        gap = 0.03 / np.linalg.norm(v)
        sf, ln = _flat([(0.8, -1.1, 0.0), (0.8, 1.6, 0.0), (-0.8, 1.6, 0.0), (-0.8, -1.1, 0.0)])
        return lk.turntable(
            -30,
            22,
            "two particles through one event, their velocities and the relative velocity",
            [
                lk.panel(
                    1.0,
                    surfaces=[sf],
                    lines=[(*c1, lk.RED, 1.6), (*c2, lk.BLUE, 1.6), ln],
                    arrows=[(O3, tuple(g1), K), (O3, tuple(g2), K), (tuple(g1 + gap * v), tuple(g2 - gap * v), lk.ORANGE), (O3, tuple(v), lk.ORANGE)],
                    points=[(O3, K, 3.4)],
                    texts=[
                        (tuple(e1), r"\gamma_1", lk.RED, None, 0),
                        (tuple(e2), r"\gamma_2", lk.BLUE, None, 0),
                        (tuple(0.82 * g1), r"\gamma_1'", K, 0, 8),
                        (tuple(0.82 * g2), r"\gamma_2'", K, 180, 8),
                        (tuple(1.04 * v), r"\vec{v}(\gamma_1, \gamma_2)", lk.ORANGE, -45, 9),
                        ((0.8, -1.1, 0.0), r"\ker(\tau)", lk.GREY, -150, 8),
                    ],
                )
            ],
            height=lk.H3D,
            width=460,
            bias=0.12,
            zoom=1.2,
        )

    def force_scene(ux, fm):
        # the worldline p + t u + t^2 v / 2m under a constant force, with u, v/m, the plane S_p and the line p + t u
        t = np.linspace(-0.4, 1.3, 90)
        x1, x2 = ux * t, 0.5 * fm * t**2
        sf, ln = _flat([(2.0, -0.6, 0), (2.0, 2.6, 0), (-2.0, 2.6, 0), (-2.0, -0.6, 0)])
        tl = np.array([-0.65, 1.65])
        lines = [ln, (ux * tl, 0 * tl, tl, lk.GREY, 1.2, [5, 4], -0.2), (x1, x2, t, lk.BLUE, 1.6)]
        arrows = [(O3, (ux, 0.0, 1.0), lk.GREEN)]
        texts = [
            ((x1[-1], x2[-1], 1.3), r"\gamma", lk.BLUE, 90, 4),
            ((ux, 0.0, 1.0), r"\vec{u}", lk.GREEN, 180, 6),
            (O3, "p", K, -135, 6),
            ((2.0, 2.6, 0), r"S_p", lk.GREY, 0, 5),
            ((1.45 * ux, 0.0, 1.45), r"p + t\vec{u}", lk.GREY, 180, 6),
        ]
        if fm > 0:
            arrows.append((O3, (0.0, fm, 0.0), lk.ORANGE))
            texts.append(((0.0, fm + 0.08, 0.0), r"\vec{v} / m", lk.ORANGE, -20, 2))
        return lk.turntable(
            -30,
            18,
            "the worldline of a particle under a constant force, with u, v/m, the plane S_p and the line p + t u",
            [lk.panel(1.3, surfaces=[sf], lines=lines, arrows=arrows, points=[(O3, K, 3.4)], texts=texts, box=((-2.0, 2.0), (-0.6, 1.8), (-0.65, 1.65)))],
            height=lk.H3D,
            width=460,
            key="L02-force",
            apart=True,
            bias=0.15,
            zoom=1.2,
        )

    def gravity_scene():
        # sigma at rest (the vertical line), gamma on an orbit around it (a helix), the slice S_gamma(t) and the force
        # arrow from gamma(t) towards sigma(t) in it
        t = np.linspace(-1.0, 1.45, 170)
        c = (0.85 * np.sin(t), 0.85 * np.cos(t), t)
        g0, tip = (0.0, 0.85, 0.0), (0.0, 0.1, 0.0)
        corners = [(1.4, -1.4, 0.0), (1.4, 1.4, 0.0), (-1.4, 1.4, 0.0), (-1.4, -1.4, 0.0)]
        sf, ln = _flat(corners)
        return lk.turntable(
            -30,
            22,
            "the particles gamma (an orbit, a helix) and sigma (at rest), the simultaneity slice through gamma(t), and the force arrow from gamma(t) to sigma(t) in it",
            [
                lk.panel(
                    1.0,
                    surfaces=[sf],
                    lines=[ln, ([0.0, 0.0], [0.0, 0.0], [-1.1, 1.65], lk.BLUE, 1.6), (*c, lk.RED, 1.6)],
                    arrows=[(g0, tip, lk.GREEN)],
                    points=[((0.0, 0.0, 0.0), K, 3.4), (g0, K, 3.4)],
                    texts=[
                        ((0.0, 0.0, 0.0), r"\sigma(t)", K, 180, 7),
                        (g0, r"\gamma(t)", K, 10, 7),
                        ((0.0, 0.0, 1.65), r"\sigma", lk.BLUE, 90, 4),
                        ((c[0][-1], c[1][-1], c[2][-1]), r"\gamma", lk.RED, 0, 6),
                        (corners[0], r"S_{\gamma(t)}", lk.GREY, -150, 8),
                    ],
                )
            ],
            height=lk.H3D,
            width=460,
            bias=0.12,
            zoom=1.2,
        )

    def addition_scene():
        # three particles through one event, their velocities, and the three relative velocities forming a
        # triangle (the two summands green, their sum plum); each label sits in space beside its own object
        vel = {"g": np.array([0.2, -0.6, 1.0]), "s": np.array([-0.5, 0.15, 1.0]), "x": np.array([0.45, 0.4, 1.0])}
        bend = {"g": (0.05, -0.1, 0), "s": (-0.08, 0.1, 0), "x": (0.1, 0.06, 0)}
        col = {"g": lk.RED, "s": lk.BLUE, "x": lk.ORANGE}
        nm = {"g": r"\gamma", "s": r"\sigma", "x": r"\xi"}
        s = np.linspace(-0.35, 0.8, 50)
        mid = sum(vel.values()) / 3
        right = np.array([-np.sin(np.radians(-30)), np.cos(np.radians(-30)), 0.0])
        side = {"g": -1, "s": -1, "x": 1}
        nside = {"g": -1, "s": 1, "x": 1}
        lines, texts = [], []
        for k in "gsx":
            c = _curve(vel[k], bend[k], s)
            lines.append((*c, col[k], 1.6))
            texts.append((tuple(np.array(_curve(vel[k], bend[k], np.array([0.5]))).ravel() + 0.1 * nside[k] * right), nm[k], col[k], None, 0))

        def short(a, b, gap=0.03):
            u = gap / np.linalg.norm(b - a)
            return (tuple(a + u * (b - a)), tuple(a + (1 - u) * (b - a)))

        arrows = [(O3, tuple(vel[q]), K) for q in "gsx"]
        arrows += [(*short(vel["g"], vel["s"]), lk.GREEN), (*short(vel["s"], vel["x"]), lk.GREEN), (*short(vel["g"], vel["x"]), PLUM)]
        texts += [(tuple(0.8 * vel[q] + 0.09 * side[q] * right), nm[q] + "'", K, None, 0) for q in "gsx"]
        for a, b, tex, c in (("g", "s", r"\vec{v}(\gamma, \sigma)", lk.GREEN), ("s", "x", r"\vec{v}(\sigma, \xi)", lk.GREEN), ("g", "x", r"\vec{v}(\gamma, \xi)", PLUM)):
            m = (vel[a] + vel[b]) / 2
            d = m - mid
            texts.append((tuple(m + 0.2 * d / np.linalg.norm(d)), tex, c, None, 0))
        return lk.turntable(
            -30,
            25,
            "three particles through one event, their velocities and the three relative velocities forming a triangle",
            [lk.panel(1.0, surfaces=[], lines=lines, arrows=arrows, points=[(O3, K, 3.4)], texts=texts)],
            height=lk.H3D,
            width=460,
            bias=0.12,
            zoom=1.2,
        )

    return addition_scene, causal_sketch, force_scene, frame_sketch, gravity_scene, particle_sketch, relvel_scene


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figure (values hidden)
    s_u = lk.slider(-1.5, 1.5, step=0.1, value=0.0, label=r"spatial part of $\vec u$", show_value=False)
    s_f = lk.slider(0.0, 1.5, step=0.05, value=0.75, label=r"$\vec v/m$", show_value=False)
    return s_f, s_u


@app.cell(hide_code=True)
def _(force_scene, s_f, s_u):
    # the scene of the constant force figure, redrawn by its sliders; its frame is in the example
    force_scene(s_u.value, s_f.value)
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        lk.aside(
            r"$\mathbb E^3$ is affine space $(\mathbb A,\mathbb V,\mk{-})$",
            r"$-$: difference between points = displacement vector",
        ),
        lk.aside(
            r"with Euclidean inner-product $\mk{\langle\ ,\ \rangle}$",
            r"$\langle\ ,\ \rangle$: measurements",
        ),
        r"Choice of &nbsp; $o\in\mathbb E^3$ origin &nbsp; and &nbsp; $\vec e_1,\vec e_2,\vec e_3\in\mathbb V$ orthonormal basis",
        r"> $\Longrightarrow$ &nbsp; usual Cartesian coordinates",
        topic="Euclidean space",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("Schutz 1.1; Carroll 1.2; Sasane 12.1, 13.1–13.2")
    return


@app.cell(hide_code=True)
def _(lk):
    lk.section("Galilean geometry")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Galilean spacetime
    # the geometry of spacetime in Newtonian physics
    lk.prose(r"$\leadsto$ &nbsp; the geometry of spacetime in Newtonian physics")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Galilean spacetime
    # spacetime and mechanics
    lk.prose(
        lk.aside(r"Spacetime $=$ set of all <span class='lk-mark'>events</span>", "events: locations in space + moments in time"),
        lk.aside(
            r"Mechanics $=$ study of the origins of <span class='lk-mark'>motion</span>",
            "motion: relations between events<br>= geometry of spacetime",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Galilean spacetime
    # definition: Galilean spacetime (first form)
    lk.definition(
        [
            r"The **Galilean spacetime** is a 4-dimensional affine space",
            lk.aside(r"$$\mathbb G^4=(\mathbb A,\mathbb V,-)$$", r"assumptions (i), (ii), (iii) as before,<br>with $\dim\mathbb V=4$"),
            lk.aside(r"together with <span class='lk-mark'>some extra structure</span>", "different assumptions needed"),
        ],
        label="def-galilean",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Galilean spacetime
    # the universal time function
    lk.prose(
        r"""
        **The universal time function**

        iv) &nbsp; there exists a function &nbsp; $\tau:\mathbb V\longrightarrow\mathbb R$

        > linear &nbsp;&nbsp; $\tau(a\vec u+b\vec v)=a\,\tau(\vec u)+b\,\tau(\vec v)$

        > non-zero &nbsp;&nbsp; $\exists\,\vec u\in\mathbb V$ with $\tau(\vec u)\neq0$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Galilean spacetime
    # time length and time distance
    lk.prose(
        lk.aside(r"$\leadsto$ &nbsp; we can define the <span class='lk-mark'>time length</span> of vectors &nbsp; $\tau(\vec u)$", "not necessarily positive"),
        lk.aside(
            r"> <span class='lk-mark'>time distance</span> between events &nbsp; $\mk{t(p,q)}=\tau(q-p)$",
            r"$t(p,q)$: from $p$ to $q$",
        ),
    )
    return


@app.cell(hide_code=True)
def _(causal_sketch, lk):
    # module: Galilean spacetime
    # definition: basic causal structure
    lk.definition(
        [
            r"""
            • &nbsp; $\vec u$ **future oriented** if &nbsp; $\tau(\vec u)>0$

            > $\leadsto$ &nbsp; $q$ in future of $p$ if &nbsp; $\tau(q-p)>0$

            • &nbsp; $\vec u$ **past oriented** if &nbsp; $\tau(\vec u)<0$

            > $\leadsto$ &nbsp; $q$ in past of $p$ if &nbsp; $\tau(q-p)<0$

            • &nbsp; $\vec u$ **spatial** if &nbsp; $\tau(\vec u)=0$

            > $\leadsto$ &nbsp; $p$ and $q$ are simultaneous if &nbsp; $\tau(q-p)=0$
            """,
            lk.figure(causal_sketch()),
        ],
        title=r"Basic causal structure in $\mathbb G^4$",
        label="def-causal-galilean",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Galilean spacetime
    # the spatial inner-product
    lk.prose(
        r"**The spatial inner-product**",
        lk.aside(r"iv′) &nbsp; there is a Euclidean inner-product on $\mk{\ker\tau}$", r"$\ker\tau$: $\dim=3$!"),
        r"$$\langle\ ,\ \rangle:\ker\tau\times\ker\tau\longrightarrow\mathbb R$$",
        r"$\leadsto$ &nbsp; we can define spatial length",
        r"> if &nbsp; $\tau(\vec u)=0$ &nbsp; $\Longrightarrow$ &nbsp; $\lVert\vec u\rVert=\sqrt{\langle\vec u,\vec u\rangle}$",
        r"$\leadsto$ &nbsp; each set of mutually simultaneous events in $\mathbb G^4$ is an identical copy of $\mathbb E^3$",
        r"$$S_p=\{q\in\mathbb G^4\mid\tau(q-p)=0\}=p+\ker\tau\approx\mathbb E^3$$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Galilean spacetime
    # definition: Galilean spacetime (complete)
    lk.definition(
        r"$\mathbb G^4=(\mathbb A,\mathbb V,-)$ &nbsp; 4-dimensional affine space together with a **universal time function** $\tau$ and a **spatial inner-product** $\langle\ ,\ \rangle$ on $\ker\tau$",
        label="def-galilean-complete",
    )
    return


@app.cell(hide_code=True)
def _(frame_sketch, lk):
    # module: inertial frames
    # theorem: Cartesian coordinates
    lk.theorem(
        [
            lk.aside(
                r"Choosing &nbsp; $\mk{o}\in\mathbb G^4$ &nbsp; and &nbsp; $\mk{\vec e_0,\vec e_1,\vec e_2,\vec e_3}\in\mathbb V$ &nbsp; such that",
                r"$o$ = origin<br>$\vec e_0,\vec e_1,\vec e_2,\vec e_3$ = inertial frame",
            ),
            lk.aside(
                r"$$\begin{aligned}&\tau(\vec e_0)=1\\[0.2em]&\tau(\vec e_i)=0,\quad i=1,2,3\\[0.2em]&\langle\vec e_i,\vec e_j\rangle=\delta_{ij}=\begin{cases}1&i=j\\0&i\neq j\end{cases}\end{aligned}$$",
                [(1, "unit future oriented"), (3, "spatial orthonormal basis")],
                rows=3,
            ),
            lk.figure(frame_sketch()),
            r"> $\Longrightarrow$ &nbsp; Cartesian coordinates &nbsp; $x^\mu:\mathbb G^4\longrightarrow\mathbb R$, &nbsp; $\mu=0,\underbrace{1,2,3}_{i}$",
            r"$$x^0(p)=\tau(p-o)\qquad x^i(p)=\langle\vec e_i,\,p-o-x^0(p)\,\vec e_0\rangle$$",
            r"> $\Longrightarrow$ &nbsp; identification &nbsp; $\mathbb R^4\approx\mathbb G^4$",
            r"$$(t,x,y,z)\longleftrightarrow p=o+t\,\vec e_0+x\,\vec e_1+y\,\vec e_2+z\,\vec e_3$$",
        ],
        label="thm-galilean-coordinates",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: inertial frames
    # time and length in coordinates
    lk.prose(
        r"$\leadsto$ &nbsp; then &nbsp; $\begin{aligned}&\tau(t,x,y,z)=t\\&\lVert(0,x,y,z)\rVert=\sqrt{x^2+y^2+z^2}\end{aligned}$"
    )
    return


@app.cell(hide_code=True)
def _(lk):
    lk.section("Kinematics and dynamics")
    return


@app.cell(hide_code=True)
def _(lk, particle_sketch):
    # module: particles
    # definition: particle
    lk.definition(
        [
            r"A **particle** in $\mathbb G^4$ is a parameterized curve",
            lk.aside(r"$$\gamma:\mathbb R\longrightarrow\mathbb G^4,\qquad s\longmapsto\gamma(s)$$", "all events in the particle's history!"),
            r"such that &nbsp; $\displaystyle\gamma'(s)=\lim_{\varepsilon\to0}\frac{\gamma(s+\varepsilon)-\gamma(s)}{\varepsilon}\in\mathbb V$",
            r"is future oriented &nbsp; $\tau(\gamma'(s))>0$ &nbsp; $\forall\,s$",
            lk.figure(particle_sketch()),
        ],
        label="def-particle-galilean",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: particles
    # dynamics as shape
    lk.prose(
        lk.aside(
            r"$\leadsto$ &nbsp; we can now study <span class='lk-mark'>dynamics</span> as the shape of a <span class='lk-mark'>curve in spacetime</span>!",
            "dynamics: change of position as function of time<br>curve in spacetime: the history of events",
        )
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: particles
    # remark: gamma' is not the velocity
    lk.remark(
        r"""
        $\gamma'(s)$ is not the particle's velocity!

        > $\leadsto$ &nbsp; it is a 4-dimensional vector …

        > $\leadsto$ &nbsp; $s$ in $\gamma(s)$ is NOT related to physical time! &nbsp; (without other assumptions)
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: absolute time
    # proposition: absolute time parameter
    lk.proposition(
        [
            r"Every particle can be parameterized by an “absolute time” parameter $t$ &nbsp; such that",
            r"$$\tau(\gamma(t_2)-\gamma(t_1))=t_2-t_1$$",
        ],
        label="prop-absolute-time",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: absolute time
    # proof (idea)
    lk.proof(
        [
            r"Up to solving some ODE we can always change parameterization so that &nbsp; $\tau(\gamma'(t))=1$",
            r"> $\Longrightarrow$ &nbsp; $\displaystyle\begin{aligned}t_2-t_1&=\int_{t_1}^{t_2}dt=\int_{t_1}^{t_2}\tau(\gamma'(t))\,dt\\[0.3em]&=\tau\Big(\int_{t_1}^{t_2}\gamma'(t)\,dt\Big)=\tau(\gamma(t_2)-\gamma(t_1))\end{aligned}$",
        ],
        title="idea",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: absolute time
    # measuring time, and spatial velocity
    lk.prose(
        r"$\leadsto$ &nbsp; we can now measure time!",
        lk.aside(r"$\leadsto$ &nbsp; how do we define <span class='lk-mark'>spatial velocity</span>?", "not possible with a single particle!"),
    )
    return


@app.cell(hide_code=True)
def _(lk, relvel_scene):
    # module: relative velocity
    # definition: relative velocity
    lk.definition(
        [
            r"Given two particles $\gamma_1,\gamma_2$ &nbsp; (with $\tau(\gamma_1')=\tau(\gamma_2')=1$)",
            r"the **relative velocity** of $\gamma_2$ with respect to $\gamma_1$ is the spatial vector",
            r"$$\vec v(\gamma_1,\gamma_2)=\gamma_2'-\gamma_1'\in\ker(\tau)$$",
            lk.figure(relvel_scene()),
        ],
        label="def-relative-velocity-galilean",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Newton's laws
    # definition: absolute acceleration
    lk.definition(
        [
            lk.aside(
                r"The <span class='lk-mark'>**absolute acceleration**</span> of a particle $\gamma$ &nbsp; $(\tau(\gamma')=1)$ &nbsp; is the spatial vector",
                "does not require other reference",
            ),
            lk.aside(
                r"$$\vec a(\gamma)=\gamma''\ \mk{\in\ker(\tau)}$$",
                r"$\in\ker(\tau)$: &nbsp; $\tau(\gamma'')=\dfrac{d}{dt}\tau(\gamma')=0$",
            ),
        ],
        label="def-absolute-acceleration",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Newton's laws
    # remark: Newton's first and second laws
    lk.remark(
        [
            r"In the absence of external forces, a particle's history is a *straight future oriented line*",
            lk.aside(
                r"$$\gamma(t)=p+t\,\vec u,\qquad\tau(\vec u)=1$$",
                r"solution of $\gamma''(t)=\vec0$, $\gamma(0)=p$, $\gamma'(0)=\vec u$<br>(inertial particle / inertial observer)",
            ),
            r"Deviation from inertial motion is determined by",
            lk.aside(
                r"$$\mk{\gamma''(t)}=\frac1m\vec F(t),\qquad\text{where}\quad\begin{aligned}&m\in\mathbb R_+&&(\text{mass})\\&\vec F(t)\in\ker(\tau)&&(\text{force})\end{aligned}$$",
                r"$\gamma''(t)=\dots$: system of second order ODEs",
            ),
            r"in Cartesian coordinates (choice of origin and inertial frame)",
            r"$$\gamma''(t)=\begin{bmatrix}t\\x(t)\\y(t)\\z(t)\end{bmatrix}''=\begin{bmatrix}0\\x''(t)\\y''(t)\\z''(t)\end{bmatrix}=\frac1m\begin{bmatrix}0\\F^x(t)\\F^y(t)\\F^z(t)\end{bmatrix}$$",
        ],
        title="Newton's first & second laws",
    )
    return


@app.cell(hide_code=True)
def _(lk, s_f, s_u):
    # module: Newton's laws
    # example: constant force
    lk.example(
        [
            r"constant force: &nbsp; $\vec F(t)=\vec v\in\ker(\tau)$",
            r"> $\Longrightarrow$ &nbsp; $\gamma(t)=p+t\,\vec u+\dfrac{1}{2m}\,t^2\,\vec v$",
            lk.interactive(lk.frame("L02-force", lk.H3D, 460), controls=[s_u, s_f]),
        ],
        label="ex-constant-force",
    )
    return


@app.cell(hide_code=True)
def _(gravity_scene, lk):
    # module: gravity and electrodynamics
    # Newtonian gravity
    lk.prose(
        r"Newtonian gravity:",
        lk.aside(
            r"$$\vec F(t)=-G\,m\,M\,\frac{\mk{\gamma(t)-\sigma(t)}}{\lVert\gamma(t)-\sigma(t)\rVert^3}\in\ker(\tau)$$",
            r"$\gamma(t),\sigma(t)$ simultaneous",
        ),
        lk.figure(gravity_scene()),
        r"$S_{\gamma(t)}=$ space of simultaneity of $\gamma(t)$ $\approx\mathbb E^3$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gravity and electrodynamics
    # Coulomb and Maxwell
    lk.prose(
        r"$\leadsto$ &nbsp; Coulomb's law of electrostatics can be written almost identically exchanging masses and charges!",
        r"$\leadsto$ &nbsp; Maxwell's electrodynamics breaks down …",
        r"> in Cartesian coordinates we want something like",
        lk.aside(
            r"$$\vec F(t)=q\big(\mk{\vec E_{\sigma(t)}}+\mk{\vec v_{\gamma(t)}}\times\mk{\vec B_{\sigma(t)}}\big)\qquad(\text{Lorentz force law})$$",
            r"$\vec E_{\sigma(t)}$: electric field generated by $\sigma$,<br>depends on the inertial frame<br>$\vec v_{\gamma(t)}$: velocity of $\gamma$ relative to the inertial frame<br>$\vec B_{\sigma(t)}$: magnetic field generated by $\sigma$,<br>depends on the inertial frame",
        ),
        r"> with",
        lk.aside(
            r"$$\begin{aligned}\vec\nabla\cdot\vec E_{\sigma(t)}&=\frac{\rho_{\sigma(t)}}{\varepsilon_0}&\qquad\vec\nabla\times\vec B_{\sigma(t)}-\frac{1}{c^2}\partial_t\vec E_{\sigma(t)}&=\mu_0\vec J_{\sigma(t)}\\[0.4em]\vec\nabla\cdot\vec B_{\sigma(t)}&=0&\qquad\vec\nabla\times\vec E_{\sigma(t)}+\partial_t\vec B_{\sigma(t)}&=0\end{aligned}$$",
            "Maxwell's equations:<br>depend on the choice of inertial frame!<br>not an intrinsic physical structure",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gravity and electrodynamics
    # remark: the wave equation
    lk.remark(
        [
            r"In the vacuum, Maxwell implies the wave equation",
            r"$$\begin{cases}\vec\nabla\cdot\vec E=0&\vec\nabla\times\vec B-\frac{1}{c^2}\partial_t\vec E=0\\[0.3em]\vec\nabla\cdot\vec B=0&\vec\nabla\times\vec E+\partial_t\vec B=0\end{cases}\quad\Longrightarrow\quad\begin{cases}\big(\Delta-\frac{1}{c^2}\partial_t^2\big)\vec E=0\\[0.3em]\big(\Delta-\frac{1}{c^2}\partial_t^2\big)\vec B=0\end{cases}$$",
            r"> $\Longrightarrow$ &nbsp; electromagnetic “waves” propagate at constant speed $c$ &nbsp; (the speed of light)",
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: gravity and electrodynamics
    # the speed of light is constant
    lk.prose(
        r"$\leadsto$ &nbsp; experimentally $c$ is independent of the choice of inertial frames!",
        lk.aside(
            r"> $\Longrightarrow$ &nbsp; the speed of light relative to any inertial particle is always constant!",
            "not possible in Galilean spacetime",
        ),
    )
    return


@app.cell(hide_code=True)
def _(addition_scene, lk):
    # module: addition of relative velocities
    # theorem: relative velocities add
    lk.theorem(
        [
            r"Given $\gamma,\sigma,\xi$ three particles in $\mathbb G^4$",
            r"$$\vec v(\gamma,\xi)=\vec v(\gamma,\sigma)+\vec v(\sigma,\xi)$$",
            lk.figure(addition_scene()),
        ],
        label="thm-addition-galilean",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: addition of relative velocities
    # triangle inequality and the contradiction
    lk.prose(
        r"triangle inequality &nbsp; $\Longrightarrow$ &nbsp; $\lVert\vec v(\gamma,\xi)\rVert\leq\lVert\vec v(\gamma,\sigma)\rVert+\lVert\vec v(\sigma,\xi)\rVert$",
        r"> with equality iff &nbsp; $\vec v(\sigma,\xi)=\lambda\,\vec v(\gamma,\sigma)$, &nbsp; $\lambda\geq0$",
        r"$\gamma,\sigma$ are inertial particles and $\xi$ is a light particle moving along same direction",
        lk.aside(
            r"> $\Longrightarrow$ &nbsp; $c=\lVert\vec v(\gamma,\sigma)\rVert+c$",
            r"contradiction unless $\gamma,\sigma$<br>have zero relative velocity",
        ),
    )
    return


if __name__ == "__main__":
    app.run()
