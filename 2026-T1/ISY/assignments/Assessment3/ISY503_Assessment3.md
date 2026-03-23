# ASSESSMENT 3 BRIEF

## Subject Code and Title
ISY503 Intelligent Systems

## Assessment
Final Project

## Individual/Group
Group & Individual

## Length
Presentation, Code and Individual contribution report
Volume of assessment: Presentation 10-15 minutes total (group),
Individual report (250 words +/- 10%)

## Learning Outcomes
The Subject Learning Outcomes demonstrated by successful completion of
the task below include:
a. Determine suitable approaches towards the construction of AI systems.
b. Determine ethical challenges which are distinctive to AI and issues  that may arise with such rapidly developing technologies.
c. Apply knowledge based or learning based methods to solve problems in complex environments that attempt to simulate  human thought and decision making processes, allowing modern society to make further advancements.
d. Communicate clearly and effectively using the technical language  of the field and constructively engage with different stakeholders.
e. Apply the foundational principles of AI learnt throughout the  course and apply it to the different areas of Natural Language Processing, Speech Recognition, Computer Vision and Machine Learning

## Submission
Due by 11:55pm AEST/AEDT, Wednesday of Week 12

## Weighting
40%

## Total Marks
100 marks

---

## Task Summary
In  a  group  (approximately  3  or  4)  you  should  apply  the  foundational  principles  of  AI  to  a  Natural Language  Processing  (NLP)  or  Computer  Vision  project  capable of  solving  a  specific  problem.  There are two problems defined for this task – and you will need to choose one. The NLP based task is where you  can  implement  a  sentiment  analysis  project.  The  Computer  Vision  project  will  provide  you  an  opportunity to train a model based on sample data that will let you perform a a self-driving simulation without crashing or leaving the road.

If you choose the NLP-based task, your solution should be delivered as a simple website with a text box to enter a sample statement for sentiment analysis and a button to execute the sentiment analysis function. The interface should also present the outcome of executing the sentiment analysis function on  the  page.  Note  that  you  will  be  training  a  machine  learning  model  to  analyse  the  sentiments of customers  reviews  and  creating  a  prediction  function  to  allow  for the  input  text  to  be  subject  to sentiment analysis based on your trained model.

With the Computer Vision project, there is also a need to train a model that the simulator will use to
run a simulation based on sample data. The model (which is trained on this sample data) will need to
be submitted as a deliverable along with a video of a full lap of the car doing a lap in the simulator.

## Context
This  assessment  moves  further  into  solving  a  more  realistic  program  by  building  a  more  complex
Intelligent System. The Intelligent System can either be an application in Natural Language Processing or Computer Vision – two of the key focus areas in industry and academia.

The project will also give you an opportunity to hone your skills and be able to collaborate with other individuals in a team. Collaboration is common in the workplace, and therefore a skill worth practising. The group work in this assessment will help you to identify the skills you might need to refine and help  you  to  understand  how  to communicate  better  with your  team mates. There  is  also  a  presentation and  report  deliverable  that  will  help  you  practise  your  verbal  and  written  communication  skills  as
these will prove to be vital in the workplace.

## Task Instructions
You should work in a group of 3 or 4 people (depending on the numbers in your class) and the tasks of  each  person  should  be  determined  at  the  beginning  of  your  project.  This  is  important  to  ensure
expectations of individual contributions are set. You are required to use the version control tools Git that can also keep a track of collaboration between members. You also need to deliver a presentation that should be no longer than 15 minutes, and is based on the project you have implemented together.

Individually, you must also prepare a report explaining each team member's contribution to the project  (250  words).  The  individual  report  explains  the  contribution  each  person  made  to  the assessment task. Finally, you should include a self-assessment of your perceived percentage
contribution to the overall assessment task, and how much each team member contributed.  Further instructions and detail are provided below.

To complete this assessment task you must:

- Participate in a group project to develop an NLP or a Computer Vision project. Your project can either be the NLP or the Computer Vision application.

