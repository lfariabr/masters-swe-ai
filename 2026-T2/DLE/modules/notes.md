# Deep Learning (DLE602) Notes
## Dr. Robin Cyriac

## Module 1 - Introduction to Deep Learning

### TLDR
- **Deep learning** is machine learning that learns layered representations from data instead of relying only on hand-built features.
- **Representation quality** strongly affects model performance; deep networks build higher-level concepts from simpler ones.
- **N-gram language models** estimate word sequence probabilities using local context, usually unigram, bigram, or trigram histories.
- **Assessment 1 link:** the N-gram reading is the technical foundation for the Twitter sentiment analysis classifier.

### Introduction
Welcome to the world of deep learning.

Deep learning is a subset of machine learning (ML) and ML is a subset of artificial intelligence (AI). AI is a technique that enables a machine to mimic human behaviour. Conversely, ML is a technique that achieves AI via algorithms that have been trained with data and deep learning is a type of ML that is inspired by the structure of the human brain.

Ever wondered how Google translates the content of an entire webpage into a different language in a matter of seconds, how self-driving cars, which once seemed like something from a science fiction novel, have now become a reality or how customer support bots are able to help millions of customers in real time? All of these are products of deep learning and these products are only the ‘firsts’ in their areas.

Read on to discover the basics of deep learning and how deep learning will meet the challenges of the future.

### Resources

#### 1. Introduction to Deep Learning
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). Deep learning. Cambridge, MA: MIT Press. Retrieved from https://www.deeplearningbook.org/

*Resource Overview:*

    This book contains an introduction to a broad range of topics in deep learning. Specifically, it covers the mathematical and conceptual background to deep learning, the deep learning techniques used in industry and research perspectives. This book will be used throughout all the DLE602 modules.

    Please read Chapter 1 for this Module. Pay special attention to the ‘Introduction’ and Section 1.2. These sections will help you ease into the world of deep learning and will introduce you to neural networks with examples and explanations.

> *Status: ✅ Read + Reviewed — see [module01_notes.md](module-01-intro-to-dl/module01_notes.md)*

#### 2. Speech and Language Processing
- Jurafsky, D. & Martin, J. H. (2008) Speech and language processing. Boston, MA: Pearson. Retrieved from: https://web.stanford.edu/~jurafsky/slp3/

*Resource Overview:*

    This book covers techniques that traditionally are taught in different machine learning and deep learning courses to describe a unified vision of speech and language processing.

    Please read Chapter 3 for this Module. Pay special attention to the ‘Introduction;’, Section 3.1 and Section 3.2. You may choose to read the rest of the chapter if you like. These sections will introduce you to the N-Gram language model. It is one of the most prominent language processing models in both ML and deep learning. Note: You need to have a good understanding of this model for Assessment 1.

> *Status: ✅ Read + Reviewed — see [module01_notes.md](module-01-intro-to-dl/module01_notes.md)*

#### 3. Introduction to Deep Learning with Examples
- Kelleher, J. D. (2019). Deep learning. Cambridge, MA: MIT Press. Retrieved from https://ebookcentral-proquest-com.torrens.idm.oclc.org/lib/think/detail.action?docID=5855529

*Resource Overview:*

    This book contains an introduction to the AI technology that enables computer vision, speech recognition, machine translation and driverless cars.

    Please read Chapter 1 for this Module. Pay special attention to the applications that are discussed as examples in the first chapter.

> *Status: 🔥 WIP — needs manual access to ProQuest eBook*

#### 4. Applied Machine Learning: Foundations for Deep Learning
- Jedamski, D. (2019). Applied machine learning: Foundations [Video file]. Retrieved from https://www.linkedin.com/learning/applied-machine-learning-foundations/leveraging-machine-learning

*Resource Overview:*

    This video course talks about all things applied ML. If you are new to ML and deep learning, it is worth completing this course.

    However, for this Module, you can simply listen to the ‘Introduction’ and ‘1. Machine Learning Basic’ sections. These sections will help you ease into the world of deep learning and will give you another point of view about the relationship between AI, ML and deep learning.

> *Status: 🔥 WIP — needs manual listen/authenticated LinkedIn access*

### Learning Activities

#### 1. Learning Activity: Introduce Yourself
Write a short paragraph about yourself in the ‘Introduce Yourself’ discussion forum. The ‘Introduce Yourself’ discussion forum is a great way for you to get to know other students and become part of the university community. It will help you to join with others to make study groups and support each other outside of class time. It also has the potential to help you to develop supportive friendships throughout the course.

Recommendation: Highlight your skill levels in relation to deep learning, programming (python), detail any work experience that you may have in this field and state how you plan to use the knowledge you acquire in this unit in your future professional life. Learn about others from their short bios and start thinking of potential group members—you may identify some appropriate teammates for this session!

> *Status: ✅ Done*

#### 2. Discussion Forum Post
Using the deep learning resources you have read in this Module, please identify at least two projects or research ideas that you would like to pursue as part of this unit.

Describe each of these in one clear problem statement and write associated challenges or research questions for each statement. In this activity, you should demonstrate your ability to identify a research gap, propose a project to address the gap and communicate details in short written form. It should also help you to connect with likeminded people in the class.

Access Module 1: Learning Activity 2 - Discussion Forum

Please read other students’ posts and provide feedback on their ideas. Most importantly, identify other students who are planning to work on projects similar to yours.

> *Status: ✅ Done*

---

## Module 2 - Deep Learning: Feedforward Neural Network and Backpropagation

### TLDR
- **Feedforward neural networks** approximate functions by passing inputs forward through hidden layers to an output layer.
- **Hidden layers and nonlinear activations** let MLPs learn representations that solve problems linear models cannot, such as XOR.
- **Backpropagation** computes gradients by applying the chain rule backward through the computational graph; optimisation algorithms then use those gradients to update weights.
- **Architecture choices** such as depth, width, activations, output units and loss functions affect capacity, trainability and generalisation.
- **Key caution:** universal approximation means a network can represent broad function classes, not that it will learn the right function or generalise automatically.

### Introduction
Neural networks form the base of deep learning. Neural networks take in data, train themselves to recognise the patterns in the input data and then predict the output using the patterns. Neural networks are modelled loosely after the human brain and are designed to recognise patterns.

The feedforward neural network is considered one of the simplest types of artificial neural networks. Feedforward neural networks are also known as multi-layered networks of neurons (MLN). These networks of models are called feedforward because the information only travels forward in the neural network. It travels through the input nodes, then through the hidden layers (a single layer or many layers) and finally, through the output nodes.

Feedforward networks are of extreme importance to artificial intelligence (AI) practitioners. They form the basis of many important commercial applications. For example, the applications used to recognise objects from photographs use a specialised type of feedforward network. Feedforward networks are a conceptual stepping stone on the path to recurrent networks, which power many natural language applications. Feedforward networks take advantage of different methods, such as backpropagation, to improve the accuracy of the application outcomes.

