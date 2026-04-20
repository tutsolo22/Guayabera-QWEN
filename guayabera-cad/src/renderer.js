// renderer.js - Main frontend logic for GuayaberaCAD

// Constants
const SCALE = 37.8; // 1 cm = 37.8 pixels (96 DPI)
const CM_TO_PX = SCALE;

// Size chart for Yucatecan Guayaberas
const SIZE_CHART = {
  XS: { pecho: 48, largo: 70, manga: 20, anchoManga: 16 },
  S: { pecho: 52, largo: 72, manga: 21, anchoManga: 17 },
  M: { pecho: 56, largo: 74, manga: 22, anchoManga: 18 },
  L: { pecho: 60, largo: 76, manga: 23, anchoManga: 19 },
  XL: { pecho: 64, largo: 78, manga: 24, anchoManga: 20 },
  '2XL': { pecho: 68, largo: 79, manga: 25, anchoManga: 21 },
  '3XL': { pecho: 72, largo: 80, manga: 26, anchoManga: 22 }
};

// Garment parameters
const GARMENT_CONFIG = {
  holgura: 3, // cm de holgura
  margenCostura: 1, // cm
  primerOjalCuello: 2.5, // cm
  numOjales: 5,
  espaciadoOjales: 8, // cm
  numAlforzas: 6,
  espaciadoAlforzas: 1.2, // cm
  margenCentro: 3 // cm del centro al primer listón
};

// Canvas setup
let canvas;
let currentPiece = null;
let pieces = [];

document.addEventListener('DOMContentLoaded', () => {
  // Initialize Fabric.js canvas
  canvas = new fabric.Canvas('fabric-canvas', {
    width: 1200,
    height: 800,
    backgroundColor: '#f8fafc',
    selection: true
  });

  // Setup event listeners
  setupEventListeners();
  
  // Check license
  checkLicense();
  
  // Update status
  updateStatus('Listo para diseñar');
});

function setupEventListeners() {
  // Tool buttons
  document.querySelectorAll('.tool-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const tool = btn.dataset.tool;
      handleToolClick(tool);
    });
  });

  // Canvas toolbar
  document.getElementById('btn-select').addEventListener('click', () => setToolMode('select'));
  document.getElementById('btn-move').addEventListener('click', () => setToolMode('move'));
  document.getElementById('btn-zoom-in').addEventListener('click', () => zoomCanvas(1.2));
  document.getElementById('btn-zoom-out').addEventListener('click', () => zoomCanvas(0.8));
  document.getElementById('btn-delete').addEventListener('click', deleteSelected);

  // Action buttons
  document.getElementById('btn-generate').addEventListener('click', generateGuayabera);
  document.getElementById('btn-new').addEventListener('click', newGarment);
  document.getElementById('btn-load').addEventListener('click', loadPiece);
  document.getElementById('btn-save').addEventListener('click', saveCurrentPiece);
  document.getElementById('btn-export').addEventListener('click', exportToDXF);

  // Canvas events
  canvas.on('selection:created', onPieceSelected);
  canvas.on('selection:updated', onPieceSelected);
  canvas.on('selection:cleared', onSelectionCleared);
  canvas.on('mouse:move', onMouseMove);
}

// License management
async function checkLicense() {
  const license = await window.guayaberaAPI.loadLicense();
  
  if (license && license.valid) {
    updateLicenseStatus(true);
  } else {
    showLicenseModal();
  }
}

function showLicenseModal() {
  document.getElementById('license-modal').classList.remove('hidden');
  
  document.getElementById('btn-activate').addEventListener('click', async () => {
    const key = document.getElementById('license-key').value.trim();
    const result = await window.guayaberaAPI.validateLicense(key);
    
    if (result.valid) {
      await window.guayaberaAPI.saveLicense(result);
      updateLicenseStatus(true);
      document.getElementById('license-modal').classList.add('hidden');
    } else {
      alert('❌ Licencia inválida o expirada');
    }
  });
}

function updateLicenseStatus(active) {
  const dot = document.querySelector('.status-dot');
  const text = document.querySelector('.status-text');
  
  if (active) {
    dot.classList.add('active');
    text.textContent = 'Licencia activa';
  } else {
    dot.classList.remove('active');
    text.textContent = 'Sin licencia';
  }
}

