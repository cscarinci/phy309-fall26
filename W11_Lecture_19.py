import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 19 · Connections on manifolds", css_file="lecturekit/style.css")


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
    return lk, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(19, "Connections on manifolds")
    return


@app.cell(hide_code=True)
def _(lk, np):
    # Helpers of this lecture: the two sphere scenes (unit sphere, x, y, z axes, view 30/18)

    AZ, EL = 30, 18
    BOX = ((-0.82, 0.82), (-0.82, 0.82), (-0.82, 0.82))
    AXES = [((0, 0, 0), (1.4, 0, 0), "x", 208), ((0, 0, 0), (0, 1.4, 0), "y", -8), ((0, 0, 0), (0, 0, 1.4), "z", 90)]

    def _screen(v):
        # the direction (degrees, 0 = right, 90 = up) of the vector v on the screen of the first view
        a, e = np.radians(AZ), np.radians(EL)
        right = np.array([-np.sin(a), np.cos(a), 0.0])
        up = np.array([-np.sin(e) * np.cos(a), -np.sin(e) * np.sin(a), np.cos(e)])
        return float(np.degrees(np.arctan2(v @ up, v @ right)))

    def _sphere():
        s, t = np.meshgrid(np.linspace(0, np.pi, 25), np.linspace(0, 2 * np.pi, 97), indexing="ij")
        return lk.sheet(np.sin(s) * np.cos(t), np.sin(s) * np.sin(t), np.cos(s), alpha=0.45)  # smooth, outlined

    def latitude_scene(f0):
        # the latitude gamma(t) = (phi_0, t), an integral curve of d_theta, and its acceleration
        # A = nabla_{d_theta} d_theta = -sin(phi_0) cos(phi_0) d_phi (zero at the equator)
        th = np.radians(AZ + 25)  # the point shown: on the front of the sphere
        s = np.linspace(0, 2 * np.pi, 181)
        p = np.array([np.sin(f0) * np.cos(th), np.sin(f0) * np.sin(th), np.cos(f0)])
        dphi = np.array([np.cos(f0) * np.cos(th), np.cos(f0) * np.sin(th), -np.sin(f0)])
        v = np.sin(f0) * np.array([-np.sin(th), np.cos(th), 0.0])
        A = -np.sin(f0) * np.cos(f0) * dphi
        zero = abs(np.cos(f0)) < 0.01
        arrows = [(tuple(p), tuple(p + v), lk.ORANGE, 1.8)]
        texts = [(tuple(p + v), r"\gamma'(t)", lk.ORANGE, _screen(v), 8)]
        if zero:
            texts.append((tuple(p), r"A_{\gamma(t)}=0", lk.RED, -60, 10))
        else:
            arrows.append((tuple(p), tuple(p + A), lk.RED, 2.2))
            texts.append((tuple(p + A), r"A_{\gamma(t)}", lk.RED, _screen(A), 12))
        return lk.turntable(
            AZ,
            EL,
            "the latitude of the sphere at the chosen phi_0, the point gamma(t) on it, its velocity gamma'(t) along the latitude, and its acceleration, tangent to the sphere along the meridian",
            [
                lk.panel(
                    1.0,
                    surfaces=[_sphere()],
                    outlines=[("sphere", (0, 0, 0), 1.0, lk.GREY, 1.0)],
                    lines=[(np.sin(f0) * np.cos(s), np.sin(f0) * np.sin(s), np.cos(f0) + 0 * s, lk.BLUE, 2.2)],
                    points=[((0, 0, 0), "#000000", 2.6), (tuple(p), "#000000")],
                    axes=AXES,
                    arrows=arrows,
                    texts=texts,
                    box=BOX,
                )
            ],
            height=460,
            key="L19-latitude",
            apart=True,
        )

    def great_circle_scene(L, t):
        # the geodesic for kappa = 1 and angular momentum L: the great circle in the plane through the origin
        # spanned by u and v (outlined as a square), the point gamma(t) and its velocity gamma'(t) (length 1)
        th0 = np.radians(AZ + 120)  # theta_0 of the plane: never edge-on in the first view
        w = np.sqrt(max(1 - L * L, 0.0))
        u = np.array([-np.sin(th0), np.cos(th0), 0.0])
        v = np.array([L * np.cos(th0), L * np.sin(th0), w])

        def at(s):
            s = np.asarray(s, float)
            return -np.cos(s)[..., None] * u + np.sin(s)[..., None] * v

        g, dg = at(t), np.sin(t) * u + np.cos(t) * v
        circle = at(np.linspace(0, 2 * np.pi, 241))
        S = 1.1
        corners = [S * (a * u + b * v) for a, b in [(-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)]]
        edge = np.concatenate([corners[k] + np.linspace(0, 1, 40, endpoint=False)[:, None] * (corners[k + 1] - corners[k]) for k in range(4)] + [corners[0][None, :]])
        return lk.turntable(
            AZ,
            EL,
            "the geodesics of the sphere: for kappa = 1 and the chosen L, a great circle, the plane through the origin that contains it, and the point gamma(t) with the velocity gamma'(t), of length 1",
            [
                lk.panel(
                    1.0,
                    surfaces=[_sphere()],
                    outlines=[("sphere", (0, 0, 0), 1.0, lk.GREY, 1.0)],
                    lines=[(*edge.T, lk.GREY, 1.2), (*circle.T, lk.BLUE, 2.2)],
                    points=[((0, 0, 0), "#000000", 2.6), (tuple(g), "#000000")],
                    axes=AXES,
                    arrows=[(tuple(g), tuple(g + dg), lk.ORANGE, 1.8)],
                    texts=[
                        (tuple(g + dg), r"\gamma'(t)", lk.ORANGE, _screen(dg), 8),
                        (tuple(g), r"\gamma(t)", "#000000", _screen(-g), 10),
                    ],
                    box=BOX,
                )
            ],
            height=460,
            key="L19-geodesics",
            apart=True,
        )

    return great_circle_scene, latitude_scene


