from manim import *

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 14.22
config.frame_width = 8.0

class AStarAlgorithm(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        NEON_CYAN = "#00FFFF"
        NEON_PINK = "#FF00FF"
        NEON_GREEN = "#39FF14"
        NEON_YELLOW = "#FFFF00"
        
        title = Text("A* Search Algorithm", color=NEON_CYAN, font_size=36, weight=BOLD)
        self.play(Write(title), run_time=0.4)
        self.play(title.animate.to_corner(UL).scale(0.8), run_time=0.4)
        self.wait(0.2)
        
        def get_node(name, h_val, pos):
            c = Circle(radius=0.45, color=NEON_CYAN, stroke_width=4, fill_color=BLACK, fill_opacity=1)
            t_name = Text(name, color=NEON_CYAN, font_size=28, weight=BOLD)
            t_h = Text(f"h={h_val}", color=WHITE, font_size=18).next_to(c, DOWN, buff=0.1)
            return VGroup(c, t_name, t_h).move_to(pos)
            
        def get_edge(n1, n2):
            return Line(n1[0].get_center(), n2[0].get_center(), color=NEON_PINK, stroke_width=3).set_z_index(-1)
            
        def get_weight(val, edge, offset=UP*0.2):
            return Text(str(val), color=WHITE, font_size=24, weight=BOLD).move_to(edge.get_center() + offset)

        def pop_f_cost(node, g, h, direction):
            f_val = g + h
            t = Text(f"f={g}+{h}={f_val}", color=NEON_YELLOW, font_size=20, weight=BOLD)
            t.next_to(node[0], direction, buff=0.2)
            return t

        # Adjusted for vertical top-to-bottom flow
        node_S = get_node("S", 6, [0, 5.0, 0])
        node_A = get_node("A", 4, [-2.5, 2.0, 0])
        node_B = get_node("B", 3, [2.5, 2.0, 0])
        node_C = get_node("C", 2, [-1.0, -1.0, 0])
        node_G = get_node("G", 0, [0, -4.5, 0])
        
        edge_SA = get_edge(node_S, node_A)
        edge_SB = get_edge(node_S, node_B)
        edge_AC = get_edge(node_A, node_C)
        edge_BC = get_edge(node_B, node_C)
        edge_BG = get_edge(node_B, node_G)
        edge_CG = get_edge(node_C, node_G)
        
        w_SA = get_weight(2, edge_SA, UP*0.3 + LEFT*0.3)
        w_SB = get_weight(3, edge_SB, UP*0.3 + RIGHT*0.3)
        w_AC = get_weight(3, edge_AC, LEFT*0.3)
        w_BC = get_weight(1, edge_BC, UP*0.3 + LEFT*0.3)
        w_BG = get_weight(6, edge_BG, RIGHT*0.3)
        w_CG = get_weight(2, edge_CG, DOWN*0.3 + LEFT*0.3)
        
        self.play(
            FadeIn(node_S, node_A, node_B, node_C, node_G),
            Create(edge_SA), Create(edge_SB), Create(edge_AC), 
            Create(edge_BC), Create(edge_BG), Create(edge_CG),
            FadeIn(w_SA, w_SB, w_AC, w_BC, w_BG, w_CG),
            run_time=1.5
        )
        self.wait(1)
        
        def explore_node(node):
            self.play(
                node[0].animate.set_color(NEON_YELLOW).set_stroke(width=5),
                node[1].animate.set_color(NEON_YELLOW),
                run_time=0.5
            )
            
        def check_path(edge, target_node, g, h, direction):
            f_text = pop_f_cost(target_node, g, h, direction)
            self.play(
                edge.animate.set_color(NEON_YELLOW).set_stroke(width=5),
                FadeIn(f_text, shift=direction*0.5),
                run_time=0.6
            )
            return f_text

        explore_node(node_S)
        
        # Changed text directions slightly so they don't overlap in narrow screen
        f_A = check_path(edge_SA, node_A, g=2, h=4, direction=LEFT)
        f_B = check_path(edge_SB, node_B, g=3, h=3, direction=RIGHT)
        self.wait(0.5)
        
        explore_node(node_B)
        
        f_C_from_B = check_path(edge_BC, node_C, g=4, h=2, direction=RIGHT) 
        f_G_from_B = check_path(edge_BG, node_G, g=9, h=0, direction=RIGHT) 
        self.wait(0.5)
        
        explore_node(node_C)
        
        self.play(FadeOut(f_G_from_B))
        f_G_from_C = check_path(edge_CG, node_G, g=6, h=0, direction=LEFT)
        self.wait(0.5)
        
        self.play(
            node_S[0].animate.set_color(NEON_GREEN), node_S[1].animate.set_color(NEON_GREEN),
            node_B[0].animate.set_color(NEON_GREEN), node_B[1].animate.set_color(NEON_GREEN),
            node_C[0].animate.set_color(NEON_GREEN), node_C[1].animate.set_color(NEON_GREEN),
            node_G[0].animate.set_color(NEON_GREEN).set_stroke(width=6), node_G[1].animate.set_color(NEON_GREEN),
            
            edge_SB.animate.set_color(NEON_GREEN).set_stroke(width=7),
            edge_BC.animate.set_color(NEON_GREEN).set_stroke(width=7),
            edge_CG.animate.set_color(NEON_GREEN).set_stroke(width=7),
            
            edge_SA.animate.set_color(DARK_GRAY).set_stroke(width=2),
            edge_AC.animate.set_color(DARK_GRAY).set_stroke(width=2),
            edge_BG.animate.set_color(DARK_GRAY).set_stroke(width=2),
            node_A[0].animate.set_color(DARK_GRAY), node_A[1].animate.set_color(DARK_GRAY),
            
            run_time=1.5
        )
        self.wait(3)