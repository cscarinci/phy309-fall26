import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 3 · Minkowski geometry", css_file="lecturekit/style.css")


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
    lk.lecture(3, "Minkowski geometry")
    return


@app.cell(hide_code=True)
def _(lk, math, np):
    # Helpers of this lecture: the sketches in the shared sketch style, and the two 3D figures (the light
    # cone with u and u-perp, relative velocity), coordinates (x^1, x^2, time)
    sk = lk.sk
    K = "#000000"
    O3 = (0.0, 0.0, 0.0)

    def galilean_particle_sketch():
        # a particle gamma, its velocity gamma'(t), and tau taking it to R: one unit of time per unit of t
        fig, ax = sk.sketch((-1.6, 6.0), (-0.5, 3.9))
        s = np.linspace(-0.3, 3.6, 120)
        x = 0.9 * np.tanh(1.2 * (s - 1.6))
        ax.plot(x, s, color=lk.BLUE, lw=sk.LW + 0.2)
        p = np.array([0.0, 1.6])
        sk.maps(ax, tuple(p), (1.0, 2.43), color=lk.RED)
        sk.dot(ax, tuple(p), r"$\gamma(t)$", at=(0.25, -0.15), ha="left", va="top")
        sk.label(ax, (1.1, 2.6), r"$\gamma'(t)$", lk.RED, ha="left")
        sk.maps(ax, (2.1, 1.6), (3.6, 1.6), r"$\tau$", gap=0.3)
        ax.plot([4.6, 4.6], [-0.3, 3.4], color=K, lw=sk.LW)
        sk.maps(ax, (4.6, 3.2), (4.6, 3.6), color=K)
        sk.label(ax, (4.9, 3.6), r"$\mathbb{R}$", ha="left")
        sk.dot(ax, (4.6, 1.2))
        sk.maps(ax, (4.6, 1.2), (4.6, 2.2), color=lk.RED)
        ax.plot([5.0, 5.15, 5.15, 5.0], [1.2, 1.2, 2.2, 2.2], color=lk.RED, lw=1.2)
        sk.label(ax, (5.35, 1.7), r"$t$", lk.RED, ha="left")
        return fig

    def central_sketch():
        # the inertial source sigma and a particle gamma bending around it, with the force towards sigma
        fig, ax = sk.sketch((-2.4, 2.6), (-0.4, 4.0))
        ax.plot([0, 0], [-0.3, 3.8], color=K, lw=sk.LW)
        for y in (1.2, 2.4):
            sk.maps(ax, (0, y - 0.35), (0, y), color=K)
        y = np.linspace(-0.2, 3.6, 160)
        x = np.sqrt(0.55**2 + 0.9 * (y - 1.7) ** 2) - 0.0
        x = 0.55 + 0.55 * (y - 1.7) ** 2
        ax.plot(x, y, color=lk.BLUE, lw=sk.LW)
        sk.maps(ax, (0.55, 1.7), (0.05, 1.7), color=lk.RED)
        sk.label(ax, (0.2, 3.7), r"$\sigma$", ha="left")
        sk.label(ax, (0.75, 1.7), r"$\gamma$", lk.BLUE, ha="left")
        return fig

    def addition_sketch():
        # three particles through one event, their velocities, and the relative velocities between the tips
        fig, ax = sk.sketch((-2.6, 5.0), (-0.9, 4.2))
        tips = {"g": (-1.2, 2.4), "s": (1.0, 2.4), "x": (3.2, 2.4)}
        cols = {"g": lk.RED, "s": lk.BLUE, "x": lk.ORANGE}
        names = {"g": r"$\gamma$", "s": r"$\sigma$", "x": r"$\xi$"}
        for k, (a, b) in tips.items():
            t = np.linspace(-0.3, 1.45, 2)
            ax.plot(a * t, b * t, color=cols[k], lw=1.2)
            sk.maps(ax, (0, 0), (a, b), color=cols[k])
            sk.label(ax, (a * 1.52, b * 1.52), names[k], cols[k], va="bottom")
        sk.maps(ax, (-1.15, 2.4), (0.95, 2.4), color=lk.GREEN, lw=1.3)
        sk.maps(ax, (1.05, 2.4), (3.15, 2.4), color=lk.GREEN, lw=1.3)
        sk.maps(ax, (-1.15, 3.0), (3.15, 3.0), color=PLUM, lw=1.3)
        sk.dot(ax, (0, 0))
        sk.label(ax, (-0.05, 2.28), r"$\vec v(\gamma,\sigma)$", lk.GREEN, size=12, va="top")
        sk.label(ax, (2.05, 2.28), r"$\vec v(\sigma,\xi)$", lk.GREEN, size=12, va="top")
        sk.label(ax, (0.0, 3.1), r"$\vec v(\gamma,\xi)$", PLUM, size=12, va="bottom")
        return fig

    PLUM = "#7d6596"

    def particle_sketch():
        # the light cone at two events of a particle; the velocity is inside the upper cone
        fig, ax = sk.sketch((-1.8, 3.6), (-0.4, 4.0))
        s = np.linspace(0, 3.8, 200)
        ax.plot(0.12 * s**2, s, color=lk.BLUE, lw=sk.LW + 0.2)
        for y, n in ((0.9, "1"), (2.6, "2")):
            x0 = 0.12 * y**2
            for sg in (1, -1):
                ax.plot([x0 - 0.42, x0 + 0.42], [y - sg * 0.42, y + sg * 0.42], color=lk.GREY, lw=1.2)
                t = np.linspace(0, 2 * np.pi, 120)
                ax.plot(x0 + 0.42 * np.cos(t), y + sg * 0.42 + 0.09 * np.sin(t), color=lk.GREY, lw=1.2)
            d = np.array([0.24 * y, 1.0]) / np.hypot(0.24 * y, 1.0)
            sk.maps(ax, (x0, y), (x0 + 0.85 * d[0], y + 0.85 * d[1]), color=lk.GREEN)
            sk.dot(ax, (x0, y))
            sk.label(ax, (x0 + 0.55, y - 0.15), rf"$\gamma(s_{n})$", ha="left")
            sk.label(ax, (x0 + 0.85 * d[0] - 0.15, y + 0.85 * d[1] + 0.05), rf"$\gamma'(s_{n})$", lk.GREEN, ha="right", va="bottom")
        sk.label(ax, (0.12 * 3.8**2 + 0.1, 3.75), r"$\gamma$", lk.BLUE, ha="left")
        return fig

    def _flat(corners, fill=lk.LIGHT, edge=lk.GREY, alpha=0.6, lw=1.0):
        c = np.array(corners + [corners[0]], float)
        return lk.patch(corners, fill, alpha, n=24), (c[:, 0], c[:, 1], c[:, 2], edge, lw)

    def _curve(v, k, s):
        c = s[:, None] * np.asarray(v, float) + (s**2)[:, None] * np.asarray(k, float)
        return c[:, 0], c[:, 1], c[:, 2]

    def cone_scene(u0, u1):
        # the light cone in the coordinates (u^1, u^2, u^0), the vector u (coloured by its type) and the plane u-perp
        n = -(u0**2) + u1**2
        col = (lk.ORANGE if (u0, u1) != (0, 0) else K) if abs(n) < 1e-9 else (lk.BLUE if n < 0 else lk.RED)
        H = 2.2
        r, ph = np.meshgrid(np.linspace(0, H, 12), np.linspace(0, 2 * np.pi, 49), indexing="ij")
        surfaces = [lk.sheet(r * np.sin(ph), r * np.cos(ph), sg * r, alpha=0.2) for sg in (1, -1)]
        c = np.linspace(0, 2 * np.pi, 97)
        lines = [(H * np.sin(c), H * np.cos(c), sg * H + 0 * c, lk.GREY, 1.0) for sg in (1, -1)]
        texts = [
            ((0.0, 0.45, 1.6), r"\text{timelike}", lk.BLUE, 0, 0),
            ((0.0, 0.45, -1.6), r"\text{timelike}", lk.BLUE, 0, 0),
            ((0.0, 2.15, 0.95), r"\text{spacelike}", lk.RED, 0, 0),
            ((0.0, H, -H), r"\text{lightlike}", lk.ORANGE, 0, 12),
        ]
        if (u0, u1) != (0, 0):
            L = 1.4
            w = np.array([u0, 0.0, u1]) / max(abs(u0), abs(u1))
            w = w if w[0] >= 0 else -w
            j = np.array([0.0, 1.0, 0.0])
            corners = [tuple(L * (a * w + b * j)) for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            sf, ln = _flat(corners, fill="#dcebdf", edge=lk.GREEN, alpha=0.6, lw=1.2)
            surfaces.append(sf)
            lines.append(ln)
            texts.append((corners[1], r"\vec{u}^\perp", lk.GREEN, 180, 5))
        arrows = [(O3, (0.0, 0.0, 1.0), K, 1.0), (O3, (1.0, 0.0, 0.0), K, 1.0), (O3, (0.0, 1.0, 0.0), K, 1.0)]
        texts += [((0.0, 0.0, 1.0), r"\vec{e}_0", K, 180, 6), ((1.0, 0.0, 0.0), r"\vec{e}_i", K, -150, 7), ((0.0, 1.0, 0.0), r"\vec{e}_j", K, -90, 7)]
        if (u0, u1) != (0, 0):
            arrows.append((O3, (u1, 0.0, u0), col))
            rr = math.hypot(u0, u1)
            texts.append(((u1 * (1 + 0.14 / rr), 0.0, u0 * (1 + 0.14 / rr)), r"\vec{u}", col, math.degrees(math.atan2(u0, u1)), 0))
        return lk.turntable(
            55,
            20,
            "the light cone in the coordinates u^0, u^1, u^2, the vector u and the plane u-perp",
            [lk.panel(1.0, surfaces=surfaces, lines=lines, arrows=arrows, points=[(O3, K, 3.0)], texts=texts, outlines=[("cone", (0, 0, 0), H, lk.GREY, 1.0)], box=((-2.5, 2.6), (-2.4, 2.6), (-2.5, 2.7)))],
            height=lk.H3D,
            key="L03-cone",
            zoom=1.3,
            apart=True,
            bias=0.12,
        )

    def relvel_scene():
        # two particles through one event, gamma' and sigma', the plane (gamma')^perp and the relative velocity
        gs, ss = np.array([-0.4, 0.1]), np.array([0.25, 0.55])
        g = np.array([*gs, np.sqrt(1 + gs @ gs)])
        sg = np.array([*ss, np.sqrt(1 + ss @ ss)])
        eta = -g[2] * sg[2] + gs @ ss
        sc = sg / -eta
        v = sc - g

        def gap(a, b):
            d = (b - a) / np.linalg.norm(b - a)
            return tuple(a + 0.03 * d), tuple(b - 0.03 * d)

        s = np.linspace(-0.35, 1.15, 80)
        cg, cs = _curve(g, (0.06, -0.12, 0), s), _curve(sg, (-0.04, 0.1, 0), s)

        def perp(a, b):
            return (a, b, (g[0] * a + g[1] * b) / g[2])

        sf, ln = _flat([perp(0.8, -0.45), perp(0.8, 0.75), perp(-0.45, 0.75), perp(-0.45, -0.45)])
        return lk.turntable(
            -30,
            18,
            "two particles through one event, gamma' and sigma', the plane orthogonal to gamma' and the relative velocity",
            [
                lk.panel(
                    1.0,
                    surfaces=[sf],
                    lines=[ln, (*cg, lk.RED, 1.6), (*cs, lk.BLUE, 1.6)],
                    arrows=[(O3, tuple(g), lk.RED), (O3, tuple(sg), lk.BLUE), (*gap(g, sc), lk.ORANGE), (O3, tuple(v), lk.ORANGE)],
                    points=[(O3, K, 3.4)],
                    texts=[
                        ((cg[0][0], cg[1][0], cg[2][0]), r"\gamma", lk.RED, -90, 4),
                        ((cs[0][0], cs[1][0], cs[2][0]), r"\sigma", lk.BLUE, -90, 4),
                        (tuple(0.5 * g), r"\gamma'", lk.RED, 180, 7),
                        (tuple(0.6 * sg), r"\sigma'", lk.BLUE, 0, 8),
                        (perp(-0.45, -0.45), r"(\gamma')^\perp", lk.GREY, 180, 5),
                        (tuple(1.06 * v), r"\vec{v}(\gamma, \sigma)", lk.ORANGE, -10, 2),
                    ],
                )
            ],
            height=lk.H3D,
            width=440,
            bias=0.12,
            zoom=1.2,
        )

    return addition_sketch, central_sketch, cone_scene, galilean_particle_sketch, particle_sketch, relvel_scene


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figure (values hidden)
    s_u0 = lk.slider(-2.0, 2.0, step=0.1, value=1.6, label="$u^0$", show_value=False)
    s_u1 = lk.slider(-2.0, 2.0, step=0.1, value=0.6, label="$u^i$", show_value=False)
    return s_u0, s_u1


@app.cell(hide_code=True)
def _(cone_scene, s_u0, s_u1):
    # the scene of the light cone figure, redrawn by its sliders; its frame is in the block on timelike vectors
    cone_scene(s_u0.value, s_u1.value)
    return


@app.cell(hide_code=True)
def _(central_sketch, galilean_particle_sketch, lk):
    # module: recap
    # recap
    lk.recap(
        r"$\mathbb G^4=(\mathbb A^4,\mathbb V^4,-)$ &nbsp; 4d affine space",
        r"$\tau:\mathbb V^4\longrightarrow\mathbb R$ &nbsp; universal time function",
        r"$\langle\ ,\ \rangle:\ker\tau\times\ker\tau\longrightarrow\mathbb R$ &nbsp; spatial inner product",
        lk.aside(
            r"$\gamma:\mathbb R\longrightarrow\mathbb G^4$, &nbsp; $\tau(\gamma'(t))=1$ &nbsp; <span class='lk-mark'>particle</span>",
            "parameterized by absolute time",
        ),
        lk.figure(galilean_particle_sketch()),
        r"Newton's law",
        r"$$\gamma''(t)=\frac{1}{m}\vec F(t),\qquad\vec F(t)\in\ker\tau.$$",
        lk.aside(r"> $\leadsto$ &nbsp; inertial motion", r"$\vec F(t)=0$"),
        r"> > $\gamma(t)=p+t\,\vec u$, &nbsp; $\tau(\vec u)=1$",
        lk.aside(r"> $\leadsto$ &nbsp; uniformly accelerating", r"$\vec F(t)=\vec g$"),
        r"> > $\gamma(t)=p+t\,\vec u+\tfrac12t^2\,\vec g$, &nbsp; $\tau(\vec u)=1$, &nbsp; $\tau(\vec g)=0$",
        lk.aside(r"> $\leadsto$ &nbsp; central motion", r"$\vec F(t)=-\kappa\,\dfrac{\gamma(t)-\sigma(t)}{\lVert\gamma(t)-\sigma(t)\rVert^3}$<br>$\sigma(t)=q+t\,\vec u$, &nbsp; $\tau(\vec u)=1$ &nbsp; inertial"),
        r"""
        > > $\gamma(t)=\sigma(t)+r(t)\big(\vec v\cos\varphi(t)+\vec w\sin\varphi(t)\big)$

        > > <span class='lk-ghost'>$\gamma(t)=$</span>$\tau(\vec v)=\tau(\vec w)=0$, &nbsp; $\langle\vec v,\vec w\rangle=0$, &nbsp; $\lVert\vec v\rVert=\lVert\vec w\rVert=1$
        """,
        lk.aside(
            r"> > > $\leadsto$ &nbsp; $\begin{cases}\varphi'=\dfrac{L}{r^2}\\(r')^2=2\mathcal E+\dfrac{2\kappa}{mr}-\dfrac{L^2}{r^2}\end{cases}$",
            r"conics in the $\vec v,\vec w$ plane:<br>&emsp;&emsp;$\mathcal E<0$ ellipses<br>&emsp;&emsp;$\mathcal E=0$ parabolas<br>&emsp;&emsp;$\mathcal E>0$ hyperbolas<br>here we are assuming $\kappa>0$,<br>otherwise only hyperbolas!",
        ),
        lk.figure(central_sketch()),
        topic="Galilean spacetime",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("Schutz 1.1–1.7; Carroll 1.2; Sasane 12.2")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Maxwell in Galilean spacetime
    # what central forces cover, and what they don't
    lk.prose(
        lk.aside(
            r"$\leadsto$ &nbsp; central forces cover Newton's gravity and Coulomb's electrostatics",
            r"for inertial $\sigma(t)$",
        ),
        r"$\leadsto$ &nbsp; in principle, Newton's gravity can have non-inertial sources in Galilean spacetime",
        r"$\leadsto$ &nbsp; however, Maxwell's electrodynamics is incompatible with Galilean spacetime …",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Maxwell in Galilean spacetime
    # Maxwell's equations in an inertial frame
    lk.prose(
        r"Fix an inertial frame &nbsp; $\vec e_0,\vec e_i$",
        lk.aside(
            r"> $\leadsto$ &nbsp; $\vec F=q\,\big(\mk{\vec E_\sigma+\vec v_\gamma\times\vec B_\sigma}\big)$",
            "measured in the inertial frame",
        ),
        lk.aside(
            r"$$\begin{aligned}\nabla\cdot\vec E_\sigma&=\rho_\sigma/\varepsilon_0\\\nabla\cdot\vec B_\sigma&=0\\\nabla\times\vec E_\sigma+\partial_t\vec B_\sigma&=\vec0\\\nabla\times\vec B_\sigma-\tfrac{1}{c^2}\partial_t\vec E_\sigma&=\mu_0\vec J_\sigma\end{aligned}$$",
            "Maxwell's equations:<br>depend on the choice of inertial frame …",
        ),
        r"In the vacuum",
        r"$$\Big(\Delta-\frac{1}{c^2}\partial_t^2\Big)\vec E=0=\Big(\Delta-\frac{1}{c^2}\partial_t^2\Big)\vec B.$$",
        lk.aside(
            r"> $\Longrightarrow$ &nbsp; electromagnetic “waves” propagate at a <span class='lk-mark'>constant speed $c$</span> (speed of light)",
            r"experimentally: $c$ is independent<br>of choice of inertial frame",
        ),
    )
    return


@app.cell(hide_code=True)
def _(addition_sketch, lk):
    # module: Maxwell in Galilean spacetime
    # theorem: relative velocities add
    lk.theorem(
        [
            r"Given $\gamma,\sigma,\xi$ any three particles in $\mathbb G^4$",
            r"$$\begin{aligned}\vec v(\gamma,\xi)&=\xi'-\gamma'=(\xi'-\sigma')+(\sigma'-\gamma')\\[0.3em]&=\vec v(\sigma,\xi)+\vec v(\gamma,\sigma).\end{aligned}$$",
            lk.figure(addition_sketch()),
        ],
        label="thm-galilean-addition",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Maxwell in Galilean spacetime
    # the contradiction with experiment
    lk.prose(
        r"If $\gamma,\sigma,\xi$ move in the same direction, &nbsp; $\gamma,\sigma$ inertial, &nbsp; $\xi$ particle of light",
        lk.aside(r"> $\Longrightarrow$ &nbsp; $c=\lVert\vec v(\gamma,\sigma)\rVert+c$", "experimental contradiction"),
        r"$\leadsto$ &nbsp; our solution will be to consider a new geometry for spacetime",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    lk.section("Minkowski geometry")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Minkowski spacetime
    # the geometry of special relativity
    lk.prose(r"$\leadsto$ &nbsp; geometry of special relativity")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Minkowski spacetime
    # definition: Minkowski spacetime
    lk.definition(
        [
            r"The **Minkowski spacetime** is a 4-dimensional affine space",
            r"$$\mathbb M^4=(\mathbb A^4,\mathbb V^4,-),$$",
            r"together with a **Minkowski inner product**",
            r"$$\eta:\mathbb V^4\times\mathbb V^4\longrightarrow\mathbb R,$$",
            lk.aside(
                r"> symmetric, bilinear, <span class='lk-mark'>signature $(3,1)$</span>",
                "replacement for positive definiteness<br>of the Euclidean inner product",
            ),
        ],
        label="def-minkowski",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Minkowski spacetime
    # definition: signature (3,1)
    lk.definition(
        [
            r"A symmetric bilinear function",
            r"$$\eta:\mathbb V^4\times\mathbb V^4\longrightarrow\mathbb R,$$",
            r"has **signature $(3,1)$** if",
            r"> • &nbsp; there exists $\vec u\in\mathbb V$ with $\eta(\vec u,\vec u)<0$",
            lk.aside(
                r"> • &nbsp; the restriction of $\eta$ to $\mk{\vec u^\perp}$ is positive definite",
                r"$\vec u^\perp=\{\vec v\in\mathbb V^4\mid\eta(\vec u,\vec v)=0\}$",
            ),
        ],
        label="def-signature",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Minkowski spacetime
    # copies of Euclidean space
    lk.prose(
        r"$\leadsto$ &nbsp; in $\mathbb G^4$, $\ker(\tau)$ had a Euclidean inner product",
        r"> $\Longrightarrow$ &nbsp; we had copies of $\mathbb E^3$ through each $p\in\mathbb G^4$ &nbsp;&nbsp; $S_p=p+\ker(\tau)\approx\mathbb E^3$",
        r"$\leadsto$ &nbsp; in $\mathbb M^4$, for each $\vec u\in\mathbb V^4$ with $\eta(\vec u,\vec u)<0$, $\vec u^\perp$ has a Euclidean inner product",
        r"> $\Longrightarrow$ &nbsp; we get copies of $\mathbb E^3$ through each $p\in\mathbb M^4$, for each such vector $\vec u$",
        r"$$S_p^{\vec u}=p+\vec u^\perp\approx\mathbb E^3$$",
    )
    return


@app.cell(hide_code=True)
def _(lk, s_u0, s_u1):
    # module: Minkowski spacetime
    # definition: timelike, spacelike, lightlike
    lk.module(
        lk.definition(
            [
                r"Non-zero 4-vectors $\vec u\in\mathbb V$ are called",
                lk.aside(
                    r"$$\begin{array}{lll}\textbf{timelike}&\text{if}&\lVert\vec u\rVert^2<0\\\textbf{spacelike}&\text{if}&\lVert\vec u\rVert^2>0\\\textbf{lightlike}&\text{if}&\lVert\vec u\rVert^2=0.\end{array}$$",
                    r"$\lVert\vec u\rVert^2=\eta(\vec u,\vec u)$",
                    at="middle",
                ),
            ],
            label="def-causal-character",
        ),
        lk.prose(lk.interactive(lk.frame("L03-cone", lk.H3D), controls=[s_u0, s_u1])),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Minkowski spacetime
    # inertial frames and Cartesian coordinates
    lk.prose(
        r"$\leadsto$ &nbsp; choose &nbsp; $o\in\mathbb M^4$, &nbsp; $\left.\begin{aligned}&\vec e_0\in\mathbb V^4\text{ with }\lVert\vec e_0\rVert^2=-1\\&\vec e_1,\vec e_2,\vec e_3\in\vec e_0^{\,\perp}\text{ with }\eta(\vec e_i,\vec e_j)=\delta_{ij}\end{aligned}\right\}$ &nbsp; inertial frame",
        r"> $\Longrightarrow$ &nbsp; $p=o+p^0\vec e_0+\underbrace{p^i\vec e_i}_{\footnotesize\begin{matrix}\text{sum over}\\i=1,2,3\end{matrix}}=o+\underbrace{p^\mu\vec e_\mu}_{\footnotesize\begin{matrix}\text{sum over}\\\mu=0,1,2,3\end{matrix}}\in\mathbb M^4$ &nbsp; (Cartesian coordinates)",
        r"> $\Longrightarrow$ &nbsp; $\vec u=u^0\vec e_0+u^i\vec e_i=u^\mu\vec e_\mu\in\mathbb V^4$",
        r"$$\lVert\vec u\rVert^2=\underbrace{-(u^0)^2}_{\footnotesize\begin{matrix}\text{negative sign}\\(\text{signature }(0,1))\end{matrix}}+\underbrace{(u^1)^2+(u^2)^2+(u^3)^2}_{\footnotesize\begin{matrix}\text{same as Euclidean}\\(\text{signature }(3,0))\end{matrix}}$$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: causal structure
    # definition: causal structure
    lk.definition(
        r"""
        • &nbsp; $q$ is **in the future** (past) **of** $p$ &nbsp; if $q-p$ is timelike in “upper” (“lower”) cone

        • &nbsp; $p,q$ are **spacelike separated** &nbsp; if $q-p$ is spacelike
        """,
        title=r"Causal structure in $\mathbb M^4$",
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

        > > $\mathrm{time}(p,q)=\pm\sqrt{-\lVert q-p\rVert^2}$ &nbsp; (**proper time** from $p$ to $q$)

        > • &nbsp; if $p,q$ are spacelike separated

        > > $\mathrm{dist}(p,q)=\sqrt{\lVert q-p\rVert^2}$ &nbsp; (**proper distance** from $p$ to $q$)
        """,
        label="def-proper-time-distance",
    )
    return


@app.cell(hide_code=True)
def _(lk, particle_sketch):
    # module: particles and simultaneity
    # definition: particle
    lk.module(
        lk.definition(
            [
                lk.aside(
                    r"A **particle** in $\mathbb M^4$ is a parameterized curve &nbsp; $\gamma:\mathbb R\longrightarrow\mathbb M^4$ &nbsp; such that $\gamma'(s)$ is timelike and <span class='lk-mark'>future oriented</span>.",
                    "always pointing to the<br>upper side of the cone",
                ),
            ],
            label="def-particle",
        ),
        lk.prose(lk.figure(particle_sketch())),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: particles and simultaneity
    # inertial particles
    lk.prose(
        lk.aside(
            r"An inertial particle is a straight future oriented timelike line &nbsp; $\gamma(s)=p+s\,\mk{\vec u}$",
            r"$\vec u$ timelike, &nbsp; $\vec u$ future oriented",
        ),
        lk.aside(
            r"> $\Longrightarrow$ &nbsp; simultaneity of events depends on the choice of an <span class='lk-mark'>inertial particle</span>",
            "inertial particle = inertial observer",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: particles and simultaneity
    # definition: events simultaneous to p
    lk.definition(
        [
            r"Given $p\in\mathbb M^4$, and $\vec u\in\mathbb V^4$ timelike",
            r"$$S_p^{\vec u}=\{q\in\mathbb M^4\mid q-p\in\vec u^\perp\},$$",
            r"is the **set of events simultaneous to $p$** relative to the inertial observer &nbsp; $\gamma(s)=p+s\,\vec u$",
        ],
        label="def-simultaneous",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: particles and simultaneity
    # relative simultaneity and Maxwell
    lk.prose(
        r"$\leadsto$ &nbsp; it will be this relative notion of simultaneity which will allow us to formulate Maxwell's theory<br>consistently with spacetime geometry!"
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: proper time
    # proposition: proper time parameterization
    lk.proposition(
        r"Every particle $\gamma:\mathbb R\longrightarrow\mathbb M^4$ can be parameterized by a “proper time” parameter $t$ &nbsp; such that &nbsp; $\lVert\gamma'(t)\rVert^2=-1$.",
        label="prop-proper-time",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: proper time
    # recall: absolute time in Galilean spacetime
    lk.prose(
        r"In $\mathbb G^4$, “absolute time” was defined such that $\tau(\gamma'(t))=1$",
        r"> $\displaystyle\begin{aligned}\leadsto\quad\mathrm{time}(\gamma(t_1),\gamma(t_2))&=\int_{t_1}^{t_2}\tau(\gamma'(t))\,dt\\[0.3em]&=(t_2-t_1)=\tau(\gamma(t_2)-\gamma(t_1))\end{aligned}$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: proper time
    # definition: proper time along a particle
    lk.definition(
        [
            r"The **proper time** along a particle $\gamma:\mathbb R\longrightarrow\mathbb M^4$ is",
            lk.aside(
                r"$$\begin{aligned}\mathrm{time}_\gamma(\gamma(t_1),\gamma(t_2))&=\int_{t_1}^{t_2}\sqrt{-\lVert\gamma'(t)\rVert^2}\,dt\\[0.3em]&=t_2-t_1\ \mk{\leq}\ \sqrt{-\lVert\gamma(t_2)-\gamma(t_1)\rVert^2}.\end{aligned}$$",
                r"$\leq$: with equality iff $\gamma$ is inertial!",
                at="last",
            ),
        ],
        label="def-proper-time-along",
    )
    return


@app.cell(hide_code=True)
def _(lk, relvel_scene):
    # module: relative velocity
    # definition: relative velocity
    lk.module(
        lk.definition(
            [
                r"Given two particles $\gamma,\sigma$ &nbsp; (with $\lVert\gamma'\rVert^2=\lVert\sigma'\rVert^2=-1$)",
                r"the **relative velocity** of $\sigma$ with respect to $\gamma$ is the spacelike vector orthogonal to $\gamma'$",
                r"$$\vec v(\gamma,\sigma)=\frac{\sigma'}{-\eta(\gamma',\sigma')}-\gamma'\in(\gamma')^\perp.$$",
            ],
            label="def-relative-velocity",
        ),
        lk.prose(lk.figure(relvel_scene())),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: relative velocity
    # theorem: relative speeds are bounded
    lk.theorem(
        r"$$\begin{aligned}\lVert\vec v(\gamma,\sigma)\rVert^2&=\frac{\lVert\sigma'\rVert^2}{\eta(\gamma',\sigma')^2}+\lVert\gamma'\rVert^2+\frac{2\,\eta(\gamma',\sigma')}{\eta(\gamma',\sigma')}\\[0.3em]&=1-\Big(\frac{1}{\eta(\gamma',\sigma')}\Big)^2<1\end{aligned}$$",
        label="thm-speed-bound",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: relative velocity
    # consequences: a maximal speed
    lk.prose(
        r"""
        $\Longrightarrow$ &nbsp; relative velocities in Minkowski spacetime are bounded from above!

        > $\leadsto$ &nbsp; max speed $=$ speed of light

        > $\leadsto$ &nbsp; every inertial observer agrees!
        """
    )
    return


if __name__ == "__main__":
    app.run()
