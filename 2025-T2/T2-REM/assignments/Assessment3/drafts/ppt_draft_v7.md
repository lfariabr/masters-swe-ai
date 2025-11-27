# Slide flow Suggestion from Dr. Bushra

1. Title
2. Problem Context
3. Gap
4. Questions
5. Methods
6. Expected Outcomes
7. Significance
8. Timeline
9. Conclusion

# My current structure
## Needs adjustment to fit in requirements from above!

1. Title
Exploring the relationship between 
Net Promoter Score and Revenue Growth 
in Healthcare Clinics

RESEARCH PROPOSAL | ASSESSMENT 3
RESEARCH METHODOLOGIES
Prof Dr. BUSHRA NAEEM
LUIS G. B. A. FARIA – ID A00187785

2. PROBLEM CONTEXT

• NPS adopted by 67% of Fortune 1000 (Reichheld, 2003)
• Healthcare clinics rely on NPS for patient loyalty tracking
• BUT: Zero empirical studies linking NPS → Revenue in healthcare

Research Questions:
• RQ1: To what extent is NPS correlated with monthly revenue growth?
• RQ2: Can NPS trends predict short-term revenue fluctuations?

Hypotheses:
• H0: No significant correlation between NPS and revenue
• H1: Positive correlation exists (r > 0.3, p < 0.05)

[Visual: NPS gauge with "$?" question mark]

3. POSITIONING IN THE FIELD

Literature Landscape:
┌─────────────────────────────────────────────────────┐
│ Patient Experience → Loyalty        │ ✓ Established │
│ (Godovykh & Pizam, 2023)            │               │
├─────────────────────────────────────────────────────┤
│ NPS → Intention to recommend        │ ✓ Validated  │
│ (Reichheld, 2003; Dawes, 2024)      │               │
├─────────────────────────────────────────────────────┤
│ AI Sentiment Analysis (technical)   │ ✓ Feasible    │
│ (Alkhnbashi et al., 2024)           │               │
├─────────────────────────────────────────────────────┤
│ NPS → Revenue in HEALTHCARE         │ ✗ MISSING     │
│ **This Study fills this gap**       │               │
└─────────────────────────────────────────────────────┘

Key Gap: Assumed correlation never tested empirically

[Visual: Table 1 from draft_v8 - Literature Synthesis]

4. KNOWLEDGE GAP & CONCEPTUAL MODEL

Assumed Pathway (Never Validated):

Patient       NPS         Loyalty        Revenue
Experience  → Score   →  Intent    →?→  Growth
   ✓            ✓          ✓          ?
                    ↑
              BROKEN LINK

Three Converging Gaps:
1. Metric Validation: NPS guides decisions without financial proof
2. Business Intelligence: Sentiment analysis lacks outcome validation
3. ICT Foundation: AI systems built on unverified assumptions

Contribution: Empirical validation of 27,000 records over 36 months

[Visual: Figure 2 - Conceptual Framework from draft_v8]

5. PROPOSED METHODOLOGY

Quantitative Correlational Design (Pragmatic-Positivist)

Research Pipeline:
┌──────────────────────────────────────────────┐
│ 1. Data Import (27K records, 2022-2025)     │
│ 2. Cleaning (Pandas + NumPy)                │
│ 3. Aggregation (by clinic-month)            │
│ 4. Correlation (Pearson + Spearman)         │
│ 5. Regression (lagged variables)            │
│ 6. Clustering (K-means clinic profiles)     │
│ 7. Visualization (Streamlit dashboard)      │
└──────────────────────────────────────────────┘

Triangulation: Temporal + Spatial + Methodological

[Visual: Figure 4 - Data Analytics Workflow]

6. METHODS & TOOLS

Analytical Workflow:
• Descriptive Statistics (mean, SD, distribution)
• Pearson/Spearman Correlation (strength + direction)
• Linear Regression (predictive capacity with lags)
• K-means Clustering (clinic behavioral segmentation)

Code Example:
```python
# Correlation Analysis
correlation = df[['nps', 'revenue']].corr()

# Predictive Regression Model
X_lagged = df[['nps_t1', 'nps_t2']]  # Lagged variables
model = LinearRegression().fit(X_lagged, y_revenue)
```