// Tool handling
function handleToolClick(tool) {
  switch (tool) {
    case 'frente':
      addBasicPiece('frente', 56, 74);
      break;
    case 'espalda':
      addBasicPiece('espalda', 56, 74);
      break;
    case 'manga':
      addBasicPiece('manga', 24, 22);
      break;
    case 'cuello':
      addBasicPiece('cuello', 40, 8);
      break;
    case 'bolsillo':
      addBasicPiece('bolsillo', 14, 16);
      break;
    case 'alforzas':
      if (currentPiece) {
        drawAlforzas(currentPiece);
      }
      break;
    case 'ojales':
      if (currentPiece) {
        drawOjales(currentPiece);
      }
      break;
  }
}

// Add basic piece
function addBasicPiece(type, widthCm, heightCm) {
  const widthPx = widthCm * CM_TO_PX;
  const heightPx = heightCm * CM_TO_PX;
  
  const rect = new fabric.Rect({
    left: 100 + (pieces.length * 50),
    top: 100 + (pieces.length * 50),
    width: widthPx,
    height: heightPx,
    fill: '#dbeafe',
    stroke: '#2563eb',
    strokeWidth: 2,
    selectable: true,
    hasControls: true,
    pieceType: type,
    pieceData: {
      type: type,
      widthCm: widthCm,
      heightCm: heightCm,
      widthPx: widthPx,
      heightPx: heightPx
    }
  });
  
  // Add label
  const label = new fabric.Text(`${type.toUpperCase()}`, {
    left: 100 + (pieces.length * 50) + 10,
    top: 100 + (pieces.length * 50) + 10,
    fontSize: 16,
    fill: '#1e40af',
    selectable: false,
    pieceType: 'label'
  });
  
  canvas.add(rect);
  canvas.add(label);
  canvas.setActiveObject(rect);
  
  pieces.push({ type, rect, label });
  updatePiecesCount();
  updateStatus(`Pieza "${type}" agregada: ${widthCm} × ${heightCm} cm`);
}

// Draw alforzas (pleats)
function drawAlforzas(piece) {
  const data = piece.pieceData || piece.get('pieceData');
  if (!data) return;
  
  const { widthPx, widthCm } = data;
  const startX = (widthPx / 2) + (GARMENT_CONFIG.margenCentro * CM_TO_PX);
  const startY = 5 * CM_TO_PX;
  const alforzaLength = 25 * CM_TO_PX;
  const spacing = GARMENT_CONFIG.espaciadoAlforzas * CM_TO_PX;
  const count = GARMENT_CONFIG.numAlforzas;
  
  // Clear existing alforzas
  canvas.getObjects().forEach(obj => {
    if (obj.pieceType === 'alforza') {
      canvas.remove(obj);
    }
  });
  
  // Draw alforzas
  for (let i = 0; i < count; i++) {
    const line = new fabric.Line([
      startX + (i * spacing),
      startY,
      startX + (i * spacing),
      startY + alforzaLength
    ], {
      stroke: '#10b981',
      strokeWidth: 2,
      selectable: false,
      pieceType: 'alforza'
    });
    
    canvas.add(line);
  }
  
  updateStatus(`${count} alforzas dibujadas a ${GARMENT_CONFIG.espaciadoAlforzas} cm de separación`);
}

// Draw ojales (buttonholes)
function drawOjales(piece) {
  const data = piece.pieceData || piece.get('pieceData');
  if (!data) return;
  
  const { widthPx } = data;
  const centerX = widthPx / 2;
  const startY = GARMENT_CONFIG.primerOjalCuello * CM_TO_PX;
  const spacing = GARMENT_CONFIG.espaciadoOjales * CM_TO_PX;
  const count = GARMENT_CONFIG.numOjales;
  const ojalRadius = 0.3 * CM_TO_PX; // 3mm
  
  // Clear existing ojales
  canvas.getObjects().forEach(obj => {
    if (obj.pieceType === 'ojal') {
      canvas.remove(obj);
    }
  });
  
  // Draw ojales
  for (let i = 0; i < count; i++) {
    const circle = new fabric.Circle({
      left: centerX - ojalRadius,
      top: startY + (i * spacing),
      radius: ojalRadius,
      fill: '#ef4444',
      stroke: '#dc2626',
      strokeWidth: 1,
      selectable: false,
      pieceType: 'ojal'
    });
    
    canvas.add(circle);
  }
  
  updateStatus(`${count} ojales dibujados comenzando a ${GARMENT_CONFIG.primerOjalCuello} cm del cuello`);
}

