import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 15 · Lorentzian metrics", css_file="lecturekit/style.css")


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
    lk.lecture(15, "Lorentzian metrics")
    return


@app.cell(hide_code=True)
def _(lk, mo, np):
    # Helpers of this lecture: the six figures

    def _sphere():
        s, t = np.meshgrid(np.linspace(0, np.pi, 25), np.linspace(0, 2 * np.pi, 97), indexing="ij")
        return lk.sheet(np.sin(s) * np.cos(t), np.sin(s) * np.sin(t), np.cos(s), alpha=0.45)

    SPHERE_OUTLINE = ("sphere", (0, 0, 0), 1.0, lk.GREY, 1.0)

    def light_cone(t0, x0=0.0, y0=0.0, h=1.0, rim=1.2):
        # the double cone of slope 1 with vertex (x0, y0, t0) and height h on each side, with its two rims
        s, a = np.meshgrid(np.linspace(-h, h, 21), np.linspace(0, 2 * np.pi, 49), indexing="ij")
        return lk.sheet(x0 + np.abs(s) * np.cos(a), y0 + np.abs(s) * np.sin(a), t0 + s, wire=[(0, 20, lk.GREY, rim)], alpha=0.3, tone=lk.GREY), ("cone", (x0, y0, t0), h, lk.GREY, rim)

    def stereographic_scene():
        # the angles of psi, and the projections of phi_n and phi_s
        ph, th = np.radians(40), np.radians(45)
        P = np.array([np.sin(ph) * np.cos(th), np.sin(ph) * np.sin(th), np.cos(ph)])
        Q = np.array([np.cos(th), np.sin(th), 0.0]) / np.tan(ph / 2)  # (u, v, 0)
        I = np.array([np.cos(th), np.sin(th), 0.0]) * np.tan(ph / 2)  # (u~, v~, 0)
        n, sp, o = np.array([0.0, 0.0, 1.0]), np.array([0.0, 0.0, -1.0]), np.zeros(3)
        plane = [(-1.4, -1.4, 0), (2.3, -1.4, 0), (2.3, 2.5, 0), (-1.4, 2.5, 0)]
        s = np.linspace(0, 1, 40)[:, None]
        t = np.linspace(0, 1, 30)[:, None]
        a = np.linspace(0, 1, 40)
        eq = np.linspace(0, 2 * np.pi, 121)
        edge = np.array(plane + plane[:1])
        k = np.array([-1.0, 1.0])
        ar = 0.2  # radius of the arc of theta
        return lk.turntable(
            -10,
            40,
            "the unit sphere with the plane z = 0, the angles phi and theta of a point of the sphere, the line from the top of the sphere n through that point to (u, v, 0), and the dashed line from the bottom of the sphere s to that point, which meets the plane at (u~, v~, 0)",
            [
                lk.panel(
                    1.0,
                    surfaces=[_sphere(), lk.patch(plane, "#ececec", 0.6, n=16)],
                    outlines=[SPHERE_OUTLINE],
                    lines=[
                        (*(sp + t * (P - sp)).T, lk.BLUE, 2.0, [6, 4], 2.5),
                        (*edge.T, lk.GREY, 1.2),
                        (np.cos(eq), np.sin(eq), 0 * eq, lk.GREY, 1.0),
                        (0 * k, 0 * k, k, lk.GREY, 1.0),
                        (*(o + s * (Q - o)).T, lk.GREY, 1.0),
                        (*(n + s * (Q - n)).T, lk.BLUE, 2.0, None, 2.5),
                        (*(o + s * (P - o)).T, lk.ORANGE, 1.8),
                        (0.3 * np.sin(ph * a) * np.cos(th), 0.3 * np.sin(ph * a) * np.sin(th), 0.3 * np.cos(ph * a), lk.ORANGE, 1.4),
                        (ar * np.cos(th * a), ar * np.sin(th * a), 0 * a, lk.ORANGE, 1.4),
                    ],
                    points=[(tuple(sp), "#000000", 3.4), (tuple(I), lk.BLUE, 4.0, True), (tuple(n), "#000000", 3.4), (tuple(P), "#000000", 3.4), (tuple(Q), lk.BLUE, 4.0), (tuple(o), "#000000", 2.6)],
                    axes=[((0, 0, 0), (0.6, 0, 0), "e_1", 180), ((0, 0, 0), (0, 0.6, 0), "e_2", 90), ((0, 0, 0), (0, 0, 0.6), "e_3", 150)],
                    texts=[
                        (tuple(0.5 * np.array([np.sin(ph / 2) * np.cos(th), np.sin(ph / 2) * np.sin(th), np.cos(ph / 2)])), r"\phi", lk.ORANGE, 0, 0),
                        ((ar * np.cos(th / 2), ar * np.sin(th / 2), 0), r"\theta", lk.ORANGE, -60, 5),
                        (tuple(Q), "(u, v, 0)", "#000000", 30, 7),
                        (tuple(P), "(x, y, z)", "#000000", 60, 9),
                        (tuple(n), "n", "#000000", 90, 6),
                        (tuple(sp), "s", "#000000", -90, 6),
                        (tuple(I), r"(\tilde u, \tilde v, 0)", "#000000", 20, 16),
                    ],
                )
            ],
            height=380,
            bias=0.12,
            zoom=1.2,
        )

    def latitude_scene():
        # the latitude z = cos(phi_0)
        ph = np.radians(50)
        t = np.linspace(0, 2 * np.pi, 121)
        k = np.array([-1.0, 1.0])
        return lk.turntable(
            20,
            15,
            "the unit sphere with its poles n and s and the circle z = cos(phi_0)",
            [
                lk.panel(
                    1.0,
                    surfaces=[_sphere()],
                    outlines=[SPHERE_OUTLINE],
                    lines=[(np.sin(ph) * np.cos(t), np.sin(ph) * np.sin(t), np.cos(ph) + 0 * t, lk.BLUE, 2.4), (0 * k, 0 * k, k, lk.GREY, 1.0)],
                    points=[((0, 0, 1), "#000000", 3.4), ((0, 0, -1), "#000000", 3.4), ((0, 0, 0), lk.GREY, 2.6), ((0, 0, np.cos(ph)), lk.BLUE, 2.6)],
                    axes=[((0, 0, 0), (1.4, 0, 0), "x", 208), ((0, 0, 0), (0, 1.4, 0), "y", -8), ((0, 0, 0), (0, 0, 1.4), "z", 90)],
                    texts=[
                        ((0, 0, 1), "n", "#000000", 180, 8),
                        ((0, 0, -1), "s", "#000000", -90),
                        ((0, 0, np.cos(ph)), r"z = \cos(\phi_0)", lk.BLUE, 0, 128),
                    ],
                    box=((-0.85, 0.85), (-0.85, 0.85), (-0.85, 0.85)),
                )
            ],
            height=300,
            width=380,
        )

    def cone_vector(deg):
        # the vector X in the drawing makes the angle deg with the t axis, on the left of the screen: 0..180 turns it from
        # the future cone, through the cone (45), outside it, through the cone again (135), into the past cone
        right = np.array([-np.sin(np.radians(25)), np.cos(np.radians(25)), 0.0])  # right on the screen in the first view
        a = np.radians(deg)
        e0 = 0.26 * right + np.array([0, 0, 0.62])
        X = 0.87 * (-np.sin(a) * right + np.array([0, 0, np.cos(a)]))
        return e0, X

    def cone_kind(deg):
        # what X is, as written under the slider
        e0, X = cone_vector(deg)
        eta = lambda p, q: -p[2] * q[2] + p[0] * q[0] + p[1] * q[1]
        xx, ex = eta(X, X), eta(e0, X)
        side = "future" if ex < 0 else "past"
        sign = "<" if ex < 0 else ">"
        if abs(xx) < 1e-9:
            return rf"$\eta(X,X)=0$ &nbsp; and &nbsp; $\eta(e_0,X){sign}0$ &nbsp; $\Longrightarrow$ &nbsp; $X$ lightlike, {side}"
        if xx < 0:
            return rf"$\eta(X,X)<0$ &nbsp; and &nbsp; $\eta(e_0,X){sign}0$ &nbsp; $\Longrightarrow$ &nbsp; $X$ timelike, {side}"
        return r"$\eta(X,X)>0$ &nbsp; $\Longrightarrow$ &nbsp; $X$ spacelike"

    def cone_scene(deg):
        s, o = light_cone(0.0)
        e0, X = cone_vector(deg)
        return lk.turntable(
            25,
            12,
            "the lightcone at a point, with the timelike vector e_0 and a vector X in the chosen direction: inside the upper half of the cone, on it, outside it, or inside its lower half",
            [lk.panel(1.0, surfaces=[s], outlines=[o], arrows=[((0, 0, 0), tuple(e0), lk.ORANGE), ((0, 0, 0), tuple(X), lk.BLUE)], points=[((0, 0, 0), "#000000", 3.0)], texts=[(tuple(e0), "e_0", lk.ORANGE, 0), (tuple(X), "X", lk.BLUE, 180)])],
            height=300,
            width=420,
            key="L15-cone",
            apart=True,
        )

    def orientation_figure():
        # a time orientation on M; a flat drawing with nothing to turn
        def xy(x, y):
            return x * 112 + 215, 160 - y * 112

        def path(xs, ys, close=False):
            pts = [xy(x, y) for x, y in zip(xs, ys)]
            return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + (" Z" if close else "")

        a = np.linspace(0, 2 * np.pi, 241)
        r = 1 + 0.08 * np.cos(2 * a + 1) + 0.06 * np.cos(3 * a + 2.4) + 0.04 * np.sin(5 * a)
        blob = path(1.4 * r * np.cos(a), 1.05 * r * np.sin(a), close=True)
        yy = np.linspace(-1.3, 1.3, 100)
        curves = "".join(f'<path d="{path(c - 0.35 * yy - 0.06 * yy**2, yy)}" fill="none" stroke="{lk.BLUE}" stroke-width="1.5"/>' for c in (-0.9, -0.45, 0.0, 0.45, 0.9))

        def on(c, y):
            return np.array([c - 0.35 * y - 0.06 * y**2, y])

        arrows = []
        for c, y0, dy in ((-0.9, -0.3, 0.36), (-0.45, -0.6, 0.36), (-0.45, 0.25, 0.36), (0.0, -0.8, 0.36), (0.0, 0.05, 0.36), (0.45, -0.5, 0.36), (0.45, 0.35, 0.36), (0.9, -0.45, 0.36), (0.9, 0.2, 0.36)):
            x1, y1 = xy(*on(c, y0))
            x2, y2 = xy(*on(c, y0 + dy))
            u = np.array([x2 - x1, y2 - y1]) / np.hypot(x2 - x1, y2 - y1)
            b = np.array([x2, y2]) - 9 * u
            w = 3.4 * np.array([-u[1], u[0]])
            arrows.append(
                f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{lk.ORANGE}" stroke-width="2.2" stroke-linecap="round"/>'
                f'<polygon points="{x2:.1f},{y2:.1f} {b[0] + w[0]:.1f},{b[1] + w[1]:.1f} {b[0] - w[0]:.1f},{b[1] - w[1]:.1f}" fill="{lk.ORANGE}"/>'
            )
        return mo.Html(f"""
        <svg viewBox="0 0 430 320" role="img" aria-label="a region M filled with curves and with timelike arrows pointing roughly in the same direction" style="display: block; margin: 0 auto; width: 100%; max-width: 360px; height: auto">
          <defs><clipPath id="L15-blob"><path d="{blob}"/></clipPath></defs>
          <g clip-path="url(#L15-blob)">{curves}</g>
          {''.join(arrows)}
          <path d="{blob}" fill="none" stroke="{lk.GREY}" stroke-width="1.8"/>
          <text x="392" y="48" font-size="21" style="font-family: KaTeX_Math, serif; font-style: italic" text-anchor="middle">M</text>
        </svg>
        """)

    def particle_scene():
        # a particle with light cones at three events, the middle one tilted
        a0 = np.radians(30)
        right, deep, up = np.array([-np.sin(a0), np.cos(a0), 0.0]), np.array([np.cos(a0), np.sin(a0), 0.0]), np.array([0.0, 0.0, 1.0])

        def gamma(t):
            t = np.asarray(t, float)
            return (0.6 * (1 + np.tanh((t - 1.2) / 0.8)))[..., None] * right + (0.15 * (1 - np.cos(0.8 * t)))[..., None] * deep + t[..., None] * up

        def velocity(t):
            return 0.75 / np.cosh((t - 1.2) / 0.8) ** 2 * right + 0.12 * np.sin(0.8 * t) * deep + up

        def tilted(p, tau, h):
            # the double cone with vertex p, of height h on each side, its axis leaning by tau to the right of the first view
            axis, across = np.cos(tau) * up + np.sin(tau) * right, np.cos(tau) * right - np.sin(tau) * up
            s, a = np.meshgrid(np.linspace(-h, h, 21), np.linspace(0, 2 * np.pi, 49), indexing="ij")
            q = p + s[..., None] * axis + (np.abs(s) * np.cos(a))[..., None] * across + (np.abs(s) * np.sin(a))[..., None] * deep
            return lk.sheet(q[..., 0], q[..., 1], q[..., 2], wire=[(0, 20, lk.GREY, 1.0)], alpha=0.3, tone=lk.GREY)

        c = gamma(np.linspace(-0.3, 3.5, 200))
        low, mid, top = gamma(0.4), gamma(1.6), gamma(2.8)
        tip = low + 0.6 * velocity(0.4)
        cl, ct = light_cone(low[2], low[0], low[1], h=0.4, rim=1.0), light_cone(top[2], top[0], top[1], h=0.4, rim=1.0)
        return lk.turntable(
            30,
            12,
            "a particle gamma with light cones at three events, the middle cone tilted, and its velocity gamma' at the lowest event",
            [
                lk.panel(
                    1.0,
                    surfaces=[cl[0], tilted(mid, np.radians(25), 0.4), ct[0]],
                    outlines=[cl[1], ct[1]],
                    lines=[(*c.T, lk.BLUE, 1.8)],
                    arrows=[(tuple(low), tuple(tip), lk.ORANGE)],
                    points=[(tuple(low), lk.BLUE, 3.4)],
                    texts=[(tuple(low), r"\gamma(t)", "#000000", 0, 14), (tuple(tip), r"\gamma'(t)", lk.ORANGE, 180)],
                )
            ],
            height=380,
            width=460,
        )

    def schwarzschild_scene():
        # the two lines of the sketch drawn as the cylinder r = r_0, with the sphere at r = r_0, t = 0
        s, a = np.meshgrid(np.linspace(-1.0, 1.6, 14), np.linspace(0, 2 * np.pi, 49), indexing="ij")
        ang = np.linspace(0, 2 * np.pi, 121)
        k = np.array([-1.0, 0.0])
        return lk.turntable(
            25,
            14,
            "the cylinder r = r_0, the outside region M, and the sphere at r = r_0, t = 0",
            [
                lk.panel(
                    1.0,
                    surfaces=[lk.sheet(np.cos(a), np.sin(a), s, alpha=0.3, tone=lk.RED)],
                    outlines=[("cylinder", (0, 0), 1.0, (-1.0, 1.6), lk.RED, 1.2)],
                    lines=[(np.cos(ang), np.sin(ang), 0 * ang, lk.GREEN, 2.2), (0 * k, 0 * k, k, lk.GREY, 1.1)],
                    arrows=[((0, 0, 0), (0, 0, 1.9), lk.GREY, 1.1), ((0, 0, 0), (0, 2.1, 0), lk.GREY, 1.1)],
                    texts=[
                        ((0, 0, 1.9), "t", lk.GREY, 90),
                        ((0, 2.1, 0), "r", lk.GREY, 0, 8),
                        ((0, 0, 1.1), r"M = \text{“outside” region}", lk.RED, 0, 138),
                        ((0, 0, -0.5), r"\mathbb{S}^2 \text{ at } r = r_0,\ t = 0", lk.GREEN, 0, 138),
                    ],
                )
            ],
            height=340,
            width=560,
        )

    return cone_kind, cone_scene, latitude_scene, orientation_figure, particle_scene, schwarzschild_scene, stereographic_scene


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figure.: the direction of X in steps of 5 degrees
    cone_s = lk.slider(0, 180, step=5, value=30, label=r"direction of $X$", show_value=False)
    return (cone_s,)


