# SDM404 Assessment 1 – Event Feedback & Survey Platform

**Team Members**: 
- Luis Guilherme de Barros Andrade Faria  
- [Team Member 1]  
- [Team Member 2]  
- [Team Member 3]  
**Student IDs**: 
- A00187785  
- [Student ID 1]  
- [Student ID 2]  
- [Student ID 3]  
**Project Title**: Real-Time Event Feedback & NPS Analytics Platform  
**Date**: 31 May 2025  
**Word Count**: [To be updated]

---

## 1. Project Overview
### Problem Statement
Event organizers and clinic staff face significant challenges in collecting, processing, and acting on attendee feedback in real-time. Current solutions are often cost-prohibitive or overly complex, leading to underutilized feedback and missed opportunities for improvement. This platform addresses these issues by providing a lightweight, automated feedback collection and analysis system.

### Target Users/Clients
- **Primary Users**: 
  - Event managers
  - Clinic staff
  - Team leads
- **Secondary Users**:
  - Event attendees providing feedback
  - Department heads reviewing analytics

### Project Goals
1. Create a no-cost feedback collection system using Google Forms
2. Implement real-time data processing and NPS calculation
3. Develop an automated alert system for critical feedback
4. Provide visual analytics dashboard for stakeholders
5. Ensure data privacy and security compliance

### Tools & Technologies
| Category | Technology | Purpose |
|----------|------------|----------|
| Frontend | Google Forms, Streamlit | User interface & dashboard |
| Backend | Google App Script | Data processing & automation |
| Database | Google Sheets | Data storage |
| Analytics | Python (Pandas, Matplotlib) | Data analysis & visualization |
| Hosting | Google Cloud (Free Tier) | Application hosting |

---

## 2. Development Methodology
### Selected Methodology: Agile with Sprints
This project will follow an Agile methodology with 2-week sprints to allow for iterative development and continuous feedback integration.

### Methodology Justification
1. **Iterative Development**: Enables continuous improvement based on stakeholder feedback
2. **Risk Mitigation**: Early identification and resolution of issues
3. **Flexibility**: Adaptable to changing requirements or new insights
4. **Stakeholder Engagement**: Regular demos ensure alignment with user needs

### Referenced Theory
- Cobb, C. (2015). *The Project Manager's Guide to Mastering Agile*. Wiley.
- Schwaber, K., & Sutherland, J. (2017). *The Scrum Guide*. Scrum.org

---

## 3. Scope & Deliverables
### In-Scope
- Customizable feedback form with NPS question
- Real-time data collection and processing
- Automated email alerts for critical feedback
- NPS calculation and trend analysis
- Role-based dashboard for different stakeholders
- Basic reporting and data export functionality

### Out-of-Scope
- Multi-language support
- SMS notifications
- Advanced user management
- Offline data collection
- Mobile application

### Deliverables
1. Functional Google Form with NPS integration
2. Google Sheet with automated data processing
3. Email notification system for critical feedback
4. Streamlit dashboard for data visualization
5. Comprehensive documentation

---

## 4. Timeline & Milestones
| Milestone | Tasks | Owner | Start Date | End Date | Status |
|-----------|-------|-------|------------|----------|--------|
| Sprint 1: Setup & Form Design | Project setup, Form creation, Sheet structure | [Team Member 1] | 01/06/2025 | 07/06/2025 | Not Started |
| Sprint 2: Automation | AppScript integration, Email triggers | [Team Member 2] | 08/06/2025 | 21/06/2025 | Not Started |
| Sprint 3: Dashboard | Streamlit dashboard, Basic analytics | [Team Member 3] | 22/06/2025 | 05/07/2025 | Not Started |
| Sprint 4: Refinement | Testing, Documentation, Final touches | Luis Faria | 06/07/2025 | 19/07/2025 | Not Started |
| Final Week | Review, Polish, Submit | [Team Member 1] | 20/07/2025 | 26/07/2025 | Not Started |

---

