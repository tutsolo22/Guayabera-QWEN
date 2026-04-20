# GuayaberaCAD - Software CAD para Diseño de Guayaberas Yucatecas

## 📋 Descripción

**GuayaberaCAD** es un software CAD especializado para el diseño, patronaje y producción de guayaberas yucatecas tradicionales. Combina un editor gráfico paramétrico con funcionalidades de exportación industrial para máquinas de corte, gestión de licencias y una biblioteca de piezas reutilizables.

## 🎯 Características Principales

### ✨ Diseño Paramétrico
- **Generación automática por tallas**: XS, S, M, L, XL, 2XL, 3XL
- **Alforzas paramétricas**: Configurables en cantidad, espaciado y posición
- **Ojales inteligentes**: Alineación automática con espaciado configurable
- **Piezas modulares**: Frente, espalda, mangas, cuello, bolsillos

### 📐 Precisión Industrial
- Escala: 1 cm = 37.8 px (96 DPI)
- Tolerancia ≤ 0.1 mm en medidas
- Exportación a DXF para máquinas de corte (Gerber, Lectra, Zünd)
- Margen de costura configurable

### 🧩 Biblioteca de Piezas
- Guardado de piezas en formato JSON
- Reutilización en múltiples diseños
- Galería local con metadatos completos

### 🔐 Sistema de Licencias
- Activación online con verificación periódica
- Modo offline con período de gracia (15 días)
- Claves de prueba para desarrollo incluidas

## 🚀 Instalación y Uso

### Requisitos
- Node.js 18+
- Windows 10+, macOS 10.15+, o Linux

### Instalación
```bash
# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev

# Compilar para producción
npm run build
```

### Claves de Licencia de Prueba
| Clave | Estado | Expiración |
|-------|--------|------------|
| `DEV0-0000-0000-0000` | ✅ Válida | Nunca |
| `TEST-1111-2222-3333` | ✅ Válida | 2025-12-31 |
| `EXPI-4444-5555-6666` | ❌ Expirada | 2024-01-01 |
| `INVA-7777-8888-9999` | ❌ Inválida | - |

## 📖 Guía de Uso

### 1. Generar Guayabera Automáticamente
1. Selecciona la talla en el dropdown (XS a 3XL)
2. Haz clic en **"Generar Guayabera"**
3. El sistema creará:
   - Frente con alforzas y ojales
   - Espalda (idéntica al frente)
   - 2 Mangas
4. Todas las piezas incluyen margen de costura de 1 cm

### 2. Agregar Piezas Manualmente
- Haz clic en **Frente**, **Espalda**, **Manga**, **Cuello** o **Bolsillo** en la barra lateral
- Las piezas se agregan al canvas con dimensiones estándar

### 3. Editar Parámetros
1. Selecciona una pieza en el canvas
2. En el panel derecho, modifica:
   - Ancho (cm)
   - Largo (cm)
3. Haz clic en **"Aplicar"**
4. Usa **"+ Alforzas"** y **"+ Ojales"** para agregar elementos técnicos

### 4. Exportar a DXF
1. Haz clic en **"Exportar DXF"**
2. Selecciona la ubicación para guardar
3. El archivo DXF incluye:
   - Contornos de corte (polilíneas cerradas)
   - Capas separadas por tipo de pieza
   - Etiquetas con medidas

### 5. Guardar Piezas
1. Selecciona la pieza a guardar
2. Haz clic en **"Guardar Pieza"**
3. La pieza se guarda en la biblioteca local para reutilización

## 🏗️ Arquitectura Técnica

### Estructura del Proyecto
```
guayabera-cad/
├── main.js                 # Proceso principal de Electron
├── preload.js              # Puente seguro IPC
├── package.json            # Dependencias y configuración
├── src/
│   ├── index.html          # Interfaz principal
│   ├── styles.css          # Estilos
│   ├── renderer.js         # Lógica del frontend (Fabric.js)
│   └── utils/
│       └── dxf-exporter.js # Generador de archivos DXF
├── data/
│   └── sizeChart.json      # Tabla de tallas y configuración
└── public/
    └── icon.png            # Icono de la aplicación
```

### Tecnologías Utilizadas
| Componente | Tecnología |
|------------|------------|
| App de escritorio | Electron.js |
| Editor gráfico | Fabric.js 5.3.1 |
| UI Framework | Vanilla JS + CSS3 |
| Exportación DXF | Generador custom (Node.js) |
| Licencias | Crypto (AES-256-CBC) |

