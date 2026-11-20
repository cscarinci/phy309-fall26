import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 • Lecture 18 • Calculus of tensor fields on manifolds", css_file="phy309.css")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    # ---- Building blocks shared by all lectures -------------------------
    BLUE = "#3f5f8f"

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

    return definition, header, theorem


@app.cell(hide_code=True)
def _(header):
    header("Lecture 18", "Week 11", "Lecture 18 • Calculus of tensor fields on manifolds")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    Tensor fields

    $T \in \Gamma(TM^r_s)$ &nbsp; $(r, s)$-tensor field

    $\leadsto$ &nbsp; $C^\infty(M, \mathbb{R})$-multilinear functionals of $r$ covectors and $s$ vectors

    $$
    \begin{aligned}
    \bullet \quad & X \overset{\varphi}{=} X^i\, \partial_i \in \Gamma(TM) = \Gamma(TM^1_0) \\[6pt]
    \bullet \quad & \alpha \overset{\varphi}{=} \alpha_i\, dx^i \in \Gamma(T^*M) = \Gamma(TM^0_1) \\[6pt]
    \bullet \quad & g \overset{\varphi}{=} g_{ij}\, dx^i \otimes dx^j \in \Gamma(T^*M \otimes T^*M) = \Gamma(TM^0_2) \\[2pt]
    & \small \leadsto \ \text{metric} = C^\infty(M, \mathbb{R})\text{-bilinear} + \text{symmetric} + \text{Euclid/Minkowski} \\[6pt]
    \bullet \quad & T \overset{\varphi}{=} T^{i_1 \cdots i_r}{}_{j_1 \cdots j_s}\, \partial_{i_1} \otimes \cdots \otimes \partial_{i_r} \otimes dx^{j_1} \otimes \cdots \otimes dx^{j_s} \in \Gamma(TM^r_s)
    \end{aligned}
    $$

    Given $g \overset{\varphi}{=} g_{ij}\, dx^i \otimes dx^j$ metric

    $$
    \begin{alignedat}{2}
    \Longrightarrow \quad & g : \ & \Gamma(TM) & \longrightarrow \Gamma(T^*M) \quad \text{is invertible} \\
    & & Y \overset{\varphi}{=} Y^i\, \partial_i & \longmapsto g(Y) \overset{\varphi}{=} g_{ij} Y^j\, dx^i \\[14pt]
    \Longrightarrow \quad & g^{-1} : \ & \Gamma(T^*M) & \longrightarrow \Gamma(TM) \\
    & & \alpha \overset{\varphi}{=} \alpha_i\, dx^i & \longmapsto g^{-1}(\alpha) \overset{\varphi}{=} g^{ij} \alpha_j\, \partial_i
    \end{alignedat}
    $$

    such that

    $$
    \begin{aligned}
    Y &= g^{-1}(g(Y)) \overset{\varphi}{=} \underbrace{g^{ij} g_{jk}}_{\footnotesize \delta^i{}_k} Y^k\, \partial_i = Y^i\, \partial_i \\[10pt]
    \alpha &= g(g^{-1}(\alpha)) \overset{\varphi}{=} \underbrace{g_{ij} g^{jk}}_{\footnotesize \delta_i{}^k} \alpha_k\, dx^i = \alpha_i\, dx^i
    \end{aligned}
    $$

    **Lowering / Raising indices** &nbsp; (convention)

    Given metric $g \overset{\varphi}{=} g_{ij}\, dx^i \otimes dx^j$ with inverse metric $g^{-1} \overset{\varphi}{=} g^{ij}\, \partial_i \otimes \partial_j$

    $$
    \begin{aligned}
    g(Y) &\overset{\varphi}{=} g_{ij} Y^j\, dx^i = Y_i\, dx^i \\[6pt]
    g^{-1}(\alpha) &\overset{\varphi}{=} g^{ij} \alpha_j\, \partial_i = \alpha^i\, \partial_i
    \end{aligned}
    $$

    $\leadsto$ &nbsp; the metric “transforms” contravariant indices into covariant indices (lowers upper indices)

    $\leadsto$ &nbsp; the inverse metric “transforms” covariant indices into contravariant indices (raises lower indices)

    In particular, sometimes we write

    $$
    \begin{aligned}
    g(X, Y) &\overset{\varphi}{=} g_{ij} X^i Y^j = X^i Y_i \\[6pt]
    g^{-1}(\alpha, \beta) &\overset{\varphi}{=} g^{ij} \alpha_i \beta_j = \alpha_i \beta^i
    \end{aligned}
    $$

    **In this lecture:** calculus of tensor fields on manifolds

    $\leadsto$ &nbsp; tensor fields model physical quantities

    $\leadsto$ &nbsp; in order to write physical laws we need to define their derivatives!

    **References:** <span style="white-space: nowrap">Schutz 3.7, 5.3–5.4, 6.3;</span> <span style="white-space: nowrap">Carroll 1.7, 3.2;</span> <span style="white-space: nowrap">Sasane 5.4, 6.1–6.4, 7.1–7.2</span>

    ## IV.1 &nbsp; Calculus of tensor fields on manifolds
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Recall.** On affine spaces we have congruence

    Given $p, q \in \mathbb{A}$ and $v \in \mathbb{V}_p = T_p \mathbb{A}$, &nbsp; $\exists!\ v' \in \mathbb{V}_q = T_q \mathbb{A}$ congruent

    $\Longrightarrow$ &nbsp; $\mathbb{V}_p = \mathbb{V}_q = \mathbb{V}$ can be identified

    A vector field $X$ on $\mathbb{A}$ is just a map &nbsp; $X : \mathbb{A} \longrightarrow \mathbb{V}$

    $\Longrightarrow$ &nbsp; we can define the derivative of $X$ along any differentiable path $\gamma : \mathbb{R} \to \mathbb{A}$:

    Let $X(t) = X(\gamma(t)) = X^i(t)\, e_i$

    $$
    \leadsto \quad \frac{d}{dt} X(t) = \lim_{h \to 0} \frac{X(t + h) - X(t)}{h} = \dot X(t) = \frac{d}{dt} X^i(t)\, e_i = \dot X^i(t)\, e_i
    $$

    $\Longrightarrow$ &nbsp; we can define the acceleration of $\gamma(t)$:

    $$
    \leadsto \quad \frac{d}{dt} \dot\gamma(t) = \lim_{h \to 0} \frac{\dot\gamma(t + h) - \dot\gamma(t)}{h} = \ddot\gamma(t)
    $$

    $\Longrightarrow$ &nbsp; we can define evolution equations for $\gamma(t)$

    $$
    \ddot\gamma(t) = F(\gamma(t), \dot\gamma(t))
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On manifolds, no congruence ...

    $\Longrightarrow$ &nbsp; something goes wrong!

    Let $X \in \Gamma(TM)$ be a vector field on $M$ and $\gamma : \mathbb{R} \to M$ be a path on $M$

    Consider $X(t) = X(\gamma(t)) \overset{\varphi}{=} X^i(t)\, \partial_i\big|_{\gamma(t)}$

    $$
    \begin{aligned}
    \Longrightarrow \quad & X^i : \mathbb{R} \to \mathbb{R} \quad \text{are smooth} \\[10pt]
    \Longrightarrow \quad & \dot X^i(t) = \frac{d}{dt} X^i(t) \quad \text{are well-defined!} \quad (\forall\, t \text{ such that } \gamma(t) \in U)
    \end{aligned}
    $$

    Why not define

    $$
    \frac{d}{dt} X(t) \overset{\varphi}{=} \dot X^i(t)\, \partial_i\big|_{\gamma(t)} \ ?
    $$

    Consider $X(t) \overset{\varphi}{=} X^i(t)\, \partial_i\big|_{\gamma(t)} \overset{\tilde\varphi}{=} \tilde X^i(t)\, \tilde\partial_i\big|_{\gamma(t)}$

    <span class="chain">$\displaystyle \begin{aligned}
    \Longrightarrow \quad & \tilde X^j(t) = \frac{\partial \tilde x^j}{\partial x^i}(\gamma(t))\, X^i(t) \\[14pt]
    \Longrightarrow \quad & \dot{\tilde X}{}^j(t) = \frac{\partial \tilde x^j}{\partial x^i}(\gamma(t))\, \dot X^i(t) + \frac{\partial^2 \tilde x^j}{\partial x^k \partial x^i}(\gamma(t))\, \dot x^k(t)\, X^i(t) \\[14pt]
    \Longrightarrow \quad & \dot X^i(t)\, \partial_i\big|_{\gamma(t)} \neq \dot{\tilde X}{}^i(t)\, \tilde\partial_i\big|_{\gamma(t)} \ !
    \end{aligned}$ $\displaystyle \text{where } \gamma(t) \overset{\varphi}{=} \varphi^{-1}\big(x^k(t)\, e_k\big) \text{ and } \dot x^k(t) = \frac{d}{dt} x^k(t)$</span>
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(
        r"""
    A covariant derivative on $M$ is, for each path $\gamma(t)$, an assignment

    $$
    \begin{aligned}
    \frac{D}{dt} : \left\{ \begin{matrix} \text{vector fields} \\ \text{along } \gamma(t) \end{matrix} \right\} &\longrightarrow \left\{ \begin{matrix} \text{vector fields} \\ \text{along } \gamma(t) \end{matrix} \right\} \\[10pt]
    X(t) &\longmapsto \frac{D}{dt} X(t)
    \end{aligned}
    $$

    such that

    $$
    \begin{aligned}
    \bullet \quad & \frac{D}{dt} \big( a X(t) + b Y(t) \big) = a\, \frac{D}{dt} X(t) + b\, \frac{D}{dt} Y(t), & & \forall\, a, b \in \mathbb{R} \\[12pt]
    \bullet \quad & \frac{D}{dt} \big( \lambda(t) X(t) \big) = \frac{d}{dt} \lambda(t)\, X(t) + \lambda(t)\, \frac{D}{dt} X(t), & & \forall\, \lambda : \mathbb{R} \to \mathbb{R} \\[12pt]
    \bullet \quad & \text{in each chart } \varphi : U \subseteq M \to \mathbb{R}^m
    \end{aligned}
    $$

    $$
    \begin{aligned}
    \frac{D}{dt} X(t) &\overset{\varphi}{=} \frac{D}{dt} \big( X^i(t)\, \partial_i\big|_{\gamma(t)} \big) \\[10pt]
    &= \frac{d}{dt} X^i(t)\, \partial_i\big|_{\gamma(t)} + X^i(t)\, \frac{D}{dt} \partial_i\big|_{\gamma(t)} \\[10pt]
    &= \dot X^i(t)\, \partial_i\big|_{\gamma(t)} + X^i(t)\, \underbrace{\dot x^j(t)\, \Gamma^k_{ij}(\gamma(t))\, \partial_k\big|_{\gamma(t)}}_{\mathclap{\footnotesize \begin{matrix} \dfrac{D}{dt} \partial_i|_{\gamma(t)} \text{ depends linearly} \\ \text{on the velocity } \dot\gamma(t) \end{matrix}}\vphantom{\footnotesize \begin{matrix} \dfrac{D}{dt} \partial_i|_{\gamma(t)} \text{ depends linearly} \\ \text{on the velocity } \dot\gamma(t) \end{matrix}}}
    \end{aligned}
    $$

    $$
    \Longrightarrow \quad \frac{D}{dt} X(t) \overset{\varphi}{=} \Big( \dot X^k(t) + X^i(t)\, \dot x^j(t)\, \Gamma^k_{ij}(\gamma(t)) \Big)\, \partial_k\big|_{\gamma(t)}
    $$

    $\Gamma^k_{ij}(\gamma(t))$ are the Christoffel symbols of the covariant derivative with respect to $\varphi$ along $\gamma(t)$
    """,
        "Covariant derivative",
    )
    return


