"""
Tests para el área de dibujo
"""
import unittest

from src.canvas.drawing_area import DrawingArea
from src.core.image import PaintImage


class TestDrawingArea(unittest.TestCase):
    def setUp(self):
        self.area = DrawingArea()

    def test_default_tool_is_pencil(self):
        self.assertEqual(self.area.current_tool_name, "pencil")

    def test_tool_switching(self):
        self.area.set_tool("brush")
        self.assertEqual(self.area.current_tool_name, "brush")
        self.assertIsInstance(self.area.current_tool, type(self.area.tools["brush"]))

    def test_color_setting(self):
        self.area.set_primary_color((1, 0, 0))
        self.assertEqual(self.area.primary_color, (1, 0, 0))

    def test_new_image(self):
        self.area.new_image(200, 200)
        self.assertEqual(self.area.image.width, 200)
        self.assertEqual(self.area.image.height, 200)

    def test_zoom_operations(self):
        initial_zoom = self.area.zoom
        self.area.zoom_in()
        self.assertGreater(self.area.zoom, initial_zoom)

        self.area.zoom_reset()
        self.assertEqual(self.area.zoom, 1.0)


if __name__ == "__main__":
    unittest.main()
