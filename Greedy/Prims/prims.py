from manim import *

# --- 9:16 VERTICAL FRAME (Reels / Shorts) ---
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16


class PrimAlgorithm(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Neon Color Palette
        NEON_CYAN = "#00FFFF"
        NEON_PINK = "#FF00FF"
        NEON_GREEN = "#39FF14"
        NEON_YELLOW = "#FFFF00"
        NEON_RED = "#FF3131"
        EDGE_BASE = "#4A4A6A"

        # --- GRAPH DATA (same graph as the Boruvka scene, for easy comparison) ---
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

        # --- MOBJECTS ---
        def get_node(name):
            c = Circle(radius=0.5, color=NEON_CYAN, stroke_width=6,
                       fill_color=BLACK, fill_opacity=1)
            t = Text(name, color=NEON_CYAN, font_size=36, weight=BOLD)
            return VGroup(c, t).move_to(pos[name]).set_z_index(3)

        nodes = {n: get_node(n) for n in names}

        edge_mobs, weight_tags = {}, {}
        for e in edges:
            u, v, w = e
            line = Line(pos[u], pos[v], color=EDGE_BASE, stroke_width=4)
            line.set_z_index(0)
            edge_mobs[key(e)] = line
            t = Text(str(w), color=WHITE, font_size=28, weight=BOLD)
            bg = BackgroundRectangle(t, color=BLACK, fill_opacity=1, buff=0.08)
            weight_tags[key(e)] = VGroup(bg, t).move_to(line.get_center()).set_z_index(1)

        # --- TEXT HELPERS ---
        cur_status = [None]
        cur_frontier = [None]

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

        def show_frontier(frontier):
            # Frontier list, always sorted by weight (like a priority queue)
            body = "   ".join(f"{u}-{v}({w})" for u, v, w in frontier)
            new = Text("Frontier:  " + body, color=NEON_YELLOW, font_size=26)
            if new.width > 8:
                new.scale_to_fit_width(8)
            new.to_edge(DOWN, buff=2.7)
            anims = [FadeIn(new)]
            if cur_frontier[0] is not None:
                anims.append(FadeOut(cur_frontier[0]))
            self.play(*anims, run_time=0.4)
            cur_frontier[0] = new

        # --- DRAW GRAPH ---
        self.play(
            LaggedStart(*[FadeIn(nodes[n]) for n in names], lag_ratio=0.1),
            *[Create(m) for m in edge_mobs.values()],
            *[FadeIn(t) for t in weight_tags.values()],
            run_time=1.8,
        )
        self.wait(0.5)

        # --- PRIM'S ALGORITHM ---
        start = "A"
        in_tree = {start}
        mst = set()
        lit = set()          # edges currently shown as frontier (yellow)
        total = 0

        say(f"Start from vertex {start}", NEON_GREEN)
        self.play(
            nodes[start][0].animate.set_stroke(color=NEON_GREEN, width=8),
            nodes[start][1].animate.set_color(NEON_GREEN),
            run_time=0.7,
        )
        self.wait(0.5)

        while len(in_tree) < len(names):
            # 1) frontier = all edges with exactly one endpoint in the tree
            frontier = sorted(
                [e for e in edges if (e[0] in in_tree) != (e[1] in in_tree)],
                key=lambda e: e[2],
            )
            show_frontier(frontier)
            say("Edges leaving the tree", NEON_YELLOW)
            anims = [edge_mobs[key(e)].animate.set_color(NEON_YELLOW).set_stroke(width=7)
                     for e in frontier if key(e) not in lit]
            lit |= {key(e) for e in frontier}
            if anims:
                self.play(*anims, run_time=0.5)
            self.wait(0.4)

            # 2) pick the cheapest frontier edge
            best = frontier[0]
            say(f"Cheapest edge = {best[0]}-{best[1]}  (weight {best[2]})", NEON_CYAN)
            self.play(
                edge_mobs[key(best)].animate.set_color(NEON_CYAN).set_stroke(width=10),
                Indicate(weight_tags[key(best)], color=NEON_CYAN, scale_factor=1.4),
                run_time=0.8,
            )
            self.wait(0.3)

            # 3) add the new vertex + edge to the tree
            new = best[1] if best[0] in in_tree else best[0]
            in_tree.add(new)
            mst.add(key(best))
            lit.discard(key(best))
            total += best[2]

            say(f"Add vertex {new} to the tree", NEON_GREEN)
            self.play(
                edge_mobs[key(best)].animate.set_color(NEON_GREEN).set_stroke(width=9),
                nodes[new][0].animate.set_stroke(color=NEON_GREEN, width=8),
                nodes[new][1].animate.set_color(NEON_GREEN),
                run_time=0.8,
            )

            # 4) frontier edges whose both ends are now in the tree would form a cycle
            rejected = [e for e in edges
                        if key(e) in lit and e[0] in in_tree and e[1] in in_tree]
            if rejected:
                txt = ", ".join(f"{u}-{v}" for u, v, w in rejected)
                say(f"{txt} would form a cycle - skip", NEON_RED)
                self.play(
                    *[edge_mobs[key(e)].animate.set_color(EDGE_BASE).set_stroke(width=4)
                      for e in rejected],
                    run_time=0.6,
                )
                lit -= {key(e) for e in rejected}
            self.wait(0.6)

        # --- FINAL: MST ---
        anims = [FadeOut(cur_frontier[0])]
        for e in edges:
            if key(e) in mst:
                anims.append(edge_mobs[key(e)].animate.set_color(NEON_GREEN).set_stroke(width=10))
            else:
                anims.append(edge_mobs[key(e)].animate.set_stroke(opacity=0.25))
        self.play(*anims, run_time=1.2)

        say(f"Minimum Spanning Tree  -  total weight = {total}", NEON_GREEN, rt=0.6)
        self.wait(3)