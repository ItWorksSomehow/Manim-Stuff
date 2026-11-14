from manim import *

# ─── Colour palette ───────────────────────────────────────────────────────────
BG          = "#00B140"          # bright-green chroma-key background
ROOT_COL    = "#1A1A2E"
STREAM_COL  = "#16213E"
FUNC_COL    = "#0F3460"
ARG_COL     = "#533483"
LEAF_COL    = "#E94560"
EDGE_COL    = "#FFFFFF"
TEXT_COL    = "#FFFFFF"
TOKEN_BG    = "#222831"
TOKEN_TEXT  = "#EEEEEE"


# ─── Helper: rounded-rect node ────────────────────────────────────────────────
def make_node(label: str, color: str, width=2.6, height=0.55, font_size=20):
    rect = RoundedRectangle(
        corner_radius=0.15, width=width, height=height,
        fill_color=color, fill_opacity=1,
        stroke_color=WHITE, stroke_width=2
    )
    txt = Text(label, font_size=font_size, color=TEXT_COL, weight=BOLD)
    txt.move_to(rect.get_center())
    return VGroup(rect, txt)


def make_token_chip(label: str, font_size=16):
    rect = RoundedRectangle(
        corner_radius=0.12, width=len(label)*0.13 + 0.6, height=0.42,
        fill_color=TOKEN_BG, fill_opacity=1,
        stroke_color="#AAAAAA", stroke_width=1.5
    )
    txt = Text(label, font_size=font_size, color=TOKEN_TEXT)
    txt.move_to(rect.get_center())
    return VGroup(rect, txt)


