/**
 * InputPage Component
 * Handles file uploads and initial data display
 */
import React from 'react';
import FileUploader from '../components/FileUploader';
import DataTable from '../components/DataTable';

const InputPage = ({ 
  transcriptData, 
  curriculumData, 
  onFileUpload, 
  onProcess 
}) => {
  const canProcess = transcriptData?.length > 0 && curriculumData?.length > 0;
  
  return (
    <div className="input-page">
      <div className="header-section">
        <h1>🎓 <span className="title-highlight">TTrack – Torrens Degree Tracker</span></h1>
        <p>Built by students for academic advisors at Torrens University Australia.</p>
        <em>Guided by Dr. Atif Qureshi – Software Development Management, 2025</em>
      </div>

      <div className="button-row">
        <FileUploader 
          type="transcript" 
          onFileUpload={onFileUpload} 
          label="Upload Transcript" 
          icon="📄"
        />
        
        <FileUploader 
          type="curriculum" 
          onFileUpload={onFileUpload} 
          label="Upload Curriculum" 
          icon="📚"
        />

        {canProcess && (
          <button 
            className="process-btn" 
            onClick={onProcess}
          >
            ✓ Process Data
          </button>
        )}
      </div>

      <div className="data-display">
        <DataTable title="Transcript Data" data={transcriptData} />
        <DataTable title="Curriculum Data" data={curriculumData} />
      </div>
    </div>
  );
};

export default InputPage;
