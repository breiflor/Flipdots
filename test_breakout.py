import sys
import unittest.mock as mock

# Since we want to test game logic which relies on numpy arrays for Image,
# let's only mock cv2 and paho. Numpy shouldn't be mocked if we want to run logic
sys.modules['cv2'] = mock.MagicMock()
sys.modules['paho'] = mock.MagicMock()
sys.modules['paho.mqtt'] = mock.MagicMock()
sys.modules['paho.mqtt.client'] = mock.MagicMock()
sys.modules['PySimpleGUI'] = mock.MagicMock()

from Breakout import Breakout

class TestBreakout:
    def test_run(self):
        game = Breakout()
        assert game.state == "run"

        game.control("LEFT")
        game.control("RIGHT")

        for i in range(10):
            img, speed = game.getframe()
            assert speed == 0.4
            assert img is not None
        print("Test passed successfully.")

if __name__ == "__main__":
    t = TestBreakout()
    t.test_run()
