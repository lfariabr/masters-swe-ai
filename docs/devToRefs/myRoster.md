# myRoster: from copypaste to 2-minute submissions

#python #productivity #automation #pandas

**From tedious spreadsheet rituals to 2-minute submissions: how I turned a workplace pain point into a productivity multiplier.**

> *"The best automation isn't flashy — it's invisible. It just works."*

---

## 🎯 The Challenge:
### When Spreadsheets Become a Time Sink

If you've ever worked in shift-based operations, you know the drill. Every roster cycle, the same tedious routine: open a spreadsheet, manually tick boxes for every single day you're available, triple-check you didn't miss anything, export it, draft an email, attach the file, and finally hit send. Rinse and repeat, week after week. 

![Email asking for availability](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/mdbgehalj1cfzmzdnjsr.png)

For one HR team I've met, this process was eating up valuable time that could have been spent on actual work:

| Pain Point | Impact |
|------------|--------|
| **Manual entry** | 15-20 minutes per roster cycle per employee |
| **Inconsistent formats** | HR receives varied submissions, coordination nightmare |
| **Error-prone** | Missed dates, wrong shifts, duplicate entries |
| **Soul-crushing** | Nobody looks forward to roster week |

I saw this inefficiency firsthand and thought: *There has to be a better way.*

> **Spoiler:** There was.

---

## 🤖 The Solution:
### _myRoster_: Automation Meets Simplicity

That's when **myRoster** was born: A lightweight and intuitive web application that transforms shift availability submission from a chore into a 2-minute task. 

![myRoster Web App](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/u678436flo6v69l7nbp8.png)

### **How It Works**

myRoster is built as a **Streamlit-powered** web app that runs entirely in the browser. No complex installations, no training sessions—just open the link and you're ready to go. Here's what makes it tick:

**1. Smart Roster Period Calculation** 
The app automatically calculates the next roster cycle based on HR's scheduling logic. No more guessing which dates to fill out—the system knows exactly what period you're submitting for, starting from the Monday three weeks ahead and spanning a full 4-week cycle.

**2. Interactive Spreadsheet Interface** 
Instead of static forms, users interact with a familiar spreadsheet-like grid. Each week is organized in collapsible sections, showing dates, days of the week, and three shift columns (7am-3pm, 3pm-11pm, 11pm-7am). Just click the checkboxes for your available shifts—no hunting through dropdowns or typing dates manually.

**3. One-Click Weekly Shortcuts** 
Need to mark yourself available for all morning shifts in a week? One button. Want to clear an entire week? Another click. These shortcuts eliminate repetitive clicking, cutting entry time by more than half.

**4. Real-Time Progress Tracking** 
As you make selections, myRoster instantly updates your coverage statistics—showing total shifts selected, number of days covered, and a visual progress bar. You know exactly where you stand before submitting.

**5. One-Click Submission** 
Hit "Preview & Submit," and myRoster generates a clean CSV file, automatically emails it to HR with a professional HTML template, and optionally sends you a copy. The entire process—from opening the app to hitting send—takes under 2 minutes.

### Tech Stack

I kept the technology intentionally lean:

| Layer | Technology | Purpose |
|-------|------------|---------|  
| **Backend** | Python 3.10+ | Core logic, date calculations |
| **Frontend** | Streamlit | Interactive web UI, zero JS needed |
| **Data** | Pandas | Shift matrices, CSV export |
| **Email** | Gmail SMTP (GCP) | Automated delivery |
| **Deployment** | Streamlit Cloud | One-click deploy from GitHub |

**Project Structure:**
```
myRoster/
├── app.py                    # Main Streamlit entry point
├── views/
│   └── rosterView.py         # UI components
├── helpers/
│   └── roster.py             # Date calculations
└── services/
    └── email.py              # Email automation
```

The modular architecture makes it easy to extend features or adapt for different scheduling needs.

---

## The Impact: Time Saved, Efficiency Gained

The results speak for themselves:

