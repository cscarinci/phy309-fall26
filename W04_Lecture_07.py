import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 07 · Manifolds", css_file="phy309.css")


@app.cell(hide_code=True)
def _():
    import math

    import marimo as mo
    import matplotlib
    import numpy as np
    from matplotlib.figure import Figure
    from matplotlib.patches import Arc

    # Figures use the same Computer Modern typeface as the text
    matplotlib.rcParams.update({"font.size": 14, "font.family": "serif", "font.serif": ["cmr10", "DejaVu Serif"], "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True, "axes.unicode_minus": False})

    return Arc, Figure, math, mo, np


@app.cell(hide_code=True)
def _(mo):
    # ---- Building blocks shared by all lectures -------------------------
    # Palette with fixed roles (figures only; text carries no colour):
    #   BLUE   the primary object (the particle, the point, the chosen vector)
    #   RED    the second object it is compared with
    #   GREEN  a derived quantity (velocity, relative velocity, tangent vector)
    #   ORANGE a third series, only when three are needed
    #   GREY   reference geometry (equator, light cone, inertial comparison)
    #   LIGHT  fills and grids
    BLUE, RED, GREEN, ORANGE, GREY, LIGHT = "#1b458f", "#b3261e", "#2e7d32", "#e65100", "#888888", "#cfe3f5"
    # Figure widths: FULL spans the page, HALF sits beside text or in a pair
    FULL, HALF = 7.4, 3.6

    def header(document, date, running=""):
        """Course header, as on the exercise sheets and exams."""
        return mo.Html(
            f"""
    <div class="bs-head">
      <div class="bs-running">PHY309 &bull; {running}</div>
      <div class="bs-title">Differential Geometry<br>and General Relativity</div>
      <div class="bs-inst">Daegu Gyeongbuk Institute of Science and Technology<br>School of Undergraduate Studies</div>
      <div class="bs-meta">
        <b>Document</b><span>{document}</span><b>Course</b><span>PHY309</span>
        <b>Week</b><span>{date.removeprefix('Week ')}</span><b>Instructor</b><span>Professor Scarinci</span>
      </div>
    </div>
    """
        )

    def _statement(label, title, body):
        head = f"**{label}" + (f" ({title})" if title else "") + ".**"
        return mo.md(head + "\n\n" + body).style({"border-left": f"2px solid {BLUE}", "padding-left": "1rem"})

    def definition(body, title=""):
        return _statement("Definition", title, body)

    def theorem(body, title=""):
        return _statement("Theorem", title, body)

    def proposition(body, title=""):
        return _statement("Proposition", title, body)

    def corollary(body, title=""):
        return _statement("Corollary", title, body)

    def postulate(body, title=""):
        return _statement("Postulate", title, body)

    def note(body):
        """Editorial note of the notebook (not part of the lecture)."""
        return mo.md("**Note.** " + body.strip())

    def arrow(ax, tail, tip, color, label=None, at_tip=False, lw=1.4, **kw):
        """Draw the vector from `tail` to `tip` on a 2D axis, labelled at its middle or its tip.
        One head size and one line weight for every figure, so arrows look alike across lectures."""
        ax.annotate(
            "",
            xy=tip,
            xytext=tail,
            arrowprops={"arrowstyle": "-|>,head_width=0.15,head_length=0.35", "color": color, "lw": lw, "shrinkA": 0, "shrinkB": 0, **kw},
        )
        if label:
            pos = tip if at_tip else ((tail[0] + tip[0]) / 2, (tail[1] + tip[1]) / 2)
            ax.annotate(label, pos, textcoords="offset points", xytext=(6, 6), color=color, fontsize=13)

    def plane(ax, lim):
        """Style a 2D axis as a coordinate plane with range [-lim, lim]."""
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.axhline(0, color="black", lw=0.8)
        ax.axvline(0, color="black", lw=0.8)
        ax.grid(True, color=LIGHT, lw=0.6)
        ax.set_axisbelow(True)

    def blank(w, h, xlim, ylim):
        """A figure with one bare axis (no frame) for sketches."""
        from matplotlib.figure import Figure as _Figure

        fig = _Figure(figsize=(w, h), layout="constrained")
        ax = fig.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        return fig, ax

    def blob(cx, cy, rx, ry, wobble=0.07, seed=0, n=400):
        """Closed organic curve around (cx, cy): an ellipse with a few low harmonics."""
        import numpy as _np

        rng = _np.random.default_rng(seed)
        t = _np.linspace(0, 2 * _np.pi, n)
        r = 1 + sum(wobble / k * rng.uniform(0.4, 1.0) * _np.cos(k * t + rng.uniform(0, 2 * _np.pi)) for k in (2, 3, 4, 5))
        return cx + rx * r * _np.cos(t), cy + ry * r * _np.sin(t)

    def table(rows):
        """Fixed-label readout table: rows are (label, value) pairs of markdown strings."""
        return mo.md("\n".join(["| | |", "|:--|--:|"] + [f"| {k} | {v} |" for k, v in rows]))

    return BLUE, FULL, GREEN, GREY, HALF, LIGHT, ORANGE, RED, arrow, blank, blob, corollary, definition, header, note, plane, postulate, proposition, table, theorem


@app.cell(hide_code=True)
def _(arrow):
    def cross_axes(ax, xlim, ylim, xlabel=None, ylabel=None):
        """A bare pair of coordinate axes through the origin."""
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        arrow(ax, (xlim[0], 0), (xlim[1], 0), "black", lw=0.9)
        arrow(ax, (0, ylim[0]), (0, ylim[1]), "black", lw=0.9)
        if xlabel:
            ax.annotate(xlabel, (xlim[1], 0), textcoords="offset points", xytext=(-12, -18), fontsize=13)
        if ylabel:
            ax.annotate(ylabel, (0, ylim[1]), textcoords="offset points", xytext=(8, -10), fontsize=13)

    return (cross_axes,)


@app.cell(hide_code=True)
def _(header):
    header("Lecture 07", "Week 04", "Lecture 07 · Manifolds")
    return


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREEN, GREY, arrow, fig_congruence, fig_surfaces, mo, np):
    _fig = Figure(figsize=(FULL, 2.4), layout="constrained")
    _l, _r = _fig.subplots(1, 2)
    for _ax in (_l, _r):
        _ax.set_xlim(-1.6, 1.6)
        _ax.set_ylim(-0.4, 2.1)
        _ax.axis("off")
    for _x in (-0.6, 0.6):
        _l.plot([_x, _x], [0, 2], color=BLUE)
        arrow(_l, (_x, 0), (_x, 0.9), GREEN)
        _l.plot(_x, 0, "o", color="black", ms=4)
    _l.text(-0.9, 0.5, "$v$", color=GREEN, fontsize=13)
    _l.text(0.7, 0.5, "$v' = v$", color=GREEN, fontsize=13)
    _l.text(-0.7, -0.35, "$p$", fontsize=13)
    _l.text(0.5, -0.35, "$q$", fontsize=13)
    _s = np.linspace(0, 2, 100)
    _r.plot([0, 0], [-0.2, 2.1], color="black")
    for _sgn in (-1, 1):
        _r.plot(_sgn * 0.6 * (1 - (_s / 2.05) ** 2), _s, color=BLUE)
        arrow(_r, (_sgn * 0.6, 0), (_sgn * 0.6, 0.9), GREEN)
        _r.plot(_sgn * 0.6, 0, "o", color="black", ms=4)
    _r.text(-0.9, 0.5, "$v$", color=GREEN, fontsize=13)
    _r.text(0.7, 0.5, "$v'$", color=GREEN, fontsize=13)
    _r.text(-0.7, -0.35, "$p$", fontsize=13)
    _r.text(0.5, -0.35, "$q$", fontsize=13)
    _r.text(0.1, 1.95, "source of gravity", color=GREY, fontsize=11)

    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    - so far, geometry = *affine space* + additional structure: no origins or frames, just congruence &nbsp; $\Longrightarrow$ &nbsp; straight lines &nbsp; $\Longrightarrow$ &nbsp; parallel lines
    - gravity defines free-falling particles: a notion of “straight lines” incompatible with parallelism (tidal effects), hence with congruence
    """
            ),
            _fig,
            mo.md(
                r"""
    **In this lecture:** generalize geometry so that it does *not need congruence* (drop the affine structure)

    ## II.2 &nbsp; Manifolds

    ### Charts and atlases

    differential geometry = *manifolds* + additional structure

    Manifolds: generalized spaces with points, but no displacement vectors, which look like $\mathbb{R}^m$, but only locally

    In $\mathbb{R}^m$ we have a preferred point $o = \begin{bmatrix} 0 \\ 0 \\ \vdots \\ 0 \end{bmatrix}$ and a preferred basis of vectors $e_i = \begin{bmatrix} 0 \\ \vdots \\ 1 \\ \vdots \\ 0 \end{bmatrix}$

    In $\mathbb{A}^m$ each choice of $(o, e_i) \in \mathbb{A}^m \times \mathbb{V}^m$ defines

    $$
    \varphi_{(o, e_i)} : \mathbb{A}^m \longrightarrow \mathbb{R}^m, \qquad p = \underbrace{o + x^i e_i}_{\text{using } - \,:\, \mathbb{A} \times \mathbb{A} \to \mathbb{V}} \longmapsto \begin{bmatrix} x^1 \\ x^2 \\ \vdots \\ x^m \end{bmatrix}
    $$

    Importantly $\varphi_{(o, e_i)} : \mathbb{A}^m \longrightarrow \mathbb{R}^m$ is a global bijection

    For $\varphi_{(o, e_i)}$, $\varphi_{(\tilde{o}, \tilde{e}_i)}$ two such charts

    $$
    \varphi_{(\tilde{o}, \tilde{e}_i)} \circ \varphi_{(o, e_i)}^{-1} : \mathbb{R}^m \overset{\sim}{\longrightarrow} \mathbb{R}^m, \qquad
    \begin{bmatrix} x^1 \\ \vdots \\ x^m \end{bmatrix} \longmapsto \begin{bmatrix} \tilde{x}^1 \\ \vdots \\ \tilde{x}^m \end{bmatrix} = \begin{bmatrix} A^1{}_1 & \cdots & A^1{}_m \\ \vdots & & \vdots \\ A^m{}_1 & \cdots & A^m{}_m \end{bmatrix} \begin{bmatrix} x^1 \\ \vdots \\ x^m \end{bmatrix} + \begin{bmatrix} b^1 \\ \vdots \\ b^m \end{bmatrix}
    $$

    change of coordinates = linear transformation + constant translation

    In a manifold $M^m$ we will keep the ability of producing coordinate charts

    $$
    \varphi_\alpha : U_\alpha \subseteq M^m \longrightarrow V_\alpha \subseteq \mathbb{R}^m
    $$

    - now only local bijections
    - for $\varphi_\alpha$ and $\varphi_\beta$: &nbsp; $\varphi_\beta \circ \varphi_\alpha^{-1} : V_\alpha \subseteq \mathbb{R}^m \overset{\sim}{\longrightarrow} V_\beta \subseteq \mathbb{R}^m$ &nbsp; (bijective at least in some subset of $V_\alpha$)

    **Example.** 2-sphere $\mathbb{S}^2$, &nbsp; 2-torus $\mathbb{T}^2$, &nbsp; genus 2 surface $\Sigma_2$
    """
            ),
            fig_surfaces,
            mo.md(r"""What does congruence mean on the sphere?"""),
            fig_congruence,
        ]
    )
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREEN, GREY, HALF, ORANGE, RED, arrow, math, np):
    # Surfaces of genus 0, 1, 2 as line drawings: true silhouettes, with a few surface curves (hidden parts dashed)
    _az, _el = math.radians(-30), math.radians(22)
    _d = np.array([math.cos(_el) * math.cos(_az), math.cos(_el) * math.sin(_az), math.sin(_el)])  # scene to eye
    _r = np.array([-math.sin(_az), math.cos(_az), 0.0])
    _u = np.cross(_d, _r)

    def _silhouette(ax, F, half, res=(240, 180), steps=140):
        xs, ys = np.linspace(-half, half, res[0]), np.linspace(-half, half, res[1])
        X, Y = np.meshgrid(xs, ys)
        o = X[..., None] * _r + Y[..., None] * _u + 2.2 * half * _d
        fmin = np.full(X.shape, np.inf)
        for t in np.linspace(0, 4.4 * half, steps):
            P = o - t * _d
            fmin = np.minimum(fmin, F(P[..., 0], P[..., 1], P[..., 2]))
        ax.contour(xs, ys, fmin, levels=[0.0], colors="black", linewidths=1.1)  # the silhouette, interpolated between samples

    def _surface_curve(ax, F, P, half, color="black", lw=0.9, steps=160):
        """Draw the visible part of the space curve P (n x 3) lying on F = 0."""
        X, Y = P @ _r, P @ _u
        o = P + 2.2 * half * _d  # start of the ray from the eye towards each point
        hidden = np.zeros(len(P), dtype=bool)
        for t in np.linspace(0, 2.2 * half, steps)[:-3]:
            Q = o - t * _d
            hidden |= F(Q[:, 0], Q[:, 1], Q[:, 2]) < -1e-3
        ax.plot(np.where(hidden, np.nan, X), np.where(hidden, np.nan, Y), color=color, lw=lw)

    def _torus(x, y, z, R=1.0, a=0.42):
        return (np.sqrt(x * x + y * y) - R) ** 2 + z * z - a * a

    def _genus2(x, y, z):  # two tori, smoothly joined, side by side on the screen
        xr, yr = x * _r[0] + y * _r[1], x * _d[0] + y * _d[1]
        t1, t2 = _torus(xr - 0.95, yr, z, 0.62, 0.3), _torus(xr + 0.95, yr, z, 0.62, 0.3)
        k = 0.18
        return -k * np.log(np.exp(-t1 / k) + np.exp(-t2 / k))

    _sphereF = lambda x, y, z: x * x + y * y + z * z - 1.0
    _t = np.linspace(0, 2 * np.pi, 300)
    fig_surfaces = Figure(figsize=(6.2, 2.4), layout="constrained")
    _s1, _s2, _s3 = fig_surfaces.subplots(1, 3, width_ratios=[1, 1.35, 1.65])
    fig_congruence = Figure(figsize=(HALF, 3.4), layout="constrained")
    _cg = fig_congruence.subplots()
    for _ax, _F, _half, _name in ((_s1, _sphereF, 1.1, r"$\mathbb{S}^2$"), (_s2, _torus, 1.55, r"$\mathbb{T}^2$"), (_s3, _genus2, 1.9, r"$\Sigma_2$")):
        _silhouette(_ax, _F, _half)
        _ax.set_xlim(-_half, _half)
        _ax.set_ylim(-1.5 * _half, _half)
        _ax.text(0, -1.12 * _half, _name, fontsize=13, ha="center", va="top")
        _ax.set_aspect("equal")
        _ax.axis("off")
    _E = np.column_stack([np.cos(_t), np.sin(_t), 0 * _t]) @ np.column_stack([_r, _u])  # the equator of the sphere, projected
    _front = (np.column_stack([np.cos(_t), np.sin(_t), 0 * _t]) @ _d) >= 0
    _s1.plot(np.where(_front, _E[:, 0], np.nan), np.where(_front, _E[:, 1], np.nan), color="black", lw=0.9)
    _s1.plot(np.where(_front, np.nan, _E[:, 0]), np.where(_front, np.nan, _E[:, 1]), color="black", lw=0.7, ls=(0, (3, 3)))

    def _hole(ax, cx, cy, w, tilt=0.1):  # a hole drawn by hand: a smile whose ends curl up, with a small frown nested above it
        a = np.linspace(-0.08 * np.pi, 1.08 * np.pi, 120)
        ax.plot(cx + 1.12 * w * np.cos(a), cy - 0.56 * w * np.sin(np.clip(a, 0, np.pi)) + 0.28 * w * np.maximum(0, -np.sin(a)) + tilt * w * np.cos(a), color="black", lw=1.1, solid_capstyle="round")
        a = np.linspace(0.12 * np.pi, 0.88 * np.pi, 60)
        ax.plot(cx + 0.72 * w * np.cos(a), cy - 0.24 * w + 0.34 * w * np.sin(a) + 0.7 * tilt * w * np.cos(a), color="black", lw=1.1, solid_capstyle="round")

    _hole(_s2, 0.0, 0.15, 0.55)
    for _sgn in (-1, 1):
        _c0 = _sgn * 0.95 * _r
        _hole(_s3, _c0[0] * _r[0] + _c0[1] * _r[1], 0.1, 0.36)
    # congruence on the sphere: vectors copied along the equator, then carried up to the pole
    _cg.plot(np.cos(_t), np.sin(_t), color="black")
    _cg.plot(np.cos(_t), np.where(np.sin(_t) <= 0, 0.42 * np.sin(_t), np.nan), color="black", lw=0.9)
    _cg.plot(np.cos(_t), np.where(np.sin(_t) > 0, 0.42 * np.sin(_t), np.nan), color="black", lw=0.7, ls=(0, (3, 3)))
    _ph = np.linspace(0, np.pi / 2, 80)  # meridians from the equator up to the pole r = (0, 1)
    for _x0 in (-0.9, 0.9):
        _y0 = -0.42 * np.sqrt(1 - _x0**2)
        _cg.plot(_x0 * np.cos(_ph), _y0 + (1 - _y0) * np.sin(_ph), color=GREY, lw=0.8)
    _y0 = -0.42 * np.sqrt(1 - 0.6**2)
    for _x0, _col in ((-0.6, BLUE), (0.6, RED)):
        _cg.plot(_x0 * np.cos(_ph), _y0 + (1 - _y0) * np.sin(_ph), color=_col)
    for _x0 in np.linspace(-0.6, 0.6, 6):
        _yy = -0.42 * np.sqrt(1 - _x0**2)
        arrow(_cg, (_x0, _yy), (_x0, _yy + 0.4), GREEN)
    _cg.plot([-0.6, 0.6], [_y0] * 2, "o", color="black", ms=3.5, zorder=4)
    _cg.text(-0.6, _y0 - 0.1, "$p$", fontsize=12, ha="center", va="top")
    _cg.text(0.6, _y0 - 0.1, "$q$", fontsize=12, ha="center", va="top")
    _cg.text(-0.67, _y0 + 0.1, "$v$", color=GREEN, fontsize=12, ha="right", va="center")
    _cg.text(0.67, _y0 + 0.1, "$v' = v$", color=GREEN, fontsize=12, ha="left", va="center", zorder=8, bbox=dict(boxstyle="round,pad=0.08", facecolor="white", edgecolor="none"))
    arrow(_cg, (0, 1), (-0.42, 1.32), GREEN)
    arrow(_cg, (0, 1), (0.42, 1.32), ORANGE)
    _cg.text(-0.5, 1.38, "$v$", color=GREEN, fontsize=12, ha="right")
    _cg.text(0.5, 1.38, "$v'$", color=ORANGE, fontsize=12)
    _cg.plot(0, 1, "o", color="black", ms=3.5, zorder=4)
    _cg.text(0.1, 0.78, "$r$", fontsize=12)
    _cg.set_xlim(-1.35, 1.35)
    _cg.set_ylim(-1.15, 1.55)
    _cg.set_aspect("equal")
    _cg.axis("off")
    _ = None  # no cell output: the figures are returned, not displayed here
    return fig_congruence, fig_surfaces


@app.cell(hide_code=True)
def _(BLUE, FULL, LIGHT, RED, arrow, blank, blob, definition, mo, np):
    _fig, _ax = blank(FULL, 2.9, (-0.2, 10.2), (-0.3, 3.7))
    from matplotlib.path import Path as _Path

    _ax.plot(*blob(5.0, 2.0, 1.75, 1.45, wobble=0.09, seed=3), color="black")
    _ax.text(3.2, 3.4, "$M$", fontsize=14)
    _Ua, _Ub = blob(4.55, 2.1, 0.78, 0.62, seed=1), blob(5.45, 2.0, 0.78, 0.7, seed=2)
    _g = np.linspace(0, 1, 300)
    _X, _Y = np.meshgrid(3 + 4 * _g, 0.4 + 3.2 * _g)
    _pts = np.column_stack([_X.ravel(), _Y.ravel()])
    _A = _Path(np.column_stack(_Ua)).contains_points(_pts).reshape(_X.shape)
    _B = _Path(np.column_stack(_Ub)).contains_points(_pts).reshape(_X.shape)
    _ax.contourf(_X, _Y, (_A & _B).astype(float), levels=[0.5, 1.5], colors=[LIGHT], alpha=0.9)
    _ax.plot(*_Ua, color=RED)
    _ax.plot(*_Ub, color=BLUE)
    _ax.text(3.8, 2.8, r"$U_\alpha$", color=RED, fontsize=13)
    _ax.text(5.95, 2.8, r"$U_\beta$", color=BLUE, fontsize=13)
    for _x0, _col, _name, _lab in ((0.3, RED, r"$V_\alpha \subseteq \mathbb{R}^2$", r"$\varphi_\alpha$"), (8.0, BLUE, r"$V_\beta \subseteq \mathbb{R}^2$", r"$\varphi_\beta$")):
        _ax.plot([_x0, _x0 + 1.7, _x0 + 1.7, _x0, _x0], [0.5, 0.5, 2.0, 2.0, 0.5], color=_col)
        _ax.text(_x0, 0.1, _name, color=_col, fontsize=12)
    _ax.fill([1.3, 2.0, 2.0, 1.2, 1.0], [0.5, 0.5, 2.0, 2.0, 1.2], color=LIGHT, alpha=0.9, lw=0)
    _ax.fill([8.0, 8.8, 9.0, 8.7, 8.0], [0.5, 0.5, 1.3, 2.0, 2.0], color=LIGHT, alpha=0.9, lw=0)
    arrow(_ax, (3.9, 1.7), (2.1, 1.5), RED, connectionstyle="arc3,rad=0.25")
    _ax.text(2.7, 2.1, r"$\varphi_\alpha$", color=RED, fontsize=13)
    arrow(_ax, (6.1, 1.6), (7.9, 1.5), BLUE, connectionstyle="arc3,rad=-0.25")
    _ax.text(6.9, 2.1, r"$\varphi_\beta$", color=BLUE, fontsize=13)
    arrow(_ax, (2.1, 0.8), (7.9, 0.8), "black", lw=1.0, connectionstyle="arc3,rad=0.22")
    _ax.text(5.0, -0.2, r"$\varphi_\beta \circ \varphi_\alpha^{-1}$", fontsize=13, ha="center")

    mo.vstack(
        [
            definition(
                r"""
    A **$m$-dimensional manifold** ($m$-manifold) is a set of points $M^m \ni p$, with a collection of charts $\mathcal{A} \ni \varphi_\alpha$

    $$
    \varphi_\alpha : U_\alpha \subseteq M \longrightarrow V_\alpha \subseteq \mathbb{R}^m
    $$

    where

    - $U_\alpha$ *cover* $M$ &nbsp; $\left( \bigcup_\alpha U_\alpha = M \right)$
    - $V_\alpha$ are *open sets* of $\mathbb{R}^m$ &nbsp; (given by union of open balls in $\mathbb{R}^m$)
    - $\varphi_\alpha : U_\alpha \overset{\sim}{\longrightarrow} V_\alpha$ are *bijections* &nbsp; (each $U_\alpha$ “looks like” $V_\alpha = \varphi_\alpha(U_\alpha)$ via $\varphi_\alpha$)
    - $\varphi_\alpha(U_\alpha \cap U_\beta) \subseteq V_\alpha$, &nbsp; $\varphi_\beta(U_\alpha \cap U_\beta) \subseteq V_\beta$ are also open
    - $\varphi_\beta \circ \varphi_\alpha^{-1}$ are *diffeomorphisms* &nbsp; (smooth bijections with smooth inverse)

        $$
        \varphi_\beta \circ \varphi_\alpha^{-1} : \underbrace{\varphi_\alpha(U_\alpha \cap U_\beta)}_{\subseteq\, \mathbb{R}^m} \overset{\sim}{\longrightarrow} \underbrace{\varphi_\beta(U_\alpha \cap U_\beta)}_{\subseteq\, \mathbb{R}^m}
        $$
    """,
                "Manifold",
            ),
            mo.md(
                r"""
    **Example.** &nbsp; $\mathbb{S}^2 = \{\, (x^1, x^2, x^3) \in \mathbb{R}^3 \mid (x^1)^2 + (x^2)^2 + (x^3)^2 = 1 \,\}$ &nbsp; (Earth)

    $V_\alpha \subseteq \mathbb{R}^2$ = “page $\alpha$ of a geographical atlas”, &nbsp; $V_\beta \subseteq \mathbb{R}^2$ = “page $\beta$”
    """
            ),
            _fig,
            mo.md(
                r"""
    **Remark.** $\varphi_\beta \circ \varphi_\alpha^{-1}$ diffeomorphism

    $\Longrightarrow$ &nbsp; we can do calculus on each $U_\alpha \subseteq M$ using usual calculus on $V_\alpha \subseteq \mathbb{R}^m$ and every result agrees on $U_\alpha \cap U_\beta$

    ### Topology

    **Remark.** Collection of all open sets defines a topology on $\mathbb{R}^m$ &nbsp; $\leadsto$ &nbsp; study properties of $\mathbb{R}^m$ invariant under continuous deformations

    $\varphi_\alpha : U_\alpha \longrightarrow V_\alpha$ bijection, $V_\alpha$ open, $\varphi_\alpha(U_\alpha \cap U_\beta)$ open

    $\Longrightarrow$ &nbsp; defines a topology on $M$ with open sets $\varphi_\alpha^{-1}(V_\alpha \cap W) \subseteq M$, for $W \subseteq \mathbb{R}^m$ open, and their unions

    **Remark.** We need to require a few *technical conditions* (Hausdorff + second countable) on this topology, but it will not be too important.

    ### Smooth functions
    """
            ),
            definition(
                r"""
    Given an $m$-manifold $M$, $\mathcal{A} = \{\, \varphi_\alpha : U_\alpha \longrightarrow V_\alpha \subseteq \mathbb{R}^m \,\}$, a function $f : M \longrightarrow \mathbb{R}$ is called **smooth** if, for every chart $\varphi_\alpha \in \mathcal{A}$, the composition

    $$
    f \circ \varphi_\alpha^{-1} : V_\alpha \subseteq \mathbb{R}^m \longrightarrow \mathbb{R} \qquad (\text{usual scalar function in } \mathbb{R}^m)
    $$

    is smooth
    """,
                "Smooth function",
            ),
            mo.md(
                r"""
    $\Longrightarrow$ &nbsp; we know how to calculate derivatives with respect to coordinates in $V_\alpha$

    Let's simplify notation a bit here: &nbsp; $\varphi_\alpha : U_\alpha \longrightarrow V_\alpha$ &nbsp; $\leadsto$ &nbsp; $\varphi : U \longrightarrow V \subseteq \mathbb{R}^m \ni x$

    $$
    \frac{\partial}{\partial x^\mu} (f \circ \varphi^{-1})(x) = \lim_{h \to 0} \frac{(f \circ \varphi^{-1})(x + h e_\mu) - (f \circ \varphi^{-1})(x)}{h}
    $$

    $$
    D_x (f \circ \varphi^{-1})(v) = \lim_{h \to 0} \frac{(f \circ \varphi^{-1})(x + h v) - (f \circ \varphi^{-1})(x)}{h} = v^\mu\, \frac{\partial}{\partial x^\mu} (f \circ \varphi^{-1})(x)
    $$

    $\Longrightarrow$ &nbsp; given two charts $\varphi : U \longrightarrow V \subseteq \mathbb{R}^m \ni x$, &nbsp; $\tilde{\varphi} : \tilde{U} \longrightarrow \tilde{V} \subseteq \mathbb{R}^m \ni \tilde{x}$

    $$
    \left. \begin{aligned} f \circ \varphi^{-1} &: V \longrightarrow \mathbb{R} \\ f \circ \tilde{\varphi}^{-1} &: \tilde{V} \longrightarrow \mathbb{R} \end{aligned} \right\} \quad \text{representations of } f \text{ in each chart}
    $$

    are related via

    $$
    (f \circ \varphi^{-1})(x) = (f \circ \tilde{\varphi}^{-1}) \circ \underbrace{(\tilde{\varphi} \circ \varphi^{-1})(x)}_{\tilde{x}(x)} \qquad \text{on } \varphi(U \cap \tilde{U}) \subseteq V
    $$

    $$
    \begin{aligned}
    \Longrightarrow \qquad \frac{\partial}{\partial x^\mu} (f \circ \varphi^{-1})(x) &= \frac{\partial}{\partial \tilde{x}^\nu} (f \circ \tilde{\varphi}^{-1})(\tilde{x}(x))\, \frac{\partial \tilde{x}^\nu}{\partial x^\mu}(x) \\[4pt]
    &= \underbrace{\frac{\partial \tilde{x}^\nu}{\partial x^\mu}(x)}_{\text{Jacobian matrix of the change of coordinates}} \frac{\partial}{\partial \tilde{x}^\nu} (f \circ \tilde{\varphi}^{-1})(\tilde{x}(x))
    \end{aligned}
    $$

    ($\tilde{x} = \tilde{\varphi} \circ \varphi^{-1}(x)$ &nbsp; $\leadsto$ &nbsp; smooth by the diffeo assumption!)

    $\therefore$ &nbsp; the notion of smoothness for $f : M \longrightarrow \mathbb{R}$ via charts is well-defined because changes of charts are always smooth!

    ### Stereographic charts on the sphere

    **Example.** &nbsp; $\mathbb{S}^2 = \{\, (x, y, z) \in \mathbb{R}^3 \mid x^2 + y^2 + z^2 = 1 \,\}$

    Choose a point $n = (0, 0, 1)$ (north pole)

    Define $\varphi_n : \mathbb{S}^2 - \{n\} \longrightarrow \mathbb{R}^2$ via stereographic projection

    $$
    \varphi_n(x, y, z) = (u, v) = \left( \frac{x}{1 - z},\ \frac{y}{1 - z} \right)
    $$

    Line through $n$ and $p$ in $\mathbb{R}^3$; by triangle similarity: &nbsp; $z \begin{bmatrix} u \\ v \\ 0 \end{bmatrix} = \begin{bmatrix} u - x \\ v - y \\ 0 \end{bmatrix}$ &nbsp; $\Longrightarrow$ &nbsp; $(1 - z)\, u = x$, &nbsp; $(1 - z)\, v = y$

    $\Longrightarrow$ &nbsp; $\varphi_n$ is a bijection from $\underbrace{\mathbb{S}^2 - \{n\}}_{U_n}$ to $\underbrace{\mathbb{R}^2}_{V_n}$

    Choose $s = (0, 0, -1)$ (south pole)

    $$
    \varphi_s : \underbrace{\mathbb{S}^2 - \{s\}}_{U_s} \longrightarrow \underbrace{\mathbb{R}^2}_{V_s}, \qquad (x, y, z) \longmapsto \varphi_s(x, y, z) = (\tilde{u}, \tilde{v}) = \left( \frac{x}{1 + z},\ \frac{y}{1 + z} \right)
    $$

    is also a bijection

    - $U_n \cup U_s = (\mathbb{S}^2 - \{n\}) \cup (\mathbb{S}^2 - \{s\}) = \mathbb{S}^2$
    - $V_n, V_s$ are open, &nbsp; $\varphi_n(U_n \cap U_s) = \mathbb{R}^2 - \{(0, 0)\}$, &nbsp; $\varphi_s(U_s \cap U_n) = \mathbb{R}^2 - \{(0, 0)\}$ are open
    - $\varphi_s \circ \varphi_n^{-1} : \mathbb{R}^2 - \{(0, 0)\} \longrightarrow \mathbb{R}^2 - \{(0, 0)\}$ is smooth with smooth inverse!

    $$
    \varphi_s \circ \varphi_n^{-1}(u, v) = \left( \frac{u}{u^2 + v^2},\ \frac{v}{u^2 + v^2} \right) = (\tilde{u}, \tilde{v})
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    lat = mo.ui.slider(-85, 85, 1, value=35, label="latitude of $p$ (degrees)", show_value=True)
    return (lat,)


