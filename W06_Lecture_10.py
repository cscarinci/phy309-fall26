import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 10 · Derivations", css_file="lecturekit/style.css")


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
    lk.lecture(10, "Derivations")
    return


@app.cell(hide_code=True)
def _(Figure, lk, math, np):
    # Helpers of this lecture: the three figures, and the sphere

    def _blank(w, h, xlim, ylim):
        fig = Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def _inv(u, v):
        r = 1 + u**2 + v**2
        return 2 * u / r, 2 * v / r, (r - 2) / r

    def paths_figure():
        # paths through p with the same velocity, seen on M and in a chart (shared sketch style, lk.sk)
        sk = lk.sk
        fig, ax = sk.sketch((-2.6, 12.8), (-0.6, 8.4))
        sk.outline(ax, sk.shape(5.0, 5.4, 3.2, 2.3, egg=0.05, bean=0.04), name="$M$", at=(2.0, 7.45))
        sk.outline(ax, sk.shape(5.0, 5.4, 1.45, 1.05), lk.GREY, "$U$", (3.75, 6.55), tint=False)
        P = (5.0, 5.35)
        s, s2 = np.linspace(-0.95, 0.95, 80), np.linspace(-0.75, 0.75, 80)
        for col, k in ((lk.BLUE, 0.0), (lk.RED, 0.75), (lk.ORANGE, -0.75)):
            ax.plot(*sk.path(P, (1, 0.3), k, s), color=col, lw=sk.LW, zorder=4)
        sk.maps(ax, P, (P[0] + 0.9, P[1] + 0.27), color=lk.GREEN, lw=1.8)
        sk.dot(ax, P, "$p$", at=(-0.15, -0.3), ha="right")
        sk.label(ax, (6.6, 5.0), r"$v_p = [\gamma]$", lk.GREEN, ha="left", size=13)
        # the real line and the three paths as maps from it
        ax.plot([-2.3, -0.1], [3.2, 3.2], color=sk.INK, lw=1.2)
        sk.dot(ax, (-1.2, 3.2), "$0$", at=(0, -0.3))
        sk.label(ax, (-0.2, 2.85), r"$\mathbb{R}$", va="top")
        for col, dy, name in ((lk.BLUE, 1.2, r"$\gamma$"), (lk.RED, 0.75, r"$\tilde\gamma$"), (lk.ORANGE, 0.3, r"$\hat\gamma$")):
            sk.maps(ax, (-0.9, 3.3 + dy), (1.75, 4.1 + dy), color=col, bend=0.15, lw=1.3)
            sk.label(ax, (-1.05, 3.3 + dy), name, col, ha="right")
        # the chart box
        sk.chart(ax, 7.4, 0.4, 4.8, 2.6, lk.GREY)
        sk.label(ax, (12.2, 0.15), r"$\varphi(U) \subseteq \mathbb{R}^m$", va="top", ha="right")
        Q = (8.9, 1.85)
        for col, k in ((lk.BLUE, 0.0), (lk.RED, 0.9), (lk.ORANGE, -0.9)):
            ax.plot(*sk.path(Q, (1, 0.35), k, s2), color=col, lw=sk.LW, zorder=4)
        sk.maps(ax, Q, (Q[0] + 0.95, Q[1] + 0.33), color=lk.GREEN, lw=1.8)
        sk.dot(ax, Q, r"$\varphi(p)$", at=(-0.1, -0.85))
        sk.label(ax, (9.95, 2.5), r"$(\varphi \circ \gamma)'(0)$", lk.GREEN, ha="left", size=13)
        sk.maps(ax, (7.6, 3.7), (8.6, 3.15), r"$\varphi$", bend=-0.3, side=1)
        return fig

    def height_scene():
        # the sphere with the equator gamma and the meridian sigma through p = (1, 0, 0)
        s_, t_ = np.meshgrid(np.linspace(0, np.pi, 37), np.linspace(0, 2 * np.pi, 73), indexing="ij")
        sphere = lk.sheet(np.sin(s_) * np.cos(t_), np.sin(s_) * np.sin(t_), np.cos(s_), alpha=0.45)
        c = np.linspace(0, 2 * np.pi, 241)
        t0, t1 = 0.9, -0.8  # sigma(t) above p, gamma(t) in front of p, where their names are clear
        return lk.turntable(
            -30,
            16,
            "the unit sphere with the north pole n, the point p, the equator gamma and the meridian sigma through p",
            [
                lk.panel(
                    1.0,
                    surfaces=[sphere],
                    outlines=[("sphere", (0, 0, 0), 1.0, lk.GREY, 1.2)],
                    lines=[(np.cos(c), np.sin(c), 0 * c, lk.RED, 1.6), (np.cos(c), 0 * c, np.sin(c), lk.BLUE, 1.6)],
                    arrows=[((1, 0, 0), (1, 0.45, 0), lk.RED), ((1, 0, 0), (1, 0, 0.45), lk.BLUE)],
                    points=[((1, 0, 0), "#000000", 3.4), ((0, 0, 1), "#000000", 3.4), ((math.cos(t1), math.sin(t1), 0), lk.RED, 3.4), ((math.cos(t0), 0, math.sin(t0)), lk.BLUE, 3.4)],
                    texts=[
                        ((0, 0, 1), "n", "#000000", 90),
                        ((1, 0, 0), "p", "#000000", -120, 8),
                        ((math.cos(t1), math.sin(t1), 0), r"\gamma(t)", lk.RED, -90, 8),
                        ((math.cos(t0), 0, math.sin(t0)), r"\sigma(t)", lk.BLUE, 180, 6),
                    ],
                )
            ],
            height=340,
            width=340,
            bias=0.12,
        )

    def height_chart():
        # the two paths in the chart phi_n
        fig, ax = _blank(3.4, 3.0, (-1.8, 2.6), (-1.7, 1.9))
        ax.plot([-1.7, 2.4], [0, 0], color=lk.GREY, lw=0.8)
        ax.plot([0, 0], [-1.6, 1.7], color=lk.GREY, lw=0.8)
        c = np.linspace(0, 2 * np.pi, 200)
        ax.plot(np.cos(c), np.sin(c), color=lk.RED)
        ax.plot([-1.7, 2.4], [0, 0], color=lk.BLUE)
        ax.plot(1, 0, "o", color="#000000", ms=5)
        ax.text(1.08, -0.38, r"$\varphi_n(p)$", fontsize=12)
        ax.text(-1.75, 1.25, r"$\varphi_n \circ \gamma(t)$", color=lk.RED, fontsize=12)
        ax.text(1.15, 0.22, r"$\varphi_n \circ \sigma(t)$", color=lk.BLUE, fontsize=12)
        ax.text(2.45, -0.08, "$u$", fontsize=12)
        ax.text(-0.05, 1.72, "$v$", fontsize=12, ha="center")
        return fig

    def basis_scene(u, v):
        # the coordinate curves of u and v through p and the coordinate basis vectors at p
        r = 1 + u**2 + v**2
        p = np.array(_inv(u, v))
        du = np.array([2 * (1 - u**2 + v**2), -4 * u * v, 4 * u]) / r**2
        dv = np.array([-4 * u * v, 2 * (1 + u**2 - v**2), 4 * v]) / r**2
        # each name sits at its tip, on the side its arrow points to in the first view (azimuth -30, elevation 16)
        a, e = math.radians(-30), math.radians(16)
        right = np.array([-math.sin(a), math.cos(a), 0])
        up = np.array([-math.sin(e) * math.cos(a), -math.sin(e) * math.sin(a), math.cos(e)])
        lab_u, lab_v = (float(np.degrees(np.arctan2(w @ up, w @ right))) for w in (du, dv))
        s_, t_ = np.meshgrid(np.linspace(0, np.pi, 37), np.linspace(0, 2 * np.pi, 73), indexing="ij")
        sphere = lk.sheet(np.sin(s_) * np.cos(t_), np.sin(s_) * np.sin(t_), np.cos(s_), alpha=0.45)
        plane = [(-1.25, -1.25, 0), (1.25, -1.25, 0), (1.25, 1.25, 0), (-1.25, 1.25, 0)]
        edge = np.array(plane + plane[:1])
        k = np.linspace(0, 1, 30)
        s = np.tan(np.linspace(-1.5, 1.5, 400))
        c = np.linspace(0, 2 * np.pi, 121)
        return lk.turntable(
            -30,
            16,
            "the unit sphere and the plane z = 0, with the centre, the point p, the coordinate curves of u and v through p and the coordinate basis vectors at p",
            [
                lk.panel(
                    1.0,
                    surfaces=[sphere, lk.patch(plane, "#e8e8e8", 0.6, n=16)],
                    outlines=[("sphere", (0, 0, 0), 1.0, lk.GREY, 1.2)],
                    lines=[
                        (*edge.T, lk.GREY, 1.2),
                        (np.cos(c), np.sin(c), 0 * c, "#000000", 1.0),
                        (p[0] * k, p[1] * k, p[2] * k, "#000000", 1.0),
                        (*_inv(u + s, v + 0 * s), lk.BLUE, 1.4),
                        (*_inv(u + 0 * s, v + s), lk.RED, 1.4),
                    ],
                    arrows=[(tuple(p), tuple(p + 0.8 * du), lk.BLUE), (tuple(p), tuple(p + 0.8 * dv), lk.RED)],
                    points=[(tuple(p), "#000000", 3.4), ((0, 0, 1), "#000000", 3.4), ((0, 0, 0), "#000000", 2.6)],
                    texts=[
                        ((0, 0, 1), "n", "#000000", 90),
                        (tuple(p), "p", "#000000", -120, 8),
                        (tuple(p + 0.8 * du), r"\partial_u|_p", lk.BLUE, lab_u, 4),
                        (tuple(p + 0.8 * dv), r"\partial_v|_p", lk.RED, lab_v, 4),
                    ],
                    box=((-1.25, 1.25), (-1.25, 1.25), (-0.7, 0.7)),
                )
            ],
            height=340,
            width=340,
            key="L10-basis",
            apart=True,
            bias=0.12,
        )

    def basis_chart(u, v):
        # the coordinate lines through phi_n(p) and the vectors e_u, e_v in the chart
        c = np.linspace(0, 2 * np.pi, 400)
        fig = Figure(figsize=(3.4, 3.4), layout="constrained")
        ax = fig.subplots()
        ax.set_title(r"$\varphi_n = (u, v)$", fontsize=13)
        ax.set_xlim(-3.0, 3.0)
        ax.set_ylim(-3.0, 3.0)
        ax.set_aspect("equal")
        ax.axhline(0, color="#000000", lw=0.6)
        ax.axvline(0, color="#000000", lw=0.6)
        ax.plot(np.cos(c), np.sin(c), color=lk.GREY, lw=1.0)
        ax.text(-0.83, -0.83, "equator", color=lk.GREY, fontsize=10, ha="center", va="center", rotation=-45, rotation_mode="anchor")
        ax.plot([-3.0, 3.0], [v, v], color=lk.BLUE)
        ax.plot([u, u], [-3.0, 3.0], color=lk.RED)
        lk.arrow(ax, (u, v), (u + 0.8, v), lk.BLUE)
        lk.arrow(ax, (u, v), (u, v + 0.8), lk.RED)
        ax.plot(u, v, "o", color="#000000", ms=5)
        ax.annotate(r"$\varphi_n(p)$", (u, v), textcoords="offset points", xytext=(3, -3), ha="left", va="top", fontsize=12)
        ax.set_xticks([-3, 0, 3])
        ax.set_yticks([-3, 0, 3])
        return fig

    return basis_chart, basis_scene, height_chart, height_scene, paths_figure


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figure
    s_u = lk.slider(-1.5, 1.5, step=0.1, value=1.0, label="$u$", show_value=False)
    s_v = lk.slider(-1.5, 1.5, step=0.1, value=0.0, label="$v$", show_value=False)
    return s_u, s_v


