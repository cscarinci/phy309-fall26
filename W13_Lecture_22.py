import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 22 · Tidal forces and curvature", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import sys

    import marimo as mo

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)
    import numpy as np

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return lk, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(22, "Tidal forces and curvature")
    return


@app.cell(hide_code=True)
def _(lk, np):
    # The sphere of the recap (radius drawn as 2): the loop gamma at p (on the equator) along the equator, up a meridian,
    # back along a circle of latitude and down a meridian to p (red); Z parallel transported along it, computed from the
    # Christoffel symbols of the round metric: green along the two geodesic sides, orange along the circle of latitude and
    # the last meridian, ending in P(Z) at p; the coordinate vectors d_theta and -d_phi at p (black).
    def _transport(path, z):
        """Z^phi, Z^theta parallel along the coordinate path [(phi, theta), ...] (midpoint steps)."""
        out = [np.array(z, float)]
        for (f0, t0), (f1, t1) in zip(path, path[1:]):
            f, df, dt = (f0 + f1) / 2, f1 - f0, t1 - t0
            zf, zt = out[-1]

            def rhs(zf, zt):
                # dZ^k = -Gamma^k_ij dx^i Z^j, with Gamma^phi_tt = -sin cos, Gamma^theta_pt = Gamma^theta_tp = cot
                return np.array([np.sin(f) * np.cos(f) * dt * zt, -(np.cos(f) / np.sin(f)) * (df * zt + dt * zf)])

            k = rhs(zf, zt)
            out.append(out[-1] + rhs(zf + k[0] / 2, zt + k[1] / 2))
        return out

    def _point(f, t):
        return 2 * np.array([np.sin(f) * np.cos(t), np.sin(f) * np.sin(t), np.cos(f)])

    def _vec(f, t, z, length=0.8):
        dphi = np.array([np.cos(f) * np.cos(t), np.cos(f) * np.sin(t), -np.sin(f)])
        dtheta = np.array([-np.sin(f) * np.sin(t), np.sin(f) * np.cos(t), 0.0])
        v = z[0] * dphi + z[1] * dtheta
        return _point(f, t), _point(f, t) + length * v / np.linalg.norm(v)

    _ta, _tb, _f1, _n = -0.6, 0.6, np.pi / 2 - 0.6, 120
    _sides = [
        [(np.pi / 2, t) for t in np.linspace(_ta, _tb, _n)],
        [(f, _tb) for f in np.linspace(np.pi / 2, _f1, _n)],
        [(_f1, t) for t in np.linspace(_tb, _ta, _n)],
        [(f, _ta) for f in np.linspace(_f1, np.pi / 2, _n)],
    ]
    _path = [q for k, s in enumerate(_sides) for q in (s if k == 0 else s[1:])]
    _z = _transport(_path, [-np.sin(np.pi / 12), np.cos(np.pi / 12)])
    _green = [0, _n // 2, _n - 1, _n - 1 + _n // 2]
    _orange = [2 * _n - 2, 2 * _n - 2 + _n // 2, 3 * _n - 3]
    _arrows = [(*_vec(*_path[k], _z[k]), lk.GREEN, 1.8) for k in _green]
    _arrows += [(*_vec(*_path[k], _z[k]), lk.ORANGE, 1.8) for k in _orange + [len(_path) - 1]]
    _p = _point(np.pi / 2, _ta)
    _arrows += [(*_vec(np.pi / 2, _ta, [0, 1], 0.6), "#000000", 1.6), (*_vec(np.pi / 2, _ta, [-1, 0], 0.6), "#000000", 1.6)]
    _loop = np.array([_point(*q) for q in _path])
    # the direction of the loop: a head in the middle of each side
    _heads = [(_loop[m - 8 : m + 9, 0], _loop[m - 8 : m + 9, 1], _loop[m - 8 : m + 9, 2], lk.RED, 2.4) for m in (_n // 2 + k * (_n - 1) for k in range(4))]
    _s, _t = np.meshgrid(np.linspace(0, np.pi, 25), np.linspace(0, 2 * np.pi, 97), indexing="ij")
    _T = np.linspace(0, 2 * np.pi, 181)
    _tips = {
        "Z": _vec(np.pi / 2, _ta, _z[0])[1],
        "PZ": _vec(np.pi / 2, _ta, _z[-1])[1],
        "dt": _vec(np.pi / 2, _ta, [0, 1], 0.6)[1],
        "df": _vec(np.pi / 2, _ta, [-1, 0], 0.6)[1],
    }
    parallel_loop = lk.turntable(
        0,
        12,
        "the sphere with a loop at p on the equator: along the equator, up a meridian, back along a circle of latitude and down a meridian; the vector Z parallel transported around it comes back as P(Z), turned",
        [
            lk.panel(
                1.0,
                surfaces=[lk.sheet(2 * np.sin(_s) * np.cos(_t), 2 * np.sin(_s) * np.sin(_t), 2 * np.cos(_s), wire=[(0, 4, lk.BLUE, 0.4), (1, 8, lk.BLUE, 0.4)], alpha=0.85)],
                lines=[
                    (2 * np.cos(_T), 2 * np.sin(_T), 0 * _T, lk.GREY, 1.0, [4, 3]),
                    (_loop[:, 0], _loop[:, 1], _loop[:, 2], lk.RED, 2.4),
                ],
                arrows=_arrows,
                arcs=_heads,
                points=[(tuple(_p), lk.RED)],
                texts=[
                    (tuple(_p), "p", lk.RED, -150, 10),
                    (tuple(_tips["Z"]), "Z", lk.GREEN, -10, 8),
                    (tuple(_tips["PZ"]), "P(Z)", lk.ORANGE, 20, 8),
                    (tuple(_tips["dt"]), r"\partial_\theta", "#000000", -60, 8),
                    (tuple(_tips["df"]), r"-\partial_\phi", "#000000", 170, 8),
                ],
                box=((-1.8, 1.8), (-1.8, 1.8), (-1.8, 1.8)),
            )
        ],
        height=lk.H3D,
    )
    return (parallel_loop,)


@app.cell(hide_code=True)
def _(lk, parallel_loop):
    # module: recap
    # recap
    lk.recap(
        r"Riemann curvature tensor on $(M,g)$",
        lk.under(
        r"""
        $\mathrm{Riem}\in\Gamma(TM^1_3)$

        $$
        \mathrm{Riem}(X,Y)\,Z=\nabla_X(\nabla_YZ)-\nabla_Y(\nabla_XZ)-\nabla_{[X,Y]}Z
        $$
        """,
        r"""<span class="lk-vconn"><span>$\varphi$</span><span class="lk-vconn-arrow">$\leadsto$</span></span>""",
        lk.aside(
            r"""
            $$
            \begin{aligned}
            R^k{}_{lij}\,X^iY^jZ^l&=\big(\mathrm{Riem}(\partial_i,\partial_j)\,\partial_l\big)^k\,X^iY^jZ^l\\
            &=\big(\mk{\partial_i\Gamma^k_{jl}}-\mk{\partial_j\Gamma^k_{il}}+\Gamma^k_{im}\Gamma^m_{jl}-\Gamma^k_{jm}\Gamma^m_{il}\big)\,X^iY^jZ^l
            \end{aligned}
            $$
            """,
            r"2nd derivatives of $g$",
            at="last",
        ),
        r"$\nabla:\Gamma(TM)\times\Gamma(TM)\longrightarrow\Gamma(TM)$ (Levi-Civita connection)",
        lk.aside(
            r"$$\nabla_XY\overset{\varphi}{\leadsto}X^i\big(\partial_iY^k+\mk{\Gamma^k_{ij}}\,Y^j\big)$$",
            r"1st derivatives of $g$:<br>$\displaystyle(\nabla_{\partial_i}\partial_j)^k=\tfrac12g^{kl}(\partial_ig_{lj}+\partial_jg_{il}-\partial_lg_{ij})$",
        ),
        ),
        r"$(\mathbb S^2,g_{\mathbb S^2})$",
        lk.under(
            lk.aside(
                r"$$g_{\mathbb S^2}\overset{\psi}{=}d\phi\,d\phi+(\sin\phi)^2\,d\theta\,d\theta\quad\leadsto\quad g_{ij}=\mk{\begin{bmatrix}1&0\\0&(\sin\phi)^2\end{bmatrix}}$$",
                r"bilinear form, entries $\begin{bmatrix}\phi\phi&\phi\theta\\\theta\phi&\theta\theta\end{bmatrix}$",
            ),
            r"""
            $$
            g^{-1}_{\mathbb S^2}\overset{\psi}{=}\partial_\phi\partial_\phi+\frac{1}{(\sin\phi)^2}\,\partial_\theta\partial_\theta\quad\leadsto\quad g^{ij}=\begin{bmatrix}1&0\\0&(\sin\phi)^{-2}\end{bmatrix}
            $$

            $$
            \Longrightarrow\quad\Gamma^\phi_{ij}=\begin{bmatrix}0&0\\0&-\sin\phi\cos\phi\end{bmatrix},\qquad\Gamma^\theta_{ij}=\begin{bmatrix}0&\cot\phi\\\cot\phi&0\end{bmatrix}
            $$
            """,
            lk.aside(
                r"$$\Longrightarrow\quad\underbrace{R^k{}_{l\phi\theta}}_{\mathclap{\footnotesize\mathrm{Riem}(\partial_\phi,\partial_\theta):\Gamma(TM)\to\Gamma(TM)}}=-R^k{}_{l\theta\phi}=\mk{\begin{bmatrix}0&(\sin\phi)^2\\-1&0\end{bmatrix}}$$",
                r"linear transformation, entries $\begin{bmatrix}\phi\phi&\phi\theta\\\theta\phi&\theta\theta\end{bmatrix}$",
            ),
            r"""
            $\leadsto$ &nbsp; parallel transport of $Z_p$ around a parallelogram $\gamma$ with “sides” $\varepsilon X_p$, $\delta Y_p$

            $$
            P^\gamma(Z_p)-Z_p=-\varepsilon\delta\,\mathrm{Riem}(X_p,Y_p)\,Z_p+\dots
            $$

            $$
            -\mathrm{Riem}(\partial_\theta,\partial_\phi)\,Z=(\sin\phi)^2Z^\theta\,\partial_\phi-Z^\phi\,\partial_\theta=\frac{P^\gamma(Z)-Z}{\varepsilon\delta}
            $$
            """,
            lk.figure(parallel_loop),
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(
        r"""
        Tidal forces

        $\leadsto$ &nbsp; curvature as the source of gravitation
        """,
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Newtonian gravity
    # lead-in: Newtonian gravity
    lk.prose(
        r"""
        Newtonian gravity in $\mathbb G^4$:

        > source $\sigma(t)$ of mass $M$

        > free-falling particle $\gamma(t)$ of mass $m$

        > $\Longrightarrow$ &nbsp; $\displaystyle\cancel{m}\,\gamma''(t)=-M\cancel{m}\,\frac{\gamma(t)-\sigma(t)}{\lVert\gamma(t)-\sigma(t)\rVert^3}=F(\gamma(t))$

        > > $\leadsto$ &nbsp; same acceleration for every free-falling particle!

        """,
        lk.aside(
            r"Choose an inertial chart with &nbsp; $\sigma(t)=o+t\,e_0$, &nbsp; $\gamma(t)=o+t\,e_0+\mk{x^i(t)}\,e_i$",
            r"$i=1,2,3$",
        ),
        lk.aside(
            r"""
            > $\Longrightarrow$ &nbsp; $\left\lbrace
            \begin{aligned}
            \ddot t&=0\\
            \ddot x^i(t)&=-M\,\frac{x^i(t)}{\lVert x(t)\rVert^3}=-\big(\mk{\nabla}\Phi(x(t))\big)^i
            \end{aligned}
            \right.$
            """,
            r"$\nabla$ = gradient in $\mathbb R^3$",
        ),
        r"""
        with $\displaystyle\Phi(x)=-\frac{M}{\lVert x\rVert}$ the gravitational potential

        $\leadsto$ &nbsp; can this be a geodesic equation?
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Newtonian gravity
    # argument: Newton as a geodesic equation
    lk.prose(
        r"On $(M,g)$, the geodesic equation (in a chart) is",
        lk.aside(
            r"$$\mk{\ddot x^\mu}+\Gamma^\mu_{\nu\rho}\,\dot x^\nu\dot x^\rho=0$$",
            r"$\mu=0,1,2,3$",
        ),
        r"""
        $$
        \leadsto\quad
        \left\lbrace
        \begin{aligned}
        \ddot t+\Gamma^t_{tt}\,\dot t\,\dot t+2\Gamma^t_{ti}\,\dot t\,\dot x^i+\Gamma^t_{ij}\,\dot x^i\dot x^j&=0\\
        \ddot x^i+\Gamma^i_{tt}\,\dot t\,\dot t+2\Gamma^i_{tj}\,\dot t\,\dot x^j+\Gamma^i_{jk}\,\dot x^j\dot x^k&=0
        \end{aligned}
        \right.
        $$

        is equivalent to Newton's iff &nbsp; $\Gamma^t_{\mu\nu}=0=\Gamma^i_{tj}=\Gamma^i_{jt}=\Gamma^i_{jk}$, &nbsp; $\Gamma^i_{tt}=\nabla^i\Phi$

        $\Longrightarrow$ &nbsp; non-zero curvature components:

        $$
        \boxed{\,R^i{}_{tjt}=-R^i{}_{ttj}=\nabla^i\partial_j\Phi\,}
        $$
        """,
        lk.aside(
            r"$\Longrightarrow$ &nbsp; the curvature tensor encodes the matrix of <span class='lk-mark'>2nd derivatives</span> of the gravitational potential!",
            r"Hessian matrix of $\Phi$",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tidal effects
    # argument: two neighbouring free-falling particles
    lk.prose(
        r"Consider two neighboring free-falling particles",
        lk.aside(
            r"""
            $$
            \left.
            \begin{aligned}
            \gamma_1(t)&=(t,x_1(t))\\
            \gamma_2(t)&=(t,x_2(t))
            \end{aligned}
            \right\rbrace\quad\mk{\delta(t)}=x_2(t)-x_1(t)
            $$
            """,
            r"$\delta(t)$ = coordinate displacement<br>vector at time $t$",
        ),
        lk.aside(
            r"""
            $$
            \begin{aligned}
            \Longrightarrow\quad\ddot\delta^i=\ddot x_2^i-\ddot x_1^i&=-\nabla^i\Phi(x_1+\delta)+\nabla^i\Phi(x_1)\\
            &\approx-\nabla^i\partial_j\Phi(x_1)\,\delta^j\approx-R^i{}_{tjt}\,\delta^j
            \end{aligned}
            $$
            """,
            r"relative acceleration depends on<br>displacement direction via curvature",
            at="last",
        ),
        r"""
        > $\leadsto$ &nbsp; tidal effects!
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tidal effects
    # remark: weak fields
    lk.remark(
        r"""
        This derivation is only approximately correct

        > $\leadsto$ &nbsp; accurate for “weak” gravitational fields
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tidal effects
    # theorem: geodesic deviation equation
    lk.theorem(
        r"""
        On any $(M,g)$, given neighboring geodesics &nbsp; $\gamma_1(t)\overset{\varphi}{=}\varphi^{-1}(x_1^\mu(t)\,e_\mu)$, &nbsp; $\gamma_2(t)\overset{\varphi}{=}\varphi^{-1}(x_2^\mu(t)\,e_\mu)$

        > $\Longrightarrow$ &nbsp; $\delta(t)\overset{\varphi}{=}\big(x_2^\mu(t)-x_1^\mu(t)\big)\,\partial_\mu|_{\gamma_1(t)}$ is a vector field along $\gamma_1$

        > <span class="lk-ghost">$\Longrightarrow$ &nbsp;</span>and

        $$
        \Big(\frac{D}{dt}\frac{D}{dt}\delta\Big)^\mu=-R^\mu{}_{\nu\rho\sigma}\,\dot x_1^\nu\,\delta^\rho\,\dot x_1^\sigma
        $$
        """,
        title="geodesic deviation equation",
        label="thm-deviation",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Poisson
    # lead-in: matter is the source of gravity
    lk.prose(
        r"For Newton: matter is the source of gravity",
        lk.aside(
            r"""
            $$
            \begin{aligned}
            \leadsto\quad\text{point source:}\quad\Phi(x)&=-\frac{M}{\lVert x\rVert}\\
            \leadsto\quad\text{extended source:}\quad\Phi(x)&=-\int_{\mathbb R^3}\frac{\mk{\rho(y)}}{\lVert x-y\rVert}\,dV(y)
            \end{aligned}
            $$
            """,
            r"$\rho$ = mass density",
            at="last",
        ),
        r"""
        $$
        \begin{aligned}
        \Longrightarrow\quad&\underbrace{\int_{\partial V}\nabla\Phi\cdot dA}_{\mathllap{\footnotesize\begin{array}{c}\text{flux of gravitational field}\\\text{through a surface}\end{array}\kern-1.2em}}=4\pi\underbrace{\int_V\rho\,dV}_{\mathrlap{\kern-1.2em\footnotesize\begin{array}{c}\text{mass in the region}\\\text{bounded by the surface}\end{array}}}\qquad(\text{gravitational Gauss' law!})\\[1.6em]
        \Longrightarrow\quad&\Delta\Phi(x)=4\pi\rho\qquad(\text{Poisson equation})
        \end{aligned}
        $$
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Poisson
    # computation: Poisson in terms of curvature
    lk.prose(
        r"In terms of curvature",
        lk.aside(
            r"""
            $$
            \begin{aligned}
            4\pi\rho=\Delta\Phi&=\mk{\nabla}\cdot\nabla\Phi\\
            &=\nabla^i\partial_i\Phi=\mk{R^i{}_{tit}}
            \end{aligned}
            $$
            """,
            [(1, r"$\nabla\cdot$ = divergence"), (2, r"sum over $i$")],
            rows=2,
        ),
    )
    return


if __name__ == "__main__":
    app.run()
