import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 9 · Derivative of smooth maps", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import math
    import sys

    import marimo as mo
    import numpy as np
    from matplotlib.figure import Figure

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return Figure, lk, math, mo, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(9, "Derivative of smooth maps")
    return


@app.cell(hide_code=True)
def _(Figure, lk, math, np):
    # Helpers of this lecture: the four figures, and the two sketches

    def _blank(w, h, xlim, ylim):
        fig = Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def charts_figure():
        # two charts and their change of coordinates on the overlap (shared sketch style, lk.sk)
        sk = lk.sk
        fig, ax = sk.sketch((-0.3, 12.3), (-1.0, 8.4))
        sk.outline(ax, sk.shape(6.0, 5.6, 2.9, 2.3, egg=0.06, bean=0.06), name="$M$", at=(3.2, 7.7))
        U = sk.shape(5.25, 5.5, 1.55, 1.25, egg=-0.05, tilt=8)
        V = sk.shape(6.75, 5.5, 1.55, 1.25, egg=0.05, tilt=-8)
        sk.overlap(ax, U, V)
        sk.outline(ax, U, lk.RED, "$U$", (4.35, 6.95))
        sk.outline(ax, V, lk.BLUE, r"$\tilde U$", (7.65, 6.95))
        sk.label(ax, (6.0, 5.5), r"$U \cap \tilde U$")
        for x0, frame, cut, side, name, img in (
            (0.0, lk.RED, lk.BLUE, 1, r"$\varphi(U) \subseteq \mathbb{R}^m$", r"$\varphi(U \cap \tilde U)$"),
            (8.8, lk.BLUE, lk.RED, -1, r"$\tilde\varphi(\tilde U) \subseteq \mathbb{R}^m$", r"$\tilde\varphi(U \cap \tilde U)$"),
        ):
            B = sk.chart(ax, x0, 0.3, 3.2, 2.4, frame, name)
            xm = sk.band(ax, B, side, cut, width=2.2, depth=0.35)
            sk.label(ax, (xm + side * 0.05, 1.5), img, size=13)
        sk.maps(ax, (3.4, 4.4), (1.9, 2.95), r"$\varphi$", lk.RED, bend=-0.25, side=-1)
        sk.maps(ax, (8.6, 4.4), (10.1, 2.95), r"$\tilde\varphi$", lk.BLUE, bend=0.25, side=1)
        sk.maps(ax, (3.6, 1.5), (8.4, 1.5), r"$\tilde\varphi \circ \varphi^{-1}$", side=-1, gap=0.4)
        return fig

    def smooth_figure():
        # a map between manifolds and its coordinate expression in two charts (shared sketch style, lk.sk)
        sk = lk.sk
        fig, ax = sk.sketch((-0.2, 17.4), (-1.5, 8.0))
        for cx, name, a, b, an, bn in ((3.4, "$M$", "$U$", "$f^{-1}(V)$", (2.0, 6.25), (4.6, 6.15)),
                                       (13.8, "$N$", "$f(U)$", "$V$", (12.4, 6.25), (15.2, 6.25))):
            sk.outline(ax, sk.shape(cx, 5.1, 2.8, 2.2, egg=0.05 if cx > 5 else -0.05, bean=0.04), name=name, at=(cx - 2.9, 7.3))
            A = sk.shape(cx - 0.65, 4.75, 1.2, 0.95, tilt=6)
            B = sk.shape(cx + 0.65, 4.75, 1.2, 0.95, tilt=-6)
            sk.overlap(ax, A, B)
            sk.outline(ax, A, lk.RED, a, an)
            sk.outline(ax, B, lk.BLUE, b, bn)
        sk.maps(ax, (6.7, 5.6), (10.5, 5.6), "$f$", bend=0.25, side=1)
        sk.band(ax, sk.chart(ax, 1.4, -0.7, 3.0, 2.2, lk.RED, r"$\mathbb{R}^m$"), 1, lk.BLUE)
        sk.band(ax, sk.chart(ax, 12.8, -0.7, 3.0, 2.2, lk.BLUE, r"$\mathbb{R}^n$"), -1, lk.RED)
        sk.label(ax, (3.95, 1.85), r"$\varphi(U \cap f^{-1}(V))$", size=13, va="bottom")
        sk.label(ax, (13.25, 1.85), r"$\psi(f(U) \cap V)$", size=13, va="bottom")
        sk.maps(ax, (1.0, 3.5), (1.3, 1.75), r"$\varphi$", lk.RED, bend=-0.35, side=-1)
        sk.maps(ax, (16.2, 3.5), (15.9, 1.75), r"$\psi$", lk.BLUE, bend=0.35, side=1)
        sk.maps(ax, (4.8, 0.4), (12.4, 0.4), r"$\psi \circ f \circ \varphi^{-1}$", side=1, gap=0.4)
        return fig

    def _sphere(alpha=0.45):
        s_, t_ = np.meshgrid(np.linspace(0, np.pi, 37), np.linspace(0, 2 * np.pi, 73), indexing="ij")
        return lk.sheet(np.sin(s_) * np.cos(t_), np.sin(s_) * np.sin(t_), np.cos(s_), alpha=alpha)

    def stereo_scene():
        # a path gamma through p, its images in the charts phi_n and phi_s on the plane z = 0, and their velocities
        u0, v0, a, b = 1.2, 0.6, 0.6, 0.8
        t = np.linspace(-0.6, 0.6, 121)
        u, v = u0 + t * a - 0.5 * t**2 * b, v0 + t * b + 0.5 * t**2 * a
        q, r2 = u**2 + v**2, u0**2 + v0**2
        path = (2 * u / (1 + q), 2 * v / (1 + q), (q - 1) / (1 + q))
        P = np.array([2 * u0 / (1 + r2), 2 * v0 / (1 + r2), (r2 - 1) / (1 + r2)])
        Un, Us = np.array([u0, v0, 0.0]), np.array([u0 / r2, v0 / r2, 0.0])
        vn = np.array([a, b, 0.0])
        vs = np.array([(v0**2 - u0**2) * a - 2 * u0 * v0 * b, -2 * u0 * v0 * a + (u0**2 - v0**2) * b, 0.0]) / r2**2
        n, s = np.array([0.0, 0.0, 1.0]), np.array([0.0, 0.0, -1.0])
        plane = [(-1.3, -1.3, 0), (1.9, -1.3, 0), (1.9, 1.6, 0), (-1.3, 1.6, 0)]
        edge = np.array(plane + plane[:1])
        k = np.linspace(0, 1, 40)[:, None]
        c = np.linspace(0, 2 * np.pi, 121)

        def seg(p0, p1):
            return tuple((p0 + k * (p1 - p0)).T)

        return lk.turntable(
            -60,
            24,
            "the unit sphere and the plane z = 0, with a path through p, its images through the charts phi_n and phi_s, and their velocity vectors",
            [
                lk.panel(
                    1.0,
                    surfaces=[_sphere(), lk.patch(plane, "#e8e8e8", 0.6, n=16)],
                    outlines=[("sphere", (0, 0, 0), 1.0, lk.GREY, 1.2)],
                    lines=[
                        (*edge.T, lk.GREY, 1.2),
                        (np.cos(c), np.sin(c), 0 * c, "#000000", 1.0),
                        (*seg(n, Un), lk.RED, 1.4),
                        (*seg(s, P), lk.BLUE, 1.4),
                        (*path, "#000000", 1.8),
                        (u, v, 0 * t, "#000000", 1.4),
                        (u / q, v / q, 0 * t, "#000000", 1.4),
                    ],
                    arrows=[(tuple(Un), tuple(Un + 0.6 * vn), lk.GREEN), (tuple(Us), tuple(Us + 0.6 * vs), lk.ORANGE)],
                    points=[(tuple(n), "#000000", 3.4), (tuple(s), "#000000", 3.4), (tuple(P), "#000000", 3.4), (tuple(Un), "#000000", 3.4), (tuple(Us), "#000000", 3.4)],
                    texts=[
                        (tuple(n), "n", "#000000", 90),
                        (tuple(s), "s", "#000000", -90),
                        (tuple(P), "p", "#000000", 60, 8),
                        (tuple(Un + 0.18 * np.array([0.8, -0.6, 0.0])), r"\varphi_n(p)", "#000000", -90, 2),
                        (tuple(Us), r"\varphi_s(p)", "#000000", 108, 9),
                        (tuple(Un + 0.6 * vn), r"(\varphi_n \circ \gamma)'(0) = \begin{bmatrix} a \\ b \end{bmatrix}", lk.GREEN, 80, 56),
                        (tuple(Us + 0.6 * vs), r"(\varphi_s \circ \gamma)'(0) = \begin{bmatrix} \tilde{a} \\ \tilde{b} \end{bmatrix}", lk.ORANGE, 180, 6),
                    ],
                )
            ],
            height=360,
            width=520,
            bias=0.12,
            zoom=1.35,
        )

    def charts_velocity_figure(u0, v0, a, b):
        # two paths with the same velocity in the chart phi_n, and the same two paths in the chart phi_s
        r2 = u0**2 + v0**2
        ut, vt = u0 / r2, v0 / r2
        at = ((v0**2 - u0**2) * a - 2 * u0 * v0 * b) / r2**2 + 0.0
        bt = (-2 * u0 * v0 * a + (u0**2 - v0**2) * b) / r2**2 + 0.0
        t = np.linspace(-1.0, 1.0, 300)
        g = (u0 + t * a, v0 + t * b)
        h = (u0 + t * a - 0.5 * t**2 * b, v0 + t * b + 0.5 * t**2 * a)
        Ls = max(1.6, 1.5 * max(abs(ut), abs(vt)))  # the south panel follows its point
        k = min(1.0, 0.6 * Ls / max(math.hypot(at, bt), 1e-9))  # one arrow scale for both panels, so that the south arrow fits
        Ls = max(Ls, 1.15 * max(abs(ut + k * at), abs(vt + k * bt)))
        Ln = max(1.6, 1.3 * max(np.abs(np.concatenate([*g, *h])).max(), abs(u0 + k * a), abs(v0 + k * b)))
        fig = Figure(figsize=(5.6, 3.0), layout="constrained")
        axes = fig.subplots(1, 2)
        c = np.linspace(0, 2 * np.pi, 200)
        for ax, title, L in zip(axes, (r"$\varphi_n = (u, v)$", r"$\varphi_s = (\tilde{u}, \tilde{v})$"), (Ln, Ls)):
            ax.set_title(title, fontsize=13)
            ax.set_xlim(-L, L)
            ax.set_ylim(-L, L)
            ax.set_aspect("equal")
            ax.axhline(0, color="#000000", lw=0.6)
            ax.axvline(0, color="#000000", lw=0.6)
            ax.plot(np.cos(c), np.sin(c), color=lk.GREY, lw=0.8)
            ax.text(-0.74, -0.74, "equator", color=lk.GREY, fontsize=10, ha="right", va="top")
            ax.set_xticks([-round(L, 1), 0, round(L, 1)])
            ax.set_yticks([-round(L, 1), 0, round(L, 1)])
        for (pu, pv), col, name in ((g, lk.BLUE, r"$\gamma$"), (h, lk.RED, r"$\tilde{\gamma}$")):
            axes[0].plot(pu, pv, color=col)
            du, dv = pu[-1] - pu[-2], pv[-1] - pv[-2]
            nn = math.hypot(du, dv) or 1.0
            axes[0].annotate(name, (pu[-1], pv[-1]), textcoords="offset points", xytext=(9 * du / nn, 9 * dv / nn), ha="center", va="center", color=col, fontsize=12)
            qq = pu**2 + pv**2
            qq = np.where(qq < 1e-6, np.nan, qq)  # the image of the path passes through infinity where it crosses s
            axes[1].plot(pu / qq, pv / qq, color=col)
        lk.arrow(axes[0], (u0, v0), (u0 + k * a, v0 + k * b), lk.GREEN)
        lk.arrow(axes[1], (ut, vt), (ut + k * at, vt + k * bt), lk.GREEN)
        axes[0].plot(u0, v0, "o", color="#000000", ms=5)
        axes[1].plot(ut, vt, "o", color="#000000", ms=5)
        return fig

    def derivative_figure():
        # paths with the same velocity at p and their images under f, with the same velocity at f(p)
        sk = lk.sk
        fig, ax = sk.sketch((-0.4, 16.6), (-0.1, 5.5))
        s = np.linspace(-1.6, 1.6, 120)
        for cx, name, lab, g1, g2, vel in ((3.0, "$M$", "$p$", r"$\gamma$", r"$\tilde\gamma$", r"$[\gamma] = [\tilde\gamma]$"),
                                           (13.4, "$N$", "$f(p)$", r"$f \circ \gamma$", r"$f \circ \tilde\gamma$", r"$[f \circ \gamma] = [f \circ \tilde\gamma]$")):
            sk.outline(ax, sk.shape(cx, 2.55, 2.9, 2.1, egg=0.04, bean=0.04), name=name, at=(cx - 2.8, 4.75))
            P = (cx - 0.2, 2.35)
            ax.plot(*sk.path(P, (1, 0.25), -0.35, s * 0.8), color=lk.RED, lw=sk.LW, zorder=4)
            ax.plot(*sk.path(P, (1, 0.25), -0.75, s * 0.75), color=lk.GREEN, lw=sk.LW, zorder=4)
            sk.maps(ax, P, (P[0] + 1.05, P[1] + 0.26), color=lk.ORANGE, lw=1.8)
            sk.dot(ax, P, lab, at=(-0.3, 0.25), ha="right", va="bottom")
            sk.label(ax, (P[0] + 1.4, P[1] - 0.3), g1, lk.RED, ha="left")
            sk.label(ax, (P[0] + 1.0, P[1] - 1.3), g2, lk.GREEN, ha="left")
            sk.label(ax, (P[0] + 0.5, P[1] + 1.2), vel, lk.ORANGE)
        sk.maps(ax, (6.7, 1.7), (9.1, 1.7), "$f$", side=-1)
        sk.maps(ax, (6.7, 3.4), (9.1, 3.4), "$Df_p$", lk.ORANGE, side=1)
        return fig

    def height_scene(t):
        # the equator gamma and the meridian sigma through p, their velocities at p, and the points gamma(t), sigma(t)
        c = np.linspace(0, 2 * np.pi, 241)
        plane = [(-1.25, -1.25, 0), (1.25, -1.25, 0), (1.25, 1.25, 0), (-1.25, 1.25, 0)]
        edge = np.array(plane + plane[:1])
        return lk.turntable(
            -30,
            16,
            "the unit sphere and the plane z = 0, with the equator gamma and the meridian sigma through p, their velocity vectors at p, and the points gamma(t) and sigma(t)",
            [
                lk.panel(
                    1.0,
                    surfaces=[_sphere(), lk.patch(plane, "#e8e8e8", 0.6, n=16)],
                    outlines=[("sphere", (0, 0, 0), 1.0, lk.GREY, 1.2)],
                    lines=[(*edge.T, lk.GREY, 1.2), (np.cos(c), np.sin(c), 0 * c, lk.RED, 1.6), (np.cos(c), 0 * c, np.sin(c), lk.BLUE, 1.6)],
                    arrows=[((1, 0, 0), (1, 0.75, 0), lk.GREEN), ((1, 0, 0), (1, 0, 0.75), lk.ORANGE)],
                    points=[
                        ((1, 0, 0), "#000000", 3.4),
                        ((0, 0, 1), "#000000", 3.4),
                        ((0, 0, -1), "#000000", 3.4),
                        ((0, 0, 0), "#000000", 2.6),
                        ((math.cos(t), math.sin(t), 0), lk.RED, 5.0),
                        ((math.cos(t), 0, math.sin(t)), lk.BLUE, 5.0),
                    ],
                    texts=[
                        ((1, 0, 0), "p", "#000000", -60, 8),
                        ((0, 0, 1), "n", "#000000", 90),
                        ((0, 0, -1), "s", "#000000", -90),
                        ((0, 0, 0), "o", "#000000", 150, 6),
                        ((1, 0.75, 0), r"[\gamma]", lk.GREEN, 0, 6),
                        ((1, 0, 0.75), r"[\sigma]", lk.ORANGE, 0, 6),
                        ((math.cos(-2.6), math.sin(-2.6), 0), r"\gamma", lk.RED, 90, 6),
                        ((math.cos(2.1), 0, math.sin(2.1)), r"\sigma", lk.BLUE, 150, 6),
                    ],
                )
            ],
            height=340,
            width=340,
            key="L9-height",
            apart=True,
            bias=0.12,
        )

    def height_axis(t):
        # the values of f along the two paths, on the real line
        fig, ax = _blank(2.8, 2.6, (-2.25, 2.3), (-1.3, 1.6))
        ax.plot([0, 0], [-1.15, 1.15], color="#000000")
        for y, lab in ((1, "$f(n) = 1$"), (-1, "$f(s) = -1$")):
            ax.plot(0, y, "o", color="#000000", ms=3.5)
            ax.text(0.25, y - 0.05, lab, fontsize=12)
        ax.plot(0, 0, "o", color=lk.RED, ms=6)
        ax.plot(0, math.sin(t), "o", color=lk.BLUE, ms=6)
        ax.text(0.25, -0.05, r"$f(\gamma(t)) = 0 \ \ \forall t$", fontsize=12)
        ax.text(-0.25, math.sin(t), r"$f(\sigma(t)) = \sin(t)$", fontsize=12, ha="right", va="center")
        ax.text(0, 1.35, r"$\mathbb{R}$", fontsize=13, ha="center")
        return fig

    return charts_figure, charts_velocity_figure, derivative_figure, height_axis, height_scene, smooth_figure, stereo_scene


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures
    s_u0 = lk.slider(0.9, 2.0, step=0.1, value=1.2, label="$u(0)$", show_value=False)
    s_v0 = lk.slider(-1.0, 1.0, step=0.1, value=0.6, label="$v(0)$", show_value=False)
    s_a = lk.slider(-1.0, 1.0, step=0.1, value=0.6, label="$a$", show_value=False)
    s_b = lk.slider(-1.0, 1.0, step=0.1, value=0.8, label="$b$", show_value=False)
    s_t = lk.slider(-1.5, 1.5, step=0.05, value=0.5, label="$t$", show_value=False)
    return s_a, s_b, s_t, s_u0, s_v0