In this Module, you will learn about basic feedforward neural networks and how to use these networks in machines to address complex problems. You will also learn about the important elements of a neural network structure, including the neurons, connections, weights, biases, input layer, hidden layers and output layer.

In learning about feedforward neural networks, you will encounter two important concepts: 
1. forward propagation; and 
2. backpropagation. 

Generally, forward propagation refers to the calculation of values for the hidden layers and output layer for a given neural network based on data in the input layer. Thus, under forward propagation, information flows from the input layer to the hidden layers to the output layer. Conversely, backpropagation refers only to the method for computing the gradient. Thus, under backpropagation, the method traverses the network in the reverse order (i.e., from the output to the input layer).

One key takeaway from this Module is that feedforward networks can be seen as efficient non-linear function approximators that use gradient descent to minimise the error in a function approximation.

### Resources

#### 1. Introduction to Feedforward Neural Networks
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). Deep learning. Cambridge, MA: MIT Press. Retrieved from https://www.deeplearningbook.org/

*Resource Overview:*

    This book contains an introduction to a broad range of topics in deep learning. Specifically, it covers the mathematical and conceptual background to deep learning, the deep learning techniques used in industry and research perspectives. This book will be used throughout all the DLE602 modules.

    Please read Chapter 6 for this Module. This chapter is dedicated to deep feedforward networks. Pay special attention to the introduction and all the top-level sections to Section 6.5. You may choose to skim through the subsequent subsections; for example, Sub-section 6.2.2.1 or 6.3.3. The introductory sections will help you gain necessary knowledge about deep feedforward networks. Section 6.5 will explain another key concept for this Module: backpropagation.

> *Status: ✅ Read + Reviewed — see [module02_notes.md](module-02-feedforward-and-backpropagation/module02_notes.md)*

#### 2. Introduction to Feedforward Neural Networks
- Reed, R. D. & Marks, R. J. (1999). Neural smithing: Supervised learning in feedforward artificial neural networks. Cambridge, MA: MIT Press. Retrieved from http://search.ebscohost.com.torrens.idm.oclc.org/login.aspx?direct=true&db=nlebk&AN=9366&site=ehost-live&authtype=ip,sso&custid=ns251549&ebv=EB&ppid=pp_31

*Resource Overview:*

    This book focuses on multilayer perceptrons (MLPs), a feedforward neural network model that is used in applications as diverse as finance (forecasting), manufacturing (process control) and science (speech and image recognition).

    Please read Chapter 4 for this Module. This chapter, entitled ‘MLP Representational Capabilities’, provides an easy-to-follow step-by-step guide for a basic neural network structure and also highlights some important points that are required to form a suitable neural network. It presents a practical overview of different aspects of the MLP methodology.

> *Status: ✅ Read + Reviewed — see [module02_notes.md](module-02-feedforward-and-backpropagation/module02_notes.md)*

#### 3. Neural Networks and Convolutional Neural Networks Essential Training - Neurons and Artificial Neurons
- Reference:Fernandes, J. (2018, 4 May). Neurons and artificial neurons. In Neural networks and convolutional neural networks essential training [Video file]. Retrieved from https://www.linkedin.com/learning/neural-networks-and-convolutional-neural-networks-essential-training/neurons-and-artificial-neurons?u=56744473

*Resource Overview:*

    Neural Networks and Convolutional Neural Networks Essential Training - Neurons and Artificial Neurons

> *Status: 🔥 WIP — needs manual listen/authenticated LinkedIn access*

#### 4. A Beginner's Guide to Neural Networks and Deep Learning
- Reference:Pathmind. (n.d.). A beginner’s guide to neural networks and deep learning. Retrieved from https://pathmind.com/wiki/neural-network.

*Resource Overview:*

    This is a great beginner’s guide to important topics in AI, machine learning (ML) and deep learning.
    It will introduce you to all the necessary basic concepts of the neural networks. You will also find some good examples along with related discussions.

> *Status: ✅ Read + Reviewed — see [module02_notes.md](module-02-feedforward-and-backpropagation/module02_notes.md)*

### Learning Activities

#### 1. Understanding Feedforward Networks

As part of this activity, focus on ‘Section 6.1. Example: Learning XOR’ of Goodfellow et al.’s (2016) book in the essential resource section. The authors write, ‘To make the idea of a feedforward network more concrete, we begin with an example of a fully functioning feedforward network on a very simple task: learning the XOR function’ (Goodfellow et al., 2016, p. 167).

In no more than 100 words, describe the feedforward network the above sentence (Goodfellow et al.) is referring to in your own words. Post your answer to the Understanding Feedforward Networks discussion forum. Please read the other students’ posts and select the best and the easiest description that you have read and report it to the class or to the facilitator.

Keep a counter on to see which description wins.

> *Status: 🕐 To-Do*

#### 2. Interactive Knowledge Sharing - Backpropagation

Be brave and be the first to share your understanding of backpropagation and its importance on the discussion forum. Share your thoughts and pose an interesting question about backpropagation to the class.

The discussion should yield a better understanding of backpropagation for all.

> *Status: 🕐 To-Do*

#### 3. The Disadvantage of Neural Networks

Speaking of questions in the last activity, it is our turn to ask you a question.

We have learned some exciting and amazing facts about neural networks, but what if you were asked to list some of the disadvantages of neural networks?

List and explain the disadvantages of neural networks and upload them to the discussion forum (ensure your post is no more than 100 words).

Respond to your peers by either agreeing or disagreeing and provide your rationale.

> *Status: 🕐 To-Do*

---

## Module 3 - Deep Learning Application: Natural Language Processing, Speech Recognition and Computer Vision

### TLDR
- **Deep learning powers three flagship application areas:** computer vision, speech recognition, and NLP - all built on the large-scale (GPU, distributed) infrastructure from Goodfellow Ch.12.
- **NLP arc:** classical **n-grams** (the A1 baseline) suffer the curse of dimensionality; **word embeddings** and **attention** (encoder-decoder) are the deep-learning leap that generalises better.
- **Zhao et al. (2018) is the Assessment 1 reference paper:** **GloVe-DCNN** fuses embeddings + n-grams + lexicon + Twitter features into a deep CNN, beating BoW baselines (up to 87.62% acc) on five datasets, including STS-Test and STS-Gold.
- **Noda et al. (2015)** shows **multimodal** speech recognition: a denoising autoencoder (audio) + CNN lip-reading (visual) fused by a multi-stream HMM for noise robustness.
- **Module pattern:** the right *architecture* is matched to each *sub-task* - CNN for vision, autoencoder for denoising, attention/embeddings for language.

### Introduction
Artificial intelligence (AI), deep learning and high-performance computing are enabling a new industrial revolution, which is leading to an era of smart creation and streamlined decision making.

