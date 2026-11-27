import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 20 · Geodesics of Schwarzschild spacetime", css_file="lecturekit/style.css")


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
    lk.lecture(20, "Geodesics of Schwarzschild spacetime")
    return


@app.cell(hide_code=True)
def _(Figure, lk, np):
    # Helpers of this lecture: the two 3D scenes and the three orbit drawings

    def _cylinder(r0, lo, hi):
        u, h = np.meshgrid(np.linspace(0, 2 * np.pi, 61), np.linspace(lo, hi, 9))
        # (see-through, outlined), with its two boundary circles and its waist marked
        return lk.sheet(r0 * np.cos(u), r0 * np.sin(u), h, wire=[(0, 4, lk.BLUE, 1.2)], alpha=0.3, tone=lk.BLUE)

    def schwarzschild_scene():
        # M = R x (r_0, oo) x S^2 seen in the slice phi = pi/2: t upwards, the equatorial plane across; the cylinder
        # r = r_0 is left out of M; the circle of radius r_0 at t = 0 is the equator S^1 in S^2
        r0 = 1.0
        u = np.linspace(0, 2 * np.pi, 121)
        return lk.turntable(
            -60,
            20,
            "the spacetime M outside the cylinder r = r_0, with t upwards and the equator S^1 of S^2 as a circle around it",
            [
                lk.panel(
                    1.0,
                    surfaces=[_cylinder(r0, -1.5, 1.5)],
                    outlines=[("cylinder", (0, 0), r0, (-1.5, 1.5), lk.BLUE, 1.2)],
                    lines=[(r0 * np.cos(u), r0 * np.sin(u), 0 * u, lk.GREEN, 2.2)],
                    axes=[((0, 0, -1.5), (0, 0, 1.8), "t", 90), ((0, 0, 0), (2.4, 0, 0), "r", 0)],
                    points=[((r0, 0, 0), "#000000")],
                    texts=[
                        ((r0, 0, 0), r"r_0", "#000000", -60, 8),
                        ((r0 * np.cos(-1.9), r0 * np.sin(-1.9), 0), r"\mathbb S^1\subset\mathbb S^2", lk.GREEN, -120, 10),
                        ((2.0, 0, 1.2), r"M", "#000000", 0, 0),
                    ],
                    box=((-1.2, 2.4), (-1.2, 1.2), (-1.5, 1.8)),
                )
            ],
            height=lk.H3D,
        )

    def newton_scene():
        # Galilean spacetime with tau upwards: the source of radius r_0 sweeps a cylinder around the history
        # sigma(tau) of its center of mass; a particle passing by follows a hyperbola (M = 1, e = 1.15, p = 2.3),
        # its history gamma(tau) (red) bends around the cylinder; at one point the force F(gamma(tau)) pulls
        # towards sigma(tau)
        r0, e, p = 0.5, 1.15, 2.3
        th = np.linspace(-1.3, 1.3, 400)
        r = p / (1 + e * np.cos(th))
        tau = np.concatenate([[0], np.cumsum(r[1:] ** 2 * np.diff(th))]) / np.sqrt(p)
        tau = 2.1 * (tau - tau.mean()) / (tau.max() - tau.min())
        x, y = -r * np.sin(th), r * np.cos(th)  # closest to the source along the r-axis
        k = 250
        pt = np.array([x[k], y[k], tau[k]])
        to_axis = -pt[:2] / np.linalg.norm(pt[:2])
        tip = pt + 0.5 * np.array([*to_axis, 0])
        return lk.turntable(
            0,
            20,
            "a particle's history bending around the history of a spherical source, the force pulling it towards the source's center",
            [
                lk.panel(
                    1.0,
                    surfaces=[_cylinder(r0, -1.05, 1.05)],
                    outlines=[("cylinder", (0, 0), r0, (-1.05, 1.05), lk.BLUE, 1.2)],
                    lines=[(x, y, tau, lk.RED, 2.2)],
                    axes=[((0, 0, -1.05), (0, 0, 1.35), r"\tau", 90)],
                    arrows=[(tuple(pt), tuple(tip), lk.GREEN, 2.0)],
                    points=[(tuple(pt), lk.RED)],
                    texts=[
                        (tuple(pt), r"\gamma(\tau)", lk.RED, 0, 8),
                        (tuple(tip), r"F(\gamma(\tau))", lk.GREEN, 150, 8),
                        ((0, 0, -1.05), r"\sigma(\tau)=o+\tau e_0", "#000000", -125, 24),
                    ],
                    box=((-1.2, 1.2), (-0.7, 1.4), (-1.05, 1.2)),
                )
            ],
            height=420,
        )

    from matplotlib.patches import Circle as matplotlib_circle

    def _plane(xlim, ylim, width):
        fig = Figure(figsize=(width, width * (ylim[1] - ylim[0]) / (xlim[1] - xlim[0])))
        ax = fig.add_axes((0, 0, 1, 1))
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        lk.arrow(ax, (xlim[0] + 0.1, 0), (xlim[1] - 0.15, 0), "#000000", lw=1.1)
        lk.arrow(ax, (0, ylim[0] + 0.1), (0, ylim[1] - 0.15), "#000000", lw=1.1)
        ax.text(xlim[1] - 0.15, -0.1, "$x$", fontsize=13, ha="right", va="top")
        ax.text(0.1, ylim[1] - 0.2, "$y$", fontsize=13, va="top")
        # the source: a hatched disc at the origin
        ax.add_patch(matplotlib_circle((0, 0), 0.2, fill=False, hatch="////", ec="#000000", lw=1.2))
        return fig, ax

    def _radius(ax, r, th):
        # the segment r(theta) from the origin and the angle theta from the x-axis
        ax.plot([0, r * np.cos(th)], [0, r * np.sin(th)], color="#000000", lw=1.1)
        a = np.linspace(0, th, 30)
        ax.plot(0.32 * np.cos(a), 0.32 * np.sin(a), color="#000000", lw=1.0)
        ax.text(0.45 * np.cos(th / 2), 0.45 * np.sin(th / 2), r"$\theta$", fontsize=12, ha="center", va="center")
        n = np.array([np.sin(th), -np.cos(th)])  # the normal on the clockwise side of the segment
        ax.text(*(0.6 * r * np.array([np.cos(th), np.sin(th)]) - 0.12 * n), r"$r(\theta)$", fontsize=12, ha="right", va="top")

    def _heads(ax, x, y, ks, color):
        for k in ks:
            if 0 <= k < len(x) - 2:
                lk.arrow(ax, (x[k], y[k]), (x[k + 2], y[k + 2]), color, lw=1.4)

    def newton_orbit(e):
        # r = p / (1 + e cos theta), p = 1.2, the source at the focus: an ellipse, parabola or hyperbola by e
        fig, ax = _plane((-2.8, 2.8), (-2.8, 2.8), 3.6)
        th = np.linspace(-np.pi, np.pi, 1200)
        den = 1 + e * np.cos(th)
        r = np.where(den > 1e-6, 1.2 / np.maximum(den, 1e-6), np.inf)
        x, y = r * np.cos(th), r * np.sin(th)
        x[(r > 6) | ~np.isfinite(r)] = np.nan
        ax.plot(x, y, color=lk.BLUE, lw=1.6)
        _heads(ax, x, y, (380, 800), lk.BLUE)
        _radius(ax, 1.2 / (1 + e * np.cos(1.9)), 1.9)
        return fig

    def precessing_orbit(m):
        # r = p / (1 + e cos((1 - 3 m^2) theta)), p = 1.2, e = 0.5, m = M/L: five turns
        fig, ax = _plane((-2.8, 2.8), (-2.8, 2.8), 3.6)
        k = 1 - 3 * m**2
        th = np.linspace(0, 10 * np.pi, 3000)
        r = 1.2 / (1 + 0.5 * np.cos(k * th))
        ax.plot(r * np.cos(th), r * np.sin(th), color=lk.BLUE, lw=1.4)
        _heads(ax, r * np.cos(th), r * np.sin(th), (300, 1650), lk.BLUE)
        _radius(ax, 1.2 / (1 + 0.5 * np.cos(k * 1.9)), 1.9)
        return fig

    def light_rays(m):
        # light passing the source, m = ME/L, L/E = 1: the bent ray r = 1 / (sin theta + m (1 + cos(theta)^2)) (blue)
        # and, touching it at its closest point on the y-axis, the ray for M = 0 (grey); where the bent ray
        # crosses the x-axis, its angles with it (about 2ME/L)
        fig, ax = _plane((-3.6, 3.6), (-1.7, 1.5), 4.6)
        top = 1 / (1 + m)
        ax.plot([-3.4, 3.4], [top, top], color=lk.GREY, lw=1.6)
        lk.arrow(ax, (-1.9, top), (-1.6, top), lk.GREY, lw=1.6)
        lk.arrow(ax, (1.6, top), (1.9, top), lk.GREY, lw=1.6)
        ax.text(3.45, top, "$M=0$", color=lk.GREY, fontsize=12, va="center")
        th = np.linspace(-0.9, np.pi + 0.9, 4000)
        den = np.sin(th) + m * (1 + np.cos(th) ** 2)
        r = np.where(den > 1e-4, 1 / np.maximum(den, 1e-4), np.nan)
        x, y = r * np.cos(th), r * np.sin(th)
        keep = np.isfinite(r) & (np.abs(x) < 3.4) & (y > -1.6)
        x, y = x[keep][::-1], y[keep][::-1]  # from left to right
        ax.plot(x, y, color=lk.BLUE, lw=1.6)
        for xa in (-1.3, 1.3):
            j = np.argmin(np.abs(x - xa))
            lk.arrow(ax, (x[j - 3], y[j - 3]), (x[j], y[j]), lk.BLUE, lw=1.6)
        j = np.argmin(np.abs(x - 3.1))
        ax.text(x[j] - 0.1, y[j] - 0.12, "$M>0$", color=lk.BLUE, fontsize=12, ha="right", va="top")
        ax.plot([0.12, 0.12], [0.2, top], color=lk.ORANGE, lw=1.6, ls=(0, (1.5, 2)))  # beside the y-axis
        ax.text(-0.08, 0.5 * (0.2 + top), "$L/E$", color=lk.ORANGE, fontsize=12, ha="right", va="center")
        # the angles where the ray crosses the x-axis, when that is in the drawing
        xc = 1 / (2 * m)
        if xc < 3.0:
            for s in (-1, 1):
                j = np.argmin(np.abs(x - s * xc) + 10 * np.abs(y))
                slope = np.arctan2(y[j + 5] - y[j - 5], x[j + 5] - x[j - 5])  # direction of travel
                if s > 0:
                    a = np.linspace(slope, 0, 20)
                    label, ha, at = r"$-\frac{2ME}{L}$", "left", (s * xc + 0.45, 0.28)
                else:
                    a = np.linspace(np.pi, np.pi + slope, 20)
                    label, ha, at = r"$\frac{2ME}{L}$", "right", (s * xc - 0.45, 0.28)
                ax.plot(s * xc + 0.5 * np.cos(a), 0.5 * np.sin(a), color="#000000", lw=1.0)
                ax.text(*at, label, fontsize=16, ha=ha, va="center")
        return fig

    return light_rays, newton_orbit, newton_scene, precessing_orbit, schwarzschild_scene


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    e_s = lk.slider(0.0, 1.6, step=0.05, value=0.5, label="$e$")
    ml_s = lk.slider(0.0, 0.2, step=0.01, value=0.12, label="$M/L$")
    me_s = lk.slider(0.05, 0.4, step=0.01, value=0.25, label="$ME/L$")
    return e_s, me_s, ml_s


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"""
        $$
        \begin{aligned}
        \nabla:\Gamma(TM)\times\Gamma(TM)&\longrightarrow\Gamma(TM)\\
        (X,Y)&\longmapsto\nabla_XY\overset{\varphi}{=}X^i\,(\partial_iY^k+\Gamma^k_{ij}\,Y^j)\,\partial_k
        \end{aligned}
        $$
        """,
        lk.aside(
            r"• compatibility with &nbsp; $g\overset{\varphi}{=}g_{ij}\,dx^i\mk{dx^j}$",
            r"simplifying conventions<br>⇝ dropping “$\otimes$” symbols",
        ),
        r"""
        $$
        \begin{aligned}
        X\big(g(Y,Z)\big)&=g(\nabla_XY,Z)+g(Y,\nabla_XZ)\\
        \overset{\varphi}{\Longleftrightarrow}\quad\partial_ig_{jk}&=\Gamma^l_{ij}\,g_{lk}+\Gamma^l_{ik}\,g_{jl}.
        \end{aligned}
        $$

        • torsion free

        $$
        \begin{aligned}
        (\nabla_XY-\nabla_YX)\,f&=[X,Y]\,f=X(Y(f))-Y(X(f))\\
        \overset{\varphi}{\Longleftrightarrow}\quad\Gamma^k_{ij}&=\Gamma^k_{ji}.
        \end{aligned}
        $$

        $\Longrightarrow$ &nbsp; $\Gamma^k_{ij}={\large\tfrac12}\,g^{kl}\,(\partial_ig_{lj}+\partial_jg_{il}-\partial_lg_{ij})$

        Given a path $\gamma(t)\overset{\varphi}{=}\varphi^{-1}(x^i(t)\,e_i)$

        $$
        \begin{aligned}
        \leadsto\quad\frac{D}{dt}X_{\gamma(t)}&=\nabla_{\gamma'(t)}X\qquad\text{(covariant derivative)}\\
        &\overset{\varphi}{=}\big(\dot X^k(t)+\Gamma^k_{ij}(t)\,\dot x^i(t)\,X^j(t)\big)\,\partial_k|_{\gamma(t)}\\[0.5em]
        \leadsto\quad A(t)&=\frac{D}{dt}\gamma'(t)\qquad\text{(acceleration of }\gamma\text{)}\\
        &\overset{\varphi}{=}\big(\ddot x^k(t)+\Gamma^k_{ij}(t)\,\dot x^i(t)\,\dot x^j(t)\big)\,\partial_k|_{\gamma(t)}.
        \end{aligned}
        $$

        Geodesics on $(M,g)$ = paths with zero acceleration

        $$
        \frac{D}{dt}\gamma'(t)=0\quad\overset{\varphi}{\Longleftrightarrow}\quad\ddot x^k(t)+\Gamma^k_{ij}(t)\,\dot x^i(t)\,\dot x^j(t)=0,\quad\forall\,k=1,\dots,m.
        $$
        """,
        topic="Levi-Civita connection and geodesics",
    )
    return


@app.cell(hide_code=True)
def _(lk, schwarzschild_scene):
    # module: Schwarzschild geodesics
    # example: Schwarzschild spacetime in the equatorial plane
    lk.example(
        [
            r"""
            $M=\mathbb R\times(r_0,+\infty)\times\mathbb S^2$, &nbsp; $\Psi(t,r,p)=(t,r,\phi,\theta)$
            """,
            lk.aside(r"For simplicity: &nbsp; <span class='lk-mark'>$\phi=\pi/2$</span>", r"the equator in $\mathbb S^2$"),
            lk.figure(schwarzschild_scene()),
            r"""
            $$
            \begin{aligned}
            g_{\mathrm{Sch}}&\overset{\Psi}{=}-\Big(1-\frac{2M}{r}\Big)\,dt\,dt+\frac{dr\,dr}{\big(1-\frac{2M}{r}\big)}+r^2\,d\theta\,d\theta\\
            g^{-1}_{\mathrm{Sch}}&\overset{\Psi}{=}-\frac{\partial_t\partial_t}{\big(1-\frac{2M}{r}\big)}+\Big(1-\frac{2M}{r}\Big)\,\partial_r\partial_r+\frac{1}{r^2}\,\partial_\theta\partial_\theta
            \end{aligned}
            $$
            """,
            lk.aside(
                r"""$$
                \begin{aligned}
                \overset{\Psi}{\Longrightarrow}\quad\Gamma^t_{tr}&=\Gamma^t_{rt}=\frac{M}{r^2}\Big(1-\frac{2M}{r}\Big)^{-1}&\Gamma^r_{tt}&=\frac{M}{r^2}\Big(1-\frac{2M}{r}\Big)\\
                \Gamma^\theta_{r\theta}&=\Gamma^\theta_{\theta r}=\frac1r&\Gamma^r_{rr}&=-\frac{M}{r^2}\Big(1-\frac{2M}{r}\Big)^{-1}\\
                &&\Gamma^r_{\theta\theta}&=-r\Big(1-\frac{2M}{r}\Big)
                \end{aligned}
                $$""",
                "only non-zero<br>Christoffel symbols!",
            ),
        ],
        title="Schwarzschild geodesics",
        label="ex-sch",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Schwarzschild geodesics
    # consequence: the geodesic equations and their first integrals
    lk.prose(
        r"""
        Geodesic $\gamma(\tau)\overset{\Psi}{=}\Psi^{-1}\big(t(\tau),r(\tau),\theta(\tau)\big)$

        $$
        \leadsto\quad\left\lbrace\begin{aligned}
        &\ddot t+\frac{2M}{r^2}\Big(1-\frac{2M}{r}\Big)^{-1}\dot t\,\dot r=0\\
        &\ddot\theta+\frac2r\,\dot r\,\dot\theta=0\\
        &\ddot r+\frac{M}{r^2}\Big(1-\frac{2M}{r}\Big)\dot t^2-\frac{M}{r^2}\Big(1-\frac{2M}{r}\Big)^{-1}\dot r^2-r\Big(1-\frac{2M}{r}\Big)\dot\theta^2=0
        \end{aligned}\right.
        $$

        $$
        \Longrightarrow\quad\left\lbrace\begin{aligned}
        &\frac{d}{d\tau}\Big(\Big(1-\frac{2M}{r}\Big)\dot t\Big)=0\\&\qquad\leadsto\quad\frac{d}{d\tau}\big(\underbrace{-g(\partial_t,\gamma'(\tau))}_{E}\big)=0\\
        &\frac{d}{d\tau}\big(r^2\dot\theta\big)=0\\&\qquad\leadsto\quad\frac{d}{d\tau}\big(\underbrace{g(\partial_\theta,\gamma'(\tau))}_{L}\big)=0\\
        &\frac{d}{d\tau}\Big(-\Big(1-\frac{2M}{r}\Big)\dot t^2+\Big(1-\frac{2M}{r}\Big)^{-1}\dot r^2+r^2\dot\theta^2\Big)=0\\
        &\qquad\leadsto\quad\frac{d}{d\tau}\big(\underbrace{g(\gamma'(\tau),\gamma'(\tau))}_{\kappa}\big)=0
        \end{aligned}\right.
        $$
        """,
        lk.aside(
            r"""$$
            \Longrightarrow\quad\left\lbrace\begin{aligned}
            \dot t&=\frac{E}{1-\frac{2M}{r}}\\
            \dot\theta&=\frac{L}{r^2}\\
            (\dot r)^2&=E^2-\Big(1-\frac{2M}{r}\Big)\Big(\frac{L^2}{r^2}-\kappa\Big)\\
            &=E^2-1+\frac{2M}{r}-\frac{L^2}{r^2}+\frac{2ML^2}{r^3}
            \end{aligned}\right.
            $$""",
            r"$\kappa=-1$ &nbsp;$\leadsto$&nbsp; timelike geodesic<br><span class='lk-ghost'>$\kappa=-1$ &nbsp;$\leadsto$&nbsp;</span>= free-falling particle",
            at="last",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk, newton_scene):
    # module: Newtonian orbits
    # lead-in: Newtonian orbits
    lk.prose(
        r"""
        Compare with Newtonian orbits (in Galilean spacetime)

        > $\leadsto$ &nbsp; spherically symmetric inertial source of radius $r_0$ and mass $M$

        > $\leadsto$ &nbsp; $\sigma(\tau)$ history of its center of mass

        > $\leadsto$ &nbsp; $\gamma(\tau)$ particle of mass $m$

        > $\Longrightarrow$ &nbsp; $\displaystyle m\,\gamma''(\tau)=-Mm\,\frac{\gamma(\tau)-\sigma(\tau)}{\|\gamma(\tau)-\sigma(\tau)\|^3}=F(\gamma(\tau))$
        """,
        lk.figure(newton_scene()),
        r"$\gamma(\tau)=(\tau,r(\tau),\theta(\tau))$",
        lk.aside(
            r"""$$
            \Longrightarrow\quad\left\lbrace\begin{aligned}
            \dot\tau&=1\\
            \dot\theta&=\frac{\mk{L}}{r^2}\\
            (\dot r)^2&=2\mk{\mathcal E}+\frac{2M}{r}-\frac{L^2}{r^2}
            \end{aligned}\right.
            $$""",
            [(2, r"$L$ = angular momentum"), (3, r"$\mathcal E$ = energy")],
            rows=3,
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Newtonian orbits
    # remark: conservation of energy and angular momentum
    lk.remark(
        r"""
        The two final equations are just conservation of energy and angular momentum

        $$
        \begin{aligned}
        \text{Newton:}\quad&L=r^2\dot\theta,\quad\mathcal E=\underbrace{\tfrac12\big((\dot r)^2+r^2\dot\theta^2\big)}_{\footnotesize\text{kinetic}}\underbrace{-\frac{M}{r}}_{\mathclap{\footnotesize\text{potential}}}\\[0.6em]
        \text{Schwarzschild:}\quad&L=r^2\dot\theta,\quad\underbrace{\frac{E^2-1}{2}}_{=\,\mathcal E}=\tfrac12\big((\dot r)^2+r^2\dot\theta^2\big)-\frac{M}{r}\underbrace{-\frac{ML^2}{r^3}}_{\footnotesize\begin{matrix}\text{relativistic}\\\text{correction}\end{matrix}}.
        \end{aligned}
        $$

        > $\leadsto$ &nbsp; geodesics of $g_{\mathrm{Sch}}$ follow Newton's orbits with one relativistic correction!
        """
    )
    return


@app.cell(hide_code=True)
def _(e_s, lk, newton_orbit):
    # module: orbits
    # orbit equation, Newton
    lk.prose(
        r"""
        Orbit equation: &nbsp; $r=r(\theta)$

        > $\Longrightarrow$ &nbsp; $\displaystyle\dot r=\frac{dr}{d\theta}\,\dot\theta=\frac{dr}{d\theta}\,\frac{L}{r^2}$

        $$
        \begin{aligned}
        \text{Newton:}\quad&\frac{L^2}{r^4}\Big(\frac{dr}{d\theta}\Big)^2=2\mathcal E+\frac{2M}{r}-\frac{L^2}{r^2}\\
        \Longrightarrow\quad&r(\theta)=\frac{L^2/M}{1+e\cos(\theta-\theta_0)},\qquad e^2=1+\frac{2\mathcal EL^2}{M^2}\\
        &\leadsto\quad\begin{cases}\text{ellipse},&\text{if }0<e<1,\\\text{parabola},&\text{if }e=1,\\\text{hyperbola},&\text{if }e>1\end{cases}
        \end{aligned}
        $$
        """,
        lk.interactive(newton_orbit(e_s.value), controls=[e_s]),
    )
    return


@app.cell(hide_code=True)
def _(lk, ml_s, precessing_orbit):
    # module: orbits
    # orbit equation, Schwarzschild: perihelion precession
    lk.prose(
        r"""
        $$
        \begin{aligned}
        \text{Schwarzschild:}\quad&\frac{L^2}{r^4}\Big(\frac{dr}{d\theta}\Big)^2=\underbrace{E^2-1}_{2\mathcal E}+\frac{2M}{r}-\frac{L^2}{r^2}+\underbrace{\frac{2ML^2}{r^3}}_{\footnotesize\begin{matrix}\text{relativistic}\\\text{correction}\end{matrix}}\\
        \Longrightarrow\quad&r(\theta)\approx\frac{L^2/M}{1+e\cos\big(\theta-\theta_0-\frac{3M^2}{L^2}\theta\big)},\qquad\text{for }2M\ll r(\theta)\\
        &\leadsto\quad\begin{cases}\text{“ellipses” with precessing major and minor axes},&\text{if }0<e<1,\\\text{open orbits},&\text{if }e\geq1\end{cases}
        \end{aligned}
        $$
        """,
        lk.interactive(precessing_orbit(ml_s.value), controls=[ml_s]),
        lk.aside(r"$\leadsto$ &nbsp; for each cycle, the axes rotate by &nbsp; $\mk{\Delta\theta\approx6\pi\,\dfrac{M^2}{L^2}}$", "perihelion precession"),
    )
    return


@app.cell(hide_code=True)
def _(light_rays, lk, me_s):
    # module: orbits
    # lightlike orbits: bending of light
    lk.prose(
        r"""
        Lightlike orbits:

        $$
        \frac{L^2}{r^4}\Big(\frac{dr}{d\theta}\Big)^2=E^2-\frac{L^2}{r^2}+\frac{2ML^2}{r^3}\qquad(\kappa=0),
        $$
        """,
        lk.aside(
            r"$$\Longrightarrow\quad\mk{r(\theta)\approx\frac{L/E}{\sin(\theta)+\frac{ME}{L}\big(1+\cos(\theta)^2\big)}},\qquad\text{for }M\ll r(\theta),$$",
            r"for $M=0$, $r(\theta)={\large\tfrac{L/E}{\sin(\theta)}}$<br>is a straight line",
        ),
        r"""
        $$
        \leadsto\quad r\to+\infty\quad\Longleftrightarrow\quad\theta\approx-\frac{2ME}{L}\quad\text{or}\quad\theta\approx\pi+\frac{2ME}{L}.
        $$
        """,
        lk.interactive(light_rays(me_s.value), controls=[me_s]),
        r"$\leadsto$ &nbsp; light rays bend towards the star by an angle &nbsp; $\alpha\approx{\large\tfrac{4ME}{L}}$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: orbits
    # remark: first tests of GR
    lk.remark(
        f"""
        The {lk.gloss("explanation", "1915")} of Mercury's perihelion precession

        and the {lk.gloss("observation", "1919")} of light bending by the Sun were the first experimental tests of GR!
        """
    )
    return


if __name__ == "__main__":
    app.run()
