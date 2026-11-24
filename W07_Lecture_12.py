import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 12 · Review: calculus on manifolds", css_file="lecturekit/style.css")


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
    lk.lecture(12, "Review: calculus on manifolds")
    return


@app.cell(hide_code=True)
def _(Figure, lk, math, np):
    # Helpers of this lecture: the five figures

    def _blank(w, h, xlim, ylim):
        fig = Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def derivative_figure():
        # the derivative of f at p computed through a chart (shared sketch style, lk.sk)
        sk = lk.sk
        fig, ax = sk.sketch((-0.8, 15.0), (-1.2, 8.2))
        sk.outline(ax, sk.shape(3.4, 5.4, 3.2, 2.3, egg=-0.04, bean=0.04), name="$M$", at=(0.4, 7.4))
        sk.outline(ax, sk.shape(3.4, 5.2, 1.85, 1.35), lk.GREY, "$U$", (1.2, 5.2), tint=False)
        P = (3.3, 5.35)
        ax.plot(*sk.path(P, (1, 0.5), -0.3, np.linspace(-0.3, 0.95, 60)), color=lk.BLUE, lw=sk.LW, zorder=4)
        sk.maps(ax, P, (P[0] + 1.0, P[1] + 0.5), color=lk.GREEN, lw=1.8)
        sk.dot(ax, P, r"$p = \varphi^{-1}(x)$", at=(0, -0.3))
        sk.label(ax, (3.4, 6.95), r"$[\gamma] = v^i \partial_i|_p = \gamma'(0)$", lk.GREEN, size=13)
        sk.chart(ax, 10.0, 3.6, 3.8, 3.2, lk.GREY, "$V$", where="above")
        Q = (11.4, 4.9)
        sk.maps(ax, Q, (Q[0] + 1.0, Q[1] + 0.6), color=lk.GREEN, lw=1.8)
        sk.dot(ax, Q, r"$x = \varphi(p)$", at=(0.3, -0.35))
        sk.label(ax, (12.55, 5.25), "$v$", lk.GREEN, ha="left", va="top")
        sk.maps(ax, (6.8, 6.4), (9.8, 6.4), r"$\varphi$", bend=0.2, side=1)
        ax.plot([0.4, 7.0], [0.4, 0.4], color=sk.INK, lw=1.2)
        sk.label(ax, (7.2, 0.4), r"$\mathbb{R}$", ha="left")
        sk.maps(ax, (3.4, 0.4), (5.2, 0.4), color=lk.GREEN, lw=1.8)
        sk.dot(ax, (3.4, 0.4), r"$f(p) = f \circ \varphi^{-1}(x)$", at=(0, -0.3))
        sk.label(ax, (4.3, 0.75), r"$Df(p)[\gamma]$", lk.GREEN, va="bottom", size=13)
        sk.maps(ax, (2.6, 3.0), (2.6, 1.1), "$f$", lk.BLUE, side=1)
        sk.maps(ax, (10.6, 3.4), (6.0, 0.9), r"$f \circ \varphi^{-1}$", lk.RED, bend=-0.2, side=-1, gap=0.45)
        return fig

    def height_figure(u, v, a, b):
        # z(t) along gamma(t) = phi_n^-1(u + ta, v + tb), with its tangent line at t = 0, of slope Dz(u, v)(a, b)
        r = 1 + u**2 + v**2
        slope = a * 4 * u / r**2 + b * 4 * v / r**2 + 0.0
        z0 = (r - 2) / r
        t = np.linspace(-1.5, 1.5, 300)
        q = (u + t * a) ** 2 + (v + t * b) ** 2
        fig = Figure(figsize=(5.6, 3.0), layout="constrained")
        ax = fig.subplots()
        ax.plot(t, (q - 1) / (q + 1), color=lk.BLUE)
        ax.plot(t, z0 + slope * t, color=lk.GREEN, dashes=(5, 3))
        ax.plot(0, z0, "o", color="#000000", ms=5)
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.1, 1.1)
        ax.axhline(0, color="#000000", lw=0.6)
        ax.axvline(0, color="#000000", lw=0.6)
        ax.set_xlabel("$t$")
        ax.set_xticks([-1, 0, 1])
        ax.set_yticks([-1, 0, 1])
        ax.text(0, 1.03, r"$z(t)$", color=lk.BLUE, fontsize=12, transform=ax.transAxes, va="bottom")
        ax.text(1, 1.03, r"slope $Dz(u, v)(a, b)$", color=lk.GREEN, fontsize=12, transform=ax.transAxes, ha="right", va="bottom")
        return fig

    FIELDS = {
        "∂_u": (lambda A, B: (1 + 0 * A, 0 * A), lambda A, B: (-(A**2 - B**2), -2 * A * B)),
        "∂_ṽ": (lambda A, B: (-2 * A * B, A**2 - B**2), lambda A, B: (0 * A, 1 + 0 * A)),
        "−v ∂_u + u ∂_v": (lambda A, B: (-B, A), lambda A, B: (-B, A)),
    }

    def charts_figure(name):
        # a vector field of S^2 drawn in the two stereographic charts
        g = np.linspace(-2.0, 2.0, 11)
        A, B = np.meshgrid(g, g)
        fig = Figure(figsize=(lk.FULL, 3.7), layout="constrained")
        axes = fig.subplots(1, 2)
        c = np.linspace(0, 2 * np.pi, 200)
        for ax, field, title, pole in zip(axes, FIELDS[name], (r"$\varphi_n = (u, v)$", r"$\varphi_s = (\tilde{u}, \tilde{v})$"), ("$s$", "$n$")):
            P, Q = np.broadcast_arrays(*field(A, B))
            ax.set_title(title, fontsize=13)
            ax.set_xlim(-2.5, 2.5)
            ax.set_ylim(-2.5, 2.5)
            ax.set_aspect("equal")
            ax.axhline(0, color="#000000", lw=0.5)
            ax.axvline(0, color="#000000", lw=0.5)
            ax.plot(np.cos(c), np.sin(c), color=lk.GREY, lw=1.0)
            ax.text(0.9, -1.0, "equator", color=lk.GREY, fontsize=11, ha="center", va="center")
            ax.plot(0, 0, "o", color="#000000", ms=3)
            ax.text(0.08, -0.1, pole, fontsize=12, va="top")  # the pole at the origin of this chart
            m = max(float(np.max(np.hypot(P, Q))), 1e-9)
            for a0, b0, p0, q0 in zip(A.ravel(), B.ravel(), P.ravel(), Q.ravel()):  # arrows scaled per panel
                if p0 or q0:
                    lk.arrow(ax, (a0, b0), (a0 + 0.34 * p0 / m, b0 + 0.34 * q0 / m), lk.BLUE, lw=1.0)
            ax.set_xticks([-2, 0, 2])
            ax.set_yticks([-2, 0, 2])
        return fig

    def integral_curve_figure():
        # a vector field and one of its integral curves
        fig, ax = _blank(lk.HALF, 2.3, (-0.2, 4.2), (-0.2, 2.4))
        X, Y = np.meshgrid(np.linspace(0.2, 3.8, 6), np.linspace(0.1, 2.2, 4))
        U, V = 0.45 + 0 * X, 0.22 * np.cos(1.2 * X) + 0.05 * Y
        for x, y, dx, dy in zip(X.ravel(), Y.ravel(), U.ravel(), V.ravel()):
            lk.arrow(ax, (x, y), (x + dx, y + dy), lk.BLUE, lw=0.9)
        f = lambda x, y: (0.45, 0.22 * np.cos(1.2 * x) + 0.05 * y)
        xs, ys = [0.3], [0.9]
        for _ in range(360):  # the integral curve by Euler steps
            dx, dy = f(xs[-1], ys[-1])
            xs.append(xs[-1] + 0.022 * dx)
            ys.append(ys[-1] + 0.022 * dy)
        ax.plot(xs, ys, color=lk.RED)
        x0, y0 = xs[150], ys[150]
        dx, dy = f(x0, y0)
        lk.arrow(ax, (x0, y0), (x0 + 1.4 * dx, y0 + 1.4 * dy), lk.GREEN, lw=1.1)
        ax.plot(x0, y0, "o", color="#000000", ms=4)
        ax.text(x0 + 0.05, y0 - 0.3, r"$\gamma(t)$", fontsize=12)
        ax.text(x0 + 1.4 * dx + 0.06, y0 + 1.4 * dy, r"$X_{\gamma(t)}$", color=lk.GREEN, fontsize=12, ha="left", va="center", zorder=8)
        return fig

    def _inv(u, v):
        r = 1 + u**2 + v**2
        return 2 * u / r, 2 * v / r, (r - 2) / r

    def _curve_parts(rot, u0, v0, t):
        s = np.linspace(min(0.0, t), max(0.0, t), 200)
        w = np.linspace(-np.pi, np.pi, 400) if rot else np.linspace(-3.0, 3.0, 400)  # the whole curve: one period, or the window of t
        sol = (lambda s: (u0 * np.cos(s) - v0 * np.sin(s), u0 * np.sin(s) + v0 * np.cos(s))) if rot else (lambda s: (u0 * np.exp(s), v0 * np.exp(s)))
        return sol(s), sol(w), tuple(float(a) + 0.0 for a in sol(t))

    def curves_scene(rot, u0, v0, t, key):
        # the field on a few latitudes of the sphere and the integral curve from gamma(0) to gamma(t)
        vec3 = (lambda x, y, z: (-y, x, 0 * z)) if rot else (lambda x, y, z: (-x * z, -y * z, 1 - z**2))  # u d_u + v d_v in ambient coordinates
        (us, vs), (uw, vw), (ut, vt) = _curve_parts(rot, u0, v0, t)
        s_, t_ = np.meshgrid(np.linspace(0, np.pi, 37), np.linspace(0, 2 * np.pi, 73), indexing="ij")
        sphere = lk.sheet(np.sin(s_) * np.cos(t_), np.sin(s_) * np.sin(t_), np.cos(s_))  # opaque: the vectors on the far side stay hidden
        arrows = []
        for z in (-0.75, -0.4, 0.0, 0.4, 0.75):
            rr = math.sqrt(1 - z**2)
            for a in np.linspace(0, 2 * np.pi, 12, endpoint=False):
                q = (rr * math.cos(a), rr * math.sin(a), z)
                d = vec3(*q)
                arrows.append((q, (q[0] + 0.22 * d[0], q[1] + 0.22 * d[1], q[2] + 0.22 * d[2]), lk.BLUE, 1.2))
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
            key=key,
            apart=True,
            bias=0.12,
        )

    def curves_chart(rot, u0, v0, t):
        # the same curve and field in the chart phi_n
        field = (lambda u, v: (-v, u)) if rot else (lambda u, v: (u, v))
        (us, vs), (uw, vw), (ut, vt) = _curve_parts(rot, u0, v0, t)
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
        U, V = np.meshgrid(g, g)
        FP, FQ = np.broadcast_arrays(*field(U, V))
        for a0, b0, p0, q0 in zip(U.ravel(), V.ravel(), FP.ravel(), FQ.ravel()):
            if p0 or q0:
                lk.arrow(ax, (a0, b0), (a0 + p0 / 5, b0 + q0 / 5), lk.BLUE, lw=1.0)
        ax.plot(np.cos(c), np.sin(c), color=lk.GREY, lw=1.0)
        ax.text(-0.83, -0.83, "equator", color=lk.GREY, fontsize=10, ha="center", va="center", rotation=-45, rotation_mode="anchor")
        ax.plot(uw, vw, color=lk.RED, lw=0.9)
        ax.plot(us, vs, color=lk.RED)
        ax.plot(u0, v0, "o", color=lk.RED, mfc="white", ms=6)
        ax.plot(ut, vt, "o", color=lk.RED, ms=6, clip_on=True)
        # names on fixed sides of the curve so that they never meet: on a latitude gamma(0) inside the circle and
        # gamma(t) outside it; on a meridian gamma(0) right of the ray and gamma(t) left of it
        al = math.atan2(v0, u0)
        small = math.hypot(u0, v0) < 0.3
        for (px, py), an, fix, name in (((u0, v0), al + (math.pi if rot else -math.pi / 2), (-18, 12), r"$\gamma(0)$"), ((ut, vt), al + (t if rot else math.pi / 2), (18, -12), r"$\gamma(t)$")):
            dx, dy = math.cos(an), math.sin(an)
            off = 9 * abs(dx) + 5.5 * abs(dy) + 4
            ax.annotate(name, (px, py), textcoords="offset points", xytext=fix if small else (off * dx, off * dy), ha="center", va="center", color="#000000", fontsize=11, annotation_clip=True, zorder=8).set_in_layout(False)
        ax.set_xticks([-3, 0, 3])
        ax.set_yticks([-3, 0, 3])
        return fig

    return FIELDS, charts_figure, curves_chart, curves_scene, derivative_figure, height_figure, integral_curve_figure


