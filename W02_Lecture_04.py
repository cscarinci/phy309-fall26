import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 4 · Proper time, reversed inequalities, relative velocity", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import math
    import sys

    import marimo as mo
    import numpy as np

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return lk, math, mo, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(4, "Proper time, reversed inequalities, relative velocity")
    return


@app.cell(hide_code=True)
def _(lk, math, np):
    # Helpers of this lecture: the sketches in the shared sketch style, and the two 3D figures (the twins, relative
    # velocity), coordinates (x^1, x^2, time)
    sk = lk.sk
    K = "#000000"
    O3 = (0.0, 0.0, 0.0)

    def _cone(ax, x, y, r, h, lw=None, color=K):
        # a small double cone with vertex (x, y): two slanted sides and an ellipse at each end
        lw = lw or sk.LW
        for s in (1, -1):
            ax.plot([x - r, x + r], [y - s * h, y + s * h], color=color, lw=lw)
            t = np.linspace(0, 2 * np.pi, 120)
            ax.plot(x + r * np.cos(t), y + s * h + 0.22 * r * np.sin(t), color=color, lw=lw)

    def cone_sketch():
        # the light cone at a point, with timelike, lightlike and spacelike vectors
        fig, ax = sk.sketch((-3.0, 5.6), (-2.9, 2.9))
        _cone(ax, 0, 0, 1.5, 1.5)
        sk.maps(ax, (0, 0), (0.35, 2.4), color=lk.BLUE)
        sk.maps(ax, (0, 0), (-0.3, -2.4), color=lk.BLUE)
        sk.maps(ax, (0, 0), (2.0, 2.0), color=lk.ORANGE)
        sk.maps(ax, (0, 0), (1.9, -1.9), color=lk.ORANGE)
        sk.maps(ax, (0, 0), (2.4, 0.35), color=lk.GREEN)
        sk.dot(ax, (0, 0))
        sk.label(ax, (0.55, 2.55), "timelike (future)", lk.BLUE, ha="left")
        sk.label(ax, (-0.1, -2.6), "timelike (past)", lk.BLUE, ha="left", va="top")
        sk.label(ax, (2.2, 2.0), "lightlike (future)", lk.ORANGE, ha="left")
        sk.label(ax, (2.1, -1.9), "lightlike (past)", lk.ORANGE, ha="left")
        sk.label(ax, (2.6, 0.35), "spacelike", lk.GREEN, ha="left")
        sk.label(ax, (-1.7, -0.9), "light cone", ha="right")
        return fig

    def particle_sketch():
        # a particle with the light cone at two of its events; its tangent vector is inside the upper cone
        fig, ax = sk.sketch((-1.6, 3.2), (-0.4, 4.0))
        s = np.linspace(0, 3.8, 200)
        x = 0.12 * s**2
        ax.plot(x, s, color=lk.BLUE, lw=sk.LW + 0.2)
        for y in (0.8, 2.5):
            _cone(ax, 0.12 * y**2, y, 0.42, 0.42, lw=1.2, color=lk.GREY)
            sk.dot(ax, (0.12 * y**2, y))
        p = np.array([0.12 * 2.5**2, 2.5])
        d = np.array([0.24 * 2.5, 1.0]) / np.hypot(0.24 * 2.5, 1.0)
        sk.maps(ax, tuple(p), tuple(p + 1.1 * d), color=K)
        sk.label(ax, tuple(p + np.array([0.3, -0.15])), r"$\gamma(s)$", ha="left")
        sk.label(ax, tuple(p + 1.1 * d + np.array([0.15, 0.05])), r"$\gamma'(s)$", ha="left")
        sk.label(ax, (0.12 * 0.8**2 + 0.55, 0.65), r"$\gamma$", lk.BLUE, ha="left")
        return fig

    def compare_sketch():
        # a particle from p to q and the straight q - p in M^4; a curve from p to q and the straight q - p in E^3
        fig, ax = sk.sketch((-2.9, 9.4), (-0.6, 3.6))
        s = np.linspace(0, 2.6, 120)
        ax.plot(0.6 * np.sin(np.pi * s / 2.6), s, color=lk.BLUE, lw=sk.LW)
        sk.maps(ax, (0, 0), (0, 2.6), color=lk.RED)
        sk.dot(ax, (0, 0), r"$\gamma(t_1)=p$", at=(-0.15, 0), ha="right", va="center")
        sk.dot(ax, (0, 2.6), r"$\gamma(t_2)=q$", at=(-0.15, 0), ha="right", va="center")
        sk.label(ax, (-0.15, 1.3), r"$q-p$", lk.RED, ha="right")
        sk.label(ax, (0.75, 1.3), r"$\gamma$", lk.BLUE, ha="left")
        sk.label(ax, (-2.6, 3.3), r"$\mathbb{M}^4$", ha="left")
        x = np.linspace(0, 2.6, 120)
        ax.plot(4.0 + x * 3.0 / 2.6, 0.7 + 0.8 * np.sin(np.pi * x / 2.6), color=lk.BLUE, lw=sk.LW)
        sk.maps(ax, (4.0, 0.7), (7.0, 0.7), color=lk.RED)
        sk.dot(ax, (4.0, 0.7), r"$\gamma(t_1)=p$", at=(-0.2, -0.3), ha="right")
        sk.dot(ax, (7.0, 0.7), r"$\gamma(t_2)=q$", at=(0.2, -0.3), ha="left")
        sk.label(ax, (5.5, 0.45), r"$q-p$", lk.RED, va="top")
        sk.label(ax, (5.5, 1.6), r"$\gamma$", lk.BLUE, va="bottom")
        sk.label(ax, (3.4, 3.3), r"$\mathbb{E}^3$", ha="left")
        return fig

    def _flat(corners, fill=lk.LIGHT, edge=lk.GREY, alpha=0.6, lw=1.0):
        # a flat parallelogram (cut fine so that arrows lying in it sort right) and its edge
        c = np.array(corners + [corners[0]], float)
        return lk.patch(corners, fill, alpha, n=24), (c[:, 0], c[:, 1], c[:, 2], edge, lw)

    def _curve(v, k, s):
        # the curve s -> s v + s^2 k
        c = s[:, None] * np.asarray(v, float) + (s**2)[:, None] * np.asarray(k, float)
        return c[:, 0], c[:, 1], c[:, 2]

    def twin_scene(x):
        # A at rest (A's rest frame), the star along e_1: p = (0, 0, 0), q = (0, 0, 10), r = (x, 0, 5), s = (0, 0, 5);
        # the future cone of p up to t = 5 and the past cone of q down to t = 5, and A's simultaneity plane t = 5
        p, q, r, s = O3, (0.0, 0.0, 10.0), (x, 0.0, 5.0), (0.0, 0.0, 5.0)
        rr, ph = np.meshgrid(np.linspace(0, 5, 11), np.linspace(0, 2 * np.pi, 73), indexing="ij")
        cones = [lk.sheet(rr * np.cos(ph), rr * np.sin(ph), rr, alpha=0.18), lk.sheet(rr * np.cos(ph), rr * np.sin(ph), 10 - rr, alpha=0.18)]
        c = np.linspace(0, 2 * np.pi, 145)
        rim = (5 * np.cos(c), 5 * np.sin(c), 5 + 0 * c, lk.GREY, 0.8)
        sf, ln = _flat([(5.8, -5.8, 5.0), (5.8, 5.8, 5.0), (-5.8, 5.8, 5.0), (-5.8, -5.8, 5.0)], alpha=0.3)
        arrows = [((0.0, 0.0, 1.0), q, lk.BLUE), (p, r, lk.RED), (r, q, lk.RED), (p, (0.0, 0.0, 1.0), K, 1.0), (p, (1.0, 0.0, 0.0), K, 1.0)]
        texts = [
            (p, r"p = (0, 0)", K, -60, 12),
            (q, r"q = (10, 0)", K, 20, 8),
            (s, r"s", K, 180, 7),
            (r, r"r", K, 0, 7),
            ((0.0, 0.0, 7.5), r"\mathrm{A}", lk.BLUE, 180, 7),
            ((0.75 * x, 0.0, 3.75), r"\mathrm{B}", lk.RED, -30, 7),
            ((0.0, 0.0, 0.55), r"e_0", K, 180, 6),
            ((1.0, 0.0, 0.0), r"e_1", K, 0, 6),
        ]
        return lk.turntable(
            -78,
            16,
            "the twins: A at rest from p to q, B from p to the star at r and back; the future cone of p, the past cone of q, and A's simultaneity plane through s and r",
            [lk.panel(1.0, surfaces=cones + [sf], lines=[rim, ln], arrows=arrows, points=[(p, K, 3.4), (q, K, 3.4), (r, K, 3.4), (s, K, 3.4)], texts=texts, box=((-5.9, 5.9), (-5.9, 5.9), (-0.3, 10.4)))],
            height=400,
            key="L04-twins",
            zoom=1.3,
            apart=True,
            bias=0.12,
        )

    def relvel_scene(beta):
        # u and v unit timelike, tilted by half the relative rapidity each way, moving along the horizontal direction m;
        # the planes p + u^perp, p + v^perp meet in a line; nu(u, v) from the tip of u, nu(v, u) from the tip of v
        a, el = math.radians(-78), 22
        m = np.array([-math.sin(a), math.cos(a)]) * math.cos(math.radians(12)) - np.array([math.cos(a), math.sin(a)]) * math.sin(math.radians(12))
        k = np.array([m[1], -m[0]])
        h = math.atanh(beta) / 2
        um, vm = (-math.sinh(h), math.cosh(h)), (math.sinh(h), math.cosh(h))
        u, v = np.array([um[0] * m[0], um[0] * m[1], um[1]]), np.array([vm[0] * m[0], vm[0] * m[1], vm[1]])

        def eta(x, y):
            return x[0] * y[0] + x[1] * y[1] - x[2] * y[2]

        e = eta(u, v)
        nuv, nvu = v / -e - u, u / -e - v
        assert abs(eta(nuv, u)) < 1e-9 and abs(eta(nvu, v)) < 1e-9 and abs(eta(nuv, nuv) - beta**2) < 1e-9

        def gap(x, y):
            d = (y - x) / np.linalg.norm(y - x)
            return tuple(x + 0.03 * d), tuple(y - 0.03 * d)

        def perp(wm, al, c):  # the point al k + c (m, w_m / w_t) of p + w^perp
            return (al * k[0] + c * m[0], al * k[1] + c * m[1], c * wm[0] / wm[1])

        L1, L2 = 1.3, 1.6
        su, lu = _flat([perp(um, L1, -L2), perp(um, L1, L2), perp(um, -L1, L2), perp(um, -L1, -L2)], fill="#f1e1de", edge=lk.RED, alpha=0.5)
        sv, lv = _flat([perp(vm, L1, -L2), perp(vm, L1, L2), perp(vm, -L1, L2), perp(vm, -L1, -L2)], fill="#dfe7f1", edge=lk.BLUE, alpha=0.5)
        al = np.linspace(-L1, L1, 60)
        meet = (al * k[0], al * k[1], 0 * al, lk.GREY, 0.8, None, 0.05)
        cg = _curve(u, (0.1 * k[0], 0.1 * k[1], 0), np.linspace(-1.1 / u[2], 2.1 / u[2], 80))
        cs = _curve(v, (-0.1 * k[0], -0.1 * k[1], 0), np.linspace(-1.1 / v[2], 2.1 / v[2], 80))
        texts = [
            ((cg[0][0], cg[1][0], cg[2][0]), r"\gamma", lk.RED, -90, 4),
            ((cs[0][0], cs[1][0], cs[2][0]), r"\sigma", lk.BLUE, -90, 4),
            (tuple(0.5 * u), r"u", K, 180, 7),
            (tuple(0.5 * v), r"v", K, 0, 7),
            (tuple(u), r"\nu(u, v)", lk.GREEN, 180, 7),
            (tuple(v), r"\nu(v, u)", lk.ORANGE, 135, 6),
            (perp(um, L1, L2), r"p + u^\perp = S_p^u", lk.RED, 0, 6),
            (perp(vm, L1, L2), r"p + v^\perp = S_p^v", lk.BLUE, 0, 6),
            (O3, r"p", K, -60, 8),
        ]
        return lk.turntable(
            math.degrees(a),
            el,
            "two particles through p, their velocities u and v, the planes p + u-perp and p + v-perp meeting in a line, and the relative velocities nu(u, v), nu(v, u)",
            [
                lk.panel(
                    1.0,
                    surfaces=[su, sv],
                    lines=[lu, lv, (*cg, lk.RED, 1.6), (*cs, lk.BLUE, 1.6), meet],
                    arrows=[(O3, tuple(u), K), (O3, tuple(v), K), (*gap(u, u + nuv), lk.GREEN), (*gap(v, v + nvu), lk.ORANGE)],
                    points=[(O3, K, 3.4)],
                    texts=texts,
                    box=((-2.3, 2.3), (-2.3, 2.3), (-1.4, 2.3)),
                )
            ],
            height=lk.H3D,
            key="L04-relvel",
            zoom=1.3,
            apart=True,
            bias=0.12,
        )

    return compare_sketch, cone_sketch, particle_sketch, relvel_scene, twin_scene


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures (values hidden)
    s_star = lk.slider(1.0, 4.9, step=0.1, value=4.0, label="distance to the star", show_value=False)
    s_beta = lk.slider(0.4, 0.85, step=0.05, value=0.8, label=r"$\lVert\nu(u,v)\rVert$", show_value=False)
    return s_beta, s_star


