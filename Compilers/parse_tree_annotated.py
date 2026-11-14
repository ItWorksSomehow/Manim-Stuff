from manim import *

# ─── Colour palette ───────────────────────────────────────────────────────────
BG          = "#00B140"
ROOT_COL    = "#1A1A2E"
STREAM_COL  = "#16213E"
FUNC_COL    = "#0F3460"
ARG_COL     = "#533483"
LEAF_COL    = "#E94560"
EDGE_COL    = "#FFFFFF"
TEXT_COL    = "#FFFFFF"

# Annotation palette
ANN_BG      = "#FFD700"   # gold pill background
ANN_TEXT    = "#111111"   # dark text on gold
ANN_BORDER  = "#FFA500"   # orange border
TYPE_COL    = "#00FFFF"   # cyan  — grammar-rule labels
TOKEN_COL   = "#FFD700"   # gold  — token labels on leaf edges
SEP_COL     = "#AAFFAA"   # green — separator annotations


# ─── Helpers ──────────────────────────────────────────────────────────────────
def make_node(label, color, width=2.6, height=0.55, font_size=20):
    rect = RoundedRectangle(
        corner_radius=0.15, width=width, height=height,
        fill_color=color, fill_opacity=1,
        stroke_color=WHITE, stroke_width=2,
    )
    txt = Text(label, font_size=font_size, color=TEXT_COL, weight=BOLD)
    txt.move_to(rect.get_center())
    return VGroup(rect, txt)


def make_edge(parent, child):
    return Line(parent.get_bottom(), child.get_top(),
                color=EDGE_COL, stroke_width=2.5)


def annotation_pill(label, text_col=ANN_TEXT, bg_col=ANN_BG,
                    border_col=ANN_BORDER, font_size=15):
    """A small rounded pill with a label — sits on a branch."""
    txt  = Text(label, font_size=font_size, color=text_col, weight=BOLD)
    pill = RoundedRectangle(
        corner_radius=0.12,
        width=txt.width + 0.32,
        height=txt.height + 0.18,
        fill_color=bg_col, fill_opacity=1,
        stroke_color=border_col, stroke_width=1.8,
    )
    pill.move_to(txt.get_center())
    return VGroup(pill, txt)


def place_on_edge(pill, line, side=LEFT, offset=0.18):
    """Position a pill beside the midpoint of a Line, slightly to one side."""
    mid = line.get_center()
    pill.move_to(mid + side * offset)
    return pill


