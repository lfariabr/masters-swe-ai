const express = require('express');
const multer = require('multer');
const xlsx = require('xlsx');
const cors = require('cors');
const path = require('path');

const app = express();

// Simple CORS configuration - allow all origins
app.use(cors());

// Add CORS headers to all responses
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
  
  // Handle preflight OPTIONS requests
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }
  
  next();
});

// Standard middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Configure file upload with error handling
const storage = multer.memoryStorage();
const upload = multer({ 
  storage,
  limits: { fileSize: 10 * 1024 * 1024 } // 10MB limit
}).array('files');

/**
 * API Endpoint for file upload
 * Handles Excel file parsing and validation
 */
app.post('/upload', (req, res) => {
  upload(req, res, function(err) {
    // Handle multer errors
    if (err instanceof multer.MulterError) {
      console.error('Multer error:', err);
      return res.status(400).json({ error: `File upload error: ${err.message}` });
    } else if (err) {
      console.error('Unknown error during upload:', err);
      return res.status(500).json({ error: 'Unknown error occurred during file upload' });
    }
    
    try {
      const files = req.files;
      if (!files || files.length === 0) {
        return res.status(400).json({ error: 'No files uploaded' });
      }

      const data = files.map(file => {
        try {
          const workbook = xlsx.read(file.buffer, { type: 'buffer' });
          const sheetName = workbook.SheetNames[0];
          return xlsx.utils.sheet_to_json(workbook.Sheets[sheetName]);
        } catch (xlsxError) {
          console.error('Excel parsing error:', xlsxError);
          throw new Error(`Invalid Excel file format: ${file.originalname}`);
        }
      });

      // Set CORS headers explicitly for this response
      res.setHeader('Access-Control-Allow-Origin', '*');
      res.json({ filesData: data });
    } catch (error) {
      console.error('Error processing files:', error);
      res.status(500).json({ error: error.message || 'Error processing Excel files' });
    }
  });
});

// Serve static files in production
if (!process.env.NODE_ENV || process.env.NODE_ENV === 'production') {
  app.use(express.static(path.join(__dirname, 'build')));
  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'build', 'index.html'));
  });
}

/**
 * Error handling middleware
 * This should be placed after all other middleware and routes
 */
app.use((err, req, res, next) => {
  console.error('Server error:', err.stack);
  res.status(500).json({
    error: 'Internal Server Error',
    message: err.message
  });
});

// Add a health check route for the main process to verify the server is running
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Start the server
const PORT = process.env.PORT || 5000;
const server = app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

// Handle server shutdown gracefully
process.on('SIGINT', () => {
  console.log('Express server shutting down...');
  server.close(() => {
    console.log('Express server closed');
    process.exit(0);
  });
});

// For Windows compatibility
process.on('SIGTERM', () => {
  console.log('Express server shutting down...');
  server.close(() => {
    console.log('Express server closed');
    process.exit(0);
  });
});

// Export the app for Electron to require
module.exports = app;

// Start server only when not in Electron production
if (!process.versions.electron || process.env.NODE_ENV === 'development') {
  const port = process.env.PORT || 5000;
  app.listen(port, () => console.log(`Server running on port ${port}`));
}