import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 16 · Covectors and tensors", css_file="lecturekit/style.css")


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
    return lk, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(16, "Covectors and tensors")
    return


@app.cell(hide_code=True)
def _(lk, np):
    # Helpers of this lecture: the two 3D scenes

    def static_particle_scene():
        # the cylinder r = r_0, inside it the cylinder r = 2M (its two side lines cut into short pieces, which makes them
        # dashed), and outside it the static particle, with the proper time from gamma(a) to gamma(b) beside the middle of
        # that piece of its line. r_0 = 1.: the box is moved along r, so that the drawing sits left in its frame and the
        # label fits beside it
        s, a = np.meshgrid(np.linspace(-1.0, 1.6, 14), np.linspace(0, 2 * np.pi, 49), indexing="ij")
        ang = np.linspace(0, 2 * np.pi, 121)
        k = np.array([-1.0, 0.0])
        h, rs, ta, tb = 0.57, 1.71, 0.57, 1.14
        dash = [("cylinder", (0, 0), h, (t, min(t + 0.07, 1.6)), lk.ORANGE, 1.3) for t in np.arange(-1.0, 1.6, 0.12)]
        L = np.array([-1.0, 1.6])
        g = np.linspace(0, rs, 30)
        guides = [(0 * g, g, y + 0 * g, lk.GREY, 0.8, [1.5, 3]) for y in (ta, tb)]
        guides += [(np.zeros(2), np.array([-0.04, 0.04]), y + np.zeros(2), lk.GREY, 1.1) for y in (ta, tb)]
        return lk.turntable(
            25,
            14,
            "the spacetime outside a star: the cylinder r = r0, the cylinder r = 2M inside it, the circle S^2, and a static particle at a fixed r outside the cylinder, with the points gamma(a) and gamma(b), and beside the piece of its line from gamma(a) to gamma(b) the label time_g(gamma restricted to [a, b]) = (b - a) sqrt(1 - 2M/r)",
            [
                lk.panel(
                    1.0,
                    surfaces=[lk.sheet(h * np.cos(a), h * np.sin(a), s, alpha=0.25, tone=lk.ORANGE), lk.sheet(np.cos(a), np.sin(a), s, alpha=0.3, tone=lk.RED)],
                    outlines=[("cylinder", (0, 0), 1.0, (-1.0, 1.6), lk.RED, 1.2)] + dash,
                    lines=guides + [(np.cos(ang), np.sin(ang), 0 * ang, lk.GREEN, 2.2), (0 * k, 0 * k, k, lk.GREY, 1.1), (0 * L, rs + 0 * L, L, lk.GREEN, 1.6)],
                    points=[((0, 1, 0), lk.GREEN, 4.0), ((0, h, 0), lk.ORANGE, 3.2), ((0, rs, ta), "#000000", 3.4), ((0, rs, tb), "#000000", 3.4)],
                    arrows=[((0, 0, 0), (0, 0, 1.9), lk.GREY, 1.1), ((0, 0, 0), (0, 2.35, 0), lk.GREY, 1.1), ((0, rs, 0.8), (0, rs, 0.92), lk.GREEN, 1.6)],
                    texts=[
                        ((0, 0, ta), "a", "#000000", 180, 7),
                        ((0, 0, tb), "b", "#000000", 180, 7),
                        ((0, 0, 1.9), "t", lk.GREY, 90),
                        ((0, 2.5, 0), "r", lk.GREY, 0, 0),
                        ((0, 0, 1.5), "M", lk.BLUE, 0, 190),
                        ((0, 1, 0), "r_0", lk.GREEN, 35, 20),
                        ((0, 0, -0.25), r"\mathbb{S}^2", lk.GREEN, 180, 106),
                        ((0, h, 0), "2M", lk.ORANGE, -115, 30),
                        ((0, rs, 0), "r", lk.GREEN, -45, 10),
                        ((0, rs, ta), r"\gamma(a)", "#000000", 0, 7),
                        ((0, rs, tb), r"\gamma(b)", "#000000", 0, 7),
                        ((0, rs, (ta + tb) / 2), r"\begin{array}{l} \mathrm{time}_g\big(\gamma|_{[a,b]}\big) \\ \quad = (b - a)\sqrt{1 - \frac{2M}{r}} \end{array}", "#000000", 0, 60),
                    ],
                    box=((-1.75, 1.75), (-0.45, 3.05), (-1, 1.9)),
                )
            ],
            height=340,
            width=600,
            zoom=1.3,
        )

    def height_fields_scene():
        # X = d_theta and Y = -sin(phi) d_phi, at a quarter of their length, on the circles z = constant. X is tangent to
        # these circles, where the height does not change; Y climbs them and vanishes at the poles
        a, b = np.meshgrid(np.linspace(0, np.pi, 37), np.linspace(0, 2 * np.pi, 73), indexing="ij")
        t = np.linspace(0, 2 * np.pi, 121)
        lines, arrows = [], []
        for z in (-0.75, -0.4, 0.0, 0.4, 0.75):
            rr = np.sqrt(1 - z**2)
            lines.append((rr * np.cos(t), rr * np.sin(t), z + 0 * t, lk.GREY, 1.0))
            for c in np.linspace(0, 2 * np.pi, 8, endpoint=False):
                p = np.array([rr * np.cos(c), rr * np.sin(c), z])
                x, y = np.array([-p[1], p[0], 0.0]), np.array([-p[0] * z, -p[1] * z, 1 - z**2])
                arrows += [(tuple(p), tuple(p + 0.25 * x), lk.GREEN, 1.3), (tuple(p), tuple(p + 0.25 * y), lk.RED, 1.3)]
        front = (np.cos(np.radians(-30)), np.sin(np.radians(-30)), 0.0)  # the point of the equator facing the viewer
        return lk.turntable(
            -30,
            20,
            "the unit sphere with the circles z = constant, the vector field X along these circles and the vector field Y across them, towards the north pole",
            [
                lk.panel(
                    1.0,
                    surfaces=[lk.sheet(np.sin(a) * np.cos(b), np.sin(a) * np.sin(b), np.cos(a))],  # opaque: the far side stays hidden
                    outlines=[("sphere", (0, 0, 0), 1.0, lk.BLUE, 1.2)],
                    lines=lines,
                    arrows=arrows + [((0, 0, 1.0), (0, 0, 1.4), lk.GREY, 1.1)],
                    texts=[(front, "X", lk.GREEN, -45, 28), (front, "Y", lk.RED, 110, 32), ((0, 0, 1.4), "z", lk.GREY, 90)],
                )
            ],
            height=360,
            width=400,
        )

    return height_fields_scene, static_particle_scene


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # recap
    lk.recap(
        r"""
        $$
        \begin{aligned}
        g:\Gamma(TM)\times\Gamma(TM)&\longrightarrow C^\infty(M,\mathbb R)\qquad\text{metric field}\\
        (X,Y)&\longmapsto g(X,Y)
        \end{aligned}
        $$

        > $$
        > \left.\begin{array}{l}\bullet\ \ \text{symmetric}\\\bullet\ \ \text{bilinear}\\\bullet\ \ \text{signature }(m-1,1)\end{array}\right\rbrace\ \text{at each }p\in M
        > $$
        """,
        lk.aside(
            r"particle $=\gamma:\mathbb R\to M$ &nbsp; timelike <span class='lk-mark'>future oriented</span>",
            r"assume existence of nowhere<br>vanishing timelike vector field",
        ),
        lk.aside(
            r"> $\leadsto$ &nbsp; $\mk{\mathrm{time}_g(\gamma|_{[a,b]})}=\displaystyle\int_a^b\sqrt{-g(\gamma'(t),\gamma'(t))}\,dt$",
            r"proper time of $\gamma$<br>from $\gamma(a)$ to $\gamma(b)$",
        ),
        lk.gap(),
        r"""
        Example: &nbsp; $M=\mathbb R\times(r_0,+\infty)\times\mathbb S^2\ni(t,r,p)$

        > $\leadsto$ &nbsp; spacetime outside a static spherical star of radius $r_0$ and mass $M$

        > $$
        > g\overset{\Psi}{=}\begin{bmatrix}-\big(1-{\large\tfrac{2M}{r}}\big)&0&0&0\\0&\big(1-{\large\tfrac{2M}{r}}\big)^{-1}&0&0\\0&0&r^2&0\\0&0&0&r^2(\sin\phi)^2\end{bmatrix}\overset{\Phi_n}{=}\cdots
        > $$
        """,
        topic=r"Lorentzian manifolds $(M,g)$",
    )
    return