// Generate complete guayabera by size
function generateGuayabera() {
  const selectedSize = document.getElementById('size-select').value;
  const sizeData = SIZE_CHART[selectedSize];
  
  if (!sizeData) {
    alert('Talla no válida');
    return;
  }
  
  // Clear canvas
  canvas.clear();
  canvas.backgroundColor = '#f8fafc';
  pieces = [];
  
  // Calculate dimensions
  const frenteWidth = (sizeData.pecho / 2) + GARMENT_CONFIG.holgura + (2 * GARMENT_CONFIG.margenCostura);
  const frenteHeight = sizeData.largo + (2 * GARMENT_CONFIG.margenCostura);
  const mangaWidth = sizeData.anchoManga + (2 * GARMENT_CONFIG.margenCostura);
  const mangaHeight = sizeData.manga + GARMENT_CONFIG.margenCostura;
  
  // Add frente
  const frente = new fabric.Rect({
    left: 100,
    top: 50,
    width: frenteWidth * CM_TO_PX,
    height: frenteHeight * CM_TO_PX,
    fill: '#dbeafe',
    stroke: '#2563eb',
    strokeWidth: 2,
    selectable: true,
    pieceType: 'frente',
    pieceData: {
      type: 'frente',
      widthCm: frenteWidth,
      heightCm: frenteHeight,
      widthPx: frenteWidth * CM_TO_PX,
      heightPx: frenteHeight * CM_TO_PX
    }
  });
  
  // Add espalda (same as frente)
  const espalda = new fabric.Rect({
    left: 100 + (frenteWidth * CM_TO_PX) + 50,
    top: 50,
    width: frenteWidth * CM_TO_PX,
    height: frenteHeight * CM_TO_PX,
    fill: '#dbeafe',
    stroke: '#2563eb',
    strokeWidth: 2,
    selectable: true,
    pieceType: 'espalda',
    pieceData: {
      type: 'espalda',
      widthCm: frenteWidth,
      heightCm: frenteHeight,
      widthPx: frenteWidth * CM_TO_PX,
      heightPx: frenteHeight * CM_TO_PX
    }
  });
  
  // Add mangas
  const manga1 = new fabric.Rect({
    left: 100,
    top: 50 + (frenteHeight * CM_TO_PX) + 30,
    width: mangaWidth * CM_TO_PX,
    height: mangaHeight * CM_TO_PX,
    fill: '#fef3c7',
    stroke: '#f59e0b',
    strokeWidth: 2,
    selectable: true,
    pieceType: 'manga',
    pieceData: {
      type: 'manga',
      widthCm: mangaWidth,
      heightCm: mangaHeight,
      widthPx: mangaWidth * CM_TO_PX,
      heightPx: mangaHeight * CM_TO_PX
    }
  });
  
  const manga2 = new fabric.Rect({
    left: 100 + (mangaWidth * CM_TO_PX) + 30,
    top: 50 + (frenteHeight * CM_TO_PX) + 30,
    width: mangaWidth * CM_TO_PX,
    height: mangaHeight * CM_TO_PX,
    fill: '#fef3c7',
    stroke: '#f59e0b',
    strokeWidth: 2,
    selectable: true,
    pieceType: 'manga',
    pieceData: {
      type: 'manga',
      widthCm: mangaWidth,
      heightCm: mangaHeight,
      widthPx: mangaWidth * CM_TO_PX,
      heightPx: mangaHeight * CM_TO_PX
    }
  });
  
  canvas.add(frente, espalda, manga1, manga2);
  
  // Add alforzas to frente
  drawAlforzas(frente);
  
  // Add ojales to frente
  drawOjales(frente);
  
  // Add labels
  const label1 = new fabric.Text(`FRENTE - ${selectedSize}`, {
    left: 110,
    top: 60,
    fontSize: 14,
    fill: '#1e40af',
    selectable: false
  });
  
  const label2 = new fabric.Text(`ESPALDA - ${selectedSize}`, {
    left: 110 + (frenteWidth * CM_TO_PX) + 50,
    top: 60,
    fontSize: 14,
    fill: '#1e40af',
    selectable: false
  });
  
  canvas.add(label1, label2);
  
  pieces = [
    { type: 'frente', rect: frente },
    { type: 'espalda', rect: espalda },
    { type: 'manga', rect: manga1 },
    { type: 'manga', rect: manga2 }
  ];
  
  canvas.renderAll();
  updatePiecesCount();
  updateStatus(`Guayabera ${selectedSize} generada: ${frenteWidth}×${frenteHeight} cm (frente/espalda), ${mangaWidth}×${mangaHeight} cm (mangas)`);
}

