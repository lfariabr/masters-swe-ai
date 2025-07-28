# Test Plan – ClinicTrends AI

## 1. Introduction
This document outlines the testing strategy for the ClinicTrends AI application, covering functional, non-functional, and user acceptance testing.

## 2. Test Objectives
- Verify data upload functionality.
- Validate sentiment analysis accuracy.
- Ensure visualization and export work correctly.
- Confirm performance and reliability.

## 3. Test Scope
- Included: Upload CSV, display summary, ML analysis, export PDF.
- Excluded: Backend service logic not exposed via UI.

## 4. Test Environment
- Platform: Streamlit Web App
- Data Source: Sample CSV with NPS feedback
- Libraries: pandas, scikit-learn, altair, huggingface

## 5. Test Scenarios

| ID | Description | Input | Expected Output | Status |
|----|-------------|-------|------------------|--------|
| TC01 | Upload valid CSV | `clinicTrendsAiSample.csv` | Data previewed | ✅ |
| TC02 | Invalid CSV format | `.xlsx` file | Error message | ✅ |
| TC03 | Display dashboard | Valid CSV | Charts and summary shown | ✅ |
| TC04 | Export report | Click Export | PDF generated | ✅ |
***expand more...***

## 6. Performance Testing
- Load 10k+ rows → App must respond within 5s.
- Stress test with 3+ parallel sessions.

## 7. Acceptance Criteria
- All test cases pass
- Feedback aligns with expected NPS logic
- No critical errors during demo