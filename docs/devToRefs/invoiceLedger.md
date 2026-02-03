# Invoice Ledger Analytics
## From Excel to Interactive Business Insights with Python & Streamlit

Tags:
`#python` `#streamlit` `#dataanalytics` `#automation` `#proptech` `#engineering` `#excel` `#buildingmanagement` `#portfolioproject`

---

**How I turned a multi-year building invoice ledger into an interactive analytics dashboard — and why it changed how I think about operations, data, and engineering.**

> *"The best code is the code that quietly removes friction from people's work."*

---

## 🏢 Context: Assistant Building Manager, Real Data, Real Stakes

Over a six-week stretch, I was working as an **Assistant Building Manager** at a large residential building in the south of Sydney, closely shadowing an experienced Building Manager with 25+ years across construction, water systems, and large-scale facilities operations.

Alongside day-to-day operations, I also built small internal tools — like a [Lift Finder](https://dev.to/lfariaus/engineering-principles-applied-to-daily-life-concierge-edition-1cjh) utility and [myRoster](https://dev.to/lfariaus/myroster-from-copypaste-to-2-minute-submissions-dao) (a shift automation app) — whenever I noticed repetitive friction in the workflow.

This role exposed me to the **full operational lifecycle** of a high-rise building:

* **Stakeholder management**: Owners Corporation, committee members, residents, strata, contractors
* **Maintenance workflows**: diagnosis → contractor selection → approval → execution → validation
* **Compliance & regulation**: AFSS, fire services, inspections, reporting
* **Financial reality**: invoices, budgets, approvals, recurring vs reactive spend

And obviously — massive amounts of **data**.

Around the same time, I accepted a **Data Analyst** role at **St Catherine’s School** ([Read more](https://dev.to/lfariaus/learning-sql-server-the-hard-way-16-days-of-real-world-database-work-5hla)), which reinforced the same mindset: treat operational noise as structured data waiting to be explored.

Every single decision eventually traced back to one place.

---

## 📁 The Starting Point: An Excel Invoice Ledger

Inside the building's shared drive (*S://BuildingName/Finances/Invoices*) lived an unassuming file:

* A multi-sheet **invoice ledger**
* Spanning **4+ years**
* Thousands of rows
* Dozens of contractors
* Hundreds of services
* GST, dates, approvals, variations, reworks


![Microsoft Excel File](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/irb0oqb8zf3qm2nfo4yr.png)

On paper, it was "just Excel."

In reality, it was:

> **The financial memory of the building.**

Every question led back to it:

* *How much are we spending on fire services?*
* *Is this contractor consistently expensive or just a one-off?*
* *Why did costs spike mid-2023?*
* *Are we reacting to problems or investing preventatively?*

---

## ⚠️ The Problem: Excel Doesn't Scale with Questions

### Why Excel Became the Bottleneck

| Excel Reality | Building Management Reality |
|---------------|----------------------------|
| Manual filters | Questions come fast |
| Pivot tables break | Context changes constantly |
| One question at a time | Multiple stakeholders need answers |
| 10-minute turnaround | Decisions need justification *now* |
| Version control chaos | Audit trail required |

**The typical workflow:**
1. Open Excel (wait for thousands of rows to load...)
2. Navigate to the right sheet (Building A? B? C?)
3. Apply filters (Year... Contractor... Service...)
4. Create pivot table (if you remember how)
5. Screenshot or copy-paste results
6. **Repeat** for the next question 5 minutes later

This wasn't analysis.  
It was **manual overhead**.

And in building management, manual overhead means:
- Slower contractor evaluations
- Delayed budget approvals
- Missed spending patterns
- Reactive instead of preventative decisions

---

## 🎓 The Engineering Lens: Treating Excel as a Dataset

At the same time, I'm pursuing a **Master's in Software Engineering & Artificial Intelligence** (*see my [open-source repo](https://github.com/lfariabr/masters-swe-ai)*) — so my instinct kicked in:

> This isn't an Excel problem.  
> This is a **data exploration problem**.

✅ The ledger already had:

* **Time-series data** (4+ years of invoices)
* **Categorical dimensions** (building, contractor, service)
* **Natural aggregations** (monthly spend, contractor totals)
* **Long-term trends** (seasonal patterns, cost escalation)
* **Outliers that matter financially** (unexpected spikes, recurring issues)

The data was **already structured**.  
Microsoft Excel was just the **wrong interface** for exploration.

So I built a tool in Python that lets **non-technical users explore it safely**.

---

## 🛠️ The Solution

The goal was simple: turn a static spreadsheet into a safe, visual, self-service analytics tool for non-technical users.

I built an **interactive analytics dashboard** using **Python + Pandas + Streamlit** to read from the `ledger.xlsx` file.

![Streamlit User Interface with loaded data](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/sg3gnzjy1nv8oca6tiqr.png)

In minutes, I could answer questions that used to take 10–15 minutes of Excel wrestling — and export the evidence for emails, audits, or committee meetings.

### **What It Does**

**Upload** a raw `.xlsx` invoice ledger → Instantly:

* 🏢 **Filter by building** (or view "All" for consolidated insights)
* 📅 **Filter by year(s)** (multi-select: 2023 + 2024)
* 👷 **Filter by contractor** (compare spending across vendors)
* 🔧 **Filter by service** (HVAC vs. Plumbing vs. Fire Services)
* 🔍 **Search by invoice number** (quick lookups)
* 📆 **Date range picker** (Q3 analysis, seasonal trends)
* 💰 **Amount range slider** (focus on high-value invoices)

**Auto-compute:**

* Total spend (GST inc.)
* Invoice count
* Unique contractors
* Service diversity

**Visualize:**

* 📊 **Contractor spend breakdown** (bar chart + color-coded heatmap)
* 📈 **Monthly expense timeline** (spot trends, anomalies)
* 🎨 **Cost concentration** (which contractors dominate spend?)
* 🔄 **Multi-year comparisons** (year-over-year changes)

**Export:**

* 📥 **Download filtered results as CSV** (for reports, audits, approvals)

**No pivot tables.**  
**No broken formulas.**  
**No "give me 10 minutes to check."**

---

## 🏗️ Tech Stack & Architecture

The app follows **clean software engineering principles** — modular, maintainable, production-ready.

### **Technology Choices**

| Layer | Technology | Why |
|-------|------------|-----|
| **Language** | Python 3.10+ | Standard for data + automation |
| **Web Framework** | [Streamlit](https://streamlit.io) | Rapid UI development, zero JavaScript |
| **Data Processing** | [Pandas](https://pandas.pydata.org/) | Industry-standard DataFrames |
| **Excel Integration** | [openpyxl](https://openpyxl.readthedocs.io/) | Multi-sheet Excel parsing |
| **Visualization** | Streamlit charts + Pandas styling | Built-in, no external dependencies |
| **Deployment** | Streamlit Cloud | Free hosting, GitHub integration |

### **Project Structure**

```
invoice-ledger/
├── app.py              # Main UI orchestration
├── data_loader.py      # Excel parsing & data cleaning
├── filters.py          # Interactive filter components
├── analytics.py        # Metrics, charts, visualizations
└── requirements.txt    # Dependencies
```

**Why modular?**
- ✅ **Single Responsibility** — Each file does one thing well
- ✅ **Testable** — Unit test each component independently
- ✅ **Maintainable** — Know exactly where to make changes
- ✅ **Reusable** — Port components to other PropTech projects
- ✅ **Readable** — Onboard new devs in minutes, not hours

---

> 🔍 Full module-by-module breakdown available here → [docs/ARCHITECTURE.md](https://github.com/lfariabr/invoice-ledger/tree/main/docs/ARCHITECTURE.md)

---

## 📊 The Impact: Before vs. After

| Metric | Before (Excel) | After (Dashboard) | Improvement |
|--------|----------------|-------------------|-------------|
| **Query Time** | 10-15 minutes | ~2 minutes | **80% faster** |
| **Multi-building Analysis** | Open 3 files manually | Single "All" view | **3x faster** |
| **Visualizations** | Manual pivot tables | Auto-generated charts | **100% automated** |
| **Reproducibility** | "How did I filter this again?" | Click filters → Export CSV | **100% consistent** |
| **Contractor Comparison** | Side-by-side spreadsheets | Color-coded heatmap | **Instant insights** |
| **Trend Analysis** | Copy-paste into separate tool | Built-in timeline chart | **Native support** |
| **User Training** | "Here's how Excel works..." | "Upload and click" | **Zero onboarding** |

---

## 🎯 Real-World Use Cases

### **1. Contractor Performance Review**
**Question:**  
*"How much did we spend with ABC Plumbing across all buildings in 2024?"*

**Old way:**  
- Open 3 Excel files (Building A, B, C)
- Filter each by contractor
- Sum manually
- 5 minutes

**New way:**  
- Select "All buildings"
- Filter contractor: "ABC Plumbing"
- Filter year: "2024"
- **Answer in 30 seconds** 

The result isn’t just faster — it’s **far more presentable**, making it suitable for committee meetings, audits, and stakeholder discussions.

---

### **2. Budget Planning**
**Question:**  
*"What's our average monthly HVAC spending?"*

**Old way:**  
- Filter by service
- Create pivot table by month
- Calculate average
- Hope you didn't break formulas
- 10 minutes

**New way:**  
- Filter service: "HVAC"
- View monthly timeline chart
- **Answer visible immediately**

---

### **3. Audit Trail for Committee**
**Question:**  
*"Show me all fire services invoices over $5,000 from Q4 2024"*

**Old way:**  
- Filter by service
- Filter by date range
- Filter by amount
- Screenshot or print
- 12 minutes

**New way:**  
- Apply 3 filters
- Click "Download CSV"
- Attach to email
- **Answer + deliverable in 2 minutes**

---

### **4. Anomaly Detection**
**Question:**  
*"Why was November 2023 spending so high?"*

**Old way:**  
- Create pivot table by month
- Spot the spike
- Filter November 2023
- Manually inspect rows
- 15 minutes

**New way:**  
- View monthly timeline chart (spike visible instantly)
- Filter date range: November 2023
- Heatmap shows which contractor(s) caused it
- **Root cause in 3 minutes**

---

## Fun Fact

**Built in 1 day** as a side project during my working hours.

**Origin story:**  
Started in the `southB/` directory of my [masters-swe-ai repo](https://github.com/lfariabr/masters-swe-ai/tree/main/2025-T2/T2-Extra/southB) as a quick experiment. When I realized how useful it was, I:

1. Cleaned up the code
2. Made it modular
3. Created standalone repo
4. Wrote comprehensive documentation
5. Deployed publicly

---

## 🔗 Links & Resources

| Resource | Link |
|----------|------|
| **GitHub Repo** | [github.com/lfariabr/invoice-ledger](https://github.com/lfariabr/invoice-ledger) |
| **Source Code (southB origin)** | [masters-swe-ai/southB](https://github.com/lfariabr/masters-swe-ai/tree/main/2025-T2/T2-Extra/southB) |
| **Live Demo** | [streamlit app](https://invoice-ledger.streamlit.app/) |
| **Excel Template (fake data)** | [download & explore the data safely - *fake data*](https://github.com/lfariabr/invoice-ledger/raw/main/data/invoiceLedger.xlsx) |

---

## 🚀 Future Roadmap: From Dashboard to PropTech Platform

While the current version solves the immediate problem, here's the possible expansion plan:

### **1. Database Backend (PostgreSQL/Supabase)**
**Current:** Upload Excel each time  
**Future:** Persistent database with incremental updates

**Benefits:**
- Historical version control
- Audit trail (who queried what, when)
- Multi-user access with authentication
- API for integration with other building systems

---

### **2. Predictive Analytics (ML)**
**Use cases:**
- *"Based on 4 years of data, predict next quarter's HVAC spending"*
- *"Which contractors are trending expensive year-over-year?"*
- *"Seasonal patterns: fire services spike in winter?"*

**Technical approach:**
- Time-series forecasting (Prophet)
- Contractor spending clustering
- Anomaly detection for unusual invoices

---

### **3. Automated Reporting**
**What it does:**  
Schedule weekly/monthly reports via email

**Example workflows:**
- Every Monday: Summary of last week's spending
- End of month: PDF report with charts for Owners Corporation
- Budget alerts: Email if spending exceeds threshold

---

### **4. Integration with Building Management Systems**
**Current:** Standalone dashboard  
**Future:** Connect to existing PropTech stack

**Integrations:**
- **AFSS systems** — Auto-import fire inspection costs
- **Strata software** — Sync budget approvals
- **Contractor portals** — Pull invoices directly
- **Power BI** — Feed data to enterprise dashboards

---

## Let's Connect!

Building Invoice Ledger Analytics was a perfect case for me to **turn operational friction into engineering opportunity**. If you're:

- Working in **PropTech** or building management
- Building internal tools for **finance** or **operations**
- Interested in **Python automation** and **data visualization**
- Looking for practical **Streamlit** examples
- Hiring for **backend/data/PropTech** roles

I'd love to connect:

- **LinkedIn:** [linkedin.com/in/lfariabr](https://www.linkedin.com/in/lfariabr/)
- **GitHub:** [github.com/lfariabr](https://github.com/lfariabr)
- **Portfolio:** [luisfaria.dev](https://luisfaria.dev)

---

**Tech Stack Summary:**

| Current | Future Extensions |
|---------|-------------------|
| Python, Streamlit, Pandas, openpyxl | PostgreSQL/Supabase, ML (Prophet/LangChain), Building System APIs (AFSS, Strata), React Native/PWA |

---

*Built with ☕ and firsthand building management experience*  
*"The best code is the code that quietly removes friction from people's work."*
