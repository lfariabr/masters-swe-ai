# IEEE Software Requirements Specification Template

Copyright © 1999 by Karl E. Wiegers. Permission is granted to use, modify, and distribute this document.

Note that the original template was revised to fit this course (SEP401).

---

# Software Requirements Specification

for

**ClinicTrends AI Project**

Group: 1

Students:
- Luis Guilherme de Barros Andrade Faria - A00187785
- Jing Feng Chin - A00178098
- Luong Hai Chau - A00117495

Subject Code: SEP 401

Subject Name: Software Engineering Principles

Assessment No.: 2

Title of Assessment: Proposal

Lecturer: Dr. Ranju Mandal

Date: June 2025

---

## Table of Contents

- Table of Contents
- Revision History
- 1. Introduction
  - 1.1 Purpose
  - 1.2 Product Scope
- 2. Overall Description
  - 2.1 Product Perspective
  - 2.2 Product Functions
  - 2.3 Stakeholders
  - 2.4 Operating Environment
  - 2.5 Design and Implementation Constraints
  - 2.6 Assumptions and Dependencies
- 3. External Interface Requirements
  - 3.1 User Interfaces
  - 3.2 Software Interfaces
  - 3.3 Communications Interfaces
- 4. System Features
  - 4.1 Upload Survey Data
  - 4.2 Visualize Historical Trends
  - 4.3 Predict Sentiment Trends
  - 4.4 Alert system
  - 4.5 Export Report
- 5. Other Nonfunctional Requirements
  - 5.1 Performance Requirements
  - 5.2 Security Requirements
  - 5.3 Software Quality Attributes
  - 5.4 Business Rules
- 6. References
- 7. Other Requirements
- Appendix A: Glossary
- Appendix B: Analysis Models

---

## Revision History

| Name | Date | Reason For Changes | Version |
|------|------|---------------------|---------|
|      |      |                     |         |

*(Table is blank in original PDF)*

---

## 1. Introduction

### 1.1 Purpose

ClinicTrendsAI is a software system developed to help aesthetic clinics analyze and forecast customer satisfaction trends based on historical survey data, such as Net Promoter Score (NPS) feedback. The platform applies machine learning techniques to generate predictive insights, detect early signs of declining satisfaction, and highlight key factors influencing customer sentiment. By transforming raw survey data into actionable intelligence, ClinicTrendsAI enables clinic managers to make informed, proactive decisions aimed at improving service quality, enhancing client retention, and sustaining long-term business performance.

### 1.2 Product Scope

ClinicTrendsAI will provide the following core capabilities:
- Ingest survey datasets in CSV and JSON formats for flexible data integration.
- Predict future customer satisfaction scores using machine learning regression models to anticipate emerging trends.
- Visualize satisfaction trends and alert thresholds through interactive graphs and automated flagging of concerning patterns.
- Identify key drivers of satisfaction fluctuations, using feature importance analysis for actionable insights.
- Generate exportable reports to support clinical decision-making and operational improvements.

---

## 2. Overall Description

### 2.1 Product Perspective

ClinicTrendsAI is a self-contained software product developed as a standalone application to support aesthetic clinics in proactively managing customer satisfaction. It is not part of a larger existing product family nor a replacement for any legacy system. Instead, it addresses a current gap in affordable, intelligent feedback analysis tools tailored to the needs of small and medium-sized clinics.

The application is designed to function independently, requiring only local survey data inputs, including CSV or JSON files. Built using Python and Streamlit, ClinicTrendsAI provides an intuitive interface suitable for non-technical users. It encompasses a lightweight deployment model that ensures accessibility via local or cloud-hosted environments. This product serves as the first iteration in a potential roadmap of intelligent customer insight tools designed for the healthcare and wellness service sector.

---

### 2.2 Product Functions

ClinicTrendsAI provides a set of key functions designed to enable clinic managers to analyze, monitor, and act on customer satisfaction data. The system's functionality is organized into the following core features:
- User Access Control: Restrict access to sensitive reports or data
- Clean & Preprocess Data: Automatically handle missing values, inconsistent formats, and invalid data entries
- Upload historical survey data: Allow users to upload customer satisfaction dataset in .csv format
- Visualize Historical Trends: Display satisfaction scores using interactive charts
- Predict Sentiment Trends: Applied machine learning to forecast future satisfaction levels
- Alert System: Automatically flags predicted satisfaction drops below a critical threshold
- Export Report: Allow users to export key analysis outputs and insights

---

### 2.3 Stakeholders

- **Clinic Manager**:
  - Role: Primary end user responsible for business operations and customer experiences
  - Expectations: Expect clear insights into satisfaction trends, risks, and improvement opportunities

- **Operation Analyst**:
  - Role: Analyst or data specialist reviewing performance metrics across stores
  - Expectations: Require access to raw data, trends, and feature insights to inform strategic actions.

- **Developer**:
  - Role: Responsible for Streamlit UI and features analysis
  - Expectations: Need clear UI requirements, data formats, and interaction logic

