const { app, BrowserWindow } = require('electron');
const path = require('path');
const isDev = !app.isPackaged;
const { spawn } = require('child_process');
const fs = require('fs');

let mainWindow;
let serverProcess;
const serverPort = 5000;

// process.env.DEBUG = '*';
/**
 * Start the Express server as a separate process
 */
function startExpressServer() {
  return new Promise((resolve, reject) => {
    // Kill any existing server process
    if (serverProcess) {
      serverProcess.kill();
      serverProcess = null;
    }

    console.log('Starting Express server...');
    const serverPath = isDev ? './server.js' : path.join(process.resourcesPath, 'server.js');
    
    // Start the server as a separate process
    serverProcess = spawn('node', [serverPath]);
    
    // Handle server output
    serverProcess.stdout.on('data', (data) => {
      console.log(`Server: ${data}`);
      // Resolve when server is ready
      if (data.toString().includes('Server running on port')) {
        resolve();
      }
    });
    
    serverProcess.stderr.on('data', (data) => {
      console.error(`Server error: ${data}`);
    });
    
    serverProcess.on('error', (err) => {
      console.error('Failed to start server process:', err);
      reject(err);
    });
    
    // Resolve after a timeout if no ready message is received
    setTimeout(() => {
      resolve();
    }, 2000);
  });
}

/**
 * Create the main application window
 */
async function createWindow() {
  try {
    // Start the Express server first
    await startExpressServer();
    
    mainWindow = new BrowserWindow({
      width: 1200,
      height: 800,
      webPreferences: {
        nodeIntegration: true,
        contextIsolation: false,
        enableRemoteModule: true
      }
    });

    if (isDev) {
      // Development: Load from React dev server
      console.log('Loading from React dev server at http://localhost:3000');
      mainWindow.loadURL('http://localhost:3000');
      mainWindow.webContents.openDevTools();
    } else {
      // Production: Load built files
      console.log('Loading from built files');
      mainWindow.loadFile(path.join(__dirname, 'build', 'index.html'));
    }
    
    // Handle window close
    mainWindow.on('closed', () => {
      mainWindow = null;
    });
  } catch (error) {
    console.error('Error starting application:', error);
  }
}

app.whenReady().then(createWindow);

// Properly clean up resources when the app is quitting
app.on('before-quit', () => {
  console.log('Application quitting - cleaning up resources');
  if (serverProcess) {
    console.log('Terminating Express server process');
    serverProcess.kill();
    serverProcess = null;
  }
});

app.on('window-all-closed', () => {
  // On macOS it is common for applications to stay open until explicitly quit
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  // On macOS it's common to re-create a window when the dock icon is clicked
  if (mainWindow === null) {
    createWindow();
  }
});