# ─── Scene ────────────────────────────────────────────────────────────────────
class ParseTreeScene(Scene):

    def construct(self):
        self.camera.background_color = BG

        # ── 1. TOKEN STRIP ────────────────────────────────────────────────────
        raw_tokens = [
            "cout", "<<", '"Length…"', "<<",
            "lcs", "(", "str1", ",", "str2", ",", "n", ",", "m", ")",
            "<<", "endl", ";"
        ]
        chips = VGroup(*[make_token_chip(t) for t in raw_tokens])
        chips.arrange(RIGHT, buff=0.18)
        chips.scale_to_fit_width(13.5)
        chips.move_to(DOWN * 3.5)

        self.play(LaggedStart(*[FadeIn(c, shift=UP*0.3) for c in chips],
                               lag_ratio=0.07, run_time=3))
        self.wait(0.4)

        # ── 2. BUILD TREE NODES ───────────────────────────────────────────────
        #
        #                     Output Statement
        #                           |
        #               Stream Insertion Expression
        #              /      |            |        \
        #           cout  "Length…"   FunctionCall  endl
        #                             /     |
        #                           lcs   ArgList
        #                                /  |  |  \
        #                             str1 str2 n  m
        #
        # --- Positions (manually tuned for a clean 16:9 frame) ---------------
        y0 =  3.3    # root
        y1 =  2.0    # stream expr
        y2 =  0.5    # cout / literal / FuncCall / endl
        y3 = -0.9    # lcs identifier  /  ArgList
        y4 = -2.4    # argument leaves

        root_pos   = UP * y0
        stream_pos = UP * y1

        cout_pos   = UP * y2 + LEFT * 5.0
        lit_pos    = UP * y2 + LEFT * 1.8
        fc_pos     = UP * y2 + RIGHT * 1.6
        endl_pos   = UP * y2 + RIGHT * 5.0

        lcs_id_pos = UP * y3 + LEFT * 0.3
        arglist_pos= UP * y3 + RIGHT * 3.2

        str1_pos   = UP * y4 + LEFT * 0.5
        str2_pos   = UP * y4 + RIGHT * 1.3
        n_pos      = UP * y4 + RIGHT * 2.8
        m_pos      = UP * y4 + RIGHT * 4.1

        # --- Create node VGroups ---------------------------------------------
        n_root   = make_node("Output Statement",        ROOT_COL,  width=3.2)
        n_stream = make_node("Stream Insertion Expr",   STREAM_COL, width=3.6)
        n_cout   = make_node("cout",                    LEAF_COL,  width=1.6)
        n_lit    = make_node('"Length of LCS is: "',   LEAF_COL,  width=3.4, font_size=17)
        n_fc     = make_node("Function Call",           FUNC_COL,  width=2.5)
        n_endl   = make_node("endl",                    LEAF_COL,  width=1.6)
        n_lcsid  = make_node("lcs",                     FUNC_COL,  width=1.5)
        n_arglist= make_node("Argument List",           ARG_COL,   width=2.5)
        n_str1   = make_node("str1",                    LEAF_COL,  width=1.5)
        n_str2   = make_node("str2",                    LEAF_COL,  width=1.5)
        n_n      = make_node("n",                       LEAF_COL,  width=1.0)
        n_m      = make_node("m",                       LEAF_COL,  width=1.0)

        nodes = [n_root, n_stream, n_cout, n_lit, n_fc, n_endl,
                 n_lcsid, n_arglist, n_str1, n_str2, n_n, n_m]
        positions = [root_pos, stream_pos, cout_pos, lit_pos, fc_pos, endl_pos,
                     lcs_id_pos, arglist_pos, str1_pos, str2_pos, n_pos, m_pos]
        for nd, pos in zip(nodes, positions):
            nd.move_to(pos)

        # ── 3. EDGE HELPER ────────────────────────────────────────────────────
        def animated_edge(parent, child):
            start = parent.get_bottom()
            end   = child.get_top()
            line  = Line(start, end, color=EDGE_COL, stroke_width=2.5)
            return Create(line, run_time=0.45)

        def edge(parent, child):
            return Line(parent.get_bottom(), child.get_top(),
                        color=EDGE_COL, stroke_width=2.5)

        # ── 4. ANIMATE ROOT ───────────────────────────────────────────────────
        self.play(FadeOut(chips, shift=UP*0.4), run_time=0.8)
        self.play(FadeIn(n_root, scale=0.7), run_time=0.7)
        self.wait(0.2)

        # ── 5. ROOT → STREAM EXPR ─────────────────────────────────────────────
        self.play(FadeIn(n_stream, scale=0.7), run_time=0.6)
        e_rs = edge(n_root, n_stream)
        self.play(Create(e_rs), run_time=0.5)
        self.wait(0.15)

        # ── 6. STREAM EXPR CHILDREN (left-to-right) ───────────────────────────
        for nd in [n_cout, n_lit, n_fc, n_endl]:
            self.play(FadeIn(nd, scale=0.7), run_time=0.45)
        edges_L2 = [edge(n_stream, c) for c in [n_cout, n_lit, n_fc, n_endl]]
        self.play(*[Create(e) for e in edges_L2], run_time=0.7)
        self.wait(0.2)

        # ── 7. FUNCTION CALL SUBTREE ──────────────────────────────────────────
        self.play(FadeIn(n_lcsid, scale=0.7), FadeIn(n_arglist, scale=0.7),
                  run_time=0.55)
        e_fclcs  = edge(n_fc, n_lcsid)
        e_fcargs = edge(n_fc, n_arglist)
        self.play(Create(e_fclcs), Create(e_fcargs), run_time=0.6)
        self.wait(0.15)

        # ── 8. ARGUMENT LEAVES ────────────────────────────────────────────────
        for nd in [n_str1, n_str2, n_n, n_m]:
            self.play(FadeIn(nd, scale=0.7), run_time=0.35)
        edges_args = [edge(n_arglist, c) for c in [n_str1, n_str2, n_n, n_m]]
        self.play(*[Create(e) for e in edges_args], run_time=0.6)

        # ── 9. OPERATOR / SEPARATOR LABELS ON EDGES ───────────────────────────
        def op_label(text, line, direction=UP):
            lbl = Text(text, font_size=14, color="#FFD700")
            lbl.next_to(line.get_center(), direction, buff=0.1)
            return lbl

        op_cout  = op_label("<<", e_rs,       LEFT*2.5 + UP*0.1)
        op1      = Text("<<", font_size=14, color="#FFD700")
        op1.next_to(edges_L2[1].get_center(), UP, buff=0.08)
        op2      = Text("<<", font_size=14, color="#FFD700")
        op2.next_to(edges_L2[2].get_center(), UP, buff=0.08)
        op3      = Text("<<", font_size=14, color="#FFD700")
        op3.next_to(edges_L2[3].get_center(), UP, buff=0.08)

        comma_labels = []
        for i, nd in enumerate([n_str1, n_str2, n_n]):
            lbl = Text(",", font_size=16, color="#AAFFAA")
            lbl.next_to(nd, RIGHT, buff=0.05)
            comma_labels.append(lbl)

        semi = Text(";", font_size=18, color="#AAAAFF")
        semi.next_to(n_root, RIGHT, buff=0.15)

        self.play(
            *[FadeIn(l) for l in [op1, op2, op3, semi] + comma_labels],
            run_time=0.5
        )

        # ── 10. TITLE ─────────────────────────────────────────────────────────
        title = Text("Parse Tree: cout << \"…\" << lcs(…) << endl;",
                     font_size=21, color="#FFFFFF")
        title.to_edge(UP, buff=0.12)
        self.play(FadeIn(title), run_time=0.5)

        # ── 11. HOLD FINAL FRAME ──────────────────────────────────────────────
        self.wait(3)

        # ── 12. SUBTLE GLOW PULSE ON ROOT ─────────────────────────────────────
        glow = n_root[0].copy()
        glow.set_stroke(color=YELLOW, width=6, opacity=0.6)
        self.play(FadeIn(glow), run_time=0.4)
        self.play(FadeOut(glow), run_time=0.4)
        self.wait(2)