Some examples of smart and intelligent applications include:
- Natural language processing (NLP): A branch of AI that helps machines understand, interpret and manipulate human language;
- Speech recognition: Technology employed by smart systems, such as Amazon’s Alexa or voice-recognition texting; and
- Computer vision: An analytical solution that can achieve state-of-the-art results in image classification, object detection and face recognition.
Additionally, AI and deep learning are redesigning healthcare by bringing in a new era of precision medicine, changing the eCommerce landscape to enable companies to better engage with their customers and improving manufacturing processes across the supply chain.

It is critical that early career professionals are able to envision and realise the true potential of deep learning. Once these amazing possibilities are well understood, the complex theories of deep learning become even more evident.

### Resources

#### 1. Deep Learning Applications
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). Deep learning. Cambridge, MA: MIT Press. Retrieved from https://www.deeplearningbook.org/

*Resource Overview:*

    This book contains an introduction to a broad range of topics in deep learning. Specifically, it covers the mathematical and conceptual background to deep learning, the deep learning techniques used in industry and research perspectives. This book will be used throughout all the DLE602 modules.

    Please read Chapter 12 for this Module, which discusses various deep learning applications. Section 12.1 provides you with a general overview of the building blocks of deep learning applications. Section 12.2 considers computer vision applications. Section 12.3 discusses speech recognition. While Section 12.4 describes applications for NLP.

> *Status: ✅ Read + Reviewed — see [module03_notes.md](module-03-nlp-speech-recog-computer-vision/module03_notes.md)*

#### 2. Deep Convolution Neural Networks for Twitter Sentiment Analysis
- Zhao, J., Gui, X. & Zhang, X. (2018). Deep convolution neural networks for Twitter sentiment analysis. IEEE Access, 6, 23253–23260. Retrieved from https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8244338

*Resource Overview:*

    This research paper demonstrates how to use deep learning models to analyse a Twitter dataset to better understand the sentiments hidden among all the tweets. It is a great example of research work for NLP.

    You must refer to this paper for Assessment 1. It is important that you understand the deep learning practices in this paper independent of the dataset. It is essential that you are able to apply these deep learning practices to other datasets (e.g., Facebook or LinkedIn datasets) and obtain similar results.

> *Status: ✅ Read + Reviewed — see [module03_notes.md](module-03-nlp-speech-recog-computer-vision/module03_notes.md)*

#### 3. Audio-Visual Speech Recognition using Deep Learning
- Noda, K., Yamaguchi, Y., Nakadai, K., Okuno, H. G. & Ogata, T. (2015). Audio-visual speech recognition using deep learning. Applied Intelligence, 42(4), 722–737. Retrieved from https://search-proquest-com.torrens.idm.oclc.org/docview/1674443602?OpenUrlRefId=info:xri/sid:wcdiscovery&accountid=176901

*Resource Overview:*

    This research paper demonstrates how deep neural networks can be effectively used for speech recognition applications. It is a great example of research work for the speech recognition branch of deep learning. Perhaps the most interesting part of this paper is how the proposed model addresses the noise problem that arises in every speech recognition application.

> *Status: ✅ Read + Reviewed — see [module03_notes.md](module-03-nlp-speech-recog-computer-vision/module03_notes.md)*

### Learning Activities

#### 1. Interactive Knowledge Sharing - Natural Language Processing
Step 1: Think of an exciting NLP application that is important to you and that you believe that will have a wider impact on society.

Step 2: Propose and discuss the deep learning algorithms, datasets, models and other factors that you may have to consider for this application with the class.

Step 3: Put together a flowchart in a Word document on how all the considered elements in Step 2 will come together. Clearly show the input and output, all the critical decision points, the processes that will take place in the middle and any possible errors that may occur in the process flow.

Post your flowchart to the Module 3 discussion forum.

> *Status: ✅ Done*

#### 2. Interactive Knowledge Sharing - Speech Recognition
Step 1: Think of an exciting speech recognition application that is important to you and that you believe that will have a wider impact on society.

Step 2: Propose and discuss the deep learning algorithms, datasets, models and other factors that you may have to consider for this application with the class.

Step 3: Put together a flowchart in a Word document on how all the considered elements in Step 2 will come together. Clearly show the input and output, all the critical decision points, the processes that will take place in the middle and any possible errors that may occur in the process flow.

Post your flowchart to the Module 3 discussion forum.

> *Status: 🕐 To-Do*

#### 3. Interactive Knowledge Sharing - Computer Vision
Step 1: Think of an exciting computer vision application that is important to you and that you believe that will have a wider impact on society.

Step 2: Propose and discuss all the deep learning algorithms, datasets, models and other factors that you may have to consider for this application with the class.

Step 3: Put together a flowchart in a Word document on how all the considered elements in Step 2 will come together. Clearly show the input and output, all the critical decision points, the processes that will take place in the middle and any possible errors that may occur in the process flow.

Post your flowchart to the Module 3 discussion forum.

> *Status: 🕐 To-Do*

---

## Module 4 - Regularization

### TLDR
- **Regularization** = any technique that makes a model generalise better (lower test error), bought by **trading a little bias for a lot less variance** - the cure for overfitting (Goodfellow Ch.7).
- **Parameter norm penalties:** **L2** (weight decay / ridge) shrinks weights toward zero; **L1** (lasso) drives many weights to *exactly* zero → sparsity and feature selection.
- **The practical toolkit:** dataset augmentation, **early stopping** (the most-used regularizer), **dropout** (a cheap approximation to bagging an exponential ensemble of shared-weight sub-networks), bagging, noise/label smoothing.
- **Kukačka et al. taxonomy:** there are exactly **5 levers** to regularize - **data, architecture, error function, regularization term, optimization** - so seemingly unrelated methods (augmentation, dropout, batch norm) are close cousins.
- **Wang & Klabjan:** overfitting hits **unsupervised** nets (RBM/DBN/DBM) too; their **partial DropConnect (PDC)** is the most stable fix.
- **Shubham (2018)** is the **Activity 1** hands-on: L1/L2, dropout, augmentation and early stopping on an MNIST digit-recognition net in Keras (augmentation gave the biggest leap).

### Introduction
Regularization is one of the key elements of machine learning, particularly of deep learning. Regularization refers to any supplementary technique that aims to make a deep learning model generalise better to produce better results for testing datasets. This can include various properties of the loss function, the loss optimisation algorithm or other techniques.

For example, imagine a deep learning model that was built to identify cats using any images. If the model was perfected in extreme details with training data of lions and Siberian tigers, the model may not be able to identify domestic cats from images, as the size, structure and posture of the big cats (i.e., almost all their attributes) will be bigger or larger than those of the domestic cats.

In situations like this, regularization helps deep learning models to become generalised. In this example, regularization could help the deep learning model to identify all types of cats.

### Resources

In this Module, you will learn about an important concept in deep learning called 'regularization'.

A central problem in deep learning is how to make an algorithm that will perform well not just on the training data, but also with new inputs. Many of the strategies used in deep learning have been explicitly designed to reduce test errors, possibly at the expense of increased training errors. These strategies are known collectively as 'regularization'.