Ethics & Governance:
✓ Anonymized data (clinic-month aggregation)
✓ Institutional consent (Pro-Corpo Estética)
✓ LGPD + GDPR + Australian Privacy Act compliant
✓ Researcher reflexivity statement (former collaborator)

[Visual: Figure 3 - NPS Survey Instrument]

7. EXPECTED CONTRIBUTIONS & OUTCOMES

Three Possible Results:

┌─────────────────────────────────────────────────┐
│ Strong (r > 0.7, p < 0.05)                      │
│ → Validate NPS as strategic KPI                 │
│ → Simple tracking systems sufficient            │
│ → Cost-effective patient monitoring             │
├─────────────────────────────────────────────────┤
│ Moderate (0.3 < r < 0.7, p < 0.05)              │
│ → Partial validation - NPS provides some signal │
│ → Justify AI sentiment enhancement investment   │
│ → Richer feedback dimensions needed             │
├─────────────────────────────────────────────────┤
│ Weak (r < 0.3 or p > 0.05)                      │
│ → Challenge NPS validity in healthcare          │
│ → Redirect to NLP-based alternatives            │
│ → Capture nuanced emotional/experiential data   │
└─────────────────────────────────────────────────┘

Regardless of outcome:
→ Evidence-based decision framework
→ Quantitative foundation for AI/NLP research
→ Replicable ICT R&D methodology

[Visual: Decision tree diagram with three branches]

8. SIGNIFICANCE & IMPACT

For Healthcare Managers:
• Validate or challenge NPS as financial KPI
• Data-driven patient experience investment decisions
• Cost-benefit analysis: Simple NPS vs. AI complexity

For Academic Research:
• First empirical NPS-revenue study in healthcare context
• Quantitative foundation for AI sentiment analytics
• ICT R&D methodology for business intelligence

For Torrens "Here for Good" Ethos:
• Sustainable healthcare through evidence-based decisions
• Patient-centered care aligned with financial viability
• Responsible innovation in healthcare technology

Broader Impact:
• Replicable framework for service industries
• Bridge between patient experience and business outcomes
• Foundation for future mixed-methods research

[Visual: Three icons - Manager briefcase, Research beaker, University crest]

9. TIMELINE & MILESTONES

═══════════════════════════════════════════════════════════
PHASE 1: RESEARCH PROPOSAL (Week 1-12) - Assessment 3
═══════════════════════════════════════════════════════════

Week  Phase/Task                              Deliverable
───────────────────────────────────────────────────────────
1-2   Literature Refinement                   Lit review draft
      • Consolidate Assessment 1 findings
      • Add 3-5 recent studies (2024-2025)
      • Finalize research gap statement
      
3-4   Ethics & Data Acquisition               Ethics clearance
      • Obtain Pro-Corpo consent letter
      • Verify anonymization protocols
      • Set up encrypted storage
      
5-6   Data Cleaning & Preparation             Clean dataset
      • Remove duplicates, handle missing values
      • Aggregate by clinic-month
      • Create lagged variables (t-1, t-2)
      
7-8   Descriptive & Correlation Analysis      Correlation matrix
      • Run Pearson/Spearman tests
      • Generate scatterplots & heatmaps
      • Check temporal patterns
      
9-10  Regression Modeling & Validation        Regression model
      • Build linear regression with lags
      • K-means clustering analysis
      • Cross-validate by clinic/year
      
11    Results Interpretation & Draft          Draft chapters
      • Integrate findings with theory
      • Create visualizations (Figures 5-8)
      • Write methodology & results sections
      
12    Final Report & Presentation Prep        Final submission
      • Apply feedback, edit structure
      • Finalize APA 7th references
      • Design slides, rehearse presentation
      • Submit Assessment 3 (Due: Dec 3, 2025)

═══════════════════════════════════════════════════════════
PHASE 2: ANALYSIS DEEPENING (Week 13-20) - Post-Assessment
═══════════════════════════════════════════════════════════

13-14 Extended Statistical Analysis            Robustness tests
      • Sensitivity analysis (exclude outliers)
      • Time-series decomposition (trend/seasonality)
      • Granger causality tests (if temporal)
      
15-16 Qualitative Validation (Optional)       Theme analysis
      • Code 500 text comments (NPS Question 2)
      • Identify emotion categories (anger/relief)
      • Map themes to correlation strength
      