### Natural Language Processing Project Instructions
- In case of the NLP, you need to use the following link to the dataset http://www.cs.jhu.edu/~mdredze/datasets/sentiment/index2.html The dataset is a collection of Amazon product reviews across several categories. Your task will be to train a neural network to perform sentiment analysis to allow it to match with one of the categories in the dataset. Note that the dataset already contains labelled data for positive and negative reviews. You should load all the negative and positive comments, mix and randomise the data, take some percentage of data to train your model, and use the rest for testing your model. Your solution needs to be able to:
    - Clean the data (punctuation, spelling etc.)
    - Encode the words in the review
    - Encode the labels for 'positive' and 'negative'
    - Conduct outlier removal to eliminate really short or wrong reviews.
    - Pad/truncate remaining data
    - Split the data into training, validation and test sets
    - Obtain batches of training data (you may use DataLoaders or generator functions)
    - Define the network architecture
    - Define the model class
    - Instantiate the network
    - Train your model
    - Test
    - Develop a simple web page/create an executable of your solution that will take an input sentence and provide an output of whether the review sentiment was positive or negative.
    - Run an inference on some test input data – both positive and negative and observe how often the model gets these right.
    - Repeat training and rearchitect the model if required.
- Keep in mind your ethical responsibility as a data science practitioner of the need to be fair and uniform in deriving accurate sentiment from a product review when conducting the above i.e. the dataset may have been split into positive and negative by the owner, however, can you identify any issues in their decision that you've now addressed? Note these in your report.
- Deploy the system on a simple website or provide an executable which can be run on the command line.
- The interface for the NLP solution should have an input field to insert an input sentence into as well as a button to execute the sentiment analysis function you've implemented. Note that the facilitator will test out a few input statements to verify the accuracy of your model's sentiment analysis capability. The execution of the sentiment analysis should produce an output once an input sentence is entered into the field and the button clicked in the form of "Positive review" or "Negative review" as a text output. If you're confident that you've trained your model sufficiently well on the training data, experiment to see what results you get when you provide it a sample input that is outside the training data.

### Computer Vision Project Instructions
- IF you choose to work on the Computer Vision project, you will work on Udacity's self-driving car simulator project. The download link to the simulator is provided below as is the training data. Your task is to build a machine learning model that is trained on the data provided and when run on the simulator, will hopefully keep the car on the road without running off track. You can download the Simulator here: https://github.com/udacity/self-driving-car-sim. Follow the instructions on this page
to install the game and its requisite frameworks.
- You will then use the images in the Assessment 3 folder in Blackboard to train your model.
    - You will find three folders (Left, Right, and Forward) when you unzip the file. Use these images to train your model.
- This project will require you to submit your code files on GitHub including the following:
    - model.py (script used to create and train the model)
    - drive.py (script to drive the car - feel free to modify this file)
    - model.h5 (a trained Keras model)
    - video.mp4 (a video recording of your vehicle driving autonomously around the track for at least one full lap)
- You may consult the website https://medium.com/activating-robotic-minds/introduction-to-udacity-self-driving-car-simulator-4d78198d301d for assistance on how to work with the simulator. This file is also in your Assessment 3 folder in Blackboard.
- Keep in mind your responsibilities as a data science practitioner and consider the ethical considerations of an application as a self-driving car. - For instance, the need to consider the various factors on the road when a machine is in charge of navigating the vehicle.
- Use version control tools and pair programming through Git for either project. The project should be submitted to Github and the link to Github should be provided in the report.

### Group Presentation and Individual Report Instructions
- Participate in a group presentation of your work (this means each of you must present for a few minutes). The presentation should address rationale behind the choice of project, any ethical considerations made during implementation, the accuracy of the outputs observed, and a brief explanation of implementation. The presentation delivery should be split among
the team members. It is up to the group to determine who submits the final video presentation (in Blackboard). You may want to have an online group meeting (zoom/skype etc) where you record yourselves presenting (sharing your screen with the ppt as the primary view, and each of you present your section verbally over the top).
- Write a short individual report (250 words) specifying your contribution to the work and the perceived contribution of the other members of your group. The total of your percentages should add to 100% (e.g., Tom: 15%, Rajiv 25%, Esfir 30%, Jasmine 30%).
    - The manual should list any ethical considerations about NLP or Computer Vision based on your selected project cited with APA referencing.

## Referencing
It is essential that you use appropriate APA style for citing and referencing research. Please see more information on referencing here http://library.laureate.net.au/research_skills/referencing

