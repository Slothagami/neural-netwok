from activations import MSE, MSE_prime
from layers import *

class Network:
    def __init__(self, /, loss=MSE, loss_prime=MSE_prime, lr=.1):
        self.layers = []

        self.lr = lr
        self.loss = loss
        self.loss_prime = loss_prime

    def add(self, layer): self.layers.append(layer)

    def config(self, layers, activation, activation_prime):
        for i, layer in enumerate(layers[1:]):
            self.add(FCLayer(layers[i], layer))
            self.add(ActivationLayer(activation, activation_prime))

    def predict(self, samples):
        # Predict a Batch of samples
        results = []
        for sample in samples:
            output = sample

            for layer in self.layers:
                output = layer.forward(output)

            results.append(output)

        return results

    def train(self, samples, labels, epochs):
        for epoch in range(epochs):
            disp_error = 0 

            for sample, label in zip(samples, labels):
                # Forward Propogation
                output = sample 
                for layer in self.layers:
                    output = layer.forward(output)

                # Display Error
                disp_error += self.loss(label, output)

                # Backprop
                error = self.loss_prime(label, output)
                for layer in reversed(self.layers):
                    error = layer.backprop(error, self.lr)

            # Calc Average Error
            disp_error /= len(samples)

            if epoch % 100 == 0:
                print(f"Epoch: {epoch}, Error: {disp_error}")