@app.cell(hide_code=True)
def _(lk, np):
    # Controls of the interactive figures. They are shown inside their figures, so modules can be moved freely.
    # phi_0 in steps of pi/36; L from 0 to 1 (kappa = 1); t from 0 to 2 pi
    phi0_s = lk.slider(steps=[round(float(k * np.pi / 36), 2) for k in range(3, 34)], value=0.79, label=r"$\phi_0$", show_value=False)
    L_s = lk.slider(0, 1, step=0.05, value=0.6, label="$L$", show_value=False)
    t_s = lk.slider(0, round(2 * np.pi, 2), step=0.04, value=1.0, label="$t$", show_value=False)
    return L_s, phi0_s, t_s


@app.cell(hide_code=True)
def _(latitude_scene, phi0_s):
    # the scene of the latitude figure, in place by its slider
    latitude_scene(phi0_s.value)
    return


@app.cell(hide_code=True)
def _(L_s, great_circle_scene, t_s):
    # the scene of the great circle figure, in place by its sliders
    great_circle_scene(round(L_s.value, 2), round(t_s.value, 2))
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"""
        $\gamma(t)\overset{\varphi}{=}\varphi^{-1}\big(x^k(t)\,e_k\big)\overset{\tilde\varphi}{=}\tilde\varphi^{-1}\big(\tilde x^l(t)\,e_l\big)$

        $X_{\gamma(t)}\overset{\varphi}{=}X^k(t)\,\partial_k|_{\gamma(t)}\overset{\tilde\varphi}{=}\tilde X^l(t)\,\tilde\partial_l|_{\gamma(t)}$

        > $\displaystyle\begin{aligned}\leadsto\quad\frac{D}{dt}X_{\gamma(t)}&\overset{\varphi}{=}\big(\dot X^k(t)+\dot x^i(t)\,X^j(t)\,\Gamma^k_{ij}(t)\big)\,\partial_k|_{\gamma(t)}\\&\overset{\tilde\varphi}{=}\big(\dot{\tilde X}{}^l(t)+\dot{\tilde x}{}^m(t)\,\tilde X^n(t)\,\tilde\Gamma^l_{mn}(t)\big)\,\tilde\partial_l|_{\gamma(t)}\end{aligned}$

        > $\displaystyle\begin{alignedat}{2}\Longleftrightarrow\quad\tilde x&=\tilde\varphi\circ\varphi^{-1}(x)&\qquad\dot{\tilde x}{}^l&=\frac{\partial\tilde x^l}{\partial x^k}\,\dot x^k\\[0.4em]\tilde X^l&=\frac{\partial\tilde x^l}{\partial x^k}\,X^k&\dot{\tilde X}{}^l&=\frac{\partial\tilde x^l}{\partial x^k}\,\dot X^k+\underbrace{\frac{\partial^2\tilde x^l}{\partial x^i\partial x^j}\,X^i\dot x^j}_{\footnotesize\text{non-tensorial}}\\[0.4em]\tilde\partial_l&=\frac{\partial x^k}{\partial\tilde x^l}\,\partial_k&\Gamma^k_{ij}&=\frac{\partial x^k}{\partial\tilde x^l}\,\tilde\Gamma^l_{mn}\,\frac{\partial\tilde x^m}{\partial x^i}\,\frac{\partial\tilde x^n}{\partial x^j}+\underbrace{\frac{\partial x^k}{\partial\tilde x^l}\,\frac{\partial^2\tilde x^l}{\partial x^i\partial x^j}}_{\footnotesize\text{non-tensorial}}\end{alignedat}$

        > $\Longrightarrow$ &nbsp; Christoffel symbols are not components of tensors on $M$.
        """,
        topic="Covariant derivatives on manifolds",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals("Connections on manifolds", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("Schutz 5.4, 6.3–6.4; Carroll 3.2–3.4; Sasane 6.1–6.4, 7.1–7.2, 8.1–8.3")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: connections
    # definition: connection
    lk.definition(
        [
            r"A **connection** on $M$ is an operator",
            lk.aside(
                r"""$$
                \begin{aligned}
                \nabla:\Gamma(TM)\times\Gamma(TM)&\longrightarrow\Gamma(TM)\\
                (X,Y)&\longmapsto\mk{\nabla_XY},
                \end{aligned}
                $$""",
                r"derivative of $Y$<br>in the direction of $X$",
            ),
            r"satisfying:",
            lk.aside(
                r"> i) &nbsp; $\nabla_{fX+gY}Z=f\,\nabla_XZ+g\,\nabla_YZ$ &nbsp; $\forall\,X,Y,Z\in\Gamma(TM)$, &nbsp; $\forall\,f,g\in C^\infty(M,\mathbb R)$",
                r"$C^\infty(M,\mathbb R)$-linearity",
            ),
            lk.aside(
                r"> ii) &nbsp; $\nabla_X(aY+bZ)=a\,\nabla_XY+b\,\nabla_XZ$ &nbsp; $\forall\,X,Y,Z\in\Gamma(TM)$, &nbsp; $\forall\,a,b\in\mathbb R$",
                r"$\mathbb R$-linearity",
            ),
            lk.aside(
                r"> iii) &nbsp; $\nabla_X(fY)=X(f)\,Y+f\,\nabla_XY$ &nbsp; $\forall\,X,Y\in\Gamma(TM)$, &nbsp; $\forall\,f\in C^\infty(M,\mathbb R)$",
                r"Leibniz rule",
            ),
        ],
        label="def-connection",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: connections
    # consequence: Christoffel symbols of a connection
    lk.prose(
        r"""
        $X\overset{\varphi}{=}X^i\,\partial_i$, &nbsp; $Y\overset{\varphi}{=}Y^j\,\partial_j$

        > $\displaystyle\begin{aligned}\Longrightarrow\quad\nabla_XY&\overset{\varphi}{=}(\nabla_XY)^k\,\partial_k=\nabla_{X^i\partial_i}(Y^j\,\partial_j)=X^i\,\nabla_{\partial_i}(Y^j\,\partial_j)\\&=(X^i\,\partial_iY^j)\,\partial_j+X^iY^j\,\nabla_{\partial_i}\partial_j\end{aligned}$
        """,
        lk.aside(
            r"> $\Longrightarrow$ &nbsp; $\nabla_{\partial_i}\partial_j=\mk{\Gamma^k_{ij}\,\partial_k}$",
            r"$C^\infty(M,\mathbb R)$-linear combination<br>of coordinate basis vector fields",
        ),
        r"""
        Under a change of charts &nbsp; $\partial_i={\large\tfrac{\partial\tilde x^k}{\partial x^i}}\,\tilde\partial_k$

        > $\displaystyle\begin{alignedat}{2}\Longrightarrow\quad&\nabla_{\partial_i}\partial_j=\nabla_{\frac{\partial\tilde x^k}{\partial x^i}\tilde\partial_k}\Big(\frac{\partial\tilde x^l}{\partial x^j}\,\tilde\partial_l\Big)\\\Longrightarrow\quad&\Gamma^k_{ij}=\frac{\partial x^k}{\partial\tilde x^l}\,\tilde\Gamma^l_{mn}\,\frac{\partial\tilde x^m}{\partial x^i}\,\frac{\partial\tilde x^n}{\partial x^j}+\frac{\partial x^k}{\partial\tilde x^l}\,\frac{\partial^2\tilde x^l}{\partial x^i\partial x^j}\end{alignedat}$

        > > $\leadsto$ &nbsp; Christoffel symbols are components of connections on manifolds!
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: connections
    # remark: covariant derivatives along paths
    lk.remark(
        r"""
        Connections define covariant derivatives along paths

        > For $X\in\Gamma(TM)$ along a path $\gamma(t)$: &nbsp; ${\large\tfrac{D}{dt}}X_{\gamma(t)}=\nabla_{\gamma'(t)}X$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Levi-Civita connection
    # theorem: Levi-Civita connection
    lk.theorem(
        [
            r"""
            Given a metric field $g\in\Gamma(TM^0_2)$, there exists<br>a unique connection $\nabla:\Gamma(TM)\times\Gamma(TM)\longrightarrow\Gamma(TM)$ such that
            """,
            lk.aside(r"> • &nbsp; $X\big(g(Y,Z)\big)=g(\nabla_XY,Z)+g(Y,\nabla_XZ)$", r"$\nabla$ is “compatible with $g$”"),
            lk.aside(r"> • &nbsp; $(\nabla_XY-\nabla_YX)\,f=X(Y(f))-Y(X(f))$", r"$\nabla$ is “torsion-free”"),
            r"> $\forall\,X,Y,Z\in\Gamma(TM)$, &nbsp; $\forall\,f\in C^\infty(M,\mathbb R)$",
        ],
        title="Levi-Civita connection",
        label="thm-levi-civita",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Levi-Civita connection
    # proof
    lk.proof(
        r"""
        In a chart, take $X=\partial_i$, $Y=\partial_j$, $Z=\partial_k$

        > • &nbsp; $\partial_ig_{jk}=g(\Gamma^l_{ij}\,\partial_l,\partial_k)+g(\partial_j,\Gamma^l_{ik}\,\partial_l)=g_{lk}\,\Gamma^l_{ij}+g_{jl}\,\Gamma^l_{ik}$

        > > $\leadsto$ &nbsp; $(i,j,k)+(j,i,k)-(k,i,j)$ &nbsp; $\times\,g^{kl}$

        > • &nbsp; $(\Gamma^k_{ij}-\Gamma^k_{ji})\,\partial_kf=\partial_i(\partial_jf)-\partial_j(\partial_if)=0$ &nbsp; $\Longleftrightarrow$ &nbsp; $\Gamma^k_{ij}=\Gamma^k_{ji}$

        > > $\Longrightarrow$ &nbsp; $\Gamma^k_{ij}={\large\tfrac12}\,g^{kl}\,(\partial_ig_{lj}+\partial_jg_{il}-\partial_lg_{ij})$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Levi-Civita connection
    # after the proof: what it shows
    lk.prose(r"$\leadsto$ &nbsp; this proves uniqueness; existence: this $\Gamma$ satisfies both properties")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Levi-Civita connection
    # example: the sphere
    lk.example(
        r"""
        $M=\mathbb S^2$, &nbsp; $g_{\mathbb S^2}\overset{\psi}{=}d\phi\otimes d\phi+(\sin\phi)^2\,d\theta\otimes d\theta=\begin{bmatrix}1&0\\0&(\sin\phi)^2\end{bmatrix}$

        <span class="lk-ghost">$M=\mathbb S^2$, &nbsp; </span>$g^{-1}_{\mathbb S^2}\overset{\psi}{=}\partial_\phi\otimes\partial_\phi+(\sin\phi)^{-2}\,\partial_\theta\otimes\partial_\theta=\begin{bmatrix}1&0\\0&(\sin\phi)^{-2}\end{bmatrix}$

        <span class="lk-ghost">$M=\mathbb S^2$, &nbsp; </span>$\Longrightarrow$ &nbsp; $\Gamma^\phi_{ij}={\large\tfrac12}\,g^{\phi\phi}(\partial_ig_{\phi j}+\partial_jg_{i\phi}-\partial_\phi g_{ij})=\begin{bmatrix}0&0\\0&-\sin\phi\cos\phi\end{bmatrix}$

        <span class="lk-ghost">$M=\mathbb S^2$, &nbsp; </span>$\Longrightarrow$ &nbsp; $\Gamma^\theta_{ij}={\large\tfrac12}\,g^{\theta\theta}(\partial_ig_{\theta j}+\partial_jg_{i\theta}-\partial_\theta g_{ij})=\begin{bmatrix}0&\cot\phi\\\cot\phi&0\end{bmatrix}$

        <span class="lk-ghost">$M=\mathbb S^2$, &nbsp; </span>$\leadsto$ &nbsp; $\nabla_{\partial_\phi}\partial_\phi=0$, &nbsp; $\nabla_{\partial_\theta}\partial_\theta=-\sin\phi\cos\phi\,\partial_\phi$, &nbsp; $\nabla_{\partial_\phi}\partial_\theta=\nabla_{\partial_\theta}\partial_\phi=\cot\phi\,\partial_\theta$
        """,
        label="ex-sphere-christoffel",
    )
    return


@app.cell(hide_code=True)
def _(lk, phi0_s):
    # module: geodesics
    # definition: acceleration, geodesic
    lk.module(
        lk.definition(
            [
                r"Given a path $\gamma$ on $M$, its **acceleration** is the vector field along $\gamma$ given by",
                lk.aside(
                    r"""$$
                    \begin{aligned}
                    A_{\gamma(t)}&=\frac{D}{dt}\gamma'(t)=\mk{\nabla_{\gamma'(t)}X}\\
                    &\overset{\varphi}{=}\big(\ddot x^k(t)+\dot x^i(t)\,\dot x^j(t)\,\Gamma^k_{ij}(t)\big)\,\partial_k|_{\gamma(t)}.
                    \end{aligned}
                    $$""",
                    [(1, r"where $\gamma$ is an integral<br>curve of $X\in\Gamma(TM)$")],
                    rows=2,
                ),
                r"A **geodesic** is a path with zero acceleration",
                lk.aside(
                    r"$$\frac{D}{dt}\gamma'(t)=0\quad\overset{\varphi}{\Longleftrightarrow}\quad\mk{\ddot x^k+\dot x^i\dot x^j\,\Gamma^k_{ij}=0\quad\forall\,k}.$$",
                    r"non-linear 2nd order<br>system of ODEs",
                ),
            ],
            label="def-geodesic",
        ),
        lk.prose(lk.interactive(lk.frame("L19-latitude", 460), controls=[phi0_s])),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: geodesics
    # comment: geodesics as a family of paths
    lk.prose(
        lk.aside(
            r"$\leadsto$ &nbsp; they form a special family of paths on Riemannian / <span class='lk-mark'>Lorentzian</span> manifolds",
            r"particles / photons<br>(if timelike / lightlike)",
        )
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: geodesics
    # theorem: g(γ', γ') is constant along a geodesic
    lk.theorem(
        r"""
        If $\gamma$ is a geodesic then

        $$
        g_{\gamma(t)}\big(\gamma'(t),\gamma'(t)\big)=\text{constant along }\gamma.
        $$
        """,
        label="thm-geodesic-speed",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: geodesics
    # proof
    lk.proof(
        r"""
        For any $X_{\gamma(t)}$, $Y_{\gamma(t)}$ vector fields along $\gamma(t)$

        > $g_{\gamma(t)}(X_{\gamma(t)},Y_{\gamma(t)})\overset{\varphi}{=}g_{ij}(t)\,X^i(t)\,Y^j(t)$

        > > $\displaystyle\begin{alignedat}{2}\Longrightarrow\quad&\frac{d}{dt}\big(g_{\gamma(t)}(X_{\gamma(t)},Y_{\gamma(t)})\big)&&\overset{\varphi}{=}\partial_kg_{ij}\,X^iY^j\dot x^k+g_{ij}\dot X^iY^j+g_{ij}X^i\dot Y^j\\&&&=g_{ij}(\dot X^i+\Gamma^i_{kl}\dot x^kX^l)\,Y^j+g_{ij}X^i(\dot Y^j+\Gamma^j_{kl}\dot x^kY^l)\\&&&=g_{\gamma(t)}\Big(\frac{D}{dt}X_{\gamma(t)},Y_{\gamma(t)}\Big)+g_{\gamma(t)}\Big(X_{\gamma(t)},\frac{D}{dt}Y_{\gamma(t)}\Big)\end{alignedat}$

        > > $\Longrightarrow$ &nbsp; $\displaystyle \frac{d}{dt}\,g_{\gamma(t)}(\gamma'(t),\gamma'(t))=2\,g_{\gamma(t)}\Big(\frac{D}{dt}\gamma'(t),\gamma'(t)\Big)=0$
        """
    )
    return


@app.cell(hide_code=True)
def _(L_s, lk, t_s):
    # module: geodesics
    # example: geodesics of the sphere
    lk.example(
        [
            r"$M=\mathbb S^2$, &nbsp; $\gamma(t)\overset{\psi}{=}(\phi(t),\theta(t))$ geodesic",
            lk.aside(
                r"> $\displaystyle\begin{aligned}\Longleftrightarrow\quad&\begin{cases}\ddot\theta+\Gamma^\theta_{ij}\,\dot x^i\dot x^j=0\\\ddot\phi+\Gamma^\phi_{ij}\,\dot x^i\dot x^j=0\end{cases}\quad\Longleftrightarrow\quad\begin{cases}\ddot\theta+2\cot\phi\,\dot\phi\,\dot\theta=0\\\ddot\phi-\sin\phi\cos\phi\,(\dot\theta)^2=0\end{cases}\\[0.6em]\Longleftrightarrow\quad&\begin{cases}\dfrac{d}{dt}\big(\dot\theta\,(\sin\phi)^2\big)=0&\leadsto\quad\dot\theta\,(\sin\phi)^2=L\\[0.8em]\dfrac{d}{dt}\Big(\dot\phi^2+\dfrac{L^2}{(\sin\phi)^2}\Big)=0&\leadsto\quad\dot\phi^2+\dfrac{L^2}{(\sin\phi)^2}=\mk{\kappa}\end{cases}\end{aligned}$",
                r"$\kappa=g_{\mathbb S^2}(\gamma',\gamma')$",
                at="last",
            ),
            r"""
            Note &nbsp; $\gamma'(t)=(\dot\phi(t),\dot\theta(t))$

            > $\Longrightarrow$ &nbsp; $g_{\mathbb S^2}(\gamma',\gamma')=\dot\phi^2+(\sin\phi)^2\,\dot\theta^2=\kappa$

            For $L=0$ &nbsp; $\Longrightarrow$ &nbsp; $\theta=\theta_0$, &nbsp; $\phi=\sqrt\kappa\,t+\phi_0$ &nbsp; (meridians)
            """,
            lk.aside(
                r"For $L\neq0$ &nbsp; $\Longrightarrow$ &nbsp; $\mk{\cot\phi={\large\tfrac{\sqrt{\kappa-L^2}}{L}}\cos(\theta-\theta_0)}$",
                "implicit solution",
            ),
            lk.aside(
                r"<span class='lk-ghost'>For $L\neq0$ &nbsp; </span>$\Longleftrightarrow$ &nbsp; $\mk{z={\large\tfrac{\sqrt{\kappa-L^2}}{L}}\big(\cos\theta_0\,x+\sin\theta_0\,y\big)}$",
                "plane through the origin",
            ),
            r"$\therefore$ &nbsp; the geodesics on $(\mathbb S^2,g_{\mathbb S^2})$ are the great circles of $\mathbb S^2$.",
            lk.interactive(lk.frame("L19-geodesics", 460), controls=[L_s, t_s]),
        ],
        label="ex-sphere-geodesics",
    )
    return


if __name__ == "__main__":
    app.run()
