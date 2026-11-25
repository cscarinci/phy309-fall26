import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="PHY309 · Lecture 7 · Manifolds", css_file="lecturekit/style.css")


@app.cell(hide_code=True)
async def _():
    import math
    import sys

    import marimo as mo
    import numpy as np
    from matplotlib.figure import Figure

    import matplotlib  # noqa: F401  (named here so the browser fetches it while Python starts)

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(str(mo.notebook_location() / "public" / "lecturekit-0.1.0-py3-none-any.whl"), deps=False)
    import lecturekit as lk
    return Figure, lk, math, mo, np


@app.cell(hide_code=True)
def _(lk):
    lk.lecture(7, "Manifolds")
    return


@app.cell(hide_code=True)
def _(lk, math, np):
    # Helpers of this lecture: the six figures
    sk = lk.sk

    def _sphere(alpha=0.45):
        s_, t_ = np.meshgrid(np.linspace(0, np.pi, 37), np.linspace(0, 2 * np.pi, 73), indexing="ij")
        return lk.sheet(np.sin(s_) * np.cos(t_), np.sin(s_) * np.sin(t_), np.cos(s_), alpha=alpha)

    _EDGE = ("sphere", (0, 0, 0), 1.0, lk.GREY, 1.2)

    def affine_sketch():
        # in an affine space, the vector v at p is copied to q by congruence; the straight lines through them are parallel
        fig, ax = sk.sketch((-2.6, 2.9), (-0.9, 3.6))
        for x in (-1.0, 1.0):
            ax.plot([x, x], [0, 3.4], color=lk.BLUE, lw=sk.LW)
            sk.maps(ax, (x, 0), (x, 1.5), color=lk.GREEN, lw=1.8)
        sk.dot(ax, (-1.0, 0), "$p$", at=(0, -0.3))
        sk.dot(ax, (1.0, 0), "$q$", at=(0, -0.3))
        sk.label(ax, (-1.25, 0.9), "$v$", lk.GREEN, ha="right")
        sk.label(ax, (1.25, 0.9), "$v' = v$", lk.GREEN, ha="left")
        return fig

    def gravity_sketch():
        # free-falling particles from p and q, both starting with velocity v, bend towards the source of gravity
        fig, ax = sk.sketch((-2.6, 2.9), (-0.9, 3.6))
        ax.plot([0, 0], [-0.4, 3.4], color=sk.INK, lw=sk.LW)
        s = np.linspace(0, 3.0, 100)
        for sgn in (-1, 1):
            ax.plot(sgn * 1.0 * (1 - (s / 3.4) ** 2), s, color=lk.BLUE, lw=sk.LW)
            sk.maps(ax, (sgn * 1.0, 0), (sgn * 1.0, 1.5), color=lk.GREEN, lw=1.8)
            sk.dot(ax, (sgn * 1.0, 0), "$p$" if sgn < 0 else "$q$", at=(0, -0.3))
        sk.label(ax, (-1.25, 0.9), "$v$", lk.GREEN, ha="right")
        sk.label(ax, (1.25, 0.9), "$v'$", lk.GREEN, ha="left")
        sk.label(ax, (0.2, 3.35), "source of gravity", ha="left", size=13)
        return fig

    def surfaces_scene():
        # the sphere, the torus and the genus 2 surface
        t = np.linspace(0, 2 * np.pi, 241)
        u, w = np.meshgrid(np.linspace(0, 2 * np.pi, 61), np.linspace(0, 2 * np.pi, 31), indexing="ij")
        torus_xyz = ((1.0 + 0.42 * np.cos(w)) * np.cos(u), (1.0 + 0.42 * np.cos(w)) * np.sin(u), 0.42 * np.sin(w))
        torus = lk.sheet(*torus_xyz)
        # genus 2: two tori smoothly joined, as z^2 = -S(a, b); the grid points just outside S < 0 are moved onto its rim
        az = math.radians(-30)
        ea, eb = np.array([-math.sin(az), math.cos(az)]), np.array([math.cos(az), math.sin(az)])

        def S(a, b):
            s1 = (np.hypot(a + 0.95, b) - 0.62) ** 2 - 0.09
            s2 = (np.hypot(a - 0.95, b) - 0.62) ** 2 - 0.09
            return -0.18 * np.logaddexp(-s1 / 0.18, -s2 / 0.18)

        a, b = np.meshgrid(np.linspace(-2.0, 2.0, 101), np.linspace(-1.0, 1.0, 51), indexing="ij")
        inside = S(a, b) < 0
        hole = ~inside & (np.minimum(np.hypot(a + 0.95, b), np.hypot(a - 0.95, b)) < 0.62)  # grid points in a hole
        rim = ~inside  # every grid point outside is moved onto the rim S = 0 (no gaps in the surface data)
        ra, rb = a[rim], b[rim]
        for _ in range(40):  # Newton steps onto S = 0
            ga = (S(ra + 1e-5, rb) - S(ra - 1e-5, rb)) / 2e-5
            gb = (S(ra, rb + 1e-5) - S(ra, rb - 1e-5)) / 2e-5
            k = S(ra, rb) / (ga**2 + gb**2)
            ra, rb = ra - np.clip(k * ga, -0.2, 0.2), rb - np.clip(k * gb, -0.2, 0.2)
        a[rim], b[rim] = ra, rb
        z = np.where(inside, np.sqrt(np.maximum(-S(a, b), 0.0)), 0.0)
        x, y = a * ea[0] + b * eb[0], a * ea[1] + b * eb[1]
        # unit normals for the outlines: the torus from its angles, the genus 2 surface from the gradient of z^2 + S(a, b)
        tn = (np.cos(w) * np.cos(u), np.cos(w) * np.sin(u), np.sin(w))
        ga = (S(a + 1e-5, b) - S(a - 1e-5, b)) / 2e-5
        gb = (S(a, b + 1e-5) - S(a, b - 1e-5)) / 2e-5
        gx, gy, gz = ga * ea[0] + gb * eb[0], ga * ea[1] + gb * eb[1], 2 * z
        gl = np.sqrt(gx**2 + gy**2 + gz**2)
        gn = tuple(np.where(hole, np.nan, g / gl) for g in (gx, gy, gz))  # no outline across a hole
        top, bot = (x, y, z), (x[:, ::-1], y[:, ::-1], -z[:, ::-1])
        bn = (gn[0][:, ::-1], gn[1][:, ::-1], -gn[2][:, ::-1])
        return lk.turntable(
            -30,
            45,
            "the sphere, the torus and the genus 2 surface",
            [
                lk.panel(1.0, surfaces=[_sphere(1.0)], outlines=[_EDGE], lines=[(np.cos(t), np.sin(t), 0 * t, "#000000", 1.0)], caption=r"\mathbb{S}^2"),
                lk.panel(1.0, surfaces=[torus], outlines=[("surface", torus_xyz, tn, lk.GREY, 1.2)], caption=r"\mathbb{T}^2"),
                lk.panel(1.0, surfaces=[lk.sheet(*top), lk.sheet(*bot)], outlines=[("surface", top, gn, lk.GREY, 1.2), ("surface", bot, bn, lk.GREY, 1.2)], caption=r"\Sigma_2"),
            ],
            height=240,
            cols=3,
            shared=False,
            bias=0.12,
        )

    def congruence_scene():
        # vectors v copied along the equator from p to q, then carried up the meridians of p and q to the pole r
        t = np.linspace(0, 2 * np.pi, 241)
        al = math.asin(0.6)  # longitudes of p and q
        la = np.linspace(0, np.pi / 2, 61)

        def meridian(lon):
            return np.cos(la) * math.cos(lon), np.cos(la) * math.sin(lon), np.sin(la)

        def m(lon, lt):
            return np.array((math.cos(lt) * math.cos(lon), math.cos(lt) * math.sin(lon), math.sin(lt)))

        def north(lon, lt):  # the northward unit tangent of the meridian
            return np.array((-math.sin(lt) * math.cos(lon), -math.sin(lt) * math.sin(lon), math.cos(lt)))

        p, q, r = (math.cos(al), -math.sin(al), 0.0), (math.cos(al), math.sin(al), 0.0), np.array((0.0, 0.0, 1.0))
        v, vq = np.array((-math.cos(al), math.sin(al), 0.0)), np.array((-math.cos(al), -math.sin(al), 0.0))
        return lk.turntable(
            0,
            24,
            "the sphere with vectors v copied along the equator from p to q, and the vectors v and v' carried up the meridians of p and q to the pole r",
            [
                lk.panel(
                    1.0,
                    surfaces=[_sphere(1.0)],
                    outlines=[_EDGE],
                    lines=[(np.cos(t), np.sin(t), 0 * t, "#000000", 1.0), (*meridian(-al), lk.BLUE, 1.6), (*meridian(al), lk.RED, 1.6)],
                    arrows=[((math.cos(lo), math.sin(lo), 0.0), (math.cos(lo), math.sin(lo), 0.4), lk.GREEN) for lo in np.linspace(-al, al, 6)]
                    + [(tuple(r), tuple(0.55 * v + r), lk.GREEN), (tuple(r), tuple(0.55 * vq + r), lk.ORANGE)]
                    + [(tuple(m(lo, 0.85)), tuple(m(lo, 0.85) + 0.4 * north(lo, 0.85)), c) for lo, c in ((-al, lk.GREEN), (al, lk.ORANGE))],
                    points=[(p, "#000000", 3.4), (q, "#000000", 3.4), (tuple(r), "#000000", 3.4)],
                    texts=[
                        (p, "p", "#000000", -100),
                        (q, "q", "#000000", -80),
                        (tuple(r), "r", "#000000", -90, 8),
                        ((p[0], p[1], 0.2), "v", lk.GREEN, 180, 8),
                        ((q[0], q[1], 0.2), "v", lk.GREEN, 0, 8),
                        (tuple(0.55 * v + r), "v", lk.GREEN, 0, 8),
                        (tuple(0.55 * vq + r), "v'", lk.ORANGE, 180, 8),
                    ],
                )
            ],
            height=lk.H3D,
            width=lk.H3D,
            bias=0.12,
        )

    def atlas_figure():
        # two charts on the Earth, the pages V_alpha and V_beta of an atlas, and the change of charts
        sk = lk.sk
        fig, ax = sk.sketch((-0.5, 14.2), (-1.9, 9.4))
        # the Earth: a disc, with a short arc beside its rim to show it is a sphere
        t = np.linspace(0, 2 * np.pi, 200)
        E = np.c_[7.0 + 2.8 * np.cos(t), 6.2 + 2.8 * np.sin(t)]
        sk.outline(ax, E, name="Earth", at=sk.rim(E, 165, 0.45), size=13, ha="right")
        ta = np.radians(np.linspace(112, 152, 40))
        ax.plot(7.0 + 3.05 * np.cos(ta), 6.2 + 3.05 * np.sin(ta), color=sk.INK, lw=1.0, zorder=2)
        U = sk.shape(6.35, 6.0, 1.3, 1.0, waves=((2, 0.06, 1.0), (3, 0.03, 0.3)), tilt=8)
        V = sk.shape(7.75, 6.1, 1.3, 1.0, waves=((2, 0.06, -0.6), (3, 0.03, 1.9)), tilt=-10)
        sk.overlap(ax, U, V)
        sk.outline(ax, U, lk.RED, r"$U_\alpha$", sk.rim(U, 130, 0.25), va="bottom")
        sk.outline(ax, V, lk.BLUE, r"$U_\beta$", sk.rim(V, 50, 0.25), va="bottom")
        Y = 2.0
        L = sk.shape(2.3, 1.7, 1.75, 1.35, waves=((2, 0.06, 0.4), (3, 0.03, 1.3)))
        R = sk.shape(11.5, 1.7, 1.75, 1.35, waves=((2, 0.06, 2.4), (3, 0.03, 0.2)))
        Lo = sk.shape(3.55, 1.7, 1.75, 1.9, waves=((2, 0.05, 1.1),))
        Ro = sk.shape(10.25, 1.7, 1.75, 1.9, waves=((2, 0.05, -0.8),))
        for img, other, col, cut, name, ang, x0, page in ((L, Lo, lk.RED, lk.BLUE, r"$V_\alpha$", 128, 0.0, r"page $\alpha$ of a geographical atlas"),
                                                         (R, Ro, lk.BLUE, lk.RED, r"$V_\beta$", 52, 9.4, r"page $\beta$")):
            sk.axes(ax, x0, -0.55, 4.0, 3.9, r"$\mathbb{R}^2$")
            sk.overlap(ax, other, img)
            sk.outline(ax, img, col, name, sk.rim(img, ang, 0.4))
            sk.cut(ax, other, img, cut)
            sk.label(ax, (x0 + 2.0, -1.0), page, col, va="top", size=12)
        sk.maps(ax, (sk.rim(L, 0, 0.35)[0], Y), (9.05, Y), r"$\varphi_\beta \circ \varphi_\alpha^{-1}$", side=1, gap=0.35)
        sk.maps(ax, sk.rim(E, 215, 0.3), sk.rim(L, 75, 0.35), r"chart $\varphi_\alpha$", lk.RED, bend=-0.2, side=-1, size=13, gap=0.75)
        sk.maps(ax, sk.rim(E, -35, 0.3), sk.rim(R, 105, 0.35), r"$\varphi_\beta$", lk.BLUE, bend=0.2, side=1)
        return fig

    def stereo_scene():
        # the line through n and p meets the plane z = 0 at (u, v, 0); the line through s and p at (u~, v~, 0)
        ph, th = math.radians(60), math.radians(30)
        P = np.array([math.sin(ph) * math.cos(th), math.sin(ph) * math.sin(th), math.cos(ph)])
        n, s, o = np.array([0.0, 0.0, 1.0]), np.array([0.0, 0.0, -1.0]), np.zeros(3)
        F = np.array([P[0], P[1], 0.0])
        Un = np.array([P[0] / (1 - P[2]), P[1] / (1 - P[2]), 0.0])
        Us = np.array([P[0] / (1 + P[2]), P[1] / (1 + P[2]), 0.0])
        plane = [(-1.25, -1.25, 0), (1.75, -1.25, 0), (1.75, 1.25, 0), (-1.25, 1.25, 0)]
        edge = np.array(plane + plane[:1])
        k = np.linspace(0, 1, 40)[:, None]
        c = np.linspace(0, 2 * np.pi, 121)

        def seg(a, b):
            return tuple((a + k * (b - a)).T)

        return lk.turntable(
            -30,
            18,
            "the unit sphere and the plane z = 0, with the line through n and p meeting the plane at (u, v, 0) and the line through s and p meeting it at (u~, v~, 0)",
            [
                lk.panel(
                    1.0,
                    surfaces=[_sphere(), lk.patch(plane, "#e8e8e8", 0.6, n=16)],
                    outlines=[_EDGE],
                    lines=[
                        (*edge.T, lk.GREY, 1.2),
                        (np.cos(c), np.sin(c), 0 * c, "#000000", 1.0),
                        (*seg(n, o), "#000000", 1.0, [2, 3]),
                        (*seg(P, F), "#000000", 1.0, [2, 3]),
                        (*seg(o, Un), lk.GREY, 1.0, [4, 3]),
                        (*seg(n, Un), lk.BLUE, 1.8),
                        (*seg(s, P), lk.RED, 1.8),
                    ],
                    points=[(tuple(n), "#000000", 3.4), (tuple(s), "#000000", 3.4), (tuple(o), "#000000", 2.6), (tuple(P), "#000000", 3.4), (tuple(F), "#000000", 2.6), (tuple(Un), lk.BLUE, 4.0), (tuple(Us), lk.RED, 4.0)],
                    texts=[
                        (tuple(n), "n = (0, 0, 1)", "#000000", 90),
                        (tuple(s), "s", "#000000", -90),
                        (tuple(o), "(0, 0, 0)", "#000000", 165, 10),
                        (tuple(P), "p = (x, y, z)", "#000000", 30, 12),
                        (tuple(F), "(x, y, 0)", "#000000", -90, 12),
                        (tuple(Un), "(u, v, 0)", "#000000", -60, 14),
                        (tuple(Us), r"(\tilde{u}, \tilde{v}, 0)", "#000000", -125, 26),
                    ],
                )
            ],
            height=lk.H3D,
            width=420,
            bias=0.12,
        )

    def section_figure(lat_deg):
        # the cross-section: the rays from n and from s through p, meeting the plane z = 0 at u and u~
        a = math.radians(lat_deg)
        x, z = math.cos(a), math.sin(a)
        u, ut = x / (1 - z), x / (1 + z)
        R = 2.8  # holds the projected points for every latitude of the slider (u <= 2.41 at 45 degrees)
        fig, ax = sk.sketch((-1.6, R + 0.4), (-1.5, 1.6), scale=0.75)
        th = np.linspace(0, 2 * np.pi, 200)
        ax.plot(np.cos(th), np.sin(th), color=lk.GREY, lw=sk.LW)
        ax.plot([-1.4, R + 0.2], [0, 0], color=sk.INK, lw=1.2)
        ax.plot([0, x, u], [1, z, 0], color=lk.BLUE, lw=sk.LW)  # the ray from n through p to phi_n(p)
        ax.plot([0, x, ut], [-1, z, 0], color=lk.RED, lw=sk.LW)  # the ray from s through p to phi_s(p)
        sk.dot(ax, (0, 1), "$n$", at=(-0.15, 0.05), ha="right")
        sk.dot(ax, (0, -1), "$s$", at=(-0.15, -0.05), ha="right")
        sk.dot(ax, (x, z), "$p$", at=(0.12, 0.08) if z >= 0 else (0.12, -0.08), ha="left")
        sk.dot(ax, (u, 0), "$u$", at=(0.05, 0.12), color=lk.BLUE, ha="left")
        sk.dot(ax, (ut, 0), r"$\tilde u$", at=(0.05, -0.12), color=lk.RED, ha="left")
        return fig

    return affine_sketch, atlas_figure, congruence_scene, gravity_sketch, section_figure, stereo_scene, surfaces_scene