You will also learn about related concepts, such as underfitting and overfitting. Most of the research literature available explains regularization in relation to overfitting, which occurs when a model performs exceptionally well with training data, but is not able to predict testing data. In this Module, you will learn about the concept of overfitting and how regularization helps to overcome this problem.

Finally, you will have a hands-on practical experience with regularization.

#### 1. Regularization in Deep Learning
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). Deep learning. Cambridge, MA: MIT Press. Retrieved from https://www.deeplearningbook.org/

*Resource Overview:*

    This book contains an introduction to a broad range of topics in deep learning. Specifically, it covers the mathematical and conceptual background to deep learning, the deep learning techniques used in industry and research perspectives. This book will be used throughout all the DLE602 modules.

    Please read Chapter 7 for this Module, which discusses regularization. Focus on the various general strategies used to regularise neural networks and investigate all the necessary concepts, such as generalisation, underfitting, overfitting, bias and variance.

> *Status: ✅ Read + Reviewed — see [module04_notes.md](module-04-regularization/module04_notes.md)*

#### 2. Regularization for Unsupervised Deep Neural Nets
- Wang, B. & Klabjan, D. (2017). Regularization for unsupervised deep neural nets. (ArXiv Working Paper). Retrieved from http://torrens.idm.oclc.org/login?url=https://search-proquest-com.torrens.idm.oclc.org/docview/2075336595?accountid=176901

*Resource Overview:*

    This research paper demonstrates that overfitting occurs in different deep learning models and in deep feedforward neural networks and discusses possible regularization methods to reduce overfitting.

    This research paper will help you better understand the theories related to regularization that you encountered previously. It highlights the application of regularization.

> *Status: ✅ Read + Reviewed — see [module04_notes.md](module-04-regularization/module04_notes.md)*

#### 3. Regularization for Deep Learning: A Taxonomy
- Kukacka, J., Golkov, V. & Cremers, D. (2017). Regularization for deep learning: A taxonomy. (ArXiv Working Paper). Retrieved from http://torrens.idm.oclc.org/login?url=https://search-proquest-com.torrens.idm.oclc.org/docview/2076307708?accountid=176901

*Resource Overview:*
    
    As the title suggests, this research paper presents a taxonomy of regularization in deep learning. It starts at a very basic level and then describes different regularization methods in detail.

    Read the entire paper and pay extra attention to Sections 3 to 7 to try understand the difference between different regularization methods.

> *Status: ✅ Read + Reviewed — see [module04_notes.md](module-04-regularization/module04_notes.md)*

#### 4. An Overview of Regularization Techniques in Deep Learning (with Python code)
- Shubham, J. (2018, 19 April). An overview of regularization techniques in deep learning (with Python code) [Web log post]. Retrieved from https://www.analyticsvidhya.com/blog/2018/04/fundamentals-deep-learning-regularization-techniques/

*Resource Overview:*
    
   This is a great blog post for deep learning beginners, as it provides a summarised presentation of the regularization concept. This blog highlights all the basic points that you need to know to understand regularization.

    This post also contains a case study. Pay extra attention to the case study, as it will be used in one of the in-class activities. It is highly recommended that you download all the necessary software and dataLinks to an external site. related to this case study.

> *Status: ✅ Read + Reviewed — see [module04_notes.md](module-04-regularization/module04_notes.md)*

### Learning Activities

#### 1. Programming
Let us put our understanding into practice. The resource by Shubham (2018) shares some amazing general knowledge about regularization. Additionally, at the end of the post, Shubham (2018) also discusses a case study on MNIST data with keras. This case study is about automatic digit recognition, a popular object recognition exercise in image data.

