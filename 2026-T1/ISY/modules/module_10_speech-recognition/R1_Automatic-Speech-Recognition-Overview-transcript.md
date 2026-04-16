[00:00:04] So, hi everyone, I'm Preethi,
[00:00:06] I'm in the department of Computer Science at IIT Bombay.
[00:00:09] And so today, my tutorial is going to be about ASR systems.
[00:00:14] So I'm just going to give a very kind of high level overview of
[00:00:18] how standard ASR systems work and
[00:00:21] what are some of the challenges.
[00:00:23] And hopefully leave you with some open problems and
[00:00:27] things to think about.
[00:00:29] For the uninitiated, what is an ASR system, it's one which
[00:00:34] accurately translates spoken utterances into text.
[00:00:38] So text can be either in terms of words or
[00:00:41] it can be a word sequence, or it can be in terms of syllables,
[00:00:44] or it can be any sub-word units or phones, or even characters.
[00:00:49] But you're translating speech into its corresponding
[00:00:54] text form.
[00:00:55] So lots of well-known examples, and most of you must have
[00:00:57] encountered at least one of these examples.
[00:01:00] So YouTube's closed captioning, so an ASR engine is running,
[00:01:05] and producing the corresponding transcripts for the speech,
[00:01:09] the audio, and the video clips.
[00:01:11] Then voice mail transcription,
[00:01:13] even if you've not used it, you might have looked at it and
[00:01:15] laughed at it, because it's usually typically very bad.
[00:01:19] So the voice mail transcription is also an ASR run engine which
[00:01:22] is running.
[00:01:23] Dictation systems were actually one of the older prototypes of
[00:01:27] ASR systems.
[00:01:28] And I think now, it's obviously gotten much better, but
[00:01:31] I remember Windows used to come prepackaged with a dictation
[00:01:34] system, and that used to be pretty good.
[00:01:37] So dictation systems, of course, you're speaking out, and
[00:01:41] then you automatically get the corresponding transcript.
[00:01:44] Siri, Cortana, Google Voice, so
[00:01:47] all of their front ends are ASR engines and so on.
[00:01:51] This is ASR, but if, I didn't get a picture of Cortona,
[00:01:55] I apologize, so this is Siri.
[00:01:58] But if you were to say, call me a taxi, and
[00:02:00] Siri responded from now on, I'll call you Taxi, okay?
[00:02:03] This is not the fault of an ASR system, so
[00:02:07] the ASR system did its job.
[00:02:08] But there's also a spoken language understanding module
[00:02:12] to which the ASR will feed into.
[00:02:14] And so, that didn't do its job very well, and so
[00:02:16] it got the semantics wrong.
[00:02:18] So people typically tend to correlate the understanding and
[00:02:22] the transcription part as ASR.
[00:02:24] But ASR is strictly just translating the spoken
[00:02:27] utterances into text.
[00:02:30] So why is ASR desirable, and
[00:02:32] why would you want to build ASR systems for maybe all languages?
[00:02:36] So obviously, speech is the most natural form of communication.
[00:02:39] So rather than typing, which is much more cumbersome,
[00:02:43] you can speak to your devices.
[00:02:45] And if ASR systems were good, then that kind of solves lots of
[00:02:50] issues, and also keeps your hands free,
[00:02:52] which is not always a good thing.
[00:02:55] So many car companies like Toyota and Honda are investing
[00:02:59] quite a bit to build good speech recognition systems,
[00:03:01] because they want you to be able to drive and talk.
[00:03:05] I don't know if I entirely recommend it, but clearly,
[00:03:09] it leaves other modalities open to do other things.
[00:03:13] Also, another very kind of socially desirable aspect of
[00:03:17] building ASR systems is that now you have interfaces for
[00:03:21] technology which can be used by both literate and
[00:03:23] illiterate users.
[00:03:24] So even users who cannot read or write in a particular language
[00:03:28] can interact with technology, if it is voice driven.
[00:03:31] And this was, so endangered languages was a point which
[00:03:35] brought up, that lots of languages are currently close to
[00:03:39] extinction, or they've been given this endangered status.
[00:03:42] So if you have technologies which are built for
[00:03:44] such languages,
[00:03:45] it can contribute towards the preservation of such languages.
[00:03:47] So that's just one kind of nice point of why you would want to
[00:03:50] invest in building ASR systems, so
[00:03:55] why is ASR a difficult problem?
[00:03:57] So, the origins of ASR actually go way back,
[00:04:00] it's a longstanding problem in AI, back in the 50's.
[00:04:05] So why is it such a difficult problem, when clearly it's not
[00:04:08] very difficult for humans to do speech recognition,
[00:04:10] if you're familiar with the language?
[00:04:12] It's difficult because there are several sources of variability,
[00:04:17] so one is just your style of speech.
[00:04:20] So apparently, the way I'm speaking, it's kind of semi
[00:04:23] spontaneous, but I more or less know what I'm going to say, or
[00:04:26] here I'm guided by the points on the slides.
[00:04:28] And it's suddenly continuous speech, so I'm not speaking any
[00:04:31] kind of staccato manner, or I'm not saying isolated words.
[00:04:35] So just the style of speech
[00:04:38] can have a lot to do with how ASR systems will perform.
[00:04:41] And intuitively, isolated words are much more easier for
[00:04:45] ASR systems than continuous speech.
[00:04:47] And that's because when you're speaking spontaneously,
[00:04:50] words are flowing freely into one another.
[00:04:53] And there are lots of variations which come in
[00:04:55] due to pronunciations, and
[00:04:58] there's this Phenomenon of what's known as coarticulation.
[00:05:03] So it's just that words,
[00:05:05] your preceding word affects the word which is coming, and so on.
[00:05:09] And so, because of this kinda smooth characteristic of
[00:05:12] continuous speech, that actually creates quite a lot of,
[00:05:15] it's quite challenging for ASR systems to handle it.
[00:05:18] Of course nowadays if you have lots and
[00:05:19] lots of data, this is not really a problem, but
[00:05:22] this is one prominence source of variability.
[00:05:25] Another of course is environment.
[00:05:26] So if you're speaking in very noisy conditions, or
[00:05:30] if your room acoustics are very challenging, for example,
[00:05:35] it's very reverberant, so you have a lot of etcho.
[00:05:39] Or you're speaking in the presence of interfering
[00:05:42] speakers, so that's actually a real killer.
[00:05:44] So if you're talking and there's background noise, but
[00:05:47] the background noise is not, like the vehicle noise or
[00:05:50] something which can be easily isolated, but
[00:05:52] there's actually people talking in the background,
[00:05:55] that's really hard for ASR systems to kind of pick out
[00:05:58] the voice in the foreground and work on it.
[00:06:01] So environment is another important source of
[00:06:04] variability and something which people are very actively
[00:06:06] working on now to build what are known as robust
[00:06:09] ASR systems which are robust to noise.
[00:06:12] Then of course speaker characteristics.
[00:06:15] So all of us have different ways of speaking, so of course,
[00:06:18] accent comes into play.
[00:06:20] Just your rate of speech, some people speak faster,
[00:06:23] some people enunciate more.
[00:06:25] Of course your age also changes
[00:06:30] your characteristic of your speech.
[00:06:31] So the child speech is going to be very different from
[00:06:34] adult speech.
[00:06:35] So various characteristics of speakers also,
[00:06:38] which contribute to making a challenging problem.
[00:06:41] And of course there are lots of tasks with specific constraints.
[00:06:46] For example the number of words in your vocabulary
[00:06:50] which you're trying to recognize.
[00:06:53] So if your looking at Voice Search Applications,
[00:06:55] they're looking at million word vocabularies.
[00:06:58] But if you're looking at a Command and
[00:07:01] Control task where you're only trying to move something, or
[00:07:05] your grammar is very constrained,
[00:07:07] there your vocabulary is much smaller so that task is simpler.
[00:07:11] And you might also have language constraints, so
[00:07:13] maybe you're trying to recognize speech in the language which
[00:07:16] doesn't have a written form.
[00:07:18] So doesn't have transcripts at all, then what you do?
[00:07:21] Or if you're working with the language which is very
[00:07:23] morphologically rich, or it has words which have agglutinative
[00:07:28] properties, so then what you do with your language models,
[00:07:30] maybe in grams are not good enough.
[00:07:32] So lots of tasks,
[00:07:33] specific constraints also which contribute to making this
[00:07:36] a challenging problem.
[00:07:38] Okay, so hopefully I have convinced you that
[00:07:41] ASR is quite a challenging prom to work on.
[00:07:45] So let's kind of just go through the history of ASR, and
[00:07:48] this is just a sampling.
[00:07:51] I'm not going to cover most of the important systems.
[00:07:54] There has been a lot of work since the 50s, this is actually
[00:07:57] the 20s, but I'll talk a little about what this is.
[00:08:00] So the very first kind of ASR, and I'm air coating,
[00:08:03] because it really isn't doing any recognition of any sort, but
[00:08:06] it's this charming prototype called Radio Rex.
[00:08:10] So it's this tiny dog which is sitting inside its kennel and
[00:08:13] it's controlled by a spring,
[00:08:15] which in turn is controlled by an electromagnet.
[00:08:17] And the electromagnet is sensitive to energies at
[00:08:20] frequencies around 500 Hertz.
[00:08:23] And 500 Hertz happens to be the frequency of the vowel sound
[00:08:27] e in Rex.
[00:08:29] So when someone says Rex, the dog will jump out of the kennel.
[00:08:35] So this is purely a frequency detector, so
[00:08:37] it's not doing any recognition, but
[00:08:40] it's a very charming prototype, but clearly, can anyone kind of,
[00:08:45] there's so many issues with this, but this kind of
[00:08:49] system in your hard coding needs to be fired at this 500 Hertz.
[00:08:53] What is an obvious problem with such a prototype?
[00:08:59] >> Noise.
[00:09:01] >> Noise, yeah, of course.
[00:09:03] >> Different people, it might not [CROSSTALK]
[00:09:04] >> Yeah, exactly.
[00:09:05] So this only works for adult men.
[00:09:08] So it's sexist, and it's ageist.
[00:09:10] It doesnt work on children's speech,
[00:09:11] it doesn't work on female speech.
[00:09:13] So yeah, that's obviously an issue when you
[00:09:15] hard code something.
[00:09:16] I recently discovered this is on eBay, and you can-
[00:09:21] >> [INAUDIBLE].
[00:09:22] >> Yeah.
[00:09:23] >> I wanted one of these.
[00:09:24] >> Really? Okay, yeah, yeah, yeah.
[00:09:25] >> There was one on sale for, and so I started,
[00:09:29] then actually created my account to bid for this thing.
[00:09:33] And then I noticed the person who kept bidding on top of
[00:09:36] me was someone who's called Ina Kamensky.
[00:09:39] >> No [LAUGH]. >> He's a professor at James U,
[00:09:41] because he wanted one as well.
[00:09:42] >> Okay, so he got it?
[00:09:43] >> I stopped bidding and asked him for the video if he gets it.
[00:09:46] >> [LAUGH] >> So he did buy it?
[00:09:49] >> [INAUDIBLE] Giving you the video, but he did win.
[00:09:51] >> Wow, okay.
[00:09:51] Okay, so I can add that to my slide x.
[00:09:55] [INAUDIBLE] >> He has it, yeah.
[00:09:58] Okay, so that's the very initial prototype, but
[00:10:00] that's single word, and it's a frequency detector.
[00:10:03] So that's not really doing recognition.
[00:10:06] So the next kind of major system was SHOEBOX, which was in 1962,
[00:10:10] and it was by IBM.
[00:10:11] And they actually demoed the system, it did pretty well.
[00:10:15] But what it was recognizing was just connected strings of
[00:10:19] digits.
[00:10:20] So it's just purely a digit recognizer and
[00:10:23] a few mathematic operations.
[00:10:24] So it could do basic mathematic, you could say 6+5 is, and so on.
[00:10:30] So it would perform very well ,but of course,
[00:10:33] this is also very limited.
[00:10:34] So it's just a total of 16 words, so ten digits and
[00:10:37] six operations, and it's doing isolated word recognition.
[00:10:41] So actually, sorry, this is not connected speech.
[00:10:44] You would have to say it with a lot of pause in between each of
[00:10:47] the individual words.
[00:10:49] So this was just doing isolated word recognition.
[00:10:52] And then in the 70s, there was kind of a lot of interest in
[00:10:57] developing speech recognition systems and AI based systems.
[00:11:01] And ARPA, which is this big agency in the US,
[00:11:04] funded this $3 million project in 1975, and
[00:11:07] three teams worked on this particular project.
[00:11:12] And the goal was to build a fairly advanced speech
[00:11:14] recognition system, which is not just doing some isolated word
[00:11:18] recognition and would actually evaluate continuous speech.
[00:11:22] And so, the winning system, from this particular project,
[00:11:26] was HARPY out of CMU.
[00:11:27] And HARPY actually was recognizing
[00:11:30] connected speech from 1,000 word vocabulary.
[00:11:34] So we are slowly making progress, but it still didn't
[00:11:38] use statistical models, which is kind of the current setting.
[00:11:45] And this was in the 1980s kind of
[00:11:50] pioneered by Fred Yelenik at IBM and others around the same time.
[00:11:56] Statistical models became very,
[00:11:58] very popular to be used in speech recognition.
[00:12:02] And the entire problem was formulated as a noisy channel.
[00:12:05] And one of the main machine learning paradigms, which was
[00:12:08] used for this particular problem were hidden Markov models.
[00:12:12] So I'll come to this not too much in detail, but at least,
[00:12:15] at the high level, I'll refer to those in coming slides.
[00:12:19] So, the statistical models were able to
[00:12:22] generalize much better than the previous models
[00:12:25] because the previous models are all kind of rule-based.
[00:12:28] And now, we are moving into 10K vocabulary sizes.
[00:12:32] So, the vocabulary size is getting larger, and
[00:12:35] these are now kind of falling in what are known as large
[00:12:39] vocabulary continuing speech recognition systems.
[00:12:42] Although of course, now, large vocabulary is much larger than
[00:12:46] 10K, but that was in the 80s.
[00:12:48] And we were in this plateau phase for a long time.
[00:12:51] And in 2006, deep neural networks kind of came to
[00:12:56] the forefront, and now all the state-of-the-art
[00:13:00] systems are powered by deep neural networks.
[00:13:04] So any of these systems you might have used, Cortana,
[00:13:08] Siri, Voice Search, at the backend,
[00:13:12] they're powered by deep neural network based models.
[00:13:16] So okay,
[00:13:17] so this is just a video, which was actually quite impressive.
[00:13:20] And this happens to be by the CFO of Microsoft, Rick Rashid.
[00:13:25] And this was a really impressive video.
[00:13:29] So this came out in 2012 when Microsoft had completely
[00:13:34] shifted to deep neural based models in the back end, I mean,
[00:13:38] even in the production models.
[00:13:40] And this, actually, so he's speaking, and in real time,
[00:13:43] the speech recognition system is working and giving transcripts.
[00:13:48] And you'll see that
[00:13:48] the quality of the transcriptions is really good.
[00:13:52] And while the transcriptions were being displayed on
[00:13:55] the screen, they were also doing translation into Chinese.
[00:14:00] And so there was another screen, where the MT system,
[00:14:03] the machine translation system, was working and
[00:14:06] producing real time Mandarin transcripts.
[00:14:09] So it was a very impressive demo, and I'm told it was not,
[00:14:13] maybe Sirena knows more about the demo itself, but
[00:14:17] [CROSSTALK] >> Came together to develop
[00:14:19] another breakthrough in the field of speech recognition
[00:14:23] research.
[00:14:26] The idea that they had was to use a technology
[00:14:30] in a way patterned after the way the human brain works.
[00:14:33] It's called deep neural networks.
[00:14:35] And to use that to take in much more data than had previously
[00:14:42] been able to be used with the hidden Markov models and
[00:14:46] use that to significantly improve recognition rate.
[00:14:52] So that one change, that particular breakthrough,
[00:14:55] increased recognition rates By approximately 30%.
[00:14:58] That's a big deal.
[00:15:00] That's the difference between- >> Okay, so
[00:15:03] you can see the transcripts are pretty faithful to the speech.
[00:15:08] And this, it was actually happening real time.
[00:15:11] So that's very impressive.
[00:15:14] Okay, so given all of this, so
[00:15:16] you might be wondering what's next.
[00:15:18] So whenever I tell people I work on speech recognition,
[00:15:22] I'm asked this question many times.
[00:15:24] Isn't that problem solved?
[00:15:25] So what are you doing?
[00:15:27] What are you continuing to work on?
[00:15:29] So okay, so just to kind of motivate this question, and also
[00:15:32] kind of related to the topic that our team is working on,
[00:15:36] which is accent adaptation.
[00:15:37] I'll show a video of our 12th president of India.
[00:15:42] So this is Pratibha Patil.
[00:15:44] So she is sitting in a closed room, and she's giving a speech.
[00:15:48] And this is YouTube's automatic captioning system which is
[00:15:53] working, so this is the early state of the art ASR system.
[00:15:58] And I got this a few months back, so
[00:16:00] let's look at the video.
[00:16:01] >> It is this that will define India as a unique country on
[00:16:05] the world platform.
[00:16:07] India is also an example of how economic growth can be achieved
[00:16:12] within a democratic framework.
[00:16:15] I believe economic growth should translate into the happiness and
[00:16:19] progress of all.
[00:16:21] Along with it there should be development of art and
[00:16:25] culture,literature and education, science and
[00:16:29] technology.
[00:16:30] We have to see how to harness the many resources of India for
[00:16:35] achieving common good and for inclusive group.
[00:16:39] >> Okay, so the words in red of course are the erroneous words,
[00:16:44] and this is not bad at all.
[00:16:45] So if you look at this metric which is typically used to
[00:16:49] evaluate ASR systems, so it's the word error rate.
[00:16:52] So if you take this entire word sequence and you take the true
[00:16:57] word sequence, and you compute any distance between these.
[00:17:02] So just align these two sequences and
[00:17:04] compute where the words that actually swapped for
[00:17:08] other words and where certain words are inserted, and
[00:17:10] where certain words are deleted, and you get this error rate.
[00:17:13] And that's 10%, which is fairly respectable, so that's not bad.
[00:17:17] And that's because Google has a very, very,
[00:17:20] well developed Indian English ASR system, and Google actually
[00:17:24] calls all of these variants of English different languages.
[00:17:28] So they have Indian English, Australian English,
[00:17:32] British English, various variants of English, and
[00:17:36] their system is extremely sophisticated for
[00:17:40] Indian English.
[00:17:41] >> [INAUDIBLE] >> Yeah, it's clean, it's quiet,
[00:17:44] exactly, yeah.
[00:17:45] So now, let's take speech from our 11th president who is
[00:17:49] Abdul Kalam, who, and
[00:17:51] why I picked him is because he has a more pronounced accent.
[00:17:55] Most of you must have heard his speech at some point.
[00:17:59] So, let's look at how- >> [INAUDIBLE] Which any human
[00:18:03] being can ever imagine to fight.
[00:18:06] And never stop fighting until you are able to destined place,
[00:18:10] that is the unique you.
[00:18:13] Get that unique you.
[00:18:16] It's a big battle.
[00:18:18] The back in which you don't you take a the battlements
[00:18:23] you have out for unique needs, for you need to do is you
[00:18:27] must have that battle, one is you have to set the goal.
[00:18:31] The second one is acquire the knowledge and
[00:18:35] third one is a hard work with devotion.
[00:18:38] And forth is perseverance.
[00:18:41] >> Okay, so I'm actually curious, Allen,
[00:18:43] how do you think you would have done with recognizing this?
[00:18:48] >> Well, I would definitely make errors.
[00:18:50] >> Yeah. >> Okay,
[00:18:51] because he is much more heavily accented.
[00:18:54] And what's really hard is, you can follow the transcript,
[00:18:59] I'm thinking, Yeah it looks exactly like that.
[00:19:02] >> [LAUGH] >> [CROSSTALK] Listening to it
[00:19:04] and not being right.
[00:19:06] >> And I'm assuming most of us in the room are definitely going
[00:19:09] to do better than this, right?
[00:19:10] Definitely better than 39%.
[00:19:13] So actually, when I've shown this video before, and
[00:19:16] some people from the crowd said that this is not fair,
[00:19:19] because not only, cannot entirely attribute it to
[00:19:22] accent because he's in this large room.
[00:19:24] It's more reverberant than the previous video.
[00:19:28] His sentence structure is quite non standard,
[00:19:31] like he moves in and out of various sentences.
[00:19:34] So this end, of course, reading.
[00:19:36] So the read speech has a very, very different kind
[00:19:39] of grammatical structure than this, right?
[00:19:42] So I said, okay, let's try to make it fairer, right?
[00:19:45] So I chose someone who is an American English speaker, but
[00:19:50] has an accent, because my hypothesis is that accent had
[00:19:53] a lot to do with this missed recognition rate getting higher.
[00:19:58] So, this is an American English speaker who has a strong accent
[00:20:02] and has very non-standard word order.
[00:20:05] And so,
[00:20:06] an obvious choice was Sarah Palin, if you know who she is.
[00:20:09] Most of you know who Sarah Palin is, okay.
[00:20:11] >> The illegal immigrants welcoming them in,
[00:20:14] even inducing and seducing them with gift baskets.
[00:20:17] Come on over the border and
[00:20:19] here's a gift basket full of teddy bears and soccer balls.
[00:20:22] Our kids and our grandkids, they'll never know then what it
[00:20:26] is to be rewarded for that entrepreneurial spirit that
[00:20:30] God creates within us in order to work, and to produce, and
[00:20:34] to strive, and to thrive, and to really be alive.
[00:20:38] Wisconsin, Reagan saved the hog here, your Harley Davidson.
[00:20:45] It was Reagan who saved- >> Okay, so if I were to try and
[00:20:50] predict what the next word is, given her word context,
[00:20:53] there's no way I could reproduce this.
[00:20:56] It was quite arbitrary, right?
[00:20:57] You have no idea what she's gonna say next.
[00:21:00] >> If you showed me that transcription, I would say,
[00:21:02] well, it's clearly mostly wrong.
[00:21:05] >> [LAUGH]
[00:21:06] >> Nobody could actually say that.
[00:21:06] >> So, here, clearly, language model can only help so much,
[00:21:09] cuz this is really, it's quite arbitrary.
[00:21:11] She has a strong accent, but YouTube's ASR engines
[00:21:14] do have a lot of southern dialects in their training data.
[00:21:20] And she's also speaking to a large crowd in the open.
[00:21:23] So the acoustic conditions are somewhat similar to
[00:21:25] the previous video.
[00:21:27] And the only difference is that the speaker in the previous
[00:21:30] video had a much more pronounced accent.
[00:21:32] So I'm not saying that it entirely had to do with
[00:21:35] the degradation performance.
[00:21:37] But that certainly was a major factor in why the speech
[00:21:40] recognition engine didn't do as well, yes?
[00:21:43] >> The second time it picked up correctly gift basket, but
[00:21:48] the first time it says your basket, so-
[00:21:51] >> Is that a-
[00:21:56] >> The illegal immigrants,
[00:21:57] welcoming them in even inducing and
[00:22:00] seducing them with gift baskets.
[00:22:02] Come on over the border- >> So, you see-
[00:22:05] >> Like it could not [INAUDIBLE]
[00:22:07] for the first ten minutes, and it said you all, but
[00:22:10] the next time, it correctly identified [CROSSTALK].
[00:22:14] >> I see, I see, the second, yeah, yeah, yeah, yeah.
[00:22:17] >> What would be the- >> So, and
[00:22:19] there are multiple things here at play.
[00:22:21] So maybe after I show the structure of an ASR system,
[00:22:24] I can come back to this question.
[00:22:29] Any other questions so far?
[00:22:30] Okay.
[00:22:35] Let's actually move into what's the structure of
[00:22:39] a typical ASR system?
[00:22:41] So this is more or
[00:22:42] less the pipeline of what's typically in an ASR system.
[00:22:49] So you have an acoustic analysis component, which sees the speech
[00:22:54] waveform and converts it into some discrete representation.
[00:22:59] And, or features,
[00:23:01] if most of you are familiar with the term features.
[00:23:04] So the features are then feed in to what's known
[00:23:08] as acoustic model.
[00:23:10] So actually instead of explaining each of components
[00:23:13] here, I'll kind of go into each of these individual and
[00:23:16] explain it more.
[00:23:18] So the very first component is just looking at the raw speech
[00:23:22] waveform and converting it into some representation,
[00:23:25] which your algorithms can use.
[00:23:28] This is a very high level, so there is a lot of underlying
[00:23:31] machinery and I am just giving you an overview of
[00:23:34] what is going on, so you have the raw speech signal.
[00:23:37] Which then was discretize,
[00:23:39] because you can't really work with a speech signal.
[00:23:43] So, you sample it and generate these discrete samples.
[00:23:47] And of each of these samples are typically of the order of 10 to
[00:23:52] 25 milliseconds of speech.
[00:23:54] And the idea is that once you have each of these
[00:23:57] what we know as frame, so speech frames,
[00:24:00] which are free round 25 sometimes even larger.
[00:24:05] But typically 25 milliseconds.
[00:24:07] Then you can extract acoustic features,
[00:24:09] which are representative of all the information in your signal.
[00:24:15] And another reason why you discretize at particular
[00:24:20] sampling rates is that the assumption is that
[00:24:22] within each of these frames your speech signal is stationary.
[00:24:24] If your speech signal is not stationary within
[00:24:29] the speech frames, then you can't effectively
[00:24:33] extract features form that particular slice.
[00:24:37] So, around 25 milliseconds of speech, yeah.
[00:24:42] So, you extract features, and
[00:24:44] this feature extraction is a very involved process, and
[00:24:48] it requires a long of signal processing know how.
[00:24:51] But this is also kind of motivated by how our ears work,
[00:24:55] so actually, one of the most.
[00:24:56] Common acoustic feature of presentations,
[00:24:59] which are known as Mel-frequency cepstral coefficients or MFCCs.
[00:25:02] They're actually motivated by what goes on in your ear or
[00:25:06] the filter banks, which apply in your ear.
[00:25:10] So that might be too much detail, so
[00:25:12] let's just think of it as follows.
[00:25:14] So you'll start with your raw speech wave form.
[00:25:16] You'll generate these tiny slices which are also known as
[00:25:20] speech frames.
[00:25:21] And now each speech frame is going to be represented as some
[00:25:25] real valued vector of features, which is capturing all
[00:25:28] the information and as well as possible is not redundant.
[00:25:32] So you don't have different dimensions here,
[00:25:35] which are redundant, so you want it to be as compact as possible.
[00:25:38] So, now you have these features for each frame, and now these
[00:25:43] are your inputs to the next component in the ASR system,
[00:25:46] which is known as the acoustic model.
[00:25:49] And it's a very important component.
[00:25:52] So, before I go into what an acoustic model is, for anyone
[00:25:57] plotting this cloud, everyone knows what a phoneme is.
[00:25:59] Cuz lots of linguists and
[00:26:01] many of you might have encountered it.
[00:26:03] But anyway, so a phoneme is just a discrete unit.
[00:26:08] It's a speech sound in a language,
[00:26:10] which can be used to differentiate between words.
[00:26:13] So in ASR, there is this approach,
[00:26:18] which is known as beads-on-a-string approach.
[00:26:22] And this is my terrible drawing of beads on a string.
[00:26:26] But each word can be represented as a sequence of phonemes.
[00:26:32] So five here is a sequence of three of these speech sounds.
[00:26:37] So the phoneme alphabet is very much like the alphabet for
[00:26:41] our languages, so in text, except now,
[00:26:45] it's covering the sound space, rather than the textual space.
[00:26:51] So phonemes are just the letter equal to the analogy of phonemes
[00:26:54] as letters in your written texts.
[00:26:57] And each word can be represented as a sequence of phonemes.
[00:27:01] So this mapping, so you might be wondering, how do you know that
[00:27:05] five actually maps to this sequence of phonemes?
[00:27:07] This is written down by experts in the language.
[00:27:12] So this particular mapping between the pronunciation of
[00:27:15] a word, so this is actually giving you how this particular
[00:27:18] word is pronounced.
[00:27:19] Because you know how each individual phoneme is
[00:27:22] pronounced, and this pronunciation information is
[00:27:25] actually given to us by experts.
[00:27:26] So in English, of course,
[00:27:28] we have a very well developed pronunciation dictionaries,
[00:27:31] where experts have given us pronunciations corresponding to
[00:27:35] most of the commonly occurring words in English.
[00:27:38] And actually we have CMU to thank for that, so
[00:27:41] one of the most popularly used translation dictionaries in
[00:27:44] English is CMUdict, which is freely available.
[00:27:47] And it has around 150,000 words, I think?
[00:27:50] Yeah, of that order.
[00:27:52] And that is actually one of the more extensive dictionaries.
[00:27:55] So typically, this is not a very easy resource to create.
[00:28:00] And it's clear why, because it's pretty tedious.
[00:28:04] First of all, you need to find linguistic experts in
[00:28:06] the language.
[00:28:06] And then you need to find what are the most commonly occurring
[00:28:09] words in the language, and so on.
[00:28:11] So this takes time.
[00:28:13] And not many languages have very well developed
[00:28:16] pronunciation dictionaries.
[00:28:18] And most languages have around 20 to 60 phonemes.
[00:28:20] So the phoneme inventory size is roughly 20 to 60.
[00:28:23] And this is also something which needs to be determined by
[00:28:27] experts.
[00:28:28] What are the phonemes which are applicable to a language?
[00:28:30] So this is a very language-dependent
[00:28:34] characterization, like what are the phonemes which are relevant
[00:28:37] to a particular language?
[00:28:39] Okay, so given we have these units, okay, so
[00:28:44] one more slide just to motivate,
[00:28:47] why do we need phonemes, even from a modeling standpoint.
[00:28:51] So not just from the linguistic standpoint,
[00:28:53] which is each of these sounds
[00:28:56] can be kind of discrete as in terms of these phonemes.
[00:28:58] But even from a modelling standpoint,
[00:28:59] why are phonemes useful?
[00:29:01] Why not just use words,
[00:29:03] instead of trying to split it into these subword units?
[00:29:06] So let's look at a very simple example.
[00:29:08] So say that your speech wave form is this string of digits,
[00:29:12] five, four, one, nine.
[00:29:13] And say that during training, you've seen lots and
[00:29:16] lots of samples of five, four and one.
[00:29:20] So, now you can build models to identify when someone said five,
[00:29:24] and when someone said four, and when someone said one.
[00:29:28] But when you come to nine, so this is, say, during test time,
[00:29:31] when you are evaluating this particular speech utterance.
[00:29:34] What do you then if, during training,
[00:29:36] you've never seen nine?
[00:29:38] Of course, this is not reasonable here because it is
[00:29:40] a very small vocabulary, but you can extrapolate when you
[00:29:43] move to larger vocabularies, right?
[00:29:45] So yeah, all of these words exist, but
[00:29:48] what do you do when you come here?
[00:29:50] What if you were to represent each of these words as their
[00:29:53] corresponding sequences of phonemes?
[00:29:56] So now five is this sequence of phonemes, four is this sequence
[00:30:00] of phonemes, one is this sequence of phonemes, and so on.
[00:30:03] And now you've seen acoustic speech samples,
[00:30:07] which correspond to each of these phonemes in your training.
[00:30:10] So during test time, when you see nine, you
[00:30:14] might be able to put together this string of phonemes.
[00:30:17] Because you've seen enough acoustic evidence for
[00:30:20] each of these individual phonemes, is that clear?
[00:30:24] So it helps you generalize,
[00:30:26] just to move to a more fine-grained inventory.
[00:30:30] But of course, with that said,
[00:30:32] if you have a very limited vocabulary task.
[00:30:35] I mean, say that you're almost certain that during test time
[00:30:39] you're only going to get utterances,
[00:30:41] which are going to stick to that particular vocabulary.
[00:30:45] And if you have enough samples during training,
[00:30:47] you're probably well off just building word level models, and
[00:30:50] not even moving to the phoneme level.
[00:30:52] But that is for very limited tasks, so
[00:30:55] most tasks you want to do this.
[00:30:57] So you want to move to this slightly more fine-grained
[00:31:00] representation.
[00:31:01] Okay, so that hopefully motivates why we need phonemes.
[00:31:06] So this is the problem, right?
[00:31:07] So I mentioned you have acoustic features which you extract from
[00:31:11] your raw speech signal.
[00:31:13] And you want the output on this acoustic model to be what is
[00:31:16] a likely phone sequence,
[00:31:18] which corresponded to this particular speech utterance.
[00:31:22] So this model is typically, so initially in the 80s and
[00:31:27] even now actually, Hidden Markov models is a paradigm which is
[00:31:31] used to learn this mapping.
[00:31:33] So how do I associate a set of frames, a set of features?
[00:31:39] So when I say frames and features,
[00:31:40] they're kind of interchangeable, right?
[00:31:43] So each of these acoustic-feature vectors
[00:31:45] corresponds to a speech frame.
[00:31:47] So how do I chunk, how many frames are going to correspond
[00:31:51] to a particular phone?
[00:31:52] And here I've shown you a chain of what are known
[00:31:56] as hidden states, in your Hidden Markov Model.
[00:32:02] So this is just like, think of it as a graph.
[00:32:05] And it's a weighted graph, so here I've not put weights on
[00:32:08] the axis, but the weights are all probabilities.
[00:32:11] So another thing is here, I've just shown you a single chain
[00:32:15] that is just a sequence of these phones put together.
[00:32:18] But you never know that right?
[00:32:19] So at each point you can transition to any phone,
[00:32:22] because you don't know which phone is going to appear next.
[00:32:25] So the entire model is probabilistic.
[00:32:28] So you need to have lots of hypotheses as to what
[00:32:31] the next phone could have been?
[00:32:33] So here I have obviously simplified it by just showing
[00:32:36] a single chain.
[00:32:37] And then you have estimates which say that okay,
[00:32:40] I think this initial ten frames most likely corresponds to
[00:32:44] a certain phone.
[00:32:46] And the transition properties,
[00:32:47] the properties which transition from one phone state to
[00:32:50] the other determine how many you are going to chunk.
[00:32:53] How many speech frames are going to correspond to each phone.
[00:32:56] And once you're in the particular state,
[00:32:59] there are properties for having generated each of these vectors.
[00:33:03] So once I'm in, let's say this state, there's a probability for
[00:33:07] having seen this vector, given that I'm in this state.
[00:33:11] And those properties come from what are known as
[00:33:14] Gaussian Mixture Models.
[00:33:16] So it's a probability distribution which determines
[00:33:19] that okay, once I'm in this particular state,
[00:33:21] this particular speech vector could be
[00:33:24] generated with a certain probability.
[00:33:26] And how are these probabilities learned?
[00:33:28] From training data, so
[00:33:30] that is the detail I'm not going to go into, yeah.
[00:33:33] >> [INAUDIBLE] >> Yeah,
[00:33:36] this is just the acoustic vector.
[00:33:40] >> That's it, yeah.
[00:33:43] So, any questions so far?
[00:33:46] Okay, so this has obviously glossed over lots and
[00:33:51] lots of details.
[00:33:52] But this is just to give you a high level idea of,
[00:33:55] you have a probabilistic model, which maps sequences of feature
[00:34:00] vectors to a sequence of phonemes.
[00:34:06] So Hidden Markov Models were the state-of-the-art for
[00:34:08] a long time.
[00:34:10] And now, of course, we have Deep Neural Networks,
[00:34:12] which are used for a similar mapping.
[00:34:16] So now you have your speech signal and
[00:34:18] again, you're extracting six windows of speech frames.
[00:34:23] And from these, so
[00:34:24] say that you're only considering a speech frame here.
[00:34:27] And then you have, well, I have a laser pointer.
[00:34:32] Here, so say considering a speech frame here.
[00:34:36] And then you look at a fixed window around it,
[00:34:39] a fixed window springs around it.
[00:34:41] And you generate, put all of these features together and
[00:34:44] that is your input to a deep neural network.
[00:34:48] And the output is what is the most likely phone to have been
[00:34:51] produced, given this particular set of speech rates.
[00:34:56] But this is a posterior priority over the phones.
[00:35:01] So I'm not going to go into details about what this is.
[00:35:03] But, again, here you get an estimate of what
[00:35:06] is the phone given a speech frame.
[00:35:09] What is the most likely phone?
[00:35:10] So it's actually a priority distribution over all
[00:35:13] the phones.
[00:35:13] And there are two ways in typically how DNNs is used
[00:35:18] in acoustic models.
[00:35:20] So one is, in the previous slide I mentioned,
[00:35:24] when you have HMMs, you have these states and
[00:35:28] you have these priority distributions, which govern how
[00:35:32] the speech vectors correspond to particular states.
[00:35:37] And these priority distributions are mixtures of Gaussian.
[00:35:41] But you could kind of not use mixtures of Gaussian here and
[00:35:45] instead use probabilities from your DNN.
[00:35:48] So that is one way in which the DNN and the HMM models can be
[00:35:52] combined and used within an acoustic model.
[00:35:56] So please feel free to stop and ask me any question.
[00:36:00] So at this point, I'm not really clear if I'm going too
[00:36:05] technical, so please feel free to interrupt at any point.
[00:36:10] So the idea is that we want to map acoustic features to phone
[00:36:13] sequences.
[00:36:14] And this is all probabilistic, so
[00:36:16] we are not giving you a one best sequence.
[00:36:18] We are saying this is the likely priority distribution of
[00:36:21] phone sequences.
[00:36:22] Okay, so that is the output from our acoustic model.
[00:36:25] Yes?
[00:36:26] >> Yeah, [INAUDIBLE].
[00:36:27] >> Yeah.
[00:36:29] >> [INAUDIBLE] acoustic?
[00:36:36] >> Yes, exactly, acoustic features, and
[00:36:39] then you have priority distributions.
[00:36:41] >> How will [INAUDIBLE]?
[00:36:45] >> So the priority distribution for the, so
[00:36:47] you're familiar with HMMs.
[00:36:49] So you have observation probabilities.
[00:36:51] So your observation properties,
[00:36:52] either they can be Gaussian mixture models.
[00:36:54] Or your observation properties can be scaled posteriors from
[00:36:58] your DNNs.
[00:36:58] So it's just the priority distribution, your observation
[00:37:02] priority distribution can come from the DNN, yeah.
[00:37:07] Okay, so this is the acoustic module,
[00:37:10] which produces phone sequences.
[00:37:12] So now, we eventually want to get a word sequence, right,
[00:37:15] from the speech utterance.
[00:37:17] So this is just an intermediate representation, these phones.
[00:37:21] So now how do I move from the phones to words?
[00:37:24] So I mentioned we use
[00:37:26] these large pronunciation dictionaries.
[00:37:28] So this the model,
[00:37:29] which provides a link between these phone sequences and words.
[00:37:35] So here, typically just a simple dictionary of pronunciations
[00:37:38] is maintained.
[00:37:39] So you have these large dictionaries which say that
[00:37:42] there words correspond to these sequences of phones.
[00:37:44] And this is the only module in an ASR system that is not
[00:37:48] learned.
[00:37:49] It's not learned from data.
[00:37:50] So the acoustic model was learned from training data, and
[00:37:54] we'll come to the language model that is also learned from data.
[00:37:57] But the pronunciation model is actually expert derived.
[00:38:01] So an expert gives you these mappings.
[00:38:04] So I'll talk a little about some work I did during my thesis,
[00:38:08] which was on pronunciation models.
[00:38:11] It's kind of hinting at how restricted
[00:38:15] this particular representation is.
[00:38:17] So I mentioned that each word can be represented as a sequence
[00:38:21] of phonemes.
[00:38:23] So we looked at a very popular speech corpus called
[00:38:27] Switchboard, a subset of Switchboard.
[00:38:29] It's annotated very detailed level.
[00:38:33] So not only do we have board sequences
[00:38:36] corresponding to the speech.
[00:38:38] We also have phonetic sequences.
[00:38:40] So it's also phonetically transcribed.
[00:38:42] Meaning someone listened to all of the utterances and wrote down
[00:38:47] the phone sequence corresponding to what they heard.
[00:38:51] And this was obviously done by linguists.
[00:38:53] And when I say phone,
[00:38:54] they actually listened to how the word was pronounced.
[00:38:57] Not what the word should have been according to some
[00:39:00] dictionary.
[00:39:02] And why I'm saying this is because there's lot of
[00:39:04] pronunciation variation when you actually speak, right?
[00:39:07] So, certain words, even though the dictionary says that it
[00:39:10] should be pronounced a certain way, because of our accents or
[00:39:13] just because you're talking fast and so on, the word actually
[00:39:16] ends up being pronounced in an entirely different way.
[00:39:19] So for some data from this corpus,
[00:39:21] we actually had phonetic transcriptions which
[00:39:24] are giving us exactly how people pronounce those words.
[00:39:28] So one thing that really stands out from the data, so
[00:39:31] let's look at just four words.
[00:39:33] So this probably, sense, everybody and don't.
[00:39:36] And row in blue, the phone sequences corresponding to these
[00:39:40] words, according to a dictionary.
[00:39:42] So this is how the word should be pronounced according
[00:39:46] an American, so this is the American pronunciations.
[00:39:51] And these were the actual pronunciations from the data
[00:39:54] as transcribed by a linguist.
[00:39:56] So obviously, what is the first thing that stands out here?
[00:40:01] >> There's >> Yeah, definitely there is no
[00:40:05] one pronunciation corresponding to the word.
[00:40:08] There are lots of possible pronunciations,
[00:40:10] and you'll also see, this is, you'll see lots of
[00:40:15] like inter syllables are being dropped out of words.
[00:40:18] >> [INAUDIBLE] >> Yeah, speaking very fast.
[00:40:22] >> [INAUDIBLE] >> It's wrong, but
[00:40:24] it's completely legible from the speech,
[00:40:26] just because of the context and so on.
[00:40:28] But they're speaking very fast, so
[00:40:31] if you actually looked at the phonetic transcriptions,
[00:40:35] there are entire syllables missing, and of course these
[00:40:38] are also perfectly legitimate pronunciations.
[00:40:41] So since, when you say the word,
[00:40:44] it almost feels like you're inserting a tuh at the end,
[00:40:47] before the last suh sound, sense.
[00:40:50] So there are lots of alternate pronunciations for words, and
[00:40:54] I don't remember the exact number.
[00:40:57] But I think the average number of pronunciations they found for
[00:41:00] a word was of the order of four or five, so
[00:41:02] very far from a single pronunciation for a word.
[00:41:05] Okay, so we thought, so
[00:41:07] clearly there's a lot of pronunciation variation, and
[00:41:10] this was from a corpus which was of conversational speech.
[00:41:13] So it's not read speech,
[00:41:14] where people are speaking very fast and so on.
[00:41:16] Read speech tends to be more clearer and they enunciate, and
[00:41:20] they tend to stick more to the dictionary pronunciations.
[00:41:24] But of course, you want to recognize conversation speech,
[00:41:26] you're not always only going to recognize news broadcasters.
[00:41:29] You need to recognize spontaneous,
[00:41:32] day to day speech, so how do we kind of try and
[00:41:35] model this pronunciation variation?
[00:41:37] How do we computationally model this, and so we thought,
[00:41:40] why not go to the source, so
[00:41:43] what is creating these transition variations?
[00:41:46] So it's your speech production system, so there are various, so
[00:41:49] before going into that, I'll show you these videos from
[00:41:54] the SPAN group at USC, which is led by.
[00:41:58] And they do really good work on speech production based models,
[00:42:01] to model pronunciation variation and so on.
[00:42:04] So this is an MRI of the vocal tract and
[00:42:07] it's synched with the audio, so.
[00:42:10] >> When it comes to singing, I love to sing French art songs,
[00:42:13] it's probably my favorite type of song to sing.
[00:42:17] I'm a big fan of Debussy, I mean, I also love operas,
[00:42:21] I love singing [INAUDIBLE] and Mozart and Strauss.
[00:42:26] But when i listen to music,
[00:42:27] I tend to listen to hard rock or classic rock music.
[00:42:30] One of my favorite bands is AC/DC,
[00:42:33] and my favorite song is probably Back in Black,
[00:42:37] which I'll listen to over and over again in my room.
[00:42:41] >> Okay, so these various parts of the vocal tract
[00:42:44] which are moving are known as articulators.
[00:42:47] And the articulators move in various configurations and
[00:42:51] lead to certain speech sounds being produced.
[00:42:54] So they did some really cool work on actually-
[00:42:56] >> These are the movements that
[00:42:57] shape the z sounds.
[00:42:59] >> Tracking the articulators automatically,
[00:43:02] this is really cool.
[00:43:03] So we didn't actually use these continuous counters,
[00:43:08] but we said, let's discretize the space.
[00:43:12] So that all these various articulators, which move
[00:43:15] under various configurations of these articulators,
[00:43:18] which lead to various speech sounds being produced.
[00:43:21] So if we can discretize the space and say that, okay,
[00:43:24] there are eight vocal tract variables, and
[00:43:28] each of these variables can take one of n values.
[00:43:31] Then different value assignments to these tract variables
[00:43:36] can lead to different sounds.
[00:43:38] And this didn't just come out of the blue,
[00:43:41] there's a lot of linguistic analysis on speech production.
[00:43:44] And there's lots of very well-developed linguistic
[00:43:47] theories on speech production.
[00:43:49] And we used one of them, which is known as articulatory
[00:43:52] phonology, so we'll come to that in a single slide.
[00:43:55] So now,
[00:43:56] everybody which used to be the sequence of phones, can now be
[00:44:00] represented as these streams of articulatory features.
[00:44:04] So these,
[00:44:04] if you have each variable which states different values.
[00:44:08] Now you will have these quasi-overlapping streams,
[00:44:12] articulatory features, which lead to a particular word and
[00:44:15] how it's being pronounced.
[00:44:16] And so why do I say they are overlapping,
[00:44:19] because they're not entirely independent, so
[00:44:22] one feature can affect how another feature behaves.
[00:44:26] So we kind of got inspiration from this work on this theory
[00:44:32] called articulatory phonology, by Browman and Goldstein.
[00:44:38] But they said that this representation of speech as
[00:44:41] just sequences of phonics, it's very, very constrained, and
[00:44:44] it's very restrictive.
[00:44:46] So let's think of speech as being represented as multiple
[00:44:49] streams of articulatory movements.
[00:44:52] And that actually gives you a much more elegant framework
[00:44:54] to represent pronunciation variation So
[00:44:58] if I have to go back to he previous slide where I showed
[00:45:01] you all the various pronunciations.
[00:45:03] To try and kind of motivate how you went from the dictionary
[00:45:07] pronunciation of probably to one of these things,
[00:45:10] it would require kind of deleting three phones, inserting
[00:45:14] some other phone, a huge at a distance in terms of phones.
[00:45:18] So how do you actually motivate such a large deviation in
[00:45:21] pronunciation?
[00:45:22] It turns out that if you represent pronounciations as
[00:45:25] these streams of features, you can explain transition variation
[00:45:29] in terms of asynchrony between these feature strips.
[00:45:32] So just because of certain features are not
[00:45:37] synchronously moving.
[00:45:40] Say that you're producing a nasal sound, and
[00:45:42] your next sound that you're producing is a bubble, but
[00:45:46] then there's certain remnants of the nasality which hold on.
[00:45:50] And so your bubble also becomes a little nasalized, and so on.
[00:45:55] So there was an example which I thought may not have
[00:45:59] time to go and do so, the idea is that this
[00:46:03] articulately featured framework gives you a more
[00:46:08] elegant explanations of pronunciation variation.
[00:46:13] It's certainly more elegant, but it's very hard to model, and
[00:46:18] we learned that the hard way.
[00:46:20] I did during my thesis.
[00:46:22] So we use this representation and
[00:46:26] we built what is in the olden days, these are called DBNs.
[00:46:31] Which is not Deep Belief Networks,
[00:46:33] it's Dynamic Belgian Networks, so it's the olden day DBN.
[00:46:37] So it's just a generalization of Hidden Markov Model.
[00:46:40] So the Hidden Markov Model that I described in the acoustic,
[00:46:42] when I was talking about acoustic models.
[00:46:45] This is just a generalization of that particular paradigm.
[00:46:49] So you have various variables which represent each of these
[00:46:53] articulatory features.
[00:46:54] And then you are represent constraints between these
[00:46:57] variables and so on.
[00:47:00] >> [INAUDIBLE] >> Yeah,
[00:47:05] yeah I wish I had that slide actually.
[00:47:10] If you don't mind, can I come to this at the end, because there's
[00:47:12] a slide which clearly shows- >> [INAUDIBLE]
[00:47:19] >> Yes, yes.
[00:47:21] >> [INAUDIBLE] >> Yes.
[00:47:25] So now, okay, actually we can take that as an example.
[00:47:27] So fur.
[00:47:29] So now I'll say fur.
[00:47:30] So now I'll break the fur sound into these eight variables and
[00:47:34] the values it takes.
[00:47:36] The values it takes to produce the sound fur.
[00:47:39] So you're- >> But one to
[00:47:40] one map [INAUDIBLE] >> It's not,
[00:47:42] it's actually not a one to one map.
[00:47:43] So we left it, we kept it probabilistic.
[00:47:45] So it is mostly one to one, but it's not entirely one to one.
[00:47:51] So we did allow for- >> One to one
[00:47:55] [INAUDIBLE] >> Yeah, yeah.
[00:47:58] >> Then wouldn't
[00:47:59] have the space to- >> It's not
[00:48:01] a one-to-one mapping. Yeah.
[00:48:02] It's not a one-to-one mapping.
[00:48:03] But even if it was.
[00:48:04] Yeah, so actually if I show you that example slide,
[00:48:07] I can clearly explain it, so
[00:48:08] please remind me at the end of the talk.
[00:48:10] I would like to show that.
[00:48:13] Okay, so that was the pronunciation model.
[00:48:17] And the final model is what's known as the language model,
[00:48:19] which many of you might actually be quite familiar with.
[00:48:22] So language model is just saying, so
[00:48:24] again the pronounciation model, the output was words.
[00:48:26] So now you've mapped a phone sequence to a particular word,
[00:48:30] and now the language model comes and says how should these words
[00:48:33] be ordered, according to a particular language?
[00:48:36] So the language model looks at lots and
[00:48:37] lots of texts in that particular language.
[00:48:40] And it finds occurrences of words together, and yeah,
[00:48:45] you have a question?
[00:48:51] >> [INAUDIBLE] >> But,
[00:48:59] so now, now we are coming to this language model.
[00:49:01] What about going from the phoneme sequences to words?
[00:49:03] >> The pronunciation model.
[00:49:05] So, this one, right?
[00:49:07] So the phone sequence.
[00:49:09] Once I get a phone sequence, I can start mapping
[00:49:12] chunks of the phones to valid words in the pronunciation.
[00:49:15] >> [INAUDIBLE] >> Yes.
[00:49:18] >> [INAUDIBLE] >> Yes, absolutely.
[00:49:23] So the thing is,
[00:49:23] you're not getting a single phone sequence, right?
[00:49:25] So it's probabilistic.
[00:49:27] So you have properties for every phone sequence appearing.
[00:49:31] And so even if it doesn't exactly match,
[00:49:32] maybe it will exactly match it with a lower probability.
[00:49:35] But then the language model also comes in and
[00:49:38] then the property when you add up,
[00:49:41] then you get kind of the most likely sequence here. Yes?
[00:49:45] >> [INAUDIBLE] pronunciation
[00:49:47] models [INAUDIBLE] >> Yes,
[00:49:49] they're usually not it's determined state.
[00:49:53] You just have one sequence of, typically you just have
[00:49:56] one sequence of phones which corresponds to a word.
[00:50:01] But it can be probabilistic, also.
[00:50:03] >> [INAUDIBLE] >> Yeah, exactly, the one I was
[00:50:06] building was too probabilistic, [LAUGH] too many probabilities.
[00:50:14] Okay, so here of course, so if you saw the word contex,
[00:50:18] the dog.
[00:50:19] Obviously the most likely next word to follow this particular
[00:50:23] word context is ran, maybe even can, but definitely not pan.
[00:50:27] So pan would have a very,
[00:50:30] very low probability of following the dog.
[00:50:34] And the language model is also coming to,
[00:50:36] actually related to your question.
[00:50:37] The language model is very crucial because it can be used
[00:50:41] to disambiguate between similar acoustics.
[00:50:43] So say that our transverse is, the baby crying.
[00:50:47] It could also very well map to this particular word sequence,
[00:50:50] but obviously the first word sequence is much more likely.
[00:50:54] Because if you look at large volumes of English text,
[00:50:57] is the baby crying is probably a much more likely word ordering
[00:51:02] than is the bay bee crying?
[00:51:04] And then let us pray and lettuce spray.
[00:51:06] So if you have identical acoustic sequences,
[00:51:08] your language model has to kind of come in and do its job, then.
[00:51:13] Okay, so I just wanted to put this here if you wanted to use
[00:51:16] language models in your work.
[00:51:19] So SRILM, so actually Alan also mentioned about SRI in his talk.
[00:51:24] So they've put out this toolkit,
[00:51:26] which is extensively used in many communities.
[00:51:29] So it's known as the SRILM toolkit.
[00:51:31] It has lots of in-built functionalities implemented,
[00:51:36] so this is a good tool kit to use.
[00:51:39] Another tool kit which is getting quite popular now days
[00:51:43] is KenLM Toolkit, which handles large volumes of text very,
[00:51:46] very efficiently.
[00:51:48] So the data structures which are used to implement this
[00:51:51] toolkit are much more sophisticated.
[00:51:53] So this is much faster, KenLM, but probably only need to use
[00:51:57] this if you're dealing with very large volumes of data.
[00:52:00] And there's also this OpenGrm NGram Library.
[00:52:04] So if you like finite state machines,
[00:52:05] if you like working with finite state machines,
[00:52:08] you want to represent everything as a finite state machine.
[00:52:11] Then this is the toolkit for you, so
[00:52:15] OpenGrm NGram, it was developed by Google.
[00:52:19] Okay, so language models, like I mentioned,
[00:52:22] it has many applications.
[00:52:25] So speech recognition is just one of them.
[00:52:27] Machine translation is another application where language
[00:52:30] models are heavily used.
[00:52:32] Handwriting recognition, optical character recognition, all
[00:52:36] of these also would use language models on either letters or
[00:52:40] characters.
[00:52:42] Spelling correction, again,
[00:52:43] language models are useful here because you can have
[00:52:47] language models over your character space.
[00:52:50] Summarization, dialog generation,
[00:52:52] information retrieval, the list is really long.
[00:52:54] So language models are used in a large number of applications.
[00:52:59] So I just want to mention this one point about language models.
[00:53:05] So we mentioned that you look at these word contexts.
[00:53:08] And you look at counts of these words, and these word contexts
[00:53:11] over large text corpora in a particular language.
[00:53:14] How often does this particular set of,
[00:53:17] how often do these particular set of words appear?
[00:53:20] And then you compute some relative thoughts.
[00:53:23] So you see, okay, these chunks appear so often, and
[00:53:25] these are the total number of chunks.
[00:53:27] And so you get some relative counts.
[00:53:29] And it'll give you some probability of how
[00:53:31] often you can expect this particular chunk to appear.
[00:53:34] So just to kind of slightly formalize that, so this very,
[00:53:38] very popular language model which is used are these NGram
[00:53:41] language models.
[00:53:42] So the idea is really straightforward.
[00:53:44] So you just look at co-occuring, either two words, or
[00:53:49] three words, or four words.
[00:53:51] So if your n is two, you're looking at bigrams.
[00:53:54] If n is three, you're looking at trigrams.
[00:53:57] n is four, four-grams and so on.
[00:53:59] And Alan mentioned yesterday the five-gram model.
[00:54:01] If you're already looking at five-grams,
[00:54:04] you can pretty much reconstruct English sentences really well.
[00:54:07] But of course then you're running into really, really
[00:54:11] large number of NGrams, as you increase the order of the NGram.
[00:54:15] So here I'm looking at a four-gram, so
[00:54:18] the four-gram is she taught a class.
[00:54:21] So what is the probability of this particular four-gram?
[00:54:24] That is the word class follows,
[00:54:26] this particular word context she taught a.
[00:54:28] So you look at counts of, she taught a class,
[00:54:31] in large volumes of English text.
[00:54:34] And then you normalize it with the count of, she taught,
[00:54:37] which is the word context.
[00:54:38] So how often does class come after this particular word
[00:54:43] context?
[00:54:43] So what is the obvious limitation here?
[00:54:48] >> [INAUDIBLE] >> Yeah, exactly, so
[00:54:52] we'll never see enough data.
[00:54:54] We're always going to run into NGrams,
[00:54:56] which we're not going to see in the text corpus.
[00:54:59] And this is actually This happens far more frequently than
[00:55:03] one would even expect.
[00:55:04] Even if you have really, really large databases of Ngrams,
[00:55:08] you're going to run into this issue.
[00:55:09] So just to make sure that this is true,
[00:55:12] I went into this Google Books.
[00:55:14] So Google Books has accumulated lots and lots of Ngrams
[00:55:18] from all the books which are available on Google.
[00:55:21] It is in English.
[00:55:23] So you can actually plot how Ngrams
[00:55:25] have appeared in books over some particular time frame.
[00:55:30] So you can go and
[00:55:31] play around with this if you've not seen this before.
[00:55:35] I just typed in this particular fourgram,
[00:55:37] which hopefully is not very relevant to this crowd.
[00:55:41] So feeling sleepy right now.
[00:55:44] And there weren't any valid Ngrams at all.
[00:55:46] And this is not a very, very rare fourgram, right?
[00:55:51] And even feeling sleepy, right?
[00:55:54] None of them appear in text.
[00:55:58] So this is a problem which occurs actually very,
[00:56:00] very frequently.
[00:56:02] So, even when you work with this counts from very,
[00:56:06] very large text corpora.
[00:56:09] You're always inevitably going to run in to this issue,
[00:56:11] which is you're gonna have this unseen Ngrams,
[00:56:14] which never appear in your training data.
[00:56:17] And why is this an issue?
[00:56:19] Because during test time, when you're trying to reorder words
[00:56:23] according to your particular language model.
[00:56:25] And if any of these unseen Ngrams appear on your
[00:56:27] test sentence,
[00:56:28] then the sentence is going to be assigned a probability of 0.
[00:56:30] Because it has no idea how to deal with this unseen word.
[00:56:34] So there is this problem with what are known as un-smoothed
[00:56:37] Ngram estimates.
[00:56:38] And I wanted to make it a point to actually
[00:56:41] talk about this because Ngrams are only useful with smoothing.
[00:56:46] So these unsmoothed Ngram estimates, like I mentioned,
[00:56:51] you will always run into these unseen Ngrams, and
[00:56:54] then what do you do?
[00:56:55] So there are a horde of what are known
[00:56:57] as these smoothing techniques.
[00:56:59] So you're gonna reserve some probability mass
[00:57:02] from the seen Ngrams towards the unseen Ngrams.
[00:57:06] And then there are questions like how do you distribute that
[00:57:08] probability mass across the useen Ngrams?
[00:57:10] And there are various techniques for that as well,
[00:57:13] like how do you distribute that remaining probability mass.
[00:57:16] So this is a lot of work on smoothing methods.
[00:57:19] And it's very useful to make Ngram models,
[00:57:23] to make them effective.
[00:57:24] So for anyone who is interested, I would highly recommend reading
[00:57:28] this 1998 paper by Chen and Goodman.
[00:57:30] Goodman was at MSR, I don't know where he is now.
[00:57:36] So this is an empirical study of smoothing techniques for LMs.
[00:57:39] I highly recommend this.
[00:57:41] It's kind of long but it really gives you
[00:57:44] a very deep understanding of how smoothing techniques help.
[00:57:48] Don't be fooled by the 1998, it's still very relevant
[00:57:53] today because Ngrams are very relevant even today.
[00:57:56] So Ngrams are not going anywhere.
[00:57:57] So I'm not talking about what the latest language models are.
[00:58:03] But these days in speech recognition systems,
[00:58:07] we move towards these, what are known as recurrent neural
[00:58:10] network based language models.
[00:58:12] So that's neural network based, but
[00:58:14] I believe it's still not folded into a lot of production systems
[00:58:18] because it's not very fast.
[00:58:20] So many of the production level ASL systems probably still
[00:58:25] use Ngrams.
[00:58:26] And then do a rescoring using recurrent neural network
[00:58:29] language models but, so Ngrams models are still very,
[00:58:32] very much in the picture.
[00:58:37] Okay, so we've already covered each of these individual
[00:58:40] components.
[00:58:41] But there's this big component in the middle right, which is
[00:58:44] the decoder, that's actually a very important component.
[00:58:48] So I have all of this parts of the ASR
[00:58:51] system which are giving me various estimates
[00:58:53] of what is the most likely phoneme sequence.
[00:58:55] What is the most likely word sequence and so on.
[00:58:58] But finally I just want to get the most clear word sequence
[00:59:02] corresponding to speech utterance, and so
[00:59:04] then it's a search problem.
[00:59:05] So I have these various components, and
[00:59:08] now I need to search, putting all of them together,
[00:59:10] I need to search through this entire space.
[00:59:13] So just looking at the very simple example we started with.
[00:59:17] This is what a naive search graph would look like.
[00:59:19] So you start to a particular point and say that you only
[00:59:23] expect it to be nine or one, just these two words.
[00:59:27] Then you need to transition to nine.
[00:59:29] So here, every single arc doesn't have a weight but
[00:59:32] these are all weighted,
[00:59:33] cuz they all come with their associated probabilities.
[00:59:36] So you can, from start,
[00:59:37] you can transition in to either producing the word nine or one.
[00:59:41] But each nine is a sequence of phonemes, and each sequence of
[00:59:44] each phoneme, corresponds to it's corresponding HMM.
[00:59:48] So, and which has its own probabilities.
[00:59:51] So this is already, you can see this is slight,
[00:59:54] this is quite a large graph just for these two words.
[00:59:57] And get at least like a half decent
[01:00:00] system we'll be looking at at least 20,000 or 40,000 words.
[01:00:03] So you can imagine how much the search graph blows up.
[01:00:06] So these are really large search graphs, and
[01:00:11] I think I have another slide, yeah.
[01:00:13] So if you have, say, a network of words as follows, so
[01:00:16] the birds are walking, the boy is walking.
[01:00:18] This is really simple where there's not an model,
[01:00:22] this is highly constrained.
[01:00:25] So now each of these are now going to map their corresponding
[01:00:29] phone sequences, so the, the birds, and so on.
[01:00:33] And each of those phones now are going to correspond to their
[01:00:38] underlying and very quickly, the graph blows up.
[01:00:43] So if you look at, so just to give you an estimate,
[01:00:46] a vocabulary size of around 40,000 gives you search graphs
[01:00:51] of the order of tens of millions of states.
[01:00:55] So these are really large graphs, and so
[01:00:58] now we need to search through these graphs and throw out what
[01:01:01] is the most likely word sequence to correspond to the speech.
[01:01:05] So you might be wondering, can you do an exact search through
[01:01:09] this very, very large graph?
[01:01:11] And the answer is no, you cannot do an exact search through this
[01:01:15] graph, because it's just too large.
[01:01:17] So you have to resort to approximate search techniques,
[01:01:21] and there are a bunch of them, which do a fairly good job.
[01:01:25] So none of these speech systems that you work with are actually
[01:01:29] doing an exact search through this graph.
[01:01:33] So that's the decoder, so any questions so far?
[01:01:36] So this is the entire kind of pipeline of how an ASR
[01:01:41] system works.
[01:01:45] Okay, so everyone is with me, right?
[01:01:48] So I want to kind of end with this new direction,
[01:01:51] which is kind of becoming very hot nowadays.
[01:01:54] They are known as these end-to-end ASR systems,
[01:01:58] so I showed you all of these different components which,
[01:02:02] put together, make an ASR system.
[01:02:04] But lots of people are interested in kind of doing away
[01:02:06] with all of those components.
[01:02:08] Let's not worry about how a word splits into its corresponding
[01:02:11] phone sequence.
[01:02:13] Let's just directly learn a mapping from acoustic features
[01:02:17] to letters.
[01:02:18] So this is just two characters, so
[01:02:21] directly go from speech vectors, so these acoustic vectors,
[01:02:25] to a character sequence.
[01:02:27] And then you can have character language models which re-score
[01:02:31] the character sequence, and so on.
[01:02:33] So one kind of nice advantage of this is that,
[01:02:36] because you're getting rid of the pronunciation model,
[01:02:40] which is that you're not now looking at phones at all,
[01:02:42] you don't need that mapping.
[01:02:44] The word to phone mapping, which typically is
[01:02:48] written down by experts, and that changes for each language.
[01:02:51] So now you want to build a new system for a new language.
[01:02:54] If this worked really well, then all you'd need is speech and
[01:02:59] the corresponding text.
[01:03:01] But the catch is, you need lots and lots of these for
[01:03:03] this to work, for these kinds of end to end systems to work well.
[01:03:07] So just for people in the crowd who are interested
[01:03:10] in these kinds of models,
[01:03:11] I'll just put down a few references, which you can read.
[01:03:14] So the first is this paper, which came out in 2014.
[01:03:18] I've kind of started off this thread of work, which is this
[01:03:21] end to end speech recognition with recurrent neural networks.
[01:03:25] So I won't go into details at all about the model, this is
[01:03:29] just for you to jot down if you want to go later and read it up.
[01:03:33] But I'll put this up, which is kind off the sample character
[01:03:37] level transcripts which they get out of their end-to-end systems.
[01:03:41] So here they have a bunch of target transcriptions, and
[01:03:45] the output transcriptions.
[01:03:47] So you can immediately see, so
[01:03:48] this is without any dictionary, without any language model.
[01:03:52] So this is directly mapping acoustic vectors to letters,
[01:03:57] characters.
[01:03:59] So you can see obvious issues like lexical errors,
[01:04:02] you can see things where you have phonetic similarity, so
[01:04:07] shingle becomes single.
[01:04:08] Then there are words like Dukakis and Milan,
[01:04:12] which are apparently not appearing in the vocabulary,
[01:04:16] so that is another advantage of these character models.
[01:04:21] So in principle, you don't care about whether you will see this
[01:04:24] word in your vocabulary,
[01:04:26] because you are only predicting one character at a time.
[01:04:29] So it should recover vocabulary words, but
[01:04:32] this system doesn't actually do that too well.
[01:04:35] >> [INAUDIBLE] >> It does, yeah, so they just
[01:04:39] had this without a dictionary, without a language model.
[01:04:42] But their final numbers are all with a language model, and
[01:04:46] a dictionary also, actually.
[01:04:48] So the second improvement of this paper was by Maas et al,
[01:04:52] who again explored a very,
[01:04:54] very similar structure as in this previous paper in 2014.
[01:04:59] And they had this kind of interesting analysis,
[01:05:02] which I wanted to show.
[01:05:04] So on the x-axis you have time.
[01:05:07] And each of these graphs correspond to various phones.
[01:05:11] So remember in their system there are no phones at all.
[01:05:15] But they just accumulated bunch of speech samples,
[01:05:18] which correspond to each of these phones.
[01:05:21] And averaged all the character properties corresponding
[01:05:25] to those particular forms.
[01:05:27] So, here you can see that K obviously comes out but so
[01:05:31] does C.
[01:05:32] So the letter C also corresponds the core sound and
[01:05:36] interestingly for Shah.
[01:05:38] So, this is the phone shah.
[01:05:40] So S and H, so S, H definitely comes out.
[01:05:45] But so does T, I because as in TION, T-I-O-N, so
[01:05:48] you would pronounce that as shah, right?
[01:05:51] So that actually comes out of the data, which is pretty cool.
[01:05:56] So this yeah, this was a nice analysis, so they do
[01:06:00] only slightly better than the previous paper, and yeah?
[01:06:04] >> [INAUDIBLE] >> So
[01:06:07] the X-axis is time in frames.
[01:06:10] You can think of it in speech frames.
[01:06:12] And these are just the character properties, yeah.
[01:06:18] So the last system, which came out in 2016, and
[01:06:21] kind of significantly improved over these two.
[01:06:25] Uses this very popular paradigm now in sequence to sequence
[01:06:30] models which are know as Encode or Decoder Networks or
[01:06:34] Sequence to Sequence networks.
[01:06:37] Which is first used for machine translation and
[01:06:40] now they applied it to this particular problem and
[01:06:43] also included what is known as Attention.
[01:06:46] And all of these bells and
[01:06:48] whistles together definitely make a difference.
[01:06:52] But I want to mention that End-to-End systems are not yet
[01:06:57] close to the entire standard pipeline that I showed you
[01:07:02] earlier.
[01:07:03] So, people would really like to bridge the gap between
[01:07:06] End-to-End systems and these whole pipelines.
[01:07:10] Because clearly these are much more, at least easier to
[01:07:13] understand in some sense, at least from a modeling stand
[01:07:17] point, although it's not easier to understand what it's doing.
[01:07:21] Yeah, so
[01:07:21] there's lot of work going on in this particular area.
[01:07:25] But these systems require lots of data, lots and
[01:07:29] lots of data to train.
[01:07:31] And that's because not only are you trying to understand what
[01:07:34] are the underlying speech sounds in the speech references,
[01:07:37] you're also trying to understand spelling.
[01:07:40] You're trying to figure out what spelling makes sense for
[01:07:43] a particular address.
[01:07:44] And clearly for a language like English,
[01:07:46] where the authography is so irregular, it's a hard problem.
[01:07:50] And so
[01:07:50] these models require large amounts of data to work well.
[01:07:55] Okay, so I'm gonna come back to this question I post initially,
[01:08:00] which is what's next?
[01:08:02] So what are all the kinds of problems that we could work on,
[01:08:06] if anyone was interested in speech recognition?
[01:08:10] So there are lots of, I think there are lots of next steps.
[01:08:14] So one is you need to do more to make ASR systems robust to kinda
[01:08:18] variations in age, accent of course,
[01:08:21] which is why we are working on that problem.
[01:08:25] And also this is another thing which people are interested in.
[01:08:27] So just speech ability so there are people say with speech
[01:08:31] impairments, the distractor or they have other issues and they
[01:08:35] not able to speak as clearly as maybe all of fast in the room.
[01:08:39] So how can we adapt ASI systems to work well with those people?
[01:08:45] And this is a real, very challenging task, so how do you
[01:08:48] handle kind of noisy, real life settings with many speakers?
[01:08:53] This goes back to Allen's dream of having a bot which is sitting
[01:08:57] in a meeting, and kind of transcribing and
[01:08:59] figuring out what is going on.
[01:09:01] So that would also involve the underlying ASR system in
[01:09:06] that bot.
[01:09:06] It would have to figure out that okay,
[01:09:08] these are all the interfering speakers, this is the main
[01:09:11] speaker, this is the speaker I need to kind of transcribe.
[01:09:14] I need to haze out the other interfering speakers and so on.
[01:09:18] And this is not the state of the art for the this kind of meeting
[01:09:22] speech, tasks is not very low, the error here is not very low.
[01:09:27] This is actually, it's handled pretty well now,
[01:09:31] if you have lots and lots of level speech.
[01:09:34] This pronunciation variability actually captured into acoustic
[01:09:38] model itself.
[01:09:39] But handling new languages currently, and the only way to
[01:09:43] do a good job is to go and collect lots and lots of data.
[01:09:46] Which at least personally to me, is unsatisfying.
[01:09:50] So it seems like if you have existing models,
[01:09:53] you should be able to adapt them with not bizarre amounts of
[01:09:56] fallible speech.
[01:09:58] At least they're somewhat related.
[01:10:00] We should be able to do a half decent job, by taking existing
[01:10:04] models and adapting them to the new language that we want to
[01:10:08] recognize, or the new dialect we want to recognize.
[01:10:11] So there are these problems.
[01:10:13] So in computer science, we are always trying to do things
[01:10:17] faster, and to be more efficient, right?
[01:10:20] In a both computationally, and
[01:10:21] if you are trying to do things faster from both
[01:10:24] the computational power standpoint of every standpoint,
[01:10:28] but we should also try to be resource efficient, right?
[01:10:31] We don't want to keep going and collecting more and more data,
[01:10:34] every time we come up with a new task.
[01:10:36] So can we do many of these tasks with less?
[01:10:39] This is something that I am very interested in personally, so
[01:10:43] can we reduce duplicated effort across domains and languages?
[01:10:48] And also can we reduce dependence on
[01:10:50] language specific resources?
[01:10:53] And this is of course the holy grail I think,
[01:10:55] training with less labeled data.
[01:10:58] And actually making use of unlabeled data better.
[01:11:03] Okay, so I'll also show this one direction,
[01:11:05] which Microsoft is working on, and it's kind of very promising.
[01:11:09] So this is just an excerpt from an ad.
[01:11:14] So this is Skype.
[01:11:16] >> Can you understand me now?
[01:11:18] [MUSIC]
[01:11:20] >> [FOREIGN] >> [FOREIGN]
[01:11:28] >> You speak Chinese.
[01:11:30] >> Now, if that worked seamlessly that worked here,
[01:11:33] that would be pretty cool.
[01:11:35] So I'm told this was just setup for the ad.
[01:11:39] So Microsoft has been working a lot on speech-to-speech
[01:11:41] translation.
[01:11:42] And I think this is a very interesting problem.
[01:11:45] Because there can be cues in speech, which help disambiguate
[01:11:50] utterances for the machine translation part, and so on.
[01:11:55] So I think there is something which can be leveraged from
[01:11:59] the speech component, from the SR component.
[01:12:03] So this is something that we talked about a little bit,
[01:12:06] which was using speech production models, and
[01:12:10] how we can build speech production inspired models,
[01:12:13] to handle pronunciation variability.
[01:12:16] And that actually in principle,
[01:12:18] does reduce dependence on language-specific resources.
[01:12:22] Because all of us have the same vocal tract system, right?
[01:12:25] So they're are only so many ways in which our different
[01:12:28] articulators, can form different configurations and
[01:12:31] produce sounds.
[01:12:33] So in some sense, at least in principle,
[01:12:35] moving to that kind of a model does reduce dependence on
[01:12:39] language-specific resources.
[01:12:41] So we don't need to come up with phone sets corresponding to
[01:12:43] a particular language, if you're going to represent all of
[01:12:46] the pronunciations in terms of these articulatory features.
[01:12:49] But there are other problems with that method.
[01:12:53] And this is another problem,
[01:12:55] which I think is very interesting.
[01:12:57] So how do you handle new languages, and
[01:13:00] not have to collect loads and loads of data?
[01:13:02] So just to tell you how many languages so
[01:13:04] far have ASR supports.
[01:13:06] This is actually a year or two old,
[01:13:08] maybe this number has gone up a little.
[01:13:10] So they support roughly around 80 Languages.
[01:13:14] But these languages include Indian English,
[01:13:17] Australian English, British English,
[01:13:19] which are not clearly languages.
[01:13:20] So that numbers even lesser than 80.
[01:13:23] And if you look at the distribution across continents,
[01:13:26] Europe has the highest representation in terms
[01:13:29] of languages which are supported by speech technologies.
[01:13:34] America is of course small,
[01:13:35] also because they're largely monolingual.
[01:13:38] But Asia is dismal, even though there are so
[01:13:41] many languages spoken in the Asian subcontinent.
[01:13:45] So yeah, we should all do more to build
[01:13:48] speech recognition technologies, or language technologies, for
[01:13:51] various Indian languages and languages in Asia.
[01:13:55] And so one thing that we have looked at, is can we try and
[01:13:59] crowdsource the labels for speech?
[01:14:04] So can we just place speech utterances to crowds who speak
[01:14:08] the particular language.
[01:14:10] And then try to get transcription from them.
[01:14:12] So it will be a little noisy, but then there are techniques to
[01:14:15] kind of handle the noise in those jobs transcriptions.
[01:14:17] But that also has an issue,
[01:14:18] because it's somewhat unfair to a large number of languages.
[01:14:22] So this is just a histogram, this was all the speakers
[01:14:30] who were sampled from a large crowdsourcing platform.
[01:14:33] Just MTurk, Amazon's Mechanical Turk.
[01:14:36] And this looked at the language demographic of crowd workers on
[01:14:40] Mechanical Turk.
[01:14:41] And the yellow bars are actually the speakers of those languages
[01:14:45] in the world.
[01:14:46] So you can see there's a large distribution and mismatch,
[01:14:49] between the language background of the crowdworkers, and
[01:14:53] the language expertise,
[01:14:54] which is needed to complete transcription tasks.
[01:14:57] I mean, this tail is really really long, so
[01:15:02] Forget about minority languages or languages which, it's very,
[01:15:06] very hard to get native speakers on crowdsourcing platforms.
[01:15:09] So this also may not really be a viable solution always.
[01:15:13] So I think there are lots of
[01:15:15] interesting problems to think of in that space.
[01:15:18] So with that, I'm going to stop.
[01:15:21] I'll kind of leave you with this slide.
[01:15:23] Yeah, I think I'm doing good on time.
[01:15:25] So thanks a lot.
[01:15:26] I'm happy to take more questions.
[01:15:28] >> [APPLAUSE] >> Yes.
[01:15:34] >> [INAUDIBLE]
[01:15:45] >> Yeah, so language models,
[01:15:48] you can back off all the way to a unigram model.
[01:15:51] So as long as each of the individual words you've seen
[01:15:56] somewhere in the language model, and if your acoustic
[01:15:59] model is good, so it's going to give you somewhat reasonable
[01:16:01] phone sequence corresponding down the line of speech.
[01:16:04] You might still recover the word sequence even though
[01:16:07] the language model doesn't give you too many constraints.
[01:16:10] So for example I think that the Sarah Palin speech, the language
[01:16:15] model, I don't think anything more than maybe a bi-gram model
[01:16:18] [LAUGH] or maybe a tri-gram model at the most.
[01:16:23] So as long as the individual words have been seen in text,
[01:16:28] in large volumes of text, and you're acoustic model is good,
[01:16:30] you can still recover it even if there's
[01:16:33] no continuity between the words.
[01:16:35] Does that answer your question, yeah?
[01:16:39] Any other?
[01:16:42] Okay.
[01:16:43] Yes.
[01:16:45] >> Based on your working thesis,do you ever feel
[01:16:50] you need to, have more because the [INAUDIBLE]
[01:16:54] was obviously [INAUDIBLE] find some [INAUDIBLE]
[01:16:59] more than [INAUDIBLE].
[01:17:02] >> But it had to have more than 30 phones?
[01:17:04] Actually, so 40 is the number of phonemes.
[01:17:09] Yeah, so the number of phones in English is more than 40,
[01:17:13] so even in those phonetic transcriptions,
[01:17:16] the number of phones were almost close to 80.
[01:17:20] Because it's actually annotating all the fine grained variations.
[01:17:27] And that, of course, helps if you have that kind of.
[01:17:29] Where are you every going to get that level of phonetic
[01:17:34] annotation, yeah.
[01:17:35] Yeah.
[01:17:36] >> [INAUDIBLE] next feature where character
[01:17:44] >> You need lots
[01:17:46] other than needing.
[01:17:48] You also need lots of computational resources.
[01:17:51] But other than that.
[01:17:55] Like I said it doesn't really work as well as the entire
[01:17:59] pipeline yet.
[01:18:00] So there's still a delta in terms of the performance of your
[01:18:04] state of the art systems and these end to end systems.
[01:18:07] And so currently,
[01:18:09] all these end-to-end systems are recurrent neural networks.
[01:18:14] So there is this issue of how much context to retain, and
[01:18:18] whether you retain that context effectively.
[01:18:20] Which is were these attention mechanisms come in, but
[01:18:23] attention mechanisms also really fall short.
[01:18:26] So if you're interested, there is an iClear paper this
[01:18:29] year which is, I think the title is something like
[01:18:32] Frustratingly Short Context or something like that.
[01:18:36] You can search for translation.
[01:18:37] So the idea is that even if you just look at the last five
[01:18:40] output representations, you can do as well as
[01:18:44] a really sophisticated attention mechanism.
[01:18:47] So attention mechanisms also need to be kind of improved
[01:18:51] further.
[01:18:52] Yeah?
[01:18:52] >> [INAUDIBLE] systems work for [INAUDIBLE].
[01:18:58] >> Yeah, so the [INAUDIBLE] system is actually predicting
[01:19:01] characters.
[01:19:02] So it predicts a single letter of the alphabet.
[01:19:04] So auto vocabulary is not an issue at all cuz it's
[01:19:07] predicting one character at a time.
[01:19:11] >> [INAUDIBLE] data for Indian language.
[01:19:15] >> Yeah, so that's actually something that's
[01:19:17] very interesting.
[01:19:18] So for Indian languages which are morphologically rich and
[01:19:23] where you probably cannot expect to see various forms
[01:19:28] of a word in the vocabulary.
[01:19:31] End to end might actually work really well.
[01:19:33] But no one has run this yet
[01:19:34] because this amount of data is not available here.
[01:19:38] >> In fact they didn't call that particular speech for
[01:19:44] example in English the classes >> [INAUDIBLE]
[01:19:50] [CROSSTALK] >> Yeah, but that's a good mob-
[01:19:53] >> English, right?
[01:19:54] Characters don't [INAUDIBLE] >> No, not at all.
[01:19:57] So the entire system actually needs to, all these problems,
[01:20:01] it needs to learn You need to learn the sound mapping,
[01:20:04] you need the learn spelling.
[01:20:06] So yeah, so there's no, because it's so
[01:20:09] irregular, right, the mapping.
[01:20:12] So what is the point you are saying? Sorry.
[01:20:14] >> So for example .>> Yeah.
[01:20:18] >> And this part but if I take for example,
[01:20:22] I need to have a class for and >> [INAUDIBLE]
[01:20:25] So you can have,
[01:20:26] you have [INAUDIBLE].
[01:20:29] >> Yeah, you don't need a.
[01:20:31] >> [INAUDIBLE] >> Yeah, it's up here, yeah.
[01:20:34] >> [INAUDIBLE] >> No,
[01:20:38] you might have double of 36 because you, so you have one.
[01:20:41] So split it.
[01:20:44] Unicode that is an initiative.
[01:20:46] So you would have c which is plus e.
[01:20:51] So you would predict and you predict the model and
[01:20:54] you predict and so on.
[01:20:56] >> Might be enable for
[01:20:57] all the single- >> No, you're talking about.
[01:21:00] So you just predict each of these.
[01:21:03] >> S-E-E [INAUDIBLE] so you [INAUDIBLE] then E, then E.
[01:21:05] >> Yeah. >> [INAUDIBLE]
[01:21:07] >> Yeah, yeah,
[01:21:08] that's [INAUDIBLE] but little size, of course
[01:21:12] the little space becomes larger, but probably [INAUDIBLE] double.
[01:21:15] I don't think it'll be more than that.
[01:21:18] Which if you have enough data should be okay.
[01:21:22] >> Quick fix. >> I think yes the cost of
[01:21:24] the of the mapping is much more stable.
[01:21:25] It actually might do even better than in English. Yes?
[01:21:28] >> What do you think about
[01:21:29] the minimum about the data is letting me if you want to?
[01:21:37] >> Yes so I ask this too in terms of who will and so on.
[01:21:41] So they use like $10,000 So speech,
[01:21:43] [LAUGH] all of you must be using speech [INAUDIBLE].
[01:21:49] So I know the standard pipeline.
[01:21:51] So for switchboard, for instance, so
[01:21:52] switchboard is around 200 hours of speech.
[01:21:55] And the error rates now are 5%, the latest was 5%.
[01:22:01] >> So of course with lot of machinery. So-
[01:22:05] >> [INAUDIBLE].
[01:22:07] >> Yeah end to end- >> What do you think
[01:22:10] the bare minimum would be if we really wanted to [INAUDIBLE].
[01:22:12] >> To try it out.
[01:22:13] So the other papers that I showed you they
[01:22:15] actually work with [INAUDIBLE] which is 200 hours of speech.
[01:22:19] So even if you're in the 100 hours, And
[01:22:21] more, I think you can start writing on data systems.
[01:22:25] But again, 10 years,
[01:22:25] 20 years, But I would still be interested to see experiments
[01:22:28] on Indian languages with even smaller amounts of data.
[01:22:30] >> Some people are even doing it
[01:22:31] on fable languages
[01:22:32] >> Right, right >> 20 years,
[01:22:33] >> Correct
[01:22:33] >> So it's sort of beginning to
[01:22:42] work, it really has to be >> Appropriately similar data
[01:22:47] lectures from [INAUDIBLE], then maybe.
[01:22:50] >> Yes [LAUGH] That's true, that's true.
[01:22:53] >> [CROSSTALK] >> Of course, yeah.
[01:22:55] >> But [INAUDIBLE] good transcriptions,
[01:23:02] but don't estimate that [INAUDIBLE] is [CROSSTALK]
[01:23:04] >> Yeah, I think, yeah,
[01:23:04] that's a very >> I think that would be a very
[01:23:06] good just hours of Hindi speech how it itself.
[01:23:08] You have a question?
[01:23:09] >> Yea. Is there an evidence of these
[01:23:13] for making another language with this complicated
[01:23:19] >> No one has that yet.
[01:23:22] >> Not this language, any >> No so
[01:23:26] I'll not from there maybe be able and to have some.
[01:23:29] >> The only thing about that it's funny and
[01:23:32] it's working this and that it's not clear.
[01:23:34] But the argument of doing this for line is with my apology and
[01:23:37] probably the most daily token
[01:23:45] >> [INAUDIBLE] and
[01:23:47] there are people claiming that it's not a method.
[01:23:50] It's not clearly [INAUDIBLE], okay?
[01:23:53] But this is the hot research topic that people like to do.
[01:23:56] And ultimately,
[01:23:57] it would be easier because enunciation [INAUDIBLE] is hard.
[01:24:00] >> Yes, yes.
[01:24:00] [LAUGH] >> So if you can sort of get
[01:24:04] your way around that and find people that actually said it
[01:24:06] >> But, don't underestimate,
[01:24:08] people keep saying there's 26 letters in the English.
[01:24:10] No there isn't, because there's numbers and symbols and
[01:24:12] other things that you have to address.
[01:24:18] >> Mm-hm.
[01:24:23] All right.
[01:24:24] Thanks, so much.
[01:24:25] >> [APPLAUSE]