from manim import *

# --- 9:16 VERTICAL FRAME (Reels / Shorts) ---
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16


class BoruvkaAlgorithm(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Neon Color Palette
        NEON_CYAN = "#00FFFF"
        NEON_PINK = "#FF00FF"
        NEON_GREEN = "#39FF14"
        NEON_YELLOW = "#FFFF00"
        NEON_ORANGE = "#FF6700"
        NEON_PURPLE = "#BC13FE"
        NEON_RED = "#FF3131"
        EDGE_BASE = "#4A4A6A"
        palette = [NEON_CYAN, NEON_PINK, NEON_GREEN, NEON_YELLOW,
                   NEON_ORANGE, NEON_PURPLE, NEON_RED]

        # --- GRAPH DATA (all weights distinct, so no tie issues) ---
        names = list("ABCDEFG")
        pos = {
            "A": [-3.2, 3.0, 0], "B": [-1.3, 5.2, 0],
            "C": [1.3, 5.2, 0],  "D": [3.2, 3.0, 0],
            "E": [-2.4, -3.6, 0], "F": [0.0, -1.4, 0],
            "G": [2.4, -3.6, 0],
        }
        edges = [
            ("A", "B", 6), ("B", "C", 9), ("C", "D", 3),
            ("A", "E", 2), ("B", "F", 8), ("C", "F", 4),
            ("D", "G", 7), ("E", "F", 5), ("F", "G", 1),
        ]

        def key(e):
            return frozenset((e[0], e[1]))

        # --- UNION-FIND ---
        parent = {n: n for n in names}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[max(ra, rb)] = min(ra, rb)

        def gcol(root):
            # Component colour = palette colour of its smallest-named vertex
            return palette[min(names.index(n) for n in names if find(n) == root)]

        # --- MOBJECTS ---
        def get_node(name, color):
            c = Circle(radius=0.5, color=color, stroke_width=6,
                       fill_color=BLACK, fill_opacity=1)
            t = Text(name, color=color, font_size=36, weight=BOLD)
            return VGroup(c, t).move_to(pos[name]).set_z_index(3)

        nodes = {n: get_node(n, palette[i]) for i, n in enumerate(names)}

        edge_mobs, weight_tags = {}, []
        for u, v, w in edges:
            line = Line(pos[u], pos[v], color=EDGE_BASE, stroke_width=4)
            line.set_z_index(0)
            edge_mobs[key((u, v, w))] = line
            t = Text(str(w), color=WHITE, font_size=28, weight=BOLD)
            bg = BackgroundRectangle(t, color=BLACK, fill_opacity=1, buff=0.08)
            tag = VGroup(bg, t).move_to(line.get_center()).set_z_index(1)
            weight_tags.append(tag)

        # --- TEXT HELPERS ---
        cur_status = [None]
        cur_round = [None]

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

        def set_round(n):
            new = Text(f"Round {n}", color=NEON_CYAN, font_size=40,
                       weight=BOLD).to_edge(UP, buff=1.4)
            anims = [FadeIn(new)]
            if cur_round[0] is not None:
                anims.append(FadeOut(cur_round[0]))
            self.play(*anims, run_time=0.4)
            cur_round[0] = new

        # --- DRAW GRAPH ---
        self.play(
            LaggedStart(*[FadeIn(nodes[n]) for n in names], lag_ratio=0.1),
            *[Create(m) for m in edge_mobs.values()],
            *[FadeIn(t) for t in weight_tags],
            run_time=1.8,
        )
        say("Every vertex starts as its own component")
        self.wait(1)

        # --- BORUVKA ---
        chosen = set()
        total = 0
        rnd = 0

        while len({find(n) for n in names}) > 1:
            rnd += 1
            set_round(rnd)
            roots = sorted({find(n) for n in names})
            picks = []

            for r in roots:
                comp = [n for n in names if find(n) == r]
                col = gcol(r)
                out = [e for e in edges if (find(e[0]) == r) != (find(e[1]) == r)]
                best = min(out, key=lambda e: e[2])

                say("{" + ", ".join(comp) + "}  -  all outgoing edges", col)

                # 1) flash all outgoing edges in the component colour
                anims = [edge_mobs[key(e)].animate.set_color(col).set_stroke(width=7)
                         for e in out if key(e) not in chosen]
                if anims:
                    self.play(*anims, run_time=0.5)
                self.wait(0.3)

                # 2) keep only the cheapest one
                say(f"Cheapest edge = {best[0]}-{best[1]}  (weight {best[2]})",
                    NEON_YELLOW)
                anims = [edge_mobs[key(e)].animate.set_color(EDGE_BASE).set_stroke(width=4)
                         for e in out if e is not best and key(e) not in chosen]
                if key(best) not in chosen:
                    anims.append(edge_mobs[key(best)].animate.set_stroke(width=10))
                    chosen.add(key(best))
                    total += best[2]
                if anims:
                    self.play(*anims, run_time=0.5)
                self.wait(0.3)
                picks.append(best)

            # 3) merge components along the chosen edges
            say("Merge components along the chosen edges", NEON_GREEN)
            for u, v, w in picks:
                union(u, v)

            anims = []
            for n in names:
                c = gcol(find(n))
                anims.append(nodes[n][0].animate.set_stroke(color=c, width=6))
                anims.append(nodes[n][1].animate.set_color(c))
            for e in edges:
                if key(e) in chosen:
                    anims.append(edge_mobs[key(e)].animate
                                 .set_color(gcol(find(e[0]))).set_stroke(width=9))
            self.play(*anims, run_time=1.2)

            ncomp = len({find(n) for n in names})
            if ncomp > 1:
                say(f"{ncomp} components left - repeat", WHITE)
            self.wait(1)

        # --- FINAL: MST ---
        anims = []
        for n in names:
            anims.append(nodes[n][0].animate.set_stroke(color=NEON_GREEN, width=7))
            anims.append(nodes[n][1].animate.set_color(NEON_GREEN))
        for e in edges:
            m = edge_mobs[key(e)]
            if key(e) in chosen:
                anims.append(m.animate.set_color(NEON_GREEN).set_stroke(width=10))
            else:
                anims.append(m.animate.set_stroke(opacity=0.25))
        anims.append(FadeOut(cur_round[0]))
        self.play(*anims, run_time=1.5)

        say(f"Minimum Spanning Tree  -  total weight = {total}", NEON_GREEN, rt=0.6)
        self.wait(3)