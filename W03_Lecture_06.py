import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 6 · The equivalence principle", css_file="lecturekit/style.css")


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
    return lk, mo, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(6, "The equivalence principle")
    return


@app.cell(hide_code=True)
def _(lk, np):
    # Helpers of this lecture: the figure of tidal effects

    def fall(q, s):
        """Free fall from rest at the point q = (x^1, x^2), at the times s: the particle stays on the ray from M,
        at r = r0 cos^2(eta), s = sqrt(r0^3 / 2) (eta + sin(eta) cos(eta))."""
        q = np.asarray(q, float)
        r0 = float(np.hypot(*q))
        k = np.sqrt(r0**3 / 2)
        s = np.asarray(s, float)
        lo, hi = np.zeros_like(s), np.full_like(s, np.pi / 2)
        for _ in range(60):
            mid = (lo + hi) / 2
            big = mid + np.sin(mid) * np.cos(mid) > s / k
            hi, lo = np.where(big, mid, hi), np.where(big, lo, mid)
        r = r0 * np.cos((lo + hi) / 2) ** 2
        return q[0] / r0 * r, q[1] / r0 * r, s

    def tidal_scene(T):
        # two pairs of free-falling particles, released from rest: a pair side by side (delta across the direction
        # to M) comes together, a pair one above the other (delta along it) moves apart; dashed: inertial particles
        s = np.linspace(0, T, 121)
        d = np.array([0.0, 0.8])  # delta, the same for both pairs
        starts = [np.array([3.0, -0.4]), np.array([0.0, 2.6])]
        x1, x2 = (-0.9, 3.9), (-0.9, 3.9)
        c = [(x1[0], x2[0], 0.0), (x1[1], x2[0], 0.0), (x1[1], x2[1], 0.0), (x1[0], x2[1], 0.0)]
        e = np.array(c + [c[0]])
        surfaces = [lk.patch(c, lk.LIGHT, 0.45, n=12)]
        lines = [(e[:, 0], e[:, 1], e[:, 2], lk.GREY, 0.8), ((0.0, 0.0), (0.0, 0.0), (0.0, 4.0), "#000000", 1.4)]
        points, arrows = [((0.0, 0.0, 0.0), "#000000", 2.6)], []
        texts = [((0.0, 0.0, 4.0), r"M", "#000000", 90, 5)]
        for g0 in starts:
            pair = [(g0, lk.RED, r"\gamma"), (g0 + d, lk.BLUE, r"\sigma")]
            paths = [fall(q, s) for q, _c, _n in pair]
            ends = [np.array([a[-1], b[-1]]) for a, b, _t in paths]
            for k, ((q, col, name), (a, b, t)) in enumerate(zip(pair, paths)):
                lines.append(((q[0], q[0]), (q[1], q[1]), (0.0, T), lk.GREY, 1.0, [4, 3]))
                lines.append((a, b, t, col, 1.8))
                points += [((q[0], q[1], 0.0), col, 3.0), ((a[-1], b[-1], T), col, 3.0)]
                out = (ends[k] - ends[1 - k]) / np.linalg.norm(ends[k] - ends[1 - k])  # away from the other particle
                texts.append(((a[-1] + 0.3 * out[0], b[-1] + 0.3 * out[1], T), name, col, 90, 3))
            arrows.append(((g0[0], g0[1], 0.0), (g0[0] + d[0], g0[1] + d[1], 0.0), lk.GREEN, 1.4))
            texts.append(((g0[0] + d[0] / 2, g0[1] + d[1] / 2, 0.0), r"\delta", lk.GREEN, -90, 7))
        return lk.turntable(
            40,
            24,
            "two pairs of particles falling from rest towards the mass M: a pair side by side comes together, a pair one above the other moves apart; the dashed lines are inertial particles from the same starts",
            [lk.panel(0.8, surfaces=surfaces, lines=lines, arrows=arrows, points=points, texts=texts, box=(x1, x2, (0.0, 4.0)))],
            height=340,
            width=560,
            key="L06-tide",
            apart=True,
            bias=0.12,
        )

    return (tidal_scene,)


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figure (the time t of the fall)
    s_t = lk.slider(1.0, 4.0, step=0.5, value=4.0, label="$t$", show_value=False)
    return (s_t,)