Please follow the instructions in relation to the Python implementation for the above case study. Copy and download the necessary Python codes and data from Shubham (2018) or the associated links (https://datahack.analyticsvidhya.com/contest/practice-problem-identify-the-digits/). Follow the instructions, run the code using the image data provided, observe the outcome and pay extra attention to the regularization technique used in this implementation.

Discuss your experience and observations about regularization in the discussion forum.

> *Status: 🕐 To-Do*

#### 2. Analysis
Whenever we discuss regularization, we are also explicitly or implicitly talking about overfitting. As part of this activity, you are required to identify an area in which overfitting may be required and may produce better outcomes.

Share your answer to the discussion forum and explain why you would prefer to overfit your model for this selected area.

> *Status: 🕐 To-Do*

#### 3. I Wish
Share your views as to whether if you had previous knowledge of regularization, it would have made any difference to your Assessment 1 submission. If you believe it would have made a difference, discuss the impact this knowledge would have had in the discussion forum in no more than 100 words.

---

## Module 5 - Convolutional Neural Networks

### TLDR
- **A CNN** swaps general matrix multiplication for **convolution** in at least one layer; it is the go-to network for **grid-structured data** (images, audio spectrograms, even text windows).
- **Three structural ideas** make convolution work (Goodfellow Ch.9): **sparse interactions**, **parameter sharing** (tied weights) and **equivariance to translation** - together they slash the parameter count and let a feature be detected *anywhere* in the input.
- **Pooling** (usually **max pooling**) summarises a neighbourhood into one value, giving **approximate invariance to small translations** and letting the net accept variable-size inputs.
- **The landmark architectures trace the field's arc:** **AlexNet** (2012, depth + GPUs) → **VGG16** (depth via small 3×3 filters) → **GoogleNet/Inception** (width + 1×1 bottlenecks); **ResNet** later added **skip connections** to train 152 layers.
- **Training a CNN is the same loop as any net** - forward → loss → backprop → SGD; only the per-layer math changes (Zhou's from-scratch NumPy MNIST CNN reaches ~78%, ~97% in Keras).
- **Assessment link:** A1 stays classical n-grams, but the **Zhao et al. (2018) GloVe-DCNN** you cite *is* a CNN over text - Module 5 finally explains that architecture and feeds the **Review Pulse v2** direction.

### Introduction
A convolutional neural network (CNN) is the type of neural network that is most often applied to image-processing problems. You have probably seen CNNs in practise anywhere software has to identify an object in an image (e.g., when Facebook identifies you and your friends in an image that you just uploaded). However, you can also use CNNs in natural language processing. The fact that CNNs are useful in these fast growing areas is one of the main reasons why they are very important in deep learning (DL) and artificial intelligence (AI).

CNNs are designed from biologically driven models. These models try to mimic how a human perceives an image in the brain in different layers. Unlike simple neural networks that have one or several hidden layers, CNNs have many layers. This allows them to compactly represent highly nonlinear and varying functions. CNNs have proven highly efficient in image-processing pattern recognition applications.

In this Module, you will learn about a key concept in deep learning (DL) called convolutional neural networks (CNNs). CNNs are specialised neural networks that work with data that have a clear grid-structured topology and scale such neural networks to very large size. This approach has been very successful for two-dimensional image topologies.

You will also learn about related concepts, such as convolution (a specialised kind of linear operation), kernel (a second argument to the convolution) and pooling (an operation that almost all convolutional networks employ).

Finally, it is important that you pay special attention to several variants of the convolution function that are widely used in practice for neural networks. For example, one may not use only a strict linear operation to transform inputs to outputs in a convolutional layer.

### Resources

#### 1. Convolutional Neural Network
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). Deep learning. Cambridge, MA: MIT Press. Retrieved from https://www.deeplearningbook.org/

*Resource Overview:*

    This book contains an introduction to a broad range of topics in DL, including its mathematical and conceptual background, the DL techniques used in industry and different research perspectives. This book will be used throughout all the DLE602 modules.

    Please read Chapter 9 for this Module. This chapter introduces CNNs, highlights relevant concepts (e.g., convolution, kernel and pooling) and provides examples. Section 9.5 discusses some variants of the basic convolutional function.

    If the concepts discussed in the chapter are not clear, please refer to the additional resources in this Module.

> *Status: ✅ Read + Reviewed — see [module05_notes.md](module-05-cnn/module05_notes.md)*

#### 2. Convolutional and Recurrent Neural Networks
- Kelleher, J. D. (2019). Deep learning. Cambridge, MA: MIT Press. Retrieved from https://ebookcentral-proquest-com.torrens.idm.oclc.org/lib/think/reader.action?docID=5855529&ppg=173

*Resource Overview:*

    This book contains an easy to read introduction to CNNs. The discussion starts at a very basic level and builds from there with examples.

    Please read Chapter 5 for this Module. If necessary, you can read Chapter 4 to refresh your memory before jumping into the details of CNN. For this Module, you only need to read the CNN section of the chapter.

    Pay special attention to the different CNNs developed over the past decade, such as AlexNet and ResNet.

> *Status: ✅ Read + Reviewed — see [module05_notes.md](module-05-cnn/module05_notes.md)*

#### 3. Neural Networks and Convolutional Neural Networks Essential Training
- Fernandes, J. (2018). Neural networks and convolutional neural networks essential training [Video file]. Retrieved from https://www.linkedin.com/learning/neural-networks-and-convolutional-neural-networks-essential-training/convolutions?u=56744473

*Resource Overview:*

    This LinkedIn Learning course is a great resource that will ease anyone into the world of CNNs.

    You may wish to view all the short videos from Chapters 1 to 5; however, pay special attention to ‘Chapter 4: Convolutional Neural Networks’ and ‘Chapter 5: Convolutional Neural Networks in Keras’.

> *Status: 🔥 WIP — needs manual listen/authenticated LinkedIn access*

#### 4. A Review of Popular Deep Learning Architectures: AlexNet, VGG16 and GoogleNet
- Kumara, V. (2020). A review of popular deep learning architectures: AlexNet, VGG16 and GoogleNet [Web log post]. Retrieved from https://blog.paperspace.com/popular-deep-learning-architectures-alexnet-vgg-googlenet/

*Resource Overview:*

    This great blog post discusses different types of popular DL architectures.

    It is important to pay attention to the relationship between these architectures and CNNs, as this will help you implement any project that involves such architectures. Additionally, pay special attention to the unique value proposition of each architecture.

> *Status: ✅ Read + Reviewed — see [module05_notes.md](module-05-cnn/module05_notes.md)*

#### 5. CNNs, Part 2: Training a Convolutional Neural Network
- Zhou, V. (2019). CNNs, Part 2: training a convolutional neural network [Web log post]. Retrieved from https://victorzhou.com/blog/intro-to-cnns-part-2

*Resource Overview:*

    This great blog post discusses how to train a CNN.

    It is good to have sound ideas on how to train a network before putting your network into practise. Pay special attention to the Python codes shared in the post, as these will help you to better understand how to implement such codes in your final assessment.

> *Status: ✅ Read + Reviewed — see [module05_notes.md](module-05-cnn/module05_notes.md)*

### Learning Activities

#### 1. Critical Analysis I—Initial Recommendation
As part of this individual activity, describe situations, using examples, in which a CNN should be recommended over a Feedforward Neural Network. In completing this activity, ensure that you:

- Critically analyse the task;
- Form your example and present your recommendation to the discussion forum entitled ‘Critical Analysis!—Initial Recommendation’; and
- Review other students’ recommendations and provide your feedback.

> *Status: 🕐 To-Do* 

#### 2. Critical Analysis II—Final Recommendation
This is a continuation of Critical Analysis I. In completing this activity, ensure that you:
- Review the feedback you received for your initial recommendation;
- Revise your initial recommendation based on the feedback received; and
Post your final recommendation (of no more than 100 words) to the discussion forum entitled ‘Critical Analysis II—Final Recommendation’. Ensure you use your own words.

> *Status: 🕐 To-Do*

#### 3. Train the Network
As part of this activity, you will work on one of the important issues related to neural networks: training a neural network.
- Imagine that you have been tasked with training a CNN to identify the images of two types of animals: cats and dogs.
- Discuss your strategy for training the CNN and explain why it is the best. Support your claims with research.
Post your response to the discussion forum.

> *Status: 🕐 To-Do*

#### 4. Collaboration
The two common problems that are currently observed with CNNs are the:
1. Computer requirement; and
2. Memory requirement.

By now, you have been allocated to a group and your group has been assigned a stance (i.e., your group is either in favour or against the above statement).

If you have not yet been allocated to a group, please contact your facilitator immediately.

Click on DLE602 Wiki Group > Then, click on Pages.
Click on the Page titled "Module 5: Learning Activity 4 - Collaboration".
Click on Edit to edit the Page.
Insert your response in the column to which you are allocated. Justify your response.
To save your response, remember to click on the ‘Save’ button.

The facilitator will decide on the winner of the two groups.

> *Status: 🕐 To-Do*

---

## Module 6 - Linear Factor Models

### TLDR

- A **linear factor model** explains observed data as `x = Wh + b + noise`, where `h` contains unobserved explanatory factors.
- **PCA** preserves high-variance directions; **factor analysis** models shared covariance separately from variable-specific noise.
- **ICA** separates independent non-Gaussian sources; **SFA** extracts slowly changing temporal features.
- **Sparse coding** reconstructs inputs using a small number of active basis vectors, commonly encouraged by an L1 penalty.
- These classical latent-variable methods are the conceptual bridge to nonlinear **autoencoders, embeddings, and deep representation learning**.

### Introduction
Linear factor models are some of the simplest generative models and some of the simplest models that learn a representation of data. Linear factor models can help simplify neural networks by streamlining data inputs. Deep learning (DL) research involving latent variables are good candidates for using linear factor models (i.e., probabilistic models with latent variables).

Linear factor models can be better explained with a popular phenomenon called the cocktail party effect, which highlights the brain's ability to focus on the single speech signal that matters in a crowded room full of noises. How does the brain do this? Linear factor models sort of mimic this phenomenon by allowing machines to focus on the signals that matter.

Different models are often discussed under the linear factor models banner. However, the key to success is to decide the suitability and the necessity of these models for any given project.

Hearing facts: What is the cocktail party effect? [Web log post]. (2016, 25 July). Retrieved from https://global.widex.com/en/blog/hearing-facts-what-is-the-cocktail-party-effect

In this Module, you will learn about an important concept called linear factor models. This Module describes some of the simplest probabilistic models with latent variables; that is, linear factor models.

In this Module, of the many linear factor models available, you will learn about probabilistic principal component analysis (PCA), factor analysis, independent component analysis (ICA), slow feature analysis (SFA) and sparse coding. These models are often considered the most prominent by practitioners.

Finally, it is important to visualise how these linear factor models are related to the neural networks and how these models can help operate the neural networks efficiently by streamlining the input data.

### Resources

#### 1. Linear Factor Models
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). Deep learning. Cambridge, MA: MIT Press. Retrieved from https://www.deeplearningbook.org/