## 5. Team Roles & Responsibilities
| Name | Role | Key Responsibilities |
|------|------|----------------------|
| [Team Member 1] | Project Manager | Overall coordination, timeline tracking, stakeholder communication |
| [Team Member 2] | Frontend Developer | Google Forms customization, Streamlit dashboard |
| [Team Member 3] | Backend Developer | Google App Script, data processing |
| [Team Member 4] | Data Analyst | NPS calculations, reporting, visualization |
| Luis Faria | Full-Stack Developer | System architecture, integration, quality assurance |

Join the team on Discord: https://discord.gg/yExGHSxA

---

## 6. Cost & Effort Estimation
### Human Resources
| Role | Hours Required | Team Member | Rate (AUD/hour) | Total Cost |
|------|----------------|-------------|-----------------|------------|
| Project Manager | 30 | [Name] | $35 | $1,050 |
| Frontend Developer | 40 | [Name] | $30 | $1,200 |
| Backend Developer | 45 | [Name] | $30 | $1,350 |
| Data Analyst | 35 | [Name] | $30 | $1,050 |
| Full-Stack Developer | 40 | Luis Faria | $30 | $1,200 |
| **Total** | **190** | | | **$5,850** |

### Infrastructure Costs
| Resource | Specification | Cost (AUD) |
|----------|---------------|------------|
| Google Cloud | Free Tier | $0 |
| Domain Name | Not required | $0 |
| Development Tools | Open Source | $0 |
| **Total** | | **$0** |

---

## 7. Risk Management
| Risk | Likelihood (H/M/L) | Impact (H/M/L) | Mitigation Strategy |
|------|-------------------|----------------|----------------------|
| Google API Quota Limits | M | H | Implement rate limiting and caching |
| Stakeholder Engagement | H | M | Weekly summary emails, clear value demonstration |
| Data Privacy Concerns | M | H | Ensure GDPR compliance, anonymize data |
| Technical Complexity | M | M | Start with MVP, prioritize core features |

---

## 8. Communication Plan
| Tool | Purpose | Frequency | Owner |
|------|---------|-----------|-------|
| Discord | Team meetings, async communication | Daily | All |
| GitHub | Code repository, issues, PRs | Continuous | All |
| Trello | Task tracking, sprint planning | Daily | PM |
| Google Drive | Shared documents, assets | As needed | All |
| Weekly Sync | Progress updates, blockers | Weekly | PM |

### Meeting Schedule
- **Weekly Sync**: 15 mins, Weekly @ 8:30 AM (Discord)
- **Sprint Planning**: 1 hour, Every 2 weeks (Discord)
- **Retrospective**: 30 mins, End of each sprint (Discord)
- **Client Demo**: 30 mins, End of each sprint (Zoom)

### Communication Guidelines
1. **Discord Channels**:
   - #general - Announcements and general info
   - #development - Technical discussions
   - #design - UI/UX discussions
   - #random - Off-topic discussions
2. **Response Time**:
   - Urgent: 2 hours
   - Normal: 12 hours
   - Low priority: 24 hours

---

## 9. Appendices
### A. System Architecture
[To be added: Architecture diagram showing Google Forms → Google Sheets → App Script → Email/Dashboard]

### B. UI/UX Mockups
[To be added: Wireframes of the feedback form and dashboard]

### C. Meeting Logs
| Date | Key Decisions | Next Steps |
|------|---------------|-------------|
| 31/05/2025 | Project scope defined | Finalize requirements |

---

## 10. Individual Contribution Report - Luis Faria
### Tasks Performed
1. **System Architecture**
   - Designed overall system architecture
   - Set up integration between components
   - Ensured data flow efficiency

2. **Integration & QA**
   - Managed API connections
   - Implemented error handling
   - Conducted system testing

3. **Team Collaboration**
   - Facilitated technical discussions
   - Reviewed pull requests
   - Mentored junior team members

### Challenges Faced
1. **Challenge**: Coordinating between team members across time zones  
   **Solution**: Established clear communication protocols and async updates

2. **Challenge**: Ensuring consistent code quality  
   **Solution**: Implemented code reviews and CI/CD pipelines

### Lessons Learned
1. Importance of clear documentation in team settings
2. Effective remote collaboration techniques
3. Balancing individual contributions with team goals
4. Managing technical debt in a team environment

### Self-Evaluation
[To be completed during project execution]

---
*Word Count: [To be updated]*
*Last Updated: 31/05/2025*