## Submission Instructions
There are three elements that need to be completed for Assessment 3:
1. Group Code (only one member of the group needs to submit this)
2/ Group video Presentation (only one member of the group needs to submit the final version
of this)
3. Individual report and contribution summary, this includes a list of your team members with student ID's (each team member must submit this individually)

Submit this task via the Assessment 3 link in the main navigation menu in ISY503: Intelligent Systems. If you have any questions or concerns please get in touch with your learning facilitator early, do not leave this until the last minute. The Learning Facilitator will provide feedback via the Grade Centre in the LMS portal. Feedback can be viewed in My Grades

## Academic Integrity Declaration
Individual assessment tasks:

I declare that except where I have referenced, the work I am submitting for this assessment task is my own work. I have read and am aware of Torrens University Australia Academic Integrity Policy and Procedure viewable online at http://www.torrens.edu.au/policies-and-forms

I am aware that I need to keep a copy of all submitted material and their drafts, and I will do so accordingly.

Group assessment tasks:
We declare that except where we have referenced, the work we are submitting for this assessment task is our own work. We have read and are aware of Torrens University Australia Academic Integrity Policy and Procedure viewable online at http://www.torrens.edu.au/policies-and-forms

We are aware that we need to keep a copy of all submitted material and their drafts, and we will do so accordingly.

---

## Assessment Rubric

