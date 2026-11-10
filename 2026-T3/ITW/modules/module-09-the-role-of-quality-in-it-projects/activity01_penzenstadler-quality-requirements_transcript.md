Quality Requirements - RE Learning Glass Lecture 14 | Birgit Penzenstadler

Penzenstadler, B. (2018, April 16). Quality requirements - RE learning glass lecture 14 [Video]. About 11 minutes. The module text leaves the link blank.

[00:00:00] welcome back to requirements engineering
[00:00:03] today we'll talk about quality
[00:00:05] requirements quality let that sink in
[00:00:11] for a moment while I write down the
[00:00:12] title why did I say let that sink in for
[00:00:23] a moment people have very different
[00:00:27] understandings of what quality means for
[00:00:31] a specific software system I used to
[00:00:34] open this talk by him showing two mobile
[00:00:36] phones
[00:00:37] an iPhone and an Android phone and
[00:00:39] asking people which one they thought was
[00:00:41] higher quality and of course that choice
[00:00:44] came back to personal preferences
[00:00:46] because at this point of development
[00:00:47] they are pretty even overall in their
[00:00:51] quality now if you were a fan of how
[00:00:56] Apple products integrate all their
[00:00:58] services and then you may have a
[00:01:01] preference for the iPhone if you are a
[00:01:03] fan of tinkering yourself with your
[00:01:05] phone and maybe developing your own apps
[00:01:07] then maybe you prefer an Android phone
[00:01:09] and those qualities are not absolute so
[00:01:13] when you define the quality requirements
[00:01:15] for your system the most important
[00:01:17] choice you have to make first is what
[00:01:20] kind of quality model are we talking
[00:01:22] about so you have to choose your quality
[00:01:24] model
[00:01:37] but don't worry you don't have to make
[00:01:39] it up from scratch we do have a standard
[00:01:42] for it that you can seek inspiration
[00:01:44] from and that we tend to use in a lot of
[00:01:47] projects so there's the iso 2500 10
[00:01:52] which provides you the standard software
[00:01:54] quality models so i recommend looking
[00:01:58] into that one it essentially gives you
[00:02:01] an overview of what are the high-level
[00:02:04] quality attributes and quality
[00:02:06] characteristics we're not going to go
[00:02:09] through that either standard in this
[00:02:12] lecture because that makes more sense
[00:02:14] when we have slides where I can show the
[00:02:17] sub models of the ISO twenty five or ten
[00:02:20] what we will look into is how do i
[00:02:23] specify individual quality requirements
[00:02:27] so when I think about typical quality
[00:02:30] attributes like performance usability
[00:02:34] maintainability reliability
[00:02:36] accessibility and so on and so forth how
[00:02:40] do I note down a requirement for this
[00:02:44] let's start with a performance
[00:02:46] requirement
[00:02:57] my requirement is the schist the system
[00:03:01] should respond fast okay now imagine I'm
[00:03:14] passing this requirement on to my
[00:03:18] designers and my implementers what are
[00:03:23] they going to come back with a fast
[00:03:25] system a really fast system an
[00:03:28] incredibly fast system most likely
[00:03:31] they're gonna come back with a question
[00:03:32] like how fast is fast for you
[00:03:35] what does fast mean in the context of
[00:03:37] the system that you're developing are we
[00:03:41] talking about this giant database
[00:03:44] algorithm in the back where it's
[00:03:47] reasonable to consider a two-second
[00:03:49] response still as very fast or are we
[00:03:53] talking about a little mobile game or
[00:03:56] even more intense a safety-critical
[00:03:59] system that needs to react in
[00:04:02] nanoseconds to provide safety for the
[00:04:06] surroundings so depending on the type of
[00:04:08] system and the application context the
[00:04:11] definition of what fast is can vary
[00:04:13] wildly so we can have this as the
[00:04:18] initial description
[00:04:25] but then we also want to have a metric
[00:04:27] that tells us how fast is fast and that
[00:04:33] metric in our case we say response time
[00:04:40] should be less than half a second what
[00:04:52] we need to define next is how we're
[00:04:55] going to measure that like response time
[00:04:58] from when when the user clicks or when
[00:05:00] the system starts computing like when
[00:05:02] exactly do we do that and so in the next
[00:05:06] part to define oops typo that's getting
[00:05:12] worse
[00:05:20] the measurement and we probably have
[00:05:28] some benchmark tests that we've
[00:05:30] performed in the past with very precise
[00:05:37] instructions so we can just reference
[00:05:39] that one here or it may be a textual
[00:05:42] description that says 25 test users are
[00:05:46] gonna carry out the use cases 34 and 35
[00:05:50] and if the response time is less than
[00:05:53] half a second then this is accomplished
[00:05:56] now the last thing there is one fourth
[00:05:59] thing that we want to denote in all of
[00:06:01] our quality requirements any guesses
[00:06:04] what that could be
[00:06:05] we know the description we know what
[00:06:09] precisely we want to be able to measure
[00:06:11] and we talked about how we want to
[00:06:14] measure it
[00:06:15] take a step back what was the most
[00:06:18] important question what's the most
[00:06:21] important requestion in requirements
[00:06:23] engineering yeah why the most important
[00:06:28] question in requirements engineering is
[00:06:29] why so why should the system respond
[00:06:32] fast so number four is the rationale
[00:06:51] and we could state that otherwise the
[00:06:54] user will switch to different service so
[00:07:04] this is a risk that we know we'd be
[00:07:06] running if we couldn't fulfill this
[00:07:08] quality requirement so always know
[00:07:16] you're wise this is pretty much the
[00:07:20] structure how you could denote every
[00:07:23] single quality requirement now you may
[00:07:25] say come on it's an easy one performance
[00:07:27] really we can just put numbers on it and
[00:07:30] we're done let's try something else
[00:07:32] something where it's harder to put
[00:07:34] numbers on what will we do with
[00:07:37] usability the system should be easy to
[00:07:41] use
[00:08:00] what's going to be the number what's
[00:08:03] gonna be the metric that we measure here
[00:08:05] hmm for qualitative requirements of this
[00:08:10] kind I have two ways to break them down
[00:08:13] measure them one way is to detail them
[00:08:17] into sub requirements where I can find a
[00:08:19] precise metric so that could be for
[00:08:23] usability that I decide easy to use for
[00:08:28] me means the font size is large enough
[00:08:31] to read the colors have a contrast that
[00:08:35] does not cause a flim or contrast for
[00:08:37] the person that looks at it the system
[00:08:43] should have usage processes or use cases
[00:08:46] that I can come that I can complete in
[00:08:48] less than seven clicks all of those
[00:08:51] would be things I can put metrics on so
[00:08:53] I can either use that way to break it
[00:08:55] down or I can go a different route I can
[00:08:59] leave it as a qualitative one and I have
[00:09:02] to define a routine that would tell me
[00:09:06] when is it good enough what is easy to
[00:09:10] use so if I leave it on a qualitative
[00:09:12] level that means I need a representative
[00:09:15] user group that rates the system after
[00:09:18] use and says yep this is easy enough to
[00:09:21] use so either break it down into
[00:09:24] countable things or say test user group
[00:09:32] 90% of test user group
[00:09:41] rated ease of use at a nine out of ten
[00:09:51] so that could be my my metric and then
[00:09:55] the measurement would be the test
[00:10:01] routine take one hundred beta testers
[00:10:19] and have them rate the system after 15
[00:10:29] minutes of use
[00:10:35] finally the rationale we don't want to
[00:10:37] forget our wise - just user retention to
[00:10:46] be honest user retention otherwise the
[00:10:49] user will switch to a different service
[00:10:50] that's a very common rationale for a lot
[00:10:53] of our quality characteristics if the
[00:10:55] system is not at that level of quality
[00:10:58] then the user is probably going to walk
[00:11:00] off and use some competitor system that
[00:11:03] does the same thing but there could be
[00:11:05] more differentiated ones for example for
[00:11:07] reliability and robustness and for
[00:11:10] security and safety so here are two
[00:11:13] examples one where I have a direct
[00:11:16] metric that can respond to what I'm
[00:11:20] asking for in the description and one
[00:11:22] where I go a different route of having a
[00:11:24] number of users rate my system to say
[00:11:26] whether it fulfills a certain equality
[00:11:29] now go try that out for at least ten
[00:11:33] different quality characteristics