@app.cell(hide_code=True)
def _(s_star, twin_scene):
    # the scene of the twins figure, redrawn by its slider; its frame is in the twin paradox example
    twin_scene(round(s_star.value, 1))
    return


@app.cell(hide_code=True)
def _(relvel_scene, s_beta):
    # the scene of the relative velocity figure, redrawn by its slider; its frame is in the relative velocity block
    relvel_scene(s_beta.value)
    return


@app.cell(hide_code=True)
def _(cone_sketch, lk):
    # module: recap
    # recap
    lk.recap(
        lk.aside(
            r"$\mathbb M^4=\mk{(\mathbb A^4,\mathbb V^4,-)}$, &nbsp; $\mk{\eta}:\mathbb V^4\times\mathbb V^4\longrightarrow\mathbb R$",
            r"$(\mathbb A^4,\mathbb V^4,-)$ = affine space<br>$\eta$ symmetric, bilinear, signature $(3,1)$",
        ),
        lk.aside(
            r"$\mk{u}\in\mathbb V^4$ &nbsp; $\leadsto$ &nbsp; $\begin{cases}\text{timelike}&\text{if }\lVert u\rVert^2<0\\\text{spacelike}&\text{if }\lVert u\rVert^2>0\\\text{lightlike}&\text{if }\lVert u\rVert^2=0\end{cases}$",
            r"$u$ non-zero",
        ),
        lk.figure(cone_sketch()),
        topic="Minkowski spacetime",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("Schutz 1.8–1.13; Carroll 1.2; Sasane 5.1–5.3, 12.2–12.3")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: causal structure
    # definition: basic causal structure
    lk.definition(
        r"""
        • &nbsp; $q$ is **in the future of** $p$ &nbsp; if $q-p$ is timelike or lightlike in the “future” side of the cone

        • &nbsp; $q$ is **in the past of** $p$ &nbsp; if $q-p$ is timelike or lightlike in the “past” side of the cone

        • &nbsp; $p,q$ are **spacelike separated** &nbsp; if $q-p$ is spacelike
        """,
        title=r"Basic causal structure in $\mathbb M^4$",
        label="def-causal",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: causal structure
    # not a notion of simultaneity
    lk.prose(
        lk.aside(
            r"$\leadsto$ &nbsp; not a notion of <span class='lk-mark'>simultaneity</span>!",
            "will depend on additional choices!",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: causal structure
    # definition: proper time and proper distance between events
    lk.definition(
        r"""
        Given &nbsp; $p,q\in\mathbb M^4$

        > • &nbsp; if $q$ is in the future (past) of $p$

        > > $\leadsto$ &nbsp; $\mathrm{time}(p,q)=\pm\sqrt{-\lVert q-p\rVert^2}$ &nbsp; (**proper time** from $p$ to $q$)

        > • &nbsp; if $p,q$ are spacelike separated

        > > $\leadsto$ &nbsp; $\mathrm{dist}(p,q)=\sqrt{\lVert q-p\rVert^2}$ &nbsp; (**proper distance** from $p$ to $q$)
        """,
        label="def-proper-time-distance",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: proper time length
    # definition: particle
    lk.definition(
        r"A **particle** in $\mathbb M^4$ is a parameterized curve &nbsp; $\gamma:\mathbb R\longrightarrow\mathbb M^4$ &nbsp; such that $\gamma'(s)$ is timelike and future oriented",
        label="def-particle",
    )
    return


@app.cell(hide_code=True)
def _(lk, particle_sketch):
    # module: proper time length
    # the tangent vector stays inside the upper cone
    lk.prose(
        r"At every event in the history of the particle its tangent 4-vector is inside the upper light cone!",
        r"> $\Longrightarrow$ &nbsp; $\gamma(t_2)-\gamma(t_1)$ is also inside the upper cone &nbsp; $\forall\,t_2>t_1$",
        lk.figure(particle_sketch()),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: proper time length
    # theorem: proper time parameterization
    lk.theorem(
        r"Every particle in $\mathbb M^4$ can be parameterized by a “proper time length parameter” $t$ &nbsp; such that &nbsp; $\lVert\gamma'(t)\rVert^2=-1$",
        label="thm-proper-time-parameter",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: proper time length
    # recall: absolute time in Galilean spacetime
    lk.prose(
        r"$\leadsto$ &nbsp; recall, in $\mathbb G^4$, particles were parameterized by “absolute time” if $\tau(\gamma'(t))=1$",
        lk.aside(
            r"> $\displaystyle\begin{aligned}\Longrightarrow\quad\mathrm{time}(\gamma(t_1),\gamma(t_2))&=\int_{t_1}^{t_2}\tau(\gamma'(t))\,dt=\mk{t_2-t_1}\\[0.3em]&=\mk{\tau(\gamma(t_2)-\gamma(t_1))}\end{aligned}$",
            [(1, "absolute time parameterization"), (2, "for any particle")],
            rows=2,
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: proper time length
    # definition: proper time length
    lk.definition(
        [
            r"The **proper time length** of a particle $\gamma:\mathbb R\longrightarrow\mathbb M^4$ is",
            lk.aside(
                r"$$\begin{aligned}\mathrm{time}_\gamma(\gamma(t_1),\gamma(t_2))&=\int_{t_1}^{t_2}\sqrt{-\lVert\gamma'(t)\rVert^2}\,dt\\[0.3em]&=\mk{t_2-t_1}\ \mk{\leq}\ \sqrt{-\lVert\gamma(t_2)-\gamma(t_1)\rVert^2}\end{aligned}$$",
                r"$t_2-t_1$: proper time parameterization<br>$\leq$: equal only if $\gamma$ is an inertial particle",
                at="last",
            ),
        ],
        label="def-proper-time-length",
    )
    return


@app.cell(hide_code=True)
def _(compare_sketch, lk):
    # module: proper time length
    # proper time length against length
    lk.prose(
        r"$$\underbrace{\sqrt{-\lVert q-p\rVert^2}}_{\footnotesize\begin{matrix}\text{proper time}\\\text{from }p\text{ to }q\end{matrix}}\geq\underbrace{\mathrm{time}_\gamma(p,q)}_{\footnotesize\begin{matrix}\text{proper time}\\\text{length of }\gamma\end{matrix}}\qquad\qquad\underbrace{\mathrm{length}_\gamma(p,q)}_{\text{length of }\gamma}\geq\underbrace{\sqrt{\lVert q-p\rVert^2}}_{\footnotesize\begin{matrix}\text{distance}\\\text{from }p\text{ to }q\end{matrix}}$$",
        lk.figure(compare_sketch()),
        r"""
        $\leadsto$ &nbsp; like length, proper time length depends on each particle!
        """,
        lk.aside(
            r"> $\Longrightarrow$ &nbsp; each particle has its own <span class='lk-mark'>proper time length parameterization</span>",
            "its own clock!",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: reversed inequalities
    # theorem: reversed Cauchy-Schwarz and triangle inequalities
    lk.theorem(
        [
            lk.aside(r"If $u,v\in\mathbb V$ are timelike future oriented", "the inequalities are reversed!"),
            r"""
            > • &nbsp; $\eta(u,v)^2\geq\lVert u\rVert^2\lVert v\rVert^2$, &nbsp; with “$=$” iff $u,v$ are proportional

            > • &nbsp; $\sqrt{-\lVert u+v\rVert^2}\geq\sqrt{-\lVert u\rVert^2}+\sqrt{-\lVert v\rVert^2}$, &nbsp; with “$=$” iff $u,v$ are proportional
            """,
        ],
        title="Cauchy–Schwarz & triangle inequalities",
        label="thm-reversed",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: reversed inequalities
    # recall: the Euclidean inequalities
    lk.prose(
        r"$\leadsto$ &nbsp; recall in $\mathbb E^3$ &nbsp;&nbsp; $\begin{aligned}\langle u,v\rangle^2&\leq\lVert u\rVert^2\lVert v\rVert^2\\\lVert u+v\rVert&\leq\lVert u\rVert+\lVert v\rVert\end{aligned}$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: reversed inequalities
    # proof
    lk.proof(
        [
            r"Given $u,v$ future oriented timelike vectors",
            r"""
            $\eta(u,v)<0$

            > $\leadsto$ &nbsp; Choose &nbsp; $e_\mu=e_0,e_i$ &nbsp; inertial frame

            > > $\Longrightarrow$ &nbsp; $\begin{cases}u=u^0e_0+u^ie_i&\text{with }u^0>0\\v=v^0e_0+v^ie_i&\text{with }v^0>0\end{cases}$
            """,
            lk.aside(
                r"> $\lVert u\rVert^2=-(u^0)^2+\delta_{ij}u^iu^j<0$ &nbsp; $\Longrightarrow$ &nbsp; $\mk{\sqrt{\delta_{ij}u^iu^j}}<u^0$",
                r"$\sqrt{\delta_{ij}u^iu^j}=\sqrt{(u^1)^2+(u^2)^2+(u^3)^2}$",
            ),
            r"""
            > $\lVert v\rVert^2=-(v^0)^2+\delta_{ij}v^iv^j<0$ &nbsp; $\Longrightarrow$ &nbsp; $\sqrt{\delta_{ij}v^iv^j}<v^0$

            > Euclidean Cauchy–Schwarz &nbsp; $\Longrightarrow$ &nbsp; $\delta_{ij}u^iv^j\leq\sqrt{\delta_{k\ell}u^ku^\ell}\,\sqrt{\delta_{mn}v^mv^n}<u^0v^0$

            > > $\Longrightarrow$ &nbsp; $-u^0v^0+\delta_{ij}u^iv^j<0$
            """,
            lk.gap(),
            lk.aside(
                r"Consider &nbsp; $\eta(u+tv,u+tv)=\lVert u\rVert^2+2t\,\eta(u,v)+t^2\lVert v\rVert^2$",
                r"quadratic polynomial with negative leading coefficient<br>$\Longrightarrow$ achieves a maximum at $t=-\dfrac{\eta(u,v)}{\lVert v\rVert^2}$",
            ),
            r"Let &nbsp; $w=u-\dfrac{\eta(u,v)}{\lVert v\rVert^2}\,v$",
            r"""
            > $\Longrightarrow$ &nbsp; $\eta(v,w)=\eta(v,u)-\eta(u,v)\dfrac{\lVert v\rVert^2}{\lVert v\rVert^2}=0$

            > $\Longrightarrow$ &nbsp; $w\in\mk{v}^\perp$
            """,
            lk.aside(
                r"> > $\Longrightarrow$ &nbsp; $0\leq\mk{\lVert w\rVert^2}=\lVert u\rVert^2-2\dfrac{\eta(u,v)^2}{\lVert v\rVert^2}+\dfrac{\eta(u,v)^2}{\lVert v\rVert^2}$",
                r"$v$ timelike, &nbsp; $w$ spacelike",
            ),
            lk.aside(
                r"> > $\Longrightarrow$ &nbsp; $\lVert u\rVert^2\geq\dfrac{\eta(u,v)^2}{\mk{\lVert v\rVert^2}}$",
                r"$\lVert v\rVert^2$ negative",
            ),
            r"> > $\Longrightarrow$ &nbsp; $\lVert u\rVert^2\lVert v\rVert^2\leq\eta(u,v)^2$ &nbsp;&nbsp; reversed Cauchy–Schwarz ✓",
            lk.aside(
                r"> > $\Longrightarrow$ &nbsp; $-\eta(u,v)\geq\sqrt{-\lVert u\rVert^2}\,\sqrt{-\lVert v\rVert^2}$",
                r"positive: $-\eta(u,v)$, $\sqrt{-\lVert u\rVert^2}$, $\sqrt{-\lVert v\rVert^2}$",
            ),
            lk.gap(),
            r"$u+v$ is timelike",
            lk.gap(),
            r"$\displaystyle\begin{aligned}-\lVert u+v\rVert^2&=-\lVert u\rVert^2-2\,\eta(u,v)-\lVert v\rVert^2\\[0.3em]&\geq-\lVert u\rVert^2+2\sqrt{-\lVert u\rVert^2}\sqrt{-\lVert v\rVert^2}-\lVert v\rVert^2=\Big(\sqrt{-\lVert u\rVert^2}+\sqrt{-\lVert v\rVert^2}\Big)^2\end{aligned}$",
        ],
        label="pf-reversed",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: reversed inequalities
    # corollary: inertial particles maximize proper time
    lk.corollary(
        lk.aside(
            r"$$\begin{aligned}\sqrt{-\lVert\gamma(t_2)-\gamma(t_1)\rVert^2}\int_{t_1}^{t_2}\sqrt{-\lVert\gamma'(t)\rVert^2}\,dt\ &\mk{\leq}\ \int_{t_1}^{t_2}-\eta\big(\gamma(t_2)-\gamma(t_1),\gamma'(t)\big)\,dt\\[0.3em]&=\Big(\sqrt{-\lVert\gamma(t_2)-\gamma(t_1)\rVert^2}\Big)^2\end{aligned}$$",
            r"“$=$” iff $\gamma$ is inertial",
            at=1,
            rows=2,
        ),
        label="cor-inertial-max",
    )
    return


@app.cell(hide_code=True)
def _(lk, s_star):
    # module: twin paradox
    # example: the twin paradox
    lk.example(
        [
            r"Twin A stays on Earth, twin B visits a nearby star.",
            r"Twin B returns and finds twin A is older …",
            lk.interactive(lk.frame("L04-twins", 400), controls=[s_star]),
            r"$$\underbrace{\sqrt{-\underbrace{\lVert q-p\rVert^2}_{-100}}}_{\footnotesize\begin{matrix}\mathrm{time}_A(p,q)=10\\\text{A waits 10 years}\\\text{for B's return}\end{matrix}}\ \geq\ \underbrace{\sqrt{-\underbrace{\lVert r-p\rVert^2}_{-25+16}}}_{\footnotesize\begin{matrix}\mathrm{time}_B(p,r)=3\\\text{B takes 3 years}\\\text{to reach the star}\end{matrix}}+\underbrace{\sqrt{-\underbrace{\lVert q-r\rVert^2}_{-25+16}}}_{\footnotesize\begin{matrix}\mathrm{time}_B(r,q)=3\\\text{B takes another}\\\text{3 years to return}\end{matrix}}$$",
            lk.aside(
                r"$\leadsto$ &nbsp; $\sqrt{\dfrac{-\lVert \mk{s}-p\rVert^2}{-\lVert r-p\rVert^2}}=5/3$ &nbsp; is called the **time dilation factor** between A and B",
                r"$s$ = simultaneous to $r$ with respect to $q-p$<br>(A's point of view)",
            ),
            r"> > $\left(\Gamma=\dfrac{1}{\sqrt{1-\lVert\nu\rVert^2}}=\dfrac{1}{\sqrt{1-(4/5)^2}}=5/3\right)$",
        ],
        title="Twin paradox",
        label="ex-twins",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: relative velocity
    # definition: space of simultaneous events
    lk.definition(
        [
            r"Given a particle $\gamma:\mathbb R\longrightarrow\mathbb M^4$ &nbsp; ($\lVert\gamma'(t)\rVert^2=-1$)",
            r"$$\begin{aligned}S_{\gamma(t)}&=\gamma(t)+\gamma'(t)^\perp\\[0.3em]&=\textbf{space of simultaneous events}\text{ to }\gamma(t)\text{ relative to }\gamma'(t)\end{aligned}$$",
        ],
        label="def-simultaneous",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: relative velocity
    # in Galilean spacetime
    lk.prose(
        lk.aside(
            r"$\overset{\text{in }\mathbb G^4}{\leadsto}$ &nbsp; $S_{\gamma(t)}=\gamma(t)+\mk{\ker(\tau)}$",
            r"$\ker(\tau)$ independent from $\gamma$",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk, s_beta):
    # module: relative velocity
    # the velocity of one particle relative to another
    lk.prose(
        r"Given two particles $\gamma,\sigma$ &nbsp; $\left(\begin{matrix}\lVert\gamma'(t)\rVert^2=-1,\ \lVert\sigma'(s)\rVert^2=-1\\\gamma(0)=\sigma(0)=p,\ \gamma'(0)=u,\ \sigma'(0)=v\end{matrix}\right)$",
        r"The velocity of $\sigma$ relative to $\gamma$ at $p$ is the spacelike vector orthogonal to $u=\gamma'(0)$",
        lk.aside(
            r"$$\nu(u,v)=\mk{\frac{v}{-\eta(u,v)}-u}\in u^\perp$$",
            r"depends on $u$ and $v$",
        ),
        lk.interactive(lk.frame("L04-relvel", lk.H3D), controls=[s_beta]),
        lk.aside(
            r"$\overset{\text{in }\mathbb G^4}{\leadsto}$ &nbsp; $\nu(u,v)=\mk{v-u}$",
            r"independent of $u$<br>$\Rightarrow$ simple formula for the addition<br>of relative velocities $\Rightarrow$ broke Maxwell",
        ),
        r"$\Longrightarrow$ &nbsp; $\lVert\nu(u,v)\rVert^2=\dfrac{\lVert v\rVert^2}{\eta(u,v)^2}+\lVert u\rVert^2+2\,\dfrac{\eta(u,v)}{\eta(u,v)}=1+\dfrac{\lVert v\rVert^2}{\eta(u,v)^2}<1$",
        r"> $\leadsto$ &nbsp; relative speeds are bounded above (by 1)",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: relative velocity
    # for the twins
    lk.prose(
        r"For the twins &nbsp; $u=\begin{bmatrix}1\\ 0\end{bmatrix}$, &nbsp; $v=\begin{bmatrix} {\large\tfrac{5}{3}} \\[4pt] {\large\tfrac{4}{3}} \end{bmatrix}$",
        r"""
        > $\Longrightarrow$ &nbsp; $\eta(u,v)=-5/3$

        > $\Longrightarrow$ &nbsp; $\nu=\begin{bmatrix} 0 \\[4pt] {\large\tfrac{4}{5}} \end{bmatrix}$

        > $\Longrightarrow$ &nbsp; $\lVert\nu\rVert^2=16/25$
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: photons
    # definition: photon
    lk.definition(
        [
            r"A **photon** in $\mathbb M^4$ is a future oriented lightlike line",
            r"$$\xi(s)=p+s\,w\qquad(\lVert w\rVert^2=0\ \text{in the future cone})$$",
        ],
        label="def-photon",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: photons
    # the relative velocity of a photon
    lk.prose(
        r"The relative velocity of a photon relative to a particle $\gamma$ as above is",
        r"$$\nu(u,w)=\frac{w}{-\eta(u,w)}-u\in u^\perp$$",
        lk.aside(
            r"> $\Longrightarrow$ &nbsp; $\lVert\nu(u,w)\rVert^2=\mk{\dfrac{\lVert w\rVert^2}{\eta(u,w)^2}}+\lVert u\rVert^2+2\,\dfrac{\eta(u,w)}{\eta(u,w)}=1$ &nbsp; !",
            r"$\lVert w\rVert^2/\eta(u,w)^2=0$",
        ),
        lk.gap(),
        lk.aside(
            r"$\leadsto$ &nbsp; photons <span class='lk-mark'>achieve the maximal relative velocity</span>!",
            "with respect to EVERY other particle!",
        ),
        r"$\leadsto$ &nbsp; Minkowski geometry is not incompatible with Maxwell's electrodynamics (at least in principle)",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: photons
    # remark: Maxwell's equations
    lk.remark(
        [
            r"Maxwell's equations",
            lk.aside(
                r"$$\begin{cases}\underbrace{\partial_iB^i}_{\nabla\cdot B}=0\qquad&\underbrace{\epsilon^{ijk}\partial_jE_k}_{\nabla\times E}+\partial_0B^i=0\\[0.6em]\partial_iE^i=\rho&\epsilon^{ijk}\partial_jB_k-\partial_0E^i=J^i\end{cases}$$",
                "not invariant under change of<br>Galilean inertial frames …<br>(Galilean transformations)",
            ),
            r"have a very “simple” formulation in Minkowski spacetime",
            lk.aside(
                r"$$\begin{cases}\partial_\mu\tilde F^{\mu\nu}=0\\\partial_\mu F^{\mu\nu}=J^\nu\end{cases}$$",
                "invariant under change of<br>Minkowski inertial frame!<br>(Poincaré transformations)",
            ),
            r"$$F^{\mu\nu}=\begin{bmatrix}0&-E^1&-E^2&-E^3\\E^1&0&-B^3&B^2\\E^2&B^3&0&-B^1\\E^3&-B^2&B^1&0\end{bmatrix}\quad\tilde F^{\mu\nu}=\begin{bmatrix}0&-B^1&-B^2&-B^3\\B^1&0&E^3&-E^2\\B^2&-E^3&0&E^1\\B^3&E^2&-E^1&0\end{bmatrix}\quad J^\mu=\begin{bmatrix}\rho\\J^i\end{bmatrix}$$",
        ]
    )
    return


if __name__ == "__main__":
    app.run()
