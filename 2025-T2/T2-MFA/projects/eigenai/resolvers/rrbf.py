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
        self._prev_neighbor = [0.0] * n_neurons  # φ_{i-1} captured during last forward pass

    def phi(self, x, i, prev_activation):
        """
        Calculate neuron activation for RRBF Type 1:
        φ_i = e^(-(x - m_i)^2 / (2δ_i^2)) + e^(-(φ_(i−1) - m_i)^2 / (2δ_i^2))
        """
        m, d = self.centers[i], self.sigmas[i]
        term1 = math.exp(-((x - m) ** 2) / (2 * d ** 2)) # How close is input to my center?
        term2 = math.exp(-((prev_activation - m) ** 2) / (2 * d ** 2)) # How close was the previous activation to my center?
        
        # CRITICAL: Store prev_activation for correct gradient computation in backward()
        self._prev_neighbor[i] = prev_activation
        
        self.prev_phi[i] = term1 + term2
        return self.prev_phi[i]

    def forward(self, x):
        """
        Forward pass: compute output y = Σ w_i * φ_i
        """
        phis = []
        prev = 0.0

        for i in range(self.n):
            phi_val = self.phi(x, i, prev)
            phis.append(phi_val)
            prev = phi_val
        
        y = sum(w * p for w, p in zip(self.weights, phis, strict=True))
        return y, phis

    def backward(self, x, y_true):
        """
        Backward pass: compute gradient for each parameter
        and update weights, centers, and spreads.
        
        CRITICAL FIX: Include BOTH Gaussian terms in m and σ gradients.
        φᵢ = term1(x, m, σ) + term2(prev, m, σ)
        ∴ ∂φᵢ/∂m = ∂term1/∂m + ∂term2/∂m
        """
        y_pred, phis = self.forward(x)
        error = y_true - y_pred
        grads = {'w': [], 'm': [], 'd': []}
        
        for i in range(self.n):
            m, d = self.centers[i], self.sigmas[i]
            prev_activation = self._prev_neighbor[i]  # Retrieved from forward pass
            p = phis[i]

            # Recompute the two Gaussian terms for gradient calculation
            term1 = math.exp(-((x - m) ** 2) / (2 * d ** 2))
            term2 = math.exp(-((prev_activation - m) ** 2) / (2 * d ** 2))

            # Derivative components for each parameter
            dw = -error * p
            
            # CORRECT: Include both terms in center gradient
            dm = -error * self.weights[i] * (
                term1 * (x - m) / (d ** 2) +
                term2 * (prev_activation - m) / (d ** 2)
            )
            
            # CORRECT: Include both terms in spread gradient
            dd = -error * self.weights[i] * (
                term1 * ((x - m) ** 2) / (d ** 3) +
                term2 * ((prev_activation - m) ** 2) / (d ** 3)
            )

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
            for x, y in zip(X, Y, strict=True):
                err, _ = self.backward(x, y)
                total_err += abs(err)
            total_err /= len(X)
        return total_err