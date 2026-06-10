
> "Explain FNN to a beginner":
An FNN is a stack of layers of neurons where information flows forward only: it enters through the inputs, passes through hidden layers (which transform the data into more useful features), and exits the output layer as a prediction. Every connection has a weight; the network learns by adjusting those weights to make fewer mistakes. "Feedforward" = no loops, one-way signal.

> "Purpose of backpropagation":
Backprop is the blame-assignment mechanism. After the network guesses and gets it wrong, it uses the chain rule to compute how much each weight contributed to the error (the gradient), working backward from the output. Then the optimiser (SGD/Adam) uses those gradients to adjust the weights. Backprop computes the gradients; the optimiser updates them.

The 5 reflection questions (anchored to Review Pulse)

> "Why are neural networks useful?"
They learn the features themselves (no manual feature engineering), they're universal approximators, and they scale with data + compute. They shine on unstructured data: text, images, audio.

> "How do they differ from traditional ML?"
┌───────────────────────────────────────────────┬──────────────────────────────────┐
│   Traditional ML (LogReg, SVM, Naive Bayes)   │          Neural Network          │
├───────────────────────────────────────────────┼──────────────────────────────────┤
│ You engineer the features (e.g. TF-IDF in     │ The network learns the features  │
│ Review Pulse v1)                              │                                  │
├───────────────────────────────────────────────┼──────────────────────────────────┤
│ Strong on small/tabular data, interpretable   │ Strong on large/unstructured     │
│                                               │ data                             │
├───────────────────────────────────────────────┼──────────────────────────────────┤
│ Cheap, fast                                   │ Data-hungry + compute-hungry,    │
│                                               │ black-box                        │
└───────────────────────────────────────────────┴──────────────────────────────────┘

> "Why might a network need hidden layers?"
Without a hidden layer + nonly draw linear boundaries. XOR proves it: no straight line separates the 4 points, but one hidden layer "bends" the space so a linear output canwhere the intermediaterepresentations are born.

> "How does a network learn from its mistakes?"
The full loop: forward pass rror → backprop computes eachweight's blame → optimiser pushes the weights to lower the loss → repeat over thousands
of examples. Learning from mided by the loss.