17-18 Dashboard Prototype Development          Working prototype
      • Build Streamlit NPS-Revenue dashboard
      • Implement real-time correlation tracking
      • Add predictive alerts (revenue dips)
      
19-20 Comparative Industry Analysis            Benchmarking
      • Compare healthcare vs. retail NPS-revenue
      • Literature synthesis across sectors
      • Position findings in broader context

═══════════════════════════════════════════════════════════
PHASE 3: PUBLICATION PATHWAY (Week 21-40) - Dissemination
═══════════════════════════════════════════════════════════

21-24 Journal Article Preparation              Draft manuscript
      Target: International Journal of Market Research
             or Journal of Healthcare Management
      • Expand methodology (3000-4000 words)
      • Add cluster analysis visualizations
      • Discussion of managerial implications
      
25-26 Internal Review & Co-author Feedback     Revised draft
      • Share with Dr. Bushra Naeem (supervisor)
      • Incorporate academic feedback
      • Strengthen theoretical contribution
      
27-28 Submission & Peer Review (Round 1)       Journal submission
      • Submit to target journal
      • Respond to reviewer comments
      • Revise methodology if requested
      
29-32 Conference Presentation Prep             Conference paper
      Target: Australian Conference on Information Systems
             or Healthcare Management Conference
      • Create 15-min presentation
      • Poster design (if applicable)
      • Abstract submission (500 words)
      
33-36 Revised Manuscript & Resubmission        Final submission
      • Address all peer review comments
      • Add supplementary materials
      • Proofread and format per journal guidelines
      
37-40 Acceptance & Publication Process         Published article
      • Copyediting and galley proofs
      • Open access deposit (if required)
      • Promote via LinkedIn, ResearchGate

═══════════════════════════════════════════════════════════
GANTT CHART VISUALIZATION
═══════════════════════════════════════════════════════════

Week:   2  4  6  8  10 12 14 16 18 20 24 28 32 36 40
────────────────────────────────────────────────────────
Phase 1  ████████████ Assessment 3
Lit Rev  ██
Ethics     ██
Data Prep    ████
Analysis        ████
Regression          ████
Writing                 ████
                          ↓
Phase 2                  ████████ Post-Assessment
Deepening                ████
Qual Valid                  ████
Prototype                      ████
                                  ↓
Phase 3                          ████████████████ Publish
Journal Draft                    ████
Review                               ████
Conference                               ████
Revision                                     ████
Publication                                      ████

═══════════════════════════════════════════════════════════
KEY MILESTONES & DEPENDENCIES
═══════════════════════════════════════════════════════════

✓ Week 4:  Ethics clearance (blocks data analysis)
✓ Week 6:  Clean dataset ready (enables correlation)
✓ Week 10: Statistical results (informs interpretation)
✓ Week 12: Assessment 3 submission ← CRITICAL DEADLINE
✓ Week 18: Dashboard prototype (demonstrates ICT value)
✓ Week 24: Journal draft complete (begins publication)
✓ Week 32: Conference presentation (validates findings)
✓ Week 40: Published article (career milestone)

Total Duration: 10 months (Assessment → Publication)

10. REFERENCES

Key Citations (APA 7th):

Cahya, V. N. C., Setyanto, R., & Paradise, P. (2025). Analysis of 
  loyalty membership programs. Eduvest Journal, 5(9), 10974-10983.

Dawes, J. G. (2024). The net promoter score: What should managers 
  know? International Journal of Market Research, 66(2–3), 182–198.

Godovykh, M., & Pizam, A. (2023). Measuring patient experience in 
  healthcare. International Journal of Hospitality Management, 112.

Alkhnbashi, O. S., Mohammad, R., & Hammoudeh, M. (2024). Aspect-
  based sentiment analysis of patient feedback. Big Data and 
  Cognitive Computing, 8(12).

Shankar, R., & Yip, A. (2024). Transforming patient feedback into
  actionable insights through NLP. JMIR Formative Research.

Wohlin, C., & Runeson, P. (2021). Guiding the selection of research 
  methodology. Information and Software Technology, 140, 106678.

[Full reference list: 12 sources total]
[Display only - no narration needed]