/**
 * ResultsPage Component
 * Displays progress summary, status tracking, and elective recommendations
 */
import React, { useState } from 'react';
import DataTable from '../components/DataTable';
import ProgressChart from '../components/ProgressChart';
import { exportResults } from '../services/apiService';

const ResultsPage = ({ matchResults, onBack }) => {
  const [activeTab, setActiveTab] = useState('completed');
  const [isExporting, setIsExporting] = useState(false);
  const [exportUrl, setExportUrl] = useState(null);
  
  if (!matchResults) {
    return (
      <div className="results-page">
        <div className="empty-state-container">
          <h2>No results to display</h2>
          <p>Please upload transcript and curriculum data first.</p>
          <button className="back-btn" onClick={onBack}>
            ← Back to Upload
          </button>
        </div>
      </div>
    );
  }

  const { matchedCourses = [], missingCourses = [], recommendations = [], stats = {} } = matchResults;
  
  // Calculate completion percentage if not provided
  const completionPercentage = stats.percentageComplete || (
    (matchedCourses.length > 0 || missingCourses.length > 0) ?
    Math.round((matchedCourses.length / (matchedCourses.length + missingCourses.length)) * 100) : 0
  );
  
  // Handle export
  const handleExport = async () => {
    try {
      setIsExporting(true);
      const url = await exportResults(matchResults);
      setExportUrl(url);
    } catch (err) {
      console.error('Export failed:', err);
      alert('Export failed. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="results-page">
      <div className="header-section">
        <h1>🎓 <span className="title-highlight">Analysis Results</span></h1>
        <div className="header-actions">
          <button 
            className="export-btn" 
            onClick={handleExport} 
            disabled={isExporting}
          >
            {isExporting ? 'Exporting...' : '📊 Export Report'}
          </button>
          <button className="back-btn" onClick={onBack}>
            ← Back to Upload
          </button>
        </div>
      </div>

      {exportUrl && (
        <div className="export-success">
          <p>Export successful! <a href={exportUrl} download>Download Excel Report</a></p>
          <button onClick={() => setExportUrl(null)}>✕</button>
        </div>
      )}

      <div className="summary-section">
        <div className="summary-box">
          <h3>Degree Progress Summary</h3>
          <div className="summary-content">
            <div className="progress-chart-container">
              <ProgressChart percentage={completionPercentage} />
            </div>
            <div className="progress-stats">
              <div className="stat-item">
                <span className="stat-label">Completed:</span> 
                <span className="stat-value">{matchedCourses.length} courses</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Missing:</span> 
                <span className="stat-value">{missingCourses.length} courses</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Total Required:</span> 
                <span className="stat-value">{matchedCourses.length + missingCourses.length} courses</span>
              </div>
            </div>
            <div className="progress-message">
              {completionPercentage < 25 && (
                <p>Just starting your academic journey. Keep up the good work!</p>
              )}
              {completionPercentage >= 25 && completionPercentage < 50 && (
                <p>You're making good progress toward your degree.</p>
              )}
              {completionPercentage >= 50 && completionPercentage < 75 && (
                <p>You're over halfway through your program!</p>
              )}
              {completionPercentage >= 75 && completionPercentage < 100 && (
                <p>The finish line is in sight! Just a few more courses to go.</p>
              )}
              {completionPercentage === 100 && (
                <p>Congratulations! You've completed all requirements for your degree.</p>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="results-tabs">
        <div className="tab-buttons">
          <button 
            className={`tab-btn ${activeTab === 'completed' ? 'active' : ''}`}
            onClick={() => setActiveTab('completed')}
          >
            ✓ Completed ({matchedCourses.length})
          </button>
          <button 
            className={`tab-btn ${activeTab === 'missing' ? 'active' : ''}`}
            onClick={() => setActiveTab('missing')}
          >
            ✗ Missing ({missingCourses.length})
          </button>
          <button 
            className={`tab-btn ${activeTab === 'recommendations' ? 'active' : ''}`}
            onClick={() => setActiveTab('recommendations')}
          >
            ⭐ Recommendations ({recommendations.length})
          </button>
        </div>

        <div className="tab-content">
          {activeTab === 'completed' && (
            <DataTable title="Completed Courses" data={matchedCourses} />
          )}
          {activeTab === 'missing' && (
            <DataTable title="Missing Courses" data={missingCourses} />
          )}
          {activeTab === 'recommendations' && (
            <div className="recommendations-container">
              <h3>Course Recommendations</h3>
              {recommendations.length > 0 ? (
                <div className="recommendations-list">
                  {recommendations.map((course, index) => (
                    <div key={index} className="recommendation-card">
                      <div className="recommendation-header">
                        <h4>{course.CourseCode || course.Code}: {course.CourseName || course.Name}</h4>
                        {course.Status === 'Failed' && <span className="status-badge failed">Failed Previously</span>}
                      </div>
                      <div className="recommendation-body">
                        <p><strong>Type:</strong> {course.Type || 'Required Course'}</p>
                        <p><strong>Reason:</strong> {course.RecommendationReason}</p>
                        {course.Credits && <p><strong>Credits:</strong> {course.Credits}</p>}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="empty-recommendations">
                  <p>No recommendations available.</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