// Selection handling
function onPieceSelected(e) {
  const selected = e.selected[0];
  if (selected && selected.pieceType && selected.pieceType !== 'label') {
    currentPiece = selected;
    showParameterPanel(selected);
  }
}

function onSelectionCleared() {
  currentPiece = null;
  hideParameterPanel();
}

function onMouseMove(e) {
  const pointer = canvas.getPointer(e.e);
  document.getElementById('cursor-position').textContent = 
    `X: ${Math.round(pointer.x)}, Y: ${Math.round(pointer.y)}`;
}

// Parameter panel
function showParameterPanel(piece) {
  const data = piece.pieceData || piece.get('pieceData');
  if (!data) return;
  
  const panel = document.getElementById('params-content');
  panel.innerHTML = `
    <div class="param-group">
      <h4>${data.type.toUpperCase()}</h4>
      <label>Tipo:</label>
      <input type="text" value="${data.type}" disabled>
    </div>
    <div class="param-group">
      <label>Ancho (cm):</label>
      <input type="number" id="param-width" value="${data.widthCm.toFixed(1)}" step="0.1">
    </div>
    <div class="param-group">
      <label>Largo (cm):</label>
      <input type="number" id="param-height" value="${data.heightCm.toFixed(1)}" step="0.1">
    </div>
    <div class="param-group">
      <button id="btn-apply-params" class="btn btn-primary full-width">Aplicar</button>
      <button id="btn-add-alforzas" class="btn btn-secondary full-width" style="margin-top: 8px;">+ Alforzas</button>
      <button id="btn-add-ojales" class="btn btn-secondary full-width" style="margin-top: 8px;">+ Ojales</button>
    </div>
  `;
  
  document.getElementById('btn-apply-params').addEventListener('click', () => {
    const newWidth = parseFloat(document.getElementById('param-width').value);
    const newHeight = parseFloat(document.getElementById('param-height').value);
    
    piece.set({
      width: newWidth * CM_TO_PX,
      height: newHeight * CM_TO_PX,
      pieceData: {
        ...data,
        widthCm: newWidth,
        heightCm: newHeight,
        widthPx: newWidth * CM_TO_PX,
        heightPx: newHeight * CM_TO_PX
      }
    });
    
    canvas.renderAll();
    updateStatus(`Pieza actualizada: ${newWidth} × ${newHeight} cm`);
  });
  
  document.getElementById('btn-add-alforzas').addEventListener('click', () => {
    drawAlforzas(piece);
  });
  
  document.getElementById('btn-add-ojales').addEventListener('click', () => {
    drawOjales(piece);
  });
}

function hideParameterPanel() {
  document.getElementById('params-content').innerHTML = 
    '<p class="no-selection">Selecciona una pieza para editar sus parámetros</p>';
}

// Canvas tools
function setToolMode(mode) {
  document.querySelectorAll('.canvas-btn').forEach(btn => btn.classList.remove('active'));
  
  if (mode === 'select') {
    canvas.selection = true;
    canvas.forEachObject(obj => {
      if (obj.pieceType !== 'label') {
        obj.selectable = true;
      }
    });
    document.getElementById('btn-select').classList.add('active');
  } else if (mode === 'move') {
    canvas.selection = false;
    canvas.forEachObject(obj => obj.selectable = false);
    document.getElementById('btn-move').classList.add('active');
  }
}

function zoomCanvas(factor) {
  const currentZoom = canvas.getZoom();
  const newZoom = currentZoom * factor;
  canvas.setZoom(newZoom);
  canvas.renderAll();
  document.getElementById('zoom-display').textContent = `${Math.round(newZoom * 100)}%`;
}

function deleteSelected() {
  const activeObjects = canvas.getActiveObjects();
  if (activeObjects.length) {
    canvas.discardActiveObject();
    activeObjects.forEach(obj => {
      canvas.remove(obj);
      pieces = pieces.filter(p => p.rect !== obj && p.label !== obj);
    });
    updatePiecesCount();
    updateStatus('Pieza eliminada');
  }
}

