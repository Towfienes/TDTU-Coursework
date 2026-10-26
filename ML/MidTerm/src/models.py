"""NumPy implementations of the mean losses and full-batch GD in Lectures 8–9."""
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin


def sigmoid(z):
    z = np.asarray(z, dtype=float)
    result = np.empty_like(z)
    positive = z >= 0
    result[positive] = 1 / (1 + np.exp(-z[positive]))
    exponential = np.exp(z[~positive])
    result[~positive] = exponential / (1 + exponential)
    return result


def training_inputs(X, y, binary=False):
    X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
    if X.ndim != 2 or y.ndim != 1 or len(X) != len(y) or not len(y) or not X.shape[1]:
        raise ValueError('Expected a nonempty (n, d) matrix and an (n,) target.')
    if not np.isfinite(X).all() or not np.isfinite(y).all():
        raise ValueError('Inputs must be finite.')
    if binary and not np.isin(y, [0, 1]).all():
        raise ValueError('Binary targets must be 0 or 1.')
    return X, y


def linear_loss_gradient(X, y, w, b):
    error = X @ w + b - y
    return float(np.mean(error ** 2) / 2), X.T @ error / len(y), float(error.mean())


def logistic_loss_gradient(X, y, w, b):
    z = X @ w + b
    error = sigmoid(z) - y
    # logaddexp is the same cross entropy in logits, without log(0).
    loss = np.mean(np.logaddexp(0, z) - y * z)
    return float(loss), X.T @ error / len(y), float(error.mean())


class LinearRegressionGD:
    def __init__(self, learning_rate=0.3, epochs=4000, tolerance=1e-8):
        self.learning_rate, self.epochs, self.tolerance = learning_rate, epochs, tolerance

    def fit(self, X, y):
        X, y = training_inputs(X, y, binary=isinstance(self, LogisticRegressionGD))
        if not np.isfinite(self.learning_rate) or self.learning_rate <= 0:
            raise ValueError('learning_rate must be positive and finite.')
        if not isinstance(self.epochs, (int, np.integer)) or self.epochs < 1:
            raise ValueError('epochs must be a positive integer.')
        if not np.isfinite(self.tolerance) or self.tolerance < 0:
            raise ValueError('tolerance must be nonnegative and finite.')
        self.w_ = np.zeros(X.shape[1])
        self.b_ = 0.0
        self.loss_history_ = []
        for step in range(self.epochs + 1):
            loss, gradient_w, gradient_b = self.loss_gradient(X, y, self.w_, self.b_)
            if not np.isfinite(loss) or not np.isfinite(gradient_w).all() or not np.isfinite(gradient_b):
                raise FloatingPointError('GD diverged; check inputs and learning rate.')
            self.loss_history_.append(loss)
            self.gradient_norm_ = float(np.sqrt(gradient_w @ gradient_w + gradient_b ** 2))
            if step == self.epochs or self.gradient_norm_ <= self.tolerance:
                break
            self.w_ = self.w_ - self.learning_rate * gradient_w
            self.b_ = self.b_ - self.learning_rate * gradient_b
        self.n_iter_ = step
        return self

    loss_gradient = staticmethod(linear_loss_gradient)

    def decision_function(self, X):
        if not hasattr(self, 'w_'):
            raise ValueError('Fit the model before predicting.')
        X = np.asarray(X, dtype=float)
        if X.ndim != 2 or X.shape[1] != len(self.w_) or not np.isfinite(X).all():
            raise ValueError('Prediction inputs must be finite and match the fitted feature count.')
        return X @ self.w_ + self.b_

    def predict(self, X):
        return self.decision_function(X)


class LogisticRegressionGD(LinearRegressionGD):
    loss_gradient = staticmethod(logistic_loss_gradient)

    def predict_proba(self, X):
        p = sigmoid(self.decision_function(X))
        return np.column_stack((1 - p, p))

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)


class ScratchLogisticClassifier(ClassifierMixin, BaseEstimator):
    """Only the sklearn adapter; its optimization is LogisticRegressionGD above."""
    def __init__(self, learning_rate=0.5, epochs=4000):
        self.learning_rate, self.epochs = learning_rate, epochs

    def fit(self, X, y):
        X, y = training_inputs(X, y, binary=True)
        if len(np.unique(y)) != 2:
            raise ValueError('Both classes are required for this experiment.')
        self.classes_ = np.array([0, 1])
        self.n_features_in_ = X.shape[1]
        self.model_ = LogisticRegressionGD(self.learning_rate, self.epochs).fit(X, y)
        return self

    def predict(self, X):
        return self.model_.predict(X)

    def predict_proba(self, X):
        return self.model_.predict_proba(X)

    def decision_function(self, X):
        return self.model_.decision_function(X)
