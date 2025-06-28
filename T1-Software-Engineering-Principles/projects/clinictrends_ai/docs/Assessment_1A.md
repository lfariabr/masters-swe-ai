# Software Proposal

## ClinicTrends AI Project

Group: 1

Students:
- Luis Guilherme de Barros Andrade Faria - A00187785
- Jing Feng Chin - A00178098
- Luong Hai Chau - A00117495

Subject Code: SEP 401

Subject Name: Software Engineering Principles

Assessment No.: 1

Title of Assessment: Proposal

Lecturer: Dr. Ranju Mandal

Date: June 2025

---

## Table of Contents

- Introduction
- Similar Work
- Proposal
- Business Values
- Project Plan
- Deliverables
- Risk Assessment
- Key Phases
- Gantt Chart
- Evaluation
- References

---

## Introduction

In the dynamic and highly competitive landscape of local businesses, maintaining high levels of customer satisfaction is essential for client retention and business sustainability. However, satisfaction is typically measured reactively through tools such as the Net Promoter Score (NPS), offering limited insights for timely decision-making. Most businesses lack the analytical infrastructure to interpret this data proactively. ClinicTrendsAI seeks to address this gap by providing an intelligent, machine learning-powered dashboard that visualizes satisfaction trends and forecasts potential downturns, enabling pre-emptive action and strategic improvement. This project draws on prior professional experience managing large-scale clinical operations and leverages it within a software engineering context. With access to a robust dataset comprising over 25,000 (twenty-five thousand) customer NPS records, the project offers an ideal foundation for applying predictive techniques such as regression and classification models. Coupled with interactive visualizations, the solution is designed to support managers and business owners in making data-driven, forward-looking decisions.

This project is significant because it introduces automation, predictive analytics, and model explainability into an area traditionally dominated by manual reporting. By integrating advanced data science techniques within a lightweight software framework, Clinic Trends AI transforms satisfaction tracking from a reactive process into a proactive business strategy.

---

## Similar Work

Several enterprise-level platforms currently offer tools for customer satisfaction analysis. Industry leaders such as Medallia (Medallia, n.d.) and Qualtrics (Qualtrics, n.d.) provide comprehensive experience management solutions that include survey distribution, data aggregation, and trend analysis. However, these platforms typically come with significant subscription costs and are primarily designed for large organizations, making them inaccessible for small to medium-sized business, such as aesthetic clinics. Alternatively, tools like SurveyMonkey (SurveyMonkey, n.d.) enable clinics to collect feedback and display results through static dashboards and email summaries. While useful for capturing customer sentiment, such tools lack predictive capabilities and offer limited insight into the drivers behind satisfaction scores.

Academic literature also supports the need for more actionable insights in this domain. For example, Ahmad et al. (2013) identify key software maintainability and satisfaction indicators, which can inform the feature selection process for machine learning models aimed at forecasting customer behaviour.

ClinicTrendsAI differentiates itself in several critical ways:
- It offers a lightweight, open-source MVP, lowering barriers to adoption for resource-constrained clinics.
- It provides tailored predictions for NPS trends, enabling early detection of declining satisfaction levels.
- It incorporates feature importance analysis, allowing managers to understand which factors most significantly impact satisfaction and prioritize improvements accordingly.

Additionally, the need for well-structured software development practices in such initiatives is supported by established research. Ewusi-Mensah (2003) underscores how poor planning and fluctuating requirements frequently contribute to software project failures. Similarly, Stephens (2015) emphasizes the importance of following disciplined engineering methodologies to build reliable, maintainable systems. Moreover, the project draws on Agile project management principles, as outlined by Cobb (2015), to ensure iterative feedback integration and responsiveness to emerging user needs, an approach particularly well-suited for systems involving real-world data and evolving business requirements.

---

## Proposal

ClinicTrendsAI is a Python-based software solution powered by machine learning that enables proactive customer satisfaction management. Built using Streamlit, the application will load survey data from CSV files and produce visual analytics, predictive forecasts, and feature analysis to guide managerial decisions. The core features of the application include:
- Historical visualizations of NPS over time, by clinic location or staff group;
- Machine learning predictions for future NPS;
- Alerts for negative trend thresholds;
- Feature impact analysis to understand drivers of satisfaction.

Each component of the dashboard is designed to support key user personas:
- Business Owners and Managers who need a quick snapshot of satisfaction metrics and alerts;
- Regional Directors who compare performance across locations;
- Operations Analysts who require interpretable machine learning outputs to identify actionable areas for improvement.

---

## Business Values

Clinic Trends AI provides significant value to small and medium-sized businesses by:
- **Cost-Effectiveness**: Offering an open-source solution, reducing reliance on expensive subscription-based platforms.
- **Proactive Decision-Making**: Enabling managers to anticipate and address satisfaction issues before they escalate, reducing churn.
- **Scalability**: Supporting clinics of varying sizes with a lightweight, cloud-compatible application.
- **Operational Efficiency**: Automating data analysis and providing clear, actionable insights, saving time and resources.

