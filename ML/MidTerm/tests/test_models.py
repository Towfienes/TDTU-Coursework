"""Finite differences, stable extremes, exact fitting and invalid input checks."""
import sys
from pathlib import Path
import unittest
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from models import (LinearRegressionGD, LogisticRegressionGD, sigmoid,
                    linear_loss_gradient, logistic_loss_gradient)


class ModelTests(unittest.TestCase):
    def test_both_gradients_against_finite_differences(self):
        rng = np.random.default_rng(12)
        X, w, b = rng.normal(size=(9, 3)), rng.normal(size=3), 0.4
        for objective, y in [(linear_loss_gradient, rng.normal(size=9)),
                             (logistic_loss_gradient, rng.integers(0, 2, 9))]:
            _, gw, gb = objective(X, y, w, b)
            theta, numeric, h = np.r_[w, b], [], 1e-6
            for j in range(4):
                delta = np.zeros(4); delta[j] = h
                high, low = theta + delta, theta - delta
                numeric.append((objective(X, y, high[:3], high[3])[0] -
                                objective(X, y, low[:3], low[3])[0]) / (2 * h))
            np.testing.assert_allclose(np.r_[gw, gb], numeric, rtol=1e-6, atol=1e-8)

    def test_exact_linear_relation(self):
        X = np.linspace(-1, 1, 31).reshape(-1, 1)
        model = LinearRegressionGD(0.3, 1000).fit(X, 2 * X[:, 0] + 3)
        np.testing.assert_allclose(model.predict(X), 2 * X[:, 0] + 3, atol=1e-6)
        self.assertTrue(np.all(np.diff(model.loss_history_) <= 1e-12))

    def test_binary_predictions_and_stability(self):
        X = np.array([[-2.], [-1.], [1.], [2.]])
        model = LogisticRegressionGD(0.5, 300).fit(X, [0, 0, 1, 1])
        np.testing.assert_array_equal(model.predict(X), [0, 0, 1, 1])
        np.testing.assert_allclose(model.predict_proba(X).sum(axis=1), 1)
        self.assertTrue(np.all(np.diff(model.loss_history_) <= 1e-12))
        np.testing.assert_array_equal(sigmoid([-1000, 1000]), [0, 1])
        loss, gw, gb = logistic_loss_gradient(np.array([[1.], [-1.]]),
                                            np.array([0., 1.]), np.array([1000.]), 0)
        self.assertTrue(np.isfinite([loss, *gw, gb]).all())
        self.assertEqual(loss, 1000)

    def test_invalid_inputs_and_predictions(self):
        for X, y in [([], []), ([[1]], [0, 1]), ([[np.nan]], [1]), ([[1]], [[1]])]:
            with self.assertRaises(ValueError): LinearRegressionGD().fit(X, y)
        with self.assertRaises(ValueError): LogisticRegressionGD().fit([[1], [2]], [0, 2])
        with self.assertRaises(ValueError): LinearRegressionGD(-1).fit([[1]], [0])
        with self.assertRaises(ValueError): LinearRegressionGD().predict([[1]])
        with self.assertRaises(ValueError): LinearRegressionGD().fit([[1]], [0]).predict([[1, 2]])

if __name__ == '__main__': unittest.main()