@app.cell(hide_code=True)
def _(cone_s, cone_scene):
    # the scene of the lightcone figure, in place by its slider
    cone_scene(cone_s.value)
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"$g:p\in M\longmapsto g_p:T_pM\times T_pM\to\mathbb R$",
        lk.aside(
            r"assignment of <span class='lk-mark'>inner-product</span> on each tangent space",
            "symmetric, bilinear<br>Euclidean or Minkowski",
        ),
        r"> $\leadsto$ &nbsp; given $X_p,Y_p\in T_pM$, &nbsp; $g_p(X_p,Y_p)\in\mathbb R$ is well-defined independent of charts",
        lk.aside(
            r"> > $\displaystyle\begin{aligned}g_p(X_p,Y_p)&\overset{\varphi}{=}X^i(p)\,g_{ij}(p)\,Y^j(p)\\&\overset{\tilde\varphi}{=}\tilde X^k(p)\,\tilde g_{kl}(p)\,\tilde Y^l(p)\end{aligned}$",
            "but we can always choose charts and<br>work with local coordinates and components",
        ),
        r"> > > $\Longleftrightarrow$ &nbsp; $\displaystyle g_{ij}(p)=\frac{\partial\tilde x^k}{\partial x^i}(p)\,\tilde g_{kl}(p)\,\frac{\partial\tilde x^l}{\partial x^j}(p)$",
        topic="Metric fields",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals("Lorentzian metrics", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("Schutz 6.2, 10.2; Carroll 2.5, 2.7, 5.1; Sasane 5.1–5.3")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: metric fields
    # recall: vector fields as derivations
    lk.recall(
        r"""
        $X\in\Gamma(TM)$ smooth vector field

        > $X:p\in M\to X_p\in T_pM$

        > > $\leadsto$ &nbsp; $\displaystyle\begin{aligned}X:C^\infty(M,\mathbb R)&\longrightarrow C^\infty(M,\mathbb R)\\f&\longmapsto X(f):p\mapsto X_p(f)\end{aligned}$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: metric fields
    # smooth metric fields
    lk.prose(
        lk.aside(
            r"A smooth metric field $g\in\Gamma(\mk{T^*M\otimes T^*M})$",
            "will explain notation later",
        ),
        r"""
        $$
        \begin{aligned}
        g:\Gamma(TM)\times\Gamma(TM)&\longrightarrow C^\infty(M,\mathbb R)\\
        (X,Y)&\longmapsto g(X,Y):p\mapsto g_p(X_p,Y_p)
        \end{aligned}
        $$

        $\leadsto$ &nbsp; inner-product of smooth vector fields taking values on smooth functions
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk, stereographic_scene):
    # module: metric fields
    # example: the sphere
    lk.example(
        [
            r"$M=\mathbb S^2$",
            r"> $X\overset{\varphi_n}{=}X^u\,\partial_u+X^v\,\partial_v\overset{\psi}{=}X^\phi\,\partial_\phi+X^\theta\,\partial_\theta\overset{\varphi_s}{=}\cdots$",
            lk.aside(
                r"> $\displaystyle\begin{aligned}g(X,Y)&\overset{\varphi_n}{=}\frac{4\,(X^uY^u+X^vY^v)}{(1+u^2+v^2)^2}\\[0.3em]&\overset{\psi}{=}X^\phi Y^\phi+(\sin\phi)^2\,X^\theta Y^\theta\\[0.3em]&\overset{\varphi_s}{=}\cdots\end{aligned}$",
                [(1, r"on $\mathbb S^2-\{n\}$"), (2, r"on $\mathbb S^2-\{\text{meridian}\}$"), (3, r"on $\mathbb S^2-\{s\}$")],
                rows=3,
            ),
            lk.figure(stereographic_scene()),
            r"""
            > $\leadsto$ &nbsp; $X\overset{\varphi_n}{=}\begin{bmatrix}X^u\\X^v\end{bmatrix}\overset{\psi}{=}\begin{bmatrix}X^\phi\\X^\theta\end{bmatrix}$

            > <span class="lk-ghost">$\leadsto$ &nbsp; </span>$g\overset{\varphi_n}{=}\underbrace{\begin{bmatrix}{\large\tfrac{4}{(1+u^2+v^2)^2}}&0\\0&{\large\tfrac{4}{(1+u^2+v^2)^2}}\end{bmatrix}}_{\footnotesize g(u,v)}\overset{\psi}{=}\underbrace{\begin{bmatrix}1&0\\0&(\sin\phi)^2\end{bmatrix}}_{\footnotesize g(\phi,\theta)}$
            """,
            lk.gap(),
            r"""
            $(u,v)=\varphi_n\circ\psi^{-1}(\phi,\theta)=\big(\cot(\phi/2)\cos\theta,\ \cot(\phi/2)\sin\theta\big)$

            $\displaystyle\frac{\partial(u,v)}{\partial(\phi,\theta)}=-\frac{1}{2\,(\sin(\phi/2))^2}\begin{bmatrix}\cos\theta&\sin\phi\sin\theta\\\sin\theta&-\sin\phi\cos\theta\end{bmatrix}$
            """,
            lk.aside(
                r"> $\Longrightarrow$ &nbsp; $\displaystyle g(\phi,\theta)=\frac{\partial(u,v)}{\partial(\phi,\theta)}^T g(u,v)\,\frac{\partial(u,v)}{\partial(\phi,\theta)}$",
                "check!",
            ),
        ],
        label="ex-sphere-metric",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: length
    # definition: length of a path
    lk.definition(
        r"""
        Given a Riemannian metric $g$ on $M$ and a path segment $\gamma:[a,b]\to M$

        $$
        \mathrm{length}_g(\gamma)=\int_a^b\sqrt{g_{\gamma(t)}(\gamma'(t),\gamma'(t))}\,dt
        $$
        """,
        label="def-length",
    )
    return


@app.cell(hide_code=True)
def _(latitude_scene, lk):
    # module: length
    # example: length of a latitude
    lk.example(
        [
            r"$\gamma:[0,2\pi]\longrightarrow\mathbb S^2$, &nbsp; $t\longmapsto\big(\sin(\phi_0)\cos(t),\ \sin(\phi_0)\sin(t),\ \cos(\phi_0)\big)$",
            lk.figure(latitude_scene()),
            r"""
            > $\varphi_n$: &nbsp; $\begin{bmatrix}u(t)\\v(t)\end{bmatrix}=\begin{bmatrix}\cot(\phi_0/2)\cos(t)\\\cot(\phi_0/2)\sin(t)\end{bmatrix}=\cot(\phi_0/2)\begin{bmatrix}\cos(t)\\\sin(t)\end{bmatrix}$

            > <span class="lk-ghost">$\varphi_n$: &nbsp; </span>$\begin{bmatrix}u'(t)\\v'(t)\end{bmatrix}=\cot(\phi_0/2)\begin{bmatrix}-\sin(t)\\\cos(t)\end{bmatrix}$

            > $\psi$: &nbsp; $\begin{bmatrix}\phi(t)\\\theta(t)\end{bmatrix}=\begin{bmatrix}\phi_0\\t\end{bmatrix}$, &nbsp; $\begin{bmatrix}\phi'(t)\\\theta'(t)\end{bmatrix}=\begin{bmatrix}0\\1\end{bmatrix}$

            $$
            \begin{aligned}
            g_{\gamma(t)}(\gamma'(t),\gamma'(t))&=\frac{4}{(1+u(t)^2+v(t)^2)^2}\,\big(u'(t)^2+v'(t)^2\big)\\
            &=\frac{4}{(1+\cot(\phi_0/2)^2)^2}\,\cot(\phi_0/2)^2=\sin(\phi_0)^2\\
            &=\phi'(t)^2+\sin(\phi(t))^2\,\theta'(t)^2
            \end{aligned}
            $$

            > $\Longrightarrow$ &nbsp; $\displaystyle\mathrm{length}_g(\gamma)=\int_0^{2\pi}\sqrt{\sin(\phi_0)^2}\,dt=2\pi\sin(\phi_0)$
            """,
        ],
        label="ex-latitude-length",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Lorentzian metrics
    # definition: spacelike, timelike, lightlike vectors
    lk.definition(
        [
            r"Given a Lorentzian metric $g$ on $M$, tangent space $T_pM$ decomposes into",
            r"> • &nbsp; **spacelike** vectors: &nbsp; $X_p\in T_pM$ such that $g_p(X_p,X_p)>0$",
            lk.aside(
                r"> • &nbsp; **timelike** vectors: &nbsp; $X_p\in T_pM$ such that $g_p(X_p,X_p)<0$",
                "all independent of any choice of charts",
            ),
            r"> • &nbsp; **lightlike** vectors: &nbsp; $X_p\in T_pM$ such that $g_p(X_p,X_p)=0$, &nbsp; $X_p\neq0$",
        ],
        label="def-causal-vectors",
    )
    return


@app.cell(hide_code=True)
def _(cone_kind, cone_s, lk):
    # module: Lorentzian metrics
    # remark: future and past in Minkowski spacetime
    lk.remark(
        [
            r"In $\mathbb M^4$, a choice of a single timelike vector $e_0$ is enough",
            lk.aside(
                r"to determine the notion of <span class='lk-mark'>“future” and “past”</span>",
                "the “upper side” of the lightcone",
            ),
            r"> “future” timelike vectors $u$ are those that $\eta(e_0,u)<0$",
            lk.interactive(lk.frame("L15-cone", 300), controls=[cone_s], readout=lk.prose(cone_kind(cone_s.value))),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Lorentzian metrics
    # definition: time orientation
    lk.definition(
        [
            lk.aside(
                r"For $(M,g)$ Lorentzian manifold, a **time orientation** is a choice of a <span class='lk-mark'>globally defined</span> timelike vector field",
                "defined at every point",
            ),
            r"> $T\in\Gamma(TM)$ such that $g(T,T)<0$ everywhere on $M$",
        ],
        label="def-time-orientation",
    )
    return


@app.cell(hide_code=True)
def _(lk, orientation_figure):
    # module: Lorentzian metrics
    # consequence: future
    lk.prose(
        lk.aside(
            r"$\Longrightarrow$ &nbsp; defines a notion of “future” or of “<span class='lk-mark'>moving forwards in time</span>”",
            "we don't have yet a proper notion of time!",
        ),
        lk.figure(orientation_figure()),
        r"$\leadsto$ &nbsp; some Lorentzian manifolds don't admit time orientation, but we will assume ours do!",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: particles
    # definition: particle
    lk.definition(
        [
            r"A **particle** in a Lorentzian manifold $(M,g)$ is a path $\gamma:\mathbb R\to M$",
            lk.aside(
                r"such that $\gamma'(t)$ is timelike and <span class='lk-mark'>future oriented</span> for all $t\in\mathbb R$",
                r"$g_{\gamma(t)}(T_{\gamma(t)},\gamma'(t))<0$",
            ),
        ],
        label="def-particle",
    )
    return


@app.cell(hide_code=True)
def _(lk, particle_scene):
    # module: particles
    # proper time
    lk.prose(
        lk.figure(particle_scene()),
        lk.aside(
            r"The proper time length of a <span class='lk-mark'>particle segment</span>",
            "a segment of the particle's history",
        ),
        lk.aside(
            r"> $\gamma:[a,b]\to M$ &nbsp; is &nbsp; $\mathrm{time}_g(\gamma)=\mk{\displaystyle\int_a^b\sqrt{-g_{\gamma(t)}(\gamma'(t),\gamma'(t))}\,dt}$",
            "independent of the choice of parameter $t$",
        ),
        r"""
        > > $\leadsto$ &nbsp; $\gamma(t)$ is said to be parameterized by proper time if $g_{\gamma(t)}(\gamma'(t),\gamma'(t))=-1$

        > > > $\Longrightarrow$ &nbsp; $\displaystyle\mathrm{time}_g(\gamma)=\int_a^bdt=b-a$

        > > > $\Longrightarrow$ &nbsp; $t$ is the proper time parameter of $\gamma$
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: particles
    # definition: lightlike particle
    lk.definition(
        r"A **lightlike particle** in $(M,g)$ is a path $\gamma:\mathbb R\to M$ such that $\gamma'(t)$ is future oriented lightlike $\forall\,t\in\mathbb R$",
        label="def-lightlike-particle",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: particles
    # comment: no time for light
    lk.prose(
        lk.aside(
            r"$\leadsto$ &nbsp; lightlike particles have <span class='lk-mark'>no invariant notion</span> of time!",
            "no physical notion",
        )
    )
    return


@app.cell(hide_code=True)
def _(lk, schwarzschild_scene):
    # module: Schwarzschild spacetime
    # example: Schwarzschild spacetime
    lk.example(
        [
            r"$\leadsto$ &nbsp; geometry of spacetime around a static, spherical star / black hole",
            r"""
            $M=\mathbb R\times(r_0,+\infty)\times\mathbb S^2$

            $$
            \Phi(t,r,\underbrace{x,y,z}_{\footnotesize\mathclap{x^2+y^2+z^2=1}})=\big(\overbrace{t,\ r}^{\footnotesize\mathclap{\begin{array}{c}\text{identity charts on}\\\mathbb R\text{ and }(r_0,+\infty)\end{array}}},\ \underbrace{\varphi(x,y,z)}_{\footnotesize\mathclap{\text{chart on }\mathbb S^2}}\big)
            $$
            """,
            lk.gap(),
            lk.figure(schwarzschild_scene()),
            r"""
            $X\overset{\Phi_n}{=}\begin{bmatrix}X^t\\X^r\\X^u\\X^v\end{bmatrix}\overset{\Psi}{=}\begin{bmatrix}X^t\\X^r\\X^\phi\\X^\theta\end{bmatrix}$

            $$
            \begin{aligned}
            g&\overset{\Phi_n}{=}\begin{bmatrix}-\big(1-{\large\tfrac{r_0}{r}}\big)&0&0&0\\0&\big(1-{\large\tfrac{r_0}{r}}\big)^{-1}&0&0\\0&0&{\large\tfrac{4r^2}{(1+u^2+v^2)^2}}&0\\0&0&0&{\large\tfrac{4r^2}{(1+u^2+v^2)^2}}\end{bmatrix}\\[0.6em]
            &\overset{\Psi}{=}\begin{bmatrix}-\big(1-{\large\tfrac{r_0}{r}}\big)&0&0&0\\0&\big(1-{\large\tfrac{r_0}{r}}\big)^{-1}&0&0\\0&0&r^2&0\\0&0&0&r^2(\sin\phi)^2\end{bmatrix}
            \end{aligned}
            $$

            $\leadsto$ &nbsp; static and spherical because it “looks the same” for every “time” and every “angle”
            """,
        ],
        title="Schwarzschild spacetime",
        label="ex-schwarzschild",
    )
    return


if __name__ == "__main__":
    app.run()