@app.cell(hide_code=True)
def _(s_t, tidal_scene):
    # the scene of the tidal figure, redrawn by the slider; its frame is in the tidal effects block
    tidal_scene(s_t.value)
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"$\sigma:\mathbb R\longrightarrow\mathbb M^4$ &nbsp; particle, &nbsp; $m>0$",
        r"$\sigma':\mathbb R\longrightarrow\mathbb V^4$ &nbsp; 4-velocity",
        r"$\sigma'':\mathbb R\longrightarrow\mathbb V^4$ &nbsp; 4-acceleration",
        r"relativistic equations of motion",
        lk.aside(
            r"$$\underbrace{m\,\sigma''=\mk{\kappa}\,\mk{F}(\sigma,\sigma')}_{\text{2nd order system of ODEs}}$$",
            r"$\kappa$ = coupling constant (charge)<br>$F$ = force rule",
        ),
        topic="Relativistic dynamics",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("Schutz 5.1; Carroll 2.1, 4.7")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: universality of free fall
    # remark: different charges give different histories
    lk.remark(
        r"""
        For relativistic models of this type (e.g. Maxwell)

        given two particles $\sigma_1,\sigma_2$ with &nbsp; $\begin{cases}\sigma_1(0)=\sigma_2(0)=p\\\sigma_1'(0)=\sigma_2'(0)=v\end{cases}$

        > $\Longrightarrow$ &nbsp; $\sigma_2''(0)-\sigma_1''(0)=\Big(\dfrac{\kappa_2}{m_2}-\dfrac{\kappa_1}{m_1}\Big)F(p,v)$

        > $\Longrightarrow$ &nbsp; different histories
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: universality of free fall
    # for gravity, charge = mass
    lk.prose(
        lk.aside(
            r"For gravity, however, &nbsp; <span class='lk-mark'>“charge”</span> $=$ <span class='lk-mark'>mass</span> &nbsp; (weak equivalence principle)",
            r"“charge” = gravitational mass $\kappa_i$<br>mass = inertial mass $m_i$",
        ),
        lk.aside(
            r"> $\Longrightarrow$ &nbsp; $\sigma_2''(0)-\sigma_1''(0)=\mk{\Big(\dfrac{m_2}{m_2}-\dfrac{m_1}{m_1}\Big)G(p,v)}=0$",
            r"independent of the specific model<br>we would use for $G$",
        ),
        r"""
        > $\Longrightarrow$ &nbsp; $\sigma_1(s)=\sigma_2(s)\quad\forall s$ &nbsp; (by uniqueness of IVPs)

        > $\Longrightarrow$ &nbsp; gravity defines a special family of histories in spacetime!
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: universality of free fall
    # definition: free-falling particle
    lk.definition(
        r"A **free-falling particle** is a particle subject to no non-gravitational forces",
        label="def-free-falling",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: universality of free fall
    # what defines a free-falling particle
    lk.prose(
        r"$\leadsto$ &nbsp; in principle defined via",
        r"$$\begin{cases}\sigma''=G(\sigma,\sigma')\\\sigma(0)=p,\ \sigma'(0)=v\end{cases}$$",
        lk.aside(
            r"> for the given gravitational force, but <span class='lk-mark'>independent</span> of the particle's “internal structure”",
            "“universality of free fall”",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Einstein's thought experiment
    # an observer and a test particle
    lk.prose(
        lk.aside(
            r"Einstein's thought experiment",
            "an observer releases a test particle<br>and observes its evolution",
        ),
        r"Consider $\gamma$ (the “observer”) and $\sigma$ (the “test particle”) two particles with &nbsp; $\begin{cases}\sigma(0)=\gamma(0)=p\\\sigma'(0)=\gamma'(0)=v\end{cases}$",
        r"Suppose &nbsp; $\begin{aligned}m_\gamma\gamma''&=m_\gamma G(\gamma,\gamma')+\ell_\gamma H(\gamma,\gamma')\\m_\sigma\sigma''&=m_\sigma G(\sigma,\sigma')+\kappa_\sigma F(\sigma,\sigma')\end{aligned}$",
        r"> $\displaystyle\begin{aligned}\Longrightarrow\quad a(\gamma,\sigma)(p)&=\sigma''(0)-\gamma''(0)\\[0.3em]&=\frac{\kappa_\sigma}{m_\sigma}F(p,v)-\frac{\ell_\gamma}{m_\gamma}H(p,v)\end{aligned}$",
        lk.gap(),
        r"If $\gamma$ is free-falling, &nbsp; $H(\gamma,\gamma')=0$",
        r"""
        > $\Longrightarrow$ &nbsp; $a(\gamma,\sigma)(p)=\dfrac{\kappa_\sigma}{m_\sigma}F(p,v)$

        > > $\leadsto$ &nbsp; same as for an inertial observer in $\mathbb M^4$
        """,
        lk.aside(
            r"> > $\leadsto$ &nbsp; we cannot distinguish between free-falling and inertial motion from <span class='lk-mark'>local</span> measurements!",
            "local = instantaneous",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Einstein's equivalence principle
    # postulate: Einstein's equivalence principle
    lk.postulate(
        [
            lk.aside(
                r"$$\mk{\text{Physics}}\text{ in a free-falling lab}=\text{Physics in an inertial lab}$$",
                "local and non-gravitational physics",
            ),
            r"(extending the weak equivalence principle)",
        ],
        title="Einstein's equivalence principle",
        label="post-eep",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Einstein's equivalence principle
    # remark: a postulate about spacetime
    lk.remark(
        [
            r"Einstein's equivalence principle is a physical postulate, not a mathematical theorem!",
            lk.aside(
                r"> $\leadsto$ &nbsp; we will take it as a new assumption about the <span class='lk-mark'>structure of spacetime</span>",
                "the “gravitational force” is universal<br>and not locally observable by any<br>free-falling particle, so it cannot be<br>seen as a force acting on particles<br>but as a property of spacetime itself!",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk, s_t):
    # module: tidal effects
    # neighboring free-falling particles
    lk.prose(
        r"Consider now neighboring free-falling particles $\gamma,\sigma$",
        r"$$\gamma''=G(\gamma,\gamma'),\qquad\sigma''=G(\sigma,\sigma')$$",
        r"> with &nbsp; $\sigma(0)=\gamma(0)+\delta$, &nbsp; $\sigma'(0)=\gamma'(0)=v$ &nbsp; and &nbsp; $\delta\in v^\perp$",
        lk.aside(
            r"> $\displaystyle\begin{aligned}\Longrightarrow\quad a(\gamma,\sigma)(0)&=G(p+\delta,v)-G(p,v)\\[0.3em]&=D_1G(p,v)[\delta]+O(\lVert\delta\rVert^2)\\[0.3em]&=\mk{\nu(\gamma,\sigma)'(0)}\quad\text{not zero in general!}\end{aligned}$",
            r"neighboring particles with zero initial<br>relative velocity may start moving<br>towards or away from each other!<br>$\leadsto$ tidal effects",
            at="last",
        ),
        lk.interactive(lk.frame("L06-tide", 340, 560), controls=[s_t]),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tidal effects
    # remark: inertial particles stay parallel
    lk.remark(
        [
            r"This is very different from inertial particles!",
            r"For inertial particles $\gamma,\sigma$ in $\mathbb M^4$ (also in $\mathbb G^4$)",
            r"> with &nbsp; $\sigma(0)=\gamma(0)+\delta$, &nbsp; $\sigma'(0)=\gamma'(0)=v$, &nbsp; $\delta\in v^\perp$ &nbsp; ($\delta\in\ker\tau$)",
            lk.aside(
                r"> $\Longrightarrow$ &nbsp; $a(\gamma,\sigma)(0)=\mk{0=\nu(\gamma,\sigma)'(0)}$",
                "particles that start moving in the same<br>direction remain parallel forever!",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tidal effects
    # conclusions: no parallelism, no affine structure
    lk.prose(
        lk.aside(
            r"$\leadsto$ &nbsp; in the presence of gravity, spacetime has a family of preferred particles<br>which describe local physics exactly as inertial particles in $\mathbb M^4$,<br>but <span class='lk-mark'>it loses the structure of parallelism</span> between those particles!",
            "structure of parallelism = the affine structure!",
        ),
        lk.aside(
            r"$\leadsto$ &nbsp; in particular, to be able to formulate a relativistic theory of gravity,<br>we will need to reformulate our description of spacetime<br><span class='lk-mark'>without using affine spaces</span>",
            "this will lead us to<br>the theory of manifolds!",
        ),
    )
    return


if __name__ == "__main__":
    app.run()
