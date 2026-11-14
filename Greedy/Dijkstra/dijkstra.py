import heapq
from manim import *

# --- 9:16 VERTICAL FRAME (Reels / Shorts) ---
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16


class DijkstraCity(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Neon Color Palette
        NEON_CYAN = "#00FFFF"
        NEON_PINK = "#FF00FF"
        NEON_GREEN = "#39FF14"
        NEON_YELLOW = "#FFFF00"
        CITY_DOT = "#8C8CFF"      # ordinary cities
        ROAD = "#33336A"          # roads before the path is found
        GRID = "#1B1B3A"

        # --- CITY MAP: positions (A = source, B = destination) ---
        pos = {
            "A": np.array([-3.0, -5.5, 0]),
            "1": np.array([-3.2, -2.8, 0]),
            "2": np.array([0.4, -3.4, 0]),
            "3": np.array([3.0, -2.0, 0]),
            "4": np.array([-1.8, 0.0, 0]),
            "5": np.array([1.4, 0.4, 0]),
            "6": np.array([-3.0, 2.8, 0]),
            "7": np.array([0.8, 3.2, 0]),
            "B": np.array([3.0, 5.6, 0]),
        }
        # Roads: (city, city, distance in km)
        roads = [
            ("A", "1", 27), ("A", "2", 40), ("1", "2", 36), ("1", "4", 31),
            ("2", "4", 40), ("2", "3", 30), ("3", "5", 29), ("4", "5", 32),
            ("4", "6", 30), ("5", "7", 29), ("6", "7", 38), ("7", "B", 33),
            ("6", "B", 66),
        ]

        def key(u, v):
            return frozenset((u, v))

        # --- DIJKSTRA (computed for real; the scene only shows the result) ---
        graph = {n: [] for n in pos}
        for u, v, w in roads:
            graph[u].append((v, w))
            graph[v].append((u, w))
        dist = {n: float("inf") for n in pos}
        prev = {}
        dist["A"] = 0
        pq = [(0, "A")]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in graph[u]:
                if d + w < dist[v]:
                    dist[v] = d + w
                    prev[v] = u
                    heapq.heappush(pq, (dist[v], v))
        path = ["B"]
        while path[-1] != "A":
            path.append(prev[path[-1]])
        path.reverse()
        total = dist["B"]

        # --- BACKGROUND GRID (faint city-map feel) ---
        plane = NumberPlane(
            x_range=[-5, 5, 1], y_range=[-9, 9, 1], x_length=10, y_length=18,
            background_line_style={"stroke_color": GRID, "stroke_width": 1,
                                   "stroke_opacity": 0.7},
            axis_config={"stroke_color": GRID, "stroke_width": 1},
        ).set_z_index(-5)

        # --- MOBJECT BUILDERS ---
        def city_dot(p, color):
            glow = Circle(radius=0.32, stroke_width=0, fill_color=color,
                          fill_opacity=0.18)
            core = Dot(radius=0.12, color=color)
            return VGroup(glow, core).move_to(p).set_z_index(3)

        def hub(name, p, color):
            glow = Circle(radius=0.75, stroke_width=0, fill_color=color,
                          fill_opacity=0.15)
            ring = Circle(radius=0.45, color=color, stroke_width=6,
                          fill_color=BLACK, fill_opacity=1)
            t = Text(name, color=color, font_size=36, weight=BOLD)
            return VGroup(glow, ring, t).move_to(p).set_z_index(3)

        node_mobs = {}
        for n, p in pos.items():
            if n == "A":
                node_mobs[n] = hub("A", p, NEON_GREEN)
            elif n == "B":
                node_mobs[n] = hub("B", p, NEON_PINK)
            else:
                node_mobs[n] = city_dot(p, CITY_DOT)

        road_mobs, weight_tags = {}, {}
        for u, v, w in roads:
            line = Line(pos[u], pos[v], color=ROAD, stroke_width=3).set_z_index(0)
            road_mobs[key(u, v)] = line
            t = Text(str(w), color="#7777AA", font_size=20)
            bg = BackgroundRectangle(t, color=BLACK, fill_opacity=1, buff=0.06)
            weight_tags[key(u, v)] = (
                VGroup(bg, t).move_to(line.get_center()).set_z_index(1)
            )

        source_lbl = Text("Source", color=NEON_GREEN, font_size=26)
        source_lbl.next_to(node_mobs["A"], RIGHT, buff=0.3)
        dest_lbl = Text("Destination", color=NEON_PINK, font_size=26)
        dest_lbl.next_to(node_mobs["B"], UP, buff=0.3)

        # --- 1) THE CITY APPEARS ---
        self.play(FadeIn(plane), run_time=0.8)
        order = ["A", "1", "2", "3", "4", "5", "6", "7", "B"]
        self.play(
            LaggedStart(*[FadeIn(node_mobs[n], scale=0.5) for n in order],
                        lag_ratio=0.12),
            run_time=1.6,
        )
        self.play(
            LaggedStart(*[Create(r) for r in road_mobs.values()], lag_ratio=0.08),
            *[FadeIn(t) for t in weight_tags.values()],
            run_time=2.0,
        )
        self.play(
            FadeIn(source_lbl), FadeIn(dest_lbl),
            Indicate(node_mobs["A"], color=NEON_GREEN, scale_factor=1.25),
            Indicate(node_mobs["B"], color=NEON_PINK, scale_factor=1.25),
            run_time=1.0,
        )
        self.wait(0.5)

        # --- 2) A RADAR WAVE RIPPLES OUT FROM THE SOURCE ---
        ring = Circle(radius=0.5, color=NEON_GREEN, stroke_width=4)
        ring.move_to(pos["A"]).set_z_index(2)
        by_dist = sorted(
            roads, key=lambda r: min(dist[r[0]], dist[r[1]]))
        flashes = [
            ShowPassingFlash(
                road_mobs[key(u, v)].copy().set_stroke(color=NEON_CYAN, width=7),
                time_width=0.8,
            )
            for u, v, w in by_dist
        ]
        self.play(
            ring.animate.scale(14).set_stroke(opacity=0),
            LaggedStart(*flashes, lag_ratio=0.12),
            run_time=2.6,
        )
        self.remove(ring)
        self.wait(0.3)

        # --- 3) THE SHORTEST PATH DRAWS ITSELF FROM A TO B ---
        seg_colors = color_gradient([NEON_GREEN, NEON_PINK], len(path) - 1)
        traveler = Dot(radius=0.16, color=WHITE).move_to(pos["A"]).set_z_index(6)
        self.play(FadeIn(traveler), run_time=0.3)

        for i, (u, v) in enumerate(zip(path, path[1:])):
            col = seg_colors[i]
            seg = Line(pos[u], pos[v], color=col, stroke_width=10).set_z_index(2)
            glow = Line(pos[u], pos[v], color=col, stroke_width=24,
                        stroke_opacity=0.25).set_z_index(1)
            guide = Line(pos[u], pos[v])      # invisible rail for the traveller
            length = float(np.linalg.norm(pos[v] - pos[u]))
            self.play(
                Create(seg, rate_func=linear),
                Create(glow, rate_func=linear),
                MoveAlongPath(traveler, guide, rate_func=linear),
                run_time=length * 0.35,
            )
            if v != "B":
                self.play(
                    node_mobs[v].animate.set_color(col).scale(1.5),
                    Flash(pos[v], color=col, flash_radius=0.7, line_length=0.2),
                    run_time=0.45,
                )
            else:
                self.play(
                    Indicate(node_mobs["B"], color=NEON_PINK, scale_factor=1.3),
                    Flash(pos["B"], color=NEON_PINK, flash_radius=0.9,
                          line_length=0.25),
                    FadeOut(traveler),
                    run_time=0.8,
                )

        # --- 4) DIM EVERYTHING ELSE, SHOW THE DISTANCE ---
        on_path = {key(u, v) for u, v in zip(path, path[1:])}
        on_nodes = set(path)
        dim = [road_mobs[k].animate.set_stroke(opacity=0.12)
               for k in road_mobs if k not in on_path]
        dim += [FadeOut(weight_tags[k]) for k in weight_tags if k not in on_path]
        dim += [node_mobs[n].animate.set_opacity(0.25)
                for n in node_mobs if n not in on_nodes]

        result = Text(f"Shortest distance: {total} km", color=NEON_YELLOW,
                      font_size=40, weight=BOLD)
        if result.width > 8:
            result.scale_to_fit_width(8)
        result.to_edge(DOWN, buff=1.6)

        self.play(*dim, FadeIn(result, shift=UP * 0.3), run_time=1.4)
        self.wait(3)