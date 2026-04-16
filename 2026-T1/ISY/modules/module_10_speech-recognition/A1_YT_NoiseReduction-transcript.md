[00:00:00] hello folks this is Nathan welcoming you
[00:00:01] to the AI University channel where you
[00:00:03] can learn all your favorite digital
[00:00:05] technologies like machine learning deep
[00:00:07] learning AI Big Data do virtual reality
[00:00:10] augmented reality and cloud computing
[00:00:12] this is the continuation of previous
[00:00:14] video and in this video I will go in a
[00:00:17] step-by-step manner to explain how can
[00:00:19] we reduce the effect of noise you know
[00:00:22] in order to convert speech into text in
[00:00:25] a crisp and clear way you will also see
[00:00:28] how can we generate several possible
[00:00:30] transcripts from a single speech source
[00:00:33] if that is P sources noisy in nature
[00:00:36] that way you can pick up a right
[00:00:39] transcript in this video you will also
[00:00:42] see how to access your computer's
[00:00:44] microphone so that you can speak into it
[00:00:48] and then a speech recognition package
[00:00:50] will transcribe your speech in real time
[00:00:52] so stay connected till the end of this
[00:00:54] video and the series to acquire complete
[00:00:57] knowledge if you are new here then
[00:01:00] consider subscribing to this channel or
[00:01:01] if you have already subscribed then
[00:01:03] click on the bell icon to receive the
[00:01:05] notifications about hottest technology
[00:01:07] of 20%
[00:01:17] when it comes to speech recognition
[00:01:19] accuracy is one important may trick
[00:01:22] because if your speech recognition
[00:01:24] system is understanding something and
[00:01:27] transcribing it into a wrong text then
[00:01:29] it may create a big blunder consider
[00:01:32] phrase he is going to bed
[00:01:35] now if a speech recognition system has
[00:01:38] bad accuracy due to some noise then it
[00:01:41] may transcribe this phrase as he is
[00:01:44] going to tip which altogether has a
[00:01:46] different meaning so if a noise in
[00:01:48] speech is not treated well then it may
[00:01:51] have reduced the accuracy of speech
[00:01:53] recognition applications significantly
[00:01:56] hence it is very important to remove the
[00:01:59] noise from speech so let me play an
[00:02:01] audio having some noise in it so this is
[00:02:05] the audio which I am going to play so
[00:02:11] you can listen that it has lot of noise
[00:02:13] in the background right and it it was
[00:02:16] not clear what that person in the
[00:02:18] background was actually saying so let's
[00:02:20] try to convert this speech which has
[00:02:23] noise in it into text and later on I am
[00:02:26] going to utilize a method to reduce the
[00:02:29] effect of noise in the background and
[00:02:33] then getting a crisp and clear speech so
[00:02:36] that we can convert it into text in a
[00:02:38] more accurate way so let me open my
[00:02:40] Japan notebook real quick so this is my
[00:02:43] Jupiter notebook and in the first cell
[00:02:46] you can see that I'm using a file rather
[00:02:51] audio file with the name noisy
[00:02:54] underscore speech dot WAV to convert the
[00:02:57] speech in this audio file into text so
[00:03:01] the similar piece of code mentioned in
[00:03:03] the cell is already explained in the
[00:03:04] previous videos alright but this time I
[00:03:08] am utilizing this noisy speech dot WAV
[00:03:11] file which contains the noise in the
[00:03:13] background when a person was speaking
[00:03:15] something so when I ran the cell it
[00:03:18] actually generated the output as the
[00:03:20] snail smelling old beer drinkers which
[00:03:23] it is not clear yet whether this was the
[00:03:26] actual
[00:03:27] sentence a particular person in the
[00:03:29] audio was speaking so we can get rid of
[00:03:32] the noise in the background in that
[00:03:36] particular audio file in order to
[00:03:38] generate the right text with accuracy
[00:03:40] using a method called adjust for ambient
[00:03:43] noise and this method is associated with
[00:03:46] our recognizer
[00:03:49] class so in this cell which is the next
[00:03:51] cell you can see that I introduced this
[00:03:56] method here with an intent to adjust the
[00:03:59] noise before we call our this record
[00:04:02] method so this is the only difference I
[00:04:04] just introduced this one more line which
[00:04:07] contains this method adjusts for ambient
[00:04:09] noise from the above cell okay so when I
[00:04:13] ran the cell I got the output as still
[00:04:17] smell like old beer drinkers which is
[00:04:20] bit closer to the actual text right
[00:04:24] moving on so sometimes it is not
[00:04:27] possible to remove the effect of the
[00:04:29] noise in those cases you may need to do
[00:04:32] some you know data processing of the
[00:04:34] audio file in the form of applying some
[00:04:36] filters etc so there is a Python package
[00:04:40] called Sai PI which can be utilized for
[00:04:42] this purpose you can also use some
[00:04:44] professional audio editing software's as
[00:04:46] well for this particular purpose now
[00:04:49] when we have noisy audio files you can
[00:04:52] try to get many possible responses for a
[00:04:55] given a noisy speech audio file that is
[00:04:58] getting most likely transcriptions so
[00:05:02] that you can choose a right transcript
[00:05:03] from the given list based on your wisdom
[00:05:06] we can get this possible list of
[00:05:08] transcripts for the given speech by
[00:05:10] introducing an argument called show all
[00:05:13] equals to true and this argument is
[00:05:16] being used inside a recognized Google
[00:05:20] method okay so we just need to give this
[00:05:22] extra argument here in order to get the
[00:05:25] several possible or most likely
[00:05:28] transcript of a single speech source so
[00:05:33] when I ran the cell which has this
[00:05:34] argument show all equal to true you can
[00:05:37] see that it has generated various
[00:05:40] most likely transcripts of the noisy
[00:05:44] speech audio file we have right so you
[00:05:47] it generated the transcript as the
[00:05:50] snails smelly old gear vendors and it
[00:05:53] also gave the confidence level for this
[00:05:55] as well right then it generated the
[00:05:59] another transcript which was the snail
[00:06:01] smell of old gear vendors then we have
[00:06:04] the snail smelled old gear vendors and
[00:06:07] so on so now based on your wisdom you
[00:06:10] can just pick any particular transcript
[00:06:13] from the possible transcripts for your
[00:06:16] use so this is the way we can you know
[00:06:19] generate lot of other variations of a
[00:06:22] single speech source as well moving on
[00:06:26] so so far we have worked on the static
[00:06:31] audio files which were you know saved on
[00:06:33] our computer in this section we will
[00:06:36] move a step further to capture the
[00:06:39] speech in an interactive way and
[00:06:41] dynamically by making use of microphone
[00:06:44] or rather our computer's microphone and
[00:06:47] then converting into into a text in real
[00:06:50] time we will see that the text will get
[00:06:53] generated as and when we are going to
[00:06:56] speak into our microphone so now in
[00:06:58] order to access the microphone of our
[00:07:01] computer we have to install a package
[00:07:03] called pi audio please note that PI a
[00:07:06] Python version 3.7 doesn't support PI
[00:07:09] audio so you need to have a Python 3.6
[00:07:12] and below to make use of this package if
[00:07:15] you are using anaconda Python version
[00:07:18] 3.7 then you can create a fresh
[00:07:20] environment and install a version 3.6 of
[00:07:25] Python in that environment to get that
[00:07:27] working so let me open the terminal
[00:07:30] first so here you can see that I am
[00:07:34] using my own separate environment called
[00:07:37] application environment and here let's
[00:07:41] type pip install why so you can see the
[00:07:49] message that requirement already
[00:07:50] satisfied which means that I have
[00:07:53] already installed
[00:07:54] previously so that's why it is throwing
[00:07:56] this message okay so we are good here so
[00:08:00] this is the way actually you can install
[00:08:03] the PI audio package to detect or access
[00:08:06] your computer's microphone once the PI
[00:08:09] audio installation is done you can then
[00:08:11] go ahead and validate the installation
[00:08:13] by typing you know a command Python - M
[00:08:23] speech recognition into your terminal
[00:08:32] and then press Enter so you will see a
[00:08:35] message like a moment of silence please
[00:08:37] set minimum threshold to this and say
[00:08:40] something and Bravo it detected my voice
[00:08:43] and whatever I said previously it
[00:08:47] actually showed this message on to my
[00:08:50] screen so now let's close this terminal
[00:08:52] and come back to our Jupiter notebook
[00:08:56] and here we actually want to work with
[00:08:59] our microphone so you can see that I'm
[00:09:03] utilizing this class called microphone
[00:09:06] here right so I'm basically if you see
[00:09:10] this particular cell I have created an
[00:09:13] object of microphone class here and gave
[00:09:16] it a name MC now if your computer has
[00:09:20] many associated microphones then you can
[00:09:23] get the list of all those microphones
[00:09:24] using a method called list microphone
[00:09:28] names which you can see here on this
[00:09:31] particular cell and when I ran the cell
[00:09:34] it actually provided the list of all the
[00:09:39] possible microphones available on my
[00:09:41] computer so if you want to access any
[00:09:44] specific microphone from this given list
[00:09:47] then you can just pass an argument
[00:09:50] device index equals to and the number of
[00:09:54] or in the index number of that
[00:09:56] particular microphone in my example you
[00:09:59] can see that I'm using microphone called
[00:10:02] Microsoft sound mapper - input and
[00:10:05] that's why I gave the index
[00:10:08] zero because index in Python starts from
[00:10:11] zero hence the index of my microphone
[00:10:15] sound mapper is zero and I'm utilizing
[00:10:18] it here now in order to capture
[00:10:21] microphone input or listen to the
[00:10:23] microphone you can use a method called
[00:10:26] listen which I'm utilizing here okay and
[00:10:30] this particular method listen method as
[00:10:33] is associated with a recognizer class
[00:10:35] only so we will use this method inside
[00:10:38] the width block here and the method
[00:10:41] listen takes an argument which is
[00:10:44] nothing but this audio source called
[00:10:47] microphone it tries to basically capture
[00:10:51] the input from the microphone until it
[00:10:53] hears nothing or encounters the silence
[00:10:57] this is something which I am doing in
[00:10:59] the next cell here now when you run the
[00:11:03] cell and speak out any phrase or
[00:11:05] sentence your voice gets captured by
[00:11:07] microphone and speech recognition API
[00:11:10] then in turn converse it converts it
[00:11:13] into text so let me show you it in
[00:11:16] action so I will try to run this
[00:11:18] particular cell which is cell 14 okay
[00:11:21] and it will the microphone will try to
[00:11:25] capture my voice and once it completes
[00:11:27] the processing it will then convert the
[00:11:32] speech into la text which I am going to
[00:11:34] speak speak into my microphone so let me
[00:11:37] run it what is the temperature outside
[00:11:41] so it captured my voice the microphone
[00:11:45] has captured my voice now I am going to
[00:11:47] run the next cell and perfect so you can
[00:11:50] see that it has converted my speech into
[00:11:54] the text and you can see that it has
[00:11:56] converted whatever I spoke just now I
[00:11:59] spoke a sentence like what is the
[00:12:01] temperature outside and the speech
[00:12:04] recognition package basically captured
[00:12:08] that speech using a microphone and
[00:12:10] converted it into the text and it is
[00:12:15] pretty much accurate as you can see here
[00:12:17] now if you have a noisy background then
[00:12:19] he going to reduce its effect by util
[00:12:22] the previously used method called add
[00:12:24] just for ambient noise of recognizer
[00:12:27] class and we can use this method or
[00:12:30] right before a lesson method as you can
[00:12:33] see here and then can reduce the effect
[00:12:36] of the noise in the background
[00:12:38] so folks this is it for this video in
[00:12:42] the next video I am going to show you
[00:12:44] how to develop a speech recognition
[00:12:46] project in a step-by-step manner so stay
[00:12:50] tuned here is the today's question how
[00:12:53] can we see all the possible most likely
[00:12:55] transcripts of a particular noisy speech
[00:12:58] please post our answers comments in the
[00:13:00] comment section given below so that I
[00:13:02] can get a chance to incorporate your
[00:13:04] feedback you can also post your
[00:13:06] technical questions in the comment
[00:13:08] section and I will try to answer the
[00:13:09] same if you are watching this video and
[00:13:12] you are not already a subscriber to our
[00:13:14] channel consider clicking that little
[00:13:15] subscribe button in case you have
[00:13:17] already subscribed then click on the
[00:13:19] bell icon to receive the notifications
[00:13:21] whenever I will release a new video so
[00:13:24] thanks for hanging out with me guys I
[00:13:26] will be covering next topic in the
[00:13:27] upcoming video so keep on watching thank
[00:13:30] you