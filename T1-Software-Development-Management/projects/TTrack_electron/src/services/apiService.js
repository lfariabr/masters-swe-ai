/**
 * API Service for TTrack Electron
 * Handles all communication with the backend server and local processing
 */
import axios from 'axios';
import { matchCourses } from './resolverService';

/**
 * Configure API settings
 * Uses absolute URLs in development, relative URLs in production
 */
const isDev = process.env.NODE_ENV === 'development';
const API_BASE_URL = isDev ? 'http://localhost:5000' : '';

/**
 * Upload a file to the server for processing
 * @param {File} file - The file to upload
 * @param {string} fileType - The type of file (transcript or curriculum)
 * @returns {Promise<Array>} - Parsed file data
 */
export const uploadFile = async (file, fileType) => {
  try {
    const formData = new FormData();
    formData.append('files', file);

    // Create a configured instance of axios with custom settings
    const axiosInstance = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000, // 30 seconds timeout
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    // For development environments, handle CORS
    if (isDev) {
      axiosInstance.defaults.withCredentials = true;
    }

    console.log(`Uploading ${fileType} file to ${API_BASE_URL}/upload`);
    const response = await axiosInstance.post('/upload', formData);

    return response.data.filesData[0];
  } catch (error) {
    console.error(`Error uploading ${fileType} file:`, error);
    
    // Try local processing fallback if server request failed
    if (error.message === 'Network Error') {
      console.warn('Network error detected. Attempting local file processing...');
      return processFileLocally(file, fileType);
    }
    
    throw error;
  }
};

/**
 * Process file locally as a fallback when server is unavailable
 * @param {File} file - The file to process
 * @param {string} fileType - The type of file
 * @returns {Promise<Array>} - Processed data
 */
const processFileLocally = async (file, fileType) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    
    reader.onload = (e) => {
      try {
        // This is a simple example of parsing CSV data
        // In a real implementation, you would need to use a proper Excel parser library
        const lines = e.target.result.split('\n');
        const headers = lines[0].split(',');
        
        const data = [];
        for (let i = 1; i < lines.length; i++) {
          if (lines[i].trim() === '') continue;
          
          const values = lines[i].split(',');
          const entry = {};
          
          for (let j = 0; j < headers.length; j++) {
            entry[headers[j].trim()] = values[j]?.trim() || '';
          }
          
          data.push(entry);
        }
        
        resolve(data);
      } catch (error) {
        console.error('Error processing file locally:', error);
        reject(new Error('Failed to process file locally'));
      }
    };
    
    reader.onerror = () => {
      reject(new Error('Failed to read file'));
    };
    
    reader.readAsText(file);
  });
};

/**
 * Process transcript and curriculum data to generate matching results
 * First attempts server-side processing, falls back to client-side if server fails
 * @param {Array} transcriptData - Array of transcript course objects
 * @param {Array} curriculumData - Array of curriculum requirement objects
 * @returns {Object} Results containing matched courses, missing courses, and recommendations
 */
export const processMatching = async (transcriptData, curriculumData) => {
  try {
    // Try server-side processing first
    const response = await axios.post(`${API_BASE_URL}/process`, {
      transcript: transcriptData,
      curriculum: curriculumData
    });
    return response.data;
  } catch (error) {
    console.warn('Server-side processing failed, falling back to client-side:', error);
    
    // Fall back to client-side processing if server fails
    return matchCourses(transcriptData, curriculumData);
  }
};

/**
 * Export processed results to Excel file (if server supports it)
 * @param {Object} results - The processed matching results
 * @returns {string} URL to download the exported file
 */
export const exportResults = async (results) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/export`, { results });
    return response.data.fileUrl;
  } catch (error) {
    console.error('Error exporting results:', error);
    throw error;
  }
};