@app.cell(hide_code=True)
def _(lk):
    # Controls of the interactive figure (latitude of p, in degrees)
    s_lat = lk.slider(-45, 45, step=1, value=35, label=r"latitude of $p$", show_value=False)
    return (s_lat,)


@app.cell(hide_code=True)
def _(affine_sketch, gravity_sketch, lk):
    # module: recap
    # recap
    lk.recap(
        r"geometry $=\underbrace{\text{affine space}}_{\footnotesize\begin{matrix}\text{we don't need}\\\text{origins or frames}\end{matrix}}\ +$ additional structure",
        r"""
        > $\leadsto$ &nbsp; just congruence

        > > $\Longrightarrow$ &nbsp; straight lines

        > > $\Longrightarrow$ &nbsp; parallel lines
        """,
        lk.figure(affine_sketch()),
        r"""
        gravity &nbsp; $\leadsto$ &nbsp; defines free-falling particles

        > $\Longrightarrow$ &nbsp; a notion of “straight lines”

        > $\Longrightarrow$ &nbsp; incompatible with parallelism due to tidal effects!

        > $\Longrightarrow$ &nbsp; incompatible with congruence!
        """,
        lk.figure(gravity_sketch()),
        title="So far",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # goals
    lk.goals(
        lk.aside(
            r"Generalize geometry so that it does <span class='lk-mark'>not need congruence</span>!",
            "drop the affine structure!",
        ),
        title="In this lecture",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: recap
    # references
    lk.references("Schutz 6.1; Carroll 2.2; Sasane 1.1–1.3")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: manifolds
    # what replaces affine spaces
    lk.prose(
        lk.aside(
            r"differential geometry $=$ <span class='lk-mark'>manifolds</span> $+$ additional structure",
            r"manifolds = generalized spaces with points,<br>but no displacement vectors, which look like $\mathbb R^m$,<br>but only locally!",
        ),
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: manifolds
    # charts of affine spaces are global, charts of manifolds only local
    lk.prose(
        r"In $\mathbb R^m$ we have a preferred point &nbsp; $o=\begin{bmatrix}0\\0\\\vdots\\0\end{bmatrix}$",
        r"> and a preferred basis of vectors &nbsp; $e_i=\begin{bmatrix}0\\\vdots\\1\\\vdots\\0\end{bmatrix}$",
        r"In $\mathbb A^m$ each choice of $(o,e_i)\in\mathbb A^m\times\mathbb V^m$ defines",
        r"$$\varphi_{(o,e_i)}:\mathbb A^m\longrightarrow\mathbb R^m,\qquad p=\underbrace{o+x^ie_i}_{\text{using }-\,:\,\mathbb A\times\mathbb A\to\mathbb V}\longmapsto\begin{bmatrix}x^1\\x^2\\\vdots\\x^m\end{bmatrix}$$",
        r"""
        > $\leadsto$ &nbsp; importantly &nbsp; $\varphi_{(o,e_i)}:\mathbb A^m\longrightarrow\mathbb R^m$ &nbsp; is a global bijection!

        > $\leadsto$ &nbsp; for &nbsp; $\varphi_{(o,e_i)}$, &nbsp; $\varphi_{(\tilde o,\tilde e_i)}$ &nbsp; two such charts
        """,
        lk.aside(
            r"$$\begin{aligned}&\varphi_{(\tilde o,\tilde e_i)}\circ\varphi_{(o,e_i)}^{-1}:\mathbb R^m\xrightarrow{\ \sim\ }\mathbb R^m\\[0.3em]&\begin{bmatrix}x^1\\\vdots\\x^m\end{bmatrix}\longmapsto\begin{bmatrix}\tilde x^1\\\vdots\\\tilde x^m\end{bmatrix}=\begin{bmatrix}A^1{}_1&\cdots&A^1{}_m\\\vdots&&\vdots\\A^m{}_1&\cdots&A^m{}_m\end{bmatrix}\begin{bmatrix}x^1\\\vdots\\x^m\end{bmatrix}+\begin{bmatrix}b^1\\\vdots\\b^m\end{bmatrix}\end{aligned}$$",
            "change of coordinates<br>= linear transformation<br>&plus; constant translation",
            at="last",
        ),
        lk.gap(),
        r"In a manifold $M^m$ we will keep the ability of producing coordinate charts",
        r"$$\varphi_\alpha:U_\alpha\subseteq M^m\longrightarrow V_\alpha\subseteq\mathbb R^m$$",
        r"""
        > $\leadsto$ &nbsp; now only local bijections

        > $\leadsto$ &nbsp; for $\varphi_\alpha$ and $\varphi_\beta$
        """,
        lk.aside(
            r"$$\varphi_\beta\circ\varphi_\alpha^{-1}:V_\alpha\subseteq\mathbb R^m\ \mk{\xrightarrow{\ \sim\ }}\ V_\beta\subseteq\mathbb R^m$$",
            r"bijective at least in some subset of $V_\alpha$",
        ),
    )
    return


@app.cell(hide_code=True)
def _(congruence_scene, lk, surfaces_scene):
    # module: manifolds
    # example: surfaces, and congruence on the sphere
    lk.example(
        [
            r"2-sphere $\mathbb S^2$, &nbsp; 2-torus $\mathbb T^2$, &nbsp; genus 2 surface $\Sigma_2$",
            lk.figure(surfaces_scene()),
            r"What does congruence mean on the sphere?",
            lk.figure(congruence_scene()),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: manifolds
    # definition: m-manifold
    lk.definition(
        [
            r"An **$m$-dimensional manifold** ($m$-manifold) is a set of points $M^m\ni p$, with a collection of charts $\mathcal A\ni\varphi_\alpha$",
            r"$$\varphi_\alpha:U_\alpha\subseteq M\longrightarrow V_\alpha\subseteq\mathbb R^m$$",
            r"where",
            lk.aside(r"> • &nbsp; $U_\alpha$ <span class='lk-mark'>cover</span> $M$", r"$\textstyle\bigcup_\alpha U_\alpha=M$"),
            lk.aside(r"> • &nbsp; $V_\alpha$ are <span class='lk-mark'>open sets</span> of $\mathbb R^m$", r"given by union of open balls in $\mathbb R^m$"),
            lk.aside(r"> • &nbsp; $\varphi_\alpha:U_\alpha\xrightarrow{\ \sim\ }V_\alpha$ &nbsp; are <span class='lk-mark'>bijections</span>", r"each $U_\alpha$ “looks like” $V_\alpha=\varphi_\alpha(U_\alpha)$ via $\varphi_\alpha$"),
            r"> • &nbsp; $\varphi_\alpha(U_\alpha\cap U_\beta)\subseteq V_\alpha$, &nbsp; $\varphi_\beta(U_\alpha\cap U_\beta)\subseteq V_\beta$ &nbsp; are also open",
            lk.aside(
                r"> • &nbsp; $\varphi_\beta\circ\varphi_\alpha^{-1}:\underset{\begin{matrix}\cap\\\mathbb R^m\end{matrix}}{\varphi_\alpha(U_\alpha\cap U_\beta)}\xrightarrow{\ \sim\ }\underset{\begin{matrix}\cap\\\mathbb R^m\end{matrix}}{\varphi_\beta(U_\alpha\cap U_\beta)}$ &nbsp; are <span class='lk-mark'>diffeomorphisms</span>",
                "diffeomorphisms = smooth bijections<br>with smooth inverse",
            ),
        ],
        label="def-manifold",
    )
    return


@app.cell(hide_code=True)
def _(atlas_figure, lk):
    # module: manifolds
    # example: the Earth and its atlas
    lk.example(
        [
            r"$\mathbb S^2=\{(x^1,x^2,x^3)\in\mathbb R^3\mid(x^1)^2+(x^2)^2+(x^3)^2=1\}$",
            lk.figure(atlas_figure()),
        ]
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: manifolds
    # remark: calculus on each chart domain
    lk.remark(
        r"""
        $\varphi_\beta\circ\varphi_\alpha^{-1}$ &nbsp; diffeomorphism

        > $\Longrightarrow$ &nbsp; we can do calculus on each $U_\alpha\subseteq M$ using usual calculus on $V_\alpha\subseteq\mathbb R^m$ and every result agrees on $U_\alpha\cap U_\beta$
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: manifolds
    # remark: the topology of a manifold
    lk.remark(
        r"""
        Collection of all open sets defines a topology on $\mathbb R^m$

        > $\leadsto$ &nbsp; study properties of $\mathbb R^m$ invariant under continuous deformations

        $\varphi_\alpha:U_\alpha\longrightarrow V_\alpha$ &nbsp; bijection, &nbsp; $V_\alpha$ open, &nbsp; $\varphi_\alpha(U_\alpha\cap U_\beta)$ open

        > $\Longrightarrow$ &nbsp; defines a topology on $M$ with open sets

        > > $\varphi_\alpha^{-1}(V_\alpha\cap W)\subseteq M$, &nbsp; for $W\subseteq\mathbb R^m$ open, &nbsp; and their unions
        """
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: manifolds
    # remark: technical conditions
    lk.remark(
        lk.aside(
            r"This topology needs a few <span class='lk-mark'>technical conditions</span>, but they are not too important.",
            "Hausdorff + second countable",
        )
    )
    return


@app.cell(hide_code=True)
def _(lk):
    lk.section("Calculus of scalar functions")
    return


@app.cell(hide_code=True)
def _(lk):
    # module: calculus of scalar functions
    # definition: smooth function
    lk.definition(
        [
            r"Given an $m$-manifold &nbsp; $M$, &nbsp; $\mathcal A=\{\varphi_\alpha:U_\alpha\longrightarrow V_\alpha\subseteq\mathbb R^m\}$",
            r"a function $f:M\longrightarrow\mathbb R$ is called **smooth** if, for every chart $\varphi_\alpha\in\mathcal A$, the composition",
            lk.aside(
                r"$$\mk{f\circ\varphi_\alpha^{-1}}:\underset{\begin{matrix}\cap\\\mathbb R^m\end{matrix}}{V_\alpha}\longrightarrow\mathbb R$$",
                r"usual scalar function in $\mathbb R^m$",
            ),
            r"is smooth",
        ],
        label="def-smooth-function",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: calculus of scalar functions
    # derivatives in a chart
    lk.prose(
        r"$\Longrightarrow$ &nbsp; we know how to calculate derivatives with respect to coordinates in $V_\alpha$",
        r"Let's simplify notation a bit here: &nbsp; $\varphi_\alpha:U_\alpha\longrightarrow V_\alpha$ &nbsp; $\leadsto$ &nbsp; $\varphi:U\longrightarrow V\subseteq\mathbb R^m\ni x$",
        r"$$\frac{\partial}{\partial x^\mu}(f\circ\varphi^{-1})(x)=\lim_{h\to0}\frac{(f\circ\varphi^{-1})(x+he_\mu)-(f\circ\varphi^{-1})(x)}{h}$$",
        r"$$\begin{aligned}D_x(f\circ\varphi^{-1})(v)&=\lim_{h\to0}\frac{(f\circ\varphi^{-1})(x+hv)-(f\circ\varphi^{-1})(x)}{h}\\[0.3em]&=v^\mu\frac{\partial}{\partial x^\mu}(f\circ\varphi^{-1})(x)\end{aligned}$$",
    )
    return


@app.cell(hide_code=True)
def _(lk):
    # module: calculus of scalar functions
    # smoothness does not depend on the chart
    lk.prose(
        r"$\Longrightarrow$ &nbsp; given two charts &nbsp; $\begin{aligned}\varphi&:U\longrightarrow V\subseteq\mathbb R^m\ni x\\\tilde\varphi&:\tilde U\longrightarrow\tilde V\subseteq\mathbb R^m\ni\tilde x\end{aligned}$",
        lk.aside(
            r"$$\left.\begin{aligned}f\circ\varphi^{-1}&:V\longrightarrow\mathbb R\\f\circ\tilde\varphi^{-1}&:\tilde V\longrightarrow\mathbb R\end{aligned}\right\}$$",
            r"representations of $f$ in each chart",
        ),
        r"> are related via",
        r"$$(f\circ\varphi^{-1})(x)=(f\circ\tilde\varphi^{-1})\circ\underbrace{(\tilde\varphi\circ\varphi^{-1})(x)}_{\tilde x(x)}\qquad\text{on }\varphi(U\cap\tilde U)\subseteq V$$",
        lk.aside(
            r"$\displaystyle\begin{aligned}\Longrightarrow\quad\frac{\partial}{\partial x^\mu}(f\circ\varphi^{-1})(x)&=\frac{\partial}{\partial\tilde x^\nu}(f\circ\tilde\varphi^{-1})(\tilde x(x))\,\frac{\partial\tilde x^\nu}{\partial x^\mu}(x)\\[0.3em]&=\underbrace{\frac{\partial\tilde x^\nu}{\partial x^\mu}(x)}_{\footnotesize\begin{matrix}\text{Jacobian matrix of the}\\\text{change of coordinates}\\\tilde x=\tilde\varphi\circ\varphi^{-1}(x)\end{matrix}}\frac{\partial}{\partial\tilde x^\nu}(f\circ\tilde\varphi^{-1})(\tilde x(x))\end{aligned}$",
            r"smooth by assumption",
            at="last",
        ),
        r"$\therefore$ &nbsp; the notion of smoothness for $f:M\to\mathbb R$ via charts is well-defined because changes of charts are always smooth!",
    )
    return


@app.cell(hide_code=True)
def _(lk, mo, s_lat, section_figure, stereo_scene):
    # module: calculus of scalar functions
    # example: the two stereographic charts of the sphere
    lk.example(
        [
            r"$\mathbb S^2=\{(x,y,z)\in\mathbb R^3\mid x^2+y^2+z^2=1\}$",
            r"""
            Choose a point &nbsp; $n=(0,0,1)$ &nbsp; (north pole)

            > Define &nbsp; $\varphi_n:\mathbb S^2-\{n\}\longrightarrow\mathbb R^2$ &nbsp; via stereographic projection

            > > $\varphi_n(x,y,z)=(u,v)=\Big(\dfrac{x}{1-z},\ \dfrac{y}{1-z}\Big)$
            """,
            lk.figure(stereo_scene()),
            lk.aside(
                r"$$\begin{bmatrix}u\\v\\0\end{bmatrix}=\frac{1}{z}\begin{bmatrix}u-x\\v-y\\0\end{bmatrix}$$",
                r"line through $n$ and $p$ in $\mathbb R^3$,<br>by triangle similarity",
            ),
            r"> > > $\Longrightarrow$ &nbsp; $\varphi_n$ is a bijection from $\underset{\substack{\shortparallel\\\textstyle U_n}}{\mathbb S^2-\{n\}}$ to $\underset{\substack{\shortparallel\\\textstyle V_n}}{\mathbb R^2}$",
            lk.gap(),
            r"""
            Choose &nbsp; $s=(0,0,-1)$ &nbsp; (south pole)

            > $\varphi_s:\overset{\substack{\textstyle U_s\\\shortparallel}}{\mathbb S^2-\{s\}}\longrightarrow\overset{\substack{\textstyle V_s\\\shortparallel}}{\mathbb R^2}$, &nbsp;&nbsp; $(x,y,z)\longmapsto\varphi_s(x,y,z)=(\tilde u,\tilde v)=\Big(\dfrac{x}{1+z},\ \dfrac{y}{1+z}\Big)$

            > is also a bijection
            """,
            lk.interactive(section_figure(s_lat.value), controls=[s_lat]),
            r"""
            • &nbsp; $U_n\cup U_s=(\mathbb S^2-\{n\})\cup(\mathbb S^2-\{s\})=\mathbb S^2$

            $\begin{alignedat}{3}\text{•}\ \ \ &V_n,\,V_s\text{ are open},\ \ &&\varphi_n(U_n\cap U_s)&&=\mathbb R^2-\{(0,0)\}\\&&&\varphi_s(U_s\cap U_n)&&=\mathbb R^2-\{(0,0)\}\quad\text{are open}\end{alignedat}$

            • &nbsp; $\varphi_s\circ\varphi_n^{-1}:\mathbb R^2-\{(0,0)\}\longrightarrow\mathbb R^2-\{(0,0)\}$ &nbsp; is smooth with smooth inverse!

            > $\varphi_s\circ\varphi_n^{-1}(u,v)=\Big(\dfrac{u}{u^2+v^2},\ \dfrac{v}{u^2+v^2}\Big)=(\tilde u,\tilde v)$
            """,
        ],
        label="ex-stereographic",
    )
    return


if __name__ == "__main__":
    app.run()
