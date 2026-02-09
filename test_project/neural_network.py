"""
Test Project: Simple Neural Network Classifier
A demonstration project for Academic Paper Writer
"""

import numpy as np

class NeuralNetwork:
    """A simple neural network for classification"""
    
    def __init__(self, input_size, hidden_size, output_size):
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.01
        self.b2 = np.zeros((1, output_size))
    
    def forward(self, X):
        """Forward propagation"""
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = np.maximum(0, self.z1)  # ReLU
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        exp_scores = np.exp(self.z2 - np.max(self.z2, axis=1, keepdims=True))
        self.probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
        return self.probs
    
    def backward(self, X, y, learning_rate=0.01):
        """Backward propagation with gradient descent"""
        m = X.shape[0]
        
        # Output layer gradient
        delta3 = self.probs
        delta3[range(m), y] -= 1
        delta3 /= m
        
        dW2 = np.dot(self.a1.T, delta3)
        db2 = np.sum(delta3, axis=0, keepdims=True)
        
        # Hidden layer gradient
        delta2 = np.dot(delta3, self.W2.T)
        delta2[self.a1 <= 0] = 0  # ReLU derivative
        
        dW1 = np.dot(X.T, delta2)
        db1 = np.sum(delta2, axis=0, keepdims=True)
        
        # Update weights
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
    
    def train(self, X, y, epochs=1000, learning_rate=0.01):
        """Train the network"""
        for epoch in range(epochs):
            self.forward(X)
            self.backward(X, y, learning_rate)
            
            if epoch % 100 == 0:
                loss = self.compute_loss(X, y)
                accuracy = self.compute_accuracy(X, y)
                print(f"Epoch {epoch}: Loss={loss:.4f}, Acc={accuracy:.4f}")
    
    def compute_loss(self, X, y):
        """Compute cross-entropy loss"""
        m = X.shape[0]
        logprobs = -np.log(self.probs[range(m), y] + 1e-8)
        return np.sum(logprobs) / m
    
    def compute_accuracy(self, X, y):
        """Compute classification accuracy"""
        probs = self.forward(X)
        predictions = np.argmax(probs, axis=1)
        return np.mean(predictions == y)


def main():
    """Main training loop"""
    # Generate synthetic data
    np.random.seed(42)
    X = np.random.randn(1000, 10)
    y = np.random.randint(0, 3, 1000)
    
    # Create and train network
    nn = NeuralNetwork(input_size=10, hidden_size=50, output_size=3)
    print("Training neural network...")
    nn.train(X, y, epochs=1000, learning_rate=0.01)
    
    # Evaluate
    final_acc = nn.compute_accuracy(X, y)
    print(f"\nFinal Accuracy: {final_acc:.4f}")


if __name__ == "__main__":
    main()
