import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 17 · Tensor fields", css_file="lecturekit/style.css")


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
    lk.lecture(17, "Tensor fields")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        lk.aside(
            r"$\alpha:p\in M\longmapsto\alpha_p\in\mk{(T_pM)^*}=\mk{T^*_pM}$",
            r"$(T_pM)^*$ = space of linear functions on $T_pM$<br>$T^*_pM$ = cotangent space to $M$ at $p$",
        ),
        r"$\displaystyle\begin{aligned}\alpha:\Gamma(TM)&\longrightarrow C^\infty(M,\mathbb R)\\X&\longmapsto\alpha(X):p\longmapsto\alpha_p(X_p)\end{aligned}$",
        lk.aside(
            r"$\alpha\in\mk{\Gamma(T^*M)}$",
            r"space of smooth covector fields<br>= space of $C^\infty(M,\mathbb R)$-linear functionals on $\Gamma(TM)$",
        ),
        lk.aside(
            r"Charts: &nbsp; $X\overset{\varphi}{=}\mk{X^i}\,\partial_i$, &nbsp; $\alpha\overset{\varphi}{=}\mk{\alpha_i}\,dx^i$ &nbsp; $\leadsto$ &nbsp; $\underbrace{dx^i(\partial_j)=\delta^i{}_j}_{\footnotesize\text{duality}}$",
            r"$X^i=X(x^i)$, &nbsp; $\alpha_i=\alpha(\partial_i)$",
        ),
        lk.gap(),
        r"""
        > $\Longrightarrow$ &nbsp; $\alpha(X)\overset{\varphi}{=}\alpha_iX^i=\underbrace{\begin{bmatrix}\alpha_1&\cdots&\alpha_m\end{bmatrix}}_{\footnotesize\text{row of functions}}\underbrace{\begin{bmatrix}X^1\\\vdots\\X^m\end{bmatrix}}_{\mathrlap{\footnotesize\text{column of functions}}}$
        """,
        topic=r"Covector fields &nbsp;$\leftrightsquigarrow$&nbsp; Dual vector fields &nbsp;$\leftrightsquigarrow$&nbsp; 1-form fields",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals("Tensor fields", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("Schutz 3.3–3.6; Carroll 2.4; Sasane 2.6, 3.5–3.6, 4.1–4.3")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tensor product
    # definition: tensor product of covector fields
    lk.definition(
        r"""
        Given $\alpha,\beta\in\Gamma(T^*M)$ covector fields

        $$
        \begin{aligned}
        \alpha:\Gamma(TM)&\longrightarrow C^\infty(M,\mathbb R)\\
        \beta:\Gamma(TM)&\longrightarrow C^\infty(M,\mathbb R)
        \end{aligned}
        \qquad C^\infty(M,\mathbb R)\text{-linear},
        $$

        we define the **tensor product** of $\alpha$ and $\beta$

        $$
        \alpha\otimes\beta:\Gamma(TM)\times\Gamma(TM)\longrightarrow C^\infty(M,\mathbb R),
        $$

        as the $C^\infty(M,\mathbb R)$-bilinear functional on $\Gamma(TM)\times\Gamma(TM)$

        $$
        (\alpha\otimes\beta)(X,Y)=\alpha(X)\cdot\beta(Y).
        $$
        """,
        label="def-tensor-product",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tensor product
    # consequence: the tensor product in charts
    lk.prose(
        r"""
        In charts

        > $\alpha\overset{\varphi}{=}\alpha_i\,dx^i$, &nbsp; $\beta\overset{\varphi}{=}\beta_j\,dx^j$

        > > $\displaystyle\begin{alignedat}{2}\Longrightarrow\quad&\alpha\otimes\beta&&\overset{\varphi}{=}\alpha_i\beta_j\,dx^i\otimes dx^j\\&&&=\begin{bmatrix}\alpha_1&\cdots&\alpha_m\end{bmatrix}^t\begin{bmatrix}\beta_1&\cdots&\beta_m\end{bmatrix}=\begin{bmatrix}\alpha_1\beta_1&\cdots&\alpha_1\beta_m\\\vdots&\ddots&\vdots\\\alpha_m\beta_1&\cdots&\alpha_m\beta_m\end{bmatrix}\end{alignedat}$

        > > $\displaystyle\begin{alignedat}{2}\phantom{\Longrightarrow}\quad&(\alpha\otimes\beta)(X,Y)&&\overset{\varphi}{=}\alpha_iX^i\beta_jY^j\\&&&=\begin{bmatrix}X^1\\\vdots\\X^m\end{bmatrix}^t\begin{bmatrix}\alpha_1&\cdots&\alpha_m\end{bmatrix}^t\begin{bmatrix}\beta_1&\cdots&\beta_m\end{bmatrix}\begin{bmatrix}Y^1\\\vdots\\Y^m\end{bmatrix}\end{alignedat}$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tensor product
    # remark: matrix of components
    lk.remark(
        [
            r"In this “matrix of components” representation we are writing",
            lk.aside(
                r"""$$
                \partial_i=\begin{bmatrix}0\\\vdots\\0\\1\\0\\\vdots\\0\end{bmatrix}\begin{matrix}\\\\\\\leftarrow i\\\\\\\\\end{matrix},
                $$""",
                r"local basis of coordinate vector fields",
            ),
            lk.aside(
                r"$$dx^i=\begin{bmatrix}0&\cdots&0&\overset{\overset{\scriptstyle i}{\downarrow}}{1}&0&\cdots&0\end{bmatrix},$$",
                r"local basis of coordinate covector fields<br>= linear form fields",
            ),
            lk.aside(
                r"$$dx^i\otimes dx^j=\begin{bmatrix}0&\cdots&\cdots&\cdots&0\\\cdots&0&\overset{\overset{\scriptstyle ij}{\downarrow}}{1}&0&\cdots\\0&\cdots&\cdots&\cdots&0\end{bmatrix}.$$",
                r"local basis of coordinate bilinear form fields",
            ),
            r"""
            > $\Longrightarrow$ &nbsp; more general $C^\infty(M,\mathbb R)$-bilinear functionals

            > $$
            > T:\Gamma(TM)\times\Gamma(TM)\longrightarrow C^\infty(M,\mathbb R)
            > $$

            > can be written in charts as
            """,
            lk.aside(
                r"$$T\overset{\varphi}{=}\mk{T_{ij}\,dx^i\otimes dx^j},\qquad T_{ij}=T(\partial_i,\partial_j).$$",
                r"$C^\infty(M,\mathbb R)$-linear combinations<br>of tensor products of covector fields",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tensor fields
    # definition: order 2 covariant tensor field
    lk.definition(
        r"""
        A $C^\infty(M,\mathbb R)$-bilinear functional of vector fields

        $$
        T:\Gamma(TM)\times\Gamma(TM)\longrightarrow C^\infty(M,\mathbb R),
        $$

        is called an **order 2 covariant tensor field**
        """,
        label="def-covariant-2",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tensor fields
    # remark: metric fields
    lk.remark(
        [
            lk.aside(
                r"A metric field is a special type of order 2 covariant tensor, satisfying <span class='lk-mark'>extra properties</span>!",
                r"symmetry<br>well-defined signature",
            ),
            r"""
            In particular, we can also write

            > $g\overset{\varphi}{=}g_{ij}\,dx^i\otimes dx^j$
            """,
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tensor fields
    # example: Schwarzschild metric
    lk.example(
        r"""
        $$
        g_{\mathrm{sch}}\overset{\Psi}{=}-\Big(1-\frac{2M}{r}\Big)\,dt\otimes dt+\frac{1}{\big(1-\frac{2M}{r}\big)}\,dr\otimes dr+r^2\,\underbrace{\big(d\phi\otimes d\phi+(\sin\phi)^2\,d\theta\otimes d\theta\big)}_{\footnotesize g_{\mathrm{round}}\text{ on }\mathbb S^2}
        $$
        """,
        label="ex-schwarzschild-tensor",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tensor fields
    # remark: vector fields as functionals of covector fields
    lk.remark(
        r"""
        $X:\Gamma(T^*M)\longrightarrow C^\infty(M,\mathbb R)$, &nbsp; $\alpha\longmapsto\alpha(X)$

        > $\leadsto$ &nbsp; vector fields can also be seen as linear functionals of covector fields!

        $X\otimes Y:\Gamma(T^*M)\times\Gamma(T^*M)\longrightarrow C^\infty(M,\mathbb R)$, &nbsp; $(\alpha,\beta)\longmapsto X\otimes Y(\alpha,\beta)=\alpha(X)\beta(Y)$

        > $\leadsto$ &nbsp; order 2 contravariant tensor fields

        $X\otimes\beta:\Gamma(T^*M)\times\Gamma(TM)\longrightarrow C^\infty(M,\mathbb R)$, &nbsp; $(\alpha,Y)\longmapsto X\otimes\beta(\alpha,Y)=\alpha(X)\beta(Y)$

        > $\leadsto$ &nbsp; 1-contravariant, 1-covariant tensor field
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tensor fields
    # definition: (r, s)-tensor field
    lk.definition(
        [
            r"""
            For each $r,s\in\mathbb N$ pair of natural numbers, a **$(r,s)$-tensor field** ($r$-contravariant, $s$-covariant)<br>is a $C^\infty(M,\mathbb R)$-multilinear functional

            $$
            T:\underbrace{\Gamma(T^*M)\times\cdots\times\Gamma(T^*M)}_{r}\times\underbrace{\Gamma(TM)\times\cdots\times\Gamma(TM)}_{s}\longrightarrow C^\infty(M,\mathbb R).
            $$
            """,
            lk.aside(
                r"> $\leadsto$ &nbsp; $T\overset{\varphi}{=}\mk{T^{i_1\cdots i_r}{}_{j_1\cdots j_s}}\,\partial_{i_1}\otimes\cdots\otimes\partial_{i_r}\otimes dx^{j_1}\otimes\cdots\otimes dx^{j_s}$",
                r"$T^{i_1\cdots i_r}{}_{j_1\cdots j_s}=T(dx^{i_1},\dots,dx^{i_r},\partial_{j_1},\dots,\partial_{j_s})$<br>$\in C^\infty(M,\mathbb R)$",
            ),
            r"""
            We denote the space of all smooth $(r,s)$-tensor fields by

            $$
            \begin{aligned}
            \Gamma(\underbrace{TM\otimes\cdots\otimes TM}_{r}\otimes\underbrace{T^*M\otimes\cdots\otimes T^*M}_{s})&=\Gamma(TM^{\otimes r}\otimes T^*M^{\otimes s})\\
            &=\Gamma(TM^r_s).
            \end{aligned}
            $$
            """,
        ],
        label="def-tensor-field",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: tensor fields
    # remark: change of charts
    lk.remark(
        r"""
        Under change of charts $\tilde\varphi\circ\varphi^{-1}$

        > $(r,s)=(1,3)$

        > > $\displaystyle\begin{aligned}R&\overset{\varphi}{=}R^i{}_{jkl}\,\partial_i\otimes dx^j\otimes dx^k\otimes dx^l\\&\overset{\tilde\varphi}{=}\tilde R^m{}_{npq}\,\tilde\partial_m\otimes d\tilde x^n\otimes d\tilde x^p\otimes d\tilde x^q\end{aligned}$

        > > > $\Longleftrightarrow$ &nbsp; $\displaystyle R^i{}_{jkl}=\frac{\partial x^i}{\partial\tilde x^m}\,\tilde R^m{}_{npq}\,\frac{\partial\tilde x^n}{\partial x^j}\,\frac{\partial\tilde x^p}{\partial x^k}\,\frac{\partial\tilde x^q}{\partial x^l}$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: metric
    # remark: metric and inverse metric
    lk.remark(
        r"""
        Given a metric field $g\in\Gamma(TM^0_2)$

        > $\displaystyle\begin{alignedat}{2}g:\Gamma(TM)\times\Gamma(TM)&\longrightarrow C^\infty(M,\mathbb R)&\qquad&C^\infty(M,\mathbb R)\text{-bilinear}\\(X,Y)&\longmapsto g(X,Y)\end{alignedat}$

        > > $\displaystyle\begin{alignedat}{3}\Longleftrightarrow\quad&&g:\Gamma(TM)&\longrightarrow\Gamma(T^*M)&\qquad&C^\infty(M,\mathbb R)\text{-linear}\\&&Y&\longmapsto g(\cdot,Y)=\alpha&&\text{such that }\alpha(X)=g(X,Y)\end{alignedat}$

        $g_p$ Riemannian or Minkowski at each $p\in M$

        > $\displaystyle\begin{alignedat}{3}\Longrightarrow\quad&&g^{-1}:\Gamma(T^*M)&\longrightarrow\Gamma(TM)&\qquad&\text{inverse map}\\&&\alpha&\longmapsto g^{-1}(\alpha,\cdot)=Y&&\text{such that }g(X,Y)=\alpha(X)\end{alignedat}$

        > $\displaystyle\begin{alignedat}{3}\Longrightarrow\quad&&g^{-1}:\Gamma(T^*M)\times\Gamma(T^*M)&\longrightarrow C^\infty(M,\mathbb R)\\&&(\alpha,\beta)&\longmapsto g^{-1}(\alpha,\beta)\end{alignedat}$

        In charts

        > $$
        > \begin{aligned}
        > &\begin{alignedat}{2}
        > g&\overset{\varphi}{=}g_{ij}\,dx^i\otimes dx^j&\qquad g(\cdot,Y)&\overset{\varphi}{=}\overbrace{g_{ij}Y^j}^{\footnotesize\text{denoted }Y_i}\,dx^i=\alpha_i\,dx^i\\[0.6em]
        > g^{-1}&\overset{\varphi}{=}g^{ij}\,\partial_i\otimes\partial_j&g^{-1}(\alpha,\cdot)&\overset{\varphi}{=}\underbrace{g^{ij}\alpha_i}_{\footnotesize\text{denoted }\alpha^j}\,\partial_j=Y^j\,\partial_j
        > \end{alignedat}\\[6pt]
        > &\Longleftrightarrow\quad g^{ik}g_{kj}=\delta^i{}_j\ \text{and}\ g_{ik}g^{kj}=\delta_i{}^j.
        > \end{aligned}
        > $$

        > > $\leadsto$ &nbsp; $[g^{-1}]=[g]^{-1}$

        > > > <span class="lk-ghost">$\leadsto$ &nbsp; </span>$[g(\cdot,Y)]=([g][Y])^t$ &nbsp; and &nbsp; $[g^{-1}(\alpha,\cdot)]=([\alpha][g^{-1}])^t$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: metric
    # example: round metric and Schwarzschild metric with their inverses
    lk.example(
        [
            lk.aside(
                r"$\mk{g_{\mathbb S^2}}\overset{\psi}{=}d\phi\otimes d\phi+(\sin\phi)^2\,d\theta\otimes d\theta$ &nbsp; $\leftrightsquigarrow$ &nbsp; $\begin{bmatrix}1&0\\0&(\sin\phi)^2\end{bmatrix}$",
                r"$g_{\mathbb S^2}$ = round metric",
            ),
            lk.aside(
                r"$\mk{g^{-1}_{\mathbb S^2}}\overset{\psi}{=}\partial_\phi\otimes\partial_\phi+(\sin\phi)^{-2}\,\partial_\theta\otimes\partial_\theta\in\Gamma(TM^2_0)$ &nbsp; $\leftrightsquigarrow$ &nbsp; $\begin{bmatrix}1&0\\0&(\sin\phi)^{-2}\end{bmatrix}=\begin{bmatrix}1&0\\0&(\sin\phi)^2\end{bmatrix}^{-1}$",
                r"$g^{-1}_{\mathbb S^2}$ = inverse round metric",
            ),
            r"$\displaystyle\begin{aligned}g_{\mathrm{sch}}&\overset{\Psi}{=}-\Big(1-\frac{2M}{r}\Big)\,dt\otimes dt+\frac{dr\otimes dr}{\big(1-\frac{2M}{r}\big)}+r^2\big(d\phi\otimes d\phi+(\sin\phi)^2\,d\theta\otimes d\theta\big)\\[0.4em]g^{-1}_{\mathrm{sch}}&\overset{\Psi}{=}-\frac{\partial_t\otimes\partial_t}{\big(1-\frac{2M}{r}\big)}+\Big(1-\frac{2M}{r}\Big)\,\partial_r\otimes\partial_r+\frac{1}{r^2}\Big(\partial_\phi\otimes\partial_\phi+\frac{1}{(\sin\phi)^2}\,\partial_\theta\otimes\partial_\theta\Big)\end{aligned}$",
        ],
        label="ex-inverse-metrics",
    )
    return


if __name__ == "__main__":
    app.run()
