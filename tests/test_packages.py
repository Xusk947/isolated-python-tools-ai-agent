import unittest


class TestPackages(unittest.TestCase):
    def test_imports_and_basic_usage(self) -> None:
        import numpy as np
        import pandas as pd

        import scipy
        import sympy
        import tabulate

        import sklearn
        from sklearn.linear_model import LinearRegression

        self.assertTrue(np.array([1, 2, 3]).sum() == 6)
        self.assertEqual(pd.DataFrame({"a": [1, 2]}).shape, (2, 1))

        x = sympy.Symbol("x")
        self.assertEqual(sympy.expand((x + 1) ** 2), x**2 + 2 * x + 1)

        self.assertIsNotNone(getattr(scipy, "__version__", None))
        self.assertIsNotNone(getattr(sklearn, "__version__", None))

        model = LinearRegression().fit([[0], [1], [2]], [0, 1, 2])
        self.assertAlmostEqual(float(model.coef_[0]), 1.0, places=6)

        table = tabulate.tabulate([["a", 1], ["b", 2]], headers=["k", "v"])
        self.assertIn("k", table)
        self.assertIn("v", table)
