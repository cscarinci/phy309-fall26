import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 8 · Charts on the sphere, smooth maps, tangent vectors", css_file="lecturekit/style.css")


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
    lk.lecture(8, "Charts on the sphere, smooth maps, tangent vectors")
    return


@app.cell(hide_code=True)
def _(Figure, lk, math, np):
    # Helpers of this lecture: the four figures, and the sketch

    def _sphere(alpha=0.45):
        s_, t_ = np.meshgrid(np.linspace(0, np.pi, 37), np.linspace(0, 2 * np.pi, 73), indexing="ij")
        return lk.sheet(np.sin(s_) * np.cos(t_), np.sin(s_) * np.sin(t_), np.cos(s_), alpha=alpha)

    def stereo_scene():
        # the line through n and p meets the plane z = 0 at (u, v, 0); the line through s and p at (u~, v~, 0)
        ph, th = math.radians(60), math.radians(30)
        P = np.array([math.sin(ph) * math.cos(th), math.sin(ph) * math.sin(th), math.cos(ph)])
        n, s, o = np.array([0.0, 0.0, 1.0]), np.array([0.0, 0.0, -1.0]), np.zeros(3)
        F = np.array([P[0], P[1], 0.0])
        Un = np.array([P[0] / (1 - P[2]), P[1] / (1 - P[2]), 0.0])
        Us = np.array([P[0] / (1 + P[2]), P[1] / (1 + P[2]), 0.0])
        plane = [(-1.25, -1.25, 0), (1.75, -1.25, 0), (1.75, 1.25, 0), (-1.25, 1.25, 0)]
        edge = np.array(plane + plane[:1])
        k = np.linspace(0, 1, 40)[:, None]
        c = np.linspace(0, 2 * np.pi, 121)

        def seg(a, b):
            return tuple((a + k * (b - a)).T)

        return lk.turntable(
            -30,
            18,
            "the unit sphere and the plane z = 0, with the line through n and p meeting the plane at (u, v, 0) and the line through s and p meeting it at (u~, v~, 0)",
            [
                lk.panel(
                    1.0,
                    surfaces=[_sphere(), lk.patch(plane, "#e8e8e8", 0.6, n=16)],
                    outlines=[("sphere", (0, 0, 0), 1.0, lk.GREY, 1.2)],
                    lines=[
                        (*edge.T, lk.GREY, 1.2),
                        (np.cos(c), np.sin(c), 0 * c, "#000000", 1.0),
                        (*seg(n, o), "#000000", 1.0, [2, 3]),
                        (*seg(P, F), "#000000", 1.0, [2, 3]),
                        (*seg(o, Un), lk.GREY, 1.0, [4, 3]),
                        (*seg(n, Un), lk.BLUE, 1.8),
                        (*seg(s, P), lk.RED, 1.8),
                    ],
                    points=[(tuple(n), "#000000", 3.4), (tuple(s), "#000000", 3.4), (tuple(o), "#000000", 2.6), (tuple(P), "#000000", 3.4), (tuple(F), "#000000", 2.6), (tuple(Un), lk.BLUE, 4.0), (tuple(Us), lk.RED, 4.0)],
                    texts=[
                        (tuple(n), "n", "#000000", 90),
                        (tuple(s), "s", "#000000", -90),
                        (tuple(o), "o", "#000000", 150, 8),
                        (tuple(P), "p = (x, y, z)", "#000000", 30, 12),
                        (tuple(F), "(x, y, 0)", "#000000", -90, 12),
                        (tuple(Un), "(u, v, 0)", "#000000", -60, 14),
                        (tuple(Us), r"(\tilde{u}, \tilde{v}, 0)", "#000000", -160, 14),
                    ],
                )
            ],
            height=340,
            width=420,
            bias=0.12,
        )

    def angles_scene():
        # the polar angle phi from n and the azimuthal angle theta from e_1
        ph, th = math.radians(50), math.radians(40)
        P = (math.sin(ph) * math.cos(th), math.sin(ph) * math.sin(th), math.cos(ph))
        F = (P[0], P[1], 0.0)  # the foot of p on the equatorial plane
        k = np.linspace(0, 1, 30)
        a = np.linspace(0, 1, 60)
        plane = [(-1.25, -1.25, 0), (1.25, -1.25, 0), (1.25, 1.25, 0), (-1.25, 1.25, 0)]
        edge = np.array(plane + plane[:1])
        c = np.linspace(0, 2 * np.pi, 121)
        return lk.turntable(
            -30,
            20,
            "the unit sphere and the plane z = 0, with the poles n and s, the centre o, the vector e_1, a point p, and the angles phi from n and theta from e_1",
            [
                lk.panel(
                    1.0,
                    surfaces=[_sphere(), lk.patch(plane, "#e8e8e8", 0.6, n=16)],
                    outlines=[("sphere", (0, 0, 0), 1.0, lk.GREY, 1.2)],
                    lines=[
                        (*edge.T, lk.GREY, 1.2),
                        (np.cos(c), np.sin(c), 0 * c, "#000000", 1.0),
                        (0 * k, 0 * k, 2 * k - 1, "#000000", 0.9),
                        (P[0] + 0 * k, P[1] + 0 * k, P[2] * (1 - k), lk.GREY, 1.0, [4, 3]),
                        (F[0] * k, F[1] * k, 0 * k, lk.GREY, 1.0, [4, 3]),
                        (0.4 * np.sin(ph * a) * math.cos(th), 0.4 * np.sin(ph * a) * math.sin(th), 0.4 * np.cos(ph * a), lk.GREEN, 1.4),
                        (0.45 * np.cos(th * a), 0.45 * np.sin(th * a), 0 * a, lk.GREEN, 1.4),
                    ],
                    arrows=[((0, 0, 0), P, lk.BLUE), ((0, 0, 0), (1.0, 0, 0), "#000000", 1.4)],
                    points=[((0, 0, 1), "#000000", 3.4), ((0, 0, -1), "#000000", 3.4), ((0, 0, 0), "#000000", 2.6), (P, lk.BLUE, 3.4)],
                    texts=[
                        ((0, 0, 1), "n", "#000000", 90),
                        ((0, 0, -1), "s", "#000000", -90),
                        ((0, 0, 0), "o", "#000000", -150, 6),
                        (P, "p", "#000000", 125, 6),
                        ((1.0, 0, 0), "e_1", "#000000", -90, 8),
                        ((0.4 * math.sin(ph / 2) * math.cos(th), 0.4 * math.sin(ph / 2) * math.sin(th), 0.4 * math.cos(ph / 2)), r"\phi", lk.GREEN, 30, 6),
                        ((0.62 * math.cos(th / 2), 0.62 * math.sin(th / 2), 0), r"\theta", lk.GREEN, 0, 3),
                    ],
                )
            ],
            height=340,
            width=340,
            bias=0.12,
        )

    def charts_figure(phi_deg, theta_deg):
        # one point p of the sphere in the three charts psi, phi_n and phi_s, with its curve of constant phi
        ph, th = math.radians(phi_deg), math.radians(theta_deg)
        x, y, z = math.sin(ph) * math.cos(th), math.sin(ph) * math.sin(th), math.cos(ph)
        u, v = x / (1 - z), y / (1 - z)
        ut, vt = x / (1 + z), y / (1 + z)
        r = 1 / math.tan(ph / 2)  # the radius of the constant-phi circle in the north chart; 1/r in the south chart
        fig = Figure(figsize=(lk.FULL, 3.0), layout="constrained")
        axes = fig.subplots(1, 3)
        a = np.linspace(0, 2 * np.pi, 200)
        for ax, pt, title, lim in (
            (axes[0], (ph, th), r"$\psi(p) = (\phi, \theta)$", None),
            (axes[1], (u, v), r"$\varphi_n(p) = (u, v)$", max(2.0, 1.3 * r)),
            (axes[2], (ut, vt), r"$\varphi_s(p) = (\tilde{u}, \tilde{v})$", max(2.0, 1.2 / r)),
        ):
            ax.set_title(title, fontsize=12)
            if lim is None:
                ax.set_xlim(0, math.pi)
                ax.set_ylim(0, 2 * math.pi)
                ax.set_xlabel(r"$\phi$")
                ax.set_ylabel(r"$\theta$", rotation=0, labelpad=12)
                ax.set_xticks([0, math.pi / 2, math.pi], ["$0$", r"$\pi/2$", r"$\pi$"])
                ax.set_yticks([0, math.pi, 2 * math.pi], ["$0$", r"$\pi$", r"$2\pi$"])
            else:
                ax.set_xlim(-lim, lim)
                ax.set_ylim(-lim, lim)
                ax.set_aspect("equal")
                ax.axhline(0, color="#000000", lw=0.6)
                ax.axvline(0, color="#000000", lw=0.6)
                ax.plot(np.cos(a), np.sin(a), color=lk.GREY, lw=0.8)
                ax.set_xticks([])
                ax.set_yticks([])
            ax.plot(*pt, "o", color=lk.BLUE, ms=6, clip_on=False, zorder=3)
        for ax, (xn, yn) in ((axes[1], ("u", "v")), (axes[2], (r"\tilde{u}", r"\tilde{v}"))):
            ax.set_xlabel(f"${xn}$", labelpad=2)
            ax.set_ylabel(f"${yn}$", rotation=0, labelpad=8)
        axes[1].plot(r * np.cos(a), r * np.sin(a), color=lk.GREEN, lw=1.0)
        axes[2].plot(np.cos(a) / r, np.sin(a) / r, color=lk.GREEN, lw=1.0)
        axes[0].plot([ph, ph], [0, 2 * math.pi], color=lk.GREEN, lw=1.0)
        axes[2].annotate("equator", (0, 1), textcoords="offset points", xytext=(3, 2), color=lk.GREY, fontsize=10, ha="left", va="bottom")
        if r > 0.3:  # the name of the constant-phi circle only when the circle shows beyond the point
            axes[1].annotate(r"$\phi$ = const", (0, -r), textcoords="offset points", xytext=(4, -3), color=lk.GREEN, fontsize=10, ha="left", va="top")
        return fig

    def smooth_figure():
        # a map between manifolds and its coordinate expression in two charts
        sk = lk.sk
        A = "A"
        a, b, H = 3.7, 11.9, 6.4  # centres of M and N, and their height
        fig, ax = sk.sketch((-1.2, 16.8), (-0.9, 8.5))
        M = sk.shape(a, H, 2.6, 1.6, waves=((2, 0.06, 0.6), (3, 0.03, 2.2)))
        N = sk.shape(b, H, 2.6, 1.6, waves=((2, 0.06, 2.0), (3, 0.03, 0.9)))
        for Mx, name, ang, cx, u, v in ((M, "$M$", 160, a, "$U$", rf"$f^{{-1}}({A})$"), (N, "$N$", 20, b, "$f(U)$", f"${A}$")):
            sk.outline(ax, Mx, name=name, at=sk.rim(Mx, ang, 0.4))
            Ax = sk.shape(cx - 0.55, H - 0.3, 1.0, 0.7, waves=((2, 0.06, 1.0), (3, 0.03, 0.3)), tilt=10)
            Bx = sk.shape(cx + 0.55, H - 0.35, 1.0, 0.7, waves=((2, 0.06, -0.6), (3, 0.03, 1.9)), tilt=-12)
            sk.overlap(ax, Ax, Bx)
            sk.outline(ax, Ax, lk.RED, u, sk.rim(Ax, 120, 0.25), va="bottom")
            sk.outline(ax, Bx, lk.BLUE, v, sk.rim(Bx, 60, 0.25), va="bottom")
        sk.maps(ax, sk.rim(M, 0, 0.45), sk.rim(N, 180, 0.45), "$f$", bend=0.15, side=1)
        Y = 2.0
        cL, cR = a - 2.3, b + 2.3
        L = sk.shape(cL, Y, 1.1, 0.85, waves=((2, 0.06, 0.4), (3, 0.03, 1.3)))
        Lo = sk.shape(cL + 0.8, Y, 1.1, 1.2, waves=((2, 0.05, 1.1),))
        R = sk.shape(cR, Y, 1.1, 0.85, waves=((2, 0.06, 2.4), (3, 0.03, 0.2)))
        Ro = sk.shape(cR - 0.8, Y, 1.1, 1.2, waves=((2, 0.05, -0.8),))
        for img, other, col, cut, Rn, nm, cx in ((L, Lo, lk.RED, lk.BLUE, r"$\mathbb{R}^m$", rf"$\varphi(U \cap f^{{-1}}({A}))$", cL),
                                                (R, Ro, lk.BLUE, lk.RED, r"$\mathbb{R}^n$", rf"$\psi(f(U) \cap {A})$", cR)):
            sk.axes(ax, cx - 1.65, Y - 1.4, 3.0, 2.9, Rn)
            sk.overlap(ax, other, img)
            sk.outline(ax, img, col)
            sk.cut(ax, other, img, cut)
            sk.label(ax, (cx - 0.15, Y - 1.75), nm, size=13, va="top")
        sk.maps(ax, (sk.rim(L, 0, 0.45)[0], Y), (cR - 1.65 - 0.45, Y), r"$\psi \circ f \circ \varphi^{-1}$", side=1, gap=0.35)
        sk.maps(ax, sk.rim(M, 232, 0.3), sk.rim(L, 70, 0.35), r"$\varphi$", lk.RED, bend=-0.12, side=-1)
        sk.maps(ax, sk.rim(N, -52, 0.3), sk.rim(R, 110, 0.35), r"$\psi$", lk.BLUE, bend=0.12, side=1)
        return fig

    def curves_figure():
        # curves through p with the same velocity v, and the line p + tv (shared sketch style, lk.sk)
        sk = lk.sk
        fig, ax = sk.sketch((-2.6, 3.4), (-2.2, 2.6))
        t = np.linspace(-1.9, 1.9, 200)
        ax.plot(t, t, color=lk.GREY, lw=sk.LW)
        ax.plot(t + 0.3 * t**2, t - 0.3 * t**2, color=lk.RED, lw=sk.LW)
        ax.plot(t - 0.4 * t**2, t + 0.4 * t**2, color=lk.BLUE, lw=sk.LW)
        sk.maps(ax, (0, 0), (0.75, 0.75), color=lk.GREEN, lw=1.8)
        sk.dot(ax, (0, 0), "$p$", at=(0.25, -0.2), ha="left")
        sk.label(ax, (0.2, 0.75), "$v$", lk.GREEN, ha="right")
        sk.label(ax, (2.0, 1.9), "$p + tv$", lk.GREY, ha="left")
        sk.label(ax, (2.6, 0.45), r"$\gamma(t)$", lk.RED, ha="left")
        sk.label(ax, (0.05, 2.25), r"$\sigma(t)$", lk.BLUE, ha="right")
        return fig

    return angles_scene, charts_figure, curves_figure, smooth_figure, stereo_scene


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figure (in degrees)
    s_phi = lk.slider(5, 175, step=1, value=60, label=r"$\phi$", show_value=False)
    s_theta = lk.slider(1, 359, step=1, value=40, label=r"$\theta$", show_value=False)
    return s_phi, s_theta


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"$\leadsto$ &nbsp; Set of points $M\ni p$",
        r"$\leadsto$ &nbsp; Collection of charts &nbsp; $\mathcal A\ni\varphi_\alpha:U_\alpha\subseteq M\longrightarrow V_\alpha\subseteq\mathbb R^m$",
        r"""
        > • &nbsp; $\bigcup_\alpha U_\alpha=M$

        > • &nbsp; $V_\alpha\subseteq\mathbb R^m$ &nbsp; open sets

        > • &nbsp; $\varphi_\alpha:U_\alpha\overset{\sim}{\longrightarrow}V_\alpha$ &nbsp; bijection

        > • &nbsp; $\varphi_\alpha(U_\alpha\cap U_\beta)\subseteq V_\alpha$, &nbsp; $\varphi_\beta(U_\alpha\cap U_\beta)\subseteq V_\beta$ &nbsp; also open

        > • &nbsp; $\varphi_\beta\circ\varphi_\alpha^{-1}:\varphi_\alpha(U_\alpha\cap U_\beta)\longrightarrow\varphi_\beta(U_\alpha\cap U_\beta)$ &nbsp; smooth with smooth inverse
        """,
        topic="Manifolds",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("Schutz 6.1; Carroll 2.2–2.3; Sasane 1.3, 2.1")
    return