@app.cell(hide_code=True)
def _(lk, static_particle_scene):
    # module: static particles
    # remark: coordinate t is not physical time
    lk.remark(
        [
            r"""
            Coordinate $t$ is not “physical time”

            > Fix $(r,p)\in(r_0,+\infty)\times\mathbb S^2$ and take $\gamma(t)=(t,r,p)$ &nbsp; “static” particle

            > > $\gamma(t)\overset{\Psi}{=}(t,\underbrace{r,\phi,\theta}_{\footnotesize\text{fixed}})$ &nbsp; $\Longrightarrow$ &nbsp; $\gamma'(t)\overset{\Psi}{=}\begin{bmatrix}1\\0\\0\\0\end{bmatrix}$
            """,
            lk.aside(
                r"> > > $\Longrightarrow$ &nbsp; $g(\gamma'(t),\gamma'(t))=-\Big(1-\dfrac{2M}{r}\Big)$",
                r"$\gamma$ timelike if $r>2M$",
            ),
            r"> > > $\Longrightarrow$ &nbsp; $\mathrm{time}_g(\gamma|_{[a,b]})=\displaystyle\int_a^b\sqrt{1-\frac{2M}{r}}\,dt=(b-a)\sqrt{1-\frac{2M}{r}}$",
            lk.figure(static_particle_scene()),
            r"""
            • &nbsp; $\mathrm{time}_g(\gamma|_{[a,b]})\longrightarrow b-a$ &nbsp; as &nbsp; $r\to+\infty$

            > $\leadsto$ &nbsp; $t$ is the proper time of static particles “at infinity”

            Usually $2M\ll r_0$!

            > $$
            > \begin{aligned}
            > \text{Sun:}\quad&r_0=7\times10^5\text{ km}&\qquad2M&=3\text{ km}\\
            > \text{Earth:}\quad&r_0=6\times10^3\text{ km}&\qquad2M&=9\times10^{-6}\text{ km}=9\text{ mm}
            > \end{aligned}
            > $$

            $\leadsto$ &nbsp; if $2M>r_0$ strange things happen for $r_0<r\leq2M$

            > • &nbsp; $\gamma(t)$ is spacelike for $r<2M$
            """,
            lk.aside(
                r"> <span class='lk-ghost'>• &nbsp; $\gamma(t)$</span> is lightlike for $\mk{r=2M}$",
                r"also $g_{rr}=+\infty$",
            ),
            r"> > $\leadsto$ &nbsp; in this situation we have a black hole",
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(r"Covectors and tensors &nbsp; $\leadsto$ &nbsp; more general fields on manifolds!", title="In this lecture")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("Schutz 3.3–3.6; Carroll 2.4; Sasane 2.6, 3.5–3.6, 4.1–4.3")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: covectors
    # definition: covector field
    lk.definition(
        [
            r"A (smooth) **covector field** / **1-form field** on $M$ is an assignment",
            lk.aside(
                r"""$$
                \begin{aligned}
                &p\in M\longmapsto\alpha_p:T_pM\to\mathbb R\\
                \leftrightsquigarrow\quad&p\in M\longmapsto\alpha_p\in T^*_pM=\mk{(T_pM)^*}
                \end{aligned}
                $$""",
                [(2, r"dual space to $T_pM$")],
                rows=2,
            ),
            r"of a linear function on each tangent space of $M$.",
        ],
        label="def-covector-field",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: covectors
    # recall: absolute time
    lk.recall(
        r"""
        In $\mathbb G^4$ = Galilean spacetime, absolute time $\tau:\mathbb V\to\mathbb R$ was a linear function on $\mathbb V$.

        Covectors / 1-forms are similar types of objects on $T_pM$ at each $p\in M$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: covectors
    # covector fields as functionals of vector fields
    lk.prose(
        r"""
        We can also think of a smooth covector field as

        $$
        \begin{aligned}
        \alpha:\Gamma(TM)&\longrightarrow C^\infty(M,\mathbb R)\\
        X&\longmapsto\alpha(X):p\longmapsto\alpha_p(X_p)
        \end{aligned}
        $$
        """,
        lk.aside(
            r"as a <span class='lk-mark'>$C^\infty(M,\mathbb R)$-linear functional</span> of vector fields",
            r"$\alpha(fX+hY)=f\,\alpha(X)+h\,\alpha(Y)$<br>$\forall\,X,Y\in\Gamma(TM)$, $\forall\,f,h\in C^\infty(M,\mathbb R)$",
        ),
        r"""
        $\Gamma(T^*M)$ = space of all smooth covector fields
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: covectors
    # covector fields in charts
    lk.prose(
        r"In charts &nbsp; $\varphi:U\subseteq M\to\mathbb R^m$",
        lk.aside(
            r"> $X\overset{\varphi}{=}\mk{X^i}\,\mk{\partial_i}$",
            r"$X^i=X(x^i)$ = components of $X$ with respect to $\varphi$<br>$\partial_i$ = local basis of coordinate vector fields",
        ),
        lk.aside(
            r"> > $\Longrightarrow$ &nbsp; $\alpha(X)\overset{\varphi}{=}X^i\,\mk{\alpha(\partial_i)}=X^i\alpha_i$",
            r"$\alpha(\partial_i)=\alpha_i$ = components of $\alpha$ with respect to $\varphi$",
        ),
        lk.aside(
            r"> > $\Longrightarrow$ &nbsp; $\alpha\overset{\varphi}{=}\alpha_i\,\mk{dx^i}$",
            r"$dx^i$ = dual local basis of coordinate 1-forms<br>$dx^i(\partial_j)=\delta^i{}_j$",
        ),
        r"""
        > > $\leadsto$ &nbsp; $X\overset{\varphi}{=}\begin{bmatrix}X^1\\\vdots\\X^m\end{bmatrix}$, &nbsp; $\alpha\overset{\varphi}{=}\begin{bmatrix}\alpha_1&\cdots&\alpha_m\end{bmatrix}$

        > > <span class="lk-ghost">$\leadsto$ &nbsp; </span>$\alpha(X)\overset{\varphi}{=}\begin{bmatrix}\alpha_1&\cdots&\alpha_m\end{bmatrix}\cdot\begin{bmatrix}X^1\\\vdots\\X^m\end{bmatrix}=\alpha_iX^i$
        """,
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: covectors
    # change of charts
    lk.prose(
        r"Change of charts",
        lk.aside(
            r"> $X\overset{\varphi}{=}X^i\,\partial_i\overset{\tilde\varphi}{=}\tilde X^j\,\tilde\partial_j$ &nbsp; $\Longleftrightarrow$ &nbsp; $\mk{\tilde X^j={\large\tfrac{\partial\tilde x^j}{\partial x^i}}\,X^i}$",
            "contravariant transformation",
        ),
        r"> > from chain rule: &nbsp; ${\large\tfrac{\partial}{\partial x^i}}={\large\tfrac{\partial\tilde x^j}{\partial x^i}}\,{\large\tfrac{\partial}{\partial\tilde x^j}}$",
        lk.aside(
            r"> $\alpha\overset{\varphi}{=}\alpha_i\,dx^i\overset{\tilde\varphi}{=}\tilde\alpha_j\,d\tilde x^j$ &nbsp; $\Longleftrightarrow$ &nbsp; $\mk{\alpha_i={\large\tfrac{\partial\tilde x^j}{\partial x^i}}\,\tilde\alpha_j}$",
            "covariant transformation",
        ),
        r"> > from chain rule: &nbsp; $d\tilde x^j={\large\tfrac{\partial\tilde x^j}{\partial x^i}}\,dx^i$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: differentials
    # example: differentials of scalar functions
    lk.example(
        [
            r"""
            Given $f\in C^\infty(M,\mathbb R)$ smooth scalar function, its differential at $p\in M$ is the covector

            $$
            \begin{aligned}
            df_p:T_pM&\longrightarrow T_{f(p)}\mathbb R=\mathbb R\\
            X_p&\longmapsto df_p(X_p)=X_p(f)
            \end{aligned}
            $$

            > $\leadsto$ &nbsp; $df\in\Gamma(T^*M)$ is the covector field such that $df(X)=X(f)$
            """,
            lk.aside(
                r"> > $\Longrightarrow$ &nbsp; $\mk{df\overset{\varphi}{=}\partial_if\,dx^i}$",
                r"$df(X)=X(f)=X^i\,\partial_if$<br>$=\partial_if\,X(x^i)=\partial_if\,dx^i(X)$",
            ),
            r"$\leadsto$ &nbsp; the local basis of covectors $dx^i$ are the differentials of the coordinate functions!",
        ],
        title="differentials of scalar functions",
        label="ex-differentials",
    )
    return


@app.cell(hide_code=True)
def _(height_fields_scene, lk):
    # module: differentials
    # example: the height function on the sphere
    lk.example(
        [
            r"""
            $f:\mathbb S^2\to\mathbb R$ &nbsp; height function

            $$
            f(x,y,z)=z\overset{\varphi_n}{=}\frac{-1+u^2+v^2}{1+u^2+v^2}\overset{\psi}{=}\cos\phi
            $$

            $$
            \begin{aligned}
            df=dz&\overset{\varphi_n}{=}\partial_uz\,du+\partial_vz\,dv\\
            &=\frac{4u}{(1+u^2+v^2)^2}\,du+\frac{4v}{(1+u^2+v^2)^2}\,dv\\
            &\overset{\psi}{=}\partial_\phi z\,d\phi+\partial_\theta z\,d\theta\\
            &=-\sin\phi\,d\phi
            \end{aligned}
            $$

            $$
            \begin{aligned}
            X&\overset{\varphi_n}{=}-v\,\partial_u+u\,\partial_v&&\overset{\psi}{=}\partial_\theta\\
            Y&\overset{\varphi_n}{=}u\,\partial_u+v\,\partial_v&&\overset{\psi}{=}-\sin\phi\,\partial_\phi
            \end{aligned}
            $$
            """,
            lk.aside(
                r"""$$
                \begin{aligned}
                dz(X)&\overset{\varphi_n}{=}\frac{4}{(1+u^2+v^2)^2}\big(u\,du(-v\,\partial_u+u\,\cancel{\partial_v})+v\,dv(-v\,\cancel{\partial_u}+u\,\partial_v)\big)\\
                &=\frac{4}{(1+u^2+v^2)^2}\,(-uv+uv)=0\\
                &\overset{\psi}{=}-\sin\phi\,d\phi(\partial_\theta)=0
                \end{aligned}
                $$""",
                [(1, r"$du(\partial_u)=dv(\partial_v)=1$<br>$du(\partial_v)=dv(\partial_u)=0$")],
                rows=3,
            ),
            r"""
            $$
            \begin{aligned}
            dz(Y)&\overset{\varphi_n}{=}\frac{4}{(1+u^2+v^2)^2}\,(u^2+v^2)\overset{\psi}{=}(\sin\phi)^2\\
            &=x^2+y^2=1-z^2\qquad(\text{on }x^2+y^2+z^2=1)
            \end{aligned}
            $$
            """,
            lk.figure(height_fields_scene()),
        ],
        label="ex-height",
    )
    return


if __name__ == "__main__":
    app.run()