- **Machine Learning Engineer**:
  - Role: Implement prediction models and feature analysis
  - Expectations: Require clean datasets, evaluation criteria, and feedback on model performance

- **System Admin**:
  - Role: Maintain the application
  - Expectations: Require the design documentation in the details

---

### 2.4 Operating Environment

- Web browser (Chrome, Firefox)
- Backend hosted locally or on cloud VM
- Python 3.10+, Streamlit, pandas

---

### 2.5 Design and Implementation Constraints

- Technology Stack Constraint:
  - The system is developed using Python and Streamlit
- Must handle CSVs up to 200MB
- Predictions limited to linear regression and decision tree models in MVP
- Model retraining must occur asynchronously

---

### 2.6 Assumptions and Dependencies

- Survey datasets are clean or preprocessed
- Backend runs with access to Python ML environment

---

## 3. External Interface Requirements

### 3.1 User Interfaces

Streamlit dashboard with upload button, chart views, prediction box, and alerts panel.

---

### 3.2 Software Interfaces

- Python packages: pandas, matplotlib, streamlit, plotly, altair

---

### 3.3 Communications Interfaces

- Localhost or HTTP (future cloud deployment may require HTTPS)

---

## 4. System Features

### 4.1 Upload Survey Data

#### Description and Priority

Allow users to upload CSV datasets containing historical customer feedback. The priority is set as high, since this is the entry point for all analysis.

#### Stimulus/Response Sequences

- User selects file
- System validates format
- If OK, data loads into session

#### Functional Requirements

- REQ-1: System shall support .csv format
- REQ-2: System shall validate file size and structure (columns: Date, Store, Score, Comment)

---

### 4.2 Visualize Historical Trends

#### Description and Priority

Displays satisfaction trends over time, segmented by store or customer group. Priority set as High.

#### Stimulus/Response Sequences

- User selects file
- Trends appear in interactive charts
- Users can filter by store/period

#### Functional Requirements

- REQ-3: System shall generate Altair charts with NPS over time
- REQ-4: System shall provide dropdown filters for store/location

---

### 4.3 Predict Sentiment Trends

#### Description and Priority

Applies Machine Learning model to analyze comments and score data and provide Sentiment Analysis

#### Stimulus/Response Sequences

- User clicks “Analyze Sentiment” button
- System preprocesses data
- Model returns sentiment analysis + scores + confidence intervals

#### Functional Requirements

- REQ-5: System shall use a scikit-learn (e.g. Linear Regression) model to predict satisfaction
- REQ-6: System shall output predictions with a 95% confidence interval

---

### 4.4 Alert system

#### Description and Priority

Flag risks where satisfaction is predicted to drop below a defined threshold (e.g. 50). Priority is set to medium.

#### Stimulus/Response Sequences

- Model detects drop
- UI shows red warning icon or alert message

#### Functional Requirements

- REQ-7: System shall flag predictions below 50.
- REQ-8: System shall display top features influencing the drop.

---

### 4.5 Export Report

#### Description and Priority

Allows User to download analysis results and predictions as PDF or CSV.

#### Stimulus/Response Sequences

- User clicks “Export Report”
- System generates file
- File downloads locally

#### Functional Requirements

- REQ-9: System shall generate a .pdf or .csv summary
- REQ-10: Report shall include timestamp, store, predicted score, NPS trend chart.

---

## 5. Other Nonfunctional Requirements

### 5.1 Performance Requirements

- The system shall return predictions within 10 seconds of data upload.

---

### 5.2 Security Requirements

<Specify any requirements regarding security or privacy issues surrounding use of the product or protection of the data used or created by the product. Define any user identity authentication requirements. Refer to any external policies or regulations containing security issues that affect the product. Define any security or privacy certifications that must be satisfied.>

*(Note: This section is blank/placeholder in the PDF.)*

---

### 5.3 Software Quality Attributes

<Specify any additional quality characteristics for the product that will be important to either the customers or the developers. Some to consider are: adaptability, availability, correctness, flexibility, interoperability, maintainability, portability, reliability, reusability, robustness, testability, and usability. Write these to be specific, quantitative, and verifiable when possible. At the least, clarify the relative preferences for various attributes, such as ease of use over ease of learning.>

- The UI shall be intuitive for non-technical users.

*(Note: Mostly a placeholder, only one real line is filled in.)*

---

### 5.4 Business Rules

- The system shall handle incomplete rows gracefully.

---

## 6. References

*(No references are explicitly listed on the page. Possibly blank.)*

---

## Appendix A: Glossary

- **NPS**: Net Promoter Score
- **ML**: Machine Learning
- **MVP**: Minimum Viable Product

---

## Appendix B: Analysis Models

- Use Case Diagram: *(blank placeholder in PDF)*

- Activity Diagram: *(blank placeholder in PDF)*

- Data Modelling Concepts

- Class-Based Modelling: *(to-do)*

- Sequence Diagram: *(to-do)*

- Use pertinent models:
  - Use cases
  - Class Diagrams
  - Data Flow Diagram
  - Control Flow Diagram (for real-time applications)
  - State Diagram
  - Sequence Diagram