@app.cell(hide_code=True)
def _(height_scene, s_t):
    # the scene of the height function figure, in place by its slider
    height_scene(s_t.value)
    return


@app.cell(hide_code=True)
def _(charts_figure, lk, smooth_figure):
    # module: recap
    # recap
    lk.recap(
        r"$M=$ set of points, &nbsp; $\mathcal A=$ atlas of charts",
        lk.aside(
            r"> $\varphi:U\subseteq M\to\varphi(U)\subseteq\mathbb R^m$, &nbsp; $p\longmapsto\varphi(p)=\mk{x^\mu(p)}\,\mk{e_\mu}$",
            r"local coordinates $x^\mu:U\subseteq M\to\mathbb R$<br>$e_\mu$ basis of $\mathbb R^m$",
        ),
        r"> $\leadsto$ &nbsp; $\tilde\varphi\circ\varphi^{-1}:\varphi(U\cap\tilde U)\longrightarrow\tilde\varphi(U\cap\tilde U)$ &nbsp; diffeomorphism",
        lk.aside(
            r"> > $\Longrightarrow$ &nbsp; $\tilde\varphi\circ\varphi^{-1}(x)=\mk{\tilde x^\mu(x)}\,e_\mu$",
            r"change of coordinates with invertible<br>Jacobian $\dfrac{\partial\tilde x^\mu}{\partial x^\nu}(x)$ in $\varphi(U\cap\tilde U)$",
        ),
        lk.figure(charts_figure()),
        r"$(M,\mathcal A)\overset{f}{\longrightarrow}(N,\mathcal B)$ &nbsp; is smooth if",
        r"> $\psi\circ f\circ\varphi^{-1}:\varphi(U\cap f^{-1}(V))\longrightarrow\psi(f(U)\cap V)$ &nbsp; is smooth",
        r"> $\forall$ &nbsp; $\varphi:U\subseteq M\to\varphi(U)\subseteq\mathbb R^m$, &nbsp; $\psi:V\subseteq N\to\psi(V)\subseteq\mathbb R^n$",
        lk.aside(r"> $\varphi(p)=x^\mu(p)\,e_\mu$, &nbsp; $\psi(q)=y^\alpha(q)\,\mk{e_\alpha}$", r"basis of $\mathbb R^n$"),
        lk.aside(
            r"> > $\Longrightarrow$ &nbsp; $\psi\circ f\circ\varphi^{-1}(x)=\mk{y^\alpha(x)}\,e_\alpha$",
            r"coordinate expression of $f$<br>must be smooth in all coordinates!",
        ),
        lk.figure(smooth_figure()),
        topic="Manifolds & smooth maps",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals("Derivative of smooth maps", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("Carroll 2.3; Sasane 2.2–2.5")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: derivative in affine spaces
    # the derivative between affine spaces, and what it does to paths
    lk.prose(
        r"Suppose $M$ and $N$ are affine spaces",
        r"> $M=(\mathbb A^m,\mathbb V^m,-)$, &nbsp; $N=(\mathbb B^n,\mathbb W^n,-)$",
        r"Given &nbsp; $f:\mathbb A\to\mathbb B$ &nbsp; a map, &nbsp; $x\in\mathbb A$, &nbsp; $v\in\mathbb V$",
        lk.aside(
            r"> $\leadsto$ &nbsp; $Df_x(v)=\displaystyle\lim_{t\to0}\frac{\mk{f(x+tv)-f(x)}}{t}\in\mathbb W$ &nbsp; (directional derivative)",
            r"uses affine structure<br>both on $\mathbb A$ and on $\mathbb B$!",
        ),
        r"""
        > $\leadsto$ &nbsp; $f$ is differentiable if

        > > • &nbsp; $Df_x:\mathbb V\longrightarrow\mathbb W$ &nbsp; is linear
        """,
        lk.aside(
            r"> > • &nbsp; $\displaystyle\lim_{t\to0}\frac{f(\gamma(t))-f(\gamma(0))}{t}=Df_x(v)$",
            r"still depends on<br>affine structures",
        ),
        r"""
        > > > $\forall$ &nbsp; $\gamma:\mathbb R\to\mathbb A$ &nbsp; with &nbsp; $\begin{cases}x=\gamma(0)\\v=\gamma'(0)=\displaystyle\lim_{t\to0}\frac{\gamma(t)-\gamma(0)}{t}\end{cases}$

        > $\Longrightarrow$ &nbsp; now we can compute $Df_x(v)$ as follows:

        > > pick &nbsp; $\gamma:\mathbb R\to\mathbb A$ &nbsp; with &nbsp; $\begin{cases}\gamma(0)=x\\\gamma'(0)=v\end{cases}$

        > > consider &nbsp; $\sigma=f\circ\gamma:\mathbb R\to\mathbb B$ &nbsp; and compute

        > > > $\begin{cases}\sigma(0)=f(\gamma(0))=f(x)\\\sigma'(0)=Df_{\gamma(0)}(\gamma'(0))=Df_x(v)\end{cases}$

        > $\leadsto$ &nbsp; $f$ maps paths through $x$ to paths through $f(x)$

        > $\leadsto$ &nbsp; $Df_x$ maps velocities at $x$ to velocities at $f(x)$

        > > $\leadsto$ &nbsp; we can use this observation to generalize the derivative to maps between manifolds!
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tangent space
    # definition: same velocity
    lk.definition(
        r"""
        Given $M$ $m$-manifold, &nbsp; $\gamma:\mathbb R\to M$, &nbsp; $\tilde\gamma:\mathbb R\to M$ &nbsp; two smooth paths with $\gamma(0)=\tilde\gamma(0)$ are said to have the **same velocity** at $p=\gamma(0)=\tilde\gamma(0)$ if for some chart $\varphi:U\subseteq M\to\varphi(U)\subseteq\mathbb R^m$ with $p\in U$ we have

        $$(\varphi\circ\gamma)'(0)=(\varphi\circ\tilde\gamma)'(0)\in\mathbb R^m$$
        """,
        label="def-same-velocity",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tangent space
    # remark: independent of the chart
    lk.remark(r"If there is one chart for which $\gamma,\tilde\gamma$ have the same velocity, then it is also true in every other chart!")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tangent space
    # remark: an equivalence relation
    lk.remark(r"The condition $(\varphi\circ\gamma)'(0)=(\varphi\circ\tilde\gamma)'(0)$ defines an equivalence relation of paths through $p=\gamma(0)=\tilde\gamma(0)$!")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tangent space
    # definition: tangent space
    lk.definition(
        [
            r"Let $M$ be an $m$-manifold. Given $p\in M$, the **tangent space** of $M$ at $p$ is the set of all equivalence classes of smooth paths through $p$",
            lk.aside(
                r"$$T_pM=\{\mk{[\gamma]}\mid\gamma:\mathbb R\to M,\ \gamma(0)=p\}$$",
                r"equivalence class of $\gamma$<br>(all paths with same velocity at $p$)",
            ),
        ],
        label="def-tangent-space",
    )
    return


@app.cell(hide_code=True)
def _(charts_velocity_figure, lk, s_a, s_b, s_u0, s_v0, stereo_scene):
    # module: tangent space
    # example: velocities on the sphere in the two stereographic charts
    lk.example(
        [
            r"$\mathbb S^2=\{(x,y,z)\in\mathbb R^3\mid x^2+y^2+z^2=1\}$",
            r"""
            $(u,v)=\varphi_n(x,y,z)=\Big(\dfrac{x}{1-z},\ \dfrac{y}{1-z}\Big)$, &nbsp; $(x,y,z)\neq(0,0,1)$

            > $\leadsto$ &nbsp; $\varphi_n^{-1}(u,v)=\Big(\dfrac{2u}{1+u^2+v^2},\ \dfrac{2v}{1+u^2+v^2},\ \dfrac{-1+u^2+v^2}{1+u^2+v^2}\Big)$

            $(\tilde u,\tilde v)=\varphi_s(x,y,z)=\Big(\dfrac{x}{1+z},\ \dfrac{y}{1+z}\Big)$, &nbsp; $(x,y,z)\neq(0,0,-1)$

            > $\leadsto$ &nbsp; $\varphi_s^{-1}(\tilde u,\tilde v)=\Big(\dfrac{2\tilde u}{1+\tilde u^2+\tilde v^2},\ \dfrac{2\tilde v}{1+\tilde u^2+\tilde v^2},\ \dfrac{1-\tilde u^2-\tilde v^2}{1+\tilde u^2+\tilde v^2}\Big)$
            """,
            lk.gap(),
            lk.aside(
                r"Given &nbsp; $\gamma:\mathbb R\to\mathbb S^2$, &nbsp; $\mk{\gamma(t)=(x(t),y(t),z(t))}$",
                r"don't try to compute velocity<br>directly on $\mathbb S^2$",
            ),
            r"> with &nbsp; $\gamma(0)=p\neq n$",
            lk.aside(
                r"> $\Longrightarrow$ &nbsp; $\varphi_n\circ\gamma:\mathbb R\to\mathbb R^2$, &nbsp; $\mk{\varphi_n\circ\gamma(t)=(u(t),v(t))}$",
                "compute velocity in a chart",
            ),
            r"$$(\varphi_n\circ\gamma)'(0)=\begin{bmatrix}u'(0)\\v'(0)\end{bmatrix}=\begin{bmatrix}a\\b\end{bmatrix}\in\mathbb R^2$$",
            lk.figure(stereo_scene()),
            r"Another &nbsp; $\tilde\gamma:\mathbb R\to\mathbb S^2$ &nbsp; is considered equivalent to $\gamma$ if",
            r"$$\tilde\gamma(0)=\gamma(0)=p\qquad\text{and}\qquad(\varphi_n\circ\tilde\gamma)'(0)=\begin{bmatrix}a\\b\end{bmatrix}\in\mathbb R^2$$",
            lk.gap(),
            r"""
            If &nbsp; $(\varphi_n\circ\gamma)'(0)=(\varphi_n\circ\tilde\gamma)'(0)$ &nbsp; $\Longrightarrow$ &nbsp; $(\varphi_s\circ\gamma)'(0)=(\varphi_s\circ\tilde\gamma)'(0)$

            > $(\tilde u(t),\tilde v(t))=\Big(\dfrac{u(t)}{u(t)^2+v(t)^2},\ \dfrac{v(t)}{u(t)^2+v(t)^2}\Big)$

            $$\begin{bmatrix}\tilde a\\\tilde b\end{bmatrix}=\begin{bmatrix}\tilde u'\\\tilde v'\end{bmatrix}=\frac{1}{(u^2+v^2)^2}\underbrace{\begin{bmatrix}v^2-u^2&-2uv\\-2uv&u^2-v^2\end{bmatrix}}_{\footnotesize\begin{matrix}\text{only depends on}\\p=\gamma(0)=\tilde\gamma(0)\end{matrix}}\underbrace{\begin{bmatrix}u'\\v'\end{bmatrix}}_{\footnotesize=\left[\begin{smallmatrix}a\\b\end{smallmatrix}\right]}$$
            """,
            lk.interactive(charts_velocity_figure(s_u0.value, s_v0.value, s_a.value, s_b.value), controls=[s_u0, s_v0, s_a, s_b]),
        ],
        label="ex-sphere-velocities",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tangent space
    # remark: every vector is a velocity
    lk.remark(
        [
            r"Every $\left[\begin{smallmatrix}a\\b\end{smallmatrix}\right]\in\mathbb R^2$ appears as velocity vector of some path $\gamma$ on $\varphi_n$",
            r"""
            > $\leadsto$ &nbsp; $\gamma(t)=\varphi_n^{-1}\big(u(0)+t\,a,\ v(0)+t\,b\big)$

            > > $\Longrightarrow$ &nbsp; $(\varphi_n\circ\gamma)'(0)=\begin{bmatrix}a\\b\end{bmatrix}$ !
            """,
            lk.aside(r"$\therefore$ &nbsp; $T_p\mathbb S^2\mathrel{\mk{\approx}}\mathbb R^2$", "as a vector space! (later)"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(derivative_figure, lk):
    # module: derivative
    # definition: the derivative of a smooth map
    lk.definition(
        [
            r"The **derivative** of a smooth map $f:M\to N$ at $p\in M$ is the map",
            r"$$Df_p:T_pM\longrightarrow T_{f(p)}N,\qquad\underbrace{[\gamma]}_{\footnotesize\text{“velocity at }p\text{”}}\longmapsto Df_p[\gamma]=\underbrace{[f\circ\gamma]}_{\footnotesize\text{“velocity at }f(p)\text{”}}$$",
            lk.figure(derivative_figure()),
        ],
        label="def-derivative",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: derivative
    # remark: the derivative of a scalar function
    lk.remark(
        [
            r"$f:M\to\mathbb R$ &nbsp; smooth, &nbsp; $p\in M$, &nbsp; $[\gamma]\in T_pM$",
            lk.aside(
                r"$$Df_p[\gamma]=[\underbrace{f\circ\gamma}_{\footnotesize h:\mathbb R\to\mathbb R}]\mathrel{\text{“}{=}\text{”}}\mk{(f\circ\gamma)'(0)}$$",
                r"velocity of a single variable<br>scalar function",
            ),
            r"> $h\sim\tilde h$ &nbsp; $\Longleftrightarrow$ &nbsp; $h'(0)=\tilde h'(0)\in\mathbb R$",
        ]
    )
    return


@app.cell(hide_code=True)
def _(height_axis, lk, mo, s_t):
    # module: derivative
    # example: the height function on the sphere, along the equator and a meridian
    lk.example(
        [
            r"$\mathbb S^2=\{(x,y,z)\in\mathbb R^3\mid x^2+y^2+z^2=1\}$",
            lk.aside(r"$f:\mathbb S^2\to\mathbb R$, &nbsp; $f(x,y,z)=z$", "height function"),
            r"$p=(1,0,0)\in\mathbb S^2$",
            r"$$\begin{alignedat}{2}\gamma:\mathbb R\to\mathbb S^2\qquad&\gamma(t)&&=\varphi_n^{-1}\big(\cos(t),\ \sin(t)\big)\\[0.2em]&&&=\big(\cos(t),\ \sin(t),\ 0\big)\\[0.8em]\sigma:\mathbb R\to\mathbb S^2\qquad&\sigma(t)&&=\varphi_n^{-1}\Big(\frac{\cos(t)}{1-\sin(t)},\ 0\Big)\\[0.2em]&&&=\big(\cos(t),\ 0,\ \sin(t)\big)\end{alignedat}$$",
            lk.aside(
                r"$$Df_p[\gamma]=[f\circ\gamma]=\mk{[\underbrace{0}_{\footnotesize\text{zero function}}:\mathbb R\to\mathbb R]}\mathrel{\text{“}{=}\text{”}}\frac{d}{dt}\Big|_{t=0}f\circ\gamma(t)=0$$",
                r"equivalence class of functions<br>with zero derivative at $t=0$",
            ),
            lk.aside(
                r"$$\begin{aligned}Df_p[\sigma]=[f\circ\sigma]=\mk{[\sin:\mathbb R\to\mathbb R]}&\mathrel{\text{“}{=}\text{”}}\frac{d}{dt}\Big|_{t=0}f\circ\sigma(t)\\[0.3em]&=\frac{d}{dt}\Big|_{t=0}\sin(t)=1\end{aligned}$$",
                r"equivalence class of functions<br>with derivative $1$ at $t=0$",
                at="middle",
            ),
            r"$$(\varphi_n\circ\gamma)'(0)=\begin{bmatrix}0\\1\end{bmatrix},\qquad(\varphi_n\circ\sigma)'(0)=\begin{bmatrix}1\\0\end{bmatrix}$$",
            lk.interactive(
                mo.hstack([lk.frame("L9-height", 340), height_axis(s_t.value)], justify="center", align="center", gap=2),
                controls=[s_t],
            ),
        ],
        label="ex-height",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: derivative
    # remark: the ambient space
    lk.remark(
        r"""
        Using the ambient space $\mathbb R^3$

        $$[\gamma]\mathrel{\text{“}{=}\text{”}}\begin{bmatrix}0\\1\\0\end{bmatrix},\qquad[\sigma]\mathrel{\text{“}{=}\text{”}}\begin{bmatrix}0\\0\\1\end{bmatrix}$$
        """
    )
    return


if __name__ == "__main__":
    app.run()