This solution aligns with industry needs for affordable, data-driven tools and demonstrates the application of machine learning in software engineering, enhancing the team’s technical expertise. From a broader software engineering perspective, this project applies ML in a practical domain with measurable outcomes, demonstrating the potential of applied AI in enhancing customer experience.

---

## Project Plan

The proposed project will be implemented over 12 weeks using a Scrum-based Agile methodology (Heath, F. 2021). The development is divided into six sprints, each lasting two weeks. This approach supports iterative improvement, rapid feedback incorporation, and adaptability to evolving requirements from stakeholders and data insights.

---

## Deliverables

The final outputs of the ClinicTrendsAI project will include the following:
- **MVP Dashboard**:
  - A fully functional, interactive dashboard built using Streamlit and Python, allowing users to upload survey data, visualize satisfaction trends, and receive predictive insights.
- **Machine Learning module for satisfaction forecast**:
  - A predictive engine capable of forecasting future NPS values.
- **Alert system based on NPS thresholds**:
  - An automated threshold-based alert mechanism that notifies users of potential declines in predicted customer satisfaction.
- Documentation and demo video.

---

## Risk Assessment

Every software development project faces uncertainties that can affect scope, quality, timeline or even user satisfaction. Identifying and mitigating risks early is key for delivering a stable and valuable solution. In the context of ClinicTrendsAI, potential risks range from data-related issues (such as incomplete or inconsistent survey inputs) to technical challenges in machine learning model performance and stakeholder management.

This section outlines the most significant risks identified during project planning, their likelihood, potential impact and strategies that we propose to mitigate them.

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Data quality issues (incomplete/messy CSVs) | High | Medium | Implement data validation and cleaning during preprocessing and providing sample .csv for users as example. |
| Model underfitting/overfitting | Medium | Medium | Use cross-validation and holdout test set |
| Lack of stakeholder availability for feedback | Medium | High | Schedule early demos and async feedback sessions. |
| Scope creep | Medium | Medium | Maintain sprint backlog and enforce scope boundaries. |

---

## Key Phases

**Sprint 1: Project Initiation & Requirements Discovery**
- Define project scope, objectives, and success criteria
- Identify stakeholders and collect initial user stories
- Conduct risk assessment and map satisfaction-related KPIs
- Review and profile historical survey dataset (structure, quality, completeness)

**Sprint 2: Dataset Preparation & Feature Engineering**
- Clean and transform survey data using pandas
- Define NPS calculation logic and satisfaction metrics
- Explore initial data distributions and segmentations
- Create candidate features for modelling (e.g., visit frequency, feedback score, time delays)

**Sprint 3: Model Design & UI Mockups**
- Select machine learning models
- Design evaluation strategy
- Develop low-fidelity UI mockups
- Set up Streamlit framework and define UI layout structure

**Sprint 4: Development & Model Integration**
- Implement data visualization modules in Streamlit
- Train and test ML models on NPS prediction
- Integrate feature importance metrics for explainability
- Implement alert system based on predicted NPS thresholds

**Sprint 5: Testing, Evaluation & UX Refinement**
- Conduct usability testing with mock users or stakeholders
- Validate prediction outputs against holdout test set
- Apply iterative feedback to improve UI, navigation, and outputs
- Ensure system responsiveness for non-technical users

**Sprint 6: Final Delivery & Stakeholder Demo**
- Prepare final documentation, user guide, and deployment script
- Record walkthrough demo video of dashboard functionalities
- Present findings and demo to facilitator and peers
- Final polish and retrospective evaluation of project outcomes

---

## Gantt Chart

*(Note: PDF included a Gantt chart image but no textual table. Text conversion cannot represent that image. You may need to redraw it manually in markdown tables if desired.)*

---

## Evaluation

The project’s success will be evaluated through:
- System responsiveness and interpretability;
- Performance and clarity of prediction model;
- User testing for clarity and utility of dashboard;
- Ability to identify and act on customer churn risks.

---

## References

Ahmad, M. O., Markkula, J., Oivo, M. (2013). Factors affecting software maintainability from customer perspective. Journal of Systems and Software.

Cobb, C. G. (2015). The Project Manager's Guide to Mastering Agile. Wiley.

Ewusi-Mensah, K. (2003). Software Development Failures. MIT Press.

Heath, F. (2021). The Professional Scrum Master Guide. Packt Publishing.

Medallia. (n.d.). The #1 Experience Management Platform. Retrieved June 16, 2025, from https://www.medallia.com/platform

Qualtrics. (n.d.). Qualtrics by use case. Qualtrics. Retrieved June 16, 2025, from https://www.qualtrics.com/use-case/

SurveyMonkey. (n.d.). SurveyMonkey: The world’s most popular survey platform. https://www.surveymonkey.com

Stephens, R. (2015). Beginning Software Engineering. Wrox Press.