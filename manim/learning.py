from manim import *
import math

class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen

class ParabolaTest(Scene):
    def construct(self):
        ax = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            tips=False,
            axis_config={
                "include_numbers": True, 
                "color": BLACK,
                },
        )
        ax.get_x_axis().set_color(BLACK)
        ax.get_y_axis().set_color(BLACK)

        def parabola(x):
            return x**2
        
        title = Text("Basic Parabola", color=BLACK, font_size=40).to_edge(UL)

        parabola_graph = ax.plot(parabola, color=RED, x_range=[-2, 2])

        # Add everything to the scene
        self.add(ax, parabola_graph)
        self.add(title)

        # Animate the graph drawing
        self.play(Create(parabola_graph))
        for _ in range(6):
            self.play(Rotate(parabola_graph, angle=PI/3))
            self.wait(0.1)

        self.wait()

class PolyND(Scene):
    def construct(self):
        # TODO: Put stuff in helpers, clean up axis
        # dimensions and arrow scaling

        ax = self.get_axes((-20, 20), (-20, 20))

        func_x_range = (-4, 4)

        poly_func = lambda x: x**2 - 2
        poly_curve = ax.plot(poly_func, x_range=func_x_range, color=BLACK)

        arrows = VGroup()
        
        num_arrows = 7
        for x in np.linspace(func_x_range[0], func_x_range[1], num_arrows):
            y = poly_func(x)

            # Each arrow should have a max x shift that keeps it before the next arrow
            x_shift_max = (func_x_range[1] - func_x_range[0]) / num_arrows
            x_shift = (0 if y == 0 else y/abs(y)) * x_shift_max

            end_x_pre = x + x_shift
            end_y_pre = poly_func(x + x_shift)
            
            vec_shift = self.normalize_vec(np.array([end_x_pre - x, end_y_pre - y, 0]), to_length=1.5*math.sqrt(abs(y)))

            start_pos = ax.c2p(x, y, 0)
            end_pos = ax.c2p(x + vec_shift[0], y + vec_shift[1], 0)

            arrow = Arrow(start=start_pos, end=end_pos, color=RED)
            arrows.add(arrow)

        self.add(ax)
        self.play(Create(poly_curve))
        self.play(FadeOut(poly_curve), FadeIn(arrows))

        self.wait()

    def get_axes(self, x_range, y_range):
        ax = Axes(
        x_range=[x_range[0], x_range[1], 1],
        y_range=[y_range[0], y_range[1], 1],
        tips=False,
        axis_config={
            "color": BLACK,
            "include_ticks": False
            },
        )

        ax.get_x_axis().set_color(BLACK)
        ax.get_y_axis().set_color(BLACK)

        return ax
    
    def normalize_vec(self, vec, to_length=1):
        vec_len = np.linalg.norm(vec)
        if vec_len == 0:
            return vec
        
        scale_factor = to_length / vec_len
 
        return vec * scale_factor