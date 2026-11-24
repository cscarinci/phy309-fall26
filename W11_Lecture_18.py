import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 18 · Calculus of tensor fields on manifolds", css_file="lecturekit/style.css")


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
    lk.lecture(18, "Calculus of tensor fields on manifolds")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"""
        $T\in\Gamma(TM^r_s)$ &nbsp; $(r,s)$-tensor field

        > $\leadsto$ &nbsp; $C^\infty(M,\mathbb R)$-multilinear functionals of $r$ covectors and $s$ vectors

        • &nbsp; $X\overset{\varphi}{=}X^i\,\partial_i\in\Gamma(TM)=\Gamma(TM^1_0)$

        • &nbsp; $\alpha\overset{\varphi}{=}\alpha_i\,dx^i\in\Gamma(T^*M)=\Gamma(TM^0_1)$
        """,
        lk.aside(
            r"• &nbsp; $\mk{g}\overset{\varphi}{=}g_{ij}\,dx^i\otimes dx^j\in\Gamma(T^*M\otimes T^*M)=\Gamma(TM^0_2)$",
            r"metric = $C^\infty(M,\mathbb R)$-bilinear +<br>symmetric + Euclid/Minkowski",
        ),
        r"""
        • &nbsp; $T\overset{\varphi}{=}T^{i_1\cdots i_r}{}_{j_1\cdots j_s}\,\partial_{i_1}\otimes\cdots\otimes\partial_{i_r}\otimes dx^{j_1}\otimes\cdots\otimes dx^{j_s}\in\Gamma(TM^r_s)$

        Given $g\overset{\varphi}{=}g_{ij}\,dx^i\otimes dx^j$ metric

        > $\displaystyle\begin{alignedat}{3}\Longrightarrow\quad&&g:\Gamma(TM)&\longrightarrow\Gamma(T^*M)&\qquad&\text{is invertible}\\&&Y\overset{\varphi}{=}Y^i\,\partial_i&\longmapsto g(Y)\overset{\varphi}{=}g_{ij}Y^j\,dx^i\\[0.8em]\Longrightarrow\quad&&g^{-1}:\Gamma(T^*M)&\longrightarrow\Gamma(TM)\\&&\alpha\overset{\varphi}{=}\alpha_i\,dx^i&\longmapsto g^{-1}(\alpha)\overset{\varphi}{=}g^{ij}\alpha_j\,\partial_i\end{alignedat}$

        > such that

        > $$
        > \begin{aligned}
        > Y&=g^{-1}(g(Y))\overset{\varphi}{=}\underbrace{g^{ij}g_{jk}}_{\delta^i{}_k}Y^k\,\partial_i=Y^i\,\partial_i\\[0.6em]
        > \alpha&=g(g^{-1}(\alpha))\overset{\varphi}{=}\underbrace{g_{ij}g^{jk}}_{\delta_i{}^k}\alpha_k\,dx^i=\alpha_i\,dx^i
        > \end{aligned}
        > $$
        """,
        r"Lowering / Raising indices (convention)",
        lk.under(
            r"""
            Given metric $g\overset{\varphi}{=}g_{ij}\,dx^i\otimes dx^j$ with inverse metric $g^{-1}\overset{\varphi}{=}g^{ij}\,\partial_i\otimes\partial_j$

            > $$
            > \begin{aligned}
            > g(Y)&\overset{\varphi}{=}g_{ij}Y^j\,dx^i=Y_i\,dx^i\\
            > g^{-1}(\alpha)&\overset{\varphi}{=}g^{ij}\alpha_j\,\partial_i=\alpha^i\,\partial_i
            > \end{aligned}
            > $$

            """,
            lk.aside(r"> $\leadsto$ &nbsp; the metric “transforms” contravariant indices into covariant indices", "lowers upper indices"),
            lk.aside(r"> $\leadsto$ &nbsp; the inverse metric “transforms” covariant indices into contravariant indices", "raises lower indices"),
            r"""
            In particular, sometimes we write

            > $$
            > \begin{aligned}
            > g(X,Y)&\overset{\varphi}{=}g_{ij}X^iY^j=X^iY_i\\
            > g^{-1}(\alpha,\beta)&\overset{\varphi}{=}g^{ij}\alpha_i\beta_j=\alpha_i\beta^i
            > \end{aligned}
            > $$
            """
        ),
        topic="Tensor fields",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(
        r"""
        Calculus of tensor fields on manifolds

        $\leadsto$ &nbsp; tensor fields model physical quantities

        $\leadsto$ &nbsp; in order to write physical laws we need to define their derivatives!
        """,
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("Schutz 3.7, 5.3–5.4, 6.3; Carroll 1.7, 3.2; Sasane 5.4, 6.1–6.4, 7.1–7.2")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: affine spaces
    # recall: congruence on affine spaces
    lk.recall(
        [
            r"On affine spaces we have congruence",
            lk.aside(
                r"> Given $p,q\in\mathbb A$ and $v\in\mk{\mathbb V_p}$, &nbsp; $\exists!\ v'\in\mk{\mathbb V_q}$ congruent",
                r"$\mathbb V_p=T_p\mathbb A$, &nbsp; $\mathbb V_q=T_q\mathbb A$",
            ),
            r"""
            > > $\Longrightarrow$ &nbsp; $\mathbb V_p=\mathbb V_q=\mathbb V$ can be identified

            A vector field $X$ on $\mathbb A$ is just a map &nbsp; $X:\mathbb A\longrightarrow\mathbb V$

            > $\Longrightarrow$ &nbsp; we can define the derivative of $X$ along any differentiable path $\gamma:\mathbb R\to\mathbb A$:

            > > Let $X(t)=X(\gamma(t))=X^i(t)\,e_i$

            > > > $\displaystyle\begin{aligned}\leadsto\quad\frac{d}{dt}X(t)&=\lim_{h\to0}\frac{X(t+h)-X(t)}{h}=\dot X(t)\\&=\frac{d}{dt}X^i(t)\,e_i=\dot X^i(t)\,e_i\end{aligned}$

            > $\Longrightarrow$ &nbsp; we can define the acceleration of $\gamma(t)$:

            > > $\displaystyle\begin{aligned}\leadsto\quad\frac{d}{dt}\dot\gamma(t)=\lim_{h\to0}\frac{\dot\gamma(t+h)-\dot\gamma(t)}{h}=\ddot\gamma(t)\end{aligned}$

            > $\Longrightarrow$ &nbsp; we can define evolution equations for $\gamma(t)$

            > > $$
            > > \ddot\gamma(t)=F(\gamma(t),\dot\gamma(t))
            > > $$
            """,
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: manifolds
    # motivation: no congruence on manifolds
    lk.prose(
        r"""
        On manifolds, no congruence …

        > $\Longrightarrow$ &nbsp; something goes wrong!

        Let $X\in\Gamma(TM)$ be a vector field on $M$ and $\gamma:\mathbb R\to M$ be a path on $M$

        > Consider $X(t)=X(\gamma(t))\overset{\varphi}{=}X^i(t)\,\partial_i|_{\gamma(t)}$

        > > $\Longrightarrow$ &nbsp; $X^i:\mathbb R\to\mathbb R$ are smooth

        > > $\Longrightarrow$ &nbsp; $\dot X^i(t)={\large\tfrac{d}{dt}}X^i(t)$ are well-defined! &nbsp; ($\forall\,t$ such that $\gamma(t)\in U$)

        Why not define &nbsp; ${\large\tfrac{d}{dt}}X(t)\overset{\varphi}{=}\dot X^i(t)\,\partial_i|_{\gamma(t)}$ ?

        > Consider $X(t)\overset{\varphi}{=}X^i(t)\,\partial_i|_{\gamma(t)}\overset{\tilde\varphi}{=}\tilde X^i(t)\,\tilde\partial_i|_{\gamma(t)}$

        > > $\displaystyle\begin{alignedat}{2}\Longrightarrow\quad&\tilde X^j(t)=\frac{\partial\tilde x^j}{\partial x^i}(\gamma(t))\,X^i(t)\\\Longrightarrow\quad&\dot{\tilde X}{}^j(t)=\frac{\partial\tilde x^j}{\partial x^i}(\gamma(t))\,\dot X^i(t)+\frac{\partial^2\tilde x^j}{\partial x^k\partial x^i}(\gamma(t))\,\dot x^k(t)\,X^i(t)\end{alignedat}$

        > > > where $\gamma(t)\overset{\varphi}{=}\varphi^{-1}(x^k(t)\,e_k)$ and $\dot x^k(t)={\large\tfrac{d}{dt}}x^k(t)$

        > > $\Longrightarrow$ &nbsp; $\dot X^i(t)\,\partial_i|_{\gamma(t)}\neq\dot{\tilde X}{}^i(t)\,\tilde\partial_i|_{\gamma(t)}$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: covariant derivatives
    # definition: covariant derivative
    lk.definition(
        r"""
        A **covariant derivative** on $M$ is, for each path $\gamma(t)$, an assignment

        $$
        \begin{aligned}
        \frac{D}{dt}:\left\{\begin{matrix}\text{vector fields}\\\text{along }\gamma(t)\end{matrix}\right\}&\longrightarrow\left\{\begin{matrix}\text{vector fields}\\\text{along }\gamma(t)\end{matrix}\right\}\\[0.4em]
        X(t)&\longmapsto\frac{D}{dt}X(t)
        \end{aligned}
        $$

        such that

        > • &nbsp; ${\large\tfrac{D}{dt}}\big(aX(t)+bY(t)\big)=a\,{\large\tfrac{D}{dt}}X(t)+b\,{\large\tfrac{D}{dt}}Y(t)$, &nbsp; $\forall\,a,b\in\mathbb R$

        > • &nbsp; ${\large\tfrac{D}{dt}}\big(\lambda(t)X(t)\big)={\large\tfrac{d}{dt}}\lambda(t)\,X(t)+\lambda(t)\,{\large\tfrac{D}{dt}}X(t)$, &nbsp; $\forall\,\lambda:\mathbb R\to\mathbb R$

        > • &nbsp; in each chart $\varphi:U\subseteq M\to\mathbb R^m$

        > > $$
        > > \begin{aligned}
        > > \frac{D}{dt}X(t)&\overset{\varphi}{=}\frac{D}{dt}\big(X^i(t)\,\partial_i|_{\gamma(t)}\big)\\
        > > &=\frac{d}{dt}X^i(t)\,\partial_i|_{\gamma(t)}+X^i(t)\,\frac{D}{dt}\partial_i|_{\gamma(t)}\\
        > > &=\dot X^i(t)\,\partial_i|_{\gamma(t)}+X^i(t)\,\underbrace{\dot x^j(t)\,\Gamma^k_{ij}(\gamma(t))\,\partial_k|_{\gamma(t)}}_{\footnotesize\begin{array}{c}\frac{D}{dt}\partial_i|_{\gamma(t)}\text{ depends linearly}\\\text{on the velocity }\dot\gamma(t)\end{array}}\rule[-2.6em]{0pt}{0pt}
        > > \end{aligned}
        > > $$

        > > > $\Longrightarrow$ &nbsp; $\displaystyle\frac{D}{dt}X(t)\overset{\varphi}{=}\big(\dot X^k(t)+X^i(t)\,\dot x^j(t)\,\Gamma^k_{ij}(\gamma(t))\big)\,\partial_k|_{\gamma(t)}$

        $\Gamma^k_{ij}(\gamma(t))$ are the **Christoffel symbols** of the covariant derivative with respect to $\varphi$ along $\gamma(t)$
        """,
        label="def-covariant-derivative",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: covariant derivatives
    # lead-in: existence
    lk.prose(r"Do covariant derivatives exist?")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: covariant derivatives
    # theorem: change of charts
    lk.theorem(
        r"""
        Assuming existence, given $\varphi,\tilde\varphi$ charts on $M$

        > $\displaystyle \frac{D}{dt}X\overset{\varphi}{=}\big(\dot X^k+X^i\dot x^j\,\Gamma^k_{ij}\big)\,\partial_k\overset{\tilde\varphi}{=}\big(\dot{\tilde X}{}^l+\tilde X^m\dot{\tilde x}{}^n\,\tilde\Gamma^l_{mn}\big)\,\tilde\partial_l$

        > > $\Longleftrightarrow$ &nbsp; $\displaystyle \Gamma^k_{ij}=\underbrace{\frac{\partial x^k}{\partial\tilde x^l}\,\tilde\Gamma^l_{mn}\,\frac{\partial\tilde x^m}{\partial x^i}\,\frac{\partial\tilde x^n}{\partial x^j}}_{\mathllap{\footnotesize\begin{array}{c}\text{transformation}\\\text{of }(1,2)\text{-tensor}\end{array}\kern-1.2em}}+\underbrace{\frac{\partial x^k}{\partial\tilde x^l}\,\frac{\partial^2\tilde x^l}{\partial x^i\partial x^j}}_{\mathrlap{\kern-1.2em\footnotesize\begin{array}{c}\text{non-tensorial}\\\text{transformation!}\end{array}}}$
        """,
        label="thm-christoffel-change",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: covariant derivatives
    # proof
    lk.proof(
        r"""
        $\tilde X^l={\large\tfrac{\partial\tilde x^l}{\partial x^k}}\,X^k$ &nbsp; $\Longrightarrow$ &nbsp; $\dot{\tilde X}{}^l={\large\tfrac{\partial\tilde x^l}{\partial x^k}}\,\dot X^k+\underbrace{{\large\tfrac{\partial^2\tilde x^l}{\partial x^i\partial x^j}}\,\dot x^iX^j}_{\footnotesize\text{non-tensorial}}$

        $\dot{\tilde x}{}^n={\large\tfrac{\partial\tilde x^n}{\partial x^j}}\,\dot x^j$ &nbsp; and &nbsp; $\partial_k={\large\tfrac{\partial\tilde x^l}{\partial x^k}}\,\tilde\partial_l$

        > $\leadsto$ &nbsp; just replace and compare
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: covariant derivatives
    # theorem: Christoffel symbols of a metric
    lk.theorem(
        [
            r"Given a metric $g\in\Gamma(TM^0_2)$, we can define in each chart $\varphi$ a collection $\Gamma^k_{ij}$ of Christoffel symbols via",
            lk.aside(
                r"$$\mk{\Gamma^k_{ij}}=\frac12\,g^{kl}\,(\partial_ig_{lj}+\partial_jg_{il}-\partial_lg_{ij})$$",
                r"Christoffel symbols of<br>the Levi-Civita connection",
            ),
        ],
        label="thm-christoffel-metric",
    )
    return


if __name__ == "__main__":
    app.run()
