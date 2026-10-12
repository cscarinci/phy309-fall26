import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 06 · The equivalence principle", css_file="phy309.css")


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
      <div class="bs-title">Differential Geometry and General Relativity</div>
      <div class="bs-inst">Daegu Gyeongbuk Institute of Science and Technology<br>School of Undergraduate Studies</div>
      <div class="bs-meta">
        <b>Document</b><span>{document}</span><b>Course</b><span>PHY309</span>
        <b>Date</b><span>{date}</span><b>Instructor</b><span>Professor Scarinci</span>
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
            arrowprops={"arrowstyle": "-|>", "color": color, "lw": lw, "mutation_scale": 11, "shrinkA": 0, "shrinkB": 0, **kw},
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

    def table(rows):
        """Fixed-label readout table: rows are (label, value) pairs of markdown strings."""
        return mo.md("\n".join(["| | |", "|:--|--:|"] + [f"| {k} | {v} |" for k, v in rows]))

    return BLUE, FULL, GREEN, GREY, HALF, LIGHT, ORANGE, RED, arrow, blank, corollary, definition, header, note, plane, postulate, proposition, table, theorem


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
    header("Lecture 06", "Week 03", "Lecture 06 · The equivalence principle")
    return


@app.cell(hide_code=True)
def _(definition, mo, postulate, theorem):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Last time

    - relativistic dynamics: a particle $\sigma : \mathbb{R} \longrightarrow \mathbb{M}^4$ with mass $m > 0$ has 4-velocity $\sigma'$, 4-momentum $P = m\sigma'$ and 4-acceleration $\sigma''$
    - equations of motion $m\, \sigma'' = \kappa\, F(\sigma, \sigma')$: a second order system of ODEs with coupling constant (charge) $\kappa$ and force rule $F$

    **Today:** why gravity is not one more force rule: the equivalence principle

    ## II.1 &nbsp; The equivalence principle

    ### Universality of free fall

    **Remark.** For relativistic models of this type (e.g. Maxwell), given two particles $\sigma_1, \sigma_2$ with $\begin{cases} \sigma_1(0) = \sigma_2(0) = p \\ \sigma_1'(0) = \sigma_2'(0) = v \end{cases}$

    $$
    \Longrightarrow \quad \sigma_2''(0) - \sigma_1''(0) = \left( \frac{\kappa_2}{m_2} - \frac{\kappa_1}{m_1} \right) F(p, v)
    \qquad \Longrightarrow \quad \text{different histories}
    $$

    For gravity, however, *“charge” = mass* &nbsp; (gravitational mass $\kappa_i$ = inertial mass $m_i$: weak equivalence principle)

    $$
    \Longrightarrow \quad \sigma_2''(0) - \sigma_1''(0) = \underbrace{\left( \frac{m_2}{m_2} - \frac{m_1}{m_1} \right) G(p, v) = 0}_{\text{independent of the specific model we would use for } G}
    $$

    $$
    \Longrightarrow \quad \sigma_1(s) = \sigma_2(s) \quad \forall\, s \qquad (\text{by uniqueness of IVPs})
    $$

    $\Longrightarrow$ &nbsp; gravity defines a special family of histories in spacetime!
    """
            ),
            definition(
                r"""
    A **free-falling particle** is a particle subject to no non-gravitational forces
    """,
                "Free-falling particle",
            ),
            mo.md(
                r"""
    In principle defined via

    $$
    \begin{cases} \sigma'' = G(\sigma, \sigma') \\ \sigma(0) = p, \ \sigma'(0) = v \end{cases}
    $$

    for the given gravitational force, but *independent* of the particle's “internal structure” &nbsp; (“universality of free fall”)

    ### Einstein's thought experiment

    An observer releases a test particle and observes its evolution

    Consider $\gamma$ (the “observer”) and $\sigma$ (the “test particle”) two particles with $\begin{cases} \sigma(0) = \gamma(0) = p \\ \sigma'(0) = \gamma'(0) = v \end{cases}$

    Suppose

    $$
    \begin{aligned}
    m_\gamma \gamma'' &= m_\gamma G(\gamma, \gamma') + \ell_\gamma H(\gamma, \gamma') \\
    m_\sigma \sigma'' &= m_\sigma G(\sigma, \sigma') + \kappa_\sigma F(\sigma, \sigma')
    \end{aligned}
    $$

    $$
    \begin{aligned}
    \Longrightarrow \quad a(\gamma, \sigma)(p) &= \sigma''(0) - \gamma''(0) \\
    &= \frac{\kappa_\sigma}{m_\sigma} F(p, v) - \frac{\ell_\gamma}{m_\gamma} H(p, v)
    \end{aligned}
    $$

    If $\gamma$ is free-falling, $H(\gamma, \gamma') = 0$

    $$
    \Longrightarrow \quad a(\gamma, \sigma)(p) = \frac{\kappa_\sigma}{m_\sigma} F(p, v)
    $$

    - same as for an inertial observer in $\mathbb{M}^4$
    - we cannot distinguish between free-falling and inertial motion from *local measurements* (instantaneous)

    ### Einstein's equivalence principle
    """
            ),
            postulate(
                r"""
    $$
    \textit{Physics} \text{ in a free-falling lab} = \text{Physics in an inertial lab} \qquad (\textit{Physics}: \text{local and non-gravitational})
    $$

    (extends the weak equivalence principle, gravitational mass = inertial mass)
    """,
                "Einstein's equivalence principle",
            ),
            mo.md(
                r"""
    **Remark.** The equivalence principle is a physical postulate, not a mathematical theorem!

    We will take it as a new assumption about the *structure of spacetime*: the “gravitational force” is universal and not locally observable by any free-falling particle, so it cannot be seen as a force acting on particles but as a property of spacetime itself.

    ### Tidal effects

    Consider now neighboring free-falling particles $\gamma, \sigma$

    $$
    \gamma'' = G(\gamma, \gamma'), \qquad \sigma'' = G(\sigma, \sigma')
    $$

    with $\sigma(0) = \gamma(0) + \delta$, &nbsp; $\sigma'(0) = \gamma'(0) = v$ &nbsp; and $\delta \in v^\perp$

    $$
    \begin{aligned}
    \Longrightarrow \quad a(\gamma, \sigma)(0) &= G(p + \delta, v) - G(p, v) \\
    &= D_1 G(p, v)[\delta] + O(\lVert \delta \rVert^2) \\
    &= \nu(\gamma, \sigma)'(0) \quad \text{not zero in general!}
    \end{aligned}
    $$

    Neighboring particles with zero initial relative velocity may start moving towards or away from each other &nbsp; $\leadsto$ &nbsp; tidal effects
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    tide = mo.ui.slider(-1, 1, 0.1, value=-0.6, label="$k$", show_value=True)
    sep = mo.ui.slider(0.2, 1.5, 0.1, value=0.8, label=r"$\lVert \delta \rVert$", show_value=True)
    return sep, tide


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, RED, arrow, blank, mo, np, sep, tide):
    _k, _d = tide.value, sep.value
    _s = np.linspace(0, 3, 200)
    if _k < 0:
        _w = np.sqrt(-_k)
        _x = _d * np.cos(_w * _s)
    elif _k > 0:
        _x = _d * np.cosh(np.sqrt(_k) * _s)
    else:
        _x = np.full_like(_s, _d)

    _L = max(3.4, 1.15 * float(np.abs(_x).max()))
    _fig, _ax = blank(4.6, 4.0, (-0.55 * _L, _L), (-0.3, 3.2))
    _ax.set_aspect("auto")
    _ax.plot(0 * _s, _s, color=BLUE)
    _ax.plot(_x, _s, color=RED)
    _ax.plot(np.full_like(_s, _d), _s, "--", color=GREY, lw=1.0)
    arrow(_ax, (0, 0), (_d, 0), GREEN)
    _ax.text(_d / 2, -0.25, r"$\delta$", color=GREEN, fontsize=14, ha="center")
    _ax.text(-0.3, 0.25, r"$\gamma$", color=BLUE, fontsize=15)
    _ax.annotate(r"$\sigma$", (float(_x[-1]), 3.0), textcoords="offset points", xytext=(6, -4), color=RED, fontsize=15)
    _ax.text(_d, 3.05, "inertial", color=GREY, fontsize=10, ha="center", va="bottom")
    _ax.text(-0.5 * _L, 1.5, "proper time", rotation=90, fontsize=10, va="center")

    if _k < 0:
        _formula = rf"$\lVert \delta \rVert \cos\big(\sqrt{{{-_k:g}}}\, s\big)$"
    elif _k > 0:
        _formula = rf"$\lVert \delta \rVert \cosh\big(\sqrt{{{_k:g}}}\, s\big)$"
    else:
        _formula = r"$\lVert \delta \rVert$"
    _table = "\n".join(
        [
            "| | |",
            "|:--|--:|",
            r"| model: separation $x(s)$ of $\sigma$ from $\gamma$ with $x'' = k\, x$, $x(0) = \lVert \delta \rVert$, $x'(0) = 0$ | |",
            rf"| $x(s)$ | {_formula} |",
            rf"| $\nu(\gamma, \sigma)'(0) = k\, \lVert \delta \rVert$ | ${_k * _d:.3f}$ |",
            rf"| $x(3)$ | ${float(_x[-1]):.3f}$ |",
        ]
    )
    mo.vstack([mo.hstack([tide, sep], justify="start", gap=3, wrap=True), mo.md(_table), _fig])
    return


@app.cell(hide_code=True)
def _(mo, postulate):
    mo.md(r"""
    **Remark.** This is very different from inertial particles.

    For inertial particles $\gamma, \sigma$ in $\mathbb{M}^4$ (also in $\mathbb{G}^4$) with $\sigma(0) = \gamma(0) + \delta$, &nbsp; $\sigma'(0) = \gamma'(0) = v$, &nbsp; $\delta \in v^\perp$ &nbsp; ($\delta \in \ker \tau$)

    $$
    \Longrightarrow \quad a(\gamma, \sigma)(0) = 0 = \nu(\gamma, \sigma)'(0)
    $$

    Particles that start moving in the same direction remain parallel forever.

    In the presence of gravity, spacetime has a family of preferred particles which describe local physics exactly as inertial particles in $\mathbb{M}^4$, but *it loses the structure of parallelism between those particles* (the affine structure)!

    ## Summary

    - gravitational mass = inertial mass: all particles with the same initial event and 4-velocity fall along the same history, whatever the model $G$ (universality of free fall)
    - a free-falling observer cannot detect gravity by local measurements; Einstein's equivalence principle turns this into a postulate about spacetime itself
    - tidal effects: neighboring free-falling particles do not stay parallel, so gravity is incompatible with the affine structure

    **Next:** manifolds, spaces with points and local coordinates but no displacement vectors
    """)
    return


if __name__ == "__main__":
    app.run()
