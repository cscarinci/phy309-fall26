import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 11 · Vector fields", css_file="phy309.css")


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
    header("Lecture 11", "Week 06", "Lecture 11 · Vector fields")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    - $T_pM = \{\, [\gamma] \mid \gamma : \mathbb{R} \to M,\ \gamma(0) = p \,\}$ with $\gamma \sim \tilde{\gamma}$ if

        $$
        (\varphi \circ \gamma)'(0) = (\varphi \circ \tilde{\gamma})'(0)
        $$
    - $\mathrm{Der}_p(M) = \{\, X_p : C^\infty(M, \mathbb{R}) \to \mathbb{R} \mid \text{linear, } X_p(fg) = X_p(f)\, g(p) + f(p)\, X_p(g) \,\}$.
    - $T_pM \simeq \mathrm{Der}_p(M)$: $[\gamma] \longleftrightarrow X_p$ with $X_p(f) = \dfrac{d}{dt}\Big|_{t=0} (f \circ \gamma)(t)$, equivalently $(\varphi \circ \gamma)'(0) = X_p(x^i)\, e_i$. Velocity vectors are directional derivatives.
    - $T_pM$ is an $m$-dimensional vector space; a chart $\varphi$ gives the coordinate basis $\partial_i|_p$, with $\partial_i|_p f = \dfrac{\partial}{\partial x^i}(f \circ \varphi^{-1})\Big|_{\varphi(p)}$, and every $X_p = X^i(p)\, \partial_i|_p$ with $X^i(p) = X_p(x^i)$.
    - On a manifold the tangent space $T_pM$ takes the place of the vector space $\mathbb{V}$ of an affine space, but each point has its own.

    **In this lecture:** vector fields, integral curves and the tangent bundle.

    **References:** Carroll 2.3; Sasane Ch. 3
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            mo.md(r"""
    ## II.6 &nbsp; Vector fields

    ### Vector fields
    """),
            definition(
                r"""
    A **vector field** on $M$ is an assignment of a tangent vector (a velocity vector, or equivalently a derivation) to each point

    $$
    X : p \longmapsto X_p \in T_p M = \mathrm{Der}_p(M)
    $$

    With respect to a chart $\varphi : U \subseteq M \longrightarrow \mathbb{R}^m$ with local coordinates $x^i : U \longrightarrow \mathbb{R}$

    $$
    p = \varphi^{-1}(x^i(p)\, e_i), \qquad X_p = X^i(p)\, \partial_i|_p
    $$

    and the **local components** $X^i : U \subseteq M \longrightarrow \mathbb{R}$ of $X$ are functions on $U$. The vector field $X$ is **smooth** if its local components with respect to every chart are smooth.
    """,
                "Vector field",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Example on the sphere

    **Example.** &nbsp; On $\mathbb{S}^2$ with the two stereographic charts

    $$
    \varphi_n(x, y, z) = \left( \frac{x}{1 - z},\ \frac{y}{1 - z} \right) = (u, v), \qquad \varphi_s(x, y, z) = \left( \frac{x}{1 + z},\ \frac{y}{1 + z} \right) = (\tilde{u}, \tilde{v})
    $$

    define

    $$
    X : p \longmapsto X_p =
    \begin{cases}
    -v(p)\, \partial_u|_p + u(p)\, \partial_v|_p, & p \neq n \\[4pt]
    -\tilde{v}(p)\, \partial_{\tilde{u}}|_p + \tilde{u}(p)\, \partial_{\tilde{v}}|_p, & p \neq s
    \end{cases}
    $$

    The first expression is not defined at $n$, the second is not defined at $s$, and on the overlap $\mathbb{S}^2 - \{n, s\}$ the two must agree for $X$ to be well defined. Given $f \in C^\infty(\mathbb{S}^2, \mathbb{R})$

    $$
    \begin{aligned}
    X_p(f) &= -v(p)\, \partial_u|_p f + u(p)\, \partial_v|_p f \\[4pt]
    &= -v(p)\, \frac{\partial}{\partial u} (f \circ \varphi_n^{-1})\bigg|_{\varphi_n(p)} + u(p)\, \frac{\partial}{\partial v} (f \circ \varphi_n^{-1})\bigg|_{\varphi_n(p)} \\[4pt]
    &= -\tilde{v}(p)\, \frac{\partial}{\partial \tilde{u}} (f \circ \varphi_s^{-1})\bigg|_{\varphi_s(p)} + \tilde{u}(p)\, \frac{\partial}{\partial \tilde{v}} (f \circ \varphi_s^{-1})\bigg|_{\varphi_s(p)}
    \end{aligned}
    $$

    Do these agree? The chain rule through the transition map

    $$
    \varphi_s \circ \varphi_n^{-1}(u, v) = \left( \frac{u}{u^2 + v^2},\ \frac{v}{u^2 + v^2} \right) = \big( \tilde{u}(u, v),\ \tilde{v}(u, v) \big)
    $$

    $$
    \begin{aligned}
    \Longrightarrow \qquad \frac{\partial}{\partial u} (f \circ \varphi_n^{-1}) &= \frac{\partial}{\partial u} (f \circ \varphi_s^{-1} \circ \varphi_s \circ \varphi_n^{-1}) \\[4pt]
    &= \frac{\partial}{\partial \tilde{u}} (f \circ \varphi_s^{-1})\, \frac{\partial \tilde{u}}{\partial u} + \frac{\partial}{\partial \tilde{v}} (f \circ \varphi_s^{-1})\, \frac{\partial \tilde{v}}{\partial u} \\[4pt]
    &= \frac{-u^2 + v^2}{(u^2 + v^2)^2}\, \frac{\partial}{\partial \tilde{u}} (f \circ \varphi_s^{-1}) + \frac{-2uv}{(u^2 + v^2)^2}\, \frac{\partial}{\partial \tilde{v}} (f \circ \varphi_s^{-1}) \\[10pt]
    \frac{\partial}{\partial v} (f \circ \varphi_n^{-1}) &= \frac{-2uv}{(u^2 + v^2)^2}\, \frac{\partial}{\partial \tilde{u}} (f \circ \varphi_s^{-1}) + \frac{u^2 - v^2}{(u^2 + v^2)^2}\, \frac{\partial}{\partial \tilde{v}} (f \circ \varphi_s^{-1})
    \end{aligned}
    $$

    and taking $-v$ times the first plus $u$ times the second gives the coefficients

    $$
    \frac{-v (u^2 + v^2)}{(u^2 + v^2)^2} = -\tilde{v}, \qquad \frac{u (u^2 + v^2)}{(u^2 + v^2)^2} = \tilde{u}
    $$

    so they do agree.

    $$
    \Longrightarrow \qquad X : p \longmapsto X_p =
    \begin{cases}
    -v(p)\, \partial_u|_p + u(p)\, \partial_v|_p, & p \neq n \\[4pt]
    -\tilde{v}(p)\, \partial_{\tilde{u}}|_p + \tilde{u}(p)\, \partial_{\tilde{v}}|_p, & p \neq s
    \end{cases}
    $$

    is well-defined and it is smooth since

    $$
    \begin{aligned}
    X^u &= -v : \mathbb{S}^2 - \{n\} \longrightarrow \mathbb{R} \\
    X^v &= u : \mathbb{S}^2 - \{n\} \longrightarrow \mathbb{R} \\
    X^{\tilde{u}} &= -\tilde{v} : \mathbb{S}^2 - \{s\} \longrightarrow \mathbb{R} \\
    X^{\tilde{v}} &= \tilde{u} : \mathbb{S}^2 - \{s\} \longrightarrow \mathbb{R}
    \end{aligned}
    \qquad \text{are all smooth}
    $$

    What about other charts? In the spherical chart $\psi$ defined on $\mathbb{S}^2$ minus the arc of great circle $x \geq 0$, $y = 0$ from $n$ to $s$,

    $$
    \psi^{-1} : (0, \pi) \times (0, 2\pi) \longrightarrow \mathbb{S}^2, \qquad \psi^{-1}(\phi, \theta) = (\cos\theta \sin\phi,\ \sin\theta \sin\phi,\ \cos\phi)
    $$

    $$
    \varphi_n \circ \psi^{-1}(\phi, \theta) = \left( \cot\tfrac{\phi}{2} \cos\theta,\ \cot\tfrac{\phi}{2} \sin\theta \right) = \big( u(\phi, \theta),\ v(\phi, \theta) \big)
    $$

    $$
    \Longrightarrow \qquad X : p \longmapsto X_p = \partial_\theta|_p
    $$

    with smooth components, because the transition map $\varphi_n \circ \psi^{-1}$ is smooth. Smoothness in one atlas is smoothness in every compatible chart.

    ### Vector fields as operators

    **Remark.** Given a vector field $X$ and a smooth function $f$ we can define another function $X(f) : M \longrightarrow \mathbb{R}$ via

    $$
    X(f)(p) = X_p(f)
    $$
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo, theorem):
    mo.vstack(
        [
            theorem(
                r"""
    A vector field $X : p \longmapsto X_p \in T_p M$ is smooth if and only if it defines a linear differential operator on $M$

    $$
    X : C^\infty(M, \mathbb{R}) \longrightarrow C^\infty(M, \mathbb{R}), \qquad f \longmapsto X(f) : p \longmapsto X_p(f)
    $$

    In a chart $\varphi : U \subseteq M \longrightarrow \mathbb{R}^m$

    $$
    X(f) \circ \varphi^{-1} = X^i \circ \varphi^{-1}\, \frac{\partial}{\partial x^i} (f \circ \varphi^{-1})
    $$

    which is smooth for every $f$ if and only if every $X^i \circ \varphi^{-1}$ is smooth.
    """,
                "Smooth vector fields are differential operators",
            ),
            definition(
                r"""
    The space of smooth vector fields on $M$ is denoted

    $$
    \Gamma(TM) = \text{space of smooth vector fields } X : C^\infty(M, \mathbb{R}) \longrightarrow C^\infty(M, \mathbb{R})
    $$

    where $TM$ denotes the collection of all tangent spaces of $M$, the tangent bundle (defined below).
    """,
                "Smooth vector fields",
            ),
            mo.md(
                r"""
    **Remark.** In terms of a chart $\varphi : U \subseteq M \longrightarrow \mathbb{R}^m$

    $$
    \begin{gathered}
    X = X^i\, \partial_i, \\[4pt]
    X^i : U \subseteq M \longrightarrow \mathbb{R} \ \text{ local functions on } U, \qquad \partial_i \in \Gamma(TM)|_U \ \text{ local vector fields on } U
    \end{gathered}
    $$

    The $\partial_i$ form a local basis of vector fields on $U$; they play over $U$ the role of $e_i \in \mathbb{R}^m$.

    ### Integral curves
    """
            ),
            definition(
                r"""
    Given a smooth path $\gamma : I \longrightarrow M$ with $I \subseteq \mathbb{R}$ an interval, a **vector field along** $\gamma$ is an assignment

    $$
    X : t \in I \longmapsto X_{\gamma(t)} \in T_{\gamma(t)} M
    $$

    of a tangent vector at $\gamma(t)$ for each $t \in I$.
    """,
                "Vector field along a path",
            ),
            mo.md(
                r"""
    **Example.** The velocity vector field of a smooth path $\gamma : \mathbb{R} \longrightarrow M$ is the assignment $\gamma' : t \in \mathbb{R} \longmapsto \gamma'(t) \in T_{\gamma(t)} M$ such that

    $$
    \gamma'(t)(f) = (f \circ \gamma)'(t)
    $$

    $\leadsto$ &nbsp; with respect to a chart $\varphi$:

    $$
    \gamma'(t) = (x^i \circ \gamma)'(t)\ \partial_i|_{\gamma(t)}
    $$
    """
            ),
            definition(
                r"""
    Given a smooth vector field $X \in \Gamma(TM)$, a path $\gamma : I \longrightarrow M$ with $I \subseteq \mathbb{R}$ an interval is an **integral curve** of $X$ if its velocity equals the vector field along $\gamma$

    $$
    \gamma'(t) = X_{\gamma(t)} \qquad \forall\ t \in I
    $$

    With respect to a chart $\varphi$ this is a first order system of ordinary differential equations

    $$
    (x^i \circ \gamma)'(t) = X^i(\gamma(t))
    $$
    """,
                "Integral curve",
            ),
            theorem(
                r"""
    For each $p \in M$ there exists a unique *maximal* integral curve $\gamma : I \longrightarrow M$ of $X \in \Gamma(TM)$, with $I \subseteq \mathbb{R}$ an open interval containing $0$, with the initial condition $\gamma(0) = p$:

    $$
    \begin{cases} \gamma'(t) = X_{\gamma(t)} \\ \gamma(0) = p \end{cases} \quad \text{is a first order initial value problem on } M
    $$

    When $M$ is compact (for example $\mathbb{S}^2$) one has $I = \mathbb{R}$ for every $p$; in general not: for $X = x^2\, \partial_x$ on $\mathbb{R}$ with $\gamma(0) = 1$ the solution is $x(t) = \dfrac{1}{1 - t}$ with $I = (-\infty, 1)$.
    """,
                "Existence and uniqueness of integral curves",
            ),
            mo.md(
                r"""
    **Example.** &nbsp; On $\mathbb{S}^2$, with $X = \begin{cases} -v\, \partial_u + u\, \partial_v & \text{on } \mathbb{S}^2 - \{n\} \\ -\tilde{v}\, \partial_{\tilde{u}} + \tilde{u}\, \partial_{\tilde{v}} & \text{on } \mathbb{S}^2 - \{s\} \end{cases}$

    a path $\gamma : \mathbb{R} \longrightarrow \mathbb{S}^2$ with $\varphi_n(\gamma(0)) = (u_0, v_0)$ is an integral curve of $X$

    $$
    \begin{aligned}
    &\Longleftrightarrow \qquad \gamma'(t) = X_{\gamma(t)} \\[4pt]
    &\Longleftrightarrow \qquad (\varphi_n \circ \gamma)'(t) = X^i(\gamma(t))\, e_i, \qquad \begin{bmatrix} u'(t) \\ v'(t) \end{bmatrix} = \begin{bmatrix} -v(t) \\ u(t) \end{bmatrix} \\[4pt]
    &\Longleftrightarrow \qquad \begin{bmatrix} u(t) \\ v(t) \end{bmatrix} = \begin{bmatrix} u_0 \cos(t) - v_0 \sin(t) \\ u_0 \sin(t) + v_0 \cos(t) \end{bmatrix} \\[4pt]
    &\Longleftrightarrow \qquad \gamma(t) = \varphi_n^{-1}\!\left( \begin{bmatrix} u_0 \cos(t) - v_0 \sin(t) \\ u_0 \sin(t) + v_0 \cos(t) \end{bmatrix} \right)
    \end{aligned}
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    s_u0 = mo.ui.slider(-2.0, 2.0, 0.1, value=1.4, label="$u_0$", show_value=True)
    s_v0 = mo.ui.slider(-2.0, 2.0, 0.1, value=0.0, label="$v_0$", show_value=True)
    s_t = mo.ui.slider(0.0, 6.28, 0.02, value=1.0, label="$t$", show_value=True)
    return s_t, s_u0, s_v0


@app.cell(hide_code=True)
def _(BLUE, FULL, Figure, GREY, RED, arrow, math, mo, np, s_t, s_u0, s_v0, table):
    _az, _el = math.radians(-30), math.radians(20)

    def _pr(x, y, z):
        X = -x * math.sin(_az) + y * math.cos(_az)
        Y = z * math.cos(_el) - (x * math.cos(_az) + y * math.sin(_az)) * math.sin(_el)
        D = (x * math.cos(_az) + y * math.sin(_az)) * math.cos(_el) + z * math.sin(_el)
        return X, Y, D

    def _inv(u, v):
        r = 1 + u**2 + v**2
        return 2 * u / r, 2 * v / r, (r - 2) / r

    def _curve(ax, xyz, color, lw=1.4):
        X, Y, D = _pr(*xyz)
        ax.plot(np.where(D >= 0, X, np.nan), np.where(D >= 0, Y, np.nan), color=color, lw=lw)
        ax.plot(np.where(D < 0, X, np.nan), np.where(D < 0, Y, np.nan), color=color, lw=0.8, ls=(0, (4, 3)))

    _u0, _v0, _t = s_u0.value, s_v0.value, s_t.value
    _ut = _u0 * math.cos(_t) - _v0 * math.sin(_t) + 0.0
    _vt = _u0 * math.sin(_t) + _v0 * math.cos(_t) + 0.0
    _s = np.linspace(0, _t, 200)
    _us, _vs = _u0 * np.cos(_s) - _v0 * np.sin(_s), _u0 * np.sin(_s) + _v0 * np.cos(_s)
    _c = np.linspace(0, 2 * np.pi, 400)

    _fig = Figure(figsize=(FULL, 3.7), layout="constrained")
    _ax, _ax2 = _fig.subplots(1, 2, width_ratios=[1.2, 1])
    _ax.set_xlim(-1.3, 1.3)
    _ax.set_ylim(-1.3, 1.45)
    _ax.set_aspect("equal")
    _ax.axis("off")
    _ax.plot(np.cos(_c), np.sin(_c), color="black")
    _curve(_ax, (np.cos(_c), np.sin(_c), 0 * _c), GREY, lw=1.0)
    # vectors of X on a few latitude circles (front side only)
    for _z in (-0.75, -0.4, 0.0, 0.4, 0.75):
        _rr = math.sqrt(1 - _z**2)
        for _a in np.linspace(0, 2 * np.pi, 12, endpoint=False):
            _q = (_rr * math.cos(_a), _rr * math.sin(_a), _z)
            _Q = _pr(*_q)
            if _Q[2] > 0.15 and math.hypot(_Q[0] - _pr(0, 0, -1)[0], _Q[1] - _pr(0, 0, -1)[1]) > 0.25:
                _E = _pr(_q[0] - 0.22 * _q[1], _q[1] + 0.22 * _q[0], _z)
                arrow(_ax, _Q[:2], _E[:2], BLUE, lw=0.9)
    _curve(_ax, _inv(_u0 * np.cos(_c) - _v0 * np.sin(_c), _u0 * np.sin(_c) + _v0 * np.cos(_c)), RED, lw=0.9)
    _X, _Y, _D = _pr(*_inv(_us, _vs))
    _ax.plot(np.where(_D >= 0, _X, np.nan), np.where(_D >= 0, _Y, np.nan), color=RED)
    for (_uu, _vv), _fc in (((_u0, _v0), "white"), ((_ut, _vt), RED)):
        _Q = _pr(*_inv(_uu, _vv))
        _ax.plot(*_Q[:2], "o", color=RED, mfc=_fc, ms=6, alpha=1.0 if _Q[2] >= 0 else 0.4)
    for _q, _n, _dy in (((0, 0, 1), "$n$", 0.1), ((0, 0, -1), "$s$", -0.25)):
        _Q = _pr(*_q)
        _ax.plot(*_Q[:2], "o", color="black", ms=3, alpha=1.0 if _Q[2] > 0 else 0.4)
        _ax.text(_Q[0] - 0.04, _Q[1] + _dy, _n, fontsize=13)

    _ax2.set_title(r"$\varphi_n$ : $(u, v)$", fontsize=13)
    _ax2.set_xlim(-3, 3)
    _ax2.set_ylim(-3, 3)
    _ax2.set_aspect("equal")
    _ax2.axhline(0, color="black", lw=0.6)
    _ax2.axvline(0, color="black", lw=0.6)
    _g = np.linspace(-2.5, 2.5, 9)
    _U, _V = np.meshgrid(_g, _g)
    _ax2.quiver(_U, _V, -_V, _U, color=BLUE, angles="xy", scale_units="xy", scale=5, width=0.006)
    _ax2.plot(np.cos(_c), np.sin(_c), color=GREY, lw=1.0)
    _ax2.text(0.06, 1.04, "equator", color=GREY, fontsize=10, ha="left", va="bottom", bbox=dict(boxstyle="round,pad=0.1", facecolor="white", edgecolor="none"))
    _ax2.plot(_u0 * np.cos(_c) - _v0 * np.sin(_c), _u0 * np.sin(_c) + _v0 * np.cos(_c), color=RED, lw=0.9)
    _ax2.plot(_us, _vs, color=RED)
    _ax2.plot(_u0, _v0, "o", color=RED, mfc="white", ms=6)
    _ax2.annotate(r"$\gamma(0)$", (_u0, _v0), textcoords="offset points", xytext=(6, -12), color=RED, fontsize=10, bbox=dict(boxstyle="round,pad=0.08", facecolor="white", edgecolor="none"), zorder=8)
    _ax2.plot(_ut, _vt, "o", color=RED, ms=6)
    _ax2.annotate(r"$\gamma(t)$", (_ut, _vt), textcoords="offset points", xytext=(6, 4), color=RED, fontsize=10, bbox=dict(boxstyle="round,pad=0.08", facecolor="white", edgecolor="none"), zorder=8)
    _ax2.set_xticks([-3, 0, 3])
    _ax2.set_yticks([-3, 0, 3])

    _p = _inv(_ut, _vt)
    _table = table(
        [
            (r"$\varphi_n(\gamma(t)) = (u_0 \cos t - v_0 \sin t,\ u_0 \sin t + v_0 \cos t)$", rf"$({_ut:.2f},\ {_vt:.2f})$"),
            (r"$\gamma(t) = \varphi_n^{-1}(\varphi_n(\gamma(t)))$", rf"$({_p[0] + 0.0:.3f},\ {_p[1] + 0.0:.3f},\ {_p[2] + 0.0:.3f})$"),
        ]
    )
    mo.vstack([mo.hstack([s_u0, s_v0, s_t], justify="start", gap=2, wrap=True), _table, _fig])
    return


@app.cell(hide_code=True)
def _(BLUE, Figure, GREY, ORANGE, RED, arrow, definition, math, mo, np):
    # A curved surface with three tangent planes, in perspective
    _az, _el = math.radians(-35), math.radians(28)

    def _pr(x, y, z):
        X = -x * math.sin(_az) + y * math.cos(_az)
        Y = z * math.cos(_el) - (x * math.cos(_az) + y * math.sin(_az)) * math.sin(_el)
        return X, Y

    def _h(x, y):  # height of the surface
        return 0.35 * np.sin(1.1 * x) * np.cos(0.9 * y) + 0.12 * y

    def _dh(x, y):
        return 0.35 * 1.1 * np.cos(1.1 * x) * np.cos(0.9 * y), -0.35 * 0.9 * np.sin(1.1 * x) * np.sin(0.9 * y) + 0.12

    _fig = Figure(figsize=(6.0, 3.6), layout="constrained")
    _ax = _fig.subplots()
    _ax.set_aspect("equal")
    _ax.axis("off")
    _g = np.linspace(-2.2, 2.2, 160)
    for _c in np.linspace(-2.2, 2.2, 7)[1:-1]:  # a few coordinate lines on the surface
        _ax.plot(*_pr(_g, _c + 0 * _g, _h(_g, _c)), color=GREY, lw=0.6, zorder=1)
        _ax.plot(*_pr(_c + 0 * _g, _g, _h(_c, _g)), color=GREY, lw=0.6, zorder=1)
    for _e in (np.column_stack([_g, -2.2 + 0 * _g]), np.column_stack([_g, 2.2 + 0 * _g]), np.column_stack([-2.2 + 0 * _g, _g]), np.column_stack([2.2 + 0 * _g, _g])):
        _ax.plot(*_pr(_e[:, 0], _e[:, 1], _h(_e[:, 0], _e[:, 1])), color="black", lw=1.2, zorder=2)
    _ax.text(*_pr(-2.4, -2.4, _h(-2.4, -2.4) + 0.3), "$M$", fontsize=15, ha="right")
    for (_x, _y), _col, _name, _tn, _vecs in (
        ((-1.3, -0.2), BLUE, "$q$", r"$T_q M$", (((0.3, 0.2), "$Z_q$"),)),
        ((1.25, -1.0), RED, "$p$", r"$T_p M$", (((0.38, -0.12), "$X_p$"), ((0.1, 0.38), "$Y_p$"))),
        ((0.5, 1.5), ORANGE, "$r$", r"$T_r M$", (((-0.5, 0.25), "$W_r$"),)),
    ):
        _z = _h(_x, _y)
        _hx, _hy = _dh(_x, _y)
        _tx, _ty = np.array([1.0, 0.0, _hx]), np.array([0.0, 1.0, _hy])  # tangent directions
        _corners = [np.array([_x, _y, _z]) + s_ * 0.7 * _tx + t_ * 0.55 * _ty for s_, t_ in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        _CX, _CY = zip(*[_pr(*c) for c in _corners])
        _ax.plot(list(_CX) + [_CX[0]], list(_CY) + [_CY[0]], color=_col, lw=1.0, zorder=4)
        _P = _pr(_x, _y, _z)
        for (_a, _b), _lab in _vecs:
            _tip = np.array([_x, _y, _z]) + _a * _tx + _b * _ty
            _T = _pr(*_tip)
            arrow(_ax, _P, _T, _col, zorder=6)
            _dx, _dy = _T[0] - _P[0], _T[1] - _P[1]
            _nn = math.hypot(_dx, _dy)
            _ax.text(_T[0] + 0.22 * _dx / _nn, _T[1] + 0.22 * _dy / _nn, _lab, color=_col, fontsize=11, ha="center", va="center", zorder=7, bbox=dict(boxstyle="round,pad=0.08", facecolor="white", edgecolor="none"))
        _ax.plot(*_P, "o", color="black", ms=4, zorder=6)
        _ax.text(_P[0] - 0.08, _P[1] - 0.1, _name, fontsize=12, ha="right", va="top", zorder=7)
        _left = min(range(4), key=lambda i: _CX[i])
        _ax.text(_CX[_left] - 0.08, _CY[_left] + 0.02, _tn, color=_col, fontsize=12, ha="right", va="center", zorder=7, bbox=dict(boxstyle="round,pad=0.08", facecolor="white", edgecolor="none"))

    mo.vstack(
        [
            mo.md(r"""### The tangent bundle"""),
            definition(
                r"""
    The **tangent bundle** of an $m$-manifold $M$ is

    $$
    \begin{aligned}
    TM &= \text{the collection of all tangent spaces} \\
    &\text{“}=\text{”} \bigcup_{p \in M} T_p M \\
    &= \left\{\, (p, X_p) \;\middle|\; p \in M,\ X_p \in T_p M \,\right\}
    \end{aligned}
    $$

    A tangent vector $X_p$ (an equivalence class of paths with the same velocity at $p$, or a derivation at $p$) always comes with its base point, which is why the notation $X_p$ is preferable to $[\gamma]$.
    """,
                "Tangent bundle",
            ),
            mo.hstack([_fig], justify="center"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    - A vector field assigns a tangent vector $X_p \in T_pM$ to each point; in a chart $X = X^i\, \partial_i$ with local components $X^i$, and $X$ is smooth if its components are smooth in every chart.
    - A smooth vector field is a linear differential operator $f \longmapsto X(f)$ on $C^\infty(M, \mathbb{R})$; the space of smooth vector fields is $\Gamma(TM)$.
    - An integral curve of $X$ satisfies $\gamma'(t) = X_{\gamma(t)}$, a first order system $(x^i \circ \gamma)' = X^i \circ \gamma$ in any chart; through each point passes a unique maximal integral curve.
    - The tangent bundle $TM$ is the collection of all tangent spaces, the natural home of vector fields.

    **Next:** review of calculus on manifolds and differential equations in several charts.
    """)
    return


if __name__ == "__main__":
    app.run()
