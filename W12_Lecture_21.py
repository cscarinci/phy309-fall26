import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 21 · Curvature of (M, g)", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import sys

    import marimo as mo
    import numpy as np
    from matplotlib.figure import Figure

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return Figure, lk, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(21, r"Curvature of $(M,g)$")
    return


@app.cell(hide_code=True)
def _(Figure, lk, np):
    # Helpers of this lecture: bare 2D drawings, and the three figures

    def drawing(xlim, ylim, width):
        """A figure with one bare axis (no frame) filling it, its height set by the ranges."""
        fig = Figure(figsize=(width, width * (ylim[1] - ylim[0]) / (xlim[1] - xlim[0])))
        ax = fig.add_axes((0, 0, 1, 1))
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def transport_sketch():
        # a path from gamma(a) to gamma(b) that makes one loop (black); X_0 at gamma(a) (black), the parallel field
        # X_gamma(t) along it (red), and P(X_0) at gamma(b) (green); the point gamma(t) on the loop (red)
        # a rising arc from gamma(a), a small loop hanging below, then an arc up to gamma(b)
        t = np.linspace(-4.6, 3.4, 800)
        x = 0.6 * t - 1.6 * np.sin(t)
        y = -1.0 * np.cos(t) + 0.1 * (t - np.sqrt(t**2 + 0.3))
        fig, ax = drawing((-4.9, 3.6), (-1.5, 2.2), 4.6)
        ax.plot(x, y, color="#000000", lw=1.6)
        # the crossing: the path passes under on its way into the loop and over on its way out
        over = np.abs(t - 1.848) < 0.3
        ax.plot(x[over], y[over], color="#ffffff", lw=7, solid_capstyle="butt", zorder=2)
        ax.plot(x[over], y[over], color="#000000", lw=1.6, zorder=3)
        up = np.array([0.08, 0.9])
        at = lambda u: int(np.argmin(np.abs(t - u)))
        for u in (-3.75, -3.05, -1.25, 2.3, 3.0):
            k = at(u)
            lk.arrow(ax, (x[k], y[k]), (x[k] + up[0], y[k] + up[1]), lk.RED, lw=1.4)
        lk.arrow(ax, (x[0], y[0]), (x[0] + up[0], y[0] + up[1]), "#000000", lw=1.4)
        lk.arrow(ax, (x[-1], y[-1]), (x[-1] + up[0], y[-1] + up[1]), lk.GREEN, lw=1.4)
        kt = at(-1.25)
        ax.plot([x[kt]], [y[kt]], "o", color=lk.RED, ms=4)
        ax.text(x[kt] + 0.15, y[kt] - 0.12, r"$\gamma(t)$", color=lk.RED, fontsize=13, va="top")
        ax.text(x[kt] + 0.2, y[kt] + 0.55, r"$X_{\gamma(t)}$", color=lk.RED, fontsize=13, ha="left", va="center")
        ax.text(x[0], y[0] - 0.12, r"$\gamma(a)$", fontsize=13, ha="center", va="top")
        ax.text(x[-1], y[-1] - 0.12, r"$\gamma(b)$", fontsize=13, ha="center", va="top")
        ax.text(x[0] - 0.08, y[0] + 0.85, r"$X_0$", fontsize=13, ha="right")
        ax.text(x[-1] + 0.08, y[-1] + 0.98, r"$P^\gamma_{a,b}(X_0)$", color=lk.GREEN, fontsize=13, ha="center", va="bottom")
        return fig

    def parallelogram_sketch():
        # the closed path gamma = gamma_1 ... gamma_4 around the parallelogram with sides eps X and delta Y at p
        # (black, with its direction); Z_p and its transports Z_1, Z_2, Z_3 at the corners (red), Z_4 back at p (blue),
        # turned a little more at each corner
        X, Y = np.array([2.6, 0.45]), np.array([0.55, 2.0])
        c = [np.zeros(2), X, X + Y, Y]
        fig, ax = drawing((-1.9, 6.6), (-0.65, 3.4), 5.6)
        for k in range(4):
            a, b = c[k], c[(k + 1) % 4]
            ax.plot([a[0], b[0]], [a[1], b[1]], color="#000000", lw=1.5)
            lk.arrow(ax, a + 0.45 * (b - a), a + 0.58 * (b - a), "#000000", lw=1.5)
        for q in c:
            ax.plot([q[0]], [q[1]], "o", color="#000000", ms=3.5)
        ang = np.radians([30, 36, 44, 53, 62])
        L = 1.0
        for k, (q, name) in enumerate(zip(c, ("Z_p", "Z_1", "Z_2", "Z_3"))):
            tip = q + L * np.array([np.cos(ang[k]), np.sin(ang[k])])
            lk.arrow(ax, q, tip, lk.RED, lw=1.4)
            ax.text(tip[0] + 0.08, tip[1] + 0.02, f"${name}$", color=lk.RED, fontsize=13)
        tip4 = L * np.array([np.cos(ang[4]), np.sin(ang[4])])
        lk.arrow(ax, (0, 0), tip4, lk.BLUE, lw=1.4)
        ax.text(tip4[0] + 0.02, tip4[1] + 0.1, "$Z_4$", color=lk.BLUE, fontsize=13, ha="center")
        mid = lambda k: (c[k] + c[(k + 1) % 4]) / 2
        ax.text(*(mid(0) + [0.1, -0.3]), r"$\gamma_1$", fontsize=13, ha="center")
        ax.text(*(mid(1) + [0.25, -0.1]), r"$\gamma_2$", fontsize=13)
        ax.text(*(mid(2) + [0.0, 0.18]), r"$\gamma_3$", fontsize=13, ha="center")
        ax.text(*(mid(3) + [-0.2, 0.15]), r"$\gamma_4$", fontsize=13, ha="right")
        ax.text(-0.12, -0.18, r"$p=\varphi^{-1}(0)$", fontsize=12, ha="right", va="top")
        ax.text(X[0] + 0.12, X[1] - 0.18, r"$\varphi^{-1}(\varepsilon X^ie_i)$", fontsize=12, va="top")
        ax.text(X[0] + Y[0] + 0.15, X[1] + Y[1] - 0.12, r"$\varphi^{-1}(\varepsilon X^ie_i+\delta Y^je_j)$", fontsize=12, ha="left", va="top")
        ax.text(Y[0] - 0.15, Y[1] + 0.12, r"$\varphi^{-1}(\delta Y^je_j)$", fontsize=12, ha="right", va="bottom")
        return fig

    def latitude_scene(f0, tmax):
        # the sphere (radius drawn as 2) with the circle of latitude phi_0 (grey, with its direction) from gamma(0);
        # X parallel along it (red), from X_0 = X_gamma(0); after one turn P(X_0) = X_gamma(2 pi) (green), turned by
        # 2 pi cos(phi_0) against X_0. Components in the unit frame (d_phi, d_theta / sin phi) from the solution of the example
        A, B = -0.75, 0.66
        t0 = -0.35  # gamma(0) in front, a little to the left

        def at(t):
            return 2 * np.array([np.sin(f0) * np.cos(t0 + t), np.sin(f0) * np.sin(t0 + t), np.cos(f0)])

        def X(t, length=0.7):
            c = np.cos(f0)
            ef = np.array([np.cos(f0) * np.cos(t0 + t), np.cos(f0) * np.sin(t0 + t), -np.sin(f0)])
            et = np.array([-np.sin(t0 + t), np.cos(t0 + t), 0.0])
            v = (A * np.cos(t * c) + B * np.sin(t * c)) * ef + (-A * np.sin(t * c) + B * np.cos(t * c)) * et
            return at(t), at(t) + length * v / np.linalg.norm(v)

        s, t = np.meshgrid(np.linspace(0, np.pi, 25), np.linspace(0, 2 * np.pi, 97), indexing="ij")
        T = np.linspace(0, 2 * np.pi, 241)
        circ = np.array([at(u) for u in T])
        head = np.array([at(u) for u in np.linspace(np.pi - 0.15, np.pi + 0.15, 9)])
        done = tmax >= 2 * np.pi - 1e-6
        arrows = [(*X(u), lk.RED, 1.8) for u in np.arange(0, tmax - 1e-6, np.pi / 4)]
        arrows.append((*X(tmax), lk.GREEN if done else lk.RED, 1.8))
        now = (tuple(X(tmax)[1]), r"P^\gamma_{0,2\pi}(X_0)" if done else r"X_{\gamma(t)}", lk.GREEN if done else lk.RED, 180, 6)
        return lk.turntable(
            0,
            22,
            "the sphere with a circle of latitude from gamma(0); the vector X_0 parallel transported once around it comes back as P(X_0), turned",
            [
                lk.panel(
                    1.0,
                    surfaces=[lk.sheet(2 * np.sin(s) * np.cos(t), 2 * np.sin(s) * np.sin(t), 2 * np.cos(s), alpha=0.45)],  # smooth, outlined
                    outlines=[("sphere", (0, 0, 0), 2.0, lk.GREY, 1.0)],
                    lines=[(circ[:, 0], circ[:, 1], circ[:, 2], lk.GREY, 2.0)],
                    arcs=[(head[:, 0], head[:, 1], head[:, 2], lk.GREY, 2.0)],
                    arrows=arrows,
                    points=[(tuple(at(0)), "#000000")],
                    texts=[
                        (tuple(at(0)), r"\gamma(0)=\gamma(2\pi)", "#000000", -30, 12),
                        (tuple(X(0)[1]), r"X_0", lk.RED, 90, 6),
                        now,
                    ],
                    box=((-1.64, 1.64), (-1.64, 1.64), (-1.64, 1.64)),
                )
            ],
            height=460,
            key="L21-latitude",
            apart=True,
        )

    return latitude_scene, parallelogram_sketch, transport_sketch


