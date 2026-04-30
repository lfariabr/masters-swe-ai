[00:00:07] hi my name is Amy Feldman director of
[00:00:10] product marketing for application
[00:00:12] performance management at broad comms
[00:00:14] enterprise software division today I'm
[00:00:16] going to be talking to you about how to
[00:00:18] gain insights into modern application
[00:00:21] environments so as many organizations
[00:00:25] start their journey and digital
[00:00:26] transformations one of the easiest
[00:00:28] things that they do is to start moving a
[00:00:31] lot of their current services into
[00:00:34] containerized environments this allows
[00:00:39] them to be able to get a good
[00:00:41] understanding of how containers will
[00:00:43] work in their particular environment now
[00:00:45] as these organizations start to evolve
[00:00:48] and adding more digital services that
[00:00:51] might be available through a mobile
[00:00:53] device or even adding in IOT devices as
[00:00:58] part of their digital strategy they
[00:01:00] continue to evolve and start to adopt
[00:01:03] more complex micro services
[00:01:08] architectures and in a lot of ways they
[00:01:11] also start to adopt cloud native
[00:01:14] applications now certainly over the past
[00:01:18] several years we have seen the rise of
[00:01:20] containers and according to recent
[00:01:23] research over seventy five percent of
[00:01:27] organizations by 2022 will be using
[00:01:30] containers even more interesting is that
[00:01:34] 50 percent of these will span across
[00:01:37] multiple clouds now as we start to move
[00:01:46] into these micro services architectures
[00:01:48] one of the things that needs to be
[00:01:51] considered is how do I operate
[00:01:54] orchestrate and scale these environments
[00:01:56] so what ends up happening is that you
[00:01:58] end up starting to use technologies such
[00:02:01] as kubernetes and kubernetes allows you
[00:02:04] to be able to do just that be able to
[00:02:07] administer scale and operate these
[00:02:09] across these distributed clouds one of
[00:02:12] the other things that
[00:02:13] very important in this type of
[00:02:16] architecture is the communication and we
[00:02:20] see now the adoption of what is called a
[00:02:24] service mesh and a service mesh provides
[00:02:27] physical routing at the particular node
[00:02:32] along with centralized distributed
[00:02:36] routing to allow for communication
[00:02:38] across these micro services this allows
[00:02:42] for a very rich and sophisticated
[00:02:45] communication and routing for these
[00:02:48] micro services as it goes across these
[00:02:50] distributed environments so as you can
[00:02:54] see from this picture it introduces a
[00:02:57] couple of different challenges these new
[00:03:00] architecture is extremely complex it's
[00:03:04] highly distributed and it's highly
[00:03:07] dynamic so when an issue does occur
[00:03:13] within the environment how do I know
[00:03:16] what is wrong why do I have this
[00:03:20] particular problem and do I even care
[00:03:23] that this problem has occurred at all so
[00:03:27] when we talk about traditional
[00:03:28] monitoring traditional monitoring
[00:03:31] approaches will use agent based
[00:03:34] technology these agents reside with
[00:03:39] inside of the environment itself and
[00:03:41] what it does is it is pulling that
[00:03:45] particular server mainframe or database
[00:03:49] or even network at regular intervals and
[00:03:52] pulling that information so it's looking
[00:03:55] for the health and the performance as
[00:03:57] related to that particular
[00:03:58] infrastructure as we move into these
[00:04:02] modern architectures that really doesn't
[00:04:06] hold true anymore and the reason is
[00:04:08] because these micro services are built
[00:04:12] to be modular and very small and because
[00:04:15] of that it becomes very difficult to be
[00:04:18] able to put an agent with inside of this
[00:04:19] container as it will consume all of the
[00:04:22] resources so what we see is that
[00:04:25] developers are now starting to
[00:04:27] add in observability as part of their
[00:04:33] service so they're using libraries and
[00:04:36] api's to be able to push out the health
[00:04:40] and performance information and even the
[00:04:43] transactional information of that
[00:04:45] particular service so what happens then
[00:04:50] is now you have this agentless ability
[00:04:55] that then looks at that observability
[00:04:59] information and aggregates it across the
[00:05:02] entire infrastructure to be able to
[00:05:05] understand the traces as they occur
[00:05:08] across the different services as well as
[00:05:10] be able to pull the health information
[00:05:12] out of those containers so as you can
[00:05:15] see this gives you a great view of your
[00:05:20] back-end services how they're performing
[00:05:21] what they're doing what the transaction
[00:05:25] looks like but as these are related to
[00:05:29] digital services and the way digital
[00:05:32] services are being consumed by your
[00:05:33] end-user it becomes extremely important
[00:05:36] for you to be able to understand how the
[00:05:38] end-users are consuming those particular
[00:05:41] services so we need to be able to
[00:05:44] monitor that end user experience and
[00:05:48] what I mean by that is you want to be
[00:05:49] able to understand what the performance
[00:05:53] looks like from the various different
[00:05:56] devices but I also want to be able to
[00:05:58] understand what that journey looks like
[00:06:01] as they're consuming that digital
[00:06:03] service I want to be able to understand
[00:06:05] the behavior from a user experience and
[00:06:08] I also want to be able to understand
[00:06:10] what devices they're coming from and
[00:06:12] what their session details look like
[00:06:15] this gives me information into exactly
[00:06:18] how my users are consuming that
[00:06:21] particular digital service now when you
[00:06:24] combine that with the backend
[00:06:26] performance that then gives you a
[00:06:28] complete picture of the health of the
[00:06:32] services you're providing to your
[00:06:33] customers now as you can see from here
[00:06:37] as this architecture becomes more and
[00:06:40] more complex
[00:06:41] axé you're adding so much more data in
[00:06:44] the aspects of the amount of metrics
[00:06:47] you're collecting the amount of logs the
[00:06:49] amount of alerts that are being produced
[00:06:51] by this environment that volume of data
[00:06:54] becomes extremely hard to be able to
[00:06:56] manage and especially if you're using
[00:06:59] disparate tools to collect this
[00:07:01] information it can become very
[00:07:03] problematic in understanding the
[00:07:05] complete picture
[00:07:06] so what's needed is an AI op solution
[00:07:09] that allows you to be able to collect
[00:07:13] aggregate and analyze the information
[00:07:16] from the user the application the
[00:07:23] infrastructure and all the way back into
[00:07:26] the network this provides you that
[00:07:29] complete end-to-end view across your
[00:07:33] entire digital supply chain now just as
[00:07:38] we've seen in traditional environments
[00:07:41] and especially traditional monitoring
[00:07:43] tools we like to have a typology the
[00:07:46] topology provides us a map that gives us
[00:07:49] a point of reference when we start
[00:07:51] moving into this world of Micra services
[00:07:53] where everything is dynamic and
[00:07:55] ephemeral it becomes a little bit more
[00:07:57] challenging to be able to understand the
[00:07:59] dependencies and the relationships so
[00:08:02] what we want to do is we want to be able
[00:08:04] to treat all of this observability
[00:08:06] information that we're collecting from
[00:08:08] this micro services architecture treat
[00:08:10] it as a first-class citizen with inside
[00:08:12] of our data model and be able to look at
[00:08:16] the service mesh for the communication
[00:08:19] between the various different end points
[00:08:21] that then provides me the additional
[00:08:24] information I need to be able to
[00:08:26] determine where is my notes where's my
[00:08:29] application and what is the dependency
[00:08:31] in the relationship between those
[00:08:32] various different components this gives
[00:08:35] me a complete topology that then I can
[00:08:38] put into an AI system that provides the
[00:08:41] context that that system needs to be
[00:08:45] able to draw those relationships and be
[00:08:47] able to come up with that causal pattern
[00:08:50] recognition
[00:08:54] so with our a IAP solution from Broadcom
[00:09:00] when you're looking at a solution you
[00:09:04] want to be able to determine that you're
[00:09:06] able to get full stack visibility so I
[00:09:11] want to be able to get my full stack
[00:09:12] visibility across users app
[00:09:14] infrastructure and network I also want
[00:09:18] an agentless approach to be able to
[00:09:23] collect the observability information I
[00:09:28] want to be able to treat it as a
[00:09:30] first-class citizen so all of this
[00:09:35] observability information needs to be
[00:09:38] consumed as part of another data set as
[00:09:40] if I were collecting for my traditional
[00:09:42] data sources and then also be able to
[00:09:45] enrich my current typology that typology
[00:09:49] is key for giving me context that I need
[00:09:56] to be able to recognize patterns and be
[00:09:59] able to predict those patterns in the
[00:10:01] future that coupled with machine
[00:10:04] learning algorithms will may allow me to
[00:10:08] be able to reduce the noise with inside
[00:10:13] of this extremely complicated system
[00:10:15] it'll allow me to improve root-cause
[00:10:19] analysis and also be able to improve
[00:10:23] prediction and give me the insights that
[00:10:27] I need to be able to deliver a good
[00:10:29] customer experience so with our AI ops
[00:10:34] solution from Broadcom you can now gain
[00:10:37] insights into these modern architectures
[00:10:39] in order to improve your overall
[00:10:42] application performance and be able to
[00:10:44] transform your overall customer
[00:10:46] experience that is key for delivering
[00:10:49] those key business services to your end
[00:10:52] users