@app.cell(hide_code=True)
def _(lk, stereo_scene):
    # module: charts on the sphere
    # example: the atlas of the two stereographic charts
    lk.example(
        [
            r"$\mathbb S^2=\{(x,y,z)\in\mathbb R^3\mid x^2+y^2+z^2=1\}$",
            r"""
            Choose $n=(0,0,1)$

            > Define &nbsp; $\varphi_n:U_n\longrightarrow V_n$ &nbsp; via

            > > $U_n=\mathbb S^2-\{n\}$, &nbsp; $V_n=\mathbb R^2$

            > > $\varphi_n(x,y,z)=(u,v)=\Big(\dfrac{x}{1-z},\ \dfrac{y}{1-z}\Big)$

            > > $\dfrac{(u,v,0)}{1}=\dfrac{(u-x,\ v-y,\ 0)}{z}$

            > > > $\Longrightarrow$ &nbsp; $\varphi_n^{-1}(u,v)=\Big(\dfrac{2u}{1+u^2+v^2},\ \dfrac{2v}{1+u^2+v^2},\ \dfrac{-1+u^2+v^2}{1+u^2+v^2}\Big)$

            Similarly, choose $s=(0,0,-1)$

            > Define &nbsp; $\varphi_s:U_s\longrightarrow V_s$ &nbsp; via

            > > $U_s=\mathbb S^2-\{s\}$, &nbsp; $V_s=\mathbb R^2$

            > > $\varphi_s(x,y,z)=(\tilde u,\tilde v)=\Big(\dfrac{x}{1+z},\ \dfrac{y}{1+z}\Big)$

            > > > $\Longrightarrow$ &nbsp; $\varphi_s^{-1}(\tilde u,\tilde v)=\Big(\dfrac{2\tilde u}{1+\tilde u^2+\tilde v^2},\ \dfrac{2\tilde v}{1+\tilde u^2+\tilde v^2},\ \dfrac{1-\tilde u^2-\tilde v^2}{1+\tilde u^2+\tilde v^2}\Big)$
            """,
            lk.figure(stereo_scene()),
            r"""
            • &nbsp; $U_n\cup U_s=(\mathbb S^2-\{n\})\cup(\mathbb S^2-\{s\})=\mathbb S^2$

            • &nbsp; $V_n=\mathbb R^2$, &nbsp; $V_s=\mathbb R^2$ &nbsp; open

            • &nbsp; $\varphi_n:U_n\to V_n$, &nbsp; $\varphi_s:U_s\to V_s$ &nbsp; bijective

            $\begin{aligned}\text{•}\ \ \ &\varphi_n(U_n\cap U_s)=\varphi_n(\mathbb S^2-\{n,s\})=\mathbb R^2-\{(0,0)\}\\&\varphi_s(U_n\cap U_s)=\varphi_s(\mathbb S^2-\{n,s\})=\mathbb R^2-\{(0,0)\}\quad\text{open!}\end{aligned}$

            $\displaystyle\begin{alignedat}{2}\text{•}\ \ \ &\varphi_s\circ\varphi_n^{-1}(u,v)&&=\varphi_s\Big(\frac{2u}{1+u^2+v^2},\ \frac{2v}{1+u^2+v^2},\ \frac{-1+u^2+v^2}{1+u^2+v^2}\Big)\\[0.3em]&&&=\Big(\frac{2u}{2(u^2+v^2)},\ \frac{2v}{2(u^2+v^2)}\Big)\\[0.3em]&&&=\Big(\frac{u}{u^2+v^2},\ \frac{v}{u^2+v^2}\Big)=(\tilde u,\tilde v)\end{alignedat}$

            > $\leadsto$ &nbsp; diffeomorphism &nbsp; $\mathbb R^2-\{(0,0)\}\longrightarrow\mathbb R^2-\{(0,0)\}$

            > > we can differentiate it infinitely many times

            > > it is invertible &nbsp; $(\varphi_s\circ\varphi_n^{-1})^{-1}=\varphi_n\circ\varphi_s^{-1}$

            > > and inverse is also infinitely differentiable

            > > > $\varphi_n\circ\varphi_s^{-1}(\tilde u,\tilde v)=\Big(\dfrac{\tilde u}{\tilde u^2+\tilde v^2},\ \dfrac{\tilde v}{\tilde u^2+\tilde v^2}\Big)$

            $\therefore$ &nbsp; $\mathbb S^2$, &nbsp; $\mathcal A=\{\varphi_n,\varphi_s\}$ &nbsp; is a 2-manifold.
            """,
        ],
        label="ex-sphere-atlas",
    )
    return


