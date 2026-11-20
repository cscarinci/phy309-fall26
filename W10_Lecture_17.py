import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 • Lecture 17 • Tensor fields", css_file="phy309.css")


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

    return BLUE, definition, header


@app.cell(hide_code=True)
def _(header):
    header("Lecture 17", "Week 10", "Lecture 17 • Tensor fields")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    Covector fields $\leftrightsquigarrow$ Dual vector fields $\leftrightsquigarrow$ 1-form fields

    $$
    \alpha : p \in M \longmapsto \alpha_p \in \underbrace{(T_pM)^*}_{\mathclap{\footnotesize \begin{matrix} \text{space of linear} \\ \text{functions on } T_pM \end{matrix}}\vphantom{\footnotesize \begin{matrix} \text{space of linear} \\ \text{functions on } T_pM \end{matrix}}} = T^*_pM \quad \leadsto \quad \begin{matrix} \text{cotangent space} \\ \text{to } M \text{ at } p \end{matrix}
    $$

    $$
    \begin{aligned}
    \alpha : \Gamma(TM) &\longrightarrow C^\infty(M, \mathbb{R}) \\
    X &\longmapsto \alpha(X) : p \longmapsto \alpha_p(X_p)
    \end{aligned}
    $$

    $$
    \begin{aligned}
    \alpha \in \Gamma(T^*M) &\leadsto \text{space of smooth covector fields} \\[8pt]
    &= \text{space of } C^\infty(M, \mathbb{R})\text{-linear functionals on } \Gamma(TM)
    \end{aligned}
    $$

    Charts:

    $$
    \begin{aligned}
    X &\overset{\varphi}{=} X^i\, \partial_i & \qquad X^i &= X(x^i) \\[4pt]
    \alpha &\overset{\varphi}{=} \alpha_i\, dx^i & \qquad \alpha_i &= \alpha(\partial_i)
    \end{aligned}
    \qquad \leadsto \quad \smash[b]{\underbrace{dx^i(\partial_j) = \delta^i_j}_{\footnotesize \text{duality}}}
    $$

    $$
    \Longrightarrow \quad \alpha(X) \overset{\varphi}{=} \alpha_i X^i = \smash[b]{\underbrace{\begin{bmatrix} \alpha_1 & \cdots & \alpha_m \end{bmatrix}}_{\footnotesize \text{row of functions}}} \underbrace{\begin{bmatrix} X^1 \\ \vdots \\ X^m \end{bmatrix}}_{\footnotesize \text{column of functions}}
    $$

    **In this lecture:** tensor fields

    **References:** <span style="white-space: nowrap">Schutz 3.3–3.6;</span> <span style="white-space: nowrap">Carroll 2.4;</span> <span style="white-space: nowrap">Sasane 2.6, 3.5–3.6, 4.1–4.3</span>

    ## III.4 &nbsp; Tensor fields
    """)
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            definition(
                r"""
    Given $\alpha, \beta \in \Gamma(T^*M)$ covector fields

    $$
    \begin{aligned}
    \alpha : \Gamma(TM) &\longrightarrow C^\infty(M, \mathbb{R}) \\
    \beta : \Gamma(TM) &\longrightarrow C^\infty(M, \mathbb{R})
    \end{aligned}
    \qquad C^\infty(M, \mathbb{R})\text{-linear}
    $$

    we define the tensor product of $\alpha$ and $\beta$

    $$
    \alpha \otimes \beta : \Gamma(TM) \times \Gamma(TM) \longrightarrow C^\infty(M, \mathbb{R})
    $$

    as the $C^\infty(M, \mathbb{R})$-bilinear functional on $\Gamma(TM) \times \Gamma(TM)$

    $$
    (\alpha \otimes \beta)(X, Y) = \alpha(X) \cdot \beta(Y)
    $$
    """,
                "Tensor product",
            ),
            mo.md(
                r"""
    In charts &nbsp; $\alpha \overset{\varphi}{=} \alpha_i\, dx^i$, &nbsp; $\beta \overset{\varphi}{=} \beta_j\, dx^j$

    $$
    \begin{aligned}
    \Longrightarrow \quad \alpha \otimes \beta &\overset{\varphi}{=} \alpha_i \beta_j\, dx^i \otimes dx^j \\[8pt]
    &= \begin{bmatrix} \alpha_1 & \cdots & \alpha_m \end{bmatrix}^t \begin{bmatrix} \beta_1 & \cdots & \beta_m \end{bmatrix} \\[8pt]
    &= \begin{bmatrix} \alpha_1 \beta_1 & \cdots & \alpha_1 \beta_m \\ \vdots & \ddots & \vdots \\ \alpha_m \beta_1 & \cdots & \alpha_m \beta_m \end{bmatrix}
    \end{aligned}
    $$

    <span class="chain">$\displaystyle (\alpha \otimes \beta)(X, Y) \overset{\varphi}{=} \alpha_i X^i\, \beta_j Y^j$ $\displaystyle = \begin{bmatrix} X^1 \\ \vdots \\ X^m \end{bmatrix}^t \begin{bmatrix} \alpha_1 & \cdots & \alpha_m \end{bmatrix}^t \begin{bmatrix} \beta_1 & \cdots & \beta_m \end{bmatrix} \begin{bmatrix} Y^1 \\ \vdots \\ Y^m \end{bmatrix}$</span>

    **Remark.** In this “matrix of components” representation we are writing

    $$
    \begin{aligned}
    \partial_i &= \begin{bmatrix} 0 \\ \vdots \\ 0 \\ 1 \\ 0 \\ \vdots \\ 0 \end{bmatrix} \! \begin{matrix} \phantom{0} \\ \phantom{\vdots} \\ \phantom{0} \\ \leftarrow i \\ \phantom{0} \\ \phantom{\vdots} \\ \phantom{0} \end{matrix}
    & & \begin{matrix} \text{local basis of} \\ \text{coordinate vector fields} \end{matrix} \\[10pt]
    dx^i &= {\overset{\normalsize \begin{matrix} i \\ \downarrow \end{matrix}}{\begin{bmatrix} 0 & \cdots & 0 & 1 & 0 & \cdots & 0 \end{bmatrix}}}
    & & \begin{matrix} \text{local basis of} \\ \text{coordinate covector fields} \\ = \text{linear form fields} \end{matrix} \\[34pt]
    dx^i \otimes dx^j &= \begin{bmatrix} 0 & \cdots & \overset{\textstyle ij}{\downarrow} & \cdots & 0 \\ \cdots & 0 & 1 & 0 & \cdots \\ 0 & \cdots & \cdots & \cdots & 0 \end{bmatrix}
    & & \begin{matrix} \text{local basis of coordinate} \\ \text{bilinear form fields} \end{matrix}
    \end{aligned}
    $$

    $\Longrightarrow$ &nbsp; more general $C^\infty(M, \mathbb{R})$-bilinear functionals

    $$
    T : \Gamma(TM) \times \Gamma(TM) \longrightarrow C^\infty(M, \mathbb{R})
    $$

    can be written in charts as

    $$
    T \overset{\varphi}{=} \underbrace{T_{ij}\, dx^i \otimes dx^j}_{\mathclap{\footnotesize \begin{matrix} C^\infty(M, \mathbb{R})\text{-linear combinations of} \\ \text{tensor products of covector fields} \end{matrix}}\vphantom{\footnotesize \begin{matrix} C^\infty(M, \mathbb{R})\text{-linear combinations of} \\ \text{tensor products of covector fields} \end{matrix}}}, \qquad T_{ij} = T(\partial_i, \partial_j)
    $$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            definition(
                r"""
    A $C^\infty(M, \mathbb{R})$-bilinear functional of vector fields

    $$
    T : \Gamma(TM) \times \Gamma(TM) \longrightarrow C^\infty(M, \mathbb{R})
    $$

    is called an order 2 covariant tensor field
    """,
                "Order 2 covariant tensor field",
            ),
            mo.md(
                r"""
    **Remark.** A metric field is a special type of order 2 covariant tensor, satisfying $\underbrace{\text{extra properties}}_{\footnotesize \mathclap{\begin{matrix} \text{symmetry,} \\ \text{well-defined signature} \end{matrix}}\rule[-0.35em]{0pt}{0pt}}$!

    In particular, we can also write

    $$
    g \overset{\varphi}{=} g_{ij}\, dx^i \otimes dx^j
    $$

    **Example.**

    <span class="chain">$\displaystyle g_{\mathrm{sch}} \overset{\Psi}{=} -\Big(1 - \frac{2M}{r}\Big)\, dt \otimes dt$ $\displaystyle {} + \frac{1}{\big(1 - \frac{2M}{r}\big)}\, dr \otimes dr$ $\displaystyle {} + r^2 \smash[b]{\underbrace{\big(d\phi \otimes d\phi + (\sin\phi)^2\, d\theta \otimes d\theta\big)}_{g_{\mathbb{S}^2}}}$</span>

    **Remark.**

    $$
    \begin{aligned}
    X : \Gamma(T^*M) &\longrightarrow C^\infty(M, \mathbb{R}) \\
    \alpha &\longmapsto \alpha(X)
    \end{aligned}
    $$

    $\leadsto$ &nbsp; vector fields can also be seen as linear functionals of covector fields!

    $$
    \begin{aligned}
    X \otimes Y : \Gamma(T^*M) \times \Gamma(T^*M) &\longrightarrow C^\infty(M, \mathbb{R}) \\
    (\alpha, \beta) &\longmapsto (X \otimes Y)(\alpha, \beta) = \alpha(X)\, \beta(Y)
    \end{aligned}
    $$

    $\leadsto$ &nbsp; order 2 contravariant tensor fields

    $$
    \begin{aligned}
    X \otimes \beta : \Gamma(T^*M) \times \Gamma(TM) &\longrightarrow C^\infty(M, \mathbb{R}) \\
    (\alpha, Y) &\longmapsto (X \otimes \beta)(\alpha, Y) = \alpha(X)\, \beta(Y)
    \end{aligned}
    $$

    $\leadsto$ &nbsp; 1-contravariant, 1-covariant tensor field
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(definition, mo):
    mo.vstack(
        [
            definition(
                r"""
    For each $r, s \in \mathbb{N}$ pair of natural numbers a $(r, s)$-tensor field <span class="nw">($r$-contravariant, $s$-covariant)</span> is a $C^\infty(M, \mathbb{R})$-multilinear functional

    <span class="chain">$\displaystyle T : \smash[b]{\underbrace{\Gamma(T^*M) \times \cdots \times \Gamma(T^*M)}_{\footnotesize r}} \times \smash[b]{\underbrace{\Gamma(TM) \times \cdots \times \Gamma(TM)}_{\footnotesize s}}$ $\displaystyle \longrightarrow C^\infty(M, \mathbb{R})$</span>

    $$
    \begin{aligned}
    \leadsto \quad T &\overset{\varphi}{=} T^{i_1 \cdots i_r}{}_{j_1 \cdots j_s}\, \partial_{i_1} \otimes \cdots \otimes \partial_{i_r} \otimes dx^{j_1} \otimes \cdots \otimes dx^{j_s} \\[6pt]
    T^{i_1 \cdots i_r}{}_{j_1 \cdots j_s} &= T(dx^{i_1}, \ldots, dx^{i_r}, \partial_{j_1}, \ldots, \partial_{j_s}) \in C^\infty(M, \mathbb{R})
    \end{aligned}
    $$

    We denote the space of all smooth $(r, s)$-tensor fields by

    $$
    \begin{aligned}
    \Gamma\big( \underbrace{TM \otimes \cdots \otimes TM}_{\footnotesize r} \otimes \underbrace{T^*M \otimes \cdots \otimes T^*M}_{\footnotesize s} \big) &= \Gamma(TM^{\otimes r} \otimes T^*M^{\otimes s}) \\[8pt]
    &= \Gamma(TM^r_s)
    \end{aligned}
    $$
    """,
                "$(r, s)$-tensor field",
            ),
            mo.md(
                r"""
    **Remark.** Under change of charts $\tilde\varphi \circ \varphi^{-1}$, &nbsp; $(r, s) = (1, 3)$

    $$
    R \overset{\varphi}{=} R^i{}_{jkl}\, \partial_i \otimes dx^j \otimes dx^k \otimes dx^l \overset{\tilde\varphi}{=} \tilde R^m{}_{npq}\, \tilde\partial_m \otimes d\tilde x^n \otimes d\tilde x^p \otimes d\tilde x^q
    $$

    $$
    \iff \quad R^i{}_{jkl} = \frac{\partial x^i}{\partial \tilde x^m}\, \tilde R^m{}_{npq}\, \frac{\partial \tilde x^n}{\partial x^j}\, \frac{\partial \tilde x^p}{\partial x^k}\, \frac{\partial \tilde x^q}{\partial x^l}
    $$

    **Remark.** Given a metric field $g \in \Gamma(TM^0_2)$

    $$
    \begin{aligned}
    & \begin{aligned}
    g : \Gamma(TM) \times \Gamma(TM) &\longrightarrow C^\infty(M, \mathbb{R}) \qquad C^\infty(M, \mathbb{R})\text{-bilinear} \\
    (X, Y) &\longmapsto g(X, Y)
    \end{aligned} \\[14pt]
    & \quad \begin{aligned}
    \iff \quad g : \Gamma(TM) &\longrightarrow \Gamma(T^*M) \qquad C^\infty(M, \mathbb{R})\text{-linear} \\
    Y &\longmapsto g(\cdot, Y) = \alpha \qquad \text{such that } \alpha(X) = g(X, Y)
    \end{aligned}
    \end{aligned}
    $$

    $g_p$ Riemannian or Minkowski at each $p \in M$

    $$
    \begin{array}{l}
    \begin{alignedat}{2}
    \Longrightarrow \quad & & g^{-1} : \Gamma(T^*M) &\longrightarrow \Gamma(TM) \qquad \text{inverse map} \\
    & & \alpha &\longmapsto g^{-1}(\alpha, \cdot) = Y \quad \text{such that } g(X, Y) = \alpha(X)
    \end{alignedat} \\[24pt]
    \begin{alignedat}{2}
    \Longrightarrow \quad & & g^{-1} : \Gamma(T^*M) \times \Gamma(T^*M) &\longrightarrow C^\infty(M, \mathbb{R}) \\
    & & (\alpha, \beta) &\longmapsto g^{-1}(\alpha, \beta)
    \end{alignedat}
    \end{array}
    $$

    In charts

    <span class="chain">$\displaystyle g \overset{\varphi}{=} g_{ij}\, dx^i \otimes dx^j$ &emsp; $\displaystyle g(\cdot, Y) \overset{\varphi}{=} \smash[t]{\overbrace{g_{ij} Y^j}^{\mathclap{\footnotesize \text{denoted } Y_i}}} dx^i = \alpha_i\, dx^i$<br>$\displaystyle g^{-1} \overset{\varphi}{=} g^{ij}\, \partial_i \otimes \partial_j$ &emsp; $\displaystyle g^{-1}(\alpha, \cdot) \overset{\varphi}{=} \smash[b]{\underbrace{g^{ij} \alpha_i}_{\mathclap{\footnotesize \text{denoted } \alpha^j}}} \partial_j = Y^j\, \partial_j$</span>

    <span class="chain">$\displaystyle \iff \quad g^{ik} g_{kj} = \delta^i_j, \quad$ $\displaystyle g_{ik} g^{kj} = \delta^j_i$<br>$\displaystyle \leadsto \quad [g^{-1}] = [g]^{-1}$<br>$\displaystyle [g(\cdot, Y)] = \big([g][Y]\big)^t, \quad$ $\displaystyle [g^{-1}(\alpha, \cdot)] = \big([\alpha][g^{-1}]\big)^t$</span>

    **Example.**

    $$
    \begin{aligned}
    g_{\mathbb{S}^2} &\overset{\psi}{=} d\phi \otimes d\phi + (\sin\phi)^2\, d\theta \otimes d\theta \\[4pt]
    g^{-1}_{\mathbb{S}^2} &\overset{\psi}{=} \partial_\phi \otimes \partial_\phi + (\sin\phi)^{-2}\, \partial_\theta \otimes \partial_\theta \in \Gamma(TM^2_0)
    \end{aligned}
    $$

    $$
    [g_{\mathbb{S}^2}] \overset{\psi}{=} \begin{bmatrix} 1 & 0 \\ 0 & (\sin\phi)^2 \end{bmatrix} \qquad [g^{-1}_{\mathbb{S}^2}] \overset{\psi}{=} \begin{bmatrix} 1 & 0 \\ 0 & (\sin\phi)^{-2} \end{bmatrix} = [g_{\mathbb{S}^2}]^{-1}
    $$

    <span class="chain">$\displaystyle g_{\mathrm{sch}} \overset{\Psi}{=} -\Big(1 - \frac{2M}{r}\Big)\, dt \otimes dt$ $\displaystyle {} + \frac{dr \otimes dr}{\big(1 - \frac{2M}{r}\big)}$ $\displaystyle {} + r^2 \big(d\phi \otimes d\phi + (\sin\phi)^2\, d\theta \otimes d\theta\big)$</span>

    <span class="chain">$\displaystyle g_{\mathrm{sch}}^{-1} \overset{\Psi}{=} -\frac{\partial_t \otimes \partial_t}{\big(1 - \frac{2M}{r}\big)}$ $\displaystyle {} + \Big(1 - \frac{2M}{r}\Big)\, \partial_r \otimes \partial_r$ $\displaystyle {} + \frac{1}{r^2} \Big(\partial_\phi \otimes \partial_\phi + \frac{1}{(\sin\phi)^2}\, \partial_\theta \otimes \partial_\theta\Big)$</span>
    """
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
