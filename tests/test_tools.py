"""
Tests para herramientas de dibujo
"""
import unittest
import cairo

from src.canvas.tools import PencilTool, BrushTool, LineTool
from src.core.image import PaintImage


class MockCanvas:
    """Mock del canvas para testing."""
    def __init__(self):
        self.image = PaintImage(100, 100)
        self.drawing_calls = []

    def queue_draw(self):
        self.drawing_calls.append("queue_draw")

    def commit_drawing(self):
        self.drawing_calls.append("commit_drawing")


class TestPencilTool(unittest.TestCase):
    def setUp(self):
        self.tool = PencilTool()
        self.canvas = MockCanvas()

    def test_pencil_draws_pixel(self):
        self.tool.on_press(self.canvas, 10, 10, 1)
        self.tool.on_release(self.canvas, 10, 10)

        # Verificar que se dibujó algo
        self.assertIn("commit_drawing", self.canvas.drawing_calls)

    def test_pencil_uses_primary_color(self):
        self.tool.set_colors((1, 0, 0), (1, 1, 1))  # Rojo
        self.tool.on_press(self.canvas, 5, 5, 1)
        self.tool.on_release(self.canvas, 5, 5)

        # El píxel debería ser rojo
        color = self.canvas.image.get_pixel_color(5, 5)
        self.assertAlmostEqual(color[0], 1.0, places=1)  # Rojo


class TestBrushTool(unittest.TestCase):
    def setUp(self):
        self.tool = BrushTool()
        self.canvas = MockCanvas()

    def test_brush_size(self):
        self.tool.set_brush_size(5)
        self.assertEqual(self.tool.brush_size, 5)

    def test_brush_draws_line(self):
        self.tool.on_press(self.canvas, 0, 0, 1)
        self.tool.on_motion(self.canvas, 10, 10)
        self.tool.on_release(self.canvas, 10, 10)

        self.assertIn("commit_drawing", self.canvas.drawing_calls)


if __name__ == "__main__":
    unittest.main()