@app.cell(hide_code=True)
def _(mo, theorem):
    mo.vstack(
        [
            mo.md(r"Do covariant derivatives exist?"),
            theorem(
                r"""
    Assuming existence, given $\varphi, \tilde\varphi$ charts on $M$

    $$
    \frac{D}{dt} X \overset{\varphi}{=} \big( \dot X^k + X^i \dot x^j\, \Gamma^k_{ij} \big)\, \partial_k \overset{\tilde\varphi}{=} \big( \dot{\tilde X}{}^l + \tilde X^m \dot{\tilde x}{}^n\, \tilde\Gamma^l_{mn} \big)\, \tilde\partial_l
    $$

    $$
    \Longleftrightarrow \quad \Gamma^k_{ij} = \underbrace{\frac{\partial x^k}{\partial \tilde x^l}\, \tilde\Gamma^l_{mn}\, \frac{\partial \tilde x^m}{\partial x^i}\, \frac{\partial \tilde x^n}{\partial x^j}}_{\mathclap{\footnotesize \begin{matrix} \text{transformation} \\ \text{of } (1, 2)\text{-tensor} \end{matrix}}\vphantom{\footnotesize \begin{matrix} \text{transformation} \\ \text{of } (1, 2)\text{-tensor} \end{matrix}}} + \underbrace{\frac{\partial x^k}{\partial \tilde x^l}\, \frac{\partial^2 \tilde x^l}{\partial x^i \partial x^j}}_{\mathclap{\footnotesize \begin{matrix} \text{non-tensorial} \\ \text{transformation!} \end{matrix}}\vphantom{\footnotesize \begin{matrix} \text{non-tensorial} \\ \text{transformation!} \end{matrix}}}
    $$
    """
            ),
            mo.md(
                r"""
    **Proof.**

    $$
    \begin{aligned}
    \tilde X^l &= \frac{\partial \tilde x^l}{\partial x^k}\, X^k \quad \Longrightarrow \quad \dot{\tilde X}{}^l = \frac{\partial \tilde x^l}{\partial x^k}\, \dot X^k + \underbrace{\frac{\partial^2 \tilde x^l}{\partial x^i \partial x^j}\, \dot x^i X^j}_{\footnotesize \text{non-tensorial}} \\[14pt]
    \dot{\tilde x}{}^n &= \frac{\partial \tilde x^n}{\partial x^j}\, \dot x^j \quad \text{and} \quad \partial_k = \frac{\partial \tilde x^l}{\partial x^k}\, \tilde\partial_l
    \end{aligned}
    $$

    $\leadsto$ &nbsp; just replace and compare <span class="qed">$\square$</span>
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(
        r"""
    Given a metric $g \in \Gamma(TM^0_2)$, we can define in each chart $\varphi$ a collection $\Gamma^k_{ij}$ of Christoffel symbols via

    $$
    \begin{aligned}
    & \Gamma^k_{ij} = \frac{1}{2}\, g^{kl} \big( \partial_i g_{lj} + \partial_j g_{il} - \partial_l g_{ij} \big)
    \end{aligned}
    $$
    """
    )
    return


if __name__ == "__main__":
    app.run()
