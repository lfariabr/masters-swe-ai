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

> *Status: 🕐 To-Do*  

#### 2. Convolutional and Recurrent Neural Networks
- Kelleher, J. D. (2019). Deep learning. Cambridge, MA: MIT Press. Retrieved from https://ebookcentral-proquest-com.torrens.idm.oclc.org/lib/think/reader.action?docID=5855529&ppg=173

*Resource Overview:*

    This book contains an easy to read introduction to CNNs. The discussion starts at a very basic level and builds from there with examples.

    Please read Chapter 5 for this Module. If necessary, you can read Chapter 4 to refresh your memory before jumping into the details of CNN. For this Module, you only need to read the CNN section of the chapter.

    Pay special attention to the different CNNs developed over the past decade, such as AlexNet and ResNet.

> *Status: 🕐 To-Do*  

#### 3. Neural Networks and Convolutional Neural Networks Essential Training
- Fernandes, J. (2018). Neural networks and convolutional neural networks essential training [Video file]. Retrieved from https://www.linkedin.com/learning/neural-networks-and-convolutional-neural-networks-essential-training/convolutions?u=56744473

*Resource Overview:*

    This LinkedIn Learning course is a great resource that will ease anyone into the world of CNNs.

    You may wish to view all the short videos from Chapters 1 to 5; however, pay special attention to ‘Chapter 4: Convolutional Neural Networks’ and ‘Chapter 5: Convolutional Neural Networks in Keras’.

> *Status: 🕐 To-Do*  

#### 4. A Review of Popular Deep Learning Architectures: AlexNet, VGG16 and GoogleNet
- Kumara, V. (2020). A review of popular deep learning architectures: AlexNet, VGG16 and GoogleNet [Web log post]. Retrieved from https://blog.paperspace.com/popular-deep-learning-architectures-alexnet-vgg-googlenet/

*Resource Overview:*

    This great blog post discusses different types of popular DL architectures.

    It is important to pay attention to the relationship between these architectures and CNNs, as this will help you implement any project that involves such architectures. Additionally, pay special attention to the unique value proposition of each architecture.

> *Status: 🕐 To-Do*  

#### 5. CNNs, Part 2: Training a Convolutional Neural Network
- Zhou, V. (2019). CNNs, Part 2: training a convolutional neural network [Web log post]. Retrieved from https://victorzhou.com/blog/intro-to-cnns-part-2

*Resource Overview:*

    This great blog post discusses how to train a CNN.

    It is good to have sound ideas on how to train a network before putting your network into practise. Pay special attention to the Python codes shared in the post, as these will help you to better understand how to implement such codes in your final assessment.

> *Status: 🕐 To-Do*  

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