@app.cell(hide_code=True)
def _(basis_scene, s_u, s_v):
    # the scene of the coordinate basis figure, in place by its sliders
    basis_scene(s_u.value, s_v.value)
    return


@app.cell(hide_code=True)
def _(lk, paths_figure):
    # module: recap
    # recap
    lk.recap(
        r"$M$ &nbsp; $m$-manifold, &nbsp; $p\in M$ &nbsp; point on $M$",
        lk.aside(
            r"$$\begin{aligned}T_pM&=\text{tangent space to }M\text{ at }p\\[0.3em]&=\big\{[\gamma]\mid\gamma:\mathbb R\to M\text{ smooth path with }\gamma(0)=p\\[0.1em]&\phantom{=\big\{}\text{ and }\gamma\sim\tilde\gamma\text{ if }(\mk{\varphi}\circ\gamma)'(0)=(\varphi\circ\tilde\gamma)'(0)\big\}\end{aligned}$$",
            r"for some chart $\varphi$<br>(therefore for every chart)",
            at="last",
        ),
        lk.figure(paths_figure()),
        lk.aside(
            r"Given &nbsp; $f:M\to N$ &nbsp; <span class='lk-mark'>smooth at $p\in M$</span>",
            r"$\psi\circ f\circ\varphi^{-1}:\varphi(U\cap f^{-1}(V))\to\psi(f(U)\cap V)$<br>smooth $\forall\,\varphi,\psi$ $\ (p\in U\cap f^{-1}(V))$",
        ),
        r"$$Df_p:T_pM\longrightarrow T_{f(p)}N,\qquad Df_p\underbrace{[\gamma]}_{\footnotesize\begin{matrix}\text{velocity vector}\\\text{at }p\in M\end{matrix}}\qquad\quad=\qquad\quad\underbrace{[f\circ\gamma]}_{\footnotesize\begin{matrix}\text{velocity vector}\\\text{at }f(p)\in N\end{matrix}}$$",
        topic="Tangent vectors & the derivative",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("Schutz 6.1; Carroll 2.3; Sasane 2.1–2.4")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: directional derivatives
    # example: the derivative of a scalar function is a directional derivative
    lk.example(
        [
            r"$f:M\to\mathbb R$ &nbsp; smooth",
            lk.aside(r"> $\leadsto$ &nbsp; $Df_p:T_pM\longrightarrow T_{f(p)}\mathbb R\mathrel{\mk{\approx}}\mathbb R$", r"using affine structure of $\mathbb R$"),
            lk.aside(
                r"> > $v_p=[\gamma]\longmapsto[f\circ\gamma]=\dfrac{d}{dt}\Big|_{t=0}f\circ\gamma(t)=\mk{Df_p(v_p)}$",
                r"directional derivative at $p$<br>in the direction $v_p$",
            ),
        ],
        label="ex-scalar-derivative",
    )
    return


@app.cell(hide_code=True)
def _(height_chart, height_scene, lk, mo):
    # module: directional derivatives
    # example: the height function on the sphere, along a latitude and a meridian
    lk.example(
        [
            r"$\mathbb S^2=\{(x,y,z)\in\mathbb R^3\mid x^2+y^2+z^2=1\}$",
            lk.aside(r"$h:\mathbb S^2\to\mathbb R$, &nbsp; $h(x,y,z)=z$", "height function"),
            r"$p=(1,0,0)\in\mathbb S^2$",
            r"$\begin{aligned}\gamma(t)&=\big(\cos(t),\ \sin(t),\ 0\big)\\[0.2em]\sigma(t)&=\big(\cos(t),\ 0,\ \sin(t)\big)\end{aligned}$",
            lk.aside(r"$\varphi_n(x,y,z)=\Big(\dfrac{x}{1-z},\ \dfrac{y}{1-z}\Big)$", "local chart"),
            lk.aside(
                r"> $\leadsto$ &nbsp; $\varphi_n^{-1}(u,v)=\Big(\dfrac{2u}{1+u^2+v^2},\ \dfrac{2v}{1+u^2+v^2},\ \dfrac{-1+u^2+v^2}{1+u^2+v^2}\Big)$",
                "local coordinates parameterization",
            ),
            lk.aside(r"> $\leadsto$ &nbsp; $h\circ\varphi_n^{-1}(u,v)=\dfrac{-1+u^2+v^2}{1+u^2+v^2}$", r"local coordinate representation of $h$"),
            lk.aside(
                r"""
                > $\leadsto$ &nbsp; $\varphi_n\circ\gamma(t)=\big(\cos(t),\ \sin(t)\big)$

                > $\leadsto$ &nbsp; $\varphi_n\circ\sigma(t)=\Big(\dfrac{\cos(t)}{1-\sin(t)},\ 0\Big)$
                """,
                [(1.5, r"local coordinate representation of $\gamma,\sigma$")],
                rows=2,
            ),
            lk.gap(),
            lk.aside(
                r"$$\begin{aligned}Dh_p[\gamma]&=[h\circ\gamma]=\mk{(h\circ\gamma)'(0)}=\frac{d}{dt}\Big|_{t=0}(0)=0\\[0.3em]&=\big[(h\circ\varphi_n^{-1})\circ(\varphi_n\circ\gamma)\big]\end{aligned}$$",
                [
                    (1, r"velocity at $t=0$ of $h\circ\gamma:\mathbb R\to\mathbb R$"),
                    (2, r"we can only “avoid” this step because $h$ and $\gamma$ are simple<br>usually we must work with coordinate representations"),
                ],
                rows=2,
            ),
            r"$$\begin{aligned}Dh_p[\sigma]&=[h\circ\sigma]=(h\circ\sigma)'(0)=\frac{d}{dt}\Big|_{t=0}\big(\sin(t)\big)=1\\[0.3em]&=\big[(h\circ\varphi_n^{-1})\circ(\varphi_n\circ\sigma)\big]\end{aligned}$$",
            lk.figure(mo.hstack([height_scene(), height_chart()], justify="center", align="center", gap=2)),
        ],
        label="ex-height",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: directional derivatives
    # consequence: tangent vectors differentiate scalar functions
    lk.prose(
        r"""
        $\leadsto$ &nbsp; tangent vectors $v_p=[\gamma]\in T_pM$ let us differentiate scalar functions $f:M\to\mathbb R$

        $$Df_p(v_p)\mathrel{\text{“}{=}\text{”}}\frac{d}{dt}\Big|_{t=0}(f\circ\gamma)(t)$$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: derivations
    # definition: derivations at a point
    lk.definition(
        [
            lk.aside(
                r"Given $p\in M$, the space of **derivations** of $M$ at $p$ is the space of linear <span class='lk-mark'>functionals</span>",
                "functions of functions",
            ),
            lk.aside(r"$$X_p:\mk{C^\infty(M,\mathbb R)}\longrightarrow\mathbb R$$", r"space of smooth functions on $M$"),
            lk.aside(r"satisfying the <span class='lk-mark'>Leibniz rule</span>", "product rule"),
            r"$$X_p(fg)=X_p(f)\,g(p)+f(p)\,X_p(g)$$",
            lk.aside(
                r"$\mk{\mathrm{Der}_p(M)}=$ space of derivations of $M$ at $p$",
                r"= space of functionals that “behave”<br>like derivatives at $p\in M$",
            ),
        ],
        label="def-derivations",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: derivations
    # theorem: derivations are tangent vectors
    lk.theorem(
        [
            r"$$\mathrm{Der}_p(M)\approx T_pM$$",
            lk.aside(r"> $\leadsto$ &nbsp; directional derivatives <span class='lk-mark'>are derivations</span>", "satisfy Leibniz"),
            lk.aside(
                r"> $\leadsto$ &nbsp; every derivation <span class='lk-mark'>is a directional derivative</span>",
                "is associated to some<br>equivalence class of paths",
            ),
        ],
        label="thm-derivations",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: derivations
    # proof
    lk.proof(
        [
            r"""
            Given $[\gamma]\in T_pM$, choose any representative $\gamma$

            Define &nbsp; $X_p(f)=\dfrac{d}{dt}\Big|_{t=0}(f\circ\gamma)(t)\in\mathbb R$

            > $\displaystyle\begin{alignedat}{2}\Longrightarrow\quad&X_p(f\cdot g)&&=\frac{d}{dt}\Big|_{t=0}\big((f\cdot g)\circ\gamma\big)\\[0.3em]&&&=(f\circ\gamma)'(0)\,g(\gamma(0))+f(\gamma(0))\,(g\circ\gamma)'(0)\\[0.3em]&&&=X_p(f)\,g(p)+f(p)\,X_p(g)\end{alignedat}$

            > > $\therefore$ &nbsp; $X_p\in\mathrm{Der}_p(M)$
            """,
            lk.gap(),
            r"""
            $X_p$ only depends on $[\gamma]$, not on the choice of $\gamma$

            > $\leadsto$ &nbsp; work in a chart $\varphi$: &nbsp; $f\circ\varphi^{-1}$, &nbsp; $\varphi\circ\gamma$

            > > $\displaystyle\begin{alignedat}{2}\Longrightarrow\quad&\frac{d}{dt}\Big|_{t=0}(f\circ\gamma)(t)&&=\frac{d}{dt}\Big|_{t=0}(f\circ\varphi^{-1})\circ(\varphi\circ\gamma)(t)\\[0.3em]&&&=\underbrace{D(f\circ\varphi^{-1})_{\varphi(p)}}_{\footnotesize\begin{matrix}\text{independent}\\\text{of }\gamma\end{matrix}}\ \underbrace{(\varphi\circ\gamma)'(0)}_{\footnotesize\begin{matrix}\text{same for every}\\\gamma\text{ in }[\gamma]\end{matrix}}\end{alignedat}$
            """,
            lk.gap(),
            r"""
            Conversely, given $X_p\in\mathrm{Der}_p(M)$ let's define $[\gamma]\in T_pM$

            > $\leadsto$ &nbsp; work in a chart $\varphi$: &nbsp; consider $x^i:U\to\mathbb R$ such that $\varphi(q)=x^i(q)\,e_i$

            > > $\leadsto$ &nbsp; $x^i\circ\varphi^{-1}(x)=x^i$

            > > $\Longrightarrow$ &nbsp; $X_p(x^i)=v^i\in\mathbb R$

            > Define &nbsp; $\gamma(t)=\varphi^{-1}\big(\varphi(p)+t\,v^ie_i\big)=\varphi^{-1}\big((x^i(p)+t\,v^i)\,e_i\big)$

            > > $\displaystyle\begin{alignedat}{2}\Longrightarrow\quad&\frac{d}{dt}\Big|_{t=0}(f\circ\gamma)(t)&&=\frac{d}{dt}\Big|_{t=0}(f\circ\varphi^{-1})\big(\varphi(p)+t\,v^ie_i\big)\\[0.3em]&&&=\frac{\partial}{\partial x^i}(f\circ\varphi^{-1})(\varphi(p))\cdot v^i\\[0.6em]\Longrightarrow\quad&\frac{d}{dt}\Big|_{t=0}(x^i\circ\gamma)(t)&&=\frac{\partial x^i}{\partial x^j}(\varphi(p))\,v^j=v^i=X_p(x^i)\end{alignedat}$
            """,
            lk.aside(
                r"> > $\Longrightarrow$ &nbsp; $X_p$ is the directional derivative at $p$ in the <span class='lk-mark'>direction of $[\gamma]$</span>!",
                "for every $f$; which we already know is<br>independent of the choice of charts $\\varphi$",
            ),
            lk.gap(),
            r"$\therefore$ &nbsp; we have a bijection $T_pM\overset{\sim}{\longrightarrow}\mathrm{Der}_p(M)$ given with respect to a chart $\varphi$ by",
            lk.aside(
                r"> $[\gamma]$ &nbsp; such that &nbsp; $(\varphi\circ\gamma)'(0)=v^ie_i$ &nbsp; $\longleftrightarrow$ &nbsp; $X_p$ &nbsp; such that &nbsp; $X_p(\mk{x^i})=v^i$",
                r"local coordinate functions of $\varphi$",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: derivations
    # remark: the vector space structure of the tangent space
    lk.remark(
        r"""
        $\mathrm{Der}_p(M)$ is naturally a vector space!

        > if &nbsp; $X_p,Y_p\in\mathrm{Der}_p(M)$, &nbsp; $\alpha,\beta\in\mathbb R$

        > > $\Longrightarrow$ &nbsp; $\alpha X_p+\beta Y_p\in\mathrm{Der}_p(M)$

        > $\Longrightarrow$ &nbsp; the bijection above defines a vector space structure on the tangent space $T_pM$!
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: coordinate basis
    # remark: each chart defines a basis
    lk.remark(
        r"""
        Each choice of local chart defines a basis of $T_pM$

        > $\leadsto$ &nbsp; given &nbsp; $\varphi:U\subseteq M\to\varphi(U)\subseteq\mathbb R^m$, with $p\in U$, &nbsp; define &nbsp; $\partial_i|_p\in T_pM\approx\mathrm{Der}_p(M)$

        > > $\partial_i|_p=\big[t\longmapsto\varphi^{-1}(\varphi(p)+t\,e_i)\big]$

        > > > $\displaystyle\begin{alignedat}{2}\longleftrightarrow\quad&\partial_i|_p(f)&&=\frac{d}{dt}\Big|_{t=0}(f\circ\varphi^{-1})(\varphi(p)+t\,e_i)\\[0.3em]&&&=\frac{\partial}{\partial x^i}\Big|_{x=\varphi(p)}(f\circ\varphi^{-1})\end{alignedat}$
        """
    )
    return


@app.cell(hide_code=True)
def _(basis_chart, lk, mo, s_u, s_v):
    # module: coordinate basis
    # example: the coordinate basis of the north stereographic chart at p = (1, 0, 0)
    lk.example(
        [
            r"$\mathbb S^2$, &nbsp; $\varphi_n=(u,v):\mathbb S^2-\{n\}\to\mathbb R^2$, &nbsp; $p=(1,0,0)$",
            r"""
            $$
            \begin{aligned}
            \partial_u|_p&=\big[t\longmapsto\varphi_n^{-1}(1+t,0)\big]\\[0.3em]
            &=\Big[t\longmapsto\Big(\frac{2(1+t)}{1+(1+t)^2},\ 0,\ \frac{-1+(1+t)^2}{1+(1+t)^2}\Big)\Big]=[\sigma]
            \end{aligned}
            $$

            $$\partial_u|_p(f)=\frac{\partial}{\partial u}\Big|_{(u,v)=(1,0)}(f\circ\varphi_n^{-1})(u,v)$$

            $$
            \begin{aligned}
            \partial_u|_p(h)&=\frac{\partial}{\partial u}\Big|_{(1,0)}\frac{-1+u^2+v^2}{1+u^2+v^2}\\[0.3em]
            &=\frac{2u(1+u^2+v^2)-(-1+u^2+v^2)\,2u}{(1+u^2+v^2)^2}\Big|_{(1,0)}\\[0.3em]
            &=\frac{2+2}{2^2}=1
            \end{aligned}
            $$
            """,
            lk.interactive(
                mo.hstack([lk.frame("L10-basis", 340), basis_chart(s_u.value, s_v.value)], justify="center", align="center", gap=2),
                controls=[s_u, s_v],
            ),
        ],
        label="ex-coordinate-basis",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: summary
    # conclusion and outlook
    lk.prose(
        r"""
        $\therefore$ &nbsp; On manifolds, tangent vectors at a point are defined as equivalence classes of paths through that point, and can be identified with derivations of smooth functions at that point!

        Moreover, a choice of chart defines a basis of tangent vectors at a point in terms of partial derivatives with respect to the local coordinates!

        $\leadsto$ &nbsp; Next: solving differential equations on manifolds
        """
    )
    return


if __name__ == "__main__":
    app.run()
