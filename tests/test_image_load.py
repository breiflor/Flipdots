import unittest
from unittest.mock import MagicMock, patch
import sys

# Mock numpy and cv2 before importing Image
mock_np = MagicMock()
mock_cv2 = MagicMock()
sys.modules["numpy"] = mock_np
sys.modules["cv2"] = mock_cv2

# Now we can import Image
from Image import Image

class TestImageLoad(unittest.TestCase):

    @patch('Image.Image.load_image')
    def test_load_png(self, mock_load_image):
        img = Image()
        img.load("test.png")
        mock_load_image.assert_called_once_with("test.png")

    @patch('Image.Image.load_txt')
    def test_load_txt(self, mock_load_txt):
        img = Image()
        img.load("test.txt")
        mock_load_txt.assert_called_once_with("test.txt")

    @patch('builtins.print')
    @patch('Image.Image.load_image')
    @patch('Image.Image.load_txt')
    def test_load_unsupported(self, mock_load_txt, mock_load_image, mock_print):
        img = Image()
        img.load("test.jpg")
        mock_load_image.assert_not_called()
        mock_load_txt.assert_not_called()
        # Verify that the correct error message was printed
        mock_print.assert_called_with("Wrong Type loading Image Data from test.jpg (only .png and .txt supported)")

    @patch('Image.Image.load')
    def test_init_with_path(self, mock_load):
        # Test that the constructor calls the load method when a path is provided
        img = Image(imagepath="test.png")
        mock_load.assert_called_once_with("test.png")

if __name__ == '__main__':
    unittest.main()
