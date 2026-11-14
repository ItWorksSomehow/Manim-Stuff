from manim import *

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.22
config.frame_width = 8.0

class KruskalsAlgorithm(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        NEON_CYAN = "#00FFFF"
        NEON_PINK = "#FF00FF"
        NEON_GREEN = "#39FF14"
        NEON_RED = "#FF0033"
        
        title = Text("Kruskal's Algorithm", color=NEON_CYAN, font_size=36, weight=BOLD)
        self.play(Write(title), run_time=0.4)
        self.play(title.animate.to_corner(UL).scale(0.8), run_time=0.4)
        self.wait(0.2)
        
        def get_node(name, pos):
            c = Circle(radius=0.4, color=NEON_CYAN, stroke_width=4, fill_color=BLACK, fill_opacity=1)
            t = Text(name, color=NEON_CYAN, font_size=24, weight=BOLD)
            return VGroup(c, t).move_to(pos)
            
        def get_edge(n1, n2):
            return Line(n1.get_center(), n2.get_center(), color=NEON_PINK, stroke_width=3).set_z_index(-1)
            
        def get_weight(val, edge, offset=UP*0.2):
            return Text(str(val), color=WHITE, font_size=24, weight=BOLD).move_to(edge.get_center() + offset)

        # Condensed Graph for Vertical
        node_A = get_node("A", [-2.0, 3.0, 0])
        node_B = get_node("B", [0, 5.0, 0])
        node_C = get_node("C", [2.0, 3.0, 0])
        node_D = get_node("D", [-2.0, 0.0, 0])
        node_E = get_node("E", [2.0, 0.0, 0])
        
        edge_AB = get_edge(node_A, node_B)  # W: 1
        edge_CE = get_edge(node_C, node_E)  # W: 2
        edge_AD = get_edge(node_A, node_D)  # W: 3
        edge_BE = get_edge(node_B, node_E)  # W: 4
        edge_DE = get_edge(node_D, node_E)  # W: 5
        edge_BC = get_edge(node_B, node_C)  # W: 6
        
        w_AB = get_weight(1, edge_AB, UP*0.3 + LEFT*0.3)
        w_CE = get_weight(2, edge_CE, DOWN*0.3 + RIGHT*0.3)
        w_AD = get_weight(3, edge_AD, DOWN*0.3 + LEFT*0.3)
        w_BE = get_weight(4, edge_BE, LEFT*0.3 + UP*0.1)
        w_DE = get_weight(5, edge_DE, DOWN*0.3)
        w_BC = get_weight(6, edge_BC, UP*0.3 + RIGHT*0.3)
        
        self.play(
            FadeIn(node_A, node_B, node_C, node_D, node_E),
            Create(edge_AB), Create(edge_CE), Create(edge_AD), 
            Create(edge_BE), Create(edge_DE), Create(edge_BC),
            FadeIn(w_AB, w_CE, w_AD, w_BE, w_DE, w_BC),
            run_time=1.5
        )
        self.wait(1)
        
        def accept_edge(n1, n2, edge, weight):
            self.play(
                edge.animate.set_color(NEON_GREEN).set_stroke(width=6),
                weight.animate.set_color(NEON_GREEN),
                n1[0].animate.set_color(NEON_GREEN).set_stroke(width=5),
                n1[1].animate.set_color(NEON_GREEN),
                n2[0].animate.set_color(NEON_GREEN).set_stroke(width=5),
                n2[1].animate.set_color(NEON_GREEN),
                run_time=0.8
            )
            self.wait(0.4)

        def reject_edge(edge, weight):
            self.play(
                edge.animate.set_color(NEON_RED).set_stroke(width=6),
                weight.animate.set_color(NEON_RED),
                run_time=0.5
            )
            self.play(
                edge.animate.set_color(DARK_GRAY).set_stroke(width=2),
                weight.animate.set_color(DARK_GRAY),
                run_time=0.5
            )
            self.wait(0.2)

        accept_edge(node_A, node_B, edge_AB, w_AB)
        accept_edge(node_C, node_E, edge_CE, w_CE)
        accept_edge(node_A, node_D, edge_AD, w_AD)
        accept_edge(node_B, node_E, edge_BE, w_BE)
        reject_edge(edge_DE, w_DE)
        reject_edge(edge_BC, w_BC)
        
        self.wait(3)