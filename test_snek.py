import unittest

import snek

class MockHelper:
    def __init__(self):
        self.paints = []

    def setPixel(self, x, y, color):
        self.paints.append((x, y, color))

red = [200,0,0]

class TestSnakeInstance(unittest.TestCase):
    def test_creation(self):
        instance = snek.SnakeInstance(0, red)
        self.assertFalse(instance.autopilot)

    def test_die(self):
        instance = snek.SnakeInstance(0, red)
        self.assertTrue(instance.is_alive)
        instance.die()
        self.assertFalse(instance.is_alive)

    def test_paint(self):
        instance = snek.SnakeInstance(0, red)
        helper = MockHelper()
        instance.paint(helper)
        self.assertEqual(len(helper.paints), 3)

    def test_eat(self):
        instance = snek.SnakeInstance(0, red)
        self.assertEqual(instance.direction_x,0)
        self.assertEqual(instance.direction_y,1)
        mouse = snek.Mouse([instance])
        mouse.position = (0,2)
        instance.move(mouse)
        self.assertEqual(len(instance.coordinates),4)

    def test_autopilot(self):
        instance = snek.SnakeInstance(0, red)
        instance.autopilot = True
        mouse = snek.Mouse([instance])
        mouse.position = (3,3)
        instance.choose_automatically(mouse)
        self.assertEqual(instance.direction_x, 1)




    
