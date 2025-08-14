import io

from matplotlib.backends.backend_agg import FigureCanvasAgg


class FigureCanvasDocutils(FigureCanvasAgg):
    def draw(self):
        super().draw()

        f = io.BytesIO()
        self.figure.savefig(f, format="svg")
        f.buffer