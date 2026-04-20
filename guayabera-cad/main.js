const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const crypto = require('crypto');
const fs = require('fs');

// License management
const LICENSE_FILE = path.join(app.getPath('userData'), 'license.dat');
const LICENSE_SERVER = 'https://api.guayabera-cad.com/v1';

// Test license keys for development
const TEST_KEYS = {
  'DEV0-0000-0000-0000': { valid: true, expires: 'never', hwid: 'any' },
  'TEST-1111-2222-3333': { valid: true, expires: '2025-12-31', hwid: 'localhost' },
  'EXPI-4444-5555-6666': { valid: false, expires: '2024-01-01', hwid: 'any' },
  'INVA-7777-8888-9999': { valid: false, expires: 'never', hwid: 'any' }
};

function getHardwareId() {
  // Generate a simple hardware ID based on machine info
  const machineInfo = [
    process.platform,
    process.arch,
    require('os').hostname(),
    require('os').totalmem()
  ].join('-');
  
  return crypto.createHash('sha256').update(machineInfo).digest('hex').substring(0, 16);
}

function saveLicense(licenseData) {
  const encrypted = crypto.createCipher('aes-256-cbc', getHardwareId());
  let encryptedData = encrypted.update(JSON.stringify(licenseData), 'utf8', 'hex');
  encryptedData += encrypted.final('hex');
  fs.writeFileSync(LICENSE_FILE, encryptedData);
}

function loadLicense() {
  try {
    if (!fs.existsSync(LICENSE_FILE)) {
      return null;
    }
    
    const encryptedData = fs.readFileSync(LICENSE_FILE, 'utf8');
    const decrypted = crypto.createDecipher('aes-256-cbc', getHardwareId());
    let decryptedData = decrypted.update(encryptedData, 'hex', 'utf8');
    decryptedData += decrypted.final('utf8');
    
    return JSON.parse(decryptedData);
  } catch (error) {
    console.error('Error loading license:', error);
    return null;
  }
}

async function validateLicense(key) {
  // Check test keys first
  if (TEST_KEYS[key]) {
    const testKey = TEST_KEYS[key];
    return {
      valid: testKey.valid,
      expires: testKey.expires,
      token: `test-${key}`,
      isTest: true
    };
  }
  
  // For production, validate with server
  try {
    const response = await fetch(`${LICENSE_SERVER}/activate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        key: key,
        hardware_id: getHardwareId()
      })
    });
    
    if (response.ok) {
      const data = await response.json();
      return {
        valid: true,
        expires: data.expires_at,
        token: data.token,
        isTest: false
      };
    }
    
    return { valid: false, error: 'Invalid license key' };
  } catch (error) {
    // Offline mode - allow if we have a valid cached license
    const cached = loadLicense();
    if (cached && cached.valid && cached.isTest) {
      return cached;
    }
    
    return { valid: false, error: 'Offline validation failed' };
  }
}

// IPC Handlers
ipcMain.handle('validate-license', async (event, key) => {
  return await validateLicense(key);
});

ipcMain.handle('save-license', (event, licenseData) => {
  saveLicense(licenseData);
  return { success: true };
});

ipcMain.handle('load-license', () => {
  return loadLicense();
});

ipcMain.handle('export-dxf', async (event, pieces) => {
  const { exportToDXF } = require('./src/utils/dxf-exporter');
  
  const result = await dialog.showSaveDialog({
    title: 'Export DXF File',
    filters: [{ name: 'DXF Files', extensions: ['dxf'] }]
  });
  
  if (!result.canceled && result.filePath) {
    exportToDXF(result.filePath, pieces);
    return { success: true, path: result.filePath };
  }
  
  return { success: false, error: 'Export cancelled' };
});

ipcMain.handle('save-piece', (event, piece) => {
  const dataDir = path.join(app.getPath('userData'), 'library');
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }
  
  const fileName = `${piece.id}.json`;
  const filePath = path.join(dataDir, fileName);
  fs.writeFileSync(filePath, JSON.stringify(piece, null, 2));
  
  return { success: true, path: filePath };
});

ipcMain.handle('load-pieces', () => {
  const dataDir = path.join(app.getPath('userData'), 'library');
  if (!fs.existsSync(dataDir)) {
    return [];
  }
  
  const files = fs.readdirSync(dataDir).filter(f => f.endsWith('.json'));
  return files.map(file => {
    const content = fs.readFileSync(path.join(dataDir, file), 'utf8');
    return JSON.parse(content);
  });
});

// Window creation
function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    icon: path.join(__dirname, 'public', 'icon.png')
  });

  mainWindow.loadFile('src/index.html');
  
  // In development mode, open DevTools
  if (process.argv.includes('--dev')) {
    mainWindow.webContents.openDevTools();
  }
  
  // Check license on startup
  const license = loadLicense();
  if (!license || !license.valid) {
    mainWindow.webContents.send('license-required');
  }
}

app.whenReady().then(() => {
  createWindow();
  
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
