
# ClinicTrendsAI – Software Design Specification (SDS)

**Version:** 1.9.0
**Date:** July 14, 2025
**Status:** Final Draft
**Prepared by:** Luis Faria, Jing Feng Chin, Luong Hai Chau
**Subject:** SEP401 - Software Engineering Principles
**Institution:** Torrens University Australia

---

## Document Control

| Version | Date | Author | Change Description |
|---------|------|--------|--------------------|
| 1.0 | June 10, 2025 | L. Faria | Initial draft |
| 1.5 | June 25, 2025 | J. Chin | Added architectural details |
| 1.8 | July 05, 2025 | L. Chau | Added UI design principles |
| 1.9 | July 14, 2025 | L. Faria | Final revisions and integration |

---

## Table of Contents

1. [Introduction](#1-introduction)
   1. [Purpose of this Document](#11-purpose-of-this-document)
   2. [Scope of the Development Project](#12-scope-of-the-development-project)
   3. [System Overview](#13-system-overview)
   4. [Definitions, Acronyms, and Abbreviations](#14-definitions-acronyms-and-abbreviations)
   5. [References](#15-references)
2. [Design Considerations](#2-design-considerations)
   1. [Assumptions and Dependencies](#21-assumptions-and-dependencies)
   2. [General Constraints](#22-general-constraints)
   3. [Goals and Guidelines](#23-goals-and-guidelines)
   4. [Development Methods](#24-development-methods)
   5. [Quality Attributes](#25-quality-attributes)
3. [User Interface Design](#3-user-interface-design)
   1. [User Personas](#31-user-personas)
   2. [Scenarios and Use Cases](#32-scenarios-and-use-cases)
   3. [Task Flows](#33-task-flows)
   4. [Swimlane Diagrams](#34-swimlane-diagrams)
   5. [Storyboards](#35-storyboards)
   6. [UI Design Principles](#36-ui-design-principles)
   7. [User Experience Guidelines](#37-user-experience-guidelines)
4. [Architectural Strategies](#4-architectural-strategies)
   1. [Architectural Style](#41-architectural-style)
   2. [Design Patterns](#42-design-patterns)
   3. [Separation of Concerns](#43-separation-of-concerns)
   4. [Trade-offs and Decisions](#44-trade-offs-and-decisions)
5. [System Architecture](#5-system-architecture)
   1. [System Overview Diagram](#51-system-overview-diagram)
   2. [Component Architecture](#52-component-architecture)
   3. [Subsystem Architecture](#53-subsystem-architecture)
   4. [Data Flow Architecture](#54-data-flow-architecture)
   5. [Security Architecture](#55-security-architecture)
6. [Detailed System Design](#6-detailed-system-design)
   1. [Component Specifications](#61-component-specifications)
   2. [Algorithms and Pseudocode](#62-algorithms-and-pseudocode)
   3. [Data Structures](#63-data-structures)
   4. [Interface Specifications](#64-interface-specifications)
   5. [Error Handling](#65-error-handling)
7. [Implementation Plan](#7-implementation-plan)
   1. [Build and Release Procedures](#71-build-and-release-procedures)
   2. [Development Environment](#72-development-environment)
   3. [Testing Strategy](#73-testing-strategy)
   4. [Deployment Considerations](#74-deployment-considerations)
8. [Glossary](#8-glossary)
9. [Bibliography](#9-bibliography)
10. [Appendices](#10-appendices)
    1. [Appendix A: API Documentation](#appendix-a-api-documentation)
    2. [Appendix B: Data Dictionary](#appendix-b-data-dictionary)
    3. [Appendix C: Algorithm Details](#appendix-c-algorithm-details)

---

## 1. Introduction

### 1.1 Purpose of this Document

The purpose of this Software Design Specification (SDS) is to describe the architecture, components, interfaces, and design decisions for the ClinicTrendsAI project. It translates the functional and non-functional requirements from the Software Requirements Specification (SRS) into a detailed implementable design that will guide the development team. This document:

- Defines the system architecture and component-level design
- Specifies interfaces between system components
- Documents design patterns and architectural decisions with justifications
- Provides implementation guidance including algorithms and data structures
- Establishes a common understanding of the design for all stakeholders
- Serves as a reference for development, testing, and maintenance activities

The intended audience includes developers, testers, project managers, and technical stakeholders who need to understand the system design to perform their roles effectively. This SDS will be maintained throughout the development lifecycle and updated as design decisions evolve.

### 1.2 Scope of the Development Project

ClinicTrendsAI is a standalone Python-based web application that enables businesses, especially aesthetic clinics, to analyze and forecast customer satisfaction trends using historical Net Promoter Score (NPS) data and textual feedback. The project scope encompasses:

#### In-Scope Elements

**Core Functionality:**
- CSV data upload, validation, and preprocessing
- Interactive visualizations of NPS trends with filtering capabilities
- Four distinct ML pipelines for predictive modeling of future satisfaction scores
- Multi-model sentiment analysis using NLP techniques (TextBlob, scikit-learn, and Hugging Face Transformers)
- Threshold-based alerts for potential satisfaction drops with confidence intervals
- Export of analysis reports and visualizations in PDF/CSV formats
- Real-time translation features for feedback text and files using deep-translator

**Technical Implementation:**
- Front-end UI development using Streamlit
- Data processing pipeline implementation using pandas
- Machine learning model development using scikit-learn and transformers
- Visualization components using Altair and Plotly
- Deployment configuration for both local and cloud environments

#### Out-of-Scope Elements

- User authentication and role-based access control
- Persistent database integration (planned for future versions)
- Integration with external CRM or feedback collection systems
- Mobile application versions
- Real-time data streaming from external sources
- Automated model retraining and deployment pipeline

### 1.3 System Overview

ClinicTrendsAI transforms raw customer feedback into actionable business insights through a modern, modular architecture. The system follows a microservices-inspired design pattern where distinct components handle specific functional areas while maintaining clear interfaces between them.

**Key Architectural Components:**

- **Frontend Layer**: Streamlit-based web application providing an interactive user interface with navigation, visualizations, and configurable parameters
  - Multi-page navigation system
  - Responsive design adapting to different screen sizes
  - Interactive widgets for data filtering and model selection

- **Data Processing Layer**: Python modules for data ingestion, validation, cleaning, and transformation
  - CSV parser and validator
  - Data preprocessing pipelines
  - Feature engineering components

- **Analytics Layer**: Machine learning and statistical analysis components
  - Multiple ML model implementations (TF-IDF + LogisticRegression, Transformer-based)
  - Feature importance calculator
  - Statistical analysis engines

- **Visualization Layer**: Interactive charting and reporting components
  - Altair-based interactive visualizations
  - Word cloud generators for text analysis
  - Matplotlib/Plotly components for specific chart types

- **NLP Services**: Natural language processing capabilities
  - Hugging Face Transformers integration for sentiment analysis
  - TextBlob for simple sentiment scoring
  - Deep-translator for multilingual support

- **Export Services**: Report and data export functionality
  - PDF report generator
  - CSV data exporter

- **Deployment Options**: Flexible deployment configurations
  - Local execution for development and testing
  - Streamlit Cloud for production deployment

The system emphasizes modularity, scalability, and usability for non-technical business users. It processes CSV files up to 200 MB in size, producing interactive charts, predictive insights, and actionable recommendations while maintaining responsive performance.

**Key System Characteristics:**
- **Stateless operation**: Each user session is independent
- **In-memory processing**: Data is processed in memory without persistent storage
- **Asynchronous capabilities**: Long-running operations executed asynchronously to maintain UI responsiveness
- **Extensible design**: New models and visualizations can be added with minimal core changes

### 1.4 Definitions, Acronyms, and Abbreviations

| Term/Acronym | Definition |
|-------------|------------|
| API | Application Programming Interface |
| CSV | Comma-Separated Values, a file format for tabular data |
| MVP | Minimum Viable Product |
| NLP | Natural Language Processing, a field of AI focused on processing human language |
| NPS | Net Promoter Score, a metric for measuring customer satisfaction and loyalty |
| REST | Representational State Transfer, an architectural style for web services |
| SDS | Software Design Specification |
| SRS | Software Requirements Specification |
| TF-IDF | Term Frequency-Inverse Document Frequency, a numerical statistic for text analysis |
| UI | User Interface |
| UX | User Experience |
| JSON | JavaScript Object Notation, a lightweight data interchange format |
| ML | Machine Learning |

### 1.5 References

1. **ClinicTrendsAI Software Requirements Specification (SRS)**, Group 1, SEP401, June 2025
2. **IEEE Std 1016-2009**, IEEE Standard for Information Technology—Systems Design—Software Design Descriptions
3. **Streamlit Documentation**, https://docs.streamlit.io/ (Accessed: July 2025)
4. **Scikit-learn Documentation**, https://scikit-learn.org/stable/ (Accessed: July 2025)
5. **Hugging Face Transformers Documentation**, https://huggingface.co/docs/transformers/ (Accessed: July 2025)
6. **Deep-translator Documentation**, https://deep-translator.readthedocs.io/ (Accessed: July 2025)
7. **Altair Documentation**, https://altair-viz.github.io/ (Accessed: July 2025)
8. **Medallia Platform Documentation**, https://www.medallia.com/platform/ (Accessed: July 2025)
9. **Software Architecture: Foundations, Theory and Practice**, Taylor, R.N., Medvidović, N. and Dashofy, E., 2009, John Wiley & Sons

## 2. Design Considerations

### 2.1 Assumptions and Dependencies

#### Technical Assumptions

- **Client Environment**:
  - Users have access to modern web browsers (Chrome 90+, Edge 90+, Firefox 88+, Safari 14+)
  - Minimum screen resolution of 1280x720 pixels for optimal experience
  - JavaScript is enabled in the browser

- **Data Structure**:
  - Input CSV files contain mandatory columns: Date, Store/Location, Score (0-100), and Comment text
  - Date formats are standardized (YYYY-MM-DD) or can be automatically parsed
  - CSV file encoding is UTF-8 to support multilingual feedback
  - Maximum file size limit is 200MB

- **Infrastructure**:
  - Internet connectivity is available for API calls to external services (Hugging Face, Deep Translator)
  - Minimum 4GB RAM and 2 CPU cores for local deployment
  - For cloud deployment, Streamlit Cloud resources are sufficient for standard operation

#### Business/User Assumptions

- End users are primarily non-technical clinic managers and business analysts
- Users understand basic NPS principles and satisfaction metrics
- Users have permission to analyze the customer data they upload
- Users are responsible for data privacy compliance and GDPR considerations

#### Dependencies

- **External Libraries and Services**:
  - Streamlit framework (v1.45+) for web interface
  - Pandas (v2.0+) for data manipulation
  - Scikit-learn (v1.5+) for machine learning pipelines
  - Hugging Face Transformers (v4.52+) for NLP services
  - Deep-translator (v1.11+) for multilingual support
  - Altair (v5.2+) and Plotly (v5.20+) for visualization

- **Development Tools**:
  - Git for version control
  - Python 3.9+ development environment
  - Virtual environment for dependency isolation
  - pytest for testing framework

- **Deployment Dependencies**:
  - Machine learning models will be updated periodically but are not retrained during runtime
  - Pre-trained models are shipped with the application or downloaded on first use

### 2.2 General Constraints

#### Technical Constraints

- **Resource Limitations**:
  - Limited to handling CSV files up to 200MB to prevent memory issues
  - Maximum of 100,000 rows per dataset for performance reasons
  - NLP processing limited to first 5,000 characters per comment for transformer models

- **Storage Constraints**:
  - No persistent database storage; data exists only in memory per session
  - Session data is lost when browser is closed or session times out
  - No long-term storage of user uploads or analysis results

- **Performance Constraints**:
  - System must maintain UI responsiveness (<3 seconds for standard operations)
  - ML prediction operations must complete within 10 seconds
  - CSV parsing must handle files at minimum 10MB/second

- **External Dependencies Constraints**:
  - Sentiment analysis depends on third-party APIs, subject to rate limits
  - Translation services may have character limits per request
  - Transformer models may require download time on first use

#### Architectural Constraints

- **Platform Constraints**:
  - Application designed for single-user sessions due to Streamlit's architecture
  - Simultaneous access by multiple users requires separate deployment instances
  - Limited to web browser interface; no native mobile support

- **Security Constraints**:
  - Security is limited to HTTPS transport in production deployments
  - No user authentication implemented in MVP
  - No role-based access control
  - Local file system access is restricted to designated upload functionality

#### Business Constraints

- **Regulatory Constraints**:
  - Application does not store PII but users must ensure uploaded data complies with privacy regulations
  - No built-in data anonymization capabilities in MVP

- **Project Constraints**:
  - Development timeline of 12 weeks with 6 two-week sprints
  - Team size limited to 3 developers
  - Open-source dependencies preferred to reduce licensing costs

### 2.3 Goals and Guidelines

#### Architectural Goals

- **Modular Architecture**: Create a system with well-defined components that can be independently modified, tested, and extended
  - Separate UI components from business logic
  - Design clean interfaces between subsystems
  - Structure code to allow new visualization or model types without major refactoring

- **Scalability**: Design for potential growth in data volume and user base
  - Implement asynchronous processing for resource-intensive operations
  - Design efficient data loading and processing pipelines
  - Create architecture that can be extended to client-server in future versions

- **Maintainability**: Create a system that is easy to understand, debug, and enhance
  - Use consistent design patterns throughout the codebase
  - Implement comprehensive logging and error handling
  - Create clear documentation for all major components

#### Design Guidelines

- **KISS Principle**: Keep the interface minimal and simple for non-technical users
  - Present insights visually with minimal technical jargon
  - Provide clear, action-oriented UI elements
  - Implement progressive disclosure for advanced features

- **Speed vs. Complexity**: Prioritize fast load times and responsiveness
  - Optimize data processing pipelines
  - Use lazy loading for non-critical components
  - Implement caching strategies for expensive calculations
  - Provide feedback during longer operations

- **Explainability**: Make ML outputs transparent and understandable
  - Include feature importance visualizations
  - Provide confidence intervals for predictions
  - Use intuitive visualizations for complex insights
  - Include simple explanations for technical concepts

- **Open-source Stack**: Prefer open-source tools for cost-effectiveness and flexibility
  - Build on well-maintained Python libraries
  - Select components with active communities
  - Avoid dependencies with restrictive licenses

- **Error Prevention & Recovery**: Design to prevent errors and recover gracefully
  - Validate inputs early in the processing pipeline
  - Provide clear error messages with suggested actions
  - Implement fallback strategies for API failures

### 2.4 Development Methods

ClinicTrendsAI adopts an Agile Scrum methodology with six two-week sprints over a 12-week development timeline. This approach enables iterative development with continuous feedback integration and adaptation to changing requirements.

#### Development Process

- **Sprint Planning**: Two-hour sessions at the start of each sprint to identify and prioritize tasks
- **Daily Stand-ups**: 15-minute daily synchronization meetings to track progress and address blockers
- **Sprint Reviews**: Demonstrations of completed features to gather stakeholder feedback
- **Sprint Retrospectives**: Team reflection on process improvements for subsequent sprints
- **Backlog Grooming**: Continuous refinement of requirements and task prioritization

This iterative approach provides several benefits:
- Early prototypes for stakeholder feedback and validation
- Incremental feature development aligned with business priorities
- Regular integration of new components to detect issues early
- Frequent testing and usability checks throughout development
- Ability to adapt to changing requirements and technical challenges

#### Engineering Practices

- **Version Control**: Git with feature branch workflow and pull request reviews
- **Code Quality**: Implementation of linting (flake8), formatting (black), and type hints (mypy)
- **Testing Strategy**:
  - Unit tests with pytest for core components and algorithms
  - Integration tests for component interactions
  - Manual usability testing with representative users

- **Documentation**:
  - Comprehensive docstrings for all classes and functions
  - Architecture documentation with component diagrams
  - User documentation including tooltips and help sections

#### Development Tools and Environment

- **Version Control**: Git with GitHub for repository hosting
- **IDE**: VSCode with Python extensions
- **Package Management**: pip with requirements.txt for dependency tracking
- **UI Framework**: Streamlit for rapid UI development and iteration
- **ML Frameworks**:
  - Scikit-learn for traditional ML pipelines
  - Hugging Face Transformers for NLP tasks
- **Data Processing**: pandas for data manipulation and preprocessing
- **Visualization Libraries**: Altair, Plotly, and Matplotlib
- **Testing Tools**: pytest, pytest-cov for coverage analysis

#### Continuous Integration

- Automated testing on pull requests
- Code quality checks with pre-commit hooks
- Documentation generation from docstrings

### 2.5 Quality Attributes

The following quality attributes define the non-functional characteristics that are critical for ClinicTrendsAI's success. Each attribute includes specific measurable criteria to guide implementation and evaluation.

#### Usability

- **Effectiveness**:
  - Non-technical users shall be able to upload data and generate insights within 5 minutes of first use
  - Task completion rate of >90% for core workflows without assistance
  - Less than 5 user errors per session for typical workflows

- **Learnability**:
  - First-time users shall complete basic analysis tasks without training documentation
  - Tooltips and contextual help shall be available for all non-trivial features
  - Progressive disclosure of advanced features to reduce initial cognitive load

- **User Satisfaction**:
  - Target System Usability Scale (SUS) score >80/100 in user testing
  - Consistent visual design and interaction patterns throughout the application

#### Performance

- **Responsiveness**:
  - UI interactions shall respond within 0.5 seconds
  - Data uploads of typical size (10MB) shall process within 5 seconds
  - Visualizations shall render within 3 seconds for datasets up to 50,000 rows
  - ML predictions shall complete within 10 seconds including feedback

- **Throughput**:
  - System shall handle CSV files up to 200MB within memory constraints
  - System shall process at least 100,000 records for aggregation operations

- **Resource Utilization**:
  - Peak memory usage shall not exceed 2GB for typical operations
  - CPU utilization shall not exceed 70% for more than 30 seconds during normal operation
  - Application should run on standard consumer hardware (i5 equivalent or better)

#### Reliability

- **Availability**:
  - Web application shall have 99.5% uptime during business hours
  - Graceful degradation when external services (like Hugging Face) are unavailable

- **Fault Tolerance**:
  - System shall recover from malformed CSV input without crashing
  - No single point of failure in core functionality
  - System shall preserve unsaved work during minor errors

- **Recoverability**:
  - Automatic retry for transient external API failures
  - Clear error messages with recovery options for users

#### Maintainability

- **Modularity**:
  - Components shall have well-defined interfaces and responsibilities
  - No component should exceed 1000 lines of code
  - Code duplication shall be less than 5%

- **Reusability**:
  - Common functions shall be abstracted into reusable libraries
  - Visualization and data processing components shall be reusable across features

- **Testability**:
  - Unit test coverage shall exceed 80% for core business logic
  - All major workflows shall have integration tests
  - UI components shall be designed for automated testing

- **Analyzability**:
  - Comprehensive logging with appropriate detail levels
  - Clear exception handling with contextual information
  - Performance monitoring points throughout the application

#### Portability

- **Adaptability**:
  - Application shall run on Windows, macOS, and Linux
  - Frontend shall function on Chrome, Firefox, Safari, and Edge browsers
  - Responsive design supporting desktop and tablet viewports

- **Installability**:
  - Complete installation with standard pip package manager
  - All dependencies clearly specified in requirements.txt
  - Maximum installation time of 5 minutes on standard hardware

## 3. User-Interface Design

The user interface for ClinicTrendsAI is designed to balance powerful analytical capabilities with intuitive usability for non-technical business users. This section details the design approach through personas, scenarios, task flows, interaction designs, and guiding principles.

### 3.1 User Personas

The interface design is guided by the needs of these primary user personas:

#### Persona 1: Maria Chen, Clinic Manager

**Demographics & Background:**
- **Age:** 42
- **Education:** MBA
- **Technical Proficiency:** Moderate (comfortable with business software, not with data analysis tools)
- **Role:** Manager of three aesthetic clinic locations with 20+ staff

**Goals:**
- Quickly identify satisfaction trends across locations
- Detect emerging problems before they affect business performance
- Generate insights for team meetings without extensive data preparation
- Track effectiveness of service improvements

**Pain Points:**
- Limited time for manual data analysis
- Overwhelmed by technical jargon and complex analytics interfaces
- Needs to justify business decisions with concrete data
- Struggles to identify actionable insights from raw survey data

**Behaviors & Preferences:**
- Checks satisfaction metrics weekly
- Prefers visual information over tabular data
- Uses tablet devices alongside desktop computer
- Wants to share insights with non-technical stakeholders

#### Persona 2: Alex Owusu, Operations Analyst

**Demographics & Background:**
- **Age:** 29
- **Education:** Bachelor's in Business Analytics
- **Technical Proficiency:** High (experienced with Excel, Power BI, basic Python)
- **Role:** Operations analyst responsible for performance metrics across regional clinics

**Goals:**
- Perform detailed analysis of satisfaction drivers
- Identify correlations between operational changes and customer feedback
- Monitor model accuracy and statistical confidence
- Extract actionable recommendations from data patterns

**Pain Points:**
- Current tools lack predictive capabilities
- Needs more granular data exploration than executives
- Requires validation of analytical methods before trusting results
- Spends excessive time on data preparation and cleaning

**Behaviors & Preferences:**
- Conducts deep-dive analysis sessions
- Comfortable with more technical interfaces and terminology
- Expects data export capabilities for further analysis
- Values statistical rigor and methodology transparency

### 3.2 Scenarios and Use Cases

#### Scenario 1: Routine Satisfaction Monitoring

**User:** Maria Chen (Clinic Manager)

**Narrative:** Maria logs in on Monday morning to check the previous week's customer satisfaction trends. She uploads the latest CSV export from their survey system and wants to quickly identify any concerning patterns across her three clinic locations. She needs to prepare for a 10 AM staff meeting where she'll discuss performance insights.

**Key Requirements:**
- Rapid data upload and processing
- Clear visual presentation of trends by location
- Highlighted alerts for notable changes
- Easy-to-understand summary statistics

#### Scenario 2: Deep Dive Analysis

**User:** Alex Owusu (Operations Analyst)

**Narrative:** The executive team has noticed declining satisfaction scores at one location over the past quarter. Alex is tasked with identifying potential causes and recommending interventions. He needs to analyze sentiment patterns in customer comments, correlate scores with operational changes, and generate evidence-based recommendations.

**Key Requirements:**
- Advanced filtering capabilities
- Detailed sentiment breakdown of comments
- Feature importance visualization
- Access to statistical confidence measures
- Export functionality for further analysis

#### Scenario 3: Multilingual Feedback Analysis

**User:** Maria Chen (Clinic Manager)

**Narrative:** The clinic has a growing international clientele who leave feedback in multiple languages. Maria needs to understand sentiment across all customer segments but doesn't speak all the languages represented in the feedback. She needs to translate and analyze non-English comments.

**Key Requirements:**
- Text translation capabilities
- Sentiment analysis across languages
- Preservation of original text alongside translations
- Aggregated insights across language groups

#### Scenario 4: Performance Reporting

**User:** Alex Owusu (Operations Analyst)

**Narrative:** Alex needs to prepare a monthly executive summary of satisfaction trends and predictions. He must compile key visualizations, statistics, and forecasts into a professional report that can be shared with stakeholders who don't have access to the application.

**Key Requirements:**
- Comprehensive report export functionality
- Customizable report components
- Professional formatting of outputs
- Inclusion of predictive insights with confidence levels

### 3.3 Task Flows

Detailed flows of key user interactions with the system:

#### Task Flow 1: Data Upload and Initial Analysis

1. User navigates to upload page
2. User selects CSV file from local system
3. System validates file format and structure
4. System displays confirmation or error message
5. On success, system processes data and generates initial visualizations
6. System presents dashboard with key metrics and navigation options
7. User selects visualization type or filtering options
8. System updates visualizations based on user selections

#### Task Flow 2: Sentiment Analysis and Prediction

1. User navigates to Models page from dashboard
2. System presents model selection options
3. User selects desired sentiment analysis model
4. System processes feedback text through selected model
5. System displays sentiment breakdown and confidence scores
6. User requests prediction for future periods
7. System calculates predictions with confidence intervals
8. System displays prediction visualization with explanation
9. User adjusts parameters to explore different scenarios
10. System updates predictions based on new parameters

#### Task Flow 3: Report Generation and Export

1. User navigates to Export page
2. System presents report customization options
3. User selects desired charts and metrics for inclusion
4. User configures report parameters (date range, locations)
5. System generates preview of report
6. User reviews and makes adjustments as needed
7. User selects export format (PDF, CSV, etc.)
8. System generates and downloads report file

### 3.4 Swimlane Diagrams

#### Swimlane Diagram 1: Data Upload and Validation Process

```
+----------------+                +----------------+                 +----------------+
|     USER       |                |     SYSTEM     |                 |    DATABASE    |
+----------------+                +----------------+                 +----------------+
        |                                |                                  |
        | Select and Upload CSV          |                                  |
        |------------------------------->|                                  |
        |                                |                                  |
        |                                | Validate File Format             |
        |                                |--------------------------------->|
        |                                |                                  |
        |                                |<---------------------------------|
        |                                | Return Validation Results        |
        |                                |                                  |
        |                                | If Valid:                        |
        |                                | Parse and Process Data           |
        |                                |--------------------------------->|
        |                                |                                  |
        |                                |<---------------------------------|
        |                                | Store in Session Memory          |
        |                                |                                  |
        |<-------------------------------|                                  |
        | Display Success/Error Message  |                                  |
        |                                |                                  |
        | If Success:                    |                                  |
        | Navigate to Dashboard          |                                  |
        |------------------------------->|                                  |
        |                                |                                  |
        |                                | Generate Visualizations          |
        |                                |--------------------------------->|
        |                                |                                  |
        |                                |<---------------------------------|
        |                                | Retrieve Processed Data          |
        |                                |                                  |
        |<-------------------------------|                                  |
        | Display Dashboard with         |                                  |
        | Visualizations                 |                                  |
+----------------+                +----------------+                 +----------------+
```

#### Swimlane Diagram 2: Sentiment Analysis Workflow

```
+----------------+                +----------------+                 +----------------+                 +----------------+
|     USER       |                |   UI LAYER     |                 | ANALYTICS LAYER |                 |   NLP SERVICE  |
+----------------+                +----------------+                 +----------------+                 +----------------+
        |                                |                                  |                                  |
        | Select Analysis Model          |                                  |                                  |
        |------------------------------->|                                  |                                  |
        |                                |                                  |                                  |
        |                                | Request Model Options            |                                  |
        |                                |--------------------------------->|                                  |
        |                                |                                  |                                  |
        |                                |<---------------------------------|                                  |
        |                                | Return Available Models         |                                  |
        |                                |                                  |                                  |
        |<-------------------------------|                                  |                                  |
        | Display Model Options          |                                  |                                  |
        |                                |                                  |                                  |
        | Select Text for Analysis       |                                  |                                  |
        |------------------------------->|                                  |                                  |
        |                                |                                  |                                  |
        |                                | Process Analysis Request         |                                  |
        |                                |--------------------------------->|                                  |
        |                                |                                  |                                  |
        |                                |                                  | If External Model:               |
        |                                |                                  | Send Text to NLP Service         |
        |                                |                                  |--------------------------------->|
        |                                |                                  |                                  |
        |                                |                                  |<---------------------------------|
        |                                |                                  | Return Sentiment Results        |
        |                                |                                  |                                  |
        |                                |                                  | Process Results                 |
        |                                |<---------------------------------|                                  |
        |                                | Return Analysis Results          |                                  |
        |                                |                                  |                                  |
        |<-------------------------------|                                  |                                  |
        | Display Sentiment Analysis     |                                  |                                  |
        | with Visualizations            |                                  |                                  |
+----------------+                +----------------+                 +----------------+                 +----------------+
```

### 3.5 Storyboards

#### Storyboard 1: First-Time User Experience

**Frame 1: Landing Page**
- User arrives at the ClinicTrendsAI landing page
- Clean, professional interface with app logo and tagline
- Clear "Get Started" button prominently displayed
- Brief value proposition visible explaining key benefits
- Navigation menu showing Home, Upload, Dashboard, Models, and Export sections

**Frame 2: Welcome and Introduction**
- Brief tutorial overlay highlighting key features
- Quick explanation of workflow: upload → analyze → export
- Option to skip tutorial or continue
- Sample screenshots showing potential insights

**Frame 3: Data Upload**
- Simple file upload interface with drag-and-drop area
- Clear file requirements displayed (CSV format, required columns)
- Sample template download option
- Upload button and progress indicator

**Frame 4: Validation Results**
- Visual confirmation of successful upload
- Summary of data detected (number of records, date range, locations)
- Preview of first few rows
- Option to proceed to dashboard or correct issues

**Frame 5: Dashboard Overview**
- Main dashboard displays with satisfaction trend line chart
- NPS score breakdown by category (promoters, passives, detractors)
- Location comparison chart
- Date range selector and filtering options
- Navigation tabs for different analysis views

**Frame 6: Interactive Exploration**
- User clicks on trend anomaly in chart
- Drill-down view appears showing details for that time period
- Word cloud of key terms from feedback during period
- Alert indicators for significant changes

**Frame 7: Model Analysis**
- User navigates to Models section
- Model selection interface with brief descriptions
- User selects a model and initiates analysis
- Progress indicator while processing

**Frame 8: Analysis Results**
- Sentiment breakdown visualization
- Feature importance chart showing key drivers
- Prediction chart with confidence intervals
- Explanatory text for non-technical users

**Frame 9: Report Export**
- User navigates to Export section
- Checkboxes for components to include in report
- Format selection (PDF, CSV, PNG)
- Export button and download confirmation

### 3.6 UI Design Principles

ClinicTrendsAI's user interface adheres to these core design principles:

#### Clarity and Simplicity

- **Progressive Disclosure**: Complex features and options are revealed progressively to avoid overwhelming users
- **Clear Hierarchy**: Visual hierarchy guides users to important elements first
- **Minimalist Design**: Only necessary elements are displayed to reduce cognitive load
- **Consistent Terminology**: Business-oriented language rather than technical jargon

#### Information Visualization

- **Data-Ink Ratio**: Maximizing the ratio of data to visual elements by removing unnecessary decorations
- **Appropriate Chart Types**: Using the right visualization for each data type (time series, categories, distributions)
- **Interactive Exploration**: Allowing users to zoom, filter, and highlight within visualizations
- **Context Preservation**: Maintaining context when drilling down into specific data points

#### Accessibility and Inclusivity

- **Color Blind Friendly**: Using color schemes that work for users with color vision deficiencies
- **Readable Typography**: High contrast text with appropriate sizing and spacing
- **Keyboard Navigation**: All features accessible without requiring mouse interaction
- **Screen Reader Support**: Proper labeling of interactive elements for assistive technologies

#### Feedback and Guidance

- **Immediate Feedback**: Visual confirmation of actions taken
- **Helpful Error Messages**: Clear explanations when issues occur with actionable guidance
- **Loading States**: Transparent communication during processing operations
- **Tooltips and Contextual Help**: Just-in-time assistance for complex features

#### Consistency and Standards

- **Visual Consistency**: Uniform color scheme, typography, and spacing throughout
- **Behavioral Consistency**: Similar actions produce similar results across the application
- **Familiar Patterns**: Following established web conventions for common interactions
- **Component Reuse**: Using the same UI components for similar functionality

### 3.7 User Experience Guidelines

#### Information Architecture

- **Logical Organization**: Content organized by user tasks rather than system functions
- **Clear Navigation**: Consistent global navigation with breadcrumbs for deep pages
- **Scalable Structure**: Architecture accommodates future feature additions without reorganization
- **Search Capability**: When content grows, providing search functionality for quick access

#### Visual Design

- **Color System**:
  - Primary palette: Deep blue (#1E3A8A) for headers and primary actions
  - Secondary palette: Teal (#0D9488) for positive trends and success states
  - Accent colors: Amber (#F59E0B) for warnings, Red (#DC2626) for alerts
  - Neutral grays for background and text elements
  
- **Typography**:
  - Sans-serif font family (Inter) for readability on digital screens
  - Clear type hierarchy with 3 heading levels plus body text
  - Minimum 16px font size for body text
  - Line height of 1.5 for optimal readability

- **Spacing System**:
  - Consistent 8px grid system for all spacing and sizing
  - Adequate white space to reduce visual clutter
  - Responsive spacing that adapts to different screen sizes

#### Interaction Design

- **Input Methods**:
  - Primary interactions optimized for mouse/keyboard
  - Touch-friendly targets (minimum 44x44px) for tablet compatibility
  
- **Response Times**:
  - Instant feedback (<100ms) for UI interactions
  - Progress indicators for operations >1 second
  - Background processing with notifications for long operations

- **Data Entry**:
  - Minimizing manual input where possible
  - Clear validation with inline error messages
  - Autosaving of analysis configurations
  
- **Navigation Patterns**:
  - Tab-based navigation for related content areas
  - Breadcrumb trails for hierarchical navigation
  - Persistent access to main features
  - "Back" functionality for multi-step processes

### Mock-ups

Already included in SRS (Figures 2–11).

## 4. Architectural Strategies

### 4.1 Architectural Style

ClinicTrendsAI employs a **layered microservices-inspired architecture** that balances the benefits of modular design with the practical constraints of a streamlined MVP implementation. This section details our architectural decisions, patterns employed, and the rationale behind key design choices.

#### 4.1.1 Primary Architectural Patterns

- **Layered Architecture**: The system implements a layered approach with clear separation between presentation, business logic, data processing, and external service integration.

- **Component-Based Architecture**: Functionality is encapsulated in discrete, loosely-coupled components that communicate through well-defined interfaces, enabling independent development and testing.

- **Event-Driven Elements**: For responsive UI updates and asynchronous processing of computationally intensive operations like ML model training and prediction.

- **Pipeline Pattern**: For data transformation, cleaning, and processing operations, allowing for sequential application of operations with clear inputs and outputs at each stage.

#### 4.1.2 Architectural Pattern Rationale

The selection of these architectural patterns was driven by several key requirements:

1. **Business Requirements**:
   - Need for rapid MVP delivery while maintaining extensibility
   - Support for non-technical users requiring intuitive interfaces
   - Emphasis on visual insights and actionable intelligence

2. **Technical Requirements**:
   - Processing variable-quality CSV data up to 200MB
   - Supporting multiple ML models with different characteristics
   - Maintaining responsive UI during computation-heavy operations
   - Operating within memory constraints of Streamlit deployment

3. **Quality Attribute Requirements**:
   - Usability for business analysts without technical expertise
   - Maintainability through clear component boundaries
   - Scalability to handle increasing data volumes and features
   - Reliability in processing and analyzing customer feedback

### 4.2 Design Patterns

The implementation employs several proven design patterns:

#### 4.2.1 Frontend and UI Patterns

- **Model-View-Controller (MVC)**: Streamlit implements a variation of MVC where:
  - Model: Data processing components and ML models
  - View: Streamlit UI components and visualizations
  - Controller: Streamlit application logic handling user interactions

- **Observer Pattern**: Used for reactive UI updates when underlying data changes, particularly for visualizations that respond to filter changes.

- **Decorator Pattern**: Applied to extend visualization components with additional functionality like tooltips, export options, and interactive elements.

#### 4.2.2 Business Logic Patterns

- **Strategy Pattern**: Implemented for sentiment analysis and prediction models, allowing different algorithms to be selected at runtime while maintaining a consistent interface.

- **Factory Method Pattern**: Used for creating appropriate ML models and processors based on user selections and data characteristics.

- **Adapter Pattern**: Employed to provide a unified interface to different external APIs like Hugging Face Transformers and Deep-Translator.

#### 4.2.3 Data Processing Patterns

- **Pipeline Pattern**: Multi-stage data processing operations are organized as pipelines with clear inputs, transformations, and outputs.

- **Repository Pattern**: Abstracts data access operations, particularly for handling CSV file loading, validation, and in-memory storage.

- **Composite Pattern**: Applied to visualization components to enable hierarchical organization of charts, allowing simple charts to be combined into more complex dashboard views.

### 4.3 Separation of Concerns

The architecture enforces clear separation of concerns across multiple dimensions:

#### 4.3.1 Horizontal Separation (Layers)

- **Presentation Layer**: Streamlit UI components, pages, and interactive elements
- **Business Logic Layer**: Analysis workflows, model selection, alert generation
- **Data Processing Layer**: Data validation, cleaning, transformation, and feature engineering
- **Service Integration Layer**: API clients for external ML and translation services

#### 4.3.2 Vertical Separation (Features)

- **Data Upload and Validation**: Components focused on data ingestion and quality assurance
- **Visualization and Reporting**: Components for generating insights and visual representations
- **ML and Prediction**: Components handling model training, evaluation, and prediction
- **Translation and NLP**: Components for language processing and translation services

This separation enables:
- Independent development and testing of components
- Clear accountability for specific functionality
- Ability to replace or upgrade individual components without affecting others
- Simplified troubleshooting and maintenance

### 4.4 Architectural Decisions and Trade-offs

#### 4.4.1 Key Architectural Decisions

| Decision | Description | Alternatives Considered | Rationale |
|----------|-------------|-------------------------|------------|
| **Streamlit-based frontend** | Using Streamlit for UI development instead of traditional web frameworks | Django, Flask with React, Pure Dash | Streamlit offers rapid development of data-centric applications with minimal frontend code, suitable for data scientists and analysts as primary developers |
| **In-memory data processing** | Holding all data in memory during user session without persistent storage | Database storage, File-based caching | Simplifies MVP implementation, eliminates DB setup/maintenance, provides adequate performance for target data sizes |
| **Multiple ML model options** | Supporting several sentiment analysis approaches from simple (TextBlob) to complex (Transformers) | Single model approach | Provides flexibility for different accuracy/speed tradeoffs and allows users to compare model performance |
| **Asynchronous processing** | Running intensive operations asynchronously to maintain UI responsiveness | Synchronous processing | Prevents UI freezing during model training and prediction, improving user experience |
| **Modular component design** | Building system as composable components with clear interfaces | Monolithic design | Enables parallel development, simplifies testing, and allows for future replacement of individual components |

#### 4.4.2 Architectural Trade-offs

| Aspect | Trade-off | Impact |
|--------|-----------|--------|
| **Streamlit Framework** | ➕ Rapid development, built-in widgets<br>➖ Limited customization, session-based concurrency model | Faster delivery but potential scalability challenges with many concurrent users |
| **Stateless Design** | ➕ Simplicity, no database setup<br>➖ No persistence between sessions, memory constraints | Reduces infrastructure needs but requires data re-upload for each session |
| **Multiple ML Models** | ➕ Flexibility, comparison capabilities<br>➖ Increased complexity, larger deployment size | Better analytical capabilities but requires more thorough testing and documentation |
| **In-memory Processing** | ➕ Speed for smaller datasets<br>➖ Memory limitations for very large files | Good performance up to 200MB files but not suitable for GB-scale datasets |
| **External API Dependencies** | ➕ Advanced capabilities without internal implementation<br>➖ External dependencies, potential latency | Access to state-of-the-art ML models but requires network connectivity |

#### 4.4.3 Technology Selection Rationale

| Technology | Selection Rationale | Risks Mitigated |
|------------|---------------------|------------------|
| **Python** | Excellent ecosystem for data science, ML, and web applications | Widespread expertise, extensive libraries, good performance for data tasks |
| **Streamlit** | Purpose-built for data applications with minimal frontend code | Reduces frontend development complexity, built-in reactive updates |
| **pandas** | Industry standard for tabular data manipulation in Python | Robust handling of CSV data, extensive data cleaning capabilities |
| **scikit-learn** | Mature ML library with consistent APIs and good documentation | Simplified implementation of custom ML pipelines, good performance |
| **Hugging Face Transformers** | State-of-the-art NLP capabilities with simple APIs | Access to advanced models without needing to train from scratch |
| **Altair/Plotly** | Interactive visualization libraries with good Streamlit integration | Rich visualization options without custom JavaScript development |

## 5. System Architecture

### 5.1 System Overview

ClinicTrendsAI employs a modular architecture composed of specialized components that interact through well-defined interfaces. This section details the system's structural organization, component interactions, and data flows.

#### 5.1.1 High-Level System Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              CLINICTRENDS AI                                 │
└──────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                            PRESENTATION LAYER                                │
├───────────────────┬─────────────────────┬───────────────────┬───────────────┤
│    Home Page      │   Dashboard Page    │    Models Page    │  Export Page  │
│                   │                     │                   │               │
│ - App Overview    │ - Visualizations    │ - Model Selection │ - Report     │
│ - File Upload     │ - Filtering         │ - Model Training  │   Generation  │
│ - Getting Started │ - Insights          │ - Predictions     │ - Data Export │
└───────────┬───────┴──────────┬──────────┴──────────┬────────┴───────┬───────┘
            │                  │                     │                 │
            │                  │                     │                 │
            ▼                  ▼                     ▼                 ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                           BUSINESS LOGIC LAYER                             │
├────────────────┬───────────────────┬───────────────────┬──────────────────┤
│ Data Processor │  ML Pipeline      │  NLP Processor    │  Alert System    │
│                │                   │                   │                   │
│ - Validation   │ - Model Training  │ - Sentiment       │ - Threshold      │
│ - Cleaning     │ - Prediction      │   Analysis        │   Detection      │
│ - Feature      │ - Feature         │ - Translation     │ - Notification   │
│   Engineering  │   Importance      │   Services        │   Generation     │
└────────┬───────┴────────┬──────────┴────────┬──────────┴────────┬─────────┘
         │                │                    │                   │
         │                │                    │                   │
         ▼                ▼                    ▼                   ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                         SERVICE INTEGRATION LAYER                          │
├────────────────┬───────────────────┬───────────────────┬──────────────────┤
│ Visualization  │   Report          │   External API    │ Session State    │
│ Engine         │   Generator       │   Clients         │ Manager          │
│                │                   │                   │                   │
│ - Charts       │ - PDF Export      │ - Hugging Face    │ - Data Storage   │
│ - Word Clouds  │ - CSV Export      │ - Deep-Translator │ - State          │
│ - Interactive  │ - Format         │ - TextBlob        │   Persistence    │
│   Elements     │   Selection      │   Integration     │                   │
└────────┬───────┴────────┬──────────┴────────┬──────────┴────────┬─────────┘
         │                │                    │                   │
         │                │                    │                   │
         ▼                ▼                    ▼                   ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                              EXTERNAL SERVICES                             │
├────────────────┬───────────────────┬───────────────────┬──────────────────┤
│ Streamlit      │ Hugging Face      │ Deep-Translator   │ File System      │
│ Cloud          │ Transformers API  │ API               │ (Local/Cloud)    │
└────────────────┴───────────────────┴───────────────────┴──────────────────┘
```

#### 5.1.2 Component Organization

ClinicTrendsAI is composed of these primary components arranged across architectural layers:

**1. Presentation Layer Components:**
- **Frontend UI (Streamlit)**: Handles user interaction, navigation, and visualization display
- **Multi-Page Navigation**: Routes users between different functional areas of the application
- **Interactive Widgets**: Provides controls for data filtering, model selection, and parameter adjustment

**2. Business Logic Layer Components:**
- **Data Processor**: Validates CSV schemas, cleans and preprocesses data
- **ML Pipeline**: Manages model training, evaluation, and prediction workflows
- **NLP Processor**: Performs sentiment analysis and language translation
- **Alert System**: Detects and flags concerning patterns in customer feedback

**3. Service Integration Layer Components:**
- **Visualization Engine**: Generates interactive charts and word clouds
- **Report Generator**: Creates downloadable PDF and CSV reports
- **External API Clients**: Interfaces with third-party services like Hugging Face
- **Session State Manager**: Maintains user session data and state

**4. External Services:**
- **Streamlit Cloud**: Deployment platform for the web application
- **Hugging Face Transformers API**: Provides advanced NLP model capabilities
- **Deep-Translator API**: Offers translation services for multilingual feedback
- **File System**: Storage for user-uploaded files and generated reports

### 5.2 Component Interaction Diagram

```
┌────────────────────────────┐         ┌─────────────────────────────┐
│         USER               │         │      Frontend UI            │
│                            │         │                             │
│  1. Upload CSV             │         │  - Streamlit app.py         │
│  2. Select analysis        ├────────►│  - Multi-page navigation    │
│  3. View visualizations    │         │  - Interactive components   │
│  4. Export reports         │◄────────┤  - Responsive layouts       │
│                            │         │                             │
└────────────────────────────┘         └───────────┬─────────────────┘
                                                   │
                                                   ▼
┌─────────────────────────────┐         ┌─────────────────────────────┐
│                             │         │                             │
│    Data Processor           │◄────────┤     Session State Manager   │
│                             │         │                             │
│  - SchemaValidator          │         │  - In-memory data storage   │
│  - DataCleaner              ├────────►│  - State persistence        │
│  - FeatureEngineer          │         │  - Cross-component          │
│  - ValidationReport         │         │    communication            │
│                             │         │                             │
└───────────┬─────────────────┘         └─────────────────────────────┘
            │                                          ▲
            ▼                                          │
┌─────────────────────────────┐                        │
│                             │                        │
│    ML Pipeline              │                        │
│                             │                        │
│  - ModelSelector            │                        │
│  - ModelTrainer             ├────────────────────────┘
│  - Predictor                │                        ▲
│  - FeatureImportance        │                        │
│                             │                        │
└───────────┬─────────────────┘                        │
            │                                          │
            ▼                                          │
┌─────────────────────────────┐         ┌─────────────────────────────┐
│                             │         │                             │
│    NLP Processor            │         │     Visualization Engine    │
│                             │         │                             │
│  - SentimentAnalyzer        ├────────►│  - ChartBuilder            │
│  - Translator               │         │  - WordCloudGenerator      │
│  - TextProcessor            │         │  - InteractiveVisualizer  │
│                             │         │                             │
└───────────┬─────────────────┘         └───────────┬─────────────────┘
            │                                       │
            │                                       ▼
            │                           ┌─────────────────────────────┐
            │                           │                             │
            │                           │     Report Generator        │
            └──────────────────────────►│                             │
                                        │  - PDFCreator              │
                                        │  - CSVExporter             │
                                        │  - FormatSelector          │
                                        │                             │
                                        └─────────────────────────────┘
```

### 5.3 Subsystem Architecture

This section details the internal architecture of key subsystems within ClinicTrendsAI.

#### 5.3.1 Data Processor

Responsible for all data ingestion, validation, cleaning, and preparation activities.

**Subcomponents:**

- **SchemaValidator**
  - Validates CSV structure against expected schema
  - Checks for required columns (date, score, feedback text, location)
  - Verifies data types and ranges
  - Generates validation reports

- **DataCleaner**
  - Handles missing values through configurable strategies
  - Removes duplicates and outliers
  - Standardizes text formatting
  - Performs date normalization

- **FeatureEngineer**
  - Extracts features from text data
  - Creates derived metrics (e.g., NPS categories)
  - Generates time-based aggregations
  - Prepares data for visualization and ML processing

- **ValidationReport**
  - Generates data quality summaries
  - Provides statistics on data distributions
  - Flags potential data quality issues
  - Offers recommendations for data improvement

**Interfaces:**
- Input: Raw CSV data from user upload
- Output: Cleaned and processed DataFrame for analysis
- Internal: Validation metrics, cleaning logs

**Key Dependencies:**
- pandas for data manipulation
- numpy for numerical operations
- scikit-learn for preprocessing

#### 5.3.2 ML Pipeline

Manages the training, evaluation, and prediction workflows for multiple machine learning models.

**Subcomponents:**

- **ModelSelector**
  - Provides interface for model selection
  - Configures model parameters
  - Manages model registry
  - Implements model versioning

- **ModelTrainer**
  - Implements training workflows for different models
  - Performs cross-validation
  - Tracks training metrics
  - Handles model persistence

- **Predictor**
  - Generates predictions on new data
  - Calculates confidence intervals
  - Performs batch prediction
  - Provides prediction explanations

- **FeatureImportanceCalculator**
  - Extracts feature importance from models
  - Generates SHAP values for explainability
  - Ranks features by impact
  - Visualizes feature contributions

**Interfaces:**
- Input: Processed data from DataProcessor
- Output: Predictions, confidence scores, feature importance
- Internal: Model objects, training metrics

**Key Dependencies:**
- scikit-learn for traditional ML models
- SHAP for model explanations
- Streamlit for interactive model selection

#### 5.3.3 NLP Processor

Provides natural language processing capabilities for sentiment analysis and translation.

**Subcomponents:**

- **SentimentAnalyzer**
  - Implements multiple sentiment analysis approaches
  - TextBlob for basic sentiment scoring
  - Hugging Face models for advanced sentiment
  - Custom trained models for domain-specific analysis

- **Translator**
  - Integrates with Deep-Translator API
  - Detects input language
  - Translates text between languages
  - Preserves formatting and structure

- **TextProcessor**
  - Performs text cleaning and normalization
  - Tokenization and lemmatization
  - Stop word removal
  - Named entity recognition

**Interfaces:**
- Input: Text data from feedback columns
- Output: Sentiment scores, translated text, processed text features
- External: Hugging Face API, Deep-Translator API

**Key Dependencies:**
- transformers library for Hugging Face models
- TextBlob for basic NLP
- deep-translator for translation services
- NLTK for text processing

#### 5.3.4 Visualization Engine

Generates interactive visualizations for data exploration and insights.

**Subcomponents:**

- **ChartBuilder**
  - Creates various chart types (line, bar, scatter, etc.)
  - Implements responsive design for different screen sizes
  - Handles data formatting for visualization
  - Provides consistent styling across charts

- **WordCloudGenerator**
  - Generates word clouds from text data
  - Configures appearance and layout
  - Filters words by frequency and relevance
  - Colors words by sentiment or category

- **InteractiveVisualizer**
  - Adds interactive elements to charts
  - Implements tooltips and hover effects
  - Provides zoom and pan capabilities
  - Enables filtering and drill-down

**Interfaces:**
- Input: Processed data and analysis results
- Output: Interactive visualization objects
- Internal: Chart configurations, color schemes

**Key Dependencies:**
- Altair for interactive visualizations
- Plotly for complex charts
- Matplotlib for static visualizations
- WordCloud for text visualization

#### 5.3.5 Report Generator

Creates downloadable reports and data exports in various formats.

**Subcomponents:**

- **PDFCreator**
  - Generates PDF reports with visualizations
  - Formats text and charts for print
  - Includes analysis summaries and insights
  - Adds headers, footers, and pagination

- **CSVExporter**
  - Exports processed data to CSV format
  - Configures column selection and formatting
  - Implements data filtering options
  - Provides data transformation options

- **FormatSelector**
  - Manages available export formats
  - Handles format-specific configurations
  - Implements preview capabilities
  - Provides format conversion

**Interfaces:**
- Input: Analysis results, visualizations, and processed data
- Output: Downloadable files in various formats
- Internal: Formatting templates, styling configurations

**Key Dependencies:**
- ReportLab for PDF generation
- pandas for CSV export
- base64 for file encoding in Streamlit

### 5.4 Data Flow Architecture

This section describes the key data flows through the ClinicTrendsAI system.

#### 5.4.1 Data Flow Diagram (Level 1)

```
┌──────────────┐          ┌───────────────┐          ┌───────────────┐
│              │  1. CSV  │               │  2. Clean │               │
│    User      ├─────────►│ Data Processor ├─────────►│  Analysis     │
│              │  Upload  │               │   Data    │  Components   │
└──────┬───────┘          └───────────────┘          └───────┬───────┘
       │                                                      │
       │                                                      │
       │                                                      │
       │                                                      │
       │ 6. View           ┌───────────────┐  3. Analysis     │
       │ Reports &         │               │  Results         │
       └─────────────────► │ Visualization │ ◄────────────────┘
         Visualizations    │ & Reporting   │
                           │               │
                           └───────┬───────┘
                                   │
                                   │ 4. Export
                                   │ Request
                                   │
                                   ▼
                           ┌───────────────┐
                           │               │
                           │ Report        │
                           │ Generator     │
                           │               │
                           └───────┬───────┘
                                   │
                                   │ 5. Download
                                   │ Files
                                   │
                                   ▼
                           ┌───────────────┐
                           │               │
                           │ User's        │
                           │ Device        │
                           │               │
                           └───────────────┘
```

#### 5.4.2 Key Data Flows

**1. Data Ingestion Flow**

- User uploads CSV file through Streamlit interface
- File is validated for format and required columns
- Data is parsed into pandas DataFrame
- Validation results are presented to user
- On validation success, data is stored in session state

**2. Analysis Flow**

- User selects analysis parameters (model, time range, locations)
- Processed data is retrieved from session state
- Selected ML models are applied to data
- NLP processing is performed on text feedback
- Predictions and sentiment scores are calculated
- Feature importance is determined
- Results are stored in session state

**3. Visualization Flow**

- Analysis results are retrieved from session state
- Visualization components render interactive charts
- Word clouds are generated from text data
- User applies filters and parameters
- Visualizations update reactively
- Charts are displayed in Streamlit UI

**4. Export Flow**

- User configures export parameters
- Selected visualizations are rendered for export
- Analysis summaries are formatted
- PDF or CSV files are generated
- Download links are provided to user

**5. Alert Flow**

- Thresholds for alerts are configured
- Analysis results are evaluated against thresholds
- Alerts are generated for concerning patterns
- Alerts are displayed prominently in UI
- Alert details are included in reports

### 5.5 Security Architecture

The security architecture of ClinicTrendsAI addresses several key aspects of data protection and system integrity.

#### 5.5.1 Data Security

- **Stateless Operation**: No customer data is persistently stored by the application
- **In-Memory Processing**: Data exists only within user session memory
- **Data Isolation**: Each user session maintains separate data spaces
- **Transport Security**: HTTPS recommended for production deployment
- **Data Minimization**: Only necessary fields processed from CSV files

#### 5.5.2 Authentication and Authorization

- **MVP Scope**: No user authentication in initial release
- **Future Extensions**: Planned integration with authentication providers
- **Access Control**: All users have equal access to functionality
- **Session Management**: Streamlit's session state mechanism for isolation

#### 5.5.3 External Service Security

- **API Security**: Secure connections to external services (Hugging Face, Deep-Translator)
- **Error Handling**: Graceful failure without exposing sensitive information
- **Rate Limiting**: Managed access to external APIs to prevent abuse
- **Credential Management**: Environment variables for API keys (not in codebase)

#### 5.5.4 Deployment Security

- **Containerization**: Deployment via Streamlit Cloud with container isolation
- **Dependencies**: Regular updates of dependencies for security patches
- **Input Validation**: Thorough validation of all user inputs
- **Output Encoding**: Proper encoding of all output to prevent injection attacks

### 5.6 Deployment Architecture

ClinicTrendsAI supports multiple deployment configurations to accommodate different usage scenarios.

#### 5.6.1 Local Deployment

- **Development Environment**: Local Python environment with required dependencies
- **Resource Requirements**: Minimum 8GB RAM, 4 CPU cores recommended
- **Networking**: Localhost:8501 by default
- **Storage**: Local file system for temporary file operations
- **Scaling**: Single-user instance

#### 5.6.2 Cloud Deployment

- **Primary Platform**: Streamlit Cloud for public access
- **Alternative Platforms**: Heroku, AWS Elastic Beanstalk, Google Cloud Run
- **Resource Allocation**: Managed by platform, scaled based on usage
- **Networking**: Public HTTPS endpoint with Streamlit-managed domain
- **Storage**: Ephemeral storage for session duration
- **Scaling**: Multiple concurrent users supported by separate sessions

## 6. Detailed System Design

### MLModel

#### 6.1 Classification

Class

#### 6.2 Definition

Encapsulates machine learning functionality for predicting NPS trends.

#### 6.3 Responsibilities

- Train scikit-learn regression models.
- Generate NPS predictions with confidence intervals.
- Provide feature importance scores.

#### 6.4 Constraints

- Limited to linear regression and decision trees in MVP.
- Must execute predictions in under 10 seconds.
- Relies on pre-cleaned datasets.

#### 6.5 Composition

- Attributes:
    - `model_type`
    - `trained_model`
- Methods:
    - `train(data)`
    - `predict(data)`
    - `feature_importance()`

#### 6.6 Uses/Interactions

- Uses DataProcessor to receive cleaned data.
- Sends results to Visualization Engine.
- Interacts with Alert System for low NPS warnings.

#### 6.7 Resources

- CPU and memory resources.
- Python scikit-learn library.

#### 6.8 Processing

- Data transformation via TF-IDF if textual data used.
- Model prediction → Output score + confidence interval.

#### 6.9 Interface/Exports

- Exposes:
    - `predict(data)`
    - `feature_importance()`

#### 6.10 Detailed Subsystem Design

- Algorithms:
    - Linear Regression
    - Decision Trees
- Pseudocode:

```python
def predict(data):
    cleaned = preprocess(data)
    return model.predict(cleaned)
```

## 7. Glossary

| Term        | Definition                                               |
|-------------|----------------------------------------------------------|
| NPS         | Net Promoter Score, measuring customer satisfaction.     |
| TF-IDF      | Statistical method for text feature extraction.          |
| CSV         | Comma-Separated Values file format.                      |
| UI          | User Interface.                                          |
| MVP         | Minimum Viable Product.                                  |

## 8. Bibliography

- Streamlit Documentation. https://docs.streamlit.io/
- Scikit-learn Documentation. https://scikit-learn.org/stable/
- Hugging Face Transformers. https://huggingface.co/docs/transformers
- Wiegers, K. (1999). Software Requirements Specification Template.
