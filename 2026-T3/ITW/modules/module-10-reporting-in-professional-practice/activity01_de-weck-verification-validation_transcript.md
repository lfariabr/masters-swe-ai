Verification and Validation - MIT Fundamentals of Systems Engineering, Lecture 9 | Olivier de Weck

MIT OpenCourseWare. (2017, August 10). *9. Verification and validation* [Video]. YouTube. https://www.youtube.com/watch?v=-63JXElqPaY. Full lecture 1:37:49; the activity asks for the first eight minutes, transcribed here to 00:08:07 from the video's English captions (CC BY-NC-SA).

[00:00:26] OLIVIER DE WECK: OK so let's start on the material.
[00:00:29] We're following the V-model and the empty boxes
[00:00:33] are getting fewer and fewer every week here.
[00:00:36] So we're on the right side moving up
[00:00:40] toward lifecycle management and operations.
[00:00:42] And today's topic is via V&V, verification validation.
[00:00:47] And I also want to discuss the FRR
[00:00:49] as one of the key milestones, and that's the flight readiness
[00:00:54] review.
[00:00:54] If you're not building something that flies,
[00:00:56] this is your launch to market, right launch to market review.
[00:01:00] Are you ready to launch your project or product to market?
[00:01:04] The outline is-- we have quite a few things to cover.
[00:01:07] So first of all, I want to drill into verification
[00:01:10] and validation.
[00:01:11] What's the difference?
[00:01:13] What is their role?
[00:01:14] What's their position in the lifecycle?
[00:01:16] Then we'll spend quite a bit of time on the issue of testing.
[00:01:20] What kind of testing is done?
[00:01:22] Why is it done?
[00:01:23] We'll talk about aircraft testing, flight testing,
[00:01:26] we'll talk about spacecraft testing, but also some caveats.
[00:01:29] Testing is not always the--
[00:01:33] it's not free of challenges and difficulties.
[00:01:36] Then I want to talk about technical risk management,
[00:01:39] which is often covered in classes on project management,
[00:01:43] but I think it's essential here as well as a system
[00:01:45] engineer to have a good grasp on technical risk management.
[00:01:49] So I'll cover the risk matrix, the Iron Triangle,
[00:01:52] cost, schedule, scope, and risk, and then
[00:01:55] I added a small section on system safety, which is
[00:01:59] a very important topic as well.
[00:02:01] And we'll finish up with discussing the FRR, the flight
[00:02:04] readiness review.
[00:02:06] So the readings related to this lecture
[00:02:08] are sections 5.3 and 5.4 in the handbook, the System
[00:02:13] Engineering Handbook, and then there's
[00:02:14] a couple of appendices there, Appendix E And I
[00:02:17] that are very, very helpful.
[00:02:19] And at least one of these I'll mention in the lecture.
[00:02:22] Plus one of the papers, and this is a paper about a decade old--
[00:02:27] and I know a lot of work has been done on this since then,
[00:02:30] but this is a paper by Professor Leveson.
[00:02:34] Nancy Leveson was a colleague of mine
[00:02:36] here at MIT who's really an expert in systems safety.
[00:02:41] So the system safety model that she's developed
[00:02:45] is the subject of that paper.
[00:02:49] OK, so let's talk about V&V, verification and validation,
[00:02:53] and how they fit together.
[00:02:55] You've seen this diagram before, but I just
[00:02:57] want to talk through it in some detail again.
[00:03:01] So the idea is you start your project,
[00:03:03] you're undertaking, in the upper left.
[00:03:05] You do your stakeholder analysis.
[00:03:07] Who are the stakeholders, the customers, beneficiaries,
[00:03:10] the regulators, the suppliers, the partners on the project?
[00:03:16] So you really have to do a good job doing your stakeholder
[00:03:18] analysis then in order to write your requirements.
[00:03:23] And I do have to say I've been very pleased, especially
[00:03:25] with your assignment A-2.
[00:03:28] You really dug into those 47 requirements for canned set.
[00:03:31] You grouped them, you scrubbed them, you did a great job.
[00:03:35] And the idea is that for each of these requirements,
[00:03:38] you also have target values.
[00:03:40] There are certain thresholds or target values
[00:03:42] that have to be achieved.
[00:03:44] And then you actually do the development.
[00:03:47] You do the conceptual design, the detailed design,
[00:03:50] and that's written here as functional deployment.
[00:03:52] In other words, especially for the functional
[00:03:55] and the performance requirements,
[00:03:57] how will you actually implement those,
[00:03:59] embody those, in technology, hardware, software,
[00:04:02] and so forth.
[00:04:03] So that's your intended function, your concept,
[00:04:06] and then you're implemented design solution.
[00:04:09] Now the question is, do you actually
[00:04:13] satisfy A, the requirements, and do you
[00:04:16] satisfy your stakeholders?
[00:04:18] And it is possible that you satisfy the requirements,
[00:04:21] but not the stakeholders.
[00:04:23] So the way to think about this is
[00:04:24] we're going to close the loop.
[00:04:26] In fact, we're going to close two loops.
[00:04:28] An inner loop-- and I put testing here.
[00:04:32] Testing is really one of the ways
[00:04:34] to verify whether you meet requirements.
[00:04:37] There's other ways too, but testing is often
[00:04:39] the most important.
[00:04:41] So we close this inner loop.
[00:04:43] So what we ask is--
[00:04:45] we test our implemented solution,
[00:04:48] our implemented design, and ask the question, did we deliver?
[00:04:53] Did we actually satisfy the requirements
[00:04:55] as they were written?
[00:04:57] Do we satisfy the requirements as they were written?
[00:05:00] And are these attainable?
[00:05:02] Were these requirements attainable?
[00:05:04] So this loop here, this inner loop, is the verification loop.
[00:05:07] You verify whether you design as implemented satisfies
[00:05:12] the requirements as written.
[00:05:14] That's what verification is.
[00:05:16] And then there's an outer loop where
[00:05:18] you take your implemented design solution,
[00:05:21] and you essentially bring it all the way back
[00:05:26] to the stakeholders.
[00:05:27] And usually that also means you're employing it
[00:05:30] in a realistic environment, like in the environment
[00:05:33] that the stakeholders will actually use the system,
[00:05:36] not in a pristine lab environment.
[00:05:40] And you have the stakeholders try out your system
[00:05:45] and see whether they're satisfied, whether this
[00:05:47] meets their original intent.
[00:05:49] You remember the CONOPS, concept of operations?
[00:05:52] Can you actually do the CONOPS the way
[00:05:54] you had envisioned it in a realistic environment?
[00:05:57] And that's what we call validation.
[00:06:00] And that's the outer loop.
[00:06:01] You see the difference?
[00:06:03] So a lot of people who don't know system engineering who
[00:06:06] have never been exposed to this when they hear verification
[00:06:08] and validation, they think it's basically two different words
[00:06:12] for the same thing.
[00:06:14] It is it is different, it's not the same thing.
[00:06:18] And then if you successfully verify and validate,
[00:06:21] you end the SE process and you deliver, which is good.
[00:06:25] So this is something I pulled out
[00:06:28] from the handbook, which is the differences
[00:06:30] between verification and validation.
[00:06:32] And I'm just summarizing this here.
[00:06:34] So one way to ask is, was the end product realized right?
[00:06:39] Meaning, did you do the right thing?
[00:06:42] Or did you implement it correctly?
[00:06:44] So verification is often done during development,
[00:06:47] so you verify components, subsystems,
[00:06:50] you check if the requirements are met.
[00:06:52] Typically, verification is done in a laboratory environment,
[00:06:56] or on a test stand, or some environment that
[00:07:00] allows you to very carefully control the test conditions.
[00:07:05] And verification tends to be component and subsystem
[00:07:08] centric.
[00:07:09] OK, and then validation is the question
[00:07:12] was the right end product realized?
[00:07:15] Did you actually build the right thing?
[00:07:17] Did you deploy the right solution?
[00:07:20] This is often done-- so validation
[00:07:21] focuses more on during or after system integration.
[00:07:26] It's typically done in a real or simulated mission environment.
[00:07:30] You check if your stakeholder intent is met.
[00:07:32] And it's often done using the full-up system.
[00:07:35] It's difficult to do validation on a subsystem basis alone.
[00:07:40] Typically, validation implies you've
[00:07:42] got to use the whole system to do it.
[00:07:46] Or, you basically use dummy subsystems.
[00:07:50] You basically replace the actual subsystems
[00:07:52] you're going to have with something
[00:07:54] temporary so that you can go back to the stakeholder
[00:07:58] and give them as close to the real experience
[00:08:01] as they'll have with the actual system.
[00:08:03] OK, so that's essentially the distinction here.