// Piece management
function newGarment() {
  if (confirm('¿Crear nueva prenda? Se perderán los cambios no guardados.')) {
    canvas.clear();
    canvas.backgroundColor = '#f8fafc';
    pieces = [];
    currentPiece = null;
    updatePiecesCount();
    updateStatus('Nueva prenda creada');
  }
}

async function saveCurrentPiece() {
  if (!currentPiece) {
    alert('Selecciona una pieza para guardar');
    return;
  }
  
  const data = currentPiece.pieceData || currentPiece.get('pieceData');
  const pieceData = {
    id: `piece-${Date.now()}`,
    name: `${data.type}-${Date.now()}`,
    type: data.type,
    widthCm: data.widthCm,
    heightCm: data.heightCm,
    createdAt: new Date().toISOString(),
    parameters: {
      alforzas: GARMENT_CONFIG.numAlforzas,
      ojales: GARMENT_CONFIG.numOjales,
      margenCostura: GARMENT_CONFIG.margenCostura
    }
  };
  
  const result = await window.guayaberaAPI.savePiece(pieceData);
  if (result.success) {
    updateStatus(`Pieza guardada: ${pieceData.name}`);
  }
}

async function loadPiece() {
  const libraryPieces = await window.guayaberaAPI.loadPieces();
  
  if (libraryPieces.length === 0) {
    alert('No hay piezas guardadas');
    return;
  }
  
  // For now, load the first piece (in production, show a dialog)
  const piece = libraryPieces[0];
  addBasicPiece(piece.type, piece.widthCm, piece.heightCm);
  updateStatus(`Pieza cargada: ${piece.name}`);
}

async function exportToDXF() {
  const cutPieces = pieces.map(p => ({
    type: p.type,
    widthCm: p.rect.pieceData.widthCm,
    heightCm: p.rect.pieceData.heightCm
  }));
  
  const result = await window.guayaberaAPI.exportDXF(cutPieces);
  if (result.success) {
    updateStatus(`DXF exportado: ${result.path}`);
  } else {
    updateStatus('Exportación cancelada');
  }
}

// Utility functions
function updateStatus(message) {
  document.getElementById('status-message').textContent = message;
}

function updatePiecesCount() {
  document.getElementById('total-pieces').textContent = `Piezas: ${pieces.length}`;
}

// Calculate optimal alforza count based on width
function calculateAlforzaCount(widthCm, spacingCm = 1.2, marginFromCenter = 3, maxAlforzas = 8) {
  const availableWidth = (widthCm / 2) - marginFromCenter;
  const count = Math.floor(availableWidth / spacingCm);
  return Math.min(count, maxAlforzas);
}

// Nesting with rotation
function simpleNestingWithRotation(pieces, fabricWidthCm = 150) {
  // Sort by area (descending)
  const sorted = [...pieces].sort((a, b) => (b.width * b.height) - (a.width * a.height));
  
  const placed = [];
  let currentY = 0;
  let currentX = 0;
  let rowHeight = 0;
  
  sorted.forEach(piece => {
    // Try both orientations
    const option1 = { width: piece.width, height: piece.height, rotation: 0 };
    const option2 = { width: piece.height, height: piece.width, rotation: 90 };
    
    // Choose orientation that fits best in current row
    let chosen = option1;
    if (currentX + option2.width <= fabricWidthCm && option2.height < rowHeight) {
      chosen = option2;
    }
    
    // Check if it fits in current row
    if (currentX + chosen.width > fabricWidthCm) {
      // New row
      currentY += rowHeight;
      currentX = 0;
      rowHeight = 0;
    }
    
    placed.push({
      type: piece.type,
      x: currentX,
      y: currentY,
      width: chosen.width,
      height: chosen.height,
      rotation: chosen.rotation
    });
    
    currentX += chosen.width;
    rowHeight = Math.max(rowHeight, chosen.height);
  });
  
  const totalHeight = currentY + rowHeight;
  const totalArea = fabricWidthCm * totalHeight;
  const piecesArea = pieces.reduce((sum, p) => sum + (p.width * p.height), 0);
  const waste = ((totalArea - piecesArea) / totalArea) * 100;
  
  return {
    placed,
    totalHeightCm: totalHeight,
    totalAreaCm2: totalArea,
    wastePercent: waste
  };
}

// Expose functions to window for testing
window.GuayaberaCAD = {
  calculateAlforzaCount,
  simpleNestingWithRotation,
  SIZE_CHART,
  GARMENT_CONFIG,
  SCALE
};
