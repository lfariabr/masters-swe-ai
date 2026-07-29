[00:00:02] Okay, so I'm a slightly scared cuz I
[00:00:03] clicked on the Flock Life program and
[00:00:07] then I saw that the Okay, the first
[00:00:08] speaker there was me. So,
[00:00:11] uh
[00:00:12] Okay, well, I'm I'm happy to be the
[00:00:13] first speaker in a flock. Um so, I
[00:00:15] should say that uh so, this this is a a
[00:00:17] course in computational learning theory.
[00:00:19] I'm not a learning theorist. So, I'm
[00:00:21] coming at this from the side of logic. I
[00:00:23] work in logic and verification.
[00:00:25] So, if you're in core learning theory,
[00:00:28] you may find this presentation slightly
[00:00:30] idiosyncratic, but
[00:00:32] I I want to emphasize the connections
[00:00:34] with logic and verification.
[00:00:38] Okay, so if you have been living under a
[00:00:41] rock in the last 10 years, you may not
[00:00:43] have heard of this thing called machine
[00:00:44] learning,
[00:00:45] but
[00:00:46] um
[00:00:47] you know, it's well known now and the
[00:00:49] the kind of guiding idea is to have a
[00:00:52] computer solve problems
[00:00:54] by learning from data rather than being
[00:00:56] explicitly programmed. So, if you have
[00:00:58] lots of data
[00:00:59] and if your task is hard to explicitly
[00:01:02] program, then maybe machine learning is
[00:01:04] is the thing for you.
[00:01:06] And there are kind of headline
[00:01:08] successes. So, one such such such
[00:01:11] success
[00:01:13] is the
[00:01:14] ability to predict
[00:01:17] how people will rate movies based on
[00:01:20] their past ratings.
[00:01:21] And sometimes without even knowing any
[00:01:24] without even having any semantic tagging
[00:01:26] of what kind of movie a
[00:01:29] given film is about.
[00:01:33] Another notable success is in game
[00:01:35] playing. So, machine learning systems
[00:01:38] are at the level of the most advanced
[00:01:41] dedicated chess engines. And you know,
[00:01:45] the the machine learning systems have
[00:01:46] been trained either on databases of
[00:01:49] chess games or even by self-play.
[00:01:55] So, those are the kind of ripped from
[00:01:56] the headlines kind of successes of
[00:01:58] machine learning.
[00:02:00] In this talk, it I'm going to be really
[00:02:02] really specific. I'm going to focus on a
[00:02:04] very very narrow subset of machine
[00:02:07] learning. So, but I just like to start
[00:02:09] by just surveying some of the areas and
[00:02:11] I guess you'll see some of them this
[00:02:13] week. So, what will be interested in in
[00:02:15] this talk is just classification. So,
[00:02:17] this is the problem where you've got a
[00:02:19] bunch of data items and you want to
[00:02:20] assign them to a class. So, you might
[00:02:22] have a bunch of newspaper articles and
[00:02:24] you might want to say, "Is this an
[00:02:25] article about events, sports, politics,
[00:02:28] entertainment, business, or or or else?"
[00:02:30] Just by looking at the article, maybe
[00:02:31] counting the the number of occurrences
[00:02:33] of certain words.
[00:02:35] So, something we'll not talk about is
[00:02:36] regression, where you want to predict a
[00:02:38] a numerical value for each data item
[00:02:40] rather than a discrete class,
[00:02:42] a numerical
[00:02:44] value like the price of a stock. So,
[00:02:46] we'll say nothing about that. We'll say
[00:02:47] nothing about clustering. So,
[00:02:50] um
[00:02:51] you've got some So, this is kind of
[00:02:52] unsupervised learning. You've got
[00:02:55] a bunch of
[00:02:56] data items, maybe users in a social
[00:02:58] network, and you want to group them
[00:02:59] together in natural ways. So, nothing
[00:03:02] about that and nothing also about
[00:03:04] ranking. So, uh ordering results of a
[00:03:07] search query by relevance to a
[00:03:09] particular user as an example. So, this
[00:03:12] talk classification all the way. And
[00:03:15] this is kind of natural in logic because
[00:03:17] what is a formula therefore to classify
[00:03:20] some some some
[00:03:22] elements as true or false.
[00:03:25] Okay. So, um the title of the talk is
[00:03:28] learning theory.
[00:03:30] So, you've got these kind of very sexy
[00:03:33] applications of machine learning and
[00:03:34] underneath you've got these
[00:03:36] uh learning theorists and what are they
[00:03:38] doing? Well,
[00:03:40] ideally, the goal of learning theory is
[00:03:43] to help us kind of analyze formal Well,
[00:03:46] develop formal models, analyze them, and
[00:03:48] and provide some kind of guarantees for
[00:03:49] the the learning algorithm. So,
[00:03:52] you know, what can we hope to learn
[00:03:54] efficiently? How much data do we do we
[00:03:56] need? And how much computational power
[00:03:59] do we need to to achieve the kind of
[00:04:01] goals that we want in machine learning?
[00:04:04] And it's great if we can do things, but
[00:04:05] it's even better if we have some kind of
[00:04:07] guarantees that our learning algorithm
[00:04:10] on the performance of our learning
[00:04:12] algorithm.
[00:04:13] And also to understand,
[00:04:15] you know, which algorithms to deploy in
[00:04:17] in which situation.
[00:04:20] So, as I say, I mean, this is a kind of
[00:04:23] general series of set of goals for for
[00:04:25] learning theory, but what I'm
[00:04:26] particularly concerned with is
[00:04:28] connections with logic and verification.
[00:04:32] Okay, so just a a quick overview of this
[00:04:34] mini course. I have 3 hours. I'm going
[00:04:36] to I think probably 1 and 1/2 hours is a
[00:04:38] bit of a stretch for continuous
[00:04:40] lectures, so I'll probably break in the
[00:04:42] middle briefly. Um
[00:04:45] Well, what is the overview? So, I'm
[00:04:47] really going to focus very narrowly on
[00:04:49] this classical, probably PAC learning
[00:04:51] model, probably approximately correct.
[00:04:54] So, this is goes back to Valiant in the
[00:04:56] '80s.
[00:04:57] I want to talk about VC dimension
[00:05:00] uh
[00:05:01] as a characterization of PAC
[00:05:03] learnability. And I'll give some
[00:05:04] examples particularly in connection with
[00:05:07] logic, logical formulas, and say with
[00:05:09] applications to to computing VC
[00:05:11] dimension of neural nets.
[00:05:13] I want to present this classic kind of
[00:05:15] fundamental result that finite VC
[00:05:17] dimension is equivalent to PAC
[00:05:19] learnability. So, this is a
[00:05:20] characterization of learnable classes.
[00:05:23] So, this is all very fundamental and
[00:05:25] classical. One thing that's maybe a
[00:05:27] little bit more closer to the frontiers
[00:05:29] of research is I want to talk about
[00:05:31] sample compression schemes and the
[00:05:33] Littlestone-Warmuth conjecture. So, this
[00:05:36] is another characterization of PAC
[00:05:38] learnability and with very nice
[00:05:40] connections with to to logic.
[00:05:43] And well, I want to talk about concept
[00:05:46] classes that are hard to learn. Time
[00:05:47] permitting means there won't be any
[00:05:49] time, so I'm pretty sure I'll have no
[00:05:50] time for that. And lastly, I want to
[00:05:53] talk about learning with membership
[00:05:54] queries. So, it's a particularly
[00:05:56] learning automata, which is I think a
[00:05:57] thing where in verification
[00:06:00] seems to be a particular interest in
[00:06:02] verification this angle Angluin model of
[00:06:05] learning with automata. So, I should
[00:06:07] also say that I have LaTeX lecture notes
[00:06:10] for this course. They're not actually
[00:06:13] online yet because as I was preparing my
[00:06:16] my handwritten lecture notes, I saw some
[00:06:17] howlers that need to be fixed, but
[00:06:21] either today or tomorrow I'll I'll
[00:06:24] I'll distribute these, so I'll put them
[00:06:26] on the web.
[00:06:28] Okay, so
[00:06:30] let me begin by talking about the PAC
[00:06:34] model.
[00:06:35] So,
[00:06:37] uh
[00:06:38] So, learning problem is in this model is
[00:06:41] specified by an input space X and the
[00:06:43] concept class, which is a class of
[00:06:46] functions from X to 0 1. So, as I said,
[00:06:48] we're looking just at classification and
[00:06:50] here even more simply, we want to
[00:06:52] classify things as a 0 or 1.
[00:06:57] So, I'll give an example in a second.
[00:06:59] That's a problem. An instance of a
[00:07:00] problem is determined by an unknown
[00:07:03] distribution on the input space and a
[00:07:05] target concept. So, the target concept
[00:07:07] is what we're trying to learn
[00:07:09] and the distribution is governing the
[00:07:12] distribution on examples that we can
[00:07:14] draw. So, the idea is to to learn this
[00:07:16] target concept, what we're going to do
[00:07:18] is we're going to draw a training sample
[00:07:20] of size M. So, S is a sequence of
[00:07:22] elements from the input set of size M
[00:07:24] and we draw and we take these
[00:07:26] independently identically distributed
[00:07:28] from M from D.
[00:07:31] And so, our target is seeing what we
[00:07:34] what the output of the learning
[00:07:36] algorithm is is a hypothesis. So, the
[00:07:38] hypothesis is a function
[00:07:41] from the input space to 0 1. And what is
[00:07:44] our goal? Our goal is it should be
[00:07:47] approximately correct. So, we define the
[00:07:49] error of our hypothesis as the
[00:07:52] probability
[00:07:53] if I draw an input from D that the
[00:07:56] hypothesis misclassifies the input uh
[00:08:00] relative to the target. And we want that
[00:08:02] that error be small.
[00:08:04] That's our goal.
[00:08:06] So, um
[00:08:08] this is the basic setup of the the PAC
[00:08:10] model. So, here's a
[00:08:12] an example. So, spam filtering.
[00:08:14] So, this is classif- classification
[00:08:16] problem. You have an email. Either it's
[00:08:17] spam or it's not spam. So, it's a 0 1
[00:08:19] classif- classification problem. Here
[00:08:21] Here are three example emails with their
[00:08:24] their classification. So, there is a
[00:08:26] target function. So, the target function
[00:08:28] is this ideal platonic judgment about
[00:08:30] whether an
[00:08:31] an email is spam or not. And here, the
[00:08:34] first one is not spam. I think this was
[00:08:37] a real email actually.
[00:08:38] Uh I think they're all real emails
[00:08:40] actually. Yeah. So,
[00:08:41] from my inbox back in the day.
[00:08:44] Uh
[00:08:44] this one's not spam. This is spam. And
[00:08:47] this is the one so we some somehow the
[00:08:49] first two are training examples and we
[00:08:50] want to classify the third
[00:08:52] email. Is it spam or not? That's our
[00:08:55] our um
[00:08:56] our task.
[00:08:58] So, as if we want to encode this as a
[00:09:00] learning problem, how are we going to do
[00:09:02] this? So, an email is is a body of text.
[00:09:04] But one thing we might um
[00:09:06] do is identify some features of the
[00:09:08] email and try and judge whether or not
[00:09:10] it's spam based on these features. So,
[00:09:12] the features The features could be
[00:09:13] whether it has bad spelling, yes or no.
[00:09:16] Does it come with an attachment? Does it
[00:09:18] contain my name? Ben. So, so any people
[00:09:21] who know me well would know to call me
[00:09:22] Ben. Does it contain the word Viagra?
[00:09:24] And then there's the the the judgment,
[00:09:27] is it spam or not?
[00:09:29] So, in the context of the model I was
[00:09:31] just presenting to you, there's an input
[00:09:33] space which is the space of features.
[00:09:35] So, here it's 0 1 to the 4. So, every
[00:09:38] email is represented as a 4-tuple, and
[00:09:40] that's my input. And then I have to
[00:09:42] judge based on that, is it spam or not?
[00:09:45] So, the concept class here is part of
[00:09:48] the learning problem. I have to tell you
[00:09:49] what it is. So, what are the rules that
[00:09:51] I'm going to use to judge whether or not
[00:09:53] an email is spam?
[00:09:55] So, I'm going to choose the concept
[00:09:57] class here of so-called linear
[00:09:59] classifiers. So, here's a linear
[00:10:01] classifier.
[00:10:02] Um, it's a weighted combination of these
[00:10:05] feature vectors. So, if it has a bad
[00:10:08] spelling, then I give it weight two.
[00:10:10] If it contains my name, then I give it
[00:10:13] weight minus three. And if it contains
[00:10:15] Viagra, I give it weight one. And then I
[00:10:16] ask, if it exceeds the threshold two,
[00:10:18] then it's spam. So, that's a linear
[00:10:20] classifier, and the concept class here C
[00:10:24] is the class of all linear classifiers.
[00:10:26] So, what I want is so my my idea is that
[00:10:29] the target
[00:10:31] here is a linear classifier that I want
[00:10:33] to learn.
[00:10:35] So, let's say formally what the
[00:10:39] Well, I should say here that Okay, so in
[00:10:41] this
[00:10:42] in this example, there's a distribution
[00:10:44] on emails. That's the distribution of
[00:10:46] nature. And
[00:10:48] I want to learn a linear classifier
[00:10:51] that's going to classify future So, from
[00:10:53] this data here, I want to learn a linear
[00:10:56] classifier that's going to classify any
[00:10:58] new emails I receive as to whether or
[00:11:00] not they're spam.
[00:11:02] So, let me formally define the model,
[00:11:04] the PAC model.
[00:11:07] So, we're given a target concept that we
[00:11:09] want to learn, and it's in our concept
[00:11:11] class, which is
[00:11:13] part of the learning problem.
[00:11:16] And I'm going to introduce some
[00:11:17] notation. So, LCM is going to be the the
[00:11:20] collection of labeled samples. So, this
[00:11:23] is the data I draw is are going to be
[00:11:25] labeled samples. So, S here is a set of
[00:11:28] inputs, and S comes
[00:11:32] equipped with the label. So, uh the
[00:11:35] target concept is used to label the
[00:11:36] input. So, I've got a bunch of emails
[00:11:38] and they're labeled according to the
[00:11:39] target concept. Are they spam or not?
[00:11:42] And that's what I want to learn from.
[00:11:45] So, we say that the concept class C is
[00:11:48] PAC learnable
[00:11:50] with sample complexity M,
[00:11:53] accuracy epsilon, and confidence delta
[00:11:57] if there is a learning map such that So,
[00:12:00] what does this learning map do?
[00:12:02] It takes as input a sample of size M
[00:12:06] from the input space. So,
[00:12:09] the input looks like this. So,
[00:12:13] the input the learning map. So, let S
[00:12:21] So, here's a set of emails that I've
[00:12:22] just received and each email is
[00:12:23] represented as a feature vector. So,
[00:12:25] this is one email, second email.
[00:12:28] And they're labeled according
[00:12:30] for training, they're labeled according
[00:12:32] to the target concept. So, the
[00:12:35] they're labeled according to whether
[00:12:36] they're spam or not.
[00:12:40] So, that's my training data.
[00:12:42] And I say that this this if this class
[00:12:44] is PAC learnable, there's a function
[00:12:46] that uh
[00:12:47] operates on this training data and gives
[00:12:49] me
[00:12:53] a classification function as output. So,
[00:12:55] what I'm learning is this classification
[00:12:57] function. And what do I want from this?
[00:13:03] Okay. So, for any target concept,
[00:13:06] so this learning function is is
[00:13:08] monolithic. For every every target
[00:13:10] concept, I want
[00:13:12] um So, this is a mouthful. The
[00:13:14] probability over my training data. So,
[00:13:17] my training data is
[00:13:20] a set of emails of size M sample set of
[00:13:23] size M. So, S is distributed uh, from D
[00:13:26] to the M. and I want the probability
[00:13:28] that the error of the learned
[00:13:30] hypothesis, so here is the learned
[00:13:32] hypothesis, so the learning map applied
[00:13:34] to the training data,
[00:13:36] I want that this error be less than or
[00:13:38] equal to epsilon, and I want that the
[00:13:39] probability of this happening,
[00:13:41] um, uh, be uh, at least 1 minus delta.
[00:13:45] So, there are two parameters here, delta
[00:13:47] and epsilon. So, delta is the the, um,
[00:13:50] confidence. So, the idea is that one, if
[00:13:54] my training set is very, uh,
[00:13:57] unrepresentative of the true
[00:13:58] distribution, then I'm never going to
[00:14:00] learn, my learning function is going to
[00:14:01] be useless, and this is the delta here.
[00:14:05] Okay, but if the training set is good,
[00:14:07] then I can learn a function with error
[00:14:09] less than epsilon.
[00:14:11] So, are there any questions at this
[00:14:13] stage? So, this is a complex definition,
[00:14:15] yeah. Um, you you mentioned the word
[00:14:17] distribution, and sorry,
[00:14:20] what does distribution mean? Aha, okay,
[00:14:22] good question. So, uh, it's a
[00:14:24] probability distribution on, uh, the
[00:14:27] inputs, uh, input space here. So,
[00:14:31] uh, and let's assume that the input
[00:14:33] space is discrete, so I'm assigning a
[00:14:35] probability to every element. Okay, so
[00:14:38] it's a uh,
[00:14:39] uh, helpful question. I'm assigning a a
[00:14:42] probability to every element such that
[00:14:44] it it adds up to one. So, in general, of
[00:14:46] course, I I I'll be considering input
[00:14:47] spaces that are, uh,
[00:14:49] R N, and yeah.
[00:14:51] Uh, we'll take questions at the end of
[00:14:53] the lecture, I forgot to say that
[00:14:55] because of the video recording. Ah. So,
[00:14:57] sorry for the interruption. Uh, so there
[00:14:59] is there is a Slack channel that people
[00:15:01] can sign up for. You can put questions
[00:15:03] in there during the talk, I'll collect
[00:15:05] them for the end
[00:15:06] as well. Aha, okay, so I have I have
[00:15:08] some questions in the talk, but, um,
[00:15:10] I'll I'll answer I'll self-answer.
[00:15:13] Uh,
[00:15:14] okay, um,
[00:15:16] yeah.
[00:15:17] Okay, so, uh, let me then continue.
[00:15:22] Okay, so remarks on this definition. So,
[00:15:24] first of all,
[00:15:25] in terms of learning theory, this is
[00:15:26] very this is very idealistic. So, I'm
[00:15:28] assuming we're trying to learn a target
[00:15:30] concept. So, out there there's a target
[00:15:32] concept we're trying to learn. So, of
[00:15:33] course, if you're doing real learning,
[00:15:36] it's not the case you're trying to learn
[00:15:37] whether an image is an image of a cat or
[00:15:39] not.
[00:15:40] I mean, there's no perfect answer to
[00:15:42] that question. There's no target
[00:15:43] concept. And for sure that target
[00:15:45] concept, if there is one, it's not a
[00:15:47] linear classifier or even a neural net
[00:15:49] of a certain depth and with a certain
[00:15:51] number of neurons.
[00:15:53] So, what this means in learning theory
[00:15:55] jargon is we're working in the
[00:15:56] realizable setting rather than the
[00:15:57] agnostic setting. So, it's like we're
[00:15:59] trying to interpolate from a known class
[00:16:00] of functions. So, this is somehow
[00:16:03] mathematically quite nice, but
[00:16:05] slightly unrealistic.
[00:16:07] And as a consequence of the fact we're
[00:16:09] working in this realizable setting,
[00:16:11] there are whole host of issues that I'm
[00:16:12] I won't say anything about. So, for
[00:16:14] instance, model selection. So, the first
[00:16:16] thing you do when you have a learning
[00:16:17] problem is you think, well, what are the
[00:16:19] class of functions I'm going to use to
[00:16:21] try and and and do this solve this
[00:16:23] problem. Am I Am I going to use support
[00:16:25] vector machines? Am I going to use
[00:16:26] neural nets? And here
[00:16:29] we're assuming there's a a concept class
[00:16:31] is given. So,
[00:16:33] um and so there's a whole bunch of
[00:16:35] issues that we gloss over.
[00:16:39] So, I want to emphasize this
[00:16:41] this definition of PAC learnability is
[00:16:43] very strong. It says it's essentially
[00:16:46] that
[00:16:47] uh for learning a concept class, and
[00:16:49] I'll give another example in a second,
[00:16:51] I want to be able to learn it with a
[00:16:53] given number of of um examples, which
[00:16:56] only depends on this accuracy epsilon
[00:16:59] and confidence delta, but is independent
[00:17:02] of the probability distribution on the
[00:17:04] examples. So, it may be that actually,
[00:17:07] if I knew the distribution, then I
[00:17:08] could, you know, I could do better and
[00:17:10] this model is too uh pessimistic.
[00:17:14] The next point is the definition allows
[00:17:16] for improper uh learning. So, the
[00:17:19] definition I gave said nothing about the
[00:17:21] form or representation of the
[00:17:22] hypothesis. So, I've got a target class
[00:17:25] of concepts that I'm trying to learn,
[00:17:27] say linear classifiers, but I allow the
[00:17:29] learner to output a function in any
[00:17:31] representation at all.
[00:17:35] And the second thing is
[00:17:37] PAC learning. So, I I've heard one
[00:17:39] criticism say that PAC learning
[00:17:41] describes
[00:17:42] an undergraduate who's who's trying to
[00:17:44] learn for an exam by looking at past
[00:17:47] papers. So, the undergraduate maybe is
[00:17:49] not trying to understand the core
[00:17:51] concepts of physics, is just trying to
[00:17:53] predict what's going to come up on the
[00:17:54] next exam and and get the right answer.
[00:17:58] So, um
[00:17:59] as kind of formulated there, PAC makes
[00:18:03] learning seem like a a problem of
[00:18:05] prediction, but as we'll see from the
[00:18:08] the the work on sample compression
[00:18:10] schemes, there are kind of equivalent
[00:18:12] characterizations which correspond to
[00:18:15] our idea of learning as a kind of form
[00:18:17] of
[00:18:18] compression.
[00:18:19] Uh but as it's
[00:18:21] formulated, there's no kind of
[00:18:23] appearance of Occam's razor, say.
[00:18:25] Okay, so because the definition is a bit
[00:18:27] of a mouthful, I want to give another
[00:18:29] example. And this is like the classic
[00:18:31] example of PAC learnability. So, here
[00:18:35] a learning problem, I said there's a
[00:18:36] there's a concept class. So, here what
[00:18:38] is the concept class?
[00:18:41] Well, there's an input space.
[00:18:43] So, here the input space is R2.
[00:18:46] So, these are the the the the inputs to
[00:18:48] the learning problem, and the concepts
[00:18:50] here is a collection of
[00:18:53] functions from R2
[00:18:57] to 0 1
[00:19:00] such that F is the characteristic
[00:19:02] function of a rectangle.
[00:19:09] Okay, so
[00:19:14] So, these are my concepts. My concepts
[00:19:16] are rectangles, so they're geometric
[00:19:17] concepts.
[00:19:19] And the And the red and blue dots here
[00:19:22] is a training sample that I've drawn.
[00:19:24] So, I had a distribution
[00:19:26] fixed and unknown, so I don't know this
[00:19:28] distribution, but I'm drawing from this
[00:19:29] distribution.
[00:19:32] This is a distribution on R2.
[00:19:35] And I draw some training examples, and
[00:19:37] this rectangle R here is the target.
[00:19:41] This is the thing I'm trying to learn. I
[00:19:42] don't know I can't I can see this
[00:19:43] rectangle
[00:19:45] here, but uh this is unknown, and I'm
[00:19:47] trying to learn it.
[00:19:48] The training samples are labeled
[00:19:50] according to the target. So, all I can
[00:19:52] see is this training set of blue and red
[00:19:55] dots. That's all I can see as a learner,
[00:19:56] and I'm trying to figure out what is the
[00:19:58] rectangle that I'm trying to learn. So,
[00:20:00] here's one uh kind of procedure I could
[00:20:03] I could take is I could say, "Well, let
[00:20:05] me look at the blue dots, which I know
[00:20:06] are marked as being inside the
[00:20:08] rectangle.
[00:20:09] And let me take the smallest rectangle
[00:20:11] that includes all the blue dots." So, as
[00:20:13] a learner, that's going to be my
[00:20:15] hypothesis. So, this is the rectangle RS
[00:20:18] here.
[00:20:21] And what I want to uh say is that this
[00:20:24] procedure here, if I take enough If my
[00:20:27] sample's big enough, I'm going to get an
[00:20:29] accurate hypothesis
[00:20:32] um with high probability over the
[00:20:34] sample.
[00:20:35] So, this is what I I want to give you a
[00:20:37] Now, a brief argument that what I've
[00:20:39] just described here is is a PAC learning
[00:20:41] function for a large enough sample.
[00:20:44] So, let's um
[00:20:46] uh look at uh So, this is our target
[00:20:49] rectangle that we want to learn.
[00:20:51] And let's mark off some uh regions,
[00:20:53] which I'm going to call border regions,
[00:20:55] such that their probability So, the
[00:20:58] probability here is the the probability
[00:21:01] of a point landing in the the rectangle
[00:21:03] under this distribution here. So, for
[00:21:05] instance, E1 is such that the
[00:21:07] probability of a point landing in this
[00:21:09] rectangle is epsilon over 4. So, epsilon
[00:21:13] here is the uh accuracy of that I want
[00:21:16] my hypothesis to have.
[00:21:18] So, this is my target accuracy, and I
[00:21:19] want to say how many samples do I need
[00:21:21] to achieve this accuracy? So, I mark off
[00:21:24] these four border regions um
[00:21:27] of my target rectangle with mass epsilon
[00:21:30] over 4.
[00:21:31] If my target rectangle doesn't have mass
[00:21:33] epsilon
[00:21:34] at least epsilon over 4, I won't be able
[00:21:36] to do this, but in this case, I need not
[00:21:39] worry. I'll output the empty hypothesis.
[00:21:42] Okay, so these these regions exist if
[00:21:44] the the measure is absolutely
[00:21:46] continuous.
[00:21:47] And um
[00:21:50] here's the question. Given epsilon
[00:21:52] greater than zero and delta greater than
[00:21:54] zero, how many samples are needed such
[00:21:57] that the error of my hypothesis
[00:21:59] rectangle, so my hypothesis is RS,
[00:22:02] this was the smallest rectangle that
[00:22:04] enclosed all the blue dots, all the the
[00:22:06] the positively labeled examples.
[00:22:09] So, how many samples are needed such
[00:22:11] that this error rectangle has uh area
[00:22:14] less than epsilon with probability at
[00:22:16] least 1 minus delta?
[00:22:18] So, this probability here, let me
[00:22:19] emphasize, is the probability over the
[00:22:21] random sample S. So, I draw a random
[00:22:24] sample, and um
[00:22:27] I I want I want this.
[00:22:29] And the idea is as follows.
[00:22:32] Um I mean
[00:22:34] what could go wrong in in my learning?
[00:22:37] Oops. Uh
[00:22:38] what could go wrong? Um
[00:22:40] it's clear that's uh
[00:22:44] Sorry. Oh. The the board. Okay, that's
[00:22:47] that's going to work.
[00:22:49] Yeah.
[00:22:50] Okay. Maybe actually when I turn again,
[00:22:53] magically, it will be clean. We'll see.
[00:22:55] Um
[00:22:57] Yeah. Aha, that's that's what I call
[00:22:59] learning. Um
[00:23:01] Also, don't forget greedy. That's
[00:23:03] generalization. Okay. Let's
[00:23:06] try this.
[00:23:08] This is optimism. Um
[00:23:11] Okay, I'm trying to learn
[00:23:14] Uh so, well,
[00:23:16] I've drawn some samples and I've
[00:23:18] observed that these guys
[00:23:20] are positively labeled and these guys
[00:23:22] are negatively labeled.
[00:23:25] And I think, ah, well, the hypothesis
[00:23:27] rectangle I I'm I'm going to learn is
[00:23:29] this one. So, it's the smallest one that
[00:23:30] contains all the samples.
[00:23:32] Um
[00:23:35] Uh
[00:23:36] But, it turns out I was unlucky because
[00:23:38] in fact, the true
[00:23:41] target
[00:23:42] was like this. This is actually the the
[00:23:44] con- target concept. It was just I was
[00:23:46] unlucky that the sample didn't didn't
[00:23:49] contain any points here, which would
[00:23:50] tell me to expand my hypothesis.
[00:23:53] So, I want to I want to upper bound this
[00:23:55] this probability. So, the error of my
[00:23:59] hypothesis is So, if my hypothesis were
[00:24:02] here and the target were here, the error
[00:24:04] is the is the area of this under the
[00:24:07] distribution D. The probability that a
[00:24:09] random point lands in here. So, this is
[00:24:11] my error.
[00:24:12] And I'm okay just as long So, my error
[00:24:16] is the probability of the the the the
[00:24:19] target minus the hypothesis. So, the
[00:24:20] hypothesis is always inside the target.
[00:24:23] And um
[00:24:25] I'm okay just as long as my uh sample
[00:24:28] hits all four border regions.
[00:24:30] Um so, if I go back to this picture
[00:24:32] here, imagine my sample I see a When I'm
[00:24:35] drawing my sample, I see a point in here
[00:24:38] in E1, in E2, in E3, in E4, then my
[00:24:41] hypothesis will be uh expanded to hit
[00:24:44] all four border regions, and the gap
[00:24:47] between my hypothesis and the target
[00:24:49] will have area less than epsilon over
[00:24:51] four.
[00:24:52] So, I'll be okay if I hit all four
[00:24:53] border regions.
[00:24:55] So, the question is, how many samples do
[00:24:57] I need
[00:24:58] uh to hit all four border regions with
[00:25:00] probability at least 1 minus delta? So,
[00:25:03] here, let me draw the border regions
[00:25:05] here.
[00:25:07] So, the idea is that if I have a sample,
[00:25:09] if I see a plus positive point here, a
[00:25:11] positive point here, a positive point
[00:25:13] here, a positive point here, then my
[00:25:15] hypothesis rectangle will be big enough
[00:25:17] so that the gap between it and the true
[00:25:20] uh the true target concept is less than
[00:25:22] epsilon.
[00:25:24] So, uh the bad event that I want to to
[00:25:27] to avoid is that my sample points, none
[00:25:30] of them hits uh
[00:25:32] well, one of the border regions is
[00:25:34] missed by by my sample points.
[00:25:37] So, the problem So, I'm going to draw M
[00:25:38] samples. The probability that all M
[00:25:40] samples miss the border region E1, which
[00:25:42] had
[00:25:43] uh mass epsilon over 4, is then 1 minus
[00:25:46] epsilon over 4 to the M. And here, we
[00:25:50] can just use the the most useful
[00:25:52] inequality
[00:25:54] that you'll ever come across.
[00:25:57] We'll use that. So, this is less than
[00:26:00] e to the minus
[00:26:01] epsilon M over 4.
[00:26:04] So, the probability that some border
[00:26:06] region E1, E2, E3, and E4 is missed by
[00:26:09] all M samples is four times that. That's
[00:26:11] just a union bound. So, probability of A
[00:26:14] or B is less than or equal to
[00:26:16] probability of A plus B.
[00:26:18] And then, the question is, how many
[00:26:20] samples do I need? So, what do I want?
[00:26:22] This is an estimate on the probability
[00:26:24] of the bad event. My sample doesn't fill
[00:26:28] the target rectangle enough, so I don't
[00:26:30] make my hypothesis big enough.
[00:26:32] Um
[00:26:33] So, and I want this to be less than
[00:26:35] delta. And to get for this to be true, I
[00:26:37] want my sample size to be at least 4
[00:26:40] over epsilon log 4 over delta. So, this
[00:26:42] is a
[00:26:43] uh quantity you'll see in in in in these
[00:26:46] generalization bounds. So, my sample
[00:26:49] This is Well, here's a sanity check. My
[00:26:51] sample should The sample size should
[00:26:53] depend on epsilon and delta. So, epsilon
[00:26:55] is the accuracy of my hypothesis and
[00:26:58] delta is the confidence
[00:27:00] that you know, so delta
[00:27:02] delta is the
[00:27:03] the probability that my learning
[00:27:06] procedure fails completely because I
[00:27:07] draw a bad sample. But as if my sample
[00:27:10] is big enough, then I'm okay. And this
[00:27:13] this is distribution independent. I
[00:27:15] didn't assume anything about the
[00:27:16] distribution.
[00:27:19] So, what this proves is that the class
[00:27:23] so the concept So, what have we proved?
[00:27:25] We've proved that the concept class of
[00:27:27] rectangles in R2, so axis-aligned
[00:27:30] rectangles, is PAC learnable. It admits
[00:27:34] a learning map. So, let's just be very
[00:27:36] explicit about that.
[00:27:39] What is the learning map? So, again,
[00:27:43] there exists
[00:27:45] So, for for every epsilon
[00:27:50] given epsilon and delta, there exists an
[00:27:52] M
[00:27:53] and a learning map H that takes
[00:27:56] labeled samples
[00:27:58] according to M
[00:28:00] and
[00:28:03] returns a function. So, here the
[00:28:05] learning map is actually is actually
[00:28:07] going to return a rectangle.
[00:28:09] This is a so-called proper learning map
[00:28:11] such that the probability
[00:28:13] over a sample that the error of H
[00:28:18] Well, let me just
[00:28:19] just write it's a
[00:28:21] Okay. So, probability over samples
[00:28:26] that if I apply the learning map
[00:28:29] to the
[00:28:30] sample
[00:28:31] um
[00:28:32] labeled by the target concept
[00:28:35] the probability that the
[00:28:39] Okay.
[00:28:41] My hand is going to get very blue by the
[00:28:43] end of this.
[00:28:44] The probability
[00:28:47] that the error of this
[00:28:50] is greater epsilon
[00:28:52] is less than delta.
[00:28:56] So, the probability of a sample is that
[00:28:57] my hypothesis has a bad error is less
[00:28:59] than delta.
[00:29:01] Okay, so
[00:29:03] a finite sample suffices
[00:29:05] and the
[00:29:06] the size of the sample is polynomial in
[00:29:08] one over epsilon and one over delta. And
[00:29:10] what is the learning map? It's just
[00:29:11] output the smallest consistent
[00:29:13] hypothesis. So, you're given this label
[00:29:15] sample, there is there's there is a
[00:29:17] consistent hypothesis, there's a a
[00:29:19] smallest rectangle that contains all the
[00:29:20] positive examples, and that's the
[00:29:22] learning map.
[00:29:24] Uh
[00:29:24] so, I
[00:29:25] I'm really not allowed to answer ask any
[00:29:27] questions? Is this
[00:29:29] uh
[00:29:32] I can ask and answer. I can ask my
[00:29:39] Aha, I see.
[00:29:41] uh
[00:29:44] Okay.
[00:29:45] I'm permitted rhetorical questions.
[00:29:46] Like, what am what am I doing here
[00:29:48] on a fine Sunday morning?
[00:29:50] Um okay.
[00:29:52] Yeah.
[00:29:56] Aha.
[00:29:57] Okay, sounds good. Any questions that
[00:29:59] you'd like me to repeat and then try and
[00:30:01] answer?
[00:30:04] Uh okay, so
[00:30:06] um
[00:30:07] yeah.
[00:30:08] Okay, so this this is there's a lot of
[00:30:10] quantifiers in the definition, but
[00:30:13] um
[00:30:14] So, um
[00:30:17] you've seen at least if if this lecture
[00:30:19] is the only part of learning theory
[00:30:21] you've seen, you've seen now one
[00:30:22] hypothesis class. That is the class of
[00:30:24] rectangles in the plane.
[00:30:26] So, in general, well, let's think of
[00:30:28] something a more expressive hypothesis
[00:30:31] class.
[00:30:32] So, there's the so-called perceptron.
[00:30:35] So, or or less colorfully, linear
[00:30:38] classifier. So, a linear classifier is a
[00:30:40] function from Rn to -1 +1 given as
[00:30:44] follows. So,
[00:30:46] F maps to +1 so there's a there's a
[00:30:48] given vector A and a constant B. F maps
[00:30:51] to +1 if AX is greater equal to B and -1
[00:30:55] otherwise. So, if you're viewing this as
[00:30:57] a set, it's a half a half space in the
[00:31:00] in in in Rn.
[00:31:02] So, F is saying, well, you map to +1 if
[00:31:04] you're one side of this hyperplane and
[00:31:06] -1 if you're another side of the
[00:31:08] hyperplane with normal
[00:31:10] A.
[00:31:12] And um
[00:31:14] So, given such a classifier, suppose I
[00:31:16] give you a
[00:31:18] a set of
[00:31:20] labeled data.
[00:31:22] So, I give you um
[00:31:23] Let me have a
[00:31:25] Maybe I'm going to use this.
[00:31:35] This one?
[00:31:37] Oh, okay. It was
[00:31:39] Oh, you're right. Okay.
[00:31:41] It was the pen. So, um
[00:31:46] Yeah.
[00:31:50] So, I I'm given them a bunch of points
[00:31:53] in the plane.
[00:31:56] So, I'm given So, this set here is a
[00:31:58] bunch of vectors labeled with plus or
[00:32:00] minus one and now now let's say we're in
[00:32:02] the plane.
[00:32:03] And I want to know, is this
[00:32:05] consistent with some linear classifier?
[00:32:11] So, is there a linear classifier that is
[00:32:13] actually consistent with this? Well, in
[00:32:15] this case there is. So, if I take this
[00:32:18] this this line that separates them,
[00:32:20] then the the linear classifier that says
[00:32:24] assign +1 to everything this side of the
[00:32:26] hyperplane and and -1 uh minus to the
[00:32:29] other side is is is is consistent with
[00:32:31] that. And you can formulate the So,
[00:32:34] given such a point, you can given such a
[00:32:36] set, you can formulate the exist
[00:32:38] deciding the existence of such a
[00:32:39] classifier as a linear program.
[00:32:42] Okay, so one important part of learning
[00:32:46] problem is is finding a consistent
[00:32:48] classifier. So in the case of the
[00:32:50] rectangles, what we found a consistent
[00:32:52] classifier very easily by by taking the
[00:32:54] smallest rectangle that contained all
[00:32:56] the positive points.
[00:32:58] It's not much harder. So in in the
[00:33:00] concept class of rectangles, it was very
[00:33:02] easy to find consistent classifiers.
[00:33:04] It's not much harder in this case,
[00:33:06] right? For linear classifiers.
[00:33:09] Um
[00:33:10] Okay, so if a consistent linear class
[00:33:12] classifier exists, then we say that S is
[00:33:14] linear separable.
[00:33:16] But um
[00:33:18] Um here's but of course
[00:33:21] this is a very kind of inexpressive
[00:33:25] class of classifiers. So but they can be
[00:33:28] combined into so-called neural nets. And
[00:33:31] and what's the idea here is well, we
[00:33:34] want to combine perceptrons. So
[00:33:37] given a set of points in in RD and let's
[00:33:40] say an arbitrary function from S to
[00:33:43] minus one,
[00:33:44] how can we realize so this should be
[00:33:46] capital F as a composition of perceptron
[00:33:49] perceptrons? So here's the situation.
[00:33:54] I um
[00:33:57] So perceptrons are somehow not
[00:33:59] expressive enough for what we want to
[00:34:01] do. So
[00:34:03] let's take again in the plane
[00:34:07] a set of points and they're labeled
[00:34:10] positively and negatively like this.
[00:34:13] And I want to build a classifier and I'm
[00:34:15] going to build a classifier as I've said
[00:34:17] as a combination of perceptrons. And
[00:34:20] what do I mean by this? I mean
[00:34:23] as follows that
[00:34:25] um
[00:34:27] I want to take my input.
[00:34:30] I want to feed it to
[00:34:32] some perceptrons.
[00:34:36] And I want to feed these perceptrons as
[00:34:38] an input to another perceptron, and I
[00:34:40] want the output to give me the
[00:34:42] classification.
[00:34:43] Okay?
[00:34:45] And well, here's one thing I can do. So,
[00:34:48] I can say take this positive point.
[00:34:54] And say, well, there's a half space here
[00:34:58] and a half space here.
[00:35:00] So,
[00:35:01] um if I say that this point is this
[00:35:03] point is uniquely um
[00:35:06] distinguished from all the others by
[00:35:07] saying it's on this side of this half
[00:35:09] space
[00:35:11] and it's on that side of that half
[00:35:13] space.
[00:35:14] So, if I have I can let me let the
[00:35:17] linear classifier here be
[00:35:19] F
[00:35:20] and this be G. We'll call this point X
[00:35:22] here.
[00:35:24] X1, let's say.
[00:35:26] Then X1 f of X1 plus
[00:35:30] uh g of X1.
[00:35:34] So, this linear classifier gives one for
[00:35:36] this point because it's on the right
[00:35:37] side of the the hyperplane. This one
[00:35:39] gives one for this point because it's on
[00:35:40] the right side of the hyperplane. So,
[00:35:41] this is equal to two.
[00:35:43] So, if I
[00:35:45] do this, then this is minus one plus
[00:35:48] this. So, this function on X1, or let me
[00:35:51] just say this is a function of X.
[00:35:53] This function here
[00:35:55] uh on this point gives one, but on all
[00:35:58] the other points uh
[00:35:59] gives um
[00:36:01] uh minus one. So, on all other points.
[00:36:03] So, if I then take the the sign of this,
[00:36:09] this is going to be plus one here and
[00:36:11] minus one on all the other points.
[00:36:14] Okay? So,
[00:36:15] um
[00:36:17] uh
[00:36:18] by combining uh classifiers like this, I
[00:36:22] can realize any um
[00:36:24] uh
[00:36:25] uh
[00:36:26] Well, so actually yeah. So, I could So,
[00:36:28] here's here's the function that's going
[00:36:30] to realize big F. So, um in fact, what
[00:36:33] I'm doing is I'm taking all the points
[00:36:34] that are positive that I want to be
[00:36:36] positively labeled.
[00:36:37] So, for each point, I pick a linear
[00:36:39] classifier
[00:36:41] like So, this would be
[00:36:43] this here Well, this is the F and G
[00:36:46] classifier that the the hyperplanes. So,
[00:36:48] I I include each point between two
[00:36:50] hyperplanes and have classifiers for
[00:36:52] each side.
[00:36:53] So, this is to the left and to the
[00:36:55] right. And then, this thing picks that
[00:36:58] uniquely gives plus one for the point
[00:37:00] that I'm interested in XI and and minus
[00:37:02] one for all other points. And then, I
[00:37:03] take the sign. So, what it So, what it's
[00:37:05] saying in in in in in jargon is that
[00:37:08] Well, this is defining a neural net. So,
[00:37:10] these these uh there are linear
[00:37:12] classifiers in this um intermediate
[00:37:14] level, which are these guys. So, there's
[00:37:17] one hidden so-called hidden layer. And
[00:37:20] there's the output, which is
[00:37:22] the value H and the inputs, which are
[00:37:24] these XI. So, by combining perceptrons
[00:37:27] in a graph like this, I can realize
[00:37:29] this arbitrary function on a finite set.
[00:37:32] And in fact, you can realize any
[00:37:33] continuous function on a compact set can
[00:37:36] be realized up to any accuracy by a
[00:37:40] neural net with um
[00:37:42] uh
[00:37:43] one hidden layer.
[00:37:45] So, what So, more formally, what is a
[00:37:46] neural net? So, it's a directed acyclic
[00:37:51] layered graph with inputs in RN and and
[00:37:53] output in 0 1.
[00:37:55] So, um
[00:37:58] Here's the picture.
[00:38:00] Um
[00:38:03] There are some input nodes
[00:38:06] uh and some intermediate nodes. And
[00:38:12] Each node in the net is computing a
[00:38:14] function. And this function is something
[00:38:17] like a linear classifier. So,
[00:38:20] um
[00:38:21] uh
[00:38:23] uh so, for each node, there are several
[00:38:25] inputs. So, here are the inputs. And
[00:38:29] um
[00:38:32] There's So, there's a weight. So, for
[00:38:34] instance, this node
[00:38:36] it has two inputs, and there's a weight
[00:38:39] assigned to each input. And to compute
[00:38:40] the value of this node, I take the the
[00:38:43] inputs, and I sum them according to
[00:38:45] these weights.
[00:38:47] I have a kind of threshold here, W0,
[00:38:49] which is another parameter I associate
[00:38:51] with this uh node. And then I apply
[00:38:54] sigma, so-called activation function.
[00:38:56] So, for linear classifiers, this is the
[00:38:58] sign function. You just say, is this Is
[00:39:00] this positive or negative? But you can
[00:39:02] choose other activation functions.
[00:39:04] And that gives you the output
[00:39:07] of this node. And that therefore, the
[00:39:09] node uh the the net computes a function.
[00:39:13] And uh so, what I described before, the
[00:39:16] the output was a uh the activation
[00:39:18] function was a step function. Just
[00:39:20] return one if the thing is positive and
[00:39:22] zero otherwise, or minus one otherwise.
[00:39:25] Now, in uh in some sense, this is not
[00:39:28] really used because the nets are hard to
[00:39:29] train with this uh step function. If you
[00:39:32] have uh uh uh activation function which
[00:39:35] um
[00:39:36] uh is differentiable, then you can train
[00:39:38] the the the nets by gradient descent.
[00:39:40] So, uh this this is uh preferred.
[00:39:44] But okay, so uh here's a an expressive
[00:39:47] class of of concepts that you might try
[00:39:49] and learn.
[00:39:50] Okay? And the question is, well, how
[00:39:52] many examples would you need to train
[00:39:54] the a neural net?
[00:39:56] So, there are two really There Well,
[00:39:57] there are two issues. There are, you
[00:39:58] know, how many examples do you need, and
[00:40:00] what's the computational complexity of
[00:40:02] finding a consistent classifier? So,
[00:40:04] back in the world of rectangles, finding
[00:40:06] a con- consistent classifier was
[00:40:08] completely trivial.
[00:40:09] Now, it's clear that if if if I give you
[00:40:11] a bunch of positively labeled and
[00:40:13] negative labeled examples and say,
[00:40:16] "Here's a neural net." So, I present you
[00:40:17] a graph
[00:40:18] and I say find a consistent classifier.
[00:40:20] What are you going to do? You're You're
[00:40:21] going to try and find the weights of the
[00:40:23] neural net that make it classify the
[00:40:25] positive and negative examples exactly,
[00:40:28] then this uh is
[00:40:30] a difficult problem.
[00:40:32] So, the following problem is NP-hard.
[00:40:34] So, you're given a feedforward neural
[00:40:36] network. So, this is just a graph with D
[00:40:39] inputs and a single hidden layer with
[00:40:41] three neurons. So, here's the
[00:40:44] Here's the the situation. You've got D
[00:40:46] inputs.
[00:40:49] And this hidden layer is is
[00:40:51] um
[00:40:54] three neurons here. So, it's it's fully
[00:40:56] connected here.
[00:40:58] And uh what you have to do to train it
[00:41:01] is choose the weights. So, choose the
[00:41:03] weights
[00:41:05] of all these edges and the threshold
[00:41:07] weights of the three neurons. And here's
[00:41:09] the Here's the the the consistency
[00:41:11] problem, computational problem. Is there
[00:41:13] some weight setting that is consistent
[00:41:15] with a given labeled sample? So, I I've
[00:41:17] got my input points and I want, you
[00:41:19] know, to label this one minus, this one
[00:41:21] plus. So, this is NP-hard.
[00:41:24] Um but um I mean, this is with the step
[00:41:26] activation function. If you have
[00:41:28] um you know, but as as you know, if you
[00:41:31] have uh you know, ReLU activation
[00:41:33] function or sigmoidal activation
[00:41:35] function, then in practice neural nets
[00:41:36] can be be be trained. Um
[00:41:41] Okay. So, um
[00:41:43] let me just kind of wrap up, you know,
[00:41:45] what have I What have I tried to do is
[00:41:47] I've set up the basic PAC model is that
[00:41:50] there are concept classes that we try
[00:41:51] and learn.
[00:41:53] So, we have a concept class C and the
[00:41:55] question we can ask is, is this PAC
[00:41:58] learnable or not? And for the only thing
[00:42:01] we've seen so far is the rectangles in
[00:42:03] the plane are PAC learnable. And um
[00:42:06] I've And I said, well, rectangles were a
[00:42:08] boring concept uh concept class, so
[00:42:10] let's talk about neural nets. So, I
[00:42:12] didn't say
[00:42:14] uh talk about PAC learnability there,
[00:42:15] but I just said, well, I mean, one thing
[00:42:18] one obvious way to to show PAC
[00:42:19] learnability is to draw a sample and
[00:42:21] find a consistent hypothesis. Well,
[00:42:24] okay, so um
[00:42:26] uh
[00:42:28] uh
[00:42:28] we've seen that finding consistent
[00:42:30] hypotheses is is computationally hard
[00:42:32] for rectangles
[00:42:33] uh for for neural nets.
[00:42:36] But let me just say that the definition
[00:42:38] of PAC learning I I gave um
[00:42:41] if I just go back
[00:42:44] So, let me ask a rhetorical question.
[00:42:46] Uh you gave a definition of PAC learn
[00:42:48] learnability, but it said nothing
[00:42:49] whatsoever about computational
[00:42:51] complexity.
[00:42:52] Uh so, I say that the concept class C is
[00:42:55] PAC learnable with sample complexity M,
[00:42:59] accuracy epsilon, and confidence delta
[00:43:01] if there is a learning map such that
[00:43:03] probability if I draw a sample of size M
[00:43:05] that the learning map
[00:43:07] when eating the sample returns a
[00:43:08] hypothesis of error less than epsilon,
[00:43:11] the good case, this probability is
[00:43:13] greater than 1 minus delta.
[00:43:15] So, I said nothing about the complexity
[00:43:17] of executing that map. I didn't even say
[00:43:19] anything about the representability of
[00:43:21] the output of the map. So, this
[00:43:23] definition I I gave just talked about um
[00:43:26] sample complexity.
[00:43:27] And um so, I won't talk about
[00:43:30] computational complexity for a little
[00:43:32] while.
[00:43:34] Okay, so um maybe a chance for a
[00:43:37] question
[00:43:38] that could be repeated.
[00:43:43] Okay?
[00:43:45] No?
[00:43:47] Okay, so um
[00:43:49] I want now to I mean, you're given a
[00:43:52] concept class, and the question is, is
[00:43:54] it PAC learnable or not? Yes or no? And
[00:43:58] um
[00:43:59] there is a combinatorial um
[00:44:02] measure which will tell you
[00:44:04] uh which which characterizes when a
[00:44:06] class is PAC learnable. And this is VC
[00:44:08] dimension, so this is very clean and
[00:44:10] nice.
[00:44:11] So, let C be a con- concept class on
[00:44:14] input space X, such as our rectangles,
[00:44:16] and we say that
[00:44:17] that S is shattered by C if every
[00:44:20] function from S to 0 1 arises as the
[00:44:24] restriction of some
[00:44:26] uh concept C in C. So,
[00:44:30] um
[00:44:31] here is an example.
[00:44:37] Uh
[00:44:39] So, let's take the input space R2.
[00:44:46] And here's a set of four points in R2.
[00:44:49] And let me ask, is this set shattered by
[00:44:53] So, let C be rectangles in the plane.
[00:44:56] Is this set shattered by rectangles in
[00:44:59] the plane here?
[00:45:02] So, here's the set.
[00:45:05] So, every function from the set to 0 1,
[00:45:07] I mean every labeling, every labeling of
[00:45:09] positive and negative
[00:45:11] uh
[00:45:11] arises as the the labeling can be
[00:45:13] realized by some concept. So, is this
[00:45:16] set here shattered by rectangles in the
[00:45:19] plane?
[00:45:22] So, only answer if you don't know the
[00:45:23] answer. It's cheating if you do know the
[00:45:25] answer. I don't think it's shattered
[00:45:27] because if you assign like ones to the
[00:45:30] outer three and a zero to the inner one,
[00:45:33] then you can't find a rectangle.
[00:45:35] Yeah. Yeah.
[00:45:37] Exactly, yes. So, this labeling is not
[00:45:39] realized because if I want a rectangle
[00:45:42] that realizes labeling, I The rectangle
[00:45:44] has to include these points, so it has
[00:45:46] The smallest rectangle that includes
[00:45:47] these four points is this, but then I'm
[00:45:49] forced to include this point. This is
[00:45:51] not shattered. However, if I
[00:45:54] put this point outside,
[00:45:56] well, I could realize this labeling and
[00:45:57] and with these four points I could
[00:45:58] realize any labeling.
[00:46:00] So, um for instance, if you wanted a
[00:46:03] labeling So, I claim these four points
[00:46:05] are shattered. So, if I wanted a
[00:46:06] labeling where this is minus, this is
[00:46:08] plus, and this is plus, I could put a
[00:46:10] rectangle like this.
[00:46:12] Okay. So, that's shattered.
[00:46:15] Okay. And I And claim any So, to be
[00:46:18] shattered means that any labeling can be
[00:46:20] realized.
[00:46:22] And the VC dimension, so this is a the
[00:46:24] dimension of the concept class is
[00:46:26] defined as the supremum over of the
[00:46:29] sizes of all finite sets that are
[00:46:31] shattered by the concept class.
[00:46:34] So, what can we What can we have from
[00:46:35] this definition? What can we infer about
[00:46:37] the VC dimension of this class?
[00:46:40] So, I claim that this four-element set
[00:46:42] is shattered.
[00:46:44] So, this tells me that the VC dimension
[00:46:46] is
[00:46:48] at least four.
[00:46:49] Okay, maybe I can shatter a five-element
[00:46:51] set. Well, can I shatter a five-element
[00:46:53] set?
[00:46:55] So, is there a five-element set that I
[00:46:57] can shatter with the rectangles?
[00:47:04] Yeah, okay.
[00:47:06] Okay. Well, uh can I Can I shatter a
[00:47:08] five-element set uh with the concept
[00:47:10] class of axis-aligned rectangles?
[00:47:13] Uh which you're Now you'll tell me the
[00:47:15] answer.
[00:47:17] No, yeah. Okay, because I mean, if I've
[00:47:19] got five elements, then there's one
[00:47:21] element that's going to be the have the
[00:47:22] highest Y coordinate, one will have the
[00:47:24] least Y coordinate, one will have the
[00:47:26] the the the smallest X coordinate, one
[00:47:28] will have the greatest, and the other
[00:47:30] one will have to be in the small And
[00:47:32] these extremal guys will have to contain
[00:47:35] the rectangle that in that contains
[00:47:36] these extremal guys will have to contain
[00:47:39] the fifth point, and therefore the the
[00:47:41] the the labeling where these guys are
[00:47:44] all negative,
[00:47:46] and this fifth point is positive, is
[00:47:47] unrealizable. So,
[00:47:49] for any set of five points, there is an
[00:47:51] unrealizable uh labeling. So, So, okay.
[00:47:55] So,
[00:47:56] um
[00:47:57] uh what this tells us is that that this
[00:47:59] third example here, axis-aligned
[00:48:00] rectangles, the VC dimension is four.
[00:48:04] Uh what about triangles? So, let's go to
[00:48:06] the fourth thing, uh convex k-gons.
[00:48:08] What's the VC dimension of triangles in
[00:48:11] the plane?
[00:48:12] Um
[00:48:14] I mean, you know, what's the largest set
[00:48:16] that I can shatter with triangles in the
[00:48:18] plane?
[00:48:20] Um
[00:48:23] I It's a workout. I can shatter three. I
[00:48:25] can do Well,
[00:48:27] uh certainly I can shatter three. Well,
[00:48:29] here are four points.
[00:48:31] Um
[00:48:33] Okay, well, that's that's
[00:48:34] I claim I can shatter seven points. So,
[00:48:36] here are seven Here's a set of seven
[00:48:38] points.
[00:48:41] I need to uh Hold on. 1 2 3 4 5 6 7. I
[00:48:45] want to realize any labeling. So, here's
[00:48:47] a labeling.
[00:48:49] So, here's a labeling where I've only
[00:48:51] got three positive points. Then clearly
[00:48:53] I can realize that with this triangle.
[00:48:57] And you might say, "Ah, but what if you
[00:48:58] only have What What if you have um uh
[00:49:02] four positive points?
[00:49:03] The same set."
[00:49:08] So, let's say uh
[00:49:16] So, how can I realize this? Well, I can
[00:49:18] kind of realize that by cutting off the
[00:49:21] negative points like that.
[00:49:23] Okay? Okay, so, um
[00:49:26] uh in in this case it's actually So, the
[00:49:29] the VC dimension of convex k-gons is
[00:49:31] seven.
[00:49:33] Um
[00:49:35] Can I What Can I ask what the VC
[00:49:37] dimension of Boolean formulas on input
[00:49:39] space 01? So, what is the largest subset
[00:49:42] of 01 n that can be shattered by the
[00:49:44] concept class of Boolean formulas?
[00:49:50] So, I wanted to take a subset of 01 to
[00:49:53] the end and realize all labelings of
[00:49:55] that subset
[00:49:56] by a Boolean formula.
[00:50:00] So, here's S subset of 01
[00:50:04] to the end.
[00:50:06] I want to shatter S so every every way
[00:50:09] of labeling S with with 01 I want to be
[00:50:11] realized by Boolean formula.
[00:50:14] Yeah.
[00:50:16] Yeah, in fact I can shatter the whole
[00:50:17] thing cuz any function from 01 to the
[00:50:19] end uh
[00:50:21] 01 can be realized by Boolean formula.
[00:50:24] So, the VC dimension is 2 to the end.
[00:50:27] But, if I restrict to a Boolean a
[00:50:29] circuit that say within cubed gates
[00:50:31] uh well,
[00:50:33] can I realize every function
[00:50:35] from 01 to the end to 01?
[00:50:45] So, what So, any guesses on the VC
[00:50:47] dimension here? What's the largest set?
[00:50:49] I mean, roughly.
[00:50:52] Yeah.
[00:50:54] Uh sorry, yeah.
[00:50:57] Yeah, so I mean and so yeah, okay,
[00:50:59] that's good.
[00:51:00] Yeah, so they are Boolean gates.
[00:51:03] I mean, they're proportional gates but n
[00:51:04] cubed is the number of gates. That's
[00:51:06] what I mean. So, I'm restricting the the
[00:51:08] class the concept classes circuits with
[00:51:10] n inputs. So, I'm looking at circuits
[00:51:12] with n inputs.
[00:51:15] Some gates here. So, it's a graph and
[00:51:18] and but the the point is those n cubed
[00:51:21] gates. So, I'm I'm restricting the size
[00:51:23] of the circuit.
[00:51:25] Well, I mean
[00:51:27] um
[00:51:30] how many such circuits are there
[00:51:31] roughly?
[00:51:33] There's
[00:51:34] um roughly two to the
[00:51:38] two to the
[00:51:39] poly n such circuits.
[00:51:42] Because, you know, how could I choose
[00:51:44] the circuit for every pair of gates I
[00:51:46] have to choose whether they're
[00:51:46] connected, what's um what the what the
[00:51:50] label of a gate is, is it and or not.
[00:51:52] So, there are two to the poly n gates,
[00:51:54] which tells me that the VC dimension
[00:51:56] should be polynomial in n because
[00:51:59] if I want to if I if I have a set and I
[00:52:01] want to realize every labeling by one of
[00:52:04] the concepts, well, I for each concept
[00:52:06] it's going to give me at most one
[00:52:07] labeling. So, the the number of total
[00:52:09] number of labelings I can have is two to
[00:52:11] the poly n. So, the size of the set can
[00:52:13] be only polynomial polynomial. So, if S
[00:52:16] has size poly n, the number of different
[00:52:17] labelings is two to the poly poly n.
[00:52:20] So, in other words, for any every finite
[00:52:23] concept class, its VC dimension is at
[00:52:25] most log of the size of the class. So,
[00:52:28] there the VC dimension is only
[00:52:29] polynomial many poly in n.
[00:52:33] So, there we saw four there it's two two
[00:52:35] k plus one.
[00:52:36] For half spaces, the VC dimension, let
[00:52:39] me just say is is n plus one.
[00:52:42] So, given n plus one points in Rn, I can
[00:52:44] shatter Well, there is a set of n plus
[00:52:46] one points that can be shattered by half
[00:52:47] spaces.
[00:52:48] And then you if you look at these
[00:52:50] geometric examples, you have some idea
[00:52:52] that the VC dimension roughly
[00:52:54] corresponds to the number of parameters
[00:52:56] that's used to define a concept.
[00:52:59] So,
[00:53:00] um
[00:53:01] uh So, how many parameters do I need to
[00:53:03] define an axis-aligned rectangle? I need
[00:53:05] to define the two corners. So, I need
[00:53:06] four parameters.
[00:53:08] So, uh to define, say, a triangle, the
[00:53:11] parameters I need, well, I need six, I
[00:53:13] guess, for the three
[00:53:14] um
[00:53:15] uh
[00:53:16] um
[00:53:17] uh Well, I guess I I yeah.
[00:53:19] Uh six, let's say, for the three um
[00:53:22] vertices. A half space, n plus one
[00:53:24] parameters.
[00:53:26] But, the outlier is going to be this guy
[00:53:28] here.
[00:53:29] Uh so, this has VC dimension infinity.
[00:53:31] So, what is this concept class?
[00:53:34] So, it's parameterized Well, it's it's a
[00:53:35] class of functions with this parameter,
[00:53:38] and the function looks at
[00:53:40] um
[00:53:41] Well, the sign sign means
[00:53:44] if the thing is positive, return plus
[00:53:46] one. The sgn sign is
[00:53:49] and if the thing is negative, return
[00:53:50] minus one. So, here's a kind of um
[00:53:55] Uh here's a
[00:53:57] So, here's let's say I want to shatter
[00:53:59] this set here.
[00:54:02] So, I've got a set of points I want to
[00:54:03] shatter and I want to realize every
[00:54:06] labeling.
[00:54:08] So, here's a labeling. And what I can do
[00:54:11] to realize this labeling is if if my
[00:54:13] sign somehow behaves like this.
[00:54:17] So, this is sign alpha x for some alpha.
[00:54:21] Then I've realized that labeling. So, if
[00:54:22] I take the sign, so when sign is is
[00:54:25] negative, I get minus. When sign is
[00:54:26] positive, I get plus. When sign is
[00:54:28] negative, I get minus.
[00:54:30] So, the labeling here is the the VC
[00:54:32] dimension here is infinity and somehow
[00:54:35] there's a nice connection with logic
[00:54:36] here in that um
[00:54:40] uh
[00:54:42] Essentially, uh
[00:54:44] if you're working with kind of so-called
[00:54:47] tame functions, the VC dimension of the
[00:54:49] the the class of space corresponds to
[00:54:51] number of parameters that you use to
[00:54:53] define a concept. So, here there's only
[00:54:55] one parameter and the VC dimension is
[00:54:57] infinity. This is because sign is not a
[00:54:59] nice function. So, um
[00:55:02] uh so, I'll I'll speak about this um in
[00:55:05] in the second half, but essentially
[00:55:08] uh
[00:55:09] Well, okay. I'll I'll speak I'll speak
[00:55:12] about it more later. So, in particular,
[00:55:14] we're going to see that um
[00:55:17] this class here is not this is going to
[00:55:19] be our first example of of of well,
[00:55:22] this is going to be a
[00:55:24] a concept class which is not packed
[00:55:25] learnable. So, another concept class
[00:55:27] which is not packed learnable is going
[00:55:29] to be the class of all k-gons in the
[00:55:32] plane. So, where I've no bound on on k.
[00:55:34] So, all convex polygons in the plane is
[00:55:37] not It's going to It's going to be not
[00:55:38] pack learnable.
[00:55:40] So, um okay. So, I I want to just So,
[00:55:44] uh this is uh Radon's theorem is why the
[00:55:46] dimension of half spaces is n + 1, but
[00:55:49] I'm going to jump over that.
[00:55:51] Um
[00:55:53] So, let me look how I'm doing for time.
[00:55:56] Uh I'm a little bit behind. So, I'm
[00:55:59] going to going to jump over these uh
[00:56:02] um
[00:56:03] uh
[00:56:04] uh example. But, I want to talk about uh
[00:56:06] dual classes. So,
[00:56:08] uh I have a
[00:56:09] uh
[00:56:11] concept class
[00:56:13] C.
[00:56:21] Okay, so here's my concept class. And I
[00:56:24] I'm going to define the dual class. So,
[00:56:26] well, let me just refer to the slide.
[00:56:28] So, the dual class C star is a class of
[00:56:31] functions from C to 0 1. So, now that
[00:56:34] it's like the input space of this is now
[00:56:36] concepts of the the previous space. And
[00:56:38] it's going to consist of all functions
[00:56:41] from C to 0 1 um
[00:56:43] indexed by uh elements X of the original
[00:56:47] the concept class such that FX of C is C
[00:56:50] is C of X. And the claim is as follows.
[00:56:54] The VC dimension of um C is less than or
[00:56:58] equal to the VC dimension of um
[00:57:01] uh uh
[00:57:02] I think I I actually wanted to say the
[00:57:04] other.
[00:57:06] I mean,
[00:57:07] it's somehow
[00:57:08] I wanted to state it this way.
[00:57:17] Okay. So, here's the proof. Um
[00:57:21] Suppose that I could shatter
[00:57:33] So,
[00:57:34] um
[00:57:35] some set
[00:57:37] of guys
[00:57:39] in C
[00:57:41] of size 2 to the end for some n.
[00:57:46] Uh let me call them C's, yeah.
[00:57:56] Suppose I could shatter the these, then
[00:57:59] it
[00:58:00] in the these guys are in the
[00:58:02] the um
[00:58:04] uh
[00:58:06] C. By guys in the dual class, then in
[00:58:09] particular
[00:58:11] um there exists so
[00:58:20] there exists
[00:58:21] x i's such that
[00:58:24] uh f
[00:58:25] x i
[00:58:27] c j
[00:58:28] equals 1
[00:58:30] if
[00:58:32] i'th bit
[00:58:36] of j is 1.
[00:58:40] So, to say I can shatter this means that
[00:58:43] I can realize every labeling.
[00:58:45] So, a labeling that I might want to
[00:58:47] realize is I want the labeling that says
[00:58:50] um
[00:58:51] uh take c j and map it to 1 if and only
[00:58:55] if the i'th bit of j is 1. So, that
[00:58:57] labeling is realized by this function.
[00:59:00] But then in this case, if I look at the
[00:59:02] set
[00:59:03] x1 up to xn,
[00:59:06] so by construction these x i
[00:59:09] are in x,
[00:59:11] then this this set is shattered. So, in
[00:59:13] fact, this set here uh
[00:59:16] uh in in x is shattered by these
[00:59:18] functions c1 up to c2n.
[00:59:22] So, uh every So, for instance, if I have
[00:59:24] some labeling of this, then some
[00:59:27] labeling of this set will determine uh
[00:59:29] an n-bit Boolean number
[00:59:32] and the say j and cj will realize that
[00:59:36] that labeling.
[00:59:38] Um
[00:59:39] So,
[00:59:41] we have this
[00:59:43] upper bound. So, in other words,
[00:59:45] a concept class c is pack learnable if
[00:59:47] and only if it's dual class is pack
[00:59:48] learnable. And we're going to use this
[00:59:51] result
[00:59:53] well
[00:59:54] in this this this kind of approach to
[00:59:57] this little Littlestone wellness
[00:59:58] conjecture.
[01:00:01] Okay, so um
[01:00:06] Yeah, so this there is this notion of VC
[01:00:08] dimension and what we're heading towards
[01:00:10] is a result that says that a class a
[01:00:14] concept class c is pack learnable if and
[01:00:16] only if it has finite VC dimension. So,
[01:00:19] this is kind of classical result and the
[01:00:21] way we're going to So, why is VC
[01:00:23] dimension so useful? Uh it controls the
[01:00:26] so-called it's a way to get a bound on
[01:00:28] the so-called growth function of a
[01:00:30] concept class.
[01:00:31] So, um
[01:00:34] So, consider a concept class c on an
[01:00:36] input space x
[01:00:38] and given a finite sample s points drawn
[01:00:42] from x
[01:00:43] define
[01:00:45] pi c of s to be well, the following
[01:00:49] thing, the set of
[01:00:51] restrictions of concepts to to to um
[01:00:55] to s. So, the way to visualize this is
[01:00:57] you've got a you've got a set of points
[01:00:59] s and what is pi c of s? So, I've got a
[01:01:04] set of points s
[01:01:10] and I've got some concept class in the
[01:01:12] background c.
[01:01:14] So, it's clear if I pick a a concept in
[01:01:17] c c and c
[01:01:19] that induces a labeling on this set.
[01:01:25] Another concept will induce another
[01:01:27] labeling.
[01:01:28] And the question is, how many labelings
[01:01:29] are there? Well, it depends on the set,
[01:01:31] it depends on the concept class, but pi
[01:01:33] C of S gives me the set of all
[01:01:35] labelings.
[01:01:37] So, how many ways are there for me to
[01:01:39] label that set? And the growth function
[01:01:41] is defined by So, it's a function from N
[01:01:44] to N.
[01:01:45] It takes a integer M. So, it's a it it's
[01:01:48] determined by the concept class. And the
[01:01:50] the notation is pi. So, pi for
[01:01:52] partitions. And it's the maximum over
[01:01:54] all subsets of the input space of size M
[01:01:57] of the number of labelings that I can of
[01:02:00] of such a set S.
[01:02:03] So, here's a question. How can I
[01:02:04] reformulate that the a set is shattered
[01:02:08] in terms of of of this? So, when is when
[01:02:12] is a set shattered? What what does this
[01:02:13] tell me about pi C of S that S is
[01:02:16] shattered?
[01:02:22] Yeah. So,
[01:02:24] a set S is shattered if I can realize
[01:02:26] all labelings.
[01:02:27] And this is shattered if the size of
[01:02:29] this Well, if S has size M, this is 2 to
[01:02:32] the M.
[01:02:33] So, in particular, if I can find a set
[01:02:35] of every size that's shattered, then I
[01:02:38] know exactly what this function is. It's
[01:02:39] just a function M maps to 2 to the M.
[01:02:44] So, if I'm in a concept class, let's say
[01:02:47] uh
[01:02:48] uh where the VC dimension is infinite,
[01:02:49] so there every for every finite set, so
[01:02:52] every finite M there's a set of size M
[01:02:54] that's shattered, then that tells me
[01:02:56] what the growth function is.
[01:02:58] Uh okay, well, there's a an exercise in
[01:03:00] a second, but um
[01:03:02] uh
[01:03:02] let me just go back in a second.
[01:03:05] But a key thing linking the VC dimension
[01:03:07] to the growth function is as follows.
[01:03:10] Let C be a hypothesis set with finite VC
[01:03:12] dimension D. Then for all M, this is
[01:03:17] going to be the size of the sets that I
[01:03:18] I'm going to draw, I have the following
[01:03:20] bound on the growth function and the
[01:03:23] thing to focus on, well,
[01:03:25] uh
[01:03:25] this expression here. So, in particular,
[01:03:28] this is going to be polynomial in in in
[01:03:30] uh m. So, this is going to be a
[01:03:31] polynomial uh with degree uh d. So, this
[01:03:34] is going to be um
[01:03:36] O of m to the d.
[01:03:39] The growth function.
[01:03:40] Um so, there is there's a dichotomy.
[01:03:42] Either the growth function is
[01:03:43] exponential or it's polynomial. And it's
[01:03:45] polynomial when the the the the VC
[01:03:46] dimension is finite. And it's very So,
[01:03:48] this this
[01:03:50] this expression here is very easy to
[01:03:52] remember. So, what is the prototypical
[01:03:54] example of a concept class that has VC
[01:03:57] dimension d as in the statement of the
[01:04:00] theorem?
[01:04:01] So, let's take the input space to be the
[01:04:04] natural numbers and see the collection
[01:04:05] of all subsets of n of cardinality at
[01:04:07] most d. So, I should just say uh
[01:04:10] I mean, I hope it's very clear that I'm
[01:04:12] variously talking about concepts as
[01:04:13] functions to uh concept classes as
[01:04:16] classes of functions from 1 0 and as
[01:04:18] classes of sets. The same I mean, making
[01:04:21] this identification. So, this this
[01:04:23] clearly has uh
[01:04:24] VC dimension d, the class of all subsets
[01:04:26] of cardinality at most d. So, this is
[01:04:28] clear. And it's clear that the number of
[01:04:30] labelings
[01:04:32] using this concept class of a set of
[01:04:34] size m is just this.
[01:04:36] So, it's just the number of subsets of
[01:04:37] size d. So, what this is saying is,
[01:04:40] well, this
[01:04:42] um upper bound on the growth function is
[01:04:44] in fact uh I mean, this is the worst
[01:04:46] case for the growth function among among
[01:04:48] uh classes of VC dimension d.
[01:04:51] So, okay. So, now for a kind of workout,
[01:04:54] um
[01:04:55] let C be the class of annular disks like
[01:04:57] this. What is the growth function? Like
[01:04:59] like, can you work it out natively
[01:05:01] without without looking thinking about
[01:05:03] the VC dimension?
[01:05:06] So, the the concepts look like this. So,
[01:05:08] here's R2.
[01:05:10] And the question is, given given sample,
[01:05:12] how many labelings uh
[01:05:14] are there as a function of the number of
[01:05:17] of points in the sample? So, I can have
[01:05:20] Here's the sample
[01:05:23] here, and with this concept that I've
[01:05:25] drawn here,
[01:05:26] here's the labeling.
[01:05:31] And this is a sample of of M points. And
[01:05:34] the question is how does What's the
[01:05:35] upper bound?
[01:05:38] So, pi of this concept class CM is the
[01:05:42] number of labelings for a sample of size
[01:05:43] M.
[01:05:45] Uh
[01:05:46] so, again,
[01:05:48] um
[01:05:50] uh what's What's the kind of order of
[01:05:53] growth of this this function here?
[01:05:58] So, I mean, there's clearly there are
[01:06:00] some In this sample, there are clearly
[01:06:02] some labelings that are not achievable.
[01:06:04] So, I'm not
[01:06:05] uh I I I can't achieve all It's not
[01:06:07] going to be two to the end. This is kind
[01:06:09] of clearly finite VC dimension.
[01:06:12] So, let me
[01:06:16] So, there's a fixed a fixed set here.
[01:06:22] Yeah.
[01:06:24] Sorry?
[01:06:31] Um
[01:06:33] you
[01:06:34] uh well,
[01:06:35] not
[01:06:37] At least not how I was thinking about
[01:06:38] it. I was thinking, well, maybe is there
[01:06:40] any anyone else want to
[01:06:44] So, I mean, what what determines a
[01:06:45] labeling? So, if I label this guy
[01:06:47] positively, so this this just to be
[01:06:49] clear, these um these these circles have
[01:06:52] center the origin. So, here's my here's
[01:06:54] my class here.
[01:06:55] If I I look at the radius of the points,
[01:06:58] uh I look at the most The point that's
[01:07:00] furthest to So, that the whole labeling
[01:07:02] is determined by two points, namely the
[01:07:05] the the the positive point, which is has
[01:07:07] greatest radius and the positive point
[01:07:09] that has least radius.
[01:07:11] Or maybe it's only determined by one
[01:07:12] point.
[01:07:13] So, the labeling is determined by either
[01:07:15] two points if it's
[01:07:18] if it's like a fat annulus or maybe one
[01:07:21] point if it's a thin annulus that just
[01:07:23] contains one positive point or maybe no
[01:07:26] points if it's the empty set.
[01:07:28] So, uh
[01:07:30] for well, it depends on the set, but
[01:07:33] uh if for any kind of reasonable set in
[01:07:35] general position um
[01:07:38] this should be the number of um
[01:07:40] uh
[01:07:41] dichotomies that I can
[01:07:43] realize.
[01:07:44] Okay, so
[01:07:46] um
[01:07:47] yeah, okay. So, I guess I just continue
[01:07:50] for another five
[01:07:53] five or 10 minutes before a break. Uh
[01:07:56] so, there was Sauer's lemma. So, this is
[01:07:57] the connection of VC dimension
[01:08:00] and the growth function.
[01:08:02] So,
[01:08:03] um
[01:08:04] uh so, we introduced neural networks and
[01:08:07] we have an idea that the VC dimension
[01:08:10] should correspond to the number of
[01:08:12] parameters. There's a very precise
[01:08:14] formulation of that in model theory that
[01:08:17] will I'll just state it in the second
[01:08:19] half. Um
[01:08:22] so, uh
[01:08:24] so, let's fix an architecture of a
[01:08:26] neural net. And the architecture of the
[01:08:27] neural net is just a graph. So, just to
[01:08:29] to reiterate this
[01:08:31] um
[01:08:33] so, maybe I didn't make it
[01:08:35] So, why do I keep on moving the pens
[01:08:36] around? Um
[01:08:38] where do I put them? Um
[01:08:42] the archi So, fixed architecture of a
[01:08:44] neural net is just a directed graph
[01:08:46] where we've got these input nodes where
[01:08:47] we're feeding inputs um
[01:08:51] So, our inputs, let's say, come from
[01:08:54] R to the um N0. So, this is the We've
[01:08:57] got N0 inputs and we've got these
[01:09:00] internal so-called hidden layers.
[01:09:04] Uh
[01:09:05] so this is going to be a so called fully
[01:09:07] connected neural net. So, at each node
[01:09:11] it's going to take in inputs, it's going
[01:09:12] to have weights of W1, W2, W3, W4, W5.
[01:09:19] These weights are what I'm going to use
[01:09:21] to train the network.
[01:09:22] And then the output here is is is got by
[01:09:25] taking a weighted sum of the inputs,
[01:09:26] then applying the activation function,
[01:09:28] and then feeding the output to the
[01:09:30] succeeding layers. And then and then so
[01:09:33] on until
[01:09:34] the output and I'm assuming everything
[01:09:36] here is 0 1, so the activation function
[01:09:37] here is always the step function. That's
[01:09:39] it.
[01:09:40] And so if I fix a graph, then I have a
[01:09:44] concept class. The concept class is got
[01:09:46] by varying the parameters of the net.
[01:09:48] So, these weights in the graph. So, this
[01:09:51] is what I mean by fixed architecture.
[01:09:53] And in this case, so um
[01:09:56] uh N0 is the number of inputs. So, this
[01:09:59] is a concept class that takes
[01:10:01] uh tuples with dimension N0. So, these
[01:10:05] uh whoops, N0 not N20.
[01:10:08] And maps something in 0 1.
[01:10:12] So, the uh VC dimension here
[01:10:16] uh is uh at most the number of
[01:10:18] parameters.
[01:10:20] Uh it's it's linear in in the number of
[01:10:21] parameters and the log of the number of
[01:10:23] parameters.
[01:10:24] And in fact, that's easy to show just
[01:10:26] knowing what we uh
[01:10:28] um
[01:10:29] uh knowing what we know.
[01:10:32] Um so, I'm going to So, essentially, the
[01:10:34] way the way you can do this is you Well,
[01:10:36] you say, "Well, how how do you prove
[01:10:38] this?"
[01:10:39] Um so, this is for the for the step
[01:10:41] activation, which I didn't say this.
[01:10:44] Yeah, so um well, I say it in the title
[01:10:46] of the slide with step activation.
[01:10:48] So, this is a composition of
[01:10:51] perceptrons.
[01:10:52] We know the VC dimension of a linear
[01:10:54] classifier. Therefore, we have a bound
[01:10:56] on the growth function. Using a bound on
[01:10:59] the growth function for every layers,
[01:11:00] you can kind of trivially get a bound on
[01:11:02] the growth function for the whole thing.
[01:11:04] From the bound on the growth function,
[01:11:06] you get a bound on the VC dimension. So,
[01:11:08] just by kind of
[01:11:10] simple manipulations, you can you can
[01:11:12] prove this result.
[01:11:14] But, the basic idea is that the number
[01:11:15] of parameters corresponds to the number
[01:11:17] of VC dimensions. And when when we talk
[01:11:19] about sample compression schemes,
[01:11:21] there's a very general result that
[01:11:24] makes that clear.
[01:11:25] So, I'm just going to to round off the
[01:11:27] first half by now making a connection
[01:11:30] with logic.
[01:11:33] Uh so, this is the learning and logic
[01:11:37] workshop. So,
[01:11:39] um
[01:11:41] we've seen a bunch of concept classes.
[01:11:43] So, I said
[01:11:45] rectangles in the plane, linear
[01:11:47] classifiers, polygons in the plane,
[01:11:50] neural nets, and there's a with a fixed
[01:11:53] architecture. And there's a very general
[01:11:55] way that we can capture these concept
[01:11:56] classes in logic.
[01:11:58] So, um
[01:12:00] let's consider a signature sigma
[01:12:02] predicate logic. So, let's say first
[01:12:04] order signature.
[01:12:06] And let's take a formula where the
[01:12:08] variables are partitioned into two
[01:12:09] groups. So, there are variables X1 up to
[01:12:12] XM and Y1 up to YN.
[01:12:16] And let's fix a sigma structure and
[01:12:20] a set of elements B1 up to BN that we're
[01:12:23] going to instantiate the Y variables
[01:12:25] with.
[01:12:26] And then, what I'm going to define now
[01:12:27] is a class of sets.
[01:12:29] So, the notation I'm using is
[01:12:32] this notation here.
[01:12:34] So, the notation takes the the the
[01:12:36] structure and the the these these these
[01:12:39] elements B1 to BN. I'll call these
[01:12:41] parameters.
[01:12:42] So, what this is is a set of
[01:12:45] A1 up to AM two poles in the universe
[01:12:48] such that A satisfies this. So, here's
[01:12:51] the picture. We've got a formula and
[01:12:53] it's going to define a concept class.
[01:12:55] Each concept is specified by the tuple
[01:12:57] of parameters B1 up to to BM.
[01:13:00] So for every setting of parameters, I
[01:13:03] get a concept which is this set. So as I
[01:13:06] say, a concept you can think of as a
[01:13:08] function
[01:13:09] um
[01:13:11] So let me just say here that the input
[01:13:12] space here
[01:13:14] is AM where A is the the universe of the
[01:13:17] of the structure.
[01:13:18] So this is the input space. A concept A
[01:13:20] concept is a function from this to 01 or
[01:13:22] equivalently a subset of this
[01:13:24] and so this is a a general way to define
[01:13:25] a concept class. And if you think that a
[01:13:28] a lot of the concept classes we've been
[01:13:30] defining have this form. So rectangles
[01:13:32] in the plane, what are the parameters?
[01:13:34] They're the corners of the rectangle and
[01:13:36] then there's the formula that tells us
[01:13:37] whether uh uh
[01:13:40] a tuple A1, A2 is inside the rectangle.
[01:13:42] There's a single formula that does that.
[01:13:44] So the idea is that we have a single
[01:13:46] formula and by varying the parameters we
[01:13:47] get different concepts. So again, linear
[01:13:50] classifiers, what are the the
[01:13:51] parameters? They're the the coefficients
[01:13:53] of the linear function that defines the
[01:13:55] classifier.
[01:13:57] Even a neural net with a fixed graph can
[01:13:59] easily be um be put in this framework.
[01:14:02] We can have a a fixed formula. The
[01:14:04] parameters are the weights of the neural
[01:14:06] net.
[01:14:07] Of course,
[01:14:08] the signature I need and the structure
[01:14:11] I'm working on depends on the type of
[01:14:13] neural net I have. So if I have like a a
[01:14:15] sigmoidal activation function
[01:14:20] in my neural net,
[01:14:24] so what structure am I working over?
[01:14:26] Well, I'm working over
[01:14:28] oops, the structure if if my structure A
[01:14:31] is the reals
[01:14:34] with 0, 1,
[01:14:36] times, plus, and exponential,
[01:14:41] then for a fixed neural network, I can
[01:14:43] define
[01:14:45] uh for a fixed architecture, I can
[01:14:46] define a formula that defines the
[01:14:48] concept class determined by that
[01:14:50] architecture. So, again, the parameters
[01:14:51] of the formula are the weights of the
[01:14:53] neural net, and um
[01:14:55] uh, and the formula classifies tuples.
[01:14:58] And, you know, so if the structure is
[01:15:00] nice enough, the the the the the concept
[01:15:03] class, if the formula is nice enough or
[01:15:05] the structure is nice enough, the
[01:15:06] concept class will uh have nice
[01:15:09] properties. So,
[01:15:10] um
[01:15:12] So, we will will will will use this
[01:15:14] notation. So, this is a concept class
[01:15:16] that's determined by a structure and a
[01:15:17] formula.
[01:15:19] And uh again, so for every set of
[01:15:21] parameters, uh we have a concept, which
[01:15:24] is this, which is a collection of
[01:15:26] subsets of of A A to the N.
[01:15:29] Okay. And uh do I have anything to say
[01:15:32] for that? Yeah, just some notation.
[01:15:33] We'll write VC phi A for the VC
[01:15:36] dimension of this concept class. And
[01:15:38] what I kind of want to do in the the
[01:15:40] second half is talk about um various
[01:15:44] ways of of bounding this, and then
[01:15:47] connections with sample compression.
[01:15:50] Uh
[01:15:53] Yeah, so I I I want to consider
[01:15:54] structures like the reals, but also find
[01:15:57] also kind of graphs, you know, um
[01:16:00] uh discrete structures.