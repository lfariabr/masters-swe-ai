# Python Natural Language Processing
> Jalaj Thanaki

## Chapter 9: Deep Learning for NLU and NLG Problems

We have seen the rule-based approach and various machine learning techniques to solve NLP tasks in the previous chapters. In this chapter, we will see the bleeding edge subset of machine learning technique called deep learning (DL). In the past four to five years, neural networks and deep learning techniques have been creating a lot of buzz in the artificial intelligence area because many tech giants use these cutting-edge techniques to solve real-life problems, and the results from these techniques are extremely impressive. Tech giants such as Google, Apple, Amazon, OpenAI, and so on spend a lot of time and effort to create innovative solutions for real-life problems. These efforts are mostly to develop artificial general intelligence and make the world a better place for human beings.

We will first understand the overall AI, in general, to give you a fair idea of why deep learning is creating a lot of buzz nowadays. We will cover the following topics in this chapter:

How NLU and NLG are different from each other
The basics of neural networks
Building NLP and NLG applications using various deep learning techniques
After understanding the basics of DL, we will touch on some of the most recent innovations happening in the deep learning field. So let's begin!

## An overview of artificial intelligence

In this section, we will see the various aspects of AI and how deep learning is related to AI. We will see the AI components, various stages of AI, and different types of AI; at the end of this section, we will discuss why deep learning is one of the most promising techniques in order to achieve AI.

### The basics of AI

When we talk about AI, we think about an intelligent machine, and this is the basic concept of AI. AI is an area of science that is constantly progressing in the direction of enabling human-level intelligence in machines. The basic idea behind AI is to enable intelligence in machines so that they can also perform some of the tasks performed only by humans. We are trying to enable human-level intelligence in machines using some cool algorithmic techniques; in this process, whatever kind of intelligence is acquired by the machines is artificially generated. Various algorithmic techniques that are used to generate AI for machines are mostly part of machine learning techniques. Before getting into the core machine learning and deep learning part, we will understand other facts related to AI.

AI is influenced by many branches; in Figure 9.1, we will see those branches that heavily influence artificial intelligence as a single branch:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/3eb3f19e-7bdd-44de-b847-6e7ee61f62f0.png
Figure 9.1: AI influence by other branches

### Stages of AI
There are three main stages for the AI system. We will see the following stages in detail:

