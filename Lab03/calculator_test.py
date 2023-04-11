import unittest
from calculator import Calculator
from math import exp


class ApplicationTest(unittest.TestCase):
    calc = Calculator()

    def test_add(self):
        # Test valid inputs
        for i in range(5):
            x = i
            y = i + 1
            expected_output = x + y
            self.assertEqual(self.calc.add(x, y), expected_output)

        # Test invalid input
        self.assertRaises(TypeError, self.calc.add, 1, '2')

    def test_divide(self):
        # Test valid inputs
        for i in range(5):
            x = i
            y = i + 1
            expected_output = x / y
            self.assertEqual(self.calc.divide(x, y), expected_output)

        # Test invalid input
        self.assertRaises(ZeroDivisionError, self.calc.divide, 1, 0)

    def test_sqrt(self):
        # Test valid inputs
        for i in range(5):
            x = i ** 2
            expected_output = i
            self.assertEqual(self.calc.sqrt(x), expected_output)

        # Test invalid input
        self.assertRaises(ValueError, self.calc.sqrt, -1)

    def test_exp(self):
        # Test valid inputs
        for i in range(5):
            x = i
            expected_output = exp(x)
            self.assertEqual(self.calc.exp(x), expected_output)

        # Test invalid input
        self.assertRaises(TypeError, self.calc.exp, '2')


if __name__ == '__main__':
    unittest.main()
