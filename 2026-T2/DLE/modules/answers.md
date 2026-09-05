## Question 1 - representation over features
Learning layered representations is the definition of deep learning, where a machine gets understanding from raw data, instead of we hand-coding the features.

The n-gram reading and A1 are connected because it asks us to build a sentiment classifier on twitter datasets using it

## Question 2 - why dpeth needs nonlinearity
without non-linear activation functions, stacking multiple linear layers mathematically collapses into a single equivalent layer, giving a deep network no more capacity than a 1-layer model

the xor example is the case that happens when no matter how we angle a straight line, it cant separate diagonal opposite corners

non-linearity bends space so that a straight cut can separate anything

backpropagation is when the network starts at the output mistake and uses the mathemtical chain rule to trace backward through every single neuron, calculating exactly how much each individual has contributed to the failure so they can fix their weight for the next time

## Question 3 - the NLP arc
classical n-gram rely on frequency counts and the markov assumption, failing on long context and out-of-vocabulary data due to the curse of dimensionality. the leap to modern deel learning in nlp was driven by two core techniques:

technique 1: word embeddings (word2vec, glove): low-dim vector representations where 'cat' and 'dog' are placed near each other in vector space, allowing models to share statistical strenght
technique 2: attention mechanism (transformers, bahdanau): soft-lookup  over all input token representations, eliminating the fix-window markov bottleneck, allowing models to focus on relevant context across arbitrary sequence lenghts

the paper from Zhao architecture fuses together pre-trained dense embeddings (glove) + classical n-gram features + deep convolutional networks through layers and k-max pooling to achieve more than 87% accuracy on sts-gold dataset, with major improvement over classical baseline models

## Question 4 - The five regularisation layers
we have l1, l2, dropout, early stopping and bagging 
l1 make all unimportant weights to zero while l2 shrink them closer to 0 smoothly