@app.cell(hide_code=True)
def _(angles_scene, charts_figure, lk, s_phi, s_theta):
    # module: charts on the sphere
    # remark: more compatible charts, the stereographic charts at any point and the polar and azimuthal angles
    lk.remark(
        [
            r"There are many more charts $\varphi:U\subseteq\mathbb S^2\to V\subseteq\mathbb R^2$ which are “compatible” with $\varphi_n$ and $\varphi_s$ in the sense",
            r"$$\varphi_\alpha\circ\varphi^{-1}:\varphi(U\cap U_\alpha)\longrightarrow\varphi_\alpha(U\cap U_\alpha)\quad\text{is a diffeomorphism for }\alpha=n,s.$$",
            lk.aside(
                r"> $\leadsto$ &nbsp; choose any $q\in\mathbb S^2$ and define &nbsp; $\varphi_q:\mathbb S^2-\{q\}\to\mk{\mathbb R^2}$ &nbsp; the stereographic projection based at $q$",
                r"$\mathbb R^2\approx(q-o)^\perp\subseteq\mathbb R^3$",
            ),
            r"""
            > $\leadsto$ &nbsp; choose $q=n\in\mathbb S^2$ and $e_1\in(n-o)^\perp$ and define

            > > $\phi:\mathbb S^2-\{n,s\}\to(0,\pi)$, &nbsp;&nbsp; $\theta:\mathbb S^2-\{\text{half meridian through }e_1\}\to(0,2\pi)$

            > > $\cos\phi(p)=\langle p-o,n-o\rangle$, &nbsp;&nbsp; $\cos\theta(p)=\dfrac{\langle p-o,e_1\rangle}{\sin\phi(p)}$

            > > the polar and azimuthal angles, giving

            $$\psi:\mathbb S^2-\{\text{half meridian through }e_1\}\longrightarrow(0,\pi)\times(0,2\pi)\subset\mathbb R^2.$$
            """,
            lk.figure(angles_scene()),
            r"""
            > > $\displaystyle\begin{aligned}\psi^{-1}(\phi,\theta)&=(\sin\phi\cos\theta,\ \sin\phi\sin\theta,\ \cos\phi)\\[0.3em]&=(x,y,z)\\[0.3em]&=\Big(\frac{2u}{1+u^2+v^2},\ \frac{2v}{1+u^2+v^2},\ \frac{-1+u^2+v^2}{1+u^2+v^2}\Big)\\[0.3em]&=\varphi_n^{-1}(u,v)\end{aligned}$
            """,
            lk.aside(
                r"> > > $\Longrightarrow$ &nbsp; $\mk{(u,v)=\varphi_n\circ\psi^{-1}(\phi,\theta)}=\big(\cot\tfrac{\phi}{2}\cos\theta,\ \cot\tfrac{\phi}{2}\sin\theta\big)$",
                r"diffeomorphism from $(0,\pi)\times(0,2\pi)$<br>to $\mathbb R^2-\{\lambda e_1,\ \lambda\geq0\}$",
            ),
            lk.interactive(charts_figure(s_phi.value, s_theta.value), controls=[s_phi, s_theta]),
            lk.aside(
                r"$\therefore$ &nbsp; $\mathbb S^2$, &nbsp; $\mk{\mathcal A}=\{\varphi_n,\varphi_s,\varphi_q,\psi\}$ &nbsp; is also a 2-manifold.",
                r"we assume $\mathcal A$ contains all possible<br>compatible charts (maximal atlas)",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk, smooth_figure):
    # module: smooth maps
    # definition: smooth maps between manifolds
    lk.module(
        lk.definition(
            [
                r"Given two manifolds $(M^m,\mathcal A)$ and $(N^n,\mathcal B)$ we can define smooth maps from $M$ to $N$ using their charts: &nbsp; $f:M\to N$ is called **smooth** (or differentiable) (or continuous) (or any adjective)",
                r"if for any choices of charts",
                r"$$\varphi:U\subseteq M\longrightarrow V\subseteq\mathbb R^m,\qquad\psi:A\subseteq N\longrightarrow B\subseteq\mathbb R^n,$$",
                r"the local representation of $f$ in those charts",
                r"$$\psi\circ f\circ\varphi^{-1}:\underset{\begin{matrix}\cap\\\mathbb R^m\end{matrix}}{\varphi(U\cap f^{-1}(A))}\longrightarrow\underset{\begin{matrix}\cap\\\mathbb R^n\end{matrix}}{\psi(f(U)\cap A)},$$",
                r"is smooth (or differentiable) (or continuous) (or any adjective)",
            ],
            label="def-smooth-map",
        ),
        lk.prose(lk.figure(smooth_figure())),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tangent vectors
    # what is needed next
    lk.prose(
        r"""
        To define derivatives of smooth functions, we need a notion of “directions” on manifolds

        > $\leadsto$ &nbsp; tangent vectors
        """
    )
    return


@app.cell(hide_code=True)
def _(curves_figure, lk):
    # module: tangent vectors
    # derivatives on affine spaces use paths, and paths exist on manifolds too
    lk.prose(
        r"On affine spaces &nbsp; $(\mathbb A,\mathbb V,-)$, &nbsp; $(\mathbb B,\mathbb W,-)$",
        r"> given &nbsp; $p\in\mathbb A$ &nbsp; and &nbsp; $v\in\mathbb V$ &nbsp; and &nbsp; $f:\mathbb A\to\mathbb B$",
        r"> > $\leadsto$ &nbsp; derivative of $f$ at $p$ in the direction of $v$",
        lk.aside(
            r"$$\begin{aligned}Df_p(v)&=\lim_{t\to0}\frac{f(\mk{p+tv})-f(p)}{t}\\[0.3em]&=\lim_{t\to0}\frac{f(\mk{\gamma(t)})-f(p)}{t}\end{aligned}$$",
            [(1, "using affine structure"), (2, r"using curves on $\mathbb A$")],
            rows=2,
        ),
        lk.aside(
            r"for *any* curve &nbsp; $\gamma:\mathbb R\to\mathbb A$ &nbsp; such that &nbsp; $\begin{cases}\gamma(0)=p\in\mathbb A\\\mk{\gamma'(0)}=v\in\mathbb V\end{cases}$",
            r"$\gamma'(0)=\displaystyle\lim_{s\to0}\frac{\gamma(s)-\gamma(0)}{s}$",
        ),
        lk.figure(curves_figure()),
        r"> $\leadsto$ &nbsp; for $Df_p(v)$, all paths through $p$ with velocity $v$ are equivalent!",
        lk.gap(),
        r"""
        On a manifold $(M,\mathcal A)$

        > $\leadsto$ &nbsp; no immediate notion of vectors

        > $\leadsto$ &nbsp; but we can also consider paths through points!

        > $\leadsto$ &nbsp; we will *define* vectors on $M$ as equivalence classes of paths with “same velocity” in charts!
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tangent vectors
    # definition: tangent vector
    lk.definition(
        [
            r"$M$ $m$-manifold, &nbsp; $p\in M$, &nbsp; a **tangent vector** to $M$ at $p$ is an equivalence class of smooth paths on $M$",
            lk.aside(
                r"$$v_p=[\gamma]_p=\left\{\sigma:\mathbb R\to M\ \middle|\ \begin{matrix}\sigma(0)=\gamma(0)=p\ \text{ and}\\(\mk{\varphi}\circ\sigma)'(0)=(\varphi\circ\gamma)'(0)\end{matrix}\right\}.$$",
                r"for any chart $\varphi:U\subseteq M\to V\subseteq\mathbb R^m$<br>with $p\in U$",
            ),
            r"In other words, two smooth paths $\gamma,\sigma$ are considered equivalent if in a chart $\varphi$",
            r"$$\begin{cases}(\varphi\circ\gamma)(0)=(\varphi\circ\sigma)(0)&\leadsto\quad\gamma(0)=\sigma(0)=p\\[0.3em](\varphi\circ\gamma)'(0)=(\varphi\circ\sigma)'(0)&\leadsto\quad\text{“}\gamma'(0)=\sigma'(0)=v\text{”}.\end{cases}$$",
        ],
        label="def-tangent-vector",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tangent vectors
    # remark: independent of the chart
    lk.remark(
        r"""
        If $\gamma\sim\sigma$ with respect to one chart then $\gamma\sim\sigma$ with respect to any other!

        $\psi\circ\gamma(t)=\underbrace{\psi\circ\varphi^{-1}}_{\footnotesize\text{change of coordinates}}\circ\,\varphi\circ\gamma(t)$

        > $\Longrightarrow$ &nbsp; $(\psi\circ\gamma)'(t)=\underbrace{D(\psi\circ\varphi^{-1})_{\varphi\circ\gamma(t)}}_{\footnotesize\text{Jacobian matrix}}\big((\varphi\circ\gamma)'(t)\big)$

        > $\Longrightarrow$ &nbsp; $[\gamma]_p$ is defined independent of the choice of charts!
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tangent vectors
    # definition: tangent space
    lk.definition(
        r"""
        We denote by

        $$\begin{aligned}T_pM&=\text{set of tangent vectors to }M\text{ at }p\\[0.3em]&=\textbf{tangent space}\text{ to }M\text{ at }p.\end{aligned}$$
        """,
        label="def-tangent-space",
    )
    return


if __name__ == "__main__":
    app.run()
