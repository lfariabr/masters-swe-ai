# DLE602 - Module 2 - Discussion Forum Drafts

> Initial draft responses for the three Module 2 learning activities.
> Personalise before posting if you want a more casual or more academic tone.

---

## Activity 1 - Understanding Feedforward Networks

> Task: in no more than 100 words, describe the feedforward network in Goodfellow et al.'s XOR example.

**Draft post - 89 words:**

A feedforward network learns XOR by transforming two binary inputs through a hidden layer into a feature space where the output layer can separate the classes. In the original input space, XOR is not linearly separable, so a simple linear model fails. Goodfellow et al.'s example uses a hidden layer with nonlinear activation to create new representations of the four input cases. Once transformed, the output layer can map those hidden activations to the correct 0 or 1 result. The key idea is learned representation, not just more computation.

---

## Activity 2 - Interactive Knowledge Sharing: Backpropagation

> Task: share your understanding of backpropagation, explain its importance, and pose an interesting question to the class.

**Draft post:**

My current understanding is that backpropagation is the mechanism that makes multilayer neural networks trainable at scale. A forward pass sends input through the network and produces a prediction and loss. Backpropagation then works backward from that loss and uses the chain rule to calculate how sensitive the loss is to each weight and bias.

The important distinction from Goodfellow et al. (2016) is that backpropagation is not the whole learning algorithm. It computes gradients. An optimiser such as stochastic gradient descent then uses those gradients to update the parameters. So, if forward propagation is "make a prediction", backpropagation is "work out how each parameter contributed to the error", and optimisation is "change the parameters to reduce future error".

This matters because hidden layers do not have direct target labels. Backpropagation gives the model a way to assign learning signals to internal representations, even though we only observe the final output error.

Question for the class: when explaining backpropagation intuitively, do you think "blame assignment" is a useful analogy, or is "sensitivity analysis" more accurate? Where does either analogy break down when gradients vanish, explode, or get distorted by poor activation choices?

---

## Activity 3 - The Disadvantage of Neural Networks

> Task: list and explain disadvantages of neural networks in no more than 100 words.

**Draft post - 98 words:**

Neural networks are powerful, but they have real disadvantages. First, they often need large amounts of labelled data, which can be expensive or impossible to collect. Second, training can be computationally costly and sensitive to hyperparameters such as depth, learning rate, activation functions and regularisation. Third, they are less interpretable than simpler models, making it harder to explain why a prediction was made. Fourth, they can overfit training data if capacity is too high. Finally, universal approximation does not guarantee useful learning: a network may be able to represent a function but still fail to learn or generalise.

---

## Notes Before Posting

- Activity 1 and Activity 3 are already within the 100-word limits.
- Activity 2 is deliberately more conversational because the prompt asks for discussion and a question.
- Good classmate replies could compare "blame assignment" versus "sensitivity analysis", or add examples such as vanishing gradients with sigmoid/tanh activations.
