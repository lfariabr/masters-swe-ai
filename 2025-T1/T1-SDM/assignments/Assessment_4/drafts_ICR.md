## ICR
Name: Luis Faria
Project: TTrack – Torrens Degree Tracker
Date: 19/08/2025

Introduction:

During the 3 months of the course, I was able to experience the full project lifecycle, from the initial briefing to the final demonstration - and it was the first time I acted as both Software Engineer and Project Manager. In previous work experiences, I have had the opportunity to act either at one side of the project or the other, but never both at the same time.

Reflecting back on the process, I could see that I was able to apply the principles of Software Development Management like detailing and planning ahead, coding, validating with stakeholders (colleagues and Dr. Atif), getting back at details and planning, repeating the iteration process of plan -> code -> validate -> plan.

Tasks Worked On (with Dates):
An overview of tasks that I've worked on the code can be found below:
Date	Task Description
27/06/2025	First version of TTrack GUI with pandas integration
04/07/2025	Integrated sample data and file upload module	
12/07/2025	Built macOS and Windows distributions	
30/07/2025	Integrated Supabase database, allowing users to save their processed data	
05/08/2025	Layered Architecture implementation with Core, Services and Controllers	
07/08/2025  Added student_records_tab to show history of processed data
16/08/2025  Added engine matching 2.0

Problems Faced:
1. CSV parsing errors when file headers had extra spaces.
2. PyQt interface behaving differently between Windows and macOS.
3. Light and Dark mode toggle button not working.
4. Decision between using MongoDB or Supabase for database.
5. Encryption of .env file on offline app
6. Late minute change on Engine Matching

Proposed Solutions:
1. Added preprocessing to remove extra spaces from headers
2. Adjusted PyQt layouts to be responsive
3. Created a ThemeManager to handle light and dark mode
4. Chose to use Supabase, studied documentation and integrated on project
5. Added encryption of .env file during build process
6. Hardcoded ADIT and MSIT code on a dict structure to easily integrate on our data processing logic

Final Chosen Solutions:
The application runs as expected. It is able to provide login/registration options as well as simply processing data on current memory to check. 
It also offers CSV download for offline work and if logged in, possibility to save on the database.

Aside from that, it is possible to retrieve saved data for previous students by easily checking their name, student ID and progress.