@app.cell(hide_code=True)
def _(lk, np):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    # phi_0 in steps of pi/20, t in steps of pi/12, both read out as multiples of pi
    phi0_s = lk.slider(steps=[k * np.pi / 20 for k in range(2, 19)], value=[k * np.pi / 20 for k in range(2, 19)][4], label=r"$\phi_0$", show_value=False)
    t_s = lk.slider(steps=[k * np.pi / 12 for k in range(0, 25)], value=[k * np.pi / 12 for k in range(0, 25)][-1], label="$t$", show_value=False)
    return phi0_s, t_s


@app.cell(hide_code=True)
def _(latitude_scene, phi0_s, t_s):
    # the scene of Fig 21.2, in place by its sliders
    latitude_scene(phi0_s.value, t_s.value)
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"""
        Geodesics of Schwarzschild spacetime

        $\leadsto$ &nbsp; orbits, perihelion precession, and bending light rays

        $\leadsto$ &nbsp; gravitational physics beyond Newtonian mechanics (no forces acting on particles!)
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(
        lk.aside(
            r"<span class='lk-mark'>Curvature</span> of $(M,g)$",
            "origin of gravitation in GR",
        ),
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: parallel transport
    # definition: parallel vector field
    lk.definition(
        r"""
        A vector field $X_{\gamma(t)}$ along a path $\gamma(t)$ is called **parallel** if its covariant derivative is zero

        $$
        \begin{aligned}
        \frac{D}{dt}X_{\gamma(t)}&=0\qquad\leadsto\quad X_{\gamma(t)}\text{ is covariantly constant}\\
        &\overset{\varphi}{=}\big(\underbrace{\dot X^k(t)+\Gamma^k_{ij}(t)\,\dot x^i(t)\,X^j(t)}_{\mathclap{\footnotesize\text{1st order linear system of ODEs}}}\big)\,\partial_k|_{\gamma(t)}.
        \end{aligned}
        $$

        > > $\Longrightarrow$ &nbsp; $\exists!$ solution with $X_{\gamma(a)}=X_0$, &nbsp; $\forall\,X_0\in T_{\gamma(a)}M$
        """,
        label="def-parallel",
    )
    return


@app.cell(hide_code=True)
def _(lk, transport_sketch):
    # module: parallel transport
    # definition: parallel transport
    lk.module(
        lk.definition(
            [
                r"Given $\gamma(t)$ path, the **parallel transport** along $\gamma$ from $\gamma(a)$ to $\gamma(b)$ is the map",
                lk.aside(
                    r"$$P^\gamma_{a,b}:T_{\gamma(a)}M\longrightarrow T_{\gamma(b)}M,\qquad\mk{X_0}\longmapsto P^\gamma_{a,b}(X_0)=X_{\gamma(b)}.$$",
                    r"$X_0=X_{\gamma(a)}$",
                ),
            ],
            label="def-transport",
        ),
        lk.prose(lk.figure(transport_sketch())),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: parallel transport
    # remark: properties of parallel transport
    lk.remark(
        r"""
        Since ${\large\tfrac{D}{dt}}X_{\gamma(t)}=0$ is a linear ODE, $P^\gamma_{a,b}:T_{\gamma(a)}M\longrightarrow T_{\gamma(b)}M$ is a linear map!

        $P^\gamma_{b,a}\circ P^\gamma_{a,b}=\mathrm{Id}_{T_{\gamma(a)}M}$ &nbsp; $\Longrightarrow$ &nbsp; $P^\gamma_{a,b}$ is invertible!

        $$
        g_{\gamma(b)}\big(P^\gamma_{a,b}(X_0),P^\gamma_{a,b}(Y_0)\big)=g_{\gamma(a)}(X_0,Y_0)
        $$

        $$
        \begin{aligned}
        \frac{d}{dt}\,g_{\gamma(t)}(X_{\gamma(t)},Y_{\gamma(t)})&=g\Big(\frac{D}{dt}X_{\gamma(t)},Y_{\gamma(t)}\Big)+g\Big(X_{\gamma(t)},\frac{D}{dt}Y_{\gamma(t)}\Big)=0\\
        &\Longrightarrow\quad g_{\gamma(t)}(X_{\gamma(t)},Y_{\gamma(t)})\text{ is constant}
        \end{aligned}
        $$

        > $\Longrightarrow$ &nbsp; $P^\gamma_{a,b}$ preserves the metric!

        $$
        \frac{D}{dt}X_{\gamma(t)}=\lim_{h\to0}\frac{P^\gamma_{t+h,t}(X_{\gamma(t+h)})-X_{\gamma(t)}}{h}
        $$

        > $\Longrightarrow$ &nbsp; $P^\gamma_{a,b}$ gives us a notion of congruence along curves on manifolds!
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: parallel transport
    # remark: Euclidean space
    lk.remark(
        r"""
        In $\mathbb E^m$ with Cartesian coordinates $\Gamma^k_{ij}=0$

        > $\leadsto$ &nbsp; $X_{\gamma(t)}$ is parallel &nbsp; $\Longleftrightarrow$ &nbsp; has constant components

        > <span class="lk-ghost">$\leadsto$ &nbsp; $X_{\gamma(t)}$ is parallel &nbsp;</span>$\Longleftrightarrow$ &nbsp; obtained by congruence

        > > $\Longrightarrow$ &nbsp; we can extend $X_0\in T_{\gamma(a)}\mathbb E^m$ to a “constant” vector field $X_0\in\Gamma(T\mathbb E^m)$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk, np, phi0_s, t_s):
    from math import gcd

    def pi_frac(v, n):
        # the value v = k pi / n of a slider as a reduced multiple of pi
        k = round(v * n / np.pi)
        if k == 0:
            return "0"
        d = gcd(k, n)
        top = (r"\pi" if k // d == 1 else f"{k // d}\\pi")
        return top if n // d == 1 else rf"\tfrac{{{top}}}{{{n // d}}}"

    # module: parallel transport
    # example: circle of latitude on the sphere
    lk.example(
        [
            r"""
            $M=\mathbb S^2$, &nbsp; $\gamma(t)\overset{\psi}{=}(\phi_0,t)$, &nbsp; $t\in[0,2\pi]$

            $\gamma'(t)\overset{\psi}{=}\partial_\theta|_{\gamma(t)}$, &nbsp; $X_{\gamma(t)}\overset{\psi}{=}X^\phi(t)\,\partial_\phi|_{\gamma(t)}+X^\theta(t)\,\partial_\theta|_{\gamma(t)}$

            $\Gamma^\phi_{ij}=\begin{bmatrix}0&0\\0&-\sin\phi\cos\phi\end{bmatrix}$, &nbsp; $\Gamma^\theta_{ij}=\begin{bmatrix}0&\cot\phi\\\cot\phi&0\end{bmatrix}$

            $X_{\gamma(t)}$ parallel along $\gamma$

            $$
            \begin{aligned}
            \Longleftrightarrow\quad&
            \begin{cases}
            \dot X^\phi-\sin\phi_0\cos\phi_0\,X^\theta=0\\
            \dot X^\theta+\cot\phi_0\,X^\phi=0
            \end{cases}\\[0.4em]
            \Longrightarrow\quad&
            \begin{cases}
            X^\phi(t)=A\cos(t\cos\phi_0)+B\sin(t\cos\phi_0)\\
            X^\theta(t)=-{\large\tfrac{A}{\sin\phi_0}}\sin(t\cos\phi_0)+{\large\tfrac{B}{\sin\phi_0}}\cos(t\cos\phi_0)
            \end{cases},
            \end{aligned}
            $$

            $$
            \begin{aligned}
            \Longrightarrow\quad X^\phi(2\pi)&=A\cos(2\pi\cos\phi_0)+B\sin(2\pi\cos\phi_0)\neq A=X^\phi(0)\\
            X^\theta(2\pi)&=-\frac{A}{\sin\phi_0}\sin(2\pi\cos\phi_0)+\frac{B}{\sin\phi_0}\cos(2\pi\cos\phi_0)\neq\frac{B}{\sin\phi_0}=X^\theta(0).
            \end{aligned}
            $$
            """,
            lk.aside(
                r"$\Longrightarrow$ &nbsp; $P^\gamma_{0,2\pi}(X_0)\neq X_0$ &nbsp; (unless <span class='lk-mark'>$\phi_0=\pi/2$</span>!)",
                "geodesic!",
            ),
            lk.interactive(lk.frame("L21-latitude", 460), controls=[phi0_s, t_s], readout=rf"$\phi_0={pi_frac(phi0_s.value, 20)},\quad t={pi_frac(t_s.value, 12)}$"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Riemann tensor
    # definition: Riemann curvature tensor
    lk.definition(
        r"""
        The **Riemann curvature tensor** of $(M,g)$ is the $(1,3)$-tensor field $\mathrm{Riem}\in\Gamma(TM^1_3)$

        $$
        \mathrm{Riem}(X,Y)\,Z=\nabla_X(\nabla_YZ)-\nabla_Y(\nabla_XZ)-\nabla_{[X,Y]}Z,
        $$

        measuring the non-commutativity of the connection
        """,
        label="def-riem",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Riemann tensor
    # remark: Lie bracket
    lk.remark(
        [
            lk.aside(
                r"Here &nbsp; $\mk{[X,Y]}\overset{\varphi}{=}(X^i\,\partial_iY^k-Y^j\,\partial_jX^k)\,\partial_k\in\Gamma(TM)$",
                r"Lie bracket of $X$ and $Y$<br>= commutator of $X$ and $Y$",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Riemann tensor
    # computation: components of Riem (struck-through terms cancel)
    lk.prose(
        r"""
        $$
        \begin{aligned}
        \nabla_X(\nabla_YZ)&\overset{\varphi}{=}X^i\,\nabla_{\partial_i}\big(Y^j\,\nabla_{\partial_j}(Z^l\,\partial_l)\big)=X^i\Big[\cancel{\partial_iY^j\,(\partial_jZ^l+\Gamma^l_{jk}Z^k)}\,\partial_l\\
        &\qquad+Y^j\,(\cancel{\partial_i\partial_jZ^l}+\partial_i\Gamma^l_{jk}\,Z^k+\cancel{\Gamma^l_{jk}\,\partial_iZ^k})\,\partial_l+Y^j\,(\cancel{\partial_jZ^m}+\Gamma^m_{jk}Z^k)\,\Gamma^l_{im}\,\partial_l\Big]\\[0.6em]
        \nabla_Y(\nabla_XZ)&\overset{\varphi}{=}Y^j\,\nabla_{\partial_j}\big(X^i\,\nabla_{\partial_i}(Z^l\,\partial_l)\big)=Y^j\Big[\cancel{\partial_jX^i\,(\partial_iZ^l+\Gamma^l_{ik}Z^k)}\,\partial_l\\
        &\qquad+X^i\,(\cancel{\partial_j\partial_iZ^l}+\partial_j\Gamma^l_{ik}\,Z^k+\cancel{\Gamma^l_{ik}\,\partial_jZ^k})\,\partial_l+X^i\,(\cancel{\partial_iZ^m}+\Gamma^m_{ik}Z^k)\,\Gamma^l_{jm}\,\partial_l\Big]\\[0.6em]
        \nabla_{[X,Y]}Z&\overset{\varphi}{=}(\cancel{X^i\,\partial_iY^k}-\cancel{Y^j\,\partial_jX^k})\,(\partial_kZ^l+\Gamma^l_{km}Z^m)\,\partial_l
        \end{aligned}
        $$

        $$
        \therefore\quad\mathrm{Riem}(X,Y)\,Z\overset{\varphi}{=}\big(\overbrace{\partial_i\Gamma^k_{jl}-\partial_j\Gamma^k_{il}+\Gamma^k_{im}\Gamma^m_{jl}-\Gamma^k_{jm}\Gamma^m_{il}}^{\footnotesize R^k{}_{lij}\ \text{components of Riem}}\big)\,X^iY^jZ^l\,\partial_k
        $$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk, parallelogram_sketch):
    # module: curvature and parallel transport
    # lead-in: the closed path
    lk.prose(
        r"""
        How does this relate to parallel transport?

        Given $p\in M$ and $X_p,Y_p\in T_pM$, choose $\varphi$ with $\varphi(p)=0$, $X_p\overset{\varphi}{=}X^i\,\partial_i|_p$, $Y_p\overset{\varphi}{=}Y^j\,\partial_j|_p$,
        and consider the closed path $\gamma$ following

        $$
        \begin{aligned}
        \gamma_1(t)&=\varphi^{-1}(t\,X^ie_i),&t&\in[0,\varepsilon]\\
        \gamma_2(t)&=\varphi^{-1}(\varepsilon X^ie_i+t\,Y^je_j),&t&\in[0,\delta]\\
        \gamma_3(t)&=\varphi^{-1}((\varepsilon-t)\,X^ie_i+\delta\,Y^je_j),&t&\in[0,\varepsilon]\\
        \gamma_4(t)&=\varphi^{-1}((\delta-t)\,Y^je_j),&t&\in[0,\delta],
        \end{aligned}
        $$

        for sufficiently small $\varepsilon,\delta>0$
        """,
        lk.figure(parallelogram_sketch()),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: curvature and parallel transport
    # theorem: curvature from parallel transport around a loop
    lk.theorem(
        r"""
        Given $Z_p\in T_pM$, let

        $$
        Z_1=P^{\gamma_1}_{0,\varepsilon}(Z_p),\quad Z_2=P^{\gamma_2}_{0,\delta}(Z_1),\quad Z_3=P^{\gamma_3}_{0,\varepsilon}(Z_2),\quad Z_4=P^{\gamma_4}_{0,\delta}(Z_3).
        $$

        Then

        $$
        \lim_{\varepsilon,\delta\to0}\frac{Z_4-Z_p}{\varepsilon\delta}=-\mathrm{Riem}(X_p,Y_p)\,Z_p.
        $$
        """,
        label="thm-holonomy",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: curvature and parallel transport
    # proof idea
    lk.sketch(
        r"""
        Taylor expansions in $\varepsilon$ and $\delta$

        $$
        \begin{aligned}
        Z_1^k&\approx Z^k-\varepsilon\,\Gamma^k_{il}X^iZ^l+\frac{\varepsilon^2}{2}\big(\Gamma^k_{im}\Gamma^m_{jl}-\partial_i\Gamma^k_{jl}\big)X^iX^jZ^l+\dots\\
        &\ \ \vdots\\
        Z_4^k&\approx Z^k+\varepsilon\delta\,\big(\Gamma^k_{jm}\Gamma^m_{il}-\Gamma^k_{im}\Gamma^m_{jl}+\partial_j\Gamma^k_{il}-\partial_i\Gamma^k_{jl}\big)X^iY^jZ^l+\dots
        \end{aligned}
        $$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: sphere
    # example: curvature of the sphere
    lk.example(
        r"""
        $M=\mathbb S^2$, &nbsp; $g\overset{\psi}{=}d\phi\,d\phi+(\sin\phi)^2\,d\theta\,d\theta$

        $\Gamma^\phi_{ij}=\begin{bmatrix}0&0\\0&-\sin\phi\cos\phi\end{bmatrix}$, &nbsp; $\Gamma^\theta_{ij}=\begin{bmatrix}0&\cot\phi\\\cot\phi&0\end{bmatrix}$

        $$
        \underbrace{R^k{}_{lij}}_{\mathclap{\footnotesize 2^4\text{ components}}}=\underbrace{\partial_i\Gamma^k_{jl}-\partial_j\Gamma^k_{il}+\Gamma^k_{im}\Gamma^m_{jl}-\Gamma^k_{jm}\Gamma^m_{il}}_{\footnotesize\text{anti-symmetric in }ij\text{!}},
        $$

        $$
        \begin{aligned}
        \Longrightarrow\quad&R^k{}_{lij}=-R^k{}_{lji}\\
        \Longrightarrow\quad&R^k{}_{lij}=0,\quad\text{if }i=j\\
        \Longrightarrow\quad&\underbrace{R^k{}_{l\phi\theta}}_{\mathclap{\footnotesize 2^2\text{ components!}}}=-R^k{}_{l\theta\phi}\quad\text{can be non-zero!}
        \end{aligned}
        $$

        $$
        R^k{}_{l\phi\theta}=\partial_\phi\Gamma^k_{\theta l}-\partial_\theta\Gamma^k_{\phi l}+\Gamma^k_{\phi m}\Gamma^m_{\theta l}-\Gamma^k_{\theta m}\Gamma^m_{\phi l},
        $$

        $$
        \begin{alignedat}{2}
        &\leadsto\quad(k,l)=(\phi,\phi):\quad&R^\phi{}_{\phi\phi\theta}&=\partial_\phi\underbrace{\Gamma^\phi_{\theta\phi}}_{0}-\partial_\theta\underbrace{\Gamma^\phi_{\phi\phi}}_{0}+\underbrace{\Gamma^\phi_{\phi m}}_{0}\Gamma^m_{\theta\phi}-\Gamma^\phi_{\theta m}\underbrace{\Gamma^m_{\phi\phi}}_{0}=0\\[1.2em]
        &\leadsto\quad(k,l)=(\theta,\theta):\quad&R^\theta{}_{\theta\phi\theta}&=\partial_\phi\underbrace{\Gamma^\theta_{\theta\theta}}_{0}-\underbrace{\partial_\theta\Gamma^\theta_{\phi\theta}}_{0}+\underbrace{\Gamma^\theta_{\phi m}\Gamma^m_{\theta\theta}}_{\substack{\Gamma^\theta_{\phi\theta}\Gamma^\theta_{\theta\theta}\\\mathrlap{\;\;=0}\hphantom{\Gamma^\theta_{\phi\theta}\Gamma^\theta_{\theta\theta}}}}-\underbrace{\Gamma^\theta_{\theta m}\Gamma^m_{\phi\theta}}_{\substack{\Gamma^\theta_{\theta\phi}\Gamma^\phi_{\phi\theta}\\\mathrlap{\;\;=0}\hphantom{\Gamma^\theta_{\theta\phi}\Gamma^\phi_{\phi\theta}}}}=0\\[1.2em]
        &\leadsto\quad(k,l)=(\phi,\theta):\quad&R^\phi{}_{\theta\phi\theta}&=\underbrace{\partial_\phi\Gamma^\phi_{\theta\theta}}_{-(\cos\phi)^2+(\sin\phi)^2}-\partial_\theta\underbrace{\Gamma^\phi_{\phi\theta}}_{0}+\underbrace{\Gamma^\phi_{\phi m}\Gamma^m_{\theta\theta}}_{\substack{\Gamma^\phi_{\phi\phi}\Gamma^\phi_{\theta\theta}\\\mathrlap{\;\;=0}\hphantom{\Gamma^\phi_{\phi\phi}\Gamma^\phi_{\theta\theta}}}}-\underbrace{\Gamma^\phi_{\theta m}\Gamma^m_{\phi\theta}}_{\substack{\Gamma^\phi_{\theta\theta}\Gamma^\theta_{\phi\theta}\\\mathrlap{\;\;=-(\cos\phi)^2}\hphantom{\Gamma^\phi_{\theta\theta}\Gamma^\theta_{\phi\theta}}}}=(\sin\phi)^2\\[1.2em]
        &\leadsto\quad(k,l)=(\theta,\phi):\quad&R^\theta{}_{\phi\phi\theta}&=\underbrace{\partial_\phi\Gamma^\theta_{\theta\phi}}_{-(\sin\phi)^{-2}}-\partial_\theta\underbrace{\Gamma^\theta_{\phi\phi}}_{0}+\underbrace{\Gamma^\theta_{\phi m}\Gamma^m_{\theta\phi}}_{\substack{\Gamma^\theta_{\phi\theta}\Gamma^\theta_{\theta\phi}\\\mathrlap{\;\;=(\cot\phi)^2}\hphantom{\Gamma^\theta_{\phi\theta}\Gamma^\theta_{\theta\phi}}}}-\Gamma^\theta_{\theta m}\underbrace{\Gamma^m_{\phi\phi}}_{0}=-1.
        \end{alignedat}
        $$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: sphere
    # consequence: the curvature of the sphere as a matrix
    lk.prose(
        r"$$\Longrightarrow\quad R^k{}_{l\phi\theta}=-R^k{}_{l\theta\phi}=\mk{\begin{bmatrix}0&(\sin\phi)^2\\-1&0\end{bmatrix}}$$",
    )
    return


if __name__ == "__main__":
    app.run()
