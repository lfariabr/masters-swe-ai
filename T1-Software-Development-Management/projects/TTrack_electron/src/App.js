import React, { useState } from "react";
import { uploadFile, processMatching } from "./services/apiService";
import InputPage from "./pages/InputPage";
import ResultsPage from "./pages/ResultsPage";
import "./styles/App.css";

/**
 * Main App Component for TTrack Electron
 * Handles state management and page routing
 */
function App() {
  // State management
  const [transcriptData, setTranscriptData] = useState([]);
  const [curriculumData, setCurriculumData] = useState([]);
  const [matchResults, setMatchResults] = useState(null);
  const [currentPage, setCurrentPage] = useState('input');
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);

  /**
   * Handle file uploads for transcript and curriculum
   * @param {File} file - The uploaded file
   * @param {string} type - The type of file ('transcript' or 'curriculum')
   */
  const handleFileUpload = async (file, type) => {
    try {
      setError(null);
      const data = await uploadFile(file, type);
      
      if (type === "transcript") {
        setTranscriptData(data);
      } else {
        setCurriculumData(data);
      }
    } catch (err) {
      setError(`Error uploading ${type}: ${err.message}`);
      console.error(`Error uploading ${type}:`, err);
    }
  };

  /**
   * Process the transcript and curriculum data to generate results
   */
  const handleProcess = async () => {
    if (!transcriptData.length || !curriculumData.length) {
      setError("Please upload both transcript and curriculum files");
      return;
    }

    try {
      setIsProcessing(true);
      setError(null);
      
      const results = await processMatching(transcriptData, curriculumData);
      setMatchResults(results);
      setCurrentPage('results');
    } catch (err) {
      setError(`Error processing data: ${err.message}`);
      console.error('Error processing data:', err);
    } finally {
      setIsProcessing(false);
    }
  };

  /**
   * Go back to the input page from results
   */
  const handleBackToInput = () => {
    setCurrentPage('input');
  };

  // Render current page based on state
  return (
    <div className="container">
      {error && (
        <div className="error-message">
          {error}
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}
      
      {isProcessing && (
        <div className="processing-overlay">
          <div className="processing-message">
            <div className="spinner"></div>
            <p>Processing data...</p>
          </div>
        </div>
      )}
      
      {currentPage === 'input' ? (
        <InputPage
          transcriptData={transcriptData}
          curriculumData={curriculumData}
          onFileUpload={handleFileUpload}
          onProcess={handleProcess}
        />
      ) : (
        <ResultsPage
          matchResults={matchResults}
          onBack={handleBackToInput}
        />
      )}
    </div>
  );
}

export default App;