@app.cell(hide_code=True)
def _(BLUE, FULL, GREY, RED, blank, lat, math, mo, np):
    _a = math.radians(lat.value)
    _x, _z = math.cos(_a), math.sin(_a)
    _u, _ut = _x / (1 - _z), _x / (1 + _z)

    _R = max(5.2, 1.1 * max(_u, _ut))  # the frame follows the projected points: nothing is clipped or dropped
    _fig, _ax = blank(FULL, 3.6, (-0.3 * _R, _R), (-1.5, 1.6))
    _th = np.linspace(0, 2 * np.pi, 200)
    _ax.plot(np.cos(_th), np.sin(_th), color=GREY)
    _ax.plot([-0.3 * _R, _R], [0, 0], color="black")
    _ax.plot([0, _x, _u], [1, _z, 0], color=BLUE)  # ray from n through p to phi_n(p)
    _ax.plot([0, _x, _ut], [-1, _z, 0], color=RED)  # ray from s through p to phi_s(p)
    for _pt, _name, _col, _off in (((0, 1), "$n$", "black", (-14, 4)), ((0, -1), "$s$", "black", (-14, -12)), ((_x, _z), "$p$", "black", (8, 4))):
        _ax.plot(*_pt, "o", color=_col, ms=5)
        _ax.annotate(_name, _pt, textcoords="offset points", xytext=_off, color=_col, fontsize=14)
    _ax.plot(_u, 0, "o", color=BLUE, ms=5)
    _ax.annotate(r"$\varphi_n(p)$", (_u, 0), textcoords="offset points", xytext=(-8, -18), color=BLUE, fontsize=12)
    _ax.plot(_ut, 0, "o", color=RED, ms=5)
    _ax.annotate(r"$\varphi_s(p)$", (_ut, 0), textcoords="offset points", xytext=(-30, 8), color=RED, fontsize=12)

    _table = "\n".join(
        [
            "| | |",
            "|:--|--:|",
            rf"| $p = (x,\ 0,\ z)$ &nbsp; (slice $y = 0$ of $\mathbb{{S}}^2$) | $({_x:.3f},\ 0,\ {_z:.3f})$ |",
            rf"| $u = x / (1 - z)$ &nbsp; ($v = 0$) | ${_u:.3f}$ |",
            rf"| $\tilde{{u}} = x / (1 + z)$ &nbsp; ($\tilde{{v}} = 0$) | ${_ut:.3f}$ |",
            rf"| $u / (u^2 + v^2)$ | ${1 / _u:.3f}$ |",
        ]
    )
    mo.vstack([mo.hstack([lat], justify="start"), mo.md(_table), _fig])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Summary

    - a manifold is a set covered by charts $\varphi_\alpha : U_\alpha \longrightarrow V_\alpha \subseteq \mathbb{R}^m$ whose changes of chart $\varphi_\beta \circ \varphi_\alpha^{-1}$ are diffeomorphisms: locally like $\mathbb{R}^m$, globally only glued together
    - the charts define a topology on $M$, and calculus on $M$ is done chart by chart; smoothness of $f : M \longrightarrow \mathbb{R}$ is chart-independent because the change of charts is smooth
    - the sphere is a 2-manifold with the two stereographic charts $\varphi_n$, $\varphi_s$, whose change of chart is the inversion $(u, v) \longmapsto (u, v) / (u^2 + v^2)$

    **Next:** more charts on the sphere, smooth maps between manifolds, and tangent vectors
    """
    )
    return


if __name__ == "__main__":
    app.run()