@app.cell(hide_code=True)
def _(FIELDS, lk, mo):
    # Controls of the interactive figures
    s_u = lk.slider(-2.0, 2.0, step=0.1, value=1.0, label="$u$", show_value=False)
    s_v = lk.slider(-2.0, 2.0, step=0.1, value=0.5, label="$v$", show_value=False)
    s_a = lk.slider(-1.0, 1.0, step=0.1, value=1.0, label="$a$", show_value=False)
    s_b = lk.slider(-1.0, 1.0, step=0.1, value=0.5, label="$b$", show_value=False)
    d_field = mo.ui.dropdown(options=list(FIELDS), value="∂_u", label="$X$", allow_select_none=False)
    lat_u0 = lk.slider(-1.5, 1.5, step=0.1, value=1.4, label="$u_0$", show_value=False)
    lat_v0 = lk.slider(-1.5, 1.5, step=0.1, value=0.5, label="$v_0$", show_value=False)
    lat_t = lk.slider(-3.0, 3.0, step=0.05, value=1.0, label="$t$", show_value=False)
    mer_u0 = lk.slider(-1.5, 1.5, step=0.1, value=0.6, label="$u_0$", show_value=False)
    mer_v0 = lk.slider(-1.5, 1.5, step=0.1, value=0.3, label="$v_0$", show_value=False)
    mer_t = lk.slider(-3.0, 3.0, step=0.05, value=1.0, label="$t$", show_value=False)
    return d_field, lat_t, lat_u0, lat_v0, mer_t, mer_u0, mer_v0, s_a, s_b, s_u, s_v


