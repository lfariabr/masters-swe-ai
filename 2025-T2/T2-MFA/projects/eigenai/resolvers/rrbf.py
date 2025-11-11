# resolvers/rrbf.py
import math
import random

class RRBFType1:
    def __init__(self, n_neurons=5, eta=0.01):
        """
        Initialize RRBF network parameters.
        n_neurons: number of hidden neurons
        eta: learning rate
        """
        self.n = n_neurons
        self.eta = eta

        # Initialize weights, centers (m_i), and spreads (delta_i)
        self.centers = [random.uniform(-1, 1) for _ in range(n_neurons)]
        self.sigmas  = [random.uniform(0.5, 1.5) for _ in range(n_neurons)]
        self.weights = [random.uniform(-0.5, 0.5) for _ in range(n_neurons)]
        self.prev_phi = [0.0] * n_neurons

    def phi(self, x, i):
        """
        Calculate neuron activation for RRBF Type 1:
        φ_i = e^(-(x - m_i)^2 / (2δ_i^2)) + e^(-(φ_(i−1) - m_i)^2 / (2δ_i^2))
        """
        m, d, prev = self.centers[i], self.sigmas[i], self.prev_phi[i]

        term1 = math.exp(-((x - m) ** 2) / (2 * d ** 2)) # How close is input to my center?
        term2 = math.exp(-((prev - m) ** 2) / (2 * d ** 2)) # How close was the previous activation to my center?
        self.prev_phi[i] = term1 + term2
        return self.prev_phi[i]

    def forward(self, x):
        """
        Forward pass: compute output y = Σ w_i * φ_i
        """
        phis = [self.phi(x, i) for i in range(self.n)]
        y = sum(w * p for w, p in zip(self.weights, phis))
        return y, phis

    def backward(self, x, y_true):
        """
        Backward pass: compute gradient for each parameter
        and update weights, centers, and spreads.
        """
        y_pred, phis = self.forward(x)
        error = y_true - y_pred
        grads = {'w': [], 'm': [], 'd': []}
        for i in range(self.n):
            m, d = self.centers[i], self.sigmas[i]
            p = phis[i]

            # Derivative components for each parameter
            dw = -error * p
            dm = -error * self.weights[i] * p * (x - m) / (d ** 2)
            dd = -error * self.weights[i] * p * ((x - m) ** 2) / (d ** 3)

            # Gradient descent updates
            grads['w'].append(dw)
            grads['m'].append(dm)
            grads['d'].append(dd)
            
            # Update parameters
            self.weights[i] -= self.eta * dw
            self.centers[i] -= self.eta * dm
            self.sigmas[i]  -= self.eta * dd
        return error, grads

    def train(self, X, Y, epochs=100):
        """
        Train the RRBF network over the input dataset (X, Y).
        Returns final average error.
        """
        for _ in range(epochs):
            total_err = 0
            for x, y in zip(X, Y):
                err, _ = self.backward(x, y)
                total_err += abs(err)
            total_err /= len(X)
        return total_err