| Metric | Before | After |
|--------|--------|-------|
| **Submission time** | 15-20 minutes | ~2 minutes |
| **Format consistency** | Varies by employee | 100% standardized |
| **Error rate** | Frequent | Zero |
| **Employee satisfaction** | Dreaded task | Quick and painless |

---

## Future Roadmap: From MVP to Platform

While myRoster already delivers significant value in its current form, there's immense potential to evolve it from a standalone tool into a comprehensive workforce management platform. Here's what I've mapped out:

### **1. Multi-Provider Email Infrastructure**
**Current state:** Relies solely on Gmail SMTP via Google Cloud Platform 
**Next iteration:** Integration with [Resend](https://resend.com) for more reliable transactional email delivery

**Why this matters:**
- **Automated reminders**: Schedule notifications 48 hours before roster deadlines
- **Smart alerts**: Notify HR when submissions are incomplete or coverage is below threshold
- **Employee confirmations**: Send automatic receipts when availability is successfully submitted
- **Higher deliverability**: Resend offers better inbox placement and detailed analytics compared to SMTP

This would transform myRoster from a submission tool into an active communication hub that keeps everyone informed and on track.

---

### **2. Robust Backend with Supabase**

**Current limitation:** No persistent user data, authentication, or preferences 
**Next evolution:** Full-stack upgrade with Supabase as the backend

**Features unlocked:**
- **Authentication**: Secure login with email/password or SSO via EmploymentHero
- **User profiles**: Save preferred shifts, notification settings, and contact preferences
- **Historical data**: View past submissions, track coverage trends over time
- **Saved drafts**: Start filling out availability, save progress, and return later
- **Admin dashboard**: HR users get real-time coverage analytics, submission status tracking, and bulk operations
- **Role-based access control**: Employees, HR, and managers see different views and capabilities

**Why Supabase?**
- PostgreSQL database with real-time subscriptions (perfect for live coverage updates)
- Built-in authentication and row-level security
- RESTful and GraphQL APIs out of the box
- Integrates seamlessly with Python backends
- Free tier suitable for MVP, scales affordably

**Migration path:** 
Current CSV-based workflow becomes a fallback option while Supabase gradually handles user data, preferences, and analytics storage.

---

### **3. Machine Learning #1: Pattern Recognition & Predictive Scheduling**

**What it does:** 
Analyze historical availability data to identify patterns in employee behavior, building coverage needs, and seasonal trends. 

**Use cases:**
- **Coverage prediction**: "Based on historical data, Building A typically has low evening shift coverage in December. Flag this 3 weeks in advance."
- **Employee behavior insights**: "User X consistently submits availability on the last day—send them an early reminder."
- **Building-specific trends**: "Building B requires 15% more morning shifts during summer months—adjust recommendations accordingly."
- **Anomaly detection**: Flag unusual submission patterns that might indicate scheduling conflicts or errors

**Technical approach:** 
- Time-series analysis using scikit-learn or Prophet
- Clustering algorithms to group similar availability patterns
- Lightweight models that can run serverless (no heavy infrastructure needed)

**Real-world impact:** 
HR teams can proactively address coverage gaps before they become emergencies, and employees get personalized nudges based on their actual behavior patterns.

---

### **4. Machine Learning #2: RAG-Powered Knowledge Base**

**Inspired by:** [AI Engineering na Prática: Construindo RAG com Neural Networks](https://newsletter.nagringa.dev/p/ai-engineering-na-pratica-construindo)

**What it does:** 
Build a conversational AI assistant powered by Retrieval-Augmented Generation (RAG) that understands roster policies, shift rules, and employee FAQs.

**Employee experience:**
- *"Which shifts do I need to fill for Christmas week?"* 
 → AI retrieves company holiday policies + roster dates and provides personalized guidance
- *"What happens if I can't work my scheduled shift?"* 
 → AI surfaces shift swap procedures, contact info, and deadline policies
- *"Show me my availability history for Q4 2025"* 
 → AI queries the database and presents formatted historical data

**HR experience:**
- Automated responses to repetitive questions
- Instant access to shift coverage analytics via natural language queries
- Policy enforcement reminders embedded in the chat experience

**Technical stack:**
- **Vector database** (Pinecone, Weaviate, or Supabase pgvector) for document embeddings
- **LLM integration** (OpenAI GPT-4, Claude, or open-source alternatives like Llama)
- **RAG framework** (LangChain or LlamaIndex) for retrieval logic
- **Knowledge base**: Company policies, shift rules, historical data, and FAQs

**Why this is powerful:** 
Instead of just automating form submission, myRoster becomes an intelligent assistant that *understands* the nuances of scheduling, reduces HR support burden, and makes policy information instantly accessible. 

---

### **5. EmploymentHero API Integration**

**Current pain point:** Employees submit via myRoster → HR manually copies CSV data into EmploymentHero 
**Automated future:** Direct API integration eliminates manual data entry entirely

**How it works:**
1. Employee submits availability in myRoster
2. System authenticates via EmploymentHero API
3. Availability data is automatically synced to the employee's EH profile
4. HR sees updated availability directly in their scheduling dashboard—no CSV, no copy-paste, no errors

**Additional benefits:**
- **Bi-directional sync**: Pull existing shift schedules from EH into myRoster for reference
- **Conflict detection**: Cross-reference submitted availability against existing scheduled shifts
- **Deeper insights**: Combine myRoster's ML analytics with EH's payroll and attendance data for comprehensive workforce planning
- **Single source of truth**: Eliminate data duplication and version control issues

**Technical implementation:** 
EmploymentHero provides a REST API with endpoints for employee data, shift scheduling, and time & attendance. Integration would involve:
- OAuth 2.0 authentication
- Middleware service to translate myRoster data models into EH-compatible formats
- Webhook listeners for real-time updates from EH back to myRoster

**Real-world impact:** 
This closes the loop entirely. What started as "save 15 minutes per employee" becomes "eliminate an entire manual workflow for HR"—potentially saving dozens of hours per roster cycle across the organization.

> *Curious about the Timeline? Check my [CHANGELOG](https://github.com/lfariabr/roster/blob/main/docs/CHANGELOG.md) for a detailed breakdown.*

---

## Key Takeaways

This project reinforced principles I apply to every build:

1. **Start with the pain point**: Every feature traces back to real user frustration
2. **Ship fast, iterate often**: MVP in days, not months
3. **Boring tech wins**: Streamlit + Pandas = production-ready in hours
4. **Design for extensibility**: Modular architecture enables future growth
5. **Measure impact**: 90% time reduction is the kind of number that screams ROI

---

## Try It Yourself

myRoster is live and open source:

| Resource | Link |
|----------|------|
| **Live Demo** | [myroster.streamlit.app](https://myroster.streamlit.app/) |
| **Source Code** | [github.com/lfariabr/roster](https://github.com/lfariabr/roster) |

If you're building internal tools or automating workflows, I'd love to hear how you approach similar problems.

---

## Let's Connect!

Building myRoster has been a perfect example of turning workplace friction into engineering opportunity. If you're:

- Automating internal workflows
- Building tools with Streamlit
- Passionate about practical productivity solutions
- Interested in Python automation

I'd love to connect:

- **LinkedIn:** [linkedin.com/in/lfariabr](https://www.linkedin.com/in/lfariabr/)  
- **GitHub:** [github.com/lfariabr](https://github.com/lfariabr)  
- **Portfolio:** [luisfaria.dev](https://luisfaria.dev)

---

**Tech Stack Summary:**

| Current | Future |
|---------|--------|
| Python, Streamlit, Pandas, Gmail SMTP (GCP) | Supabase, Resend, OpenAI/RAG, EmploymentHero API, ML (scikit-learn/Prophet) |

--- 

*Built with ☕ and automation by [Luis Faria](https://luisfaria.dev)*