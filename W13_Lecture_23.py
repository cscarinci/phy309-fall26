import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 23 · The Einstein equation", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import sys

    import marimo as mo

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return (lk,)


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(23, "The Einstein equation")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"""
        $$
        \begin{aligned}
        \Longrightarrow\quad \Gamma^i_{tt}&\approx\nabla^i\Phi=-G^i\\
        \Longrightarrow\quad R^i{}_{tjt}&=-R^i{}_{ttj}\approx\partial_j\nabla^i\Phi=-\partial_jG^i
        \end{aligned}
        $$

        Poisson's equation:

        $$
        \begin{aligned}
        4\pi\rho=\Delta\Phi&=\partial_x^2\Phi+\partial_y^2\Phi+\partial_z^2\Phi\\
        &\approx R^x{}_{txt}+R^y{}_{tyt}+R^z{}_{tzt}=(\mathrm{Ric})_{tt}
        \end{aligned}
        $$
        """,
        topic=lk.aside(
            r"<span class='lk-mark'>Newton's gravity</span> as a <span class='lk-mark'>geodesic equation</span>",
            r"$\Phi$ = gravitational potential<br>$\nabla$ = Levi-Civita connection",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: contractions
    # section
    lk.section("Tensor contractions")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: contractions
    # definition: contraction
    lk.definition(
        r"""
        Given a tensor $T\in\Gamma(TM^r_s)$, a **contraction** of $T$ is another tensor $\hat T\in\Gamma(TM^{r-1}_{s-1})$
        obtained by evaluating a covector component of $T$ on a vector component.
        """,
        label="def-contraction",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: contractions
    # example: contractions of X ⊗ Y ⊗ α ⊗ β
    lk.example(
        [
            r"""
            $$
            T=X\otimes Y\otimes\alpha\otimes\beta\quad\leadsto\quad
            \left\lbrace
            \begin{aligned}
            \hat T_1&=\alpha(X)\,Y\otimes\beta\\
            \hat T_2&=\alpha(Y)\,X\otimes\beta\\
            \hat T_3&=\beta(X)\,Y\otimes\alpha\\
            \hat T_4&=\beta(Y)\,X\otimes\alpha
            \end{aligned}
            \right.
            $$
            """,
            lk.aside(
                r"""<span class="lk-vconn"><span>$\varphi$</span><span class="lk-vconn-arrow">$\leadsto$</span></span>""",
                r"$dx^\mu(\partial_\nu)=\delta^\mu{}_\nu$",
            ),
            r"""
            $$
            T^{\mu\nu}{}_{\rho\sigma}=X^\mu Y^\nu\alpha_\rho\beta_\sigma\quad\leadsto\quad
            \left\lbrace
            \begin{aligned}
            (\hat T_1)^\mu{}_\nu&=\alpha_\rho X^\rho\,Y^\mu\beta_\nu=T^{\rho\mu}{}_{\rho\nu}\\
            (\hat T_2)^\mu{}_\nu&=\alpha_\rho Y^\rho\,X^\mu\beta_\nu=T^{\mu\rho}{}_{\rho\nu}\\
            (\hat T_3)^\mu{}_\nu&=\beta_\rho X^\rho\,Y^\mu\alpha_\nu=T^{\rho\mu}{}_{\nu\rho}\\
            (\hat T_4)^\mu{}_\nu&=\beta_\rho Y^\rho\,X^\mu\alpha_\nu=T^{\mu\rho}{}_{\nu\rho}
            \end{aligned}
            \right.
            $$
            """,
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: contractions
    # remark: trace
    lk.remark(
        [
            r"""
            For $T\in\Gamma(TM^1_1)$,

            > $T:\Gamma(TM)\longrightarrow\Gamma(TM)$ (linear map)
            """,
            lk.aside(
                r"> > $\Longrightarrow$ &nbsp; $\mk{\hat T}\in C^\infty(M,\mathbb R)=\Gamma(TM^0_0)$ is the trace",
                r"$\hat T=\mathrm{tr}(T)\overset{\varphi}{=}T^\mu{}_\mu$<br>(sum of diagonal entries)",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Ricci
    # section
    lk.section("Ricci and scalar curvatures")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Ricci
    # definition: Ricci tensor
    lk.definition(
        r"""
        The **Ricci tensor** of $(M,g)$ is the contraction of $\mathrm{Riem}$

        $$
        \begin{aligned}
        \mathrm{Riem}&\overset{\varphi}{=}R^\mu{}_{\nu\rho\sigma}\,\partial_\mu\,dx^\nu dx^\rho dx^\sigma&&\in\Gamma(TM^1_3)\\
        \leadsto\quad\mathrm{Ric}&\overset{\varphi}{=}\underbrace{R^\rho{}_{\mu\rho\nu}}_{\footnotesize R_{\mu\nu}}\,dx^\mu dx^\nu&&\in\Gamma(TM^0_2)
        \end{aligned}
        $$
        """,
        label="def-ricci",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Ricci
    # theorem: symmetries of Riem
    lk.theorem(
        [
        r"""
        - $\mathrm{Riem}(X,Y)\,Z=-\mathrm{Riem}(Y,X)\,Z$
        - $g\big(\mathrm{Riem}(X,Y)\,Z,W\big)=-g\big(Z,\mathrm{Riem}(X,Y)\,W\big)$
        - $\mathrm{Riem}(X,Y)\,Z+\mathrm{Riem}(Y,Z)\,X+\mathrm{Riem}(Z,X)\,Y=0$
        """,
        lk.aside(
        r"""
        $$
        \begin{aligned}
        \Longrightarrow\quad&R^\mu{}_{\nu\rho\sigma}=-R^\mu{}_{\nu\sigma\rho}\qquad
        \underbrace{g_{\mu\lambda}R^\lambda{}_{\nu\rho\sigma}}_{\footnotesize R_{\mu\nu\rho\sigma}}=-\underbrace{g_{\lambda\nu}R^\lambda{}_{\mu\rho\sigma}}_{\footnotesize -R_{\nu\mu\rho\sigma}}\\[0.6em]
        &R^\mu{}_{\nu\rho\sigma}+R^\mu{}_{\rho\sigma\nu}+R^\mu{}_{\sigma\nu\rho}=0\\[0.4em]
        \Longrightarrow\quad&R^\rho{}_{\mu\rho\nu}=-R^\rho{}_{\mu\nu\rho}=R_{\mu\nu}\qquad R^\rho{}_{\rho\mu\nu}=0\\
        &\qquad \mk{R_{\mu\nu}+0-R_{\nu\mu}=0}
        \end{aligned}
        $$
        """,
        "contracting the cyclic identity",
        at="last",
        ),
        ],
        title=r"symmetries of $\mathrm{Riem}$",
        label="thm-symmetries",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Ricci
    # remark: Ric
    lk.remark(
        r"""
        $\mathrm{Ric}$ is the only non-zero contraction of $\mathrm{Riem}$

        $\mathrm{Ric}$ is symmetric!
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: scalar curvature
    # definition: scalar curvature
    lk.definition(
        [
            r"The **scalar curvature** of $(M,g)$ is the contraction of Ricci (with the metric).",
            lk.aside(
                r"""
                $$
                \begin{aligned}
                \mathrm{Ric}&\overset{\varphi}{=}R_{\mu\nu}\,dx^\mu dx^\nu&&\in\Gamma(TM^{\mk{0}}_2)\\
                \leadsto\quad g^{-1}\otimes\mathrm{Ric}&\overset{\varphi}{=}g^{\mu\nu}R_{\rho\sigma}\,\partial_\mu\partial_\nu\,dx^\rho dx^\sigma&&\in\Gamma(TM^2_2)\\
                \leadsto\quad g^{-1}\otimes\mathrm{Ric}&\xmapsto[\text{twice}]{\text{contraction}}S\overset{\varphi}{=}g^{\mu\nu}R_{\mu\nu}&&\in C^\infty(M,\mathbb R)
                \end{aligned}
                $$
                """,
                [(1, "no vector components")],
                rows=3,
            ),
        ],
        label="def-scalar",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: scalar curvature
    # remark: metric contractions
    lk.remark(
        r"""
        Using the metric and the inverse metric, we can contract pairs of vectors and pairs of covectors!
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: matter
    # section
    lk.section("Matter")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: matter
    # lead-in: mass density depends on the observer
    lk.prose(
        lk.aside(
            r"Newton: &nbsp; source of gravity $=$ <span class='lk-mark'>mass density $\rho$</span>",
            "single function",
        ),
        r"""
        Relativity: &nbsp; mass density depends on the observer!

        > $\Longrightarrow$ &nbsp; cannot be described by one function alone!
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: matter
    # lead-in: dust, 4-momentum density
    lk.prose(
        r"""
        Consider a cloud of non-interacting particles (dust)

        For each observer $\gamma$ in $M$, $\lVert\gamma'(t)\rVert^2=-1$, let
        """,
        lk.aside(
            r"> $\varepsilon_{\gamma(t)}=$ energy density, &nbsp; $\mk{\pi_{\gamma(t)}}=$ momentum density",
            r"$\pi_{\gamma(t)}\in\gamma'(t)^\perp$",
        ),
        r"""
        of the dust per unit of volume relative to $\gamma$ at $\gamma(t)$

        > $\Longrightarrow$ &nbsp; $J_{\gamma(t)}=\varepsilon_{\gamma(t)}\,\gamma'(t)+\pi_{\gamma(t)}$ (4-momentum density)

        $\leadsto$ &nbsp; $J_\gamma$ depends on $\gamma$, but it can be encoded in a single observer independent quantity
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: matter
    # definition: energy-momentum tensor of the dust
    lk.definition(
        r"""
        The **energy-momentum tensor** of the dust is the symmetric $(0,2)$-tensor $T\in\Gamma(TM^0_2)$ such that
        for each observer $\gamma(t)$ and $X_{\gamma(t)}\in T_{\gamma(t)}M$

        $$
        T(\gamma'(t),X)=-g(J_{\gamma(t)},X)
        $$

        $$
        \leadsto\quad
        \begin{cases}
        T(\gamma'(t),\gamma'(t))=\varepsilon_{\gamma(t)}\\
        T(\gamma'(t),X)=-g(\pi_{\gamma(t)},X) & \text{for } g(\gamma'(t),X)=0
        \end{cases}
        $$
        """,
        label="def-energy-momentum",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: matter
    # consequence: dust particle as observer
    lk.prose(
        r"""
        $\leadsto$ &nbsp; if $\gamma(t)$ is itself a dust particle

        > $\Longrightarrow$ &nbsp; $\pi_{\gamma(t)}=0$, &nbsp; $J_{\gamma(t)}=\varepsilon_{\gamma(t)}\,\gamma'(t)$
        """,
        lk.aside(
            r"> $\Longrightarrow$ &nbsp; $\varepsilon_{\gamma(t)}=\mk{\rho(\gamma(t))}=T(\gamma'(t),\gamma'(t))$",
            r"$\rho$ = rest mass density of the dust",
        ),
        r"""
        > > $\leadsto$ &nbsp; $T_{tt}=\rho$ on a chart with $\gamma'(t)=\partial_t$
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: matter contents
    # prose: general matter contents
    lk.prose(
        r"""
        More general matter contents in $(M,g)$ are described by more general symmetric $(0,2)$-tensors $T\in\Gamma(TM^0_2)$.
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: matter contents
    # example: vacuum, dust, electromagnetic field
    lk.example(
        [
            lk.aside(
                r"$T_{\mathrm{vacuum}}=0$, &nbsp; $T_{\mathrm{dust}}\overset{\varphi}{=}\rho\,\mk{u_\mu}u_\nu\,dx^\mu dx^\nu$",
                r"$\lVert u\rVert^2=-1$",
            ),
            lk.aside(
                r"$T_{\mathrm{EM}}\overset{\varphi}{=}\dfrac{1}{4\pi}\Big(\mk{F_{\mu\rho}}F_\nu{}^\rho-\dfrac14\,g_{\mu\nu}F_{\rho\sigma}F^{\rho\sigma}\Big)\,dx^\mu dx^\nu$",
                r"$F_{\mu\nu}=-F_{\nu\mu}$",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: covariant derivatives
    # section
    lk.section("Covariant derivatives of tensor fields")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: covariant derivatives
    # lead-in: Leibniz rule
    lk.prose(
        r"""
        We can extend covariant derivatives from vector fields to tensor fields via the Leibniz rule.

        - For covector fields $\alpha\in\Gamma(T^*M)$ define $\nabla_X\alpha\in\Gamma(T^*M)$ so that

        $$
        X(\alpha(Y))=(\nabla_X\alpha)(Y)+\alpha(\nabla_XY)
        $$

        <span class="lk-vconn"><span>$\varphi$</span><span class="lk-vconn-arrow">$\leadsto$</span></span>

        $$
        \begin{aligned}
        X^\mu\partial_\mu(\alpha_\rho Y^\rho)&=(\nabla_X\alpha)_\mu Y^\mu+\alpha_\rho\big(X^\mu\partial_\mu Y^\rho+\Gamma^\rho_{\mu\nu}X^\mu Y^\nu\big)\\
        \Longleftrightarrow\quad(\nabla_X\alpha)_\nu&=X^\mu\big(\underbrace{\partial_\mu\alpha_\nu-\Gamma^\rho_{\mu\nu}\,\alpha_\rho}_{\footnotesize \nabla_\mu\alpha_\nu}\big)
        \end{aligned}
        $$

        - For tensor products $T=\alpha\otimes\beta\in\Gamma(TM^0_2)$

        $$
        \begin{aligned}
        \nabla_X(\alpha\otimes\beta)&=(\nabla_X\alpha)\otimes\beta+\alpha\otimes(\nabla_X\beta)\\
        \Longrightarrow\quad(\nabla_XT)_{\mu\nu}&=X^\rho\big(\underbrace{\partial_\rho T_{\mu\nu}-\Gamma^\lambda_{\rho\mu}T_{\lambda\nu}-\Gamma^\lambda_{\rho\nu}T_{\mu\lambda}}_{\footnotesize \nabla_\rho T_{\mu\nu}}\big)
        \end{aligned}
        $$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: covariant derivatives
    # definition: covariant derivative of a tensor
    lk.definition(
        r"""
        For $T\in\Gamma(TM^r_s)$, $\nabla T\in\Gamma(TM^r_{s+1})$ is called the **covariant derivative** of $T$.

        $$
        \leadsto\quad\nabla T\overset{\varphi}{=}\nabla_\rho T_{\mu\nu}\,dx^\rho dx^\mu dx^\nu\in\Gamma(TM^0_3)\quad\text{for }T\in\Gamma(TM^0_2)
        $$
        """,
        label="def-covariant-tensor",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: covariant derivatives
    # definition: divergence
    lk.definition(
        r"""
        A **divergence** of a tensor $T$ is a contraction of its covariant derivative.

        $$
        \leadsto\quad\nabla\cdot T=\widehat{\nabla T}\overset{\varphi}{=}g^{\rho\sigma}\,\nabla_\rho T_{\sigma\mu}\,dx^\mu\in\Gamma(TM^0_1)
        $$
        """,
        label="def-divergence",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: conservation
    # section
    lk.section(r"Conservation of energy on $(M,g)$")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: conservation
    # statement: conservation of energy
    lk.prose(
        r"""
        For $T\in\Gamma(TM^0_2)$ the energy-momentum tensor, the contraction $\nabla\cdot T\in\Gamma(TM^0_1)$ of $\nabla T\in\Gamma(TM^0_3)$
        must vanish everywhere!

        $$
        \nabla^\mu T_{\mu\nu}=0
        $$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: conservation
    # example: inertial chart in Minkowski space
    lk.example(
        [
            r"In an inertial chart in $\mathbb M^4$: &nbsp; $\eta=-dt\,dt+dx\,dx+dy\,dy+dz\,dz$",
            lk.aside(
                r"> $\leadsto$ &nbsp; ${-\partial_tT_{tt}}+\delta^{ij}\partial_iT_{jt}=-(\partial_t\varepsilon+\partial_i\pi^i)=0$",
                r"$T_{tt}=\varepsilon$, $T_{jt}=-\pi_j$",
            ),
            r"> > $\Longrightarrow$ &nbsp; $\displaystyle\frac{d}{dt}\int_V\varepsilon\,dV=-\int_{\partial V}\pi\cdot dA$",
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Einstein equation
    # lead-in: back to Newton's gravity
    lk.prose(
        r"Back to Newton's gravity as a geodesic equation",
        lk.aside(
            r"> $R_{tt}\approx4\pi\rho=4\pi T_{tt}$ &nbsp; $\leadsto$ &nbsp; $\mk{\mathrm{Ric}\approx4\pi T}$",
            r"not compatible with<br>energy conservation…",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Einstein equation
    # theorem: divergence of Ric
    lk.theorem(
        r"""
        On any $(M,g)$

        $$
        \nabla\cdot\mathrm{Ric}=\frac12\,dS
        $$

        $\leadsto$ &nbsp; $\nabla\cdot\mathrm{Ric}\neq0$ unless $S$ is constant
        """,
        label="thm-div-ric",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Einstein equation
    # theorem: Einstein tensor
    lk.theorem(
        r"""
        The only divergence-free $(0,2)$-tensor constructed via contractions of $\mathrm{Riem}$ is

        $$
        G=\mathrm{Ric}-\frac12\,S\,g\qquad(\text{the Einstein tensor})
        $$

        $\leadsto$ &nbsp; up to a constant factor and adding $\Lambda g$, $\Lambda\in\mathbb R$
        """,
        label="thm-einstein-tensor",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Einstein equation
    # definition: Einstein equation
    lk.definition(
        r"""
        Given an energy-momentum tensor $T$, the **Einstein equation** on $(M,g)$ is

        $$
        \mathrm{Ric}-\frac12\,S\,g=8\pi T
        $$
        """,
        label="def-einstein",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: Einstein equation
    # remark: back to Newton
    lk.remark(
        [
            r"""
            Contraction with $g^{-1}$:

            > $g^{\mu\nu}\Big(R_{\mu\nu}-\dfrac12\,S\,g_{\mu\nu}\Big)=S-2S=-S=8\pi\hat T$

            > > $\Longrightarrow$ &nbsp; $\mathrm{Ric}=8\pi\Big(T-\dfrac12\,\hat T\,g\Big)$

            $\leadsto$ &nbsp; dust, on a chart with $\gamma'(t)=\partial_t$: &nbsp; $T_{tt}=\rho$, &nbsp; $\hat T=-\rho$
            """,
            lk.aside(
                r"> $\Longrightarrow$ &nbsp; $R_{tt}=8\pi\Big(\rho+\dfrac12\,\rho\,\mk{g_{tt}}\Big)\approx4\pi\rho$",
                r"$g_{tt}\approx-1$",
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