Machine learning
Machine intelligence
Machine consciousness
Before getting into the details of each stage of AI, refer to Figure 9.4:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/c2e3f1cb-a353-48e5-9db6-a6d10b86c164.png
Figure 9.4: Stages of AI (Image credit: https://cdn-images-1.medium.com/max/1600/0*aefkt8m-V66Wf5-j.png)

We will begin from the bottom to the top, so we will understand the machine learning stage first, then machine intelligence, and finally machine consciousness.

### Types of artificial intelligence

There are three types of AI, as follows:

Artificial narrow intelligence
Artificial general intelligence
Artificial superintelligence

### Goals and applications of AI

This is the time and section where we need to understand the goals and applications for AI in general for various areas. These goals and applications are just to give you an idea about the current state of AI-enabled applications, but if you can think of some crazy but useful application in any area, then you should try to include it in this list. You should try to implement various types and stages of AI in that application.

Now let's see the areas where we want to integrate various stages of AI and make those applications AI-enabled:

Reasoning
Machine learning
Natural language processing
Robotics
Implementing general intelligence
Computer vision
Automated learning and scheduling
Speech analysis
You can refer to Figure 9.5, which shows many different areas and related applications:
https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/bb5e865d-edf1-43d8-8e2d-b739a33dfbed.png
Figure 9.5 : Various areas of AI and applications (Image credit: http://vincejeffs.com/)
Now let's see the applications from some of the areas in the preceding list.

## Comparing NLU and NLG
We have already seen the NLU and NLG definitions, details, and differences in Chapter 3, Understanding Structure of Sentences. In this section, we are comparing these two subareas of NLP in terms of an AI-enabled application.

### Natural language understanding
Earlier, we have seen that NLU is more about dealing with an understanding of the structure of the language, whether it is words, phrases, or sentences. NLU is more about applying various ML techniques on already generated NL. In NLU, we focus on syntax as well as semantics. We also try to solve the various types of ambiguities related to syntax and semantics. We have seen the lexical ambiguity, syntactic ambiguity, semantic ambiguity, and pragmatics ambiguity.

Now let's see where we can use AI that helps machines understand the language structure and meaning more accurately and efficiently. AI and ML techniques are not much behind to address these aspects of NL. To give an example, deep learning gives us an impressive result in machine translation. Now when we talk about solving syntactic ambiguity and semantic ambiguity, we can use deep learning. Suppose you have a NER tool that will use deep learning and Word2vec, then we can solve the syntactic ambiguity. This is just one application, but you can also improve parser results and POS taggers.

Now let's talk about pragmatics ambiguity, where we really need AGI as well as ASI. This ambiguity occurs when you try to understand the long distance context of a sentence with other previously written or spoken sentences, and it also depends on the speaker's intent of speaking or writing.

Let's see an example of pragmatics ambiguity. You and your friend are having a conversation, and your friend told you long ago that she had joined an NGO and would do some social activity for poor students. Now you ask her how was the social activity. In this case, you and your friend know about what social activities you are talking about. This is because as humans, our brain stores the information as well as knows when to fetch that information, how to interpret it, and what is the relevance of the fetched information to your current conversation that you are having with your friend. Both you and your friend can understand the context and relevance of each other's questions and answers, but machines don't have this kind of capability of understanding the context and speaker's intent.

This is what we expect from an intelligent machine. We want the machine to understand this kind of complex situation as well. Enabling this kind of capability of resolving pragmatics ambiguity is included in MSI. This will definitely be possible in future, but right now, we are at a stage where machines are trying to adopt AGI and using statistical techniques to understand semantics.

### Natural language generation
NLG is an area where we are trying to teach machines how to generate NL in a sensible manner. This, in itself, is a challenging AI task. Deep learning has really helped us perform this kind of challenging task. Let me give you an example. If you are using Google's new inbox, then you may notice that when you reply to any mail, you will get three most relevant replies in the form of sentences for the given mail. Google used millions of e-mails and made an NLG model that was trained using deep learning to generate or predict the most relevant reply for any given mail. You can refer to Figure 9.8:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/5d3f8aff-2f1b-416f-bbb4-014607e475c5.png
Figure 9.8: Google's new inbox smart reply
Apart from this application, there is another application: after seeing the images, the machine will provide a caption of a particular image. This is also an NLG application that uses deep learning. The task of generating language is less complex than the generation of NL, that is, coherence, and this is where we need AGI.

We have talked a lot about the term, deep learning, but how does it actually work and why is it so promising? This we will see in an upcoming section of this chapter. We will explain the coding part for NLU and NLG applications. We are also going to develop NLU and NLG applications from scratch. Before that, you must understand the concepts of ANN and deep learning. I will include mathematics in upcoming sections and try my best to keep it simple. Let's dive deep into the world of ANN and deep learning!

## A brief overview of deep learning

Machine learning is a sub-branch of AI and deep learning is a sub-branch of ML. Refer to Figure 9.9:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/335cc3a3-947b-4a28-b9b8-5fab7d792e9b.png
Figure 9.9: Deep learning as a sub-branch of ML
Deep learning uses ANN that is not just one or two layers, but many layers deep, called deep neural network (DNN). When we use DNN to solve a given problem by predicting a possible result for the same problem, it is called deep learning.

Deep learning can use labeled data or unlabeled data, so we can say that deep learning can be used in supervised techniques as well as unsupervised techniques. The main idea of using deep learning is that using DNN and a humongous amount of data, we want the machines to generalize the particular tasks and provide us with a result that we think only humans can generate. Deep learning includes a bunch of techniques and algorithms that can help us solve various problems in NLP such as machine translation, question answering system, summarization, and so on. Apart from NLP, you can find other areas of applications such as image recognition, speech recognition, object identification, handwritten digit recognition, face detection, and artificial face generation.

Deep learning seems promising to us in order to build AGI and ASI. You can see some of the applications where deep learning has been used, in Figure 9.10:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/40f17204-35b6-4839-a335-e0562411b318.png
Figure 9.10: Applications using deep learning (Image credit: http://www.fullai.org/)
This section gives you a brief overview about deep learning. We will see many aspects of deep learning in this chapter, but before that, I want to explain concepts that are related to deep learning and ANN. These concepts will help you understand the technicality of deep learning.

## Basics of neural networks
The concept of neural networks is one of the oldest techniques in ML. Neural network is derived from the human brain. In this section, we will see the human brain's components and then derive the ANN.

In order to understand ANN, we first need to understand the basic workflow of the human brain. You can refer to Figure 9.11:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/a2cf65ec-ebf8-470e-af8a-3d7c730d07c1.png
Figure 9.11: Neurons of human brain (Image credit: https://en.wikipedia.org/wiki/File:Blausen_0657_MultipolarNeuron.png)
The human brain consists of an estimated hundreds of billion nerve cells called neurons. Each neuron performs three jobs that are mentioned as follows:

Receiving a signal: It receives a set of signals from its dendrites
Deciding to pass the signal to the cell body: It integrates those signals together to decide whether or not the information should be passed on to the cell body
Sending the signal: If some of the signals pass a certain threshold, it sends these signals, called action potentials, onward via its axon to the next set of neurons
You can refer to Figure 9.12, which demonstrate components that are used to perform these three jobs in the biological neural network:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/0e260ec9-4f13-4237-afbc-fb74a9120076.png
Figure 9.12: Demonstrates the components that performs the three jobs
This is a very brief overview on how our brain learns and processes some decision. Now the question is: can we build an ANN that uses a non-biological substrate like silicon or other metal? We can build it, and then by providing a lot of computer power and data, we can solve the problems much faster as compared to humans.

ANN is a biologically inspired algorithm that learns to identify the pattern in the dataset.

We have seen a brief history of ANN earlier in this chapter, but now it's time to see ANN and its history in detail.

### The first computation model of the neuron
In mid-1943, researchers McCulloch-Pitts invented the first computation model of a neuron. Their model is fairly simple. The model has a neuron that receives binary inputs, sums them, and, if the sum exceeds a certain threshold value, then output is one, if not then output is zero. You can see the pictorial representation in Figure 9.13:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/fca196dd-1bd8-44ae-959a-c85e4ae2733c.png
Figure 9.13: McCulloch-Pitts computation model of neuron (Image credit for NN: http://wwwold.ece.utep.edu/research/webfuzzy/docs/kk-thesis/kk-thesis-html/node12.html)
It looks very simple, but as it was invented in the early days of AI, an invention of this kind of model was a really big deal.

### Perceptron

After a few years of the invention of the first computational model of neuron, a psychologist named Frank Rosenblatt found out that the McCulloch-Pitts model did not have the mechanism to learn from the input data. So he invented the neural network that was built on the idea of the first computational model of neuron. Frank Rosenblatt called this model the perceptron. It is also called a single-layer feedforward neural network. We call this model a feed forward neural network because, in this neural network, data flows in only one direction--the forward direction.

Now let's understand the working of the perceptron that has incorporated the idea of having weights on the given inputs. If you provide some training set of input output examples, it should learn a function from it by increasing and decreasing the weights continuously for each of the training examples, depending on what was the output of the given input example. These weight values are mathematically applied to the input such that after each iteration, the output prediction gets more accurate. This whole process is called training. Refer to Figure 9.14 to understand the schematic of Rosenblatt's perceptron:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/db870c10-9eaf-4c45-8c20-98c94b354709.png
Figure 9.14: Schematic of Rosenblatt's perceptron (Image credit for NN: http://sebastianraschka.com/Articles/2015_singlelayer_neurons.html)
We will see the ANN-related mathematical concepts such as gradient descent, activation function, and loss function in the next section. So get ready for some mathematics!

### Understanding mathematical concepts of ANN
Understanding mathematical concepts for ANN
This section is very important because ML, ANN, and DL use a bunch of mathematical concepts and we are going to see some of the most important ones. These concepts will really help you optimize your ML, ANN, and DL models. We will also see different types of activation functions and some tips about which activation function you should select. We are going to see the following mathematical concepts:

Gradient descent
Activation function
Loss function

## Implementation of ANN
In this section, we will implement our first ANN in Python using numpy as our dependency. During this implementation, you can relate how gradient descent, activation function, and loss function have been integrated into our code. Apart from this, we will see the concept of backpropagation.

We will see the implementation of a single-layer NN with backpropagation.

### Single-layer NN with backpropagation
Here, we will see the concept of backpropagation first, then we will start coding and I will explain things as we code.

### Exercise
Build a three-layer deep ANN using numpy as a dependency. (Hint: In a single-layer ANN, we used single layer, but here, you will use three layers. Backpropagation usually uses recursively taken derivatives, but in our one layer demo, there was no recursion. So you need to apply recursive derivatives.)

## Deep learning and deep neural networks
Now, just shift from ANN to DNN. In the upcoming section, we will see deep learning, architecture of DNN, and compare the approaches of DL for NLP and ML for NLP.

### Revisiting DL
We have seen some basic details about DL. Here, the purpose is just to recall things as a little refresher. ANN that is not two or three layers but many layers deep is called DNN. When we use many layers deep neural networks on lots of data using lots of computing power, we call this process deep learning.

Let's see the architecture of a deep neural network.

### The basic architecture of DNN
In this section, we will see the architecture of a DNN. The pictorial representation looks very simple and is defined with some cool mathematical formulas in the form of activation function, activation function for hidden layer, loss function, and so on. In Figure 9.41, you can see the basic architecture of a DNN:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/70fd1f89-7609-4bdc-86e2-a8786869b8be.png
Figure 9.41: Architecture of DNN (Image credit: https://cdn-images-1.medium.com/max/800/1*5egrX--WuyrLA7gBEXdg5A.png)

Now why are we using a multi-layer deep neural network, are there any certain reasons for this, and what is the significance of having many layers?

Let me explain why we are using multi-layer DNNs. Suppose, as a coder, you want to develop a system that identifies the images of fruits. Now you have some images of oranges and apples and you develop a logic such as I can identify images using the color of the fruits and you have also added shape as an identification parameter. You do some coding and are ready with the result. Now if someone tells you that we also have images that are black and white. Now you need to redo your coding work. Some varieties of images are too complex for you, as a human, to code, although your brain is very good at identifying the actual fruit name. So if you have such a complex problem and you don't know how to code or you know less details about the features or parameters that will be helpful for the machine to solve the problem, then you use a deep neural network. There are several reasons and those are mentioned as follows:

DNN has been derived using the abstract concept of how a human brain works.
Using DNN, we flip the approach of our coding. Initially, we provided features like color, shape, and so on to the machine to identify the fruit name in the given images, but with DNN and DL, we provide many examples to the machine and the machine will learn about the features by itself. After this, when we provide a new image of a fruit to the machine, it will predict the name of the fruit.
Now you really want to know how DNN can learn features by itself, so let's highlight some points as follows:

DNN uses a cascade of many layers of non-linear processing units that are used for feature extraction and transformation. Each successive layer of DNN uses the output from the previous layer as input, and this process is very similar to how the human brain transmits information from one neuron to the other. So we try to implement the same structure with the help of DNN.
In DL, features have been learned using multiple levels of representation with the help of DNNs. Higher levels of features or representation are derived from the lower level of features. So we can say that the concept of deriving features or representation in DNN is hierarchical. We learn something new using this lower level of ideas and we try to learn something extra. Our brain also uses and derives concepts in a hierarchical manner. This different level of features or representation is related to different levels of abstraction.
Multi-layers of DNN helps the machine to derive the hierarchical representation and this is the significance of having many layers as part of the architecture.
With the help of DNN and mathematical concepts, machines are capable to mimic some of the processes of the human brain.
DL can be applied to a supervised as well as unsupervised dataset to develop NLP applications such as machine translation, summarization, question answering system, essay generation, image caption tagging, and so on.
Now we will move to the next section where we will discuss the need of deep learning in NLP.

### Deep learning in NLP
The early era of NLP is based on the rule-based system, and for many applications, an early prototype is based on the rule-based system because we did not have huge amounts of data. Now, we are applying ML techniques to process natural language, using statistical and probability-based approaches where we are representing words in form of one-hot encoded format or co-occurrence matrix.

In this approach, we are getting mostly syntactic representations instead of semantic representations. When we are trying out lexical-based approaches such as bag of words, ngrams, and so on, we cannot differentiate certain context.

We hope that all these issues will be solved by DNN and DL because nowadays, we have huge amounts of data that we can use. We have developed good algorithms such as word2vec, GloVe, and so on in order to capture the semantic aspect of natural language. Apart from this, DNN and DL provide some cool capabilities that are listed as follows:

Expressibility: This capability expresses how well the machine can do approximation for a universal function
Trainability: This capability is very important for NLP applications and indicates how well and fast a DL system can learn about the given problem and start generating significant output
Generalizability: This indicates how well the machine can generalize the given task so that it can predict or generate an accurate result for unseen data
Apart from the preceding three capabilities, there are other capabilities that DL provides us with, such as interpretability, modularity, transferability, latency, adversarial stability, and security.

We know languages are complex things to deal with and sometimes we also don't know how to solve certain NLP problems. The reason behind this is that there are so many languages in the world that have their own syntactic structure and word usages and meanings that you can't express in other languages in the same manner. So we need some techniques that help us generalize the problem and give us good results. All these reasons and factors lead us in the direction of the usage of DNN and DL for NLP applications.

Now let's see the difference between classical NLP techniques and DL NLP techniques because that will connect our dots in terms of how DL can be more useful for us to solve NLP domain-related problems.

Difference between classical NLP and deep learning NLP techniques
In this section, we will compare the classical NLP techniques and DL techniques for NLP. So let's begin! Refer to Figure 9.42:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/32b50a1a-d3b9-4b84-be2e-f38cf4f102b9.png
Figure 9.42: Classical NLP approach (Image credit: https://s3.amazonaws.com/aylien-main/misc/blog/images/nlp-language-dependence-small.png)
Refer to Figure 9.43 for DL techniques:
https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/ae3bd2b6-0018-4e98-9396-9120c9f2d9b1.png
Figure 9.43: Deep learning approach for NLP (Image credit: https://s3.amazonaws.com/aylien-main/misc/blog/images/nlp-language-dependence-small.png)
In classical NLP techniques, we preprocessed the data in the early stages before generating features out of the data. In the next phase, we use hand-crafted features that are generated using NER tools, POS taggers, and parsers. We feed these features as input to the ML algorithm and train the model. We will check the accuracy, and if the accuracy is not good, we will optimize some of the parameters of the algorithm and try to generate a more accurate result. Depending on the NLP application, you can include the module that detects the language and then generates features.

Now let's see the deep learning techniques for an NLP application. In this approach, we do some basic preprocessing on the data that we have. Then we convert our text input data to a form of dense vectors. To generate the dense vectors, we will use word-embedding techniques such as word2vec, GloVe, doc2vec, and so on, and feed these dense vector embedding to the DNN. Here, we are not using hand-crafted features but different types of DNN as per the NLP application, such as for machine translation, we are using a variant of DNN called sequence-to-sequence model. For summarization, we are using another variant, that is, Long short-term memory units.(LSTMs). The multiple layers of DNNs generalize the goal and learn the steps to achieve the defined goal. In this process, the machine learns the hierarchical representation and gives us the result that we validate and tune the model as per the necessity.

If you really want to see the coding of different variants of DNNs, then use this GitHub link:
https://github.com/wagamamaz/tensorflow-tutorial
The next section is the most interesting part of this chapter. We are going to build two major applications: one is for NLU and one is for NLG. We are using TensorFlow and Keras as our main dependencies to code the example. We will understand a variant of DNN such as sequence-to-sequence and LSTM as we code them for better understanding.

Guess what we are going to build? We are going to build a machine translator as part of an NLP application and we will generate a summary from recipes. So let's jump to the coding part! I will give you some interesting exercises!


## Deep learning techniques and NLU
This section is coding-based and I will explain concepts as we go. The application that we are building here is one of the main applications in NLU.

There are so many languages spoken, written, or read by humans. Have you ever tried to learn a new language? If yes, then you know how difficult it is to acquire the skill of speaking a new language or writing a new language. Have you ever thought how Google translator is used in order to translate languages? If you are curious, then let's begin developing a machine translation application using a deep learning technique. Don't worry about questions like what type of DNN we will use because I'm explaining things to you in detail. So let's do some translation!

Note that DL takes a lot of computing power so we are not going to actually train the model, although I will give you details about the training code, we will use the trained model to replicate the results at our end. Just to give you an idea: Google uses 100 GPU for one week continuously to train the language translation model. So we get through the code, understand the concept, use an already trained model, and see the result.
If you want to use any specific version of TensorFlow, you can follow this command. If you want to install TensorFlow 0.12 version, you can install it with the following commands:

```bash
$ export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.12.1-cp27-none-linux_x86_64.whl
$ sudo pip install --upgrade $TF_BINARY_URL
```
  
If you want to use the version of TensorFlow then when you run the code please update you import statements. You can use the simple following command to install TensorFlow for CPU. I'm using GPU version only:

```bash
$ pip install tensorflow
```

If you want to run on GPU, you can use a cloud platform such as Google Cloud, AWS, or any other cloud platform or you need a GPU-enabled computer. To install TensorFlow for GPU, you can follow this link:

https://www.tensorflow.org/install/

### Machine translation

Machine translation (MT) is a widely known application in the NLU domain. Researchers and tech giants are experimenting a lot in order to make a single MT system that can translate any language. This MT system is called a universal machine translation system. So the long-term goal is that we want to build a single MT system that can translate English to German and the same MT system should also translate English to French. We are trying to make one system that can help us translate any language. Let's talk about the efforts and experiments done by researchers till date to build a universal machine translation system.

In 1954, the first machine translation demo had been given, which translated 250 words between Russian and English. This was a dictionary-based approach, and this approach used the mapping of words for source and target languages. Here, translation was done word by word and it wasn't able to capture syntactic information, which means that the accuracy was not good.

The next version was interlingual; it took the source language and generated an intermediary language to encode and represent a certain rule about the source language syntax, grammar, and so on and then generated a target language from the intermediary language. This approach was good compared to the first one but soon this approach was replaced by statistical machine translation (SMT) techniques.

IBM used this SMT approach; they broke the text into segments and then compared it to an aligned bilingual corpus. After this, using statistical techniques and probabilities, the most likely translation was chosen.

The most used SMT in the world is Google translation, and recently, Google published a paper stating that their machine translation system uses deep learning to generate the great result. We are using the TensorFlow library, which is an open source library for deep learning provided by Google. We will code to know how to do machine translation using deep learning.

We are using movies subtitles as our dataset. This dataset includes both German and English languages. We are building a model that will translate the German language into English and vice versa. You can download the data from http://opus.lingfil.uu.se/OpenSubtitles.php. Here, I'm using the pickle format of data. Using pickle, which is a Python dependency, we can serialize our dataset.

To begin with, we are using LSTMs network that is used to remember long term and short term dependencies. We are using TensorFlow's built-in data_utils class to preprocess the data. Then we need to define the vocabulary size on which we need to train the model. Here, our dataset has a small size of vocabulary so we are considering all the words in the dataset, but we define vocab (vocabulary) size such as 30,000 words, that is, a small set of training dataset. We will use the data_utils class to read the data from the data directory. This class gives us tokenized and formatted words from both languages. Then we define TensorFlow's placeholder that are encoders and decoders for inputs. These both will be integer tensors that represent the discrete values. They are embedded into dense representation. We will feed our vocabulary words to the encoder and the encoded representation that is learned to the decoder. You can see the code at this Github link: https://github.com/jalajthanaki/NLPython/tree/master/ch9/MT/Machine_Translation_GR_EN.

Now we can build our model. You can see the code snippets in Figure 9.44, Figure 9.45, and Figure 9.46:
https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/f4ef819d-cc0a-4548-8ff7-6133c93cc300.png

Figure 9.44: Code snippet for MT
https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/6ddc743f-d3f6-41be-a541-b9daef007fce.png

Figure 9.45: Code snippet for MT
https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/d9f73c8c-821a-4a91-a700-78a88fa3a8b9.png

Figure 9.46: Code snippet for MT
Now let's understand this encoder- and decoder-based system. Google recently published a paper where they discuss the system that they integrated into their translation system, that is, neural machine translation (NMT). It is an encoder decoder-based model with the new NMT architecture. Earlier, Google translated from language A to language English and then to language B. Now, Google translator can translate directly from one language to the other. Refer to Figure 9.47:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/b5fc7c9c-052a-41d1-862c-597580b4dce2.png
Figure 9.47: LSTM-based encoder and decoder architecture (Image credit: https://camo.githubusercontent.com/242210d7d0151cae91107ee63bff364a860db5dd/687474703a2f2f6936342e74696e797069632e636f6d2f333031333674652e706e67 )
Now with the existence of NMT, there is no need to memorize phrase-to-phrase translation. With the help of NMT, a translation system can encode semantics of the sentences. This encoding is generalized so that it can translate from Chinese to English, French to English as well as translate language pairs like Korean to Japanese, which has not been seen before.

Now can we use this simple LSTM-based encoder-decoder architecture? We will see some of the fundamental details of the architecture. Refer to Figure 9.48:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/1bfafce8-bdeb-437a-b0d3-988c3a855dcc.png
Figure 9.48: LSTM recurrent NN for translation (Image credit: https://smerity.com/articles/2016/google_nmt_arch.html)
We can use LSTM recurrent NN to encode a sentence of language A. The RNN splits a hidden state S, as shown in Figure 9.48. This S represents the vectorized content of the sentence. After that, we pass this vectorized form to the decoder that generates the translated sentence in language B, word by word. It's easy to understand this architecture, isn't it? However, this architecture has some drawbacks. This architecture has limited memory. The hidden state S of the LSTM is where we are trying to cram the whole sentence that we want to translate, but here S is usually a few hundred floating point numbers long. We need to fit our sentence into this fixed dimensionality and if we force our sentence to fit into this fixed dimensionality, then our network becomes more lossy, which means that we lose some information if we are forcefully fitting our sentence into a fixed size of dimensionality. We could increase the hidden size of LSTMs because their main purpose is to remember long-term dependencies, but if we increase the hidden size, then the training time increases exponentially. So, we should not use an architecture that takes a lot of time to converge.

We will introduce another architecture--attention-based encoder-decoder model. As humans, when we see a long sentence and we need to translate it, then we probably glance back at the source sentence a couple of times to make sure that we are capturing all the details. The human mind iteratively pays attention to the relevant parts of the source sentence. We want the neural network do the same thing for us by letting it store and refer to the previous output of the LST. This increases the storage of our model without changing the functionality of LSTMs. Refer to Figure 9.49:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/f9e91ecb-06ff-442c-83f8-49d575088208.png
Figure 9.49: Architecture of attention-based NMT (Image credit: https://heuritech.files.wordpress.com/2016/01/trad_attention1.png?w=470)
Once we have the LSTM output from the encoders stored, we can query each output asking how relevant it is to the current computation happening in the decoder. Each encoder output gets a relevancy score that we can convert to a probability score using the softmax activation function. Refer to Figure 9.50:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/c29a7b47-d0f5-4a0e-9bc4-95ece769d7b1.png
Figure 9.50: SoftMax function to generate the relevance score (Image credit: https://smerity.com/)
Then, we extract a context vector that is the weighted summation of the encoder's output depending on how relevant they are. Now let's get back to the code. To implement this attention-based functionality, we will use TensorFlow's built-in embedding attention sequence-to-sequence function. This function will take encoder and decoder inputs as arguments as well as some additional hyperparameters. This function is the same architecture that we have discussed. TensorFlow has some really great built-in models that we can use easily. Refer to Figure 9.51 for the code snippet:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/54e5ca7f-7f32-49fc-a610-f911509a9e7f.png
Figure 9.51: Code snippet for attention-based sequence-to-sequence model
Refer to Figure 9.52 for the output of the preceding code:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/2288a615-d3dc-4e07-9581-93bfbee1bbd5.png
Figure 9.52: Output for MT
You can also follow this link, https://www.tensorflow.org/tutorials/seq2seq, to run the MT example without making your customized code. This tutorial is an example of French to English and English to French translation system. This is a really easy way to run this example. I would recommend you to use this way because customized code is much complicated to begin with.

1. First, you need to download 2.4GB training giga-fren.tar dataset from this link: http://www.statmt.org/wmt10/training-giga-fren.tar.

2. Now you need to store this data in the data_dir directory and save your trained model time to time. For this, we need to create a checkpoint directory inside train_dir.

3. After that, you can execute the following command:
```bash
python translate.py  --data_dir [your_data_directory] --train_dir          [checkpoints_directory]  --en_vocab_size=40000 --fr_vocab_size=40000
```

4. If the preceding command takes a lot of memory of the GPU, then execute this command:
```bash
python translate.py  --data_dir [your_data_directory] --train_dir  [checkpoints_directory]  --size=256 --num_layers=2 -- steps_per_checkpoint=50
```  

5. Once your epoch reaches 340 K with batch size 64, you can use the model for translation before that also you can use it but accuracy will as follows:
```bash
python translate.py --decode  --data_dir [your_data_directory] --train_dir [checkpoints_directory]Reading model parameters from /tmp/translate.ckpt-340000>  Who is the president of the United States? Qui est le président des États-Unis ?
```

Our German to English (GR_EN) translation model gives us a fairly good result and we are doing only one round of training, but if we really want to get the same accuracy that Google has in their translation system, then we need to train this model for several weeks using high computational capability such as 100 GPUs for several weeks continuously running. Here, we are definitely not going to implement that model, but I will explain its working. So let's dive conceptually.

If the output doesn't have sufficient context for the encoded source sentence, then the model won't be able to give us a good translation result. In this case, we need to give the information about the future words so that the encoder output is determined by the words on the left and right. As humans, we use this kind of full context to understand the meaning of the sentence. This will happen on the machine level by including bidirectional encoders so that it contains two recurrent neural nets (RNN). One goes forward over the sentence and the other goes backward. So for each word, it concatenates the vector outputs that produce the vector with context of both sides. Refer to Figure 9.53:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/ffcd4d3b-eac4-456c-a130-7548bcfc79d7.png
Figure 9.53: Bidirectional RNN architecture for MT (Image credit: http://img.yantuwan.com/weiyuehao.php?http://mmbiz.qpic.cn/mmbiz_png/KmXPKA19gW81aVM2Gdgrxfsa0vR4YVib2wCIHNabCic1Hr144r4PAuSDMLNMHGgWz12GtibYdgF1jTvHtuniauHYSw/0?wx_fmt=png)
Google has included lots of layers to the models as well as encoders that have one bidirectional RNN layer and seven unidirection layers. The decoder has eight unidirectional RNN layers. If you add more layers, then the training time increases. Here, we are using only one bidirectional layer. If all layers are bidirectional, then the whole layer would have to finish their computation before other layer dependencies could start their computation. With the help of a unidirection layer, we can perform computation in parallel.

This is all about machine translation. We have generated the machine translation output but still there is more room for improvement. Using DL, we are going to build a single universal machine translation system.

Now let's begin our next part of coding that is based on NLG.

## Deep learning techniques and NLG
In this section, we are going build a very simple but intuitive application for NLG. We are going to generate a one-line summary from shot articles. We will see all the details about summarization in this section.

This application took a lot of training time so you can put your model to train on CPU and meanwhile, you can do some other task. If you don't have any other task, then let me give you one.

### Exercise
Try to figure out how you can generate a Wikipedia article by just providing some starting character sequences. Don't take me wrong! I'm serious! You seriously need to think on this. This is the dataset that you can use: https://einstein.ai/research/the-wikitext-long-term-dependency-language-modeling-dataset. Jump to the download section and download this dataset named Download WikiText-103 word level (181 MB).

(Hint: See this link, https://github.com/kumikokashii/lstm-text-generator.)

Don't worry ;after understanding the concepts of summarization, you can attempt this. So let's begin the summarization journey!

### Recipe summarizer and title generation
Before jumping into the code, I want to give you some brief background about summarization. Architecture and other technical parts will be understood as we code.

Semantics is a really big deal in NLP. As data increases in the density of the text, information also increases. Nowadays, people around you really expect that you say the most important thing effectively in a short amount of time.

Text summarization started in the 90s. The Canadian government built a system named forecast generator (FoG) that uses weather forecast data and generates a summary. That was the template-based approach where the machine just needed to fill in certain values. Let me give you an example, Saturday will be sunny with 10% chances of rain. The word sunny and 10% are actually generated by FoG.

The other areas are finance, medical, and so on. In the recent world, doctors find the summarization of a patient's medical history very useful and they can diagnose people efficiently and effectively.

There are two types of summary that are given as follows:

Extractive
Abstractive
Most summarization tools in the past were of the extractive type; they selected an existing set of words from the article to create a summary for the article. As humans, we do something more; that is, when we summarize, we build an internal semantic representation of what we have read. Using this internal semantic representation, we can summarize text. This kind of summarization is called abstractive summarization.

So let's build an abstractive summarization tool using Keras.

Keras is a high-level wrapper for TensorFlow and Theano. This example needs multiple GPUs for more than 12 hours. If you want to reproduce the result at your end, then it shall take a lot of computation power.
These are the steps for the coding part. Here, for the first time, we are using Python 3:

1. Clone the GitHub Repository:
https://github.com/jalajthanaki/recipe-summarization

2. Initialized submodules:
```bash
git submodule update --init -recursive
```

3. Go inside the folder:
```bash
python src/config.py
```
4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Set up directories:
```bash
python src/config.py
```

6. Scrape recipes from the web or use the existing one at this link:
```bash
wget -P recipe-box/data https://storage.googleapis.com/recipe-  box/recipes_raw.zip; unzip recipe-box/data/recipes_raw.zip -d recipe-box/data
```

7. Tokenize the data:
```bash
python src/tokenize_recipes.py
```

8. Initialize word embeddings with GloVe vectors:

8.1 Get the GloVe vectors trained model:
```bash
wget -P data http://nlp.stanford.edu/data/glove.6B.zip;
unzip data/glove.6B.zip -d data
```

8.2 Initialize embeddings:
```bash
python src/vocabulary-embedding.py
```

9. Train the model:
```bash
python src/train_seq2seq.py
```

10. Make predictions:
```bash
use src/predict.ipynb
```

Here, for vectorization, we are using GloVe because we want a global-level representation of the words for summarization, and we are using the sequence-to-sequence model (Seq2Seq model) to train our data. Seq2Seq is the same model that we discussed in the Machine translation section. See the code snippets in Figure 9.54, Figure 9.55, and Figure 9.56, and after training, you can see the output in Figure 9.57:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/774350b6-b0c1-4852-8511-ce23d7b33e67.png
Figure 9.54: Tokenization code snippet
Refer to the following figure for vocab building using GloVe:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/3e784e55-84ac-4929-8f20-b64e775d0ada.png
Figure 9.55: Vocab building using GloVe
Refer to the following figure to train the model:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/964a4407-12e0-4da8-9f5f-fe3571ea7c66.png
Figure 9.56: Training of the model
Examples are given in the following figure:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/84094480-18c5-45b1-8d25-32a62a772ce9.png
Figure 9.57: Prediction result of the model
I know that the summarization example will take a lot of computational power and maybe there will be a situation where your local machine does not have enough memory (RAM) to run this code. In that case, don't worry; there are various cloud options available that you can use. You can use Google Cloud, Amazon Web Services (AWS), or any other.

Now you have enough idea about the NLU and NLG applications. I have also put one more application related to the NLG domain at this GitHub Link:
https://github.com/tensorflow/models/tree/master/im2txt

This application generates captions for images; this is a kind of combined application of computer vision and NLG. Necessary details are on GitHub so check out this example as well.

In the next section, we will see the gradient descent-based optimization strategy. TensorFlow provides us with some variants of the gradient descent algorithm. Once we have an idea of how all these variants work and what are the drawbacks and advantages of each of them, then it will be easy for us to choose the best option for the optimization of our DL algorithm. So let's understand the gradient descent-based optimization.

## Gradient descent-based optimization

In this section, we will discuss gradient descent-based optimization options that are provided by TensorFlow. Initially, it will not be clear which optimization option you should use, but as and when you know the actual logic of the DL algorithm, it will became much clearer to you.

We use a gradient descent-based approach to develop an intelligent system. Using this algorithm, the machine can learn how to identify patterns from the data. Here, our end goal is to obtain the local minimum and the objective function is the final prediction that the machine will make or result that is generated by the machine. In the gradient descent-based algorithm, we are not concentrating on how to achieve the best final goal for our objective function in the first step, but we will iteratively or repeatedly take small steps and select the intermediate best option that leads us to achieve the final best option, that is, our local minima. This kind of educated guess and check method works well to obtain local minima. When the DL algorithm obtains local minima, the algorithm can generate the best result. We have already seen the basic gradient descent algorithm. If you face overfitting and underfitting situations, you can optimize the algorithm using different types of gradient descent. There are various flavors of gradient descent that can help us in order to generate the ideal local minima, control the variance of the algorithm, update our parameters, and lead us to converge our ML or DL algorithm. Let's take an example. If you have function Y = X2, then the partial derivative of the given function is 2X. When we randomly guess the stating value and we start with value X = 3, then Y = 2(3) =6 and to obtain local minima, we need to take a step in the negative direction--so Y = -6. After the first iteration, if you guess the value X = 2.3, then Y = 2(2.3) = 4.6 and we need to move in the negative direction again--Y = -4.6--because we get a positive value. If we get a negative value, then we move in the positive direction. After certain iterations, the value of Y is very near zero and that is our local minima. Now let's start with basic gradient descent. Let's start exploring varieties of gradient descent.

Basic gradient descent

In basic gradient descent, we calculate the gradient of loss function with regards to the parameters present in the entire training dataset, and we need to calculate gradient for the entire dataset to perform a single update. For a single update, we need to consider the whole training dataset as well as all parameters so it is very slow. You can see the equation in Figure 9.58:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/7b8ef16a-da38-4822-862e-66d42a50b2a2.png
Figure 9.58: Equation for gradient descent (Image credit: http://sebastianruder.com/optimizing-gradient-descent/index.html#challenges)
You can find the sample logic code for understanding purposes in Figure 9.59:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/4224bd92-3687-45ac-b1be-64c67d519676.png
Figure 9.59: Sample code for gradient descent (Image credit: http://sebastianruder.com/optimizing-gradient-descent/index.html#challenges)
As this technique is slow, we will introduce a new technique called Stochastic Gradient Descent.

Stochastic gradient descent

In this technique, we update the parameters for each training example and label so we just need to add a loop for our training dataset and this method updates the parameters faster compared to basic gradient descent. You can see the equation in Figure 9.60:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/9ea66aa6-aeaf-46f8-aa38-cd42d767e815.png
Figure 9.60: Equation for stochastic gradient descent (Image credit: http://sebastianruder.com/optimizing-gradient-descent/index.html#challenges)
You can find the sample logic code for understanding purposes in Figure 9.61:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/4983e3bb-2285-4c0b-880b-f9e100da46a0.png
Figure 9.61: Sample code for stochastic gradient descent (Image credit: http://sebastianruder.com/optimizing-gradient-descent/index.html#challenges)
This method also has some issues. This method makes convergence complicated and sometimes updating the parameters is too fast. The algorithm can overshoot the local minima and keep running. To avoid this problem, another method is introduced called Mini-Batch Gradient Descent.

Mini-batch gradient descent

In this method, we will take the best part from both basic gradient descent and stochastic gradient descent. We will take a subset of the training dataset as a batch and update the parameters from them. This type of gradient descent is used for basic types of ANNs.

You can see the equation in Figure 9.62:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/ea637bf4-9d39-42be-b88c-db54c3eb1513.png
Figure 9.62: Equation for mini-batch gradient descent (Image credit: http://sebastianruder.com/optimizing-gradient-descent/index.html#challenges)
You can find the sample logic code for understanding purposes in Figure 9.63:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/23b21169-fb95-4586-88f0-4e59625d1649.png
Figure 9.63: Sample code for mini-batch gradient descent (Image credit: http://sebastianruder.com/optimizing-gradient-descent/index.html#challenges)
If we have a high-dimensional dataset, then we can use some other gradient descent method; let's begin with momentum.

Momentum

If all the possible parameters' values surface curves much more steeply in one dimension than in another, then in this kind of case, this are very common around local optima. In these scenarios, SGD oscillates across the slopes. So to solve this oscillation issue, we will use the momentum method. You can see the equation in Figure 9.64:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/d0de2757-8da0-4dd8-9622-31f965891b99.png
Figure 9.64: Equation for momentum (Image credit: http://sebastianruder.com/optimizing-gradient-descent/index.html#challenges)
If you see the equation, we are adding a fraction of the direction of the gradient from the previous time step to the current step, and we amplify the parameter update in the right direction that speeds up our convergence and reduces the oscillation. So here, the concept of momentum is similar to the concept of momentum in physics. This variant doesn't slow down when local minima is obtained because at that time, the momentum is high. In this situation, our algorithm can miss the local minima entirely and this problem can be solved by Nesterov accelerated gradient.

Nesterov accelerated gradient

This method was invented by Yurii Nesterov. He was trying to solve the issue that occurred in the momentum technique. He has published a paper that you can see at this link:

You can see the equation in Figure 9.65:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/301534eb-f693-43e5-bf8f-3b1607dd3f3d.png
Figure 9.65: Equation for Nesterov accelerated gradient (Image credit: http://sebastianruder.com/optimizing-gradient-descent/index.html#challenges)
As you can see, we are doing the same calculation that we have done for momentum but we have changed the order of calculation. In momentum, we compute the gradient make jump in that direction amplified by the momentum, whereas in the Nesterov accelerated gradient method, we first make a jump based on the previous momentum then calculate gradient and after that we add a correction and generate the final update for our parameter. This helps us provide parameter values more dynamically.

Adagrad

Adagrad is stands for adaptive gradient. This method allows the learning rate to adapt based on the parameters. This algorithm provides a big update for infrequent parameters and a small update for frequent parameters. You can see the equation in Figure 9.66:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/666299f3-4f5a-46af-86f7-2deef8e1188f.png
Figure 9.66: Equation for Adagrad (Image credit: http://sebastianruder.com/optimizing-gradient-descent/index.html#challenges)
This method provides a different learning rate for every parameter at the given timestamp based on the past gradient computed for that parameter. Here, we don't need to manually tune our learning rate although it has a limitation. As per the equation, the learning rate is always decreasing as the accumulation of the squared gradients placed in the denominator is always positive, and as the denominator grows, the whole term will decrease. Sometimes, the learning rate becomes so small that the ML-model stops learning. To solve this problem. the method called Adadelta has come into the picture.

Adadelta

Adadelta is an extension of Adagrad. In Adagrad, we constantly add the square root to the sum causing the learning rate to decrease. Instead of summing all the past square roots, we restrict the window to the accumulated past gradient to a fixed size.

You can see the equation in Figure 9.67:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/72c1a17c-1bd5-4af0-93d7-c52406dbcd26.png
Figure 9.67: Equation for Adadelta (Image credit: http://sebastianruder.com/optimizing-gradient-descent/index.html#challenges)
As you can see in the equation, we will use the sum of gradient as a decaying average of all past squared gradients. Here, the running average E[g2]t at a given timestamp is dependent on the previous average and the current gradient.

After seeing all the optimization techniques, you know how we can calculate the individual learning rate for each parameter, how we can calculate the momentum, and how we can prevent the decaying learning rate. Still, there is room for improvement by applying some adaptive momentum and that leads us to our final optimization method called Adam.

Adam

Adam stands for adaptive momentum estimation. As we are calculating the learning rate for each parameter, we can also store the momentum changes for each of them separately.

You can see the equation in Figure 9.68:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/ffc6ace5-3525-4373-95cf-9de59ab2ca74.png
Figure 9.68: Mean and variance for Adam (Image credit: http://sebastianruder.com/optimizing-gradient-descent/index.html#challenges)
First, we will be calculating the mean of the gradient, then we are going to calculate the uncentered variance of the gradient, and use these values to update the parameters. Just like an Adadelta. You can see the equation of Adam in Figure 9.69:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781787121423/files/assets/2fe35988-9e9c-466d-9bd0-4bb0368661d8.png
Figure 9.69: Equation for Adam (Image credit: http://sebastianruder.com/optimizing-gradient-descent/index.html#challenges)
So now you want to know which method we should use; according to me, Adam is the best overall choice because it outperforms the other methods. You can also use Adadelta and Adagrad. If your data is sparse, then you should not use SGD, momentum, or Nesterov.

## Artificial intelligence versus human intelligence
From the last one year, you may have heard this kind of question. In the AI world, these kinds of questions have become common. People have created a hype that AI will make humanity vanish and machines will take away all the powers from us. Now let me tell you, this is not the truth. These kinds of threats sound like science-fiction stories. According to me, AI is in its high pace development phase but its purpose is to complement humanity and make human life easier. We are still figuring out some of the complex and unknown truths of this universe that can help us provide more insight on how we can build AI-enabled systems. So AI is purely going to help us. AI will amaze our lives for sure but it is not going to be saturated with its inventions soon. So enjoy this AI phase and contribute to the AI ecosystem in a positive manner.

People have concerns that AI will take away our jobs. It will not take away your job. It will make your job easier. If you are a doctor and want to give your final words on some cancer report, AI will help you. In the Information Technology (IT) industry, there's a concern that AI will replace the coders. If you believe that very soon researchers and tech companies will be able to build machines that are more powerful than humans and that the AI shift will happen soon and machines will take away our jobs, then it is better for you to acquire ML, DL, and AI related skill sets to have jobs, and perhaps you are the last person on this planet who has some job to do! We assume that AI would take away some jobs, but this AI ecosystem will also create so many new jobs. So don't worry! This discussion can be ongoing but I want to really give you guys some time window to think on this.

## Summary
Congratulations guys! We have made it to the last chapter! I really appreciate your efforts. In this chapter, you have learned a lot of things such as artificial intelligence aspects that help you understand why deep learning is the buzzword nowadays. We have seen the concept of ANNs. We have seen concepts such as gradient descent, various activation functions, and loss functions. We have seen the architecture of DNN and the DL life cycle. We have also touched on the basics of the sequence-to-sequence model and developed applications such as machine translation, title generation, and summarization. We have also seen the gradient descent-based optimization techniques.

The next sections are Appendices A to C, that will provide you with an overview about frameworks such as hadoop, spark, and so on. You can also see the installation guide for these frameworks as well as other tools and libraries. Apart from this, you can find cheatsheets for many Python libraries that are very handy if you are new to Python. There are some tips from my side if you really want to improve your data science as well as NLP skills. I have also provided Gitter links in the appendices that you can use to connect with me in case you have any questions.