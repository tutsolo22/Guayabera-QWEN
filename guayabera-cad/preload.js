const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('guayaberaAPI', {
  // License management
  validateLicense: (key) => ipcRenderer.invoke('validate-license', key),
  saveLicense: (licenseData) => ipcRenderer.invoke('save-license', licenseData),
  loadLicense: () => ipcRenderer.invoke('load-license'),
  
  // Piece management
  savePiece: (piece) => ipcRenderer.invoke('save-piece', piece),
  loadPieces: () => ipcRenderer.invoke('load-pieces'),
  
  // Export
  exportDXF: (pieces) => ipcRenderer.invoke('export-dxf', pieces),
  
  // Listen for license events
  onLicenseRequired: (callback) => {
    ipcRenderer.on('license-required', callback);
  }
});