*Resource Overview:*

    This book contains an introduction to a broad range of topics in DL, including its mathematical and conceptual background, the DL techniques used in industry and different research perspectives. This book will be used throughout all the DLE602 modules.

    Please read Chapter 13 for this Module. This chapter introduces you to various linear factor models. It is recommended that you study at least the first four models (i.e., Section 13.1 to Section 13.4) closely.

    It is also highly recommended that you take a look at all the other resources in this Module that contain additional introductory information on these linear factor models.

> *Status: ✅ Read + Reviewed — see [module06_notes.md](module-06-linear-factors-models/module06_notes.md)*

#### 2. SPSS Statistics Essential Training: Factor Analysis and Principle Component Analysis
- Poulson, B. (2019). SPSS statistics essential training: Factor analysis and principle component analysis [Video file]. Retrieved from https://www.linkedin.com/learning/spss-statistics-essential-training-2/factor-analysis-and-principal-component-analysis?u=56744473

*Resource Overview:*

    This LinkedIn learning video contains an easy-to-understand explanation of PCA and factor analysis based on an example dataset. In watching the video, it is not necessary to know anything about the SPSS software and you need not pay attention to any discussions on SPSS. Listen to the introduction to PCA in the first minute of the video and then follow the overall processes used to reduce the dimensionality of the dataset.

    This will provide you with a basic understanding of PCA and factor analysis. This resource will help you to better understand the detail analysis in (Goodfellow, 2016).

> *Status: ✅ Read + Reviewed — see [module06_notes.md](module-06-linear-factors-models/module06_notes.md)*

#### 3. What is Independent Component Analysis?
- Hyvärinen, A. (2019). What is independent component analysis?. Retrieved from https://www.cs.helsinki.fi/u/ahyvarin/whatisica.shtml

*Resource Overview:*

    This short blog post from the University of Helsinki contains an easy-to-understand explanation of ICA.

    This will provide you with a basic understanding of ICA. This resource will help you to better understand the detail analysis in (Goodfellow, 2016).

> *Status: ✅ Read + Reviewed — see [module06_notes.md](module-06-linear-factors-models/module06_notes.md)*

#### 4. A Quick Introduction to Slow Feature Analysis
- Hlynsson, H. (2017, 21 October). A quick introduction to slow feature analysis [Web log post]. Retrieved from https://towardsdatascience.com/a-brief-introduction-to-slow-feature-analysis-18c901bc2a58

*Resource Overview:*

    This short blog post contains an easy-to-understand explanation of SFA.

    This will provide you with a basic understanding of SFA. This resource will help you to better understand the detail analysis in (Goodfellow, 2016).

> *Status: ✅ Read + Reviewed — see [module06_notes.md](module-06-linear-factors-models/module06_notes.md)*

#### 5. Sparse Coding
- UFLDL Tutorial. (2017). Sparse coding. Retrieved from http://ufldl.stanford.edu/tutorial/unsupervised/SparseCoding/

*Resource Overview:*

    This short blog post contains an easy-to-understand explanation of sparse coding.

    This will provide you with a basic understanding of sparse coding. This resource will help you to better understand the detail analysis in (Goodfellow, 2016).

> *Status: ✅ Read + Reviewed — see [module06_notes.md](module-06-linear-factors-models/module06_notes.md)*

#### 6. Difference between Machine Learning and Statistical Modelling
- Srivastava, T. (2015, 1 July). Difference between machine learning and statistical modeling [Web log post]. Retrieved from https://www.analyticsvidhya.com/blog/2015/07/difference-machine-learning-statistical-modeling/

*Resource Overview:*

    This great post discusses the difference between machine learning and statistical modelling.

    As you complete this Module, you may find that some of the concepts sound quite statistical. This additional reading will help you visualise how these statistical studies are often related to machine learning and thus to DL. Keep in mind that DL does not standalone and is a subset of machine learning and machine learning is a subset of artificial intelligence.

> *Status: ✅ Read + Reviewed — see [module06_notes.md](module-06-linear-factors-models/module06_notes.md)*

### Learning Activities

#### 1. Comparison
Your understanding of linear factor models will be tested in this activity.

Answer the following questions in no more than 150 words and post your responses to the Module 6 discussion forum:
- When should ICA be preferred over PCA?

Please read other students’ posts and provide feedback.

> *Status: 🕐 To-Do* 

#### 2. Idea Generation
As part of this activity, you will generate some project or application ideas in relation to linear factor models.

Propose one application for each of the following: (i) natural language processing; (ii) speech recognition; and (iii) computer vision. Ensure that the applications proposed could use linear factor models. Explain how linear factor models are used for the proposed applications.

The key here is to identify and discuss as many applications as possible from each of the three categories mentioned above.

> *Status: 🕐 To-Do* 

#### 3. Open Forum
This discussion forum is meant to be an open forum where you and your peers can post questions and answers. An open forum is a great way to learn from and share knowledge with other participants. It is a great opportunity to ask any questions and find out other people’s points of view.

This forum is meant to be fun and useful. Thus, do not hesitate to ask any question you have or seek clarification. Some example questions include:
- What is a latent variable?
- Can you share an example of latent variable?
- Can you explain factor analysis in purely statistical terms?
- I do not understand ‘…’, can anyone explain?

> *Status: 🕐 To-Do* 

---

## Module 7 - Autoencoders

### TLDR

