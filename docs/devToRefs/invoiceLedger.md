# Invoice Ledger Analytics
## From Excel Pivot Table to Interactive Building Management Insights

Tags:
`#python` `#streamlit` `#dataanalytics` `#automation` `#proptech` `#engineering` `#excel` `#buildingmanagement` `#portfolioproject`

---

**How I turned a multi-year building invoice ledger into an interactive analytics dashboard — and why it changed how I think about operations, data, and engineering.**

> *"The best code is the code that quietly removes friction from people's work."*

---

## 🏢 Context: Assistant Building Manager, Real Data, Real Stakes

Over the last few weeks, I was working as an **Assistant Building Manager** at one particular building in the south of Sydney, closely shadowing an experienced Building Manager with 25+ years across construction, water systems, and large-scale facilities operations.

This role exposed me to the **full operational lifecycle** of a high-rise building:

* **Stakeholder management**: Owners Corporation, committee members, residents, strata, contractors
* **Maintenance workflows**: diagnosis → contractor selection → approval → execution → validation
* **Compliance & regulation**: AFSS, fire services, inspections, reporting
* **Financial reality**: invoices, budgets, approvals, recurring vs reactive spend

And obviously — massive amounts of **data**.

Every single decision eventually traced back to one place.

---

## 📁 The Starting Point: An Excel Invoice Ledger

Inside the building shared drive lived an unassuming file:

* A multi-sheet **invoice ledger**
* Spanning **4+ years**
* Thousands of rows
* Dozens of contractors
* Hundreds of services
* GST, dates, approvals, variations, reworks

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

| Excel Reality | Building Management Reality |
|---------------|----------------------------|
| Manual filters | Questions come fast |
| Pivot tables break | Context changes constantly |
| One question at a time | Multiple stakeholders need answers |
| 10-minute turnaround | Decisions need justification *now* |
| Version control chaos | Audit trail required |

**The typical workflow:**
1. Open Excel (wait for 1,500+ rows to load...)
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

## 🎓 The Engineering Lens: "This Is a Dataset"

At the same time, I'm completing a **Master's in Software Engineering & AI** — so my instinct kicked in:

> This isn't an Excel problem.  
> This is a **data exploration problem**.

✅ The ledger already had:

* **Time-series data** (4+ years of invoices)
* **Categorical dimensions** (building, contractor, service)
* **Natural aggregations** (monthly spend, contractor totals)
* **Long-term trends** (seasonal patterns, cost escalation)
* **Outliers that matter financially** (unexpected spikes, recurring issues)

The data was **already structured**.  
Excel was just the **wrong interface** for exploration.

So I built a tool that lets **non-technical users explore it safely**.

---

## 🛠️ The Solution

I rebuilt the ledger as an **interactive analytics dashboard** using **Python + Streamlit**.

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

## 📐 Module Breakdown (For Engineers)

### **`app.py` — Main Entry Point**
```python
def main():
    st.set_page_config(page_title="Invoice Ledger Analytics", layout="wide")
    
    # File upload
    uploaded_file = st.file_uploader("Upload Ledger Excel File", type=["xlsx"])
    
    # Load data (multi-sheet support)
    ledger_data = load_ledger(uploaded_file)
    
    # Building selector
    selected_sheet = st.sidebar.selectbox("Select Building:", ["All"] + sheet_names)
    
    # Apply filters
    df = apply_filters(df)
    
    # Show analytics
    show_summary_metrics(df)
    show_analytics(df)
```

**Responsibilities:**
- UI flow orchestration
- File upload handling
- Calls functions from specialized modules

---

### **`data_loader.py` — Smart Data Ingestion**
```python
@st.cache_data  # Caches loaded data for performance
def load_ledger(file_path):
    # Load all sheets
    df = pd.read_excel(file_path, sheet_name=None)
    
    for sheet_name, data in df.items():
        # Normalize column names (remove newlines, extra spaces)
        data.columns = data.columns.str.replace('\n', ' ').str.strip()
        
        # Convert dates intelligently
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
        
        # Parse amounts as numeric
        data['Amount inc GST'] = pd.to_numeric(data['Amount inc GST'], errors='coerce')
        
        # Standardize contractor names (title case)
        data['Contractor'] = data['Contractor'].str.title()
    
    return df
```

**Key features:**
- **Multi-sheet parsing** (each building = separate sheet)
- **Data normalization** (consistent formatting)
- **Type conversion** (dates, amounts)
- **Caching** (load once, use everywhere)

---

### **`filters.py` �� Real-Time Interactions**
```python
def apply_filters(df):
    # Year filter (multi-select)
    years = st.sidebar.multiselect("Year(s):", sorted(df['Year'].unique()))
    if years:
        df = df[df['Year'].isin(years)]
    
    # Contractor filter
    contractors = st.sidebar.multiselect("Contractor(s):", sorted(df['Contractor'].unique()))
    if contractors:
        df = df[df['Contractor'].isin(contractors)]
    
    # Amount range slider
    min_amt, max_amt = float(df['Amount inc GST'].min()), float(df['Amount inc GST'].max())
    amount_range = st.sidebar.slider("Amount Range:", min_amt, max_amt, (min_amt, max_amt))
    df = df[(df['Amount inc GST'] >= amount_range[0]) & (df['Amount inc GST'] <= amount_range[1])]
    
    return df
```

**Design decision:**  
**No "Apply" button** — filters update instantly as users interact (Streamlit's reactive model)

---

### **`analytics.py` — Visualizations**
```python
def show_summary_metrics(df):
    """4-card KPI dashboard"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Total Amount", f"${df['Amount inc GST'].sum():,.2f}")
    with col3:
        st.metric("Contractors", df['Contractor'].nunique())
    with col4:
        st.metric("Services", df['Service'].nunique())

def show_contractor_spending(df):
    """Bar chart + heatmap table"""
    contractor_spending = df.groupby('Contractor')['Amount inc GST'].sum().sort_values(ascending=False)
    
    # Bar chart
    st.bar_chart(contractor_spending)
    
    # Heatmap table (red = high spend, green = low)
    styled_df = contractor_df.style.format({'Total Spent': '${:,.2f}'}).background_gradient(
        subset=['Total Spent'],
        cmap='RdYlGn_r'  # Red → Yellow → Green
    )
    st.dataframe(styled_df)

def show_spending_over_time(df):
    """Monthly timeline chart"""
    monthly = df.set_index('Date').resample('ME')['Amount inc GST'].sum()
    st.line_chart(monthly)
```

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
- 15 minutes

**New way:**  
- Select "All buildings"
- Filter contractor: "ABC Plumbing"
- Filter year: "2024"
- **Answer in 30 seconds**

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
| **Live Demo** | Coming soon (Streamlit Cloud) |
| **Excel Template (fake data)** | Coming soon (test drive the dashboard) |

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

## 🚀 Closing Thought

What started as *"let's make Excel less painful"* became a concrete example of **applied software engineering in the real world**.

**No buzzwords.**  
**No hype.**  
**Just code that makes work lighter.**

Once you see an invoice ledger as a dataset —  
you never see Excel the same way again.

---

## 💬 Let's Connect!

Building Invoice Ledger Analytics was a perfect example of **turning operational friction into engineering opportunity**. If you're:

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
| Python, Streamlit, Pandas, openpyxl | PostgreSQL/Supabase, ML (Prophet), Building System APIs, React Native/PWA |

---

*Built with ☕ and firsthand building management experience*  
*"The best code is the code that quietly removes friction from people's work."*
