from manim import *

# --- 9:16 VERTICAL FRAME (Reels / Shorts) ---
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16


class HNode:
    """One node of the Huffman forest / tree."""

    def __init__(self, freq, order, sym=None, left=None, right=None):
        self.freq = freq
        self.order = order      # tie-breaker for the priority queue
        self.sym = sym          # None for internal nodes
        self.left = left
        self.right = right
        self.mob = None
        self.l_edge = None
        self.r_edge = None


class HuffmanEncoding(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Neon Color Palette
        NEON_CYAN = "#00FFFF"
        NEON_PINK = "#FF00FF"
        NEON_GREEN = "#39FF14"
        NEON_YELLOW = "#FFFF00"
        NEON_ORANGE = "#FF6700"
        NEON_PURPLE = "#BC13FE"
        EDGE_BASE = "#6A6A9A"
        table_colors = [NEON_CYAN, NEON_PINK, NEON_GREEN,
                        NEON_YELLOW, NEON_ORANGE, NEON_PURPLE]

        # --- INPUT: symbol frequencies (all distinct, so no ties) ---
        freqs = [("A", 5), ("B", 9), ("C", 12), ("D", 13), ("E", 16), ("F", 45)]

        # --- LAYOUT CONSTANTS ---
        Y_TOP, DY = 5.6, 1.65     # root height, vertical gap per level
        SP, GAP = 1.25, 0.25      # leaf spacing, extra gap between trees

        counter = [0]

        def new_order():
            counter[0] += 1
            return counter[0]

        def is_leaf(n):
            return n.left is None

        def qlabel(n):
            return f"{n.sym}{n.freq}" if is_leaf(n) else f"[{n.freq}]"

        def sort_forest(forest):
            forest.sort(key=lambda n: (n.freq, n.order))

        # --- FOREST LAYOUT: trees side by side, root row at the top ---
        def layout(forest):
            pos = {}
            cx = [0.0]

            def place(node, depth):
                y = Y_TOP - depth * DY
                if is_leaf(node):
                    x = cx[0]
                    cx[0] += SP
                else:
                    lx = place(node.left, depth + 1)
                    rx = place(node.right, depth + 1)
                    x = (lx + rx) / 2
                pos[node] = np.array([x, y, 0.0])
                return x

            for i, root in enumerate(forest):
                if i > 0:
                    cx[0] += GAP
                place(root, 0)
            xs = [p[0] for p in pos.values()]
            shift = (max(xs) + min(xs)) / 2
            for p in pos.values():
                p[0] -= shift
            return pos

        # --- MOBJECT BUILDERS ---
        def build_node_mob(n):
            if is_leaf(n):
                c = Circle(radius=0.45, color=NEON_CYAN, stroke_width=6,
                           fill_color=BLACK, fill_opacity=1)
                s = Text(n.sym, color=NEON_CYAN, font_size=26, weight=BOLD)
                f = Text(str(n.freq), color=WHITE, font_size=20)
                content = VGroup(s, f).arrange(DOWN, buff=0.02)
            else:
                c = Circle(radius=0.45, color=NEON_YELLOW, stroke_width=6,
                           fill_color=BLACK, fill_opacity=1)
                content = Text(str(n.freq), color=NEON_YELLOW,
                               font_size=28, weight=BOLD)
            content.move_to(c.get_center())
            return VGroup(c, content).set_z_index(3)

        def make_edge(parent, child, bit):
            p, c = parent.mob[0].get_center(), child.mob[0].get_center()
            line = Line(p, c, color=EDGE_BASE, stroke_width=4).set_z_index(0)
            line.add_updater(
                lambda l, a=parent, b=child: l.put_start_and_end_on(
                    a.mob[0].get_center(), b.mob[0].get_center())
            )
            t = Text(str(bit), color=NEON_PINK if bit else NEON_CYAN,
                     font_size=26, weight=BOLD)
            bg = BackgroundRectangle(t, color=BLACK, fill_opacity=1, buff=0.06)
            lab = VGroup(bg, t).set_z_index(1)
            off = RIGHT * 0.3 if bit else LEFT * 0.3
            lab.move_to((p + c) / 2 + off)
            lab.add_updater(
                lambda m, a=parent, b=child, o=off: m.move_to(
                    (a.mob[0].get_center() + b.mob[0].get_center()) / 2 + o)
            )
            return line, lab

        # --- TEXT HELPERS ---
        cur_status = [None]
        cur_queue = [None]

        def say(msg, color=WHITE, rt=0.4):
            new = Text(msg, color=color, font_size=30)
            if new.width > 8:
                new.scale_to_fit_width(8)
            new.to_edge(DOWN, buff=1.6)
            anims = [FadeIn(new, shift=UP * 0.2)]
            if cur_status[0] is not None:
                anims.append(FadeOut(cur_status[0]))
            self.play(*anims, run_time=rt)
            cur_status[0] = new

        def show_queue(forest):
            body = "  ".join(qlabel(n) for n in forest)
            new = Text("Queue:  " + body, color=NEON_YELLOW, font_size=26)
            if new.width > 8:
                new.scale_to_fit_width(8)
            new.to_edge(DOWN, buff=2.7)
            anims = [FadeIn(new)]
            if cur_queue[0] is not None:
                anims.append(FadeOut(cur_queue[0]))
            self.play(*anims, run_time=0.4)
            cur_queue[0] = new

        # --- BUILD INITIAL FOREST (one leaf per symbol) ---
        forest = [HNode(f, new_order(), sym=s) for s, f in freqs]
        sort_forest(forest)
        all_nodes = list(forest)
        pos = layout(forest)
        for n in forest:
            n.mob = build_node_mob(n).move_to(pos[n])

        say("Count how often each symbol appears")
        self.play(LaggedStart(*[FadeIn(n.mob) for n in forest], lag_ratio=0.15),
                  run_time=1.6)
        show_queue(forest)
        self.wait(0.8)

        # --- HUFFMAN: repeatedly merge the two smallest trees ---
        while len(forest) > 1:
            a, b = forest[0], forest[1]     # smallest two (a < b)
            rest = forest[2:]

            say(f"Take the two smallest:  {qlabel(a)}  and  {qlabel(b)}", NEON_CYAN)
            self.play(
                Indicate(a.mob, color=NEON_CYAN, scale_factor=1.3),
                Indicate(b.mob, color=NEON_CYAN, scale_factor=1.3),
                run_time=0.9,
            )

            total = a.freq + b.freq
            parent = HNode(total, new_order(), left=a, right=b)
            say(f"Merge:  {a.freq} + {b.freq} = {total}", NEON_YELLOW)

            forest = rest + [parent]
            sort_forest(forest)
            pos = layout(forest)

            # (a) existing nodes slide to their new places (edges follow)
            self.play(*[n.mob.animate.move_to(pos[n]) for n in all_nodes],
                      run_time=0.9)

            # (b) the new parent drops in with its two labelled edges
            parent.mob = build_node_mob(parent).move_to(pos[parent])
            parent.l_edge, l_lab = make_edge(parent, a, 0)
            parent.r_edge, r_lab = make_edge(parent, b, 1)
            self.play(
                FadeIn(parent.mob),
                Create(parent.l_edge), Create(parent.r_edge),
                FadeIn(l_lab), FadeIn(r_lab),
                run_time=0.9,
            )
            all_nodes.append(parent)

            show_queue(forest)
            self.wait(0.4)

        root = forest[0]
        say(f"One tree left - root = {root.freq} (total count)", NEON_GREEN)
        self.wait(1)

        # --- READ THE CODES: root -> leaf, left = 0, right = 1 ---
        codes, paths, leaves = {}, {}, {}

        def walk(node, code, path):
            if is_leaf(node):
                codes[node.sym] = code
                paths[node.sym] = path
                leaves[node.sym] = node
            else:
                walk(node.left, code + "0", path + [node.l_edge])
                walk(node.right, code + "1", path + [node.r_edge])

        walk(root, "", [])

        self.play(FadeOut(cur_queue[0]), run_time=0.4)
        say("Read the edge bits from the root to each symbol", NEON_GREEN)
        self.wait(0.5)

        order = sorted(codes, key=lambda s: (len(codes[s]), codes[s]))
        for i, sym in enumerate(order):
            code = codes[sym]
            leaf_circle = leaves[sym].mob[0]

            say(f"Path to {sym}:  {code}", NEON_GREEN, rt=0.3)
            self.play(
                *[e.animate.set_color(NEON_GREEN).set_stroke(width=9)
                  for e in paths[sym]],
                leaf_circle.animate.set_stroke(color=NEON_GREEN, width=9),
                run_time=0.6,
            )

            entry = Text(f"{sym} = {code}", color=table_colors[i], font_size=36,
                         weight=BOLD)
            col, row = divmod(i, 3)
            entry.move_to([-2.2 + col * 4.4, -2.7 - row * 1.2, 0])
            self.play(FadeIn(entry, shift=UP * 0.2), run_time=0.4)

            self.play(
                *[e.animate.set_color(EDGE_BASE).set_stroke(width=4)
                  for e in paths[sym]],
                leaf_circle.animate.set_stroke(color=NEON_CYAN, width=6),
                run_time=0.4,
            )

        # --- COMPARE WITH FIXED-LENGTH CODE ---
        huff_bits = sum(f * len(codes[s]) for s, f in freqs)
        total_count = sum(f for _, f in freqs)
        fixed_bits = total_count * 3        # 6 symbols need 3 bits each
        saved = round(100 * (fixed_bits - huff_bits) / fixed_bits)

        say(f"Huffman: {huff_bits} bits  vs  fixed 3-bit: {fixed_bits} bits"
            f"  ({saved}% smaller)", NEON_GREEN, rt=0.6)
        self.wait(3)