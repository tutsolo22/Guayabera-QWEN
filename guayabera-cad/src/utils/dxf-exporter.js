// dxf-exporter.js - Export pieces to DXF format for cutting machines

const fs = require('fs');

function exportToDXF(filePath, pieces) {
  let dxfContent = generateDXFHeader();
  
  // Add pieces as POLYLINE entities
  pieces.forEach((piece, index) => {
    dxfContent += generatePieceDXF(piece, index);
  });
  
  dxfContent += generateDXFFooter();
  
  fs.writeFileSync(filePath, dxfContent, 'utf8');
  return { success: true, path: filePath };
}

function generateDXFHeader() {
  return `  0
SECTION
  2
HEADER
  9
$ACADVER
  1
AC1015
  9
$EXTMIN
 10
0.0
 20
0.0
 30
0.0
  9
$EXTMAX
 10
10000.0
 20
10000.0
 30
0.0
ENDSEC
  0
SECTION
  2
TABLES
  0
TABLE
  2
LTYPE
  70
1
  0
LTYPE
  5
24
  2
CONTINUOUS
 70
64
  3

 72
65
 73
0
 40
0.0
ENDTAB
  0
TABLE
  2
LAYER
 70
5
  0
LAYER
  5
25
  2
FRENTE
 70
64
 62
7
  6
CONTINUOUS
  0
LAYER
  5
26
  2
ESPALDA
 70
64
 62
4
  6
CONTINUOUS
  0
LAYER
  5
27
  2
MANGA
 70
64
 62
1
  6
CONTINUOUS
  0
LAYER
  5
28
  2
CUELLO
 70
64
 62
3
  6
CONTINUOUS
ENDTAB
ENDSEC
  0
SECTION
  2
ENTITIES
`;
}

function generatePieceDXF(piece, index) {
  const layerName = piece.type.toUpperCase();
  const widthPx = piece.widthCm * 37.8; // Convert cm to pixels
  const heightPx = piece.heightCm * 37.8;
  
  // Determine layer color
  let colorCode = 7; // Default (white)
  switch (piece.type) {
    case 'frente':
    case 'FRENTE':
      colorCode = 5; // Blue
      break;
    case 'espalda':
    case 'ESPALDA':
      colorCode = 4; // Cyan
      break;
    case 'manga':
    case 'MANGA':
      colorCode = 1; // Red
      break;
    case 'cuello':
    case 'CUELLO':
      colorCode = 3; // Green
      break;
  }
  
  // Create rectangle as polyline
  let content = `  0
POLYLINE
  5
${100 + index}
  8
${layerName}
 66
1
 70
9
`;

  // Add vertices (closed rectangle)
  const vertices = [
    [0, 0],
    [widthPx, 0],
    [widthPx, heightPx],
    [0, heightPx],
    [0, 0] // Close the polyline
  ];
  
  vertices.forEach((vertex, vIndex) => {
    content += `  0
VERTEX
  5
${200 + (index * 10) + vIndex}
  8
${layerName}
 10
${vertex[0].toFixed(2)}
 20
${vertex[1].toFixed(2)}
 30
0.0
`;
  });
  
  // Close polyline
  content += `  0
SEQEND
  5
${300 + index}
  8
${layerName}
`;

  // Add text label with piece info
  content += `  0
TEXT
  5
${400 + index}
  8
${layerName}
 10
${(widthPx / 2).toFixed(2)}
 20
${(heightPx / 2).toFixed(2)}
 30
0.0
 40
${14 * 37.8 / 10} // Text height
  1
${piece.type.toUpperCase()} ${piece.widthCm.toFixed(1)}x${piece.heightCm.toFixed(1)}cm
`;

  return content;
}

function generateDXFFooter() {
  return `ENDSEC
  0
SECTION
  2
OBJECTS
  0
DICTIONARY
  5
C
100
AcDbDictionary
281
0
ENDSEC
  0
EOF
`;
}

module.exports = { exportToDXF };
