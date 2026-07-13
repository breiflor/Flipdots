import sys
from unittest.mock import MagicMock

# Mock numpy and cv2 before they are imported by Image or Animation
sys.modules['numpy'] = MagicMock()
sys.modules['cv2'] = MagicMock()

import unittest
from Animation import Animation

class TestAnimation(unittest.TestCase):
    def test_init_resets_state(self):
        """Test that init() correctly sets loop and resets current_index."""
        anim = Animation()

        # Set to non-default values
        anim.loop = True
        anim.current_index = 5

        # Call init with loop=False
        anim.init(loop=False)

        self.assertFalse(anim.loop)
        self.assertEqual(anim.current_index, 0)

    def test_init_sets_loop_true(self):
        """Test that init(loop=True) correctly sets the loop attribute."""
        anim = Animation()

        # Ensure it starts at False (default)
        anim.loop = False
        anim.current_index = 10

        # Call init with loop=True
        anim.init(loop=True)

        self.assertTrue(anim.loop)
        self.assertEqual(anim.current_index, 0)

if __name__ == '__main__':
    unittest.main()