| Assessment Attributes | Fail (Yet to achieve minimum standard) 0–49% | Pass (Functional) 50–64% | Credit (Proficient) 65–74% | Distinction (Advanced) 75–84% | High Distinction (Exceptional) 85–100% |
|---|---|---|---|---|---|
| **Project Correctness** — The project has determined a suitable approach towards the construction of AI systems, including any ethical considerations that are relevant. **Percentage: 40%** | Project has not been implemented or delivered or has been copied from external source without any modifications (the source of NLP or Computer Vision project should be mentioned in the manual report). Ethical considerations are not considered. | The NLP or Computer Vision project has been modified a little not showing enough contribution from students (the contributed parts should be highlighted with comments and the main source should also be mentioned in the manual report). Ethical considerations are mentioned without addressing the potential concerns. | The NLP or Computer Vision project has been implemented in such a way that shows sufficient contribution of students to it. In other words, it is not just copied from another source (the contributed parts should be highlighted with comments and the main source should also be mentioned in the manual report). If the NLP project has been implemented, it allows for inputs through a text box on a web interface or through a command line executable. When a sample positive or negative input statement is provided (from the training data), it provides the right sentiment classification 80% of the time. In case of Computer Vision solution, the model has been trained on the provided training data and successfully completes a lap on the road with some deviations. Ethical considerations are identified and discussed. | The NLP or Computer Vision project has been implemented in such a way that shows sufficient contribution of students to it. In other words, it is not just copied from another source (the contributed parts should be highlighted with comments and the main source should also be mentioned in the manual report). If the NLP project has been implemented, it allows for inputs through a text box on a web interface or through a command line executable. When a sample positive or negative input statement is provided (from the training data), it accurately (>90% but less than 100% of the time) provides the right sentiment classification. In case of Computer Vision solution, the model has been trained on the provided training data and successfully completes a lap on the road with only a few minor deviations. Ethical considerations are highlighted and addressed in detail. | The NLP or Computer Vision project has been implemented in such a way that shows sufficient contribution of students to it. In other words, it is not just copied from another source (the contributed parts should be highlighted with comments and the main source should also be mentioned in the manual report). If the NLP project has been implemented, it allows for inputs through a text box on a web interface or through a command line executable. When a sample positive or negative input statement is provided (not necessarily from the training data), it accurately (100% of the time) provides the right sentiment classification. In case of Computer Vision solution, the model has been trained on the provided training data and successfully completes a lap on the road with no deviations. Ethical considerations are highlighted and comprehensively addressed. |
| **Effective Communication (Presentation/Oral)** — Evidence of clear communication and effective use of the technical language of the field. **Percentage: 30%** | Difficult to understand for audience, no logical/clear structure, poor flow of ideas, argument lacks supporting evidence. Specialised language and terminology is rarely or inaccurately employed. Stilted, awkward and/or oversimplified delivery. Limited use of engaging presentation techniques. Presentation aids are not employed or developed as directed. No reference is made to the following within the presentation content: the rationale behind the choice of project, any ethical considerations made during implementation, the accuracy of the outputs observed, and a brief explanation of implementation. | Presentation is sometimes difficult to follow. Information, arguments and evidence are presented in a way that is not always clear and logical. Employs some specialised language and terminology with accuracy. Correct, but often stilted or awkward delivery. Sometimes uses engaging presentation techniques (e.g. posture; eye contact; gestures; volume, pitch and pace of voice). Employs basic, but generally accurate presentation aids as directed. A number of aspects require further refinement (e.g. amount of information, styling, editing, etc.). The content of the presentation mentions some of the following: the rationale behind the choice of project, any ethical considerations made during implementation, the accuracy of the outputs observed, and a brief explanation of implementation. | Presentation is easy to follow. Information, arguments and evidence are well presented, mostly clear flow of ideas and arguments. Accurately employs specialised language and terminology. Correct, but occasionally stilted or awkward delivery. Uses engaging presentation techniques (e.g. posture; eye contact; gestures; volume, pitch and pace of voice). Employs clear and somewhat engaging presentation aids as directed. A few aspects require further refinement (e.g. amount of information, styling, editing, etc.). The content of the presentation briefly touches on each of: the rationale behind the choice of project, any ethical considerations made during implementation, the accuracy of the outputs observed, and a brief explanation of implementation. | Engages audience interest. Information, arguments and evidence are very well presented; the presentation is logical, clear and well-supported by evidence. Accurately employs a wide range of specialised language and terminology. Clear and confident delivery. Confidently and consistently uses a range of engaging presentation techniques (e.g. posture; eye contact, expression; gestures; volume, pitch and pace of voice; stance; movement). Employs succinct, styled and engaging presentation aids that incorporate a range of elements (graphics, multi-media, text, charts, etc.). The content of the presentation addresses in some detail: the rationale behind the choice of project, any ethical considerations made during implementation, the accuracy of the outputs observed, and a brief explanation of implementation. | Engages and sustains audience interest. Expertly presented; the presentation is logical, persuasive, and well-supported by evidence, demonstrating a clear flow of ideas and arguments. Discerningly selects and precisely employs a wide range of specialised language and terminology. Clear, confident and persuasive delivery. Dynamic, integrated and professional use of a wide range of engaging presentation techniques (e.g. posture; eye contact, expression; gestures; volume, pitch and pace of voice; stance; movement). Employs succinct, creative and engaging presentation aids that effectively integrate a wide range of elements (graphics, multi-media, text, charts, etc.). The content of the presentation addresses in great detail: the rationale behind the choice of project, any ethical considerations made during implementation, the accuracy of the outputs observed, and a brief explanation of implementation. |
| **Individual Contribution** — Individual report and contribution summary. **Percentage: 30%** | No evidence of individual contribution. No report with self-assessment and team members' assessment has been provided. | A report with self-assessment and team members' assessment has been provided. Basic attempt at describing individual contribution in the report and group code. No ethical considerations of NLP or Computer Vision based on the selected project has been listed in the report. | A report with self-assessment and team members' assessment has been provided. The report and group code demonstrates a structure of contribution from team members with individual contribution briefly discussed. The report lists at least one reasonable ethical aspect of the chosen project. | A report with self-assessment and team members' assessment has been provided. The report and group code demonstrates a considered effort in establishing a structure of contribution from team members with individual contributions discussed in detail. The report lists multiple reasonable ethical aspects of the chosen project. | A manual with self-assessment and team members' assessment has been provided. The report demonstrates significant thought being given to establishing a structure of contribution from team members with individual contributions of the student to the project explained in detail. The report lists multiple reasonable ethical aspects and their implications on the chosen project. |

---

## The following Subject Learning Outcomes are addressed in this assessment

| SLO | Description |
|-----|-------------|
| SLO a) | Determine suitable approaches towards the construction of AI systems. |
| SLO b) | Determine ethical challenges which are distinctive to AI and issues that may arise with such rapidly developing technologies. |
| SLO c) | Apply knowledge based or learning based methods to solve problems in complex environments that attempt to simulate human thought and decision making processes, allowing modern society to make further advancements. |
| SLO d) | Communicate clearly and effectively using the technical language of the field and constructively engage with different stakeholders. |
| SLO e) | Apply the foundational principles of AI learnt throughout the course and apply it to the different areas of Natural Language Processing,  Speech Recognition, Computer Vision and Machine Learning. |
