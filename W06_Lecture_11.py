import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 11 · Vector fields", css_file="lecturekit/style.css")


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
    lk.lecture(11, "Vector fields")
    return


@app.cell(hide_code=True)
def _(Figure, lk, math, np):
    # Helpers of this lecture: the two figures

    def _inv(u, v):
        r = 1 + u**2 + v**2
        return 2 * u / r, 2 * v / r, (r - 2) / r

    def _parts(u0, v0, t):
        sol = lambda s: (u0 * np.cos(s) - v0 * np.sin(s), u0 * np.sin(s) + v0 * np.cos(s))
        return sol(np.linspace(0, t, 200)), sol(np.linspace(0, 2 * np.pi, 400)), tuple(float(a) + 0.0 for a in sol(t))

    def curve_scene(u0, v0, t):
        # the field on a few latitudes of the sphere and the integral curve from gamma(0) to gamma(t)
        (us, vs), (uw, vw), (ut, vt) = _parts(u0, v0, t)
        s_, t_ = np.meshgrid(np.linspace(0, np.pi, 37), np.linspace(0, 2 * np.pi, 73), indexing="ij")
        sphere = lk.sheet(np.sin(s_) * np.cos(t_), np.sin(s_) * np.sin(t_), np.cos(s_))  # opaque: the vectors on the far side stay hidden
        arrows = []
        for z in (-0.75, -0.4, 0.0, 0.4, 0.75):
            rr = math.sqrt(1 - z**2)
            for a in np.linspace(0, 2 * np.pi, 12, endpoint=False):
                q = (rr * math.cos(a), rr * math.sin(a), z)
                arrows.append((q, (q[0] - 0.22 * q[1], q[1] + 0.22 * q[0], z), lk.BLUE, 1.2))
        return lk.turntable(
            -30,
            20,
            "the unit sphere with the vector field X on a few latitudes and the integral curve gamma from gamma(0) to gamma(t)",
            [
                lk.panel(
                    1.0,
                    surfaces=[sphere],
                    outlines=[("sphere", (0, 0, 0), 1.0, lk.GREY, 1.2)],
                    lines=[(*_inv(uw, vw), lk.RED, 0.9), (*_inv(us, vs), lk.RED, 1.8)],
                    arrows=arrows,
                    points=[(_inv(u0, v0), lk.RED, 4.0, True), (_inv(ut, vt), lk.RED, 4.0), ((0, 0, 1), "#000000", 3.4), ((0, 0, -1), "#000000", 3.4)],
                    texts=[((0, 0, 1), "n", "#000000", 90), ((0, 0, -1), "s", "#000000", -90)],
                )
            ],
            height=340,
            width=340,
            key="L11-curve",
            apart=True,
            bias=0.12,
        )

    def curve_chart(u0, v0, t):
        # the same curve and field in the chart phi_n
        (us, vs), (uw, vw), (ut, vt) = _parts(u0, v0, t)
        c = np.linspace(0, 2 * np.pi, 400)
        fig = Figure(figsize=(3.4, 3.4), layout="constrained")
        ax = fig.subplots()
        ax.set_title(r"$\varphi_n = (u, v)$", fontsize=13)
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_aspect("equal")
        ax.axhline(0, color="#000000", lw=0.6)
        ax.axvline(0, color="#000000", lw=0.6)
        g = np.linspace(-2.5, 2.5, 9)
        for a0 in g:
            for b0 in g:
                if a0 or b0:
                    lk.arrow(ax, (a0, b0), (a0 - b0 / 5, b0 + a0 / 5), lk.BLUE, lw=1.0)
        ax.plot(np.cos(c), np.sin(c), color=lk.GREY, lw=1.0)
        ax.text(-0.83, -0.83, "equator", color=lk.GREY, fontsize=10, ha="center", va="center", rotation=-45, rotation_mode="anchor")
        ax.plot(uw, vw, color=lk.RED, lw=0.9)
        ax.plot(us, vs, color=lk.RED)
        ax.plot(u0, v0, "o", color=lk.RED, mfc="white", ms=6)
        ax.plot(ut, vt, "o", color=lk.RED, ms=6)
        al = math.atan2(v0, u0)
        w = 1 / math.hypot(1.2, 1)
        for (px, py), an, sg, name in (((u0, v0), al, -1, r"$\gamma(0)$"), ((ut, vt), al + t, 1, r"$\gamma(t)$")):
            # mostly outward from the circle, a little behind (gamma(0)) or ahead (gamma(t)) along it, clear of the other name
            nx, ny = math.cos(an), math.sin(an)
            dx, dy = (1.2 * nx - sg * ny) * w, (1.2 * ny + sg * nx) * w
            off = max(9 * abs(dx) + 5.5 * abs(dy) + 3, (9 * abs(nx) + 5.5 * abs(ny) + 3) / (1.2 * w), min(11 / (w * abs(ny) + 1e-9), 7.5 / (w * abs(nx) + 1e-9)))
            ax.annotate(name, (px, py), textcoords="offset points", xytext=(off * dx, off * dy), ha="center", va="center", color="#000000", fontsize=11, annotation_clip=False, zorder=8).set_in_layout(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel(r"$u$", labelpad=2)
        ax.set_ylabel(r"$v$", rotation=0, labelpad=8)
        return fig

    def bundle_scene():
        # a curved surface M with the tangent planes at three points and tangent vectors in each
        def h(x, y):
            return 0.35 * np.sin(1.1 * x) * np.cos(0.9 * y) + 0.12 * y

        def dh(x, y):
            return 0.35 * 1.1 * np.cos(1.1 * x) * np.cos(0.9 * y), -0.35 * 0.9 * np.sin(1.1 * x) * np.sin(0.9 * y) + 0.12

        X, Y = np.meshgrid(np.linspace(-2.2, 2.2, 43), np.linspace(-2.2, 2.2, 43), indexing="ij")
        g = np.linspace(-2.2, 2.2, 160)
        k = -2.2 + 0 * g
        lines = [(g, k, h(g, k), "#000000", 1.2), (g, -k, h(g, -k), "#000000", 1.2), (k, g, h(k, g), "#000000", 1.2), (-k, g, h(-k, g), "#000000", 1.2)]
        arrows, points, texts = [], [], [((-2.2, -2.2, h(-2.2, -2.2)), "M", "#000000", -150, 10)]
        surfaces = [lk.sheet(X, Y, h(X, Y))]  # smooth surface, no wire grid
        spots = {"W_r": (-1.15, 0.4, 180), "Z_q": (0.9, 0.62, 45), r"T_q M": (0.0, 0.8, 90), r"T_r M": (0.75, -0.7, -60), "Y_p": (0.22, 0.4, 0)}
        for (x, y), col, fill, name, tn, vecs in (
            ((-1.3, -0.2), lk.BLUE, "#dbe8f6", "q", r"T_q M", (((0.3, 0.2), "Z_q"),)),
            ((1.25, -1.0), lk.RED, "#f4d6d4", "p", r"T_p M", (((0.38, -0.12), "X_p"), ((0.1, 0.38), "Y_p"))),
            ((0.5, 1.5), lk.ORANGE, "#fde0c8", "r", r"T_r M", (((-0.5, 0.25), "W_r"),)),
        ):
            P = np.array([x, y, h(x, y)])
            hx, hy = dh(x, y)
            tx, ty = np.array([1.0, 0.0, hx]), np.array([0.0, 1.0, hy])
            corners = np.array([P + s * 0.7 * tx + t * 0.55 * ty for s, t in ((-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1))])
            surfaces.append(lk.patch(corners[:4], fill, 0.6))
            lines.append((*corners.T, col, 1.2, None, 0.6))
            for (a, b), lab in vecs:
                tip = P + a * tx + b * ty
                arrows.append((tuple(P), tuple(tip), col))
                sp = spots.get(lab)
                texts.append((tuple(P + sp[0] * tx + sp[1] * ty), lab, col, sp[2], 0) if sp else (tuple(tip), lab, col, math.degrees(math.atan2(b, a)), 6))
            points.append((tuple(P), "#000000", 3.4))
            sp = spots.get(tn)
            texts += [(tuple(P), name, "#000000", -135, 6), (tuple(P + sp[0] * tx + sp[1] * ty), tn, col, sp[2], 0) if sp else (tuple(corners[0]), tn, col, 180, 6)]
        return lk.turntable(
            -35,
            28,
            "a curved surface M with the tangent planes at three points q, p, r and tangent vectors in each",
            [lk.panel(1.0, surfaces=surfaces, lines=lines, arrows=arrows, points=points, texts=texts)],
            height=340,
            width=560,
            bias=0.25,
            zoom=1.45,
        )

    return bundle_scene, curve_chart, curve_scene


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figure
    s_u0 = lk.slider(-1.5, 1.5, step=0.1, value=1.4, label="$u_0$", show_value=False)
    s_v0 = lk.slider(-1.5, 1.5, step=0.1, value=0.0, label="$v_0$", show_value=False)
    s_t = lk.slider(0.0, 6.28, step=0.02, value=1.0, label="$t$", show_value=False)
    return s_t, s_u0, s_v0


@app.cell(hide_code=True)
def _(curve_scene, s_t, s_u0, s_v0):
    # the scene of the integral curve figure, in place by its sliders
    curve_scene(s_u0.value, s_v0.value, s_t.value)
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"Tangent vectors & derivations",
        lk.under(
            r"$M$ &nbsp; $m$-manifold, &nbsp; $p\in M$",
            r"""
            $T_pM=\{[\gamma]\mid\gamma:\mathbb R\to M,\ \gamma(0)=p\}$

            > $\gamma\sim\tilde\gamma$ &nbsp; if &nbsp; $(\varphi\circ\gamma)'(0)=(\varphi\circ\tilde\gamma)'(0)$

            $\mathrm{Der}_p(M)=\{X_p:C^\infty(M,\mathbb R)\to\mathbb R\mid\text{linear + Leibniz}\}$

            > $X_p(fg)=X_p(f)\,g(p)+f(p)\,X_p(g)$

            $T_pM\simeq\mathrm{Der}_p(M)$

            > $[\gamma]\longleftrightarrow X_p$ &nbsp; if &nbsp; $X_p(f)=\dfrac{d}{dt}\Big|_{t=0}(f\circ\gamma)(t)$
            """,
            lk.aside(
                r"> <span class='lk-ghost'>$[\gamma]\longleftrightarrow X_p$ &nbsp; if &nbsp;</span> $\Longleftrightarrow$ &nbsp; $(\varphi\circ\gamma)'(0)=X_p(\mk{x^i})\,e_i$",
                r"$x^i:U\subseteq M\to\mathbb R$ coordinate functions<br>of $\varphi:U\subseteq M\to\mathbb R^m$",
            ),
            r"""
            > $\Longrightarrow$ &nbsp; on manifolds, we can also identify velocity vectors with directional derivatives!

            Corollary: &nbsp; $T_pM$ is an $m$ dimensional vector space!

            > • &nbsp; $[\rho]=a[\gamma]+b[\sigma]$ &nbsp; $\Longleftrightarrow$ &nbsp; $Z_p=aX_p+bY_p$

            > • &nbsp; basis: for each $\varphi:U\subseteq M\to\mathbb R^m$ we have

            > > $\partial_i|_p\in\mathrm{Der}_p(M)$, &nbsp; $\partial_i|_pf=\dfrac{\partial}{\partial x^i}(f\circ\varphi^{-1})\Big|_{\varphi(p)}$

            > > > $\leadsto$ &nbsp; every $X_p=X^i(p)\,\partial_i|_p$ &nbsp; with &nbsp; $X^i(p)=X_p(x^i)$.

            > > $\partial_i|_p\longleftrightarrow[t\mapsto\varphi^{-1}(\varphi(p)+t\,e_i)]$

            > > > $\leadsto$ &nbsp; velocity with respect to $\varphi$ $=e_i$
            """,
        ),
        lk.aside(
            r"$\leadsto$ &nbsp; working with manifolds $M$, in place of affine spaces $(\mathbb A,\mathbb V,-)$,<br>the tangent space <span class='lk-mark'>$T_pM$</span> takes the place of the vector space $\mathbb V$",
            "each point has its own vector space!",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals("Vector fields", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("Carroll 2.3; Sasane Ch. 3")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: vector fields
    # definition: vector field, its local components, smoothness
    lk.definition(
        [
            r"A **vector field** on $M$ is an assignment of a tangent vector to each point $p\in M$",
            lk.aside(
                r"$$X:p\in M\longmapsto \mk{X_p}\in T_pM=\mathrm{Der}_p(M).$$",
                r"can be viewed as a velocity vector<br>or as a derivation at $p$",
            ),
            r"With respect to a chart &nbsp; $\varphi:U\subseteq M\to\mathbb R^m$",
            lk.aside(
                r"> $p=\varphi^{-1}(\mk{x^i(p)}\,e_i)$",
                r"local coordinates of $p$ with respect to $\varphi$<br>$\leadsto$ local coordinates of $\varphi$: &nbsp;$x^i:U\subseteq M\to\mathbb R$",
            ),
            lk.aside(
                r"> $X_p=\mk{X^i(p)}\,\partial_i|_p$",
                r"local components of $X_p$ with respect to $\varphi$<br>$\leadsto$ local components of $X$: &nbsp;$X^i:U\subseteq M\to\mathbb R$",
            ),
            r"""
            A vector field $X$ is called **smooth** if all of its local components $X^i:U\subseteq M\to\mathbb R$

            with respect to all charts $\varphi:U\subseteq M\to\mathbb R^m$ are smooth
            """,
        ],
        label="def-vector-field",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: vector fields
    # example: a vector field on the sphere in the two stereographic charts, and in spherical coordinates
    lk.example(
        [
            r"$\mathbb S^2$ &nbsp; $\varphi_n(x,y,z)=\Big(\dfrac{x}{1-z},\ \dfrac{y}{1-z}\Big)=(u,v)$",
            r"<span class='lk-ghost'>$\mathbb S^2$ &nbsp;</span> $\varphi_s(x,y,z)=\Big(\dfrac{x}{1+z},\ \dfrac{y}{1+z}\Big)=(\tilde u,\tilde v)$",
            lk.aside(
                r"$$X:p=(x,y,z)\longmapsto X_p=\begin{cases}-v(p)\,\partial_u|_p+u(p)\,\partial_v|_p,&p\neq(0,0,1),\\[0.3em]-\tilde v(p)\,\partial_{\tilde u}|_p+\tilde u(p)\,\partial_{\tilde v}|_p,&p\neq(0,0,-1)\end{cases}$$",
                [(1, r"not defined for $p=n$"), (2.2, r"defined for $p=n$, not defined for $p=s$<br>must agree on $\mathbb S^2-\{n,s\}$")],
                rows=2,
            ),
            r"Given &nbsp; $f\in C^\infty(\mathbb S^2,\mathbb R)$",
            r"""
            $$
            \begin{aligned}
            X_p(f)&=-v(p)\,\partial_u|_pf+u(p)\,\partial_v|_pf\\[0.3em]
            &=-v(p)\frac{\partial}{\partial u}(f\circ\varphi_n^{-1})\Big|_{\varphi_n(p)}+u(p)\frac{\partial}{\partial v}(f\circ\varphi_n^{-1})\Big|_{\varphi_n(p)}\\[0.3em]
            &=-\tilde v(p)\frac{\partial}{\partial\tilde u}(f\circ\varphi_s^{-1})\Big|_{\varphi_s(p)}+\tilde u(p)\frac{\partial}{\partial\tilde v}(f\circ\varphi_s^{-1})\Big|_{\varphi_s(p)}.
            \end{aligned}
            $$

            > $\leadsto$ &nbsp; do these agree? yes!

            $\varphi_s\circ\varphi_n^{-1}(u,v)=\Big(\dfrac{u}{u^2+v^2},\ \dfrac{v}{u^2+v^2}\Big)=\big(\tilde u(u,v),\ \tilde v(u,v)\big)$

            > $\displaystyle\begin{alignedat}{2}\Longrightarrow\quad&\frac{\partial}{\partial u}(f\circ\varphi_n^{-1})&&=\frac{\partial}{\partial u}(f\circ\varphi_s^{-1}\circ\varphi_s\circ\varphi_n^{-1})\\[0.3em]&&&=\frac{\partial}{\partial\tilde u}(f\circ\varphi_s^{-1})\frac{\partial\tilde u}{\partial u}+\frac{\partial}{\partial\tilde v}(f\circ\varphi_s^{-1})\frac{\partial\tilde v}{\partial u}\\[0.3em]&&&=\frac{-u^2+v^2}{(u^2+v^2)^2}\frac{\partial}{\partial\tilde u}(f\circ\varphi_s^{-1})+\frac{-2uv}{(u^2+v^2)^2}\frac{\partial}{\partial\tilde v}(f\circ\varphi_s^{-1})\\[0.6em]&\frac{\partial}{\partial v}(f\circ\varphi_n^{-1})&&=\frac{-2uv}{(u^2+v^2)^2}\frac{\partial}{\partial\tilde u}(f\circ\varphi_s^{-1})+\frac{u^2-v^2}{(u^2+v^2)^2}\frac{\partial}{\partial\tilde v}(f\circ\varphi_s^{-1})\end{alignedat}$

            > > $\displaystyle\Longrightarrow\quad-v\frac{\partial}{\partial u}(f\circ\varphi_n^{-1})+u\frac{\partial}{\partial v}(f\circ\varphi_n^{-1})=\underbrace{\frac{-v(u^2+v^2)}{(u^2+v^2)^2}}_{\footnotesize=-\tilde v}\frac{\partial}{\partial\tilde u}(f\circ\varphi_s^{-1})+\underbrace{\frac{u(u^2+v^2)}{(u^2+v^2)^2}}_{\footnotesize=\tilde u}\frac{\partial}{\partial\tilde v}(f\circ\varphi_s^{-1})$
            """,
            lk.gap(),
            r"""
            $\Longrightarrow$ &nbsp; $X:p\longmapsto X_p=\begin{cases}-v(p)\,\partial_u|_p+u(p)\,\partial_v|_p,&p\neq n,\\-\tilde v(p)\,\partial_{\tilde u}|_p+\tilde u(p)\,\partial_{\tilde v}|_p,&p\neq s\end{cases}$

            > is well-defined and it is smooth since

            > > $\begin{aligned}X^u&=-v:\mathbb S^2-\{n\}\to\mathbb R\\X^v&=u:\mathbb S^2-\{n\}\to\mathbb R\\X^{\tilde u}&=-\tilde v:\mathbb S^2-\{s\}\to\mathbb R\\X^{\tilde v}&=\tilde u:\mathbb S^2-\{s\}\to\mathbb R\end{aligned}$ &nbsp;&nbsp; are all smooth!
            """,
            lk.gap(),
            r"""
            $\leadsto$ &nbsp; what about other charts?

            > $\psi:\mathbb S^2-\underbrace{\{\text{arc of great circle from }n\text{ to }s\}}_{\footnotesize x\geq0,\ y=0}\longrightarrow(0,\pi)\times(0,2\pi)$

            > $$
            > \begin{aligned}
            > \varphi_n\circ\psi^{-1}(\phi,\theta)&=\varphi_n(\cos\theta\sin\phi,\ \sin\theta\sin\phi,\ \cos\phi)\\[0.3em]
            > &=\big(\cot\tfrac{\phi}{2}\cos\theta,\ \cot\tfrac{\phi}{2}\sin\theta\big)=\big(u(\phi,\theta),\ v(\phi,\theta)\big)
            > \end{aligned}
            > $$
            """,
            lk.aside(
                r"> > $\Longrightarrow$ &nbsp; $X:p\longmapsto X_p=\partial_\theta|_p$",
                r"smooth components due to smoothness of $\varphi_n\circ\psi^{-1}$",
            ),
        ],
        label="ex-sphere-rotation-field",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: vector fields as operators
    # remark: X(f)
    lk.remark(
        [
            r"Given a vector field $X$ and a smooth function $f$ we can define another function $X(f):M\to\mathbb R$ via",
            lk.aside(r"$$X(f)(p)=X_p(f).$$", r"well-defined since $f$ smooth"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: vector fields as operators
    # theorem: smooth vector fields are linear differential operators
    lk.theorem(
        [
            r"A vector field $X:p\longmapsto X_p$ is smooth iff it defines a linear differential operator on $M$",
            r"$$X:C^\infty(M,\mathbb R)\longrightarrow C^\infty(M,\mathbb R),\qquad\underset{\text{smooth}}{f}\longmapsto\underset{\text{smooth}}{X(f)}:p\longmapsto X_p(f).$$",
            r"$\leadsto$ &nbsp; in a chart &nbsp; $\varphi:U\subseteq M\to\mathbb R^m$",
            lk.aside(
                r"> $X(f)\circ\varphi^{-1}=\mk{X^i\circ\varphi^{-1}\,\dfrac{\partial}{\partial x^i}(f\circ\varphi^{-1})}$",
                r"smooth $\Longleftrightarrow$ $X^i\circ\varphi^{-1}$ is smooth $\forall\,i$",
            ),
        ],
        label="thm-vector-fields-operators",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: vector fields as operators
    # definition: the space of smooth vector fields
    lk.definition(
        [
            r"The space of smooth vector fields on $M$ is denoted",
            lk.aside(
                r"$$\Gamma(\mk{TM})=\text{space of smooth vector fields }X:C^\infty(M,\mathbb R)\to C^\infty(M,\mathbb R).$$",
                r"denotes the “collection” of all tangent<br>spaces of $M$ (the tangent bundle of $M$)",
            ),
        ],
        label="def-gamma-tm",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: vector fields as operators
    # remark: local basis
    lk.remark(
        [
            r"In terms of a chart &nbsp; $\varphi:U\subseteq M\to\mathbb R^m$",
            lk.aside(r"> $X=X^i\,\partial_i$ &nbsp; where &nbsp; $X^i:U\subseteq M\to\mathbb R$", r"local function on $U$"),
            lk.aside(
                r"> <span class='lk-ghost'>$X=X^i\,\partial_i$ &nbsp;</span> and &nbsp; $\mk{\partial_i}\in\Gamma(TM)|_U$",
                r"local vector field on $U$<br>form a “local basis” of vector fields on $U$<br>$\leadsto$ plays the role of $e_i\in\mathbb R^m$ over $U$",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: integral curves
    # definition: vector field along a path
    lk.definition(
        r"""
        Given a smooth path $\gamma:\mathbb R\to M$, a **vector field along** $\gamma$ is an assignment

        $$
        X:t\in\mathbb R\longmapsto X_{\gamma(t)}\in T_{\gamma(t)}M,
        $$

        of a tangent vector at $\gamma(t)$ for each $t\in\mathbb R$
        """,
        label="def-field-along",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: integral curves
    # example: velocity vector field
    lk.example(
        r"""
        The velocity vector field of $\gamma:\mathbb R\to M$ (smooth) is the assignment &nbsp; $\gamma':t\in\mathbb R\longmapsto\gamma'(t)\in T_{\gamma(t)}M$ &nbsp; such that

        $$
        \gamma'(t)(f)=(f\circ\gamma)'(t).
        $$

        > $\leadsto$ &nbsp; with respect to a chart $\varphi$: &nbsp; $\gamma'(t)=(x^i\circ\gamma)'(t)\,\partial_i|_{\gamma(t)}$
        """,
        label="ex-velocity-field",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: integral curves
    # definition: integral curve
    lk.definition(
        [
            r"Given a vector field $X\in\Gamma(TM)$, a path $\gamma:\mathbb R\to M$ is an **integral curve** of $X$ if",
            lk.aside(r"$$\gamma'(t)=X_{\gamma(t)}\qquad\forall\,t\in\mathbb R.$$", "the velocity vector equals<br>the vector field along $\\gamma$"),
            lk.aside(r"> $\leadsto$ &nbsp; with respect to a chart $\varphi$: &nbsp; $(x^i\circ\gamma)'(t)=X^i(\gamma(t))$", "1st order system of ODEs!"),
        ],
        label="def-integral-curve",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: integral curves
    # theorem: existence and uniqueness
    lk.theorem(
        [
            lk.aside(r"For each $p\in M$, there exists a unique integral curve $\gamma:I\to M$ of $X\in\Gamma(TM)$", "$I\\subseteq\\mathbb R$ the maximal open interval with $0\\in I$"),
            lk.aside(r"such that &nbsp; $\mk{\gamma(0)=p}$", "initial condition"),
            r"> $\leadsto$ &nbsp; $\begin{cases}\gamma'(t)=X_{\gamma(t)}\\\gamma(0)=p\end{cases}$ &nbsp; is a 1st order IVP on $M$",
        ],
        label="thm-integral-curves",
    )
    return


@app.cell(hide_code=True)
def _(curve_chart, lk, mo, s_t, s_u0, s_v0):
    # module: integral curves
    # example: integral curves of the rotation field of the sphere
    lk.example(
        [
            r"on $\mathbb S^2$, &nbsp; $X=\begin{cases}-v\,\partial_u+u\,\partial_v,&\text{on }\mathbb S^2-\{n\},\\-\tilde v\,\partial_{\tilde u}+\tilde u\,\partial_{\tilde v},&\text{on }\mathbb S^2-\{s\}\end{cases}$",
            r"""
            > $\gamma:\mathbb R\to\mathbb S^2$ &nbsp; integral curve of $X$

            > > $\displaystyle\begin{alignedat}{1}\Longleftrightarrow\quad&\gamma'(t)=X(\gamma(t))\\[0.3em]\Longleftrightarrow\quad&(\varphi\circ\gamma)'(t)=X^i(\gamma(t))\,e_i\\[0.3em]&\begin{bmatrix}u'(t)\\v'(t)\end{bmatrix}=\begin{bmatrix}-v(t)\\u(t)\end{bmatrix}\\[0.3em]\Longleftrightarrow\quad&\begin{bmatrix}u(t)\\v(t)\end{bmatrix}=\begin{bmatrix}u_0\cos(t)-v_0\sin(t)\\u_0\sin(t)+v_0\cos(t)\end{bmatrix}\\[0.3em]\Longleftrightarrow\quad&\gamma(t)=\varphi^{-1}\Big(\begin{bmatrix}u_0\cos(t)-v_0\sin(t)\\u_0\sin(t)+v_0\cos(t)\end{bmatrix}\Big)\end{alignedat}$
            """,
            lk.interactive(
                mo.hstack([lk.frame("L11-curve", 340), curve_chart(s_u0.value, s_v0.value, s_t.value)], justify="center", align="center", gap=2),
                controls=[s_u0, s_v0, s_t],
            ),
        ],
        label="ex-rotation-curves",
    )
    return


@app.cell(hide_code=True)
def _(bundle_scene, lk):
    # module: tangent bundle
    # definition: tangent bundle
    lk.module(
        lk.definition(
            [
                r"The **tangent bundle** of an $m$-manifold $M$ is",
                lk.aside(
                    r"$$\begin{aligned}TM&=\text{the collection of all tangent spaces}\\[0.3em]&\mathrel{\text{“}{=}\text{”}}\bigcup_{p\in M}T_pM\\[0.3em]&=\{(p,\mk{X_p})\mid p\in M,\ X_p\in T_pM\}.\end{aligned}$$",
                    [(3, r"this notation is better than $[\gamma]$<br>equivalence class of paths with same velocity at $p$<br>derivations at $p$")],
                    rows=3,
                ),
            ],
            label="def-tangent-bundle",
        ),
        lk.prose(lk.figure(bundle_scene())),
    )
    return


if __name__ == "__main__":
    app.run()