- An **autoencoder** is a neural net that copies its input to its output through a bottleneck **code** `h` (encoder `h=f(x)` → decoder `r=g(h)`); the value comes from copying *imperfectly*, forcing it to learn the data's salient structure (Goodfellow Ch.14).
- An **undercomplete autoencoder with linear encoder/decoder mappings and squared-error (MSE) loss recovers the PCA subspace** at its global optimum - Baldi (2012) proves that optimum is the projection onto the top eigenvectors; the real payoff of autoencoders is the **nonlinear, deep, stackable** generalisation of PCA.
- **Regularized variants** shape what `h` keeps: **sparse** (few active units, L1/Laplace), **denoising** (reconstruct clean from a corrupted input - implicitly learns the data manifold / score), **contractive** (features insensitive to small input changes).
- **Bengio (2012):** deep, stacked autoencoders learn abstract representations that **transfer** to new tasks with very few labels - the academic backbone of the Review Pulse transfer-learning story. Bengio cites **Glorot et al. (2011b)**, who used stacked denoising autoencoders with sparse rectifiers for **domain adaptation in sentiment classification** - essentially the same task one deep-learning generation earlier.
- **Applications:** dimensionality reduction, semantic-hashing information retrieval, and **deepfakes** (two autoencoders sharing an encoder, swap the decoders - Dickson 2020).
- **Overfitting caution:** an overcomplete autoencoder with too much capacity just learns the identity function and nothing useful - regularization is the cure (Module 4, now on an unsupervised net).

### Introduction
Autoencoders are neural networks that are trained to attempt to copy input to output. They reduce the dimensionality of input and then reconstruct the output from this representation.

Autoencoders are currently used in a limited set of real-world applications. However, recently, they have been receiving significant attention for their ability to produce deepfake videos. Deepfake videos or audios are recordings that look and sound just like the original object or person.

Autoencoders use an unsupervised learning process that allows you to take advantage of your unlabelled data and learn interesting things about the structure of the data that is often useful for another context. At a high level, autoencoders learn to throw away noisy details from the initial raw data and only keep the data important for inputs to, for example, another neural network.

In this Module, you will learn about autoencoders. Autoencoders are a unique form of neural networks. Autoencoder architecture can be divided into two parts: 1) the encoder; and 2) decoder. The encoder part encodes the features of the input training data. While the decoder part tries to convert those encoded features back to the input features. Autoencoders have been successfully applied to dimensionality reduction and information retrieval tasks.

In this Module, you will learn about different autoencoders; for example, denoising, contractive, sparse and other autoencoders. Each of these autoencoders differ slightly and offer unique value propositions to deep learning (DL) practitioners.

Despite their limited use at this time, autoencoders are full of potential. An ability to envision the future use of autoencoders will provide you with a competitive edge in the world of DL. Thus, reviewing the current applications of autoencoders is an important exercise in this Module.

### Resources

#### 1. Autoencoders
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). Deep learning. Cambridge, MA: MIT Press. Retrieved from https://www.deeplearningbook.org/

*Resource Overview:*

    This book contains an introduction to a broad range of topics in DL, including its mathematical and conceptual background, the DL techniques used in industry and different research perspectives. This book will be used throughout all the DLE602 modules.

    Please read Chapter 14 for this Module. This chapter introduces you to autoencoders and discusses various types of autoencoders. It will be beneficial to read from 'Section 14.1: Undercomplete Autoencoders' to 'Section 14.7: Contractive Autoencoders' to learn about different types of autoencoders.

    Finally, read 'Section 14.9: Applications of Autoencoders' to learn about the applicability of autoencoders.

> *Status: ✅ Read + Reviewed — see [module07_notes.md](module-07-autoencoders/module07_notes.md)*

#### 2. Autoencoders, Unsupervised Learning and Deep Architectures
- Baldi, P. (2012). Autoencoders, unsupervised learning and deep architectures. Proceedings of ICML Workshop on Unsupervised and Transfer Learning, in Proceedings of Machine Learning Research (PMLR) 27, 37-49. Retrieved from http://proceedings.mlr.press/v27/baldi12a/baldi12a.pdf

*Resource Overview:*

    This paper will provide you with an understanding of the basic concept of autoencoders. It discusses both linear and non-linear autoencoders. It is worth paying attention to both linear and non-linear autoencoders, as data often do not follow a simple model.

    Studying the above in detail will enable you to gain a general perspective on autoencoders and define the key properties that are shared by different autoencoders.

> *Status: ✅ Read + Reviewed — see [module07_notes.md](module-07-autoencoders/module07_notes.md)*

#### 3. Deep Learning of Representations for Unsupervised and Transfer Learning
- Bengio, Y. (2012). Deep learning of representations for unsupervised and transfer learning. Proceedings of ICML Workshop on Unsupervised and Transfer Learning in Proceedings of Machine Learning Research (PMLR), 27, 17-36. Retrieved from http://proceedings.mlr.press/v27/bengio12a/bengio12a.pdf

*Resource Overview:*

    One of the main focuses of this research paper is unsupervised learning in the world of DL. This topic is intimately related to autoencoders. This paper reiterates the point that autoencoders use an unsupervised learning process that allows you to take advantage of your unlabelled data.

    Perhaps the most interesting section of this paper is 'Section 3: A Zoo of Possible Layer-Wise Unsupervised Learning Algorithms'. This section not only discusses autoencoders but also briefly discusses linear factor models, which you learned about in Module 6.

> *Status: ✅ Read + Reviewed — see [module07_notes.md](module-07-autoencoders/module07_notes.md)*

#### 4. What is a Deepfake?
- Dickson, B. (2020, 5 March). What Is a deepfake? Retrieved from https://au.pcmag.com/news/65869/what-is-a- deepfake

*Resource Overview:*

    This great post discusses the concept of a deepfake and provides examples. It is worth watching the video examples in the post as you read.

    Have fun while reading! The idea is to look at some extreme examples of deepfake that can be built using autoencoders. This should kick your brain into thinking outside of the box in relation to applications that could rely on autoencoders.

> *Status: ✅ Read + Reviewed — see [module07_notes.md](module-07-autoencoders/module07_notes.md)*

### Learning Activities

#### 1. Comparison
For this activity, you will compare linear factor models (see Module 6) and autoencoders in terms of their ability to reduce the dimensionality of input data.

In this Module, you learned that autoencoders reduce the dimensionality of input and then reconstruct the output from this representation. Previously, in Module 6, you learned about linear factor models and their ability to reduce dimensionality.

Given the above, do you think autoencoders offer you anything distinct from linear factor models?

Write a post critically analysing and answering the above question in your own words (your post should be no more than 150 words). Post your answer to the Module 7 discussion forum.

You should also read other students' posts and provide feedback.

> *Status: 🕐 To-Do* 

#### 2. Fake to Real
In this Module, you have learned that deepfake videos or audios are recordings that look and sound just like the original object or person. Certainly, it is very easy to think of many unethical applications of deepfake videos or audios. However, your challenge is to think of an ethical deep learning application using the deepfake concept that will do a world of good for its users.

Describe an application in your own words highlighting the relevant scientific and technical information (your post should be no more than 150 words). Post your answer to the Module 7 discussion forum.

Please read other students' posts and provide feedback.

> *Status: 🕐 To-Do* 

#### 3. Discussion Forum
Do you agree with this statement: 'Autoencoders may cause overfitting?'

Discuss your views with the class. Support your views with scientific and technical facts, examples or references.

> *Status: 🕐 To-Do* 

---

## Module 8 - Recurrent Neural Networks and Long Short-Term Memory