@app.cell(hide_code=True)
def _(curves_scene, lat_t, lat_u0, lat_v0):
    # the scene of the latitudes figure, in place by its sliders
    curves_scene(True, lat_u0.value, lat_v0.value, lat_t.value, "L12-latitudes")
    return


@app.cell(hide_code=True)
def _(curves_scene, mer_t, mer_u0, mer_v0):
    # the scene of the meridians figure, in place by its sliders
    curves_scene(False, mer_u0.value, mer_v0.value, mer_t.value, "L12-meridians")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: references
    # references
    lk.references("Schutz 6.1; Carroll 2.2–2.3; Sasane Ch. 1–3")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: manifolds
    # recall: manifolds
    lk.recall(
        [
            r"Let's take a few steps back …",
            lk.gap(),
            r"**Manifolds**: &nbsp; set of points $p\in M$",
            r"> with local charts &nbsp; $\varphi:U\subseteq M\to V\subseteq\mathbb R^m$",
            lk.aside(
                r"> > such that &nbsp; $\tilde\varphi\circ\varphi^{-1}:V\xrightarrow{\ \sim\ }\tilde V$ &nbsp; is <span class='lk-mark'>smooth with smooth inverse</span> &nbsp; $\forall\,\tilde\varphi,\varphi$",
                "diffeomorphism",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: manifolds
    # charts, local coordinates, local parameterizations
    lk.prose(
        r"""
        A chart &nbsp; $\varphi:U\subseteq M\to V\subseteq\mathbb R^m$ &nbsp; is the same as

        > $p\longmapsto\varphi(p)=x^i(p)\,e_i=\begin{bmatrix}x^1(p)\\\vdots\\x^m(p)\end{bmatrix}$

        > • &nbsp; local coordinates &nbsp; $x^i:U\subseteq M\to\mathbb R$, &nbsp; $p\longmapsto x^i(p)$

        > • &nbsp; local parameterizations &nbsp; $\varphi^{-1}:V\to U\subseteq M$, &nbsp; $x\longmapsto\varphi^{-1}(x)=“p(x)”$
        """,
        lk.gap(),
        lk.aside(
            r"The map &nbsp; $\tilde\varphi\circ\varphi^{-1}:V\to\tilde V$ &nbsp; is the change of <span class='lk-mark'>charts</span>",
            "change of coordinates<br>change of parameterization",
        ),
        r"""
        > $x\longmapsto\tilde x=\underbrace{\tilde\varphi\circ\varphi^{-1}(x)}_{\footnotesize\tilde x(x)}$

        $\tilde\varphi\circ\varphi^{-1}$ diffeomorphism &nbsp; $\Longleftrightarrow$ &nbsp; Jacobian matrix &nbsp; $\displaystyle\frac{\partial\tilde x}{\partial x}(x)=\Big[\frac{\partial\tilde x^j}{\partial x^i}(x)\Big]$

        <span class="lk-ghost">$\tilde\varphi\circ\varphi^{-1}$ diffeomorphism &nbsp; $\Longleftrightarrow$ &nbsp;</span> is invertible and varies smoothly &nbsp; $\forall\,x\in\varphi(U\cap\tilde U)\subseteq V$
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: manifolds
    # example: the stereographic charts of the sphere
    lk.example(
        [
            r"$\mathbb S^2$",
            r"""
            > $\varphi_n(x,y,z)=\Big(\dfrac{x}{1-z},\ \dfrac{y}{1-z}\Big)=\big(u(x,y,z),\ v(x,y,z)\big)$

            > > $\leadsto$ &nbsp; $\varphi_n^{-1}(u,v)=\Big(\dfrac{2u}{1+u^2+v^2},\ \dfrac{2v}{1+u^2+v^2},\ \dfrac{-1+u^2+v^2}{1+u^2+v^2}\Big)=(x,y,z)$

            > $\varphi_s(x,y,z)=\Big(\dfrac{x}{1+z},\ \dfrac{y}{1+z}\Big)=\big(\tilde u(x,y,z),\ \tilde v(x,y,z)\big)$

            > > $\leadsto$ &nbsp; $\varphi_s^{-1}(\tilde u,\tilde v)=\Big(\dfrac{2\tilde u}{1+\tilde u^2+\tilde v^2},\ \dfrac{2\tilde v}{1+\tilde u^2+\tilde v^2},\ \dfrac{1-\tilde u^2-\tilde v^2}{1+\tilde u^2+\tilde v^2}\Big)=(x,y,z)$
            """,
            lk.gap(),
            lk.aside(
                r"> $(\tilde u,\tilde v)=\varphi_s\circ\varphi_n^{-1}(u,v)=\Big(\dfrac{u}{u^2+v^2},\ \dfrac{v}{u^2+v^2}\Big)$",
                r"smooth with smooth inverse<br>$\forall\,(u,v)\neq(0,0)$",
            ),
            lk.aside(
                r"> $\dfrac{\partial(\tilde u,\tilde v)}{\partial(u,v)}=\dfrac{1}{(u^2+v^2)^2}\begin{bmatrix}-u^2+v^2&-2uv\\-2uv&u^2-v^2\end{bmatrix}$",
                r"invertible matrix<br>smooth $\forall\,(u,v)\neq(0,0)$",
            ),
        ],
        label="ex-stereographic-charts",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    lk.section("Calculus of functions on $M$")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: smooth functions
    # which functions are smooth?
    lk.prose(
        r"**Which functions are smooth?**",
        lk.aside(
            r"$f:M\to\mathbb R$, &nbsp; $p\longmapsto f(p)$ &nbsp; $\overset{\varphi}{\leadsto}$ &nbsp; $\mk{f\circ\varphi^{-1}}:V\subseteq\mathbb R^m\to\mathbb R$, &nbsp; $x\longmapsto f(\varphi^{-1}(x))=f(p(x))$",
            r"local representation of $f$",
        ),
        r"$f$ smooth &nbsp; $\Longleftrightarrow$ &nbsp; $f\circ\varphi^{-1}$ smooth &nbsp; $\forall\,\varphi$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: smooth functions
    # example: a smooth function and a function smooth away from x = 0
    lk.example(
        [
            r"$f:\mathbb S^2\to\mathbb R$, &nbsp; $(x,y,z)\longmapsto z$",
            lk.aside(r"> $f\circ\varphi_n^{-1}(u,v)=\dfrac{-1+u^2+v^2}{1+u^2+v^2}$", r"smooth $\forall\,(u,v)\in\mathbb R^2$"),
            lk.aside(r"> $f\circ\varphi_s^{-1}(\tilde u,\tilde v)=\dfrac{1-\tilde u^2-\tilde v^2}{1+\tilde u^2+\tilde v^2}$", r"smooth $\forall\,(\tilde u,\tilde v)\in\mathbb R^2$"),
            r"> > $\Longrightarrow$ &nbsp; $f$ is smooth!",
            lk.gap(),
            r"$g:\mathbb S^2\to\mathbb R$, &nbsp; $(x,y,z)\longmapsto y/x$",
            lk.aside(r"> $g\circ\varphi_n^{-1}(u,v)=v/u$", r"smooth $\forall\,(u,v)$ with $u\neq0$"),
            lk.aside(r"> $g\circ\varphi_s^{-1}(\tilde u,\tilde v)=\tilde v/\tilde u$", r"smooth $\forall\,(\tilde u,\tilde v)$ with $\tilde u\neq0$"),
            r"> > $\Longrightarrow$ &nbsp; $g$ is smooth $\forall\,(x,y,z)$ with $x\neq0$",
        ],
        label="ex-smooth-functions",
    )
    return


@app.cell(hide_code=True)
def _(derivative_figure, lk):
    # module: derivatives
    # how to compute derivatives?
    lk.prose(
        r"""
        **How to compute derivatives?**

        $f:M\to\mathbb R$ &nbsp; smooth at $p\in M$

        > $\Longrightarrow$ &nbsp; $f\circ\varphi^{-1}:V\subseteq\mathbb R^m\to\mathbb R$ &nbsp; smooth at $x=\varphi(p)$

        > $\Longrightarrow$ &nbsp; $\displaystyle D(f\circ\varphi^{-1})(x)=\Big[\frac{\partial}{\partial x^i}(f\circ\varphi^{-1})(x)\Big]:\mathbb R^m\to\mathbb R$

        > <span class="lk-ghost">$\Longrightarrow$ &nbsp;</span> defines 1st order approximation of $f\circ\varphi^{-1}$ at $x=\varphi(p)$
        """,
        lk.aside(
            r"$$\begin{aligned}(f\circ\varphi^{-1})(x+v)&=f\circ\varphi^{-1}(x)+D(f\circ\varphi^{-1})(x)(v)+\mk{o(v)}\\[0.3em]&=f\circ\varphi^{-1}(x)+v^i\frac{\partial}{\partial x^i}(f\circ\varphi^{-1})(x)+o(v)\end{aligned}$$",
            [(1.5, r"small compared to $v$")],
            rows=2,
        ),
        lk.aside(
            r"$\displaystyle\begin{alignedat}{2}\leadsto\quad&D(f\circ\varphi^{-1})(x)(v)&&=v^i\frac{\partial}{\partial x^i}(f\circ\varphi^{-1})(x)\\[0.3em]&&&=\frac{d}{dt}\Big|_{t=0}(f\circ\varphi^{-1})(x+tv)\\[0.3em]&&&=\frac{d}{dt}\Big|_{t=0}(f\circ\gamma)(t), \quad\text{with }\gamma(t)=\varphi^{-1}(x+tv)\\[0.3em]&&&=v^i\,\mk{\partial_i|_p}f\\[0.3em]&&&=Df(p)([\gamma]), \quad\text{with }[\gamma]=v^i\,\partial_i|_p=\gamma'(0)\\[0.3em]&&&=Df(p)(\gamma'(0))\end{alignedat}$",
            [
                (2, r"directional derivative of $f\circ\varphi^{-1}$<br>at $x$ in the direction of $v\in\mathbb R^m$"),
                (3, r"directional derivative of $f$ at $p$ in the direction of $[\gamma]$<br>$[\gamma]$ only depends on $v$: &nbsp; $\varphi\circ\gamma(0)=x$, &nbsp; $(\varphi\circ\gamma)'(0)=v$"),
                (4, r"basis of $T_pM=\mathrm{Der}_p(M)$"),
            ],
            rows=6,
        ),
        lk.figure(derivative_figure()),
    )
    return


@app.cell(hide_code=True)
def _(height_figure, lk, s_a, s_b, s_u, s_v):
    # module: derivatives
    # example: the derivative of the height function
    lk.example(
        [
            r"$f:\mathbb S^2\to\mathbb R$, &nbsp; $f(x,y,z)=z$",
            lk.aside(
                r"$$\begin{aligned}Dz(u,v)(a,b)&=\Big[\frac{\partial}{\partial u}z(u,v)\ \ \frac{\partial}{\partial v}z(u,v)\Big]\begin{bmatrix}a\\b\end{bmatrix}\\[0.3em]&=\Big[\frac{\partial}{\partial u}\Big(\frac{-1+u^2+v^2}{1+u^2+v^2}\Big)\ \ \frac{\partial}{\partial v}\Big(\frac{-1+u^2+v^2}{1+u^2+v^2}\Big)\Big]\begin{bmatrix}a\\b\end{bmatrix}\\[0.3em]&=a\frac{\partial}{\partial u}\Big(\frac{-1+u^2+v^2}{1+u^2+v^2}\Big)+b\frac{\partial}{\partial v}\Big(\frac{-1+u^2+v^2}{1+u^2+v^2}\Big)\\[0.3em]&=a\mk{\frac{\partial}{\partial u}}z(u,v)+b\mk{\frac{\partial}{\partial v}}z(u,v)\\[0.3em]&=a\,\mk{\partial_u|_{(x,y,z)}}z+b\,\mk{\partial_v|_{(x,y,z)}}z\\[0.3em]&=Dz(x,y,z)(\mk{[\gamma]})\\[0.3em]&=\frac{d}{dt}\Big|_{t=0}z(t)=\frac{d}{dt}\Big|_{t=0}\frac{-1+(u+ta)^2+(v+tb)^2}{1+(u+ta)^2+(v+tb)^2}\end{aligned}$$",
                [
                    (4.65, r"basis of derivations of $\mathbb R^2$ at $(u,v)$"),
                    (5, r"basis of derivations of $M$ at $(x,y,z)=\varphi_n^{-1}(u,v)$"),
                    (6, r"$\gamma(t)=\varphi_n^{-1}(u+ta,v+tb)=(x(t),y(t),z(t))$"),
                ],
                rows=7,
            ),
            lk.interactive(height_figure(s_u.value, s_v.value, s_a.value, s_b.value), controls=[s_u, s_v, s_a, s_b]),
        ],
        label="ex-height-derivative",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: vector fields
    # tangent vectors and vector fields as derivations
    lk.prose(
        r"**Vector fields**",
        r"""
        $\displaystyle\begin{alignedat}{3}&\text{tangent vector }[\gamma]=X_p\in T_pM&\quad\leadsto\quad&X_p:C^\infty(M,\mathbb R)\to\mathbb R,\ \ f\longmapsto X_p(f)&\qquad&\text{linear + Leibniz}\\[0.4em]&\text{smooth vector field }X\in\Gamma(TM)&\quad\leadsto\quad&X:C^\infty(M,\mathbb R)\to C^\infty(M,\mathbb R),\ \ f\longmapsto X(f)&\qquad&\text{linear + Leibniz}\end{alignedat}$

        $X\in\Gamma(TM)$, &nbsp; $f,g\in C^\infty(M,\mathbb R)$, &nbsp; $a,b\in\mathbb R$, &nbsp; $p\in M$

        > $\displaystyle\begin{alignedat}{2}\Longrightarrow\quad&X(af+bg)=a\,X(f)+b\,X(g)\in C^\infty(M,\mathbb R)\\&X(fg)=X(f)\,g+f\,X(g)\in C^\infty(M,\mathbb R)\end{alignedat}$

        > $\Longrightarrow$ &nbsp; $X$ evaluated at $p$ $=X_p\in T_pM$
        """,
        lk.aside(
            r"$\overset{\varphi}{\leadsto}$ &nbsp; $X_p=\mk{v^i}\,\mk{\partial_i|_p}$",
            r"$v^i\in\mathbb R$, &nbsp; $\partial_i|_p$ basis of $T_pM$",
        ),
        lk.aside(
            r"> $\Longrightarrow$ &nbsp; $\displaystyle X=\mk{X^i}\,\mk{\partial_i}=\underbrace{X^i\frac{\partial\tilde x^j}{\partial x^i}}_{\footnotesize\tilde X^j}\tilde\partial_j$",
            r"$X^i\in C^\infty(U,\mathbb R)$<br>$\partial_i$ basis of $\Gamma(TM)$, only on $U\subseteq M$",
        ),
        r"""
        > <span class="lk-ghost">$\Longrightarrow$ &nbsp;</span> where &nbsp; $\tilde x=\tilde\varphi\circ\varphi^{-1}(x)$

        > $\Longrightarrow$ &nbsp; $\displaystyle\partial_i=\frac{\partial\tilde x^j}{\partial x^i}\,\tilde\partial_j$
        """,
    )
    return


@app.cell(hide_code=True)
def _(charts_figure, d_field, lk):
    # module: vector fields
    # example: vector fields on the sphere
    lk.example(
        [
            r"$\partial_u|_{(x,y,z)},\ \partial_v|_{(x,y,z)}$ &nbsp; form a basis of $T_{(x,y,z)}\mathbb S^2$ &nbsp; $\forall\,(x,y,z)\neq(0,0,1)$",
            r"$\partial_{\tilde u}|_{(x,y,z)},\ \partial_{\tilde v}|_{(x,y,z)}$ &nbsp; form a basis of $T_{(x,y,z)}\mathbb S^2$ &nbsp; $\forall\,(x,y,z)\neq(0,0,-1)$",
            lk.gap(),
            r"For &nbsp; $(x,y,z)\neq(0,0,\pm1)$, &nbsp; $(\tilde u,\tilde v)=\Big(\dfrac{u}{u^2+v^2},\ \dfrac{v}{u^2+v^2}\Big)$",
            lk.aside(
                r"$$\begin{aligned}\partial_u&=\frac{\partial\tilde u}{\partial u}\,\partial_{\tilde u}+\frac{\partial\tilde v}{\partial u}\,\partial_{\tilde v}=\frac{-u^2+v^2}{(u^2+v^2)^2}\,\partial_{\tilde u}-\frac{2uv}{(u^2+v^2)^2}\,\partial_{\tilde v}\\[0.3em]&=\underbrace{-(\tilde u^2-\tilde v^2)\,\partial_{\tilde u}-2\tilde u\tilde v\,\partial_{\tilde v}}_{\footnotesize=0\text{ at }(0,0,1)}\\[0.8em]\partial_v&=\frac{\partial\tilde u}{\partial v}\,\partial_{\tilde u}+\frac{\partial\tilde v}{\partial v}\,\partial_{\tilde v}=-\frac{2uv}{(u^2+v^2)^2}\,\partial_{\tilde u}+\frac{u^2-v^2}{(u^2+v^2)^2}\,\partial_{\tilde v}\\[0.3em]&=\underbrace{-2\tilde u\tilde v\,\partial_{\tilde u}+(\tilde u^2-\tilde v^2)\,\partial_{\tilde v}}_{\footnotesize=0\text{ at }(0,0,1)}\end{aligned}$$",
                [(2.5, r"well-defined at $(0,0,1)$<br>but don't form basis!")],
                rows=4,
            ),
            r"$\leadsto$ &nbsp; $X=\begin{cases}\partial_u&\text{for }(x,y,z)\neq(0,0,1)\\0&\text{for }(x,y,z)=(0,0,1)\end{cases}\in\Gamma(TM)$",
            r"$\leadsto$ &nbsp; $X=\begin{cases}\partial_{\tilde v}&\text{for }(x,y,z)\neq(0,0,-1)\\0&\text{for }(x,y,z)=(0,0,-1)\end{cases}\in\Gamma(TM)$",
            lk.aside(
                r"$\leadsto$ &nbsp; $X=\begin{cases}-v\,\partial_u+u\,\partial_v&(x,y,z)\neq(0,0,1)\\-\tilde v\,\partial_{\tilde u}+\tilde u\,\partial_{\tilde v}&(x,y,z)\neq(0,0,-1)\end{cases}\in\Gamma(TM)$",
                r"components agree for $(x,y,z)\neq(0,0,\pm1)$<br>under change of coordinates!",
            ),
            lk.interactive(charts_figure(d_field.value), controls=[d_field]),
        ],
        label="ex-sphere-vector-fields",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: differential equations
    # heading
    lk.prose(r"**Differential equations**")
    return


@app.cell(hide_code=True)
def _(integral_curve_figure, lk):
    # module: differential equations
    # definition: integral curve
    lk.definition(
        [
            r"$X\in\Gamma(TM)$ &nbsp; smooth vector field",
            r"$\gamma:\mathbb R\to M$ &nbsp; smooth path",
            r"> is **integral curve** of $X$ if",
            r"> > $\gamma'(t)=X_{\gamma(t)}$ &nbsp; $\forall\,t\in\mathbb R$",
            lk.figure(integral_curve_figure()),
            r"""
            > > > $\underset{\varphi}{\Longleftrightarrow}$ &nbsp; $\dfrac{d}{dt}\,x^i(t)=X^i(t)$ &nbsp; $\forall\,t,\ \forall\,i$

            > > > <span class="lk-ghost">$\underset{\varphi}{\Longleftrightarrow}$ &nbsp;</span> where &nbsp; $\gamma(t)=\varphi^{-1}(x^i(t)\,e_i)=\tilde\varphi^{-1}(\tilde x^i(t)\,e_i)$

            > > > <span class="lk-ghost">$\underset{\varphi}{\Longleftrightarrow}$ &nbsp; where &nbsp;</span> $X_{\gamma(t)}=X^i(t)\,\partial_i|_{\gamma(t)}=\tilde X^i(t)\,\tilde\partial_i|_{\gamma(t)}$

            > > > $\underset{\tilde\varphi}{\Longleftrightarrow}$ &nbsp; $\dfrac{d}{dt}\,\tilde x^i(t)=\tilde X^i(t)$ &nbsp; $\forall\,t,\ \forall\,i$
            """,
        ],
        label="def-integral-curve",
    )
    return


@app.cell(hide_code=True)
def _(curves_chart, lat_t, lat_u0, lat_v0, lk, mo):
    # module: differential equations
    # example: latitudes
    lk.example(
        [
            r"$X=-v\,\partial_u+u\,\partial_v=-\tilde v\,\partial_{\tilde u}+\tilde u\,\partial_{\tilde v}$",
            r"""
            > $\leadsto$ &nbsp; integral curves

            > > $\begin{cases}u'(t)=-v(t)\\v'(t)=u(t)\end{cases}$ &nbsp; on &nbsp; $\varphi_n(\mathbb S^2-\{(0,0,1)\})$

            > > > $\Longrightarrow$ &nbsp; $\begin{cases}u(t)=u_0\cos(t)-v_0\sin(t)\\v(t)=u_0\sin(t)+v_0\cos(t)\end{cases}$

            > > > $\displaystyle\begin{alignedat}{2}\Longrightarrow\quad&\gamma(t)&&=\varphi_n^{-1}(u(t),v(t))\\&&&=\big(\sin\phi_0\cos(\theta_0+t),\ \sin\phi_0\sin(\theta_0+t),\ \cos\phi_0\big)\end{alignedat}$

            > > > > $\leadsto$ &nbsp; horizontal latitudes around $z$-axis
            """,
            lk.interactive(
                mo.hstack([lk.frame("L12-latitudes", 340), curves_chart(True, lat_u0.value, lat_v0.value, lat_t.value)], justify="center", align="center", gap=2),
                controls=[lat_u0, lat_v0, lat_t],
            ),
        ],
        label="ex-latitudes",
    )
    return


@app.cell(hide_code=True)
def _(curves_chart, lk, mer_t, mer_u0, mer_v0, mo):
    # module: differential equations
    # example: meridians
    lk.example(
        [
            r"$X=u\,\partial_u+v\,\partial_v=-\tilde u\,\partial_{\tilde u}-\tilde v\,\partial_{\tilde v}$",
            r"""
            > $\leadsto$ &nbsp; integral curves

            > > $\begin{cases}u'(t)=u(t)\\v'(t)=v(t)\end{cases}$ &nbsp; on &nbsp; $\varphi_n(\mathbb S^2-\{(0,0,1)\})$

            > > > $\Longrightarrow$ &nbsp; $\begin{cases}u(t)=u_0\,e^t\\v(t)=v_0\,e^t\end{cases}$

            > > > $\displaystyle\begin{alignedat}{2}\Longrightarrow\quad&\gamma(t)&&=\varphi_n^{-1}(u(t),v(t))\\&&&=\big(\operatorname{sech}(t-t_0)\cos\theta_0,\ \operatorname{sech}(t-t_0)\sin\theta_0,\ \tanh(t-t_0)\big)\end{alignedat}$

            > > > > $\leadsto$ &nbsp; vertical meridian from $s$ to $n$
            """,
            lk.interactive(
                mo.hstack([lk.frame("L12-meridians", 340), curves_chart(False, mer_u0.value, mer_v0.value, mer_t.value)], justify="center", align="center", gap=2),
                controls=[mer_u0, mer_v0, mer_t],
            ),
        ],
        label="ex-meridians",
    )
    return


if __name__ == "__main__":
    app.run()
