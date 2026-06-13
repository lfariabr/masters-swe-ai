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

> *Status: 🕐 To-Do*

#### 2. Deep Convolution Neural Networks for Twitter Sentiment Analysis
- Zhao, J., Gui, X. & Zhang, X. (2018). Deep convolution neural networks for Twitter sentiment analysis. IEEE Access, 6, 23253–23260. Retrieved from https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8244338

*Resource Overview:*

    This research paper demonstrates how to use deep learning models to analyse a Twitter dataset to better understand the sentiments hidden among all the tweets. It is a great example of research work for NLP.

    You must refer to this paper for Assessment 1. It is important that you understand the deep learning practices in this paper independent of the dataset. It is essential that you are able to apply these deep learning practices to other datasets (e.g., Facebook or LinkedIn datasets) and obtain similar results.

> *Status: 🕐 To-Do*

#### 3. Audio-Visual Speech Recognition using Deep Learning
- Noda, K., Yamaguchi, Y., Nakadai, K., Okuno, H. G. & Ogata, T. (2015). Audio-visual speech recognition using deep learning. Applied Intelligence, 42(4), 722–737. Retrieved from https://search-proquest-com.torrens.idm.oclc.org/docview/1674443602?OpenUrlRefId=info:xri/sid:wcdiscovery&accountid=176901

*Resource Overview:*

    This research paper demonstrates how deep neural networks can be effectively used for speech recognition applications. It is a great example of research work for the speech recognition branch of deep learning. Perhaps the most interesting part of this paper is how the proposed model addresses the noise problem that arises in every speech recognition application.

> *Status: 🕐 To-Do*

### Learning Activities

#### 1. Interactive Knowledge Sharing - Natural Language Processing
Step 1: Think of an exciting NLP application that is important to you and that you believe that will have a wider impact on society.

Step 2: Propose and discuss the deep learning algorithms, datasets, models and other factors that you may have to consider for this application with the class.

Step 3: Put together a flowchart in a Word document on how all the considered elements in Step 2 will come together. Clearly show the input and output, all the critical decision points, the processes that will take place in the middle and any possible errors that may occur in the process flow.

Post your flowchart to the Module 3 discussion forum.

> *Status: 🕐 To-Do*

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
