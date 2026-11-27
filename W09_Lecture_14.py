import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 14 · Metrics", css_file="lecturekit/style.css")


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
    lk.lecture(14, "Metrics")
    return


@app.cell(hide_code=True)
def _(lk, math, mo, np):
    # Helpers of this lecture: the three figures

    def _name(x, y, tex, colour="#000", anchor="start"):
        return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" fill="{colour}" font-family="KaTeX_Math" font-style="italic" font-size="19">{tex}</text>'

    _sub = '<tspan font-family="KaTeX_Main" font-style="normal" font-size="13" dy="4">{}</tspan>'

    def plane_figure():
        # the point p in both charts of the plane
        B, G, O = lk.BLUE, lk.GREY, lk.ORANGE
        return mo.Html(f"""
        <svg viewBox="0 0 400 250" style="display: block; margin: 0 auto; width: 400px; max-width: 100%;" role="img"
             aria-label="the plane with origin o, the orthonormal vectors e1 and e2 along the axes, and a point p, at x and y along the axes, at distance r from o and at angle theta from the first axis">
          <line x1="25" y1="200" x2="372" y2="200" stroke="#000" stroke-width="1.1"/><polygon points="380,200 370,196 370,204" fill="#000"/>
          <line x1="70" y1="238" x2="70" y2="22" stroke="#000" stroke-width="1.1"/><polygon points="70,14 66,24 74,24" fill="#000"/>
          <line x1="245" y1="62" x2="245" y2="200" stroke="{G}" stroke-width="1.2" stroke-dasharray="5 4"/>
          <line x1="245" y1="62" x2="70" y2="62" stroke="{G}" stroke-width="1.2" stroke-dasharray="5 4"/>
          <path d="M 112 200 A 42 42 0 0 0 103.0 173.9" fill="none" stroke="{G}" stroke-width="1.2"/>
          <line x1="70" y1="200" x2="239.5" y2="66.4" stroke="{B}" stroke-width="2"/><polygon points="245,62 233.5,65.9 238.4,72.2" fill="{B}"/>
          <line x1="70" y1="200" x2="136" y2="200" stroke="{O}" stroke-width="2"/><polygon points="146,200 135,195.5 135,204.5" fill="{O}"/>
          <line x1="70" y1="200" x2="70" y2="134" stroke="{O}" stroke-width="2"/><polygon points="70,124 65.5,135 74.5,135" fill="{O}"/>
          <circle cx="245" cy="62" r="4" fill="#000"/><circle cx="70" cy="200" r="3.6" fill="#000"/>
          {_name(52, 222, "o")}
          {_name(122, 226, "e" + _sub.format(1), O)}
          {_name(42, 150, "e" + _sub.format(2), O)}
          {_name(240, 224, "x")}
          {_name(48, 68, "y")}
          {_name(254, 56, "p")}
          {_name(140, 112, "r", B)}
          {_name(120, 188, "θ")}
        </svg>
        """)

    def polar_figure(r):
        # the coordinate vectors of the polar chart at p, for theta fixed and r chosen by the slider
        B, G, O = lk.BLUE, lk.GREY, lk.ORANGE
        U, TH, OX, OY = 70, math.radians(30), 50, 305  # pixels per unit, theta, the origin in the picture
        c, s = math.cos(TH), math.sin(TH)

        def at(x, y):
            return OX + U * x, OY - U * y

        def arrow(a, b, colour, w=2.0):
            (x0, y0), (x1, y1) = at(*a), at(*b)
            L = math.hypot(x1 - x0, y1 - y0)
            ux, uy = (x1 - x0) / L, (y1 - y0) / L
            bx, by = x1 - 10 * ux, y1 - 10 * uy
            return (
                f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{colour}" stroke-width="{w}"/>'
                f'<polygon points="{x1:.1f},{y1:.1f} {bx - 4.5 * uy:.1f},{by + 4.5 * ux:.1f} {bx + 4.5 * uy:.1f},{by - 4.5 * ux:.1f}" fill="{colour}"/>'
            )

        def ddx(x, y, letter):
            # the fraction d/d(letter), with its left end at x and its bar at height y
            return (
                f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x + 22:.1f}" y2="{y:.1f}" stroke="{O}" stroke-width="1"/>'
                f'<text x="{x + 11:.1f}" y="{y - 5:.1f}" text-anchor="middle" fill="{O}" font-family="KaTeX_Main" font-size="16">∂</text>'
                f'<text x="{x + 11:.1f}" y="{y + 16:.1f}" text-anchor="middle" fill="{O}" font-family="KaTeX_Math" font-style="italic" font-size="16"><tspan font-family="KaTeX_Main" font-style="normal">∂</tspan>{letter}</text>'
            )

        p = (r * c, r * s)
        dr = (p[0] + c, p[1] + s)
        dth = (p[0] - r * s, p[1] + r * c)
        px, py = at(*p)
        rx, ry = at(*dr)
        tx, ty = at(*dth)
        mx, my = at(p[0] / 2 - 0.2 * s, p[1] / 2 + 0.2 * c)
        ax0, ay0 = at(0.34 * c, 0.34 * s)
        return mo.Html(f"""
        <svg viewBox="0 36 305 309" style="display: block; margin: 0 auto; width: 305px; max-width: 100%;" role="img"
             aria-label="the point p at distance r from o, with the coordinate vectors d/dr, of length 1 along the ray, and d/dtheta, perpendicular to it and of length r">
          <line x1="20" y1="{OY}" x2="288" y2="{OY}" stroke="#000" stroke-width="1.1"/><polygon points="296,{OY} 286,{OY - 4} 286,{OY + 4}" fill="#000"/>
          <line x1="{OX}" y1="335" x2="{OX}" y2="52" stroke="#000" stroke-width="1.1"/><polygon points="{OX},44 {OX - 4},54 {OX + 4},54" fill="#000"/>
          <path d="M {OX + 0.34 * U:.1f} {OY} A {0.34 * U:.1f} {0.34 * U:.1f} 0 0 0 {ax0:.1f} {ay0:.1f}" fill="none" stroke="{G}" stroke-width="1.2"/>
          <line x1="{OX}" y1="{OY}" x2="{px:.1f}" y2="{py:.1f}" stroke="{B}" stroke-width="1.6"/>
          {arrow(p, dr, O)}
          {arrow(p, dth, O)}
          <circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="#000"/><circle cx="{OX}" cy="{OY}" r="3.6" fill="#000"/>
          {_name(OX - 18, OY + 22, "o")}
          {_name(OX + 42, OY - 6, "θ")}
          {_name(mx, my + 6, "r", B, "middle")}
          {_name(px + 10, py + 21, "p")}
          {ddx(rx + 8, ry + 2, "r")}
          {ddx(tx - 11, ty - 26, "θ")}
        </svg>
        """)

    def latitude_scene():
        # the latitude z = cos(phi_0)
        s_, t_ = np.meshgrid(np.linspace(0, np.pi, 25), np.linspace(0, 2 * np.pi, 97), indexing="ij")
        sphere = lk.sheet(np.sin(s_) * np.cos(t_), np.sin(s_) * np.sin(t_), np.cos(s_), alpha=0.45)
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
                    surfaces=[sphere],
                    outlines=[("sphere", (0, 0, 0), 1.0, lk.GREY, 1.0)],
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

    return latitude_scene, plane_figure, polar_figure


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figure.: r from 1 to 2
    polar_r = lk.slider(1.0, 2.0, step=0.1, value=1.5, label=r"$r$", show_value=False)
    return (polar_r,)


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        lk.aside(
            r"$\displaystyle\left.\begin{aligned}X:p\in M&\longrightarrow X_p\in T_pM\\X:C^\infty(M,\mathbb R)&\longrightarrow C^\infty(M,\mathbb R)\\f&\longmapsto X(f)\quad\text{linear + Leibniz}\end{aligned}\ \right\}\ \mk{X\in\Gamma(TM)}$",
            "smooth vector fields",
            at="middle",
        ),
        lk.aside(
            r"> $\overset{\varphi}{\leadsto}$ &nbsp; $X=X^i\,\partial_i$ &nbsp; where &nbsp; $\mk{X^i}=X(x^i):U\to\mathbb R$",
            r"component functions of $X$ with respect to $\varphi$<br>derivative of local coordinates in the direction of $X$",
        ),
        lk.aside(
            r"> <span class='lk-ghost'>$\overset{\varphi}{\leadsto}$ &nbsp; $X=X^i\,\partial_i$ &nbsp;</span> and &nbsp; $\mk{\partial_i|_p}\in T_pM$",
            r"coordinate basis of $T_pM$ with respect to $\varphi$<br>basis of partial derivatives with respect to local coordinates",
        ),
        lk.aside(
            r"> $\overset{\tilde\varphi}{\leadsto}$ &nbsp; $X=\tilde X^j\,\tilde\partial_j$ &nbsp; are related via &nbsp; $\mk{\dfrac{\partial\tilde x^j}{\partial x^i}}$",
            "the Jacobian matrix of the change of coordinates",
        ),
        lk.gap(),
        r"If &nbsp; $p=\varphi^{-1}(x^ie_i)=\tilde\varphi^{-1}(\tilde x^je_j)$",
        r"> $\Longrightarrow$ &nbsp; $\tilde x^j(x^ie_i)\,e_j=\tilde\varphi\circ\varphi^{-1}(x^ie_i)$",
        lk.aside(
            r"> $\displaystyle\begin{alignedat}{2}\Longrightarrow\quad&\partial_i&&=\frac{\partial\tilde x^j}{\partial x^i}\,\tilde\partial_j\\[0.3em]&\tilde X^j&&=\frac{\partial\tilde x^j}{\partial x^i}\,X^i\end{alignedat}$",
            [(1, r"$i$ free, $j$ summed over"), (2, r"$j$ free, $i$ summed over<br>coordinates and their indices must remain<br>coherent on both sides of the equations!")],
            rows=2,
        ),
        r"> > $\leadsto$ &nbsp; $\begin{bmatrix}\tilde X^1\\\vdots\\\tilde X^m\end{bmatrix}=\begin{bmatrix}{\large\tfrac{\partial\tilde x^1}{\partial x^1}}&\cdots&{\large\tfrac{\partial\tilde x^1}{\partial x^m}}\\\vdots&\ddots&\vdots\\{\large\tfrac{\partial\tilde x^m}{\partial x^1}}&\cdots&{\large\tfrac{\partial\tilde x^m}{\partial x^m}}\end{bmatrix}\begin{bmatrix}X^1\\\vdots\\X^m\end{bmatrix}$",
        topic="Smooth vector fields",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: integral curves
    # definition: integral curve
    lk.definition(
        [
            r"A path $\gamma(t)\in M$ is an **integral curve** of a smooth vector field $X\in\Gamma(TM)$ if",
            lk.aside(
                r"> $\gamma'(t)=X_{\gamma(t)}\in T_{\gamma(t)}M$",
                "velocity vector equals vector field along path",
            ),
            lk.aside(
                r"> > $\Longleftrightarrow$ &nbsp; $\dfrac{d}{dt}\,f\circ\gamma(t)=X_{\gamma(t)}(f)$ &nbsp; $\forall\,f\in C^\infty(M,\mathbb R)$",
                "directional derivative equals derivation",
            ),
            r"> > $\overset{\varphi}{\Longleftrightarrow}$ &nbsp; $\dfrac{d}{dt}\,x^i(t)=X^i(t)$ &nbsp; where &nbsp; $\gamma(t)=\varphi^{-1}(x^i(t)\,e_i)$",
            r"> > <span class='lk-ghost'>$\overset{\varphi}{\Longleftrightarrow}$ &nbsp; $\dfrac{d}{dt}\,x^i(t)=X^i(t)$ &nbsp; where &nbsp;</span> $X_{\gamma(t)}=X^i(t)\,\partial_i|_{\gamma(t)}$",
            lk.aside(
                r"> > > $\leadsto$ &nbsp; $\begin{cases}\dfrac{d}{dt}\,x^1(t)=X^1(t)\\\qquad\vdots\\\dfrac{d}{dt}\,x^m(t)=X^m(t)\end{cases}$",
                "1st order system of ODEs<br>for components of path",
            ),
        ],
        label="def-integral-curve",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: integral curves
    # comment: special integral curves need more structure
    lk.prose(
        r"""
        $\leadsto$ &nbsp; in affine spaces we could put the “same” vector at different points in space

        > $\Longrightarrow$ &nbsp; we have special vector fields on affine spaces (constant vector fields)

        > $\Longrightarrow$ &nbsp; we have special integral curves (straight lines)<br>which later became important physically (inertial particles)
        """,
        lk.aside(
            r"$\leadsto$ &nbsp; on manifolds, in order to obtain special vector fields,<br>and their special integral curves, we will need <span class='lk-mark'>more structure</span>!",
            "connections",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(
        lk.aside(
            r"Metrics (will give us <span class='lk-mark'>connections</span> later)",
            r"all elementary interactions in the standard model<br>of particle physics are given by types of connections<br>$\leadsto$ gravity as well!",
        ),
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("Schutz 5.2, 6.2; Carroll 2.5; Sasane 5.1–5.2")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: metrics
    # recall: Euclidean and Minkowski spaces
    lk.recall(
        [
            r"$\mathbb E^3=\big((\mathbb A^3,\mathbb V^3,-),\ \langle\cdot,\cdot\rangle\big)$",
            r"> $\langle\cdot,\cdot\rangle:\mathbb V^3\times\mathbb V^3\longrightarrow\mathbb R$ &nbsp; symmetric bilinear positive definite",
            r"$\mathbb M^{3,1}=\big((\mathbb A^4,\mathbb V^4,-),\ \eta(\cdot,\cdot)\big)$",
            lk.aside(
                r"> $\eta(\cdot,\cdot):\mathbb V^4\times\mathbb V^4\longrightarrow\mathbb R$ &nbsp; symmetric bilinear of <span class='lk-mark'>signature $(3,1)$</span>",
                "restriction to orthogonal complement<br>of timelike vector is Euclidean",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: metrics
    # definition: metric
    lk.definition(
        [
            r"""
            A **metric** on a manifold $M$ is an assignment

            $$
            g:p\in M\longmapsto g_p(\cdot,\cdot):T_pM\times T_pM\longrightarrow\mathbb R,
            $$

            of an inner product on each tangent space
            """,
            lk.aside(r"> • &nbsp; if $g_p$ is <span class='lk-mark'>Euclidean</span> for every $p\in M$", "positive definite"),
            r"> > $\leadsto$ &nbsp; $g$ is called a **Riemannian metric**",
            lk.aside(r"> • &nbsp; if $g_p$ is <span class='lk-mark'>Minkowski</span> for every $p\in M$", r"signature $(m-1,1)$"),
            r"> > $\leadsto$ &nbsp; $g$ is called a **Lorentzian metric**",
        ],
        label="def-metric",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: metrics in charts
    # components of a metric in a chart
    lk.prose(
        r"""
        In a chart &nbsp; $\varphi:U\subseteq M\to\mathbb R^m$

        > $p=\varphi^{-1}(x^ie_i)\in M$, &nbsp; $X_p=X^i(p)\,\partial_i|_p\in T_pM$, &nbsp; $Y_p=Y^j(p)\,\partial_j|_p\in T_pM$
        """,
        lk.aside(
            r"> > $\displaystyle\begin{alignedat}{2}\Longrightarrow\quad&g_p(X_p,Y_p)&&=g_p\big(X^i(p)\,\partial_i|_p,\ Y^j(p)\,\partial_j|_p\big)\\[0.3em]&&&=X^i(p)\,g_p(\partial_i|_p,\partial_j|_p)\,Y^j(p)\\[0.3em]&&&=X^i(p)\,\mk{g_{ij}(p)}\,Y^j(p)\\[0.3em]&&&=\big[X^1(p)\ \cdots\ X^m(p)\big]\begin{bmatrix}g_{11}(p)&\cdots&g_{1m}(p)\\\vdots&\ddots&\vdots\\g_{m1}(p)&\cdots&g_{mm}(p)\end{bmatrix}\begin{bmatrix}Y^1(p)\\\vdots\\Y^m(p)\end{bmatrix}\\[0.3em]&&&=[X^i(p)]^T\,[g_{ij}(p)]\,[Y^j(p)]\end{alignedat}$",
            [(2.5, r"components of $g_p$ with respect to $\varphi$"), (5.2, "matrix multiplication")],
            rows=5,
        ),
        lk.gap(),
        lk.aside(
            r"$g$ metric on $M$ &nbsp; $\overset{\varphi}{\leftrightsquigarrow}$ &nbsp; $\mk{g_{ij}}:U\subseteq M\to\mathbb R$",
            r"component functions of $g$ with respect to $\varphi$",
        ),
        r"<span class='lk-ghost'>$g$ metric on $M$ &nbsp;</span> $\overset{\tilde\varphi}{\leftrightsquigarrow}$ &nbsp; $\tilde g_{kl}:\tilde U\subseteq M\to\mathbb R$",
        r"""
        $$
        \begin{aligned}
        g_p(X_p,Y_p)&=[X^i(p)]^T\,[g_{ij}(p)]\,[Y^j(p)]\\[0.3em]
        &=[\tilde X^k(p)]^T\,[\tilde g_{kl}(p)]\,[\tilde Y^l(p)]\\[0.3em]
        &=[X^i(p)]^T\Big[\frac{\partial\tilde x^k}{\partial x^i}(p)\Big]^T[\tilde g_{kl}(p)]\Big[\frac{\partial\tilde x^l}{\partial x^j}(p)\Big][Y^j(p)]
        \end{aligned}
        $$
        """,
        lk.aside(
            r"> $\Longrightarrow$ &nbsp; $\displaystyle\boxed{\ g_{ij}=\frac{\partial\tilde x^k}{\partial x^i}\,\tilde g_{kl}\,\frac{\partial\tilde x^l}{\partial x^j},\quad\text{on }U\cap\tilde U\ }$",
            r"transformation of components of $g$<br>under change of charts",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk, plane_figure, polar_figure, polar_r):
    # module: metrics in charts
    # example: the Euclidean plane
    lk.example(
        [
            r"Euclidean plane $\mathbb E^2$",
            r"> Choose &nbsp; $o\in\mathbb E^2$, &nbsp; $e_1,e_2\in\mathbb V^2$ orthonormal.",
            lk.figure(plane_figure()),
            lk.aside(
                r"> $p=o+x\,e_1+y\,e_2=o+r\cos\theta\,e_1+r\sin\theta\,e_2$",
                r"$x=x^1$, &nbsp; $y=x^2$, &nbsp; $r=\tilde x^1$, &nbsp; $\theta=\tilde x^2$",
            ),
            r"""
            $$
            \begin{aligned}
            &\begin{aligned}
            X_p&=X^1\frac{\partial}{\partial x}+X^2\frac{\partial}{\partial y}=\tilde X^1\frac{\partial}{\partial r}+\tilde X^2\frac{\partial}{\partial\theta}\\[0.3em]
            &=\tilde X^1\Big(\frac{\partial x}{\partial r}\frac{\partial}{\partial x}+\frac{\partial y}{\partial r}\frac{\partial}{\partial y}\Big)+\tilde X^2\Big(\frac{\partial x}{\partial\theta}\frac{\partial}{\partial x}+\frac{\partial y}{\partial\theta}\frac{\partial}{\partial y}\Big)\\[0.3em]
            &=\big(\cos\theta\,\tilde X^1-r\sin\theta\,\tilde X^2\big)\frac{\partial}{\partial x}+\big(\sin\theta\,\tilde X^1+r\cos\theta\,\tilde X^2\big)\frac{\partial}{\partial y}
            \end{aligned}\\[6pt]
            &\Longrightarrow\quad \begin{bmatrix}X^1\\X^2\end{bmatrix}=\begin{bmatrix}\cos\theta&-r\sin\theta\\\sin\theta&r\cos\theta\end{bmatrix}\begin{bmatrix}\tilde X^1\\\tilde X^2\end{bmatrix}.
            \end{aligned}
            $$

            $$
            \begin{aligned}
            g_p(X_p,Y_p)&=X^1Y^1+X^2Y^2=[X^1\ X^2]\underbrace{\begin{bmatrix}1&0\\0&1\end{bmatrix}}_{\footnotesize\begin{bmatrix}g_{11}&g_{12}\\g_{21}&g_{22}\end{bmatrix}}\begin{bmatrix}Y^1\\Y^2\end{bmatrix}\\[0.5em]
            &=[\tilde X^1\ \tilde X^2]\begin{bmatrix}\cos\theta&\sin\theta\\-r\sin\theta&r\cos\theta\end{bmatrix}\begin{bmatrix}1&0\\0&1\end{bmatrix}\begin{bmatrix}\cos\theta&-r\sin\theta\\\sin\theta&r\cos\theta\end{bmatrix}\begin{bmatrix}\tilde Y^1\\\tilde Y^2\end{bmatrix}\\[0.5em]
            &=[\tilde X^1\ \tilde X^2]\underbrace{\begin{bmatrix}1&0\\0&r^2\end{bmatrix}}_{\footnotesize\begin{bmatrix}\tilde g_{11}&\tilde g_{12}\\\tilde g_{21}&\tilde g_{22}\end{bmatrix}}\begin{bmatrix}\tilde Y^1\\\tilde Y^2\end{bmatrix}=\tilde X^1\tilde Y^1+r^2\,\tilde X^2\tilde Y^2
            \end{aligned}
            $$
            """,
            lk.interactive(polar_figure(polar_r.value), controls=[polar_r]),
        ],
        label="ex-plane-metric",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: metrics in charts
    # example: the sphere
    lk.example(
        [
            r"$\mathbb S^2=\{(x,y,z)\in\mathbb R^3\mid x^2+y^2+z^2=1\}$",
            r"""
            $$
            \begin{aligned}
            &\begin{aligned}
            (x,y,z)&\overset{\varphi_n}{=}\Big(\frac{2u}{1+u^2+v^2},\ \frac{2v}{1+u^2+v^2},\ \frac{-1+u^2+v^2}{1+u^2+v^2}\Big)\\[0.3em]
            &\overset{\psi}{=}\big(\sin\phi\cos\theta,\ \sin\phi\sin\theta,\ \cos\phi\big)
            \end{aligned}\\[6pt]
            &\Longrightarrow\quad (u,v)=\big(\cot(\phi/2)\cos\theta,\ \cot(\phi/2)\sin\theta\big).
            \end{aligned}
            $$

            $\displaystyle X_p\overset{\varphi_n}{=}X^u\frac{\partial}{\partial u}+X^v\frac{\partial}{\partial v}\overset{\psi}{=}X^\phi\frac{\partial}{\partial\phi}+X^\theta\frac{\partial}{\partial\theta}$

            > $\Longrightarrow$ &nbsp; $\begin{bmatrix}X^u\\X^v\end{bmatrix}=\dfrac{-1}{2\sin(\phi/2)^2}\begin{bmatrix}\cos\theta&\sin\phi\sin\theta\\\sin\theta&-\sin\phi\cos\theta\end{bmatrix}\begin{bmatrix}X^\phi\\X^\theta\end{bmatrix}$
            """,
            lk.aside(
                r"$$\begin{aligned}g(X,Y)&\overset{\varphi_n}{=}\frac{4}{(1+u^2+v^2)^2}\,\big(X^uY^u+X^vY^v\big)\\[0.3em]&\overset{\psi}{=}X^\phi Y^\phi+(\sin\phi)^2\,X^\theta Y^\theta\\[0.3em]&\overset{\varphi_s}{=}\frac{4}{(1+\tilde u^2+\tilde v^2)^2}\,\big(X^{\tilde u}Y^{\tilde u}+X^{\tilde v}Y^{\tilde v}\big)\end{aligned}$$",
                [(2, r"round metric on $\mathbb S^2$")],
                rows=3,
            ),
        ],
        label="ex-sphere-round-metric",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: length
    # definition: length of a path
    lk.definition(
        r"""
        Given a Riemannian metric $g$ on $M$ and given $\gamma:[a,b]\to M$ a path segment on $M$

        $$
        \mathrm{length}_g(\gamma)=\int_a^b\sqrt{g_{\gamma(t)}(\gamma'(t),\gamma'(t))}\,dt.
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
            &\begin{aligned}
            g_{\gamma(t)}(\gamma'(t),\gamma'(t))&=\frac{4}{(1+u(t)^2+v(t)^2)^2}\,\big(u'(t)^2+v'(t)^2\big)\\
            &=\frac{4}{(1+\cot(\phi_0/2)^2)^2}\,\cot(\phi_0/2)^2=\sin(\phi_0)^2\\
            &=\phi'(t)^2+\sin(\phi(t))^2\,\theta'(t)^2
            \end{aligned}\\[6pt]
            &\Longrightarrow\quad \mathrm{length}_g(\gamma)=\int_0^{2\pi}\sqrt{\sin(\phi_0)^2}\,dt=2\pi\sin(\phi_0).
            \end{aligned}
            $$
            """,
        ],
        label="ex-latitude-length",
    )
    return


if __name__ == "__main__":
    app.run()