### TLDR
- **RNNs process sequences** by reusing the *same* weights at every time step (**parameter sharing across time**), so one network handles variable-length inputs and generalises a pattern wherever it appears. The hidden state `h(t)` is a **lossy summary** of everything seen so far.
- **They are hard to train.** Unrolled through time, backprop (**BPTT**) multiplies by the same weight matrix repeatedly, so gradients **vanish** (eigenvalues < 1) or **explode** (eigenvalues > 1). Plain-SGD RNNs fail beyond ~10-20 steps (Goodfellow et al. 2016, §10.7; Bengio et al. 1994).
- **LSTM fixes this** with a gated **linear self-loop** (the cell state) plus three gates - **forget / input / output** - that let the network *learn* what to remember. **GRU** is the leaner 2-gate cousin. **Gradient clipping** tames the exploding half.
- **CNN vs RNN:** CNN shares weights across *space* (grids/images, translation-invariant); RNN shares across *time* (sequences, order-sensitive). Combine them for image captioning (CNN encoder → LSTM decoder).
- **Applied evidence** (Laib et al. 2019, *Energy* 177, p. 540): per-cluster LSTMs beat MLP/SARIMAX/MLR baselines on day-ahead gas forecasting (weighted-average test MAPE 5.48%), especially on irregular days.
- Detailed source notes: [module08_notes.md](module-08-rnn-lstm/module08_notes.md).

### Introduction
Recurrent neural networks (RNNs) are a class of neural networks that allow previous outputs to be used as inputs while having hidden states. An RNN is a type of neural network that is designed to capture information from sequences or time-series data. Its ability to do this is perhaps one of the most notable attributes of an RNN. Unlike RNNs, traditional feed forward neural networks are designed for fixed sized input and fixed sized output.

The applications of RNNs are extremely versatile and may range from speech recognition applications to driverless cars. One can imagine that RNNs will be able to generate full-on music very easily in the near future without any human input.

Typically, RNNs are extremely difficult networks to train. This is where Long Short-Term Memory (LSTM) networks come into play. LSTM networks are a modified version of RNNs that make it easier to remember past data in memory.

### Resources

#### 1. Recurrent Neural Networks and Long Short-Term Memory
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). Deep learning. Cambridge, MA: MIT Press. Retrieved from https://www.deeplearningbook.org/

*Resource Overview:*
    
    This book contains an introduction to a broad range of topics in DL, including its mathematical and conceptual background, the DL techniques used in industry and different research perspectives. This book will be used throughout all the DLE602 modules.

    Please read Chapter 10 for this Module. This chapter introduces you to RNNs and discusses an important variant of RNNs called LSTM. The main sections on the basics of RNNs and LSTM are '10.2: Recurrent Neural Networks' and '10.10: The Long Short-Term Memory and Other Gated RNNs'.

    Finally, read about other variants of RNNs in this Chapter, as they all have their unique features.

> *Status: ✅ Read + Reviewed — see [module08_notes.md](module-08-rnn-lstm/module08_notes.md)*

#### 2. Recurrent Neural Networks
- Kelleher, J. D. (2019). Deep learning. Cambridge, MA: MIT Press. Retrieved from https://ebookcentral.proquest.com/lib/think/detail.action?docID=5855529

*Resource Overview:*
    
    This book contains an easy-to-read introduction on RNNs. The discussions start at the very basic level and build on top of that with examples.

    Please read Chapter 5 for this Module. For this Module, you simply need to read the Recurrent Neural Networks section of the chapter.

> *Status: ✅ Read + Reviewed — see [module08_notes.md](module-08-rnn-lstm/module08_notes.md)*

#### 3. Toward Efficient Energy Systems Based on Natural Gas Consumption Prediction with Long Short-Term Memory Recurrent Neural Networks
- Laib, O., Khadir, T, M. & Mihaylova, L. (2019). Toward efficient energy systems based on natural gas consumption prediction with LSTM recurrent neural networks. Energy, 177, 530–542. https://doi.org/10.1016/j.energy.2019.04.075

*Resource Overview:*
    
    One of the main focuses of this research paper was to find suitable forecasting methods for the effective management of energy resources. To do this, LSTM models are proposed that can efficiently predict natural gas consumption.

    Having read this paper, you should have a good understanding of the applications of RNNs and LSTM. Some of the implementations in this paper may seem complex but a basic understanding at this stage is fine.

> *Status: ✅ Read + Reviewed — see [module08_notes.md](module-08-rnn-lstm/module08_notes.md)*

#### 4. Understanding RNN and LSTM
- Mittal, A. (2019, 12 October). Understanding RNN and LSTM. Retrieved from https://towardsdatascience.com/understanding-rnn-and-lstm-f7cdf6dfc14e

*Resource Overview:*
    
    A short, accessible blog primer (~4 minutes) that introduces RNNs as feedforward networks with an internal memory, then walks through the vanishing/exploding-gradient problem and how LSTM's three gates (input, forget, output) address it.

    Use it as a fast vocabulary and intuition refresher before the heavier Goodfellow and Kelleher readings. It is background material, not an academic source to cite in submissions.

> *Status: ✅ Read + Reviewed — see [module08_notes.md](module-08-rnn-lstm/module08_notes.md)*

### Learning Activities

#### 1. Comparison
For this activity, you will compare convolutional neural networks (CNNs) and RNNs.
- First, explain what the most important difference is between the two above-mentioned networks as per your understanding.
- Second, explain whether there is a situation in which you might still prefer CNNs to RNNs.

Post your responses to the Module 8 discussion forum. Please read other students’ posts and provide feedback.

> *Status: 🕐 To-Do*

#### 2. What Do You Think?
This activity requires you to look deep into RNNs and LSTM models.

In this Module, you learned that LSTM models are expected to produce better outcomes than RNNs. Do you agree?
- If no, provide your justification.
- If yes, explain why LSTM models produce better accuracy than RNNs?
Your post should be written in your own words and be no more than 100 words. Post your answer to the Module 8 discussion forum.

Please read other students’ posts and provide feedback.

> *Status: 🕐 To-Do*

#### 3. Applications
It is always a good idea to think of applications for any neural networks. As part of this activity, you are asked to think of suitable applications for RNNs.

Throughout this subject, we have been highlighting applications in the field of natural language processing, speech recognition and computer vision. Are RNNs better suited to any of these applications (i.e., natural language processing, speech recognition or computer vision)?

Present your views verbally to the class. Back your views with scientific and technical facts, examples or references.

Please listen to other students and join in the conversation.

> *Status: 🕐 To-Do*

---

```bash
--- PLACEHOLDER:
## Module X - ...
### TLDR
### Introduction
### Resources
### Learning Activities

--- STATUS
# *Status: 🕐 To-Do*                <--- starting point
# *Status: ✅ Watched + Reviewed*   <--- for video resources
# *Status: ✅ Read + Reviewed*      <--- for articles, papers, chapters
# *Status: ✅ Done*                 <--- for activities
```