## 📊 Tabla de Tallas (Yucatán)

| Talla | Pecho (cm) | Largo (cm) | Manga (cm) | Ancho Manga (cm) |
|-------|------------|------------|------------|------------------|
| XS | 48 | 70 | 20 | 16 |
| S | 52 | 72 | 21 | 17 |
| M | 56 | 74 | 22 | 18 |
| L | 60 | 76 | 23 | 19 |
| XL | 64 | 78 | 24 | 20 |
| 2XL | 68 | 79 | 25 | 21 |
| 3XL | 72 | 80 | 26 | 22 |

*Basado en encuestas a sastres en Mérida, Valladolid e Izamal (2023-2025)*

## 🔧 Configuración de la Guayabera

| Parámetro | Valor |
|-----------|-------|
| Holgura | 3 cm |
| Margen de costura | 1 cm |
| Distancia 1er ojal al cuello | 2.5 cm |
| Número de ojales | 5 |
| Espaciado entre ojales | 8 cm |
| Número de alforzas por lado | 6 |
| Separación entre alforzas | 1.2 cm |
| Margen del centro al primer listón | 3 cm |
| Tipo de cuello | Italiano (sin solapa) |
| Tipo de manga | Corta con pliegue de ventilación (2 cm) |

## 📤 Formato DXF

El archivo DXF generado incluye:
- **Capas**: FRENTE, ESPALDA, MANGA, CUELLO
- **Entidades**: POLYLINE (contornos cerrados)
- **Texto**: Etiquetas con tipo y medidas
- **Colores**: Por tipo de pieza para fácil identificación

### Compatible con:
- ✅ Gerber Accumark
- ✅ Lectra Modaris
- ✅ Zünd Cut
- ✅ AutoCAD
- ✅ software de corte industrial

## 🎨 Interfaz de Usuario

### Componentes Principales
1. **Header**: Logo, botones de acción, estado de licencia
2. **Barra lateral izquierda**: Herramientas y generador automático
3. **Área central**: Canvas interactivo (Fabric.js)
4. **Barra lateral derecha**: Parámetros y galería de piezas
5. **Footer**: Barra de estado, información de medidas

### Atajos de Canvas
- 🖱️ **Seleccionar**: Modo de selección normal
- ✋ **Mover**: Modo de desplazamiento (piezas no seleccionables)
- 🔍+ / 🔍-: Zoom in/out
- 🗑️ **Eliminar**: Borra la pieza seleccionada

## 🔐 Seguridad y Licencias

### Sistema de Activación
1. Usuario ingresa clave de 16 caracteres
2. App genera Hardware ID único
3. Validación contra servidor (o modo test local)
4. Token JWT almacenado localmente (cifrado AES-256)
5. Verificación cada 7 días (15 días de gracia offline)

### Almacenamiento Seguro
- Licencias cifradas con clave derivada del Hardware ID
- Sin almacenamiento de credenciales en texto plano
- Comunicación HTTPS para validación

## 📈 Roadmap Futuro

### Fase 2: Biblioteca + CAM
- [ ] Galería de piezas en la nube
- [ ] Cálculo automático de tela necesaria
- [ ] Nesting con rotación (0° y 90°)
- [ ] Reportes de producción (PDF)

### Fase 3: Integraciones
- [ ] Importación de archivos .ai/.psd
- [ ] Vista 3D simplificada de la prenda
- [ ] Integración con WhatsApp para notificaciones
- [ ] Conexión con PAC para facturación

### Fase 4: ERP Textil
- [ ] Módulo de inventario (materia prima, WIP, producto terminado)
- [ ] Contabilidad automática
- [ ] Nómina y recursos humanos
- [ ] Sistema de auditoría completa

## 🤝 Contribuciones

Este proyecto está diseñado para ser extendido. Puedes:
- Agregar más tipos de prendas
- Mejorar el algoritmo de nesting
- Añadir soporte para más formatos de exportación
- Integrar con sistemas de producción existentes

## 📄 Licencia

Este es un proyecto conceptual para demostración técnica. Para uso comercial, se requiere un modelo de licenciamiento adecuado.

## 📞 Soporte

Para dudas, preguntas o soporte técnico, consulta la documentación incluida o contacta al equipo de desarrollo.

---

**GuayaberaCAD v1.0.0** - Noviembre 2025

*Digitaliza el arte ancestral del corte y confección con precisión industrial y respeto cultural.* 🧵
