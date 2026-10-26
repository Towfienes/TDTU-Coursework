import unittest
import numpy as np
from src.q1_models import LinearRegressionGD, LogisticRegressionGD, gradient_check


class TestScratch(unittest.TestCase):
    def test_gradients_multiple_shapes(self):
        for seed in range(4):
            rng = np.random.default_rng(seed)
            for n, d in [(1, 1), (7, 1), (9, 3), (5, 6)]:
                X = rng.normal(size=(n, d))
                for model, y in [
                    (LinearRegressionGD(), rng.normal(size=n)),
                    (LogisticRegressionGD(), rng.integers(0, 2, n)),
                ]:
                    with self.subTest(seed=seed, n=n, d=d, model=type(model).__name__):
                        self.assertLess(gradient_check(model, X, y), 1e-7)

    def test_one_step_and_formulas(self):
        X = np.array([[1.0, 2.0], [-1.0, 0.0], [0.0, 1.0]])
        for model, y in [
            (
                LinearRegressionGD(learning_rate=0.1, epochs=1),
                np.array([2.0, 0.0, 1.0]),
            ),
            (
                LogisticRegressionGD(learning_rate=0.1, epochs=1),
                np.array([1.0, 0.0, 1.0]),
            ),
        ]:
            loss, dw, db = model._loss_grad(X, y, np.zeros(2), 0.0)
            model.fit(X, y)
            np.testing.assert_allclose(model.weights_, -0.1 * dw)
            self.assertAlmostEqual(model.bias_, -0.1 * db)
            self.assertEqual(len(model.loss_history_), 2)
            self.assertAlmostEqual(model.loss_history_[0], loss)
            self.assertAlmostEqual(
                model.loss_history_[-1],
                model._loss_grad(X, y, model.weights_, model.bias_)[0],
            )
        linear = LinearRegressionGD()
        loss, dw, db = linear._loss_grad(X, np.zeros(3), np.array([2.0, -1.0]), 3.0)
        e = X @ np.array([2.0, -1.0]) + 3.0
        self.assertAlmostEqual(loss, (e @ e) / 6)
        np.testing.assert_allclose(dw, X.T @ e / 3)
        self.assertAlmostEqual(db, e.mean())

    def test_stability(self):
        model = LogisticRegressionGD()
        with np.errstate(over="raise", invalid="raise", divide="raise"):
            np.testing.assert_allclose(
                model.sigmoid(np.array([-1000.0, 0.0, 1000.0])), [0, 0.5, 1]
            )
            loss, dw, db = model._loss_grad(
                np.array([[-1000.0], [1000.0]]),
                np.array([1.0, 0.0]),
                np.array([1.0]),
                0.0,
            )
        self.assertEqual(loss, 1000.0)
        self.assertTrue(np.isfinite(dw).all() and np.isfinite(db))

    def test_invalid_inputs(self):
        for cls in [LinearRegressionGD, LogisticRegressionGD]:
            for X, y in [
                (np.empty((0, 2)), []),
                ([[1, 2]], [0, 1]),
                ([[np.nan]], [0]),
                ([[1]], [np.inf]),
                ([1, 2], [0, 1]),
            ]:
                with self.subTest(cls=cls, X=X):
                    with self.assertRaises(ValueError):
                        cls().fit(X, y)
            for lr, epochs in [(0, 1), (-1, 1), (np.nan, 1), (0.1, 0), (0.1, 1.5)]:
                with self.assertRaises(ValueError):
                    cls(learning_rate=lr, epochs=epochs).fit([[1.0]], [0.0])
        with self.assertRaises(ValueError):
            LogisticRegressionGD().fit([[1.0]], [2.0])

    def test_determinism_shapes_and_convergence(self):
        rng = np.random.default_rng(5)
        X = rng.normal(size=(80, 3))
        y = X @ [2.0, -1.0, 3.0] + 4.0
        a = LinearRegressionGD().fit(X, y)
        b = LinearRegressionGD().fit(X, y[:, None])
        np.testing.assert_array_equal(a.weights_, b.weights_)
        np.testing.assert_allclose(a.predict(X), y, atol=1e-8)
        self.assertEqual(a.predict(X).shape, (80,))
        log = LogisticRegressionGD().fit(X, (y > 4).astype(int))
        self.assertEqual(log.predict_proba(X).shape, (80,))
        self.assertTrue(np.all(np.diff(log.loss_history_) <= 1e-12))
        with self.assertRaises(ValueError):
            log.predict(X, threshold=2)
        with self.assertRaises(ValueError):
            log.predict(np.ones((2, 4)))


if __name__ == "__main__":
    unittest.main()