# ─── Scene ────────────────────────────────────────────────────────────────────
class AnnotatedParseTree(Scene):

    def construct(self):
        self.camera.background_color = BG

        # ══════════════════════════════════════════════════════════════════════
        # 1.  POSITIONS  (identical to original)
        # ══════════════════════════════════════════════════════════════════════
        y0, y1, y2, y3, y4 = 3.3, 2.0, 0.5, -0.9, -2.4

        root_pos    = UP * y0
        stream_pos  = UP * y1
        cout_pos    = UP * y2 + LEFT * 5.0
        lit_pos     = UP * y2 + LEFT * 1.8
        fc_pos      = UP * y2 + RIGHT * 1.6
        endl_pos    = UP * y2 + RIGHT * 5.0
        lcs_id_pos  = UP * y3 + LEFT * 0.3
        arglist_pos = UP * y3 + RIGHT * 3.2
        str1_pos    = UP * y4 + LEFT * 0.5
        str2_pos    = UP * y4 + RIGHT * 1.3
        n_pos       = UP * y4 + RIGHT * 2.8
        m_pos       = UP * y4 + RIGHT * 4.1

        # ══════════════════════════════════════════════════════════════════════
        # 2.  NODES
        # ══════════════════════════════════════════════════════════════════════
        n_root    = make_node("Output Statement",       ROOT_COL,   width=3.2)
        n_stream  = make_node("Stream Insertion Expr",  STREAM_COL, width=3.6)
        n_cout    = make_node("cout",                   LEAF_COL,   width=1.6)
        n_lit     = make_node('"Length of LCS is: "',  LEAF_COL,   width=3.4, font_size=17)
        n_fc      = make_node("Function Call",          FUNC_COL,   width=2.5)
        n_endl    = make_node("endl",                   LEAF_COL,   width=1.6)
        n_lcsid   = make_node("lcs",                    FUNC_COL,   width=1.5)
        n_arglist = make_node("Argument List",          ARG_COL,    width=2.5)
        n_str1    = make_node("str1",                   LEAF_COL,   width=1.5)
        n_str2    = make_node("str2",                   LEAF_COL,   width=1.5)
        n_n       = make_node("n",                      LEAF_COL,   width=1.0)
        n_m       = make_node("m",                      LEAF_COL,   width=1.0)

        all_nodes = [n_root, n_stream, n_cout, n_lit, n_fc, n_endl,
                     n_lcsid, n_arglist, n_str1, n_str2, n_n, n_m]
        all_pos   = [root_pos, stream_pos, cout_pos, lit_pos, fc_pos, endl_pos,
                     lcs_id_pos, arglist_pos, str1_pos, str2_pos, n_pos, m_pos]
        for nd, pos in zip(all_nodes, all_pos):
            nd.move_to(pos)

        # ══════════════════════════════════════════════════════════════════════
        # 3.  EDGES
        # ══════════════════════════════════════════════════════════════════════
        e_root_stream  = make_edge(n_root,    n_stream)
        e_stream_cout  = make_edge(n_stream,  n_cout)
        e_stream_lit   = make_edge(n_stream,  n_lit)
        e_stream_fc    = make_edge(n_stream,  n_fc)
        e_stream_endl  = make_edge(n_stream,  n_endl)
        e_fc_lcs       = make_edge(n_fc,      n_lcsid)
        e_fc_args      = make_edge(n_fc,      n_arglist)
        e_args_str1    = make_edge(n_arglist, n_str1)
        e_args_str2    = make_edge(n_arglist, n_str2)
        e_args_n       = make_edge(n_arglist, n_n)
        e_args_m       = make_edge(n_arglist, n_m)

        all_edges = [e_root_stream, e_stream_cout, e_stream_lit,
                     e_stream_fc, e_stream_endl, e_fc_lcs, e_fc_args,
                     e_args_str1, e_args_str2, e_args_n, e_args_m]

        # ══════════════════════════════════════════════════════════════════════
        # 4.  TITLE
        # ══════════════════════════════════════════════════════════════════════
        title = Text('cout << "Length of LCS is: " << lcs(str1, str2, n, m) << endl ;',
                     font_size=19, color=WHITE)
        title.to_edge(UP, buff=0.14)

        # ══════════════════════════════════════════════════════════════════════
        # 5.  DRAW THE FULL TREE INSTANTLY (no build animation)
        # ══════════════════════════════════════════════════════════════════════
        tree_group = VGroup(*all_edges, *all_nodes, title)
        self.add(tree_group)
        self.wait(0.6)

        # ══════════════════════════════════════════════════════════════════════
        # 6.  ANNOTATION DEFINITIONS
        #
        #   Each tuple: (pill_label, bg_col, text_col, border_col,
        #                line_object, side, offset)
        #
        #   Grammar-rule labels  → cyan bg
        #   Token/terminal labels → gold bg
        #   Separator labels      → green bg
        # ══════════════════════════════════════════════════════════════════════
        CYAN_BG  = "#003A5C"
        CYAN_BD  = "#00FFFF"
        CYAN_TX  = "#00FFFF"

        GOLD_BG  = "#3D2F00"
        GOLD_BD  = "#FFD700"
        GOLD_TX  = "#FFD700"

        GREEN_BG = "#003310"
        GREEN_BD = "#AAFFAA"
        GREEN_TX = "#AAFFAA"

        RED_BG   = "#3D0010"
        RED_BD   = "#FF6688"
        RED_TX   = "#FF6688"

        def ann(label, bg, tx, bd, line, side=LEFT, off=0.28, fsize=15):
            p = annotation_pill(label, text_col=tx, bg_col=bg,
                                 border_col=bd, font_size=fsize)
            place_on_edge(p, line, side=side, offset=off)
            return p

        annotations = [
            # ── root → stream  (the whole statement rule)
            ann("output-stmt",   CYAN_BG, CYAN_TX, CYAN_BD,
                e_root_stream,   LEFT, 0.9),

            # ── stream → cout  (leftmost operand / stream object)
            ann("stream-obj",    CYAN_BG, CYAN_TX, CYAN_BD,
                e_stream_cout,   LEFT, 0.9),
            ann("Identifier",    GOLD_BG, GOLD_TX, GOLD_BD,
                e_stream_cout,   RIGHT, 0.75),

            # ── stream → literal  (first << operand)
            ann("<<",            GOLD_BG, GOLD_TX, GOLD_BD,
                e_stream_lit,    LEFT, 0.55),
            ann("string-literal", CYAN_BG, CYAN_TX, CYAN_BD,
                e_stream_lit,    RIGHT, 0.85),

            # ── stream → function call  (second << operand)
            ann("<<",            GOLD_BG, GOLD_TX, GOLD_BD,
                e_stream_fc,     LEFT, 0.45),
            ann("expr",          CYAN_BG, CYAN_TX, CYAN_BD,
                e_stream_fc,     RIGHT, 0.55),

            # ── stream → endl  (third << operand)
            ann("<<",            GOLD_BG, GOLD_TX, GOLD_BD,
                e_stream_endl,   LEFT, 0.55),
            ann("Identifier",    GOLD_BG, GOLD_TX, GOLD_BD,
                e_stream_endl,   RIGHT, 0.75),

            # ── fc → lcs identifier
            ann("func-id",       CYAN_BG, CYAN_TX, CYAN_BD,
                e_fc_lcs,        LEFT, 0.7),
            ann("Identifier",    GOLD_BG, GOLD_TX, GOLD_BD,
                e_fc_lcs,        RIGHT, 0.7),

            # ── fc → arg-list
            ann("arg-list",      CYAN_BG, CYAN_TX, CYAN_BD,
                e_fc_args,       LEFT, 0.65),
            ann("( … )",         GREEN_BG, GREEN_TX, GREEN_BD,
                e_fc_args,       RIGHT, 0.6),

            # ── arg-list → str1
            ann("param₁",        CYAN_BG, CYAN_TX, CYAN_BD,
                e_args_str1,     LEFT, 0.62),
            ann("Identifier",    GOLD_BG, GOLD_TX, GOLD_BD,
                e_args_str1,     RIGHT, 0.72),

            # ── arg-list → str2
            ann("param₂",        CYAN_BG, CYAN_TX, CYAN_BD,
                e_args_str2,     LEFT, 0.6),
            ann("Identifier",    GOLD_BG, GOLD_TX, GOLD_BD,
                e_args_str2,     RIGHT, 0.72),

            # ── arg-list → n
            ann("param₃",        CYAN_BG, CYAN_TX, CYAN_BD,
                e_args_n,        LEFT, 0.62),
            ann("Identifier",    GOLD_BG, GOLD_TX, GOLD_BD,
                e_args_n,        RIGHT, 0.72),

            # ── arg-list → m
            ann("param₄",        CYAN_BG, CYAN_TX, CYAN_BD,
                e_args_m,        LEFT, 0.6),
            ann("Identifier",    GOLD_BG, GOLD_TX, GOLD_BD,
                e_args_m,        RIGHT, 0.72),
        ]

        # ══════════════════════════════════════════════════════════════════════
        # 7.  ANIMATE ANNOTATIONS — pop in one by one with a scale bounce
        # ══════════════════════════════════════════════════════════════════════
        for pill in annotations:
            self.play(
                FadeIn(pill, scale=0.4),
                run_time=0.38,
                rate_func=there_and_back_with_pause  # little bounce
            )
            # override: we want it to STAY visible, so just use GrowFromCenter
        # redo with proper staying animation
        for pill in annotations:
            self.remove(pill)

        self.wait(0.2)

        # Proper sequential pop-in that stays
        for pill in annotations:
            self.play(
                GrowFromCenter(pill),
                run_time=0.32
            )
            self.wait(0.08)

        # ══════════════════════════════════════════════════════════════════════
        # 8.  LEGEND  (bottom-left corner)
        # ══════════════════════════════════════════════════════════════════════
        self.wait(0.4)

        leg_items = [
            ("Grammar Rule",  CYAN_BG,  CYAN_TX,  CYAN_BD),
            ("Token / Terminal", GOLD_BG, GOLD_TX, GOLD_BD),
            ("Separator",     GREEN_BG, GREEN_TX, GREEN_BD),
        ]
        legend_pills = []
        for lbl, bg, tx, bd in leg_items:
            p = annotation_pill(lbl, text_col=tx, bg_col=bg,
                                 border_col=bd, font_size=13)
            legend_pills.append(p)

        legend = VGroup(*legend_pills).arrange(RIGHT, buff=0.3)
        legend.to_corner(DL, buff=0.22)

        legend_title = Text("Legend:", font_size=13, color=WHITE)
        legend_title.next_to(legend, UP, buff=0.1, aligned_edge=LEFT)

        self.play(
            FadeIn(legend_title),
            LaggedStart(*[GrowFromCenter(p) for p in legend_pills],
                        lag_ratio=0.2, run_time=0.8)
        )

        # ══════════════════════════════════════════════════════════════════════
        # 9.  FINAL HOLD + ROOT GLOW
        # ══════════════════════════════════════════════════════════════════════
        self.wait(1.5)

        glow = n_root[0].copy()
        glow.set_stroke(color=YELLOW, width=7, opacity=0.7)
        self.play(FadeIn(glow), run_time=0.4)
        self.play(FadeOut(glow), run_time=0.4)

        self.wait(3)