import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 5 · Lorentz factor, photons, relativistic dynamics", css_file="lecturekit/style.css")


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
    return Figure, lk, mo, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(5, "Lorentz factor, photons, relativistic dynamics")
    return


@app.cell(hide_code=True)
def _(Figure, lk, np):
    # Helpers of this lecture: the three figures The two 3D pictures use the coordinates (x^1, x^2, time): inertial
    # particles gamma, sigma and the photon xi are straight lines through p, with the plane u^perp through p and the
    # light cone at p; eta(a, b) = a^1 b^1 + a^2 b^2 - a^0 b^0
    O3 = (0.0, 0.0, 0.0)
    K = "#000000"
    PLUM = "#7d6596"  # nu(gamma, xi): green is nu(gamma, sigma)

    def _eta(a, b):
        return a[0] * b[0] + a[1] * b[1] - a[2] * b[2]

    def _unit(b):  # future timelike unit vector with spatial velocity b
        b = np.asarray(b, float)
        return np.array([*b, 1.0]) / np.sqrt(1 - b @ b)

    _bu, _bv = np.array([0.1, -0.45]), np.array([-0.1, 0.45])  # gamma to the left, sigma to the right
    _n = np.array([np.cos(np.radians(25)), np.sin(np.radians(25))])  # xi forward and a little to the right
    _u, _v = _unit(_bu), _unit(_bv)
    _w = 1.1 * np.array([*_n, 1.0])
    _G = -_eta(_u, _v)  # Lorentz factor
    _nus = _v / _G - _u  # nu(gamma, sigma)
    _nux = _w / (-_eta(_u, _w)) - _u  # nu(gamma, xi)
    # each drawn value checked against its formula; both nu end on their lines
    assert abs(_eta(_u, _u) + 1) < 1e-12 and abs(_eta(_v, _v) + 1) < 1e-12 and abs(_eta(_w, _w)) < 1e-12
    assert abs(_eta(_u, _nus)) < 1e-12 and abs(_eta(_u, _nux)) < 1e-12
    _es, _ex = _u + _nus, _u + _nux
    _t = np.linspace(-0.6, 1.55, 2)
    _H = 1.1  # height of the light cone

    def _gap(a, b):  # a small gap at both ends
        d = (b - a) / np.linalg.norm(b - a)
        return tuple(a + 0.03 * d), tuple(b - 0.03 * d)

    def _line(b, col):
        return (b[0] * _t, b[1] * _t, _t, col, 1.6)

    def _start(b):
        return (b[0] * _t[0], b[1] * _t[0], _t[0])

    def _perp(a, b):  # the point a e_1 + b e_2 + time of u^perp
        return (a, b, (_u[0] * a + _u[1] * b) / _u[2])

    _corners = [_perp(1.0, -1.2), _perp(1.0, 2.2), _perp(-0.7, 2.2), _perp(-0.7, -1.2)]
    _r, _ph = np.meshgrid(np.linspace(0, _H, 10), np.linspace(0, 2 * np.pi, 49), indexing="ij")
    _c = np.linspace(0, 2 * np.pi, 97)

    def decomposition_scene(photon=False):
        # the particles through p, their 4-velocities, the relative velocities from the tip of u, the plane
        # u-perp and the light cone at p
        e = np.array(_corners + [_corners[0]], float)
        surfaces = [lk.patch(_corners, lk.LIGHT, 0.6, n=24)] + [lk.sheet(_r * np.sin(_ph), _r * np.cos(_ph), sg * _r, alpha=0.2) for sg in (1, -1)]
        lines = [(e[:, 0], e[:, 1], e[:, 2], lk.GREY, 1.0), _line(_bu, lk.RED), _line(_bv, lk.BLUE)]
        lines += [(_H * np.sin(_c), _H * np.cos(_c), sg * _H + 0 * _c, lk.GREY, 1.0) for sg in (1, -1)]
        arrows = [(O3, tuple(_u), K), (O3, tuple(_v), K), (*_gap(_u, _es), lk.GREEN)]
        texts = [
            (_start(_bu), r"\gamma", lk.RED, -90, 4),
            (_start(_bv), r"\sigma", lk.BLUE, -90, 4),
            (tuple(0.8 * _u), "u", K, 180, 7),
            (tuple((0.9 if photon else 0.45) * _v), "v", K, 0, 7),
            (O3, "p", K, 165, 9),
            (_corners[1], r"u^\perp", lk.GREY, -60, 8),
            (tuple(_u + 0.5 * _nus), r"\nu(\gamma,\sigma)", lk.GREEN, 90, 6),
        ]
        if photon:
            lines.append(_line(_n, lk.ORANGE))
            arrows += [(O3, tuple(_w), K), (*_gap(_u, _ex), PLUM)]
            texts += [(_start(_n), r"\xi", lk.ORANGE, -90, 4), (tuple(0.55 * _w), "w", K, -30, 7), (tuple(_u + 0.8 * _nux), r"\nu(\gamma,\xi)", PLUM, 60, 7)]
        return lk.turntable(
            -30,
            35,
            ("the particles gamma, sigma and the photon xi through p, the vectors u, v, w, the relative velocities nu(gamma, sigma) and nu(gamma, xi) from the tip of u, the plane u-perp and the light cone at p"
             if photon else
             "the inertial particles gamma and sigma through p, their 4-velocities u and v, the relative velocity nu(gamma, sigma) from the tip of u, the plane u-perp and the light cone at p"),
            [lk.panel(1.0, surfaces=surfaces, lines=lines, arrows=arrows, points=[(O3, K, 3.4)], texts=texts, outlines=[("cone", (0, 0, 0), _H, lk.GREY, 1.0)], box=((-1.15, 1.45), (-1.2, 2.2), (-1.15, 1.6)))],
            height=lk.H3D,
            bias=0.12,
            zoom=1.3,
        )

    def lorentz_figure():
        # the plot: the Lorentz factor against the relative speed, and its Newtonian approximation
        x = np.linspace(0, 0.985, 300)
        fig = Figure(figsize=(3.6, 2.4), layout="constrained")
        ax = fig.subplots()
        ax.plot(x, 1 / np.sqrt(1 - x**2), color=lk.BLUE)
        ax.plot(x, 1 + 0.5 * x**2, "--", color=lk.RED)
        # names at the curve ends, no legend
        ax.text(0.80, 3.45, r"$\Gamma = 1/\sqrt{1-\|\nu\|^2}$", color=lk.BLUE, fontsize=11, ha="right", va="center")
        ax.text(1.0, 1.22, r"$1+\frac{1}{2}\|\nu\|^2$", color=lk.RED, fontsize=11, ha="right", va="top")
        ax.set_xlim(0, 1)
        ax.set_ylim(0.9, 4)
        ax.set_xticks([0, 1])
        ax.set_yticks([1])
        ax.set_xlabel(r"$\|\nu\|$")
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        return fig

    return decomposition_scene, lorentz_figure


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"$\gamma:\mathbb R\longrightarrow\mathbb M^4$, &nbsp; $\gamma'(t)$ timelike future oriented",
        r"> $\leadsto$ &nbsp; $\lVert\gamma'(t)\rVert^2=-1$ &nbsp; (proper-time length parameterization)",
        topic="Particles in Minkowski spacetime",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("Schutz 2.3–2.7; Carroll 1.4, 1.9; Sasane 12.3–12.4")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Lorentz factor
    # definition: 4-velocity, space of simultaneity
    lk.definition(
        r"""
        Given a particle $\gamma:\mathbb R\longrightarrow\mathbb M^4$ we call

        > $u(t)=\gamma'(t)$ &nbsp; the **4-velocity** of $\gamma$ at $\gamma(t)$ &nbsp; (assumed $\lVert u(t)\rVert^2=-1$)

        > $S^{u(t)}_{\gamma(t)}=\gamma(t)+u(t)^\perp$ &nbsp; the **space of simultaneity** of $\gamma$ at $\gamma(t)$
        """,
        label="def-4-velocity",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Lorentz factor
    # theorem: the decomposition of a 4-velocity
    lk.theorem(
        [
            r"Given two particles $\gamma,\sigma$, with &nbsp; $\gamma(t)=\sigma(s)=p$, &nbsp; $\gamma'(t)=u(t)$, &nbsp; $\sigma'(s)=v(s)$",
            r"the 4-velocity of $\sigma$ at $p$ decomposes uniquely as",
            r"$$\begin{aligned}v&=\underbrace{-\eta(u,v)\,u}_{\text{parallel to }u}+\underbrace{\big(v+\eta(u,v)\,u\big)}_{\text{orthogonal to }u}\\[0.4em]&=\underbrace{\Gamma(\gamma,\sigma)}_{\footnotesize\begin{matrix}\text{Lorentz factor}\\\text{of }\sigma\text{ relative }\gamma\end{matrix}}\big(u+\underbrace{\nu(\gamma,\sigma)}_{\footnotesize\begin{matrix}\text{velocity of }\sigma\\\text{relative }\gamma\end{matrix}}\big)\qquad(\text{at }p)\end{aligned}$$",
            r"> $\leadsto$ &nbsp; $\begin{cases}\Gamma(\gamma,\sigma)=-\eta(u,v)>0\\\nu(\gamma,\sigma)=\dfrac{v}{\Gamma(\gamma,\sigma)}-u\in u^\perp\end{cases}$ &nbsp;&nbsp; (at $p$)",
        ],
        label="thm-decomposition",
    )
    return


@app.cell(hide_code=True)
def _(decomposition_scene, lk):
    # module: Lorentz factor
    # example: two inertial particles
    lk.example(
        [
            r"Suppose &nbsp; $\gamma(t)=p+t\,u$, &nbsp; $\sigma(s)=p+s\,v$ &nbsp; are inertial particles (straight lines)",
            r"""
            > Choose &nbsp; $o=p\in\mathbb M^4$ &nbsp; origin event

            > > and &nbsp; $\left.\begin{aligned}e_0&=u\in\mathbb V\\e_i&\in u^\perp\subset\mathbb V\end{aligned}\right\}$ &nbsp; inertial frame

            > $\Longrightarrow$ &nbsp; $\gamma(t)=\begin{bmatrix}t\\0\\0\\0\end{bmatrix}$, &nbsp;&nbsp; $\sigma(s)=\begin{bmatrix}s\,v^0\\s\,v^1\\s\,v^2\\s\,v^3\end{bmatrix}$
            """,
            r"$$\Gamma(\gamma,\sigma)=-\eta(u,v)=-(-1)\,v^0=v^0>0$$",
            lk.aside(
                r"$$\nu(\gamma,\sigma)=\frac{1}{v^0}\begin{bmatrix}v^0\\v^1\\v^2\\v^3\end{bmatrix}-\begin{bmatrix}1\\0\\0\\0\end{bmatrix}=\frac{1}{v^0}\begin{bmatrix}0\\v^1\\v^2\\v^3\end{bmatrix}\in u^\perp$$",
                r"$\nu(\gamma,\sigma)=\dfrac{\text{displacement along }u^\perp}{\text{displacement along }u}$",
            ),
            lk.figure(decomposition_scene()),
        ],
        label="ex-inertial-pair",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Lorentz factor
    # theorem: the relative speed is bounded
    lk.theorem(
        [
            r"For any two particles $\gamma,\sigma$",
            lk.aside(
                r"$$\begin{aligned}\lVert\nu(\gamma,\sigma)\rVert^2&=\frac{\lVert v\rVert^2}{\Gamma(\gamma,\sigma)^2}+2\,\mk{\frac{\Gamma(\gamma,\sigma)}{\Gamma(\gamma,\sigma)}}+\mk{\lVert u\rVert^2}\\[0.3em]&=1+\frac{\lVert v\rVert^2}{\Gamma(\gamma,\sigma)^2}<1\end{aligned}$$",
                r"$\Gamma(\gamma,\sigma)/\Gamma(\gamma,\sigma)=1$, &nbsp; $\lVert u\rVert^2=-1$",
                at=1,
                rows=2,
            ),
        ],
        label="thm-speed-bound",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Lorentz factor
    # consequence: a universal speed limit
    lk.prose(
        lk.aside(
            r"$\leadsto$ &nbsp; speed of $\sigma$ relative to $\gamma$ is <span class='lk-mark'>bounded above</span>!",
            "universal maximum relative speed limit",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Lorentz factor
    # corollary: the Lorentz factor from the relative speed
    lk.corollary(
        [
            r"For any two particles $\gamma,\sigma$",
            r"$$\Gamma(\gamma,\sigma)=\frac{1}{\sqrt{1-\lVert\nu(\gamma,\sigma)\rVert^2}}\geq1\qquad(\text{at }p=\gamma(t)=\sigma(s))$$",
        ],
        label="cor-lorentz-factor",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: photons
    # definition: photon
    lk.definition(
        [
            r"A **photon** in $\mathbb M^4$ is a future oriented lightlike line",
            r"$$\xi(s)=p+s\,w\qquad(\lVert w\rVert^2=0,\ \text{in the future cone})$$",
        ],
        label="def-photon",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: photons
    # theorem: the decomposition for a photon
    lk.theorem(
        [
            r"Given a particle $\gamma$ and a photon $\xi$ &nbsp; $\left(\begin{matrix}p=\gamma(t)=\xi(s)\\\gamma'(t)=u(t)\\\xi'(s)=w(s)\end{matrix}\right)$",
            r"$$\begin{aligned}w&=\underbrace{-\eta(u,w)\,u}_{\text{parallel}}+\underbrace{\big(w+\eta(u,w)\,u\big)}_{\text{orthogonal}}\\[0.4em]&=-\eta(u,w)\big(u+\nu(\gamma,\xi)\big)\end{aligned}$$",
        ],
        label="thm-photon",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: photons
    # corollary: photons move at the maximum speed
    lk.corollary(
        lk.aside(
            r"$$\lVert\nu(\gamma,\xi)\rVert^2=\frac{\mk{\lVert w\rVert^2}}{\eta(u,w)^2}+2\,\mk{\frac{\eta(u,w)}{\eta(u,w)}}+\mk{\lVert u\rVert^2}=1\ !$$",
            r"$\lVert w\rVert^2=0$, &nbsp; $\lVert u\rVert^2=-1$,<br>$\eta(u,w)/\eta(u,w)=1$",
        ),
        label="cor-photon-speed",
    )
    return


@app.cell(hide_code=True)
def _(decomposition_scene, lk):
    # module: photons
    # consequences: photons are the particles of light
    lk.prose(
        r"$\leadsto$ &nbsp; photons achieve the maximum speed relative to any particle!",
        lk.aside(
            r"$\leadsto$ &nbsp; Maxwell's electromagnetic waves evolve along <span class='lk-mark'>photons</span> in Minkowski spacetime!",
            r"photons = particles of light (with $c=1$)",
        ),
        lk.figure(decomposition_scene(photon=True)),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    lk.section("Relativistic dynamics")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: energy and momentum
    # definition: 4-momentum
    lk.definition(
        [
            r"If a particle $\sigma(s)$ has mass $m>0$ its **4-momentum** at $\sigma(s)$ is",
            r"$$P(s)=m\,\sigma'(s)=m\,v(s)$$",
        ],
        label="def-4-momentum",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: energy and momentum
    # energy and spatial momentum relative to another particle
    lk.prose(
        r"Given another particle $\gamma(t)$",
        r"> the 4-momentum of $\sigma$ at an event $\sigma(s)=\gamma(t)$",
        r"$$\begin{aligned}P&=\underbrace{m\,\Gamma(\gamma,\sigma)}_{\footnotesize\begin{matrix}\text{energy of }\sigma\\\text{relative to }\gamma\end{matrix}}u+\underbrace{m\,\Gamma(\gamma,\sigma)\,\nu(\gamma,\sigma)}_{\footnotesize\begin{matrix}\text{spatial momentum}\\\text{of }\sigma\text{ relative to }\gamma\end{matrix}}\\[0.4em]&=\varepsilon(\gamma,\sigma)\,u+\underbrace{\pi(\gamma,\sigma)}_{\in\,u^\perp}\end{aligned}$$",
        r"> > $\Longrightarrow$ &nbsp; $\begin{cases}\varepsilon=-\eta(P,u)\\\pi=P-\varepsilon\,u\end{cases}$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: energy and momentum
    # corollary: energy, mass and momentum
    lk.corollary(
        [
            r"$$\lVert P\rVert^2=m^2\lVert v\rVert^2=\varepsilon(\gamma,\sigma)^2\lVert u\rVert^2+\lVert\pi(\gamma,\sigma)\rVert^2$$",
            lk.aside(
                r"> $\Longrightarrow$ &nbsp; $\varepsilon(\gamma,\sigma)^2=m^2+\lVert\pi(\gamma,\sigma)\rVert^2$",
                r"(energy of $\sigma$ measured by $\gamma$)² =<br>(mass of $\sigma$)² &plus;<br>(spatial momentum of $\sigma$ measured by $\gamma$)²",
            ),
        ],
        label="cor-energy-momentum",
    )
    return


@app.cell(hide_code=True)
def _(lk, lorentz_figure):
    # module: energy and momentum
    # example: small relative speeds
    lk.example(
        [
            r"For small relative speeds &nbsp; $\lVert\nu(\gamma,\sigma)\rVert^2\ll1$",
            lk.aside(
                r"$$\begin{aligned}\varepsilon&=\sqrt{m^2+\lVert\pi\rVert^2}=m\sqrt{1+\frac{\lVert\nu\rVert^2}{1-\lVert\nu\rVert^2}}\approx m+\mk{\tfrac12m\lVert\nu\rVert^2}+O(\lVert\nu\rVert^4)\\[0.3em]\pi&=m\,\Gamma\,\nu=m\frac{\nu}{\sqrt{1-\lVert\nu\rVert^2}}\approx\mk{m\,\nu}+O(\lVert\nu\rVert^3)\end{aligned}$$",
                [(1, r"$\tfrac12m\lVert\nu\rVert^2$: Newtonian limit"), (2, r"$m\,\nu$: Newtonian limit")],
                rows=2,
            ),
            r"$\leadsto$ &nbsp; for $\nu(\gamma,\sigma)=0$ &nbsp; $\Longrightarrow$ &nbsp; $\varepsilon=mc^2$ &nbsp; (with $c=1$)!",
            lk.figure(lorentz_figure()),
        ],
        label="ex-small-speeds",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: force
    # definition: 4-acceleration and 4-force
    lk.definition(
        [
            r"The **4-acceleration** of a particle $\sigma:\mathbb R\longrightarrow\mathbb M^4$ &nbsp; ($\lVert\sigma'(s)\rVert^2=-1$) &nbsp; at $p=\sigma(s)$ is",
            r"$$A(s)=\frac{d}{ds}v(s)=\sigma''(s)$$",
            r"The **4-force** acting on $\sigma$ at $p=\sigma(s)$ is",
            r"$$F(s)=\frac{d}{ds}P(s)=m\,A(s)$$",
        ],
        label="def-4-force",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: force
    # relativistic models
    lk.prose(
        r"$\leadsto$ &nbsp; a relativistic model in $\mathbb M^4$ is the prescription of a 4-force $F(s)=\mathcal F(\sigma(s),\sigma'(s))$<br>along a particle $\sigma:\mathbb R\longrightarrow\mathbb M^4$ for some rule",
        r"$$\mathcal F:\mathbb M^4\times\mathbb V\longrightarrow\mathbb V$$",
        r"e.g. Maxwell: &nbsp; $\mathcal F$ anti-symmetric &plus; Maxwell's equations",
        lk.aside(
            r"> $\displaystyle\begin{aligned}\Longrightarrow\quad\sigma''(s)&=\frac{q}{m}\,\mathcal F(\sigma(s),\sigma'(s))\\[0.3em]&=\frac{q}{m}\,\Gamma(\gamma,\sigma)\Big(\eta\big(E(\gamma),\nu(\gamma,\sigma)\big)\,u\\&\hspace{6em}+E(\gamma)+\nu(\gamma,\sigma)\times B(\gamma)\Big)\end{aligned}$",
            r"with respect to any other particle $\gamma$",
            at="last",
        ),
    )
    return


if __name__ == "__main__":
    app.run()
