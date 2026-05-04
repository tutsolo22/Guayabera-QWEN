# Frontend - Guayabera ERP

## Descripción

Este es el componente frontend de la suite Guayabera ERP, un sistema integral de planificación de recursos empresariales con una identidad visual profesional y moderna.

## Identidad Visual

La interfaz de usuario sigue los principios de la identidad visual del proyecto Guayabera ERP, que combina:

- **Profesionalismo**: Interfaces limpias y organizadas que facilitan la toma de decisiones empresariales
- **Modernidad**: Diseño contemporáneo con elementos visuales claros y jerarquía visual bien definida
- **Adaptabilidad**: Responsive design que funciona en múltiples dispositivos y contextos
- **Escalabilidad**: Sistema de componentes modulares que permite extender la interfaz fácilmente

## Paleta de Colores

### Colores Primarios:
- **Azul Profundo (#1B365D)**: Usado para encabezados y elementos de navegación
- **Verde Empresarial (#2E8B57)**: Usado para indicadores de éxito y validaciones
- **Gris Noble (#F5F7FA)**: Color de fondo principal

### Colores Secundarios:
- **Naranja Destaque (#FF8C42)**: Para botones primarios y llamadas a la acción
- **Verde Energía (#4A9B3F)**: Indicadores positivos y validaciones
- **Rojo Alerta (#DC3545)**: Errores, alertas y elementos críticos
- **Amarillo Destaque (#F4D03F)**: Notificaciones y elementos de atención media

## Estructura de Archivos

- `/public`: Archivos públicos y recursos estáticos
- `/src`: Código fuente del frontend
  - `/components`: Componentes reutilizables
  - `/services`: Servicios de comunicación con el backend
  - `/store`: Almacenamiento de estado global (si aplica)
  - `/styles`: Archivos de estilos CSS
    - `variables.css`: Variables de diseño con la paleta de colores
    - `index.css`: Estilos base y componentes visuales

## Instalación

1. Asegúrate de tener Node.js instalado en tu sistema
2. Instala las dependencias:
```bash
npm install
```
3. Inicia el servidor de desarrollo:
```bash
npm start
```

## Contribución

Cuando contribuyas al frontend, por favor:

1. Sigue la identidad visual definida en la paleta de colores
2. Usa las variables CSS definidas en `variables.css`
3. Mantén la coherencia visual con los componentes existentes
4. Asegúrate de que los nuevos componentes sean responsive
5. Documenta nuevos componentes visuales en este README

## Licencia

Este proyecto forma parte de Guayabera ERP Suite y se distribuye bajo la licencia MIT.

# 🎨 GuayaberaERP Frontend - React + Ant Design

## 🚀 Inicio Rápido

### Instalar dependencias
```bash
cd frontend
npm install
```

### Ejecutar en modo desarrollo
```bash
npm start
```

La aplicación se abrirá en http://localhost:3000

### Compilar para producción
```bash
npm run build
```

---

## 📦 Tecnologías Utilizadas

- **React 18** - Framework UI
- **TypeScript** - Tipado estático
- **Ant Design 5** - Componentes UI profesionales
- **Redux Toolkit** - Estado global
- **RTK Query** - Gestión de APIs
- **React Router 6** - Enrutamiento

---

## 🗂️ Estructura de Carpetas

```
frontend/src/
├── components/
│   ├── layouts/
│   │   └── MainLayout.tsx          # Layout principal con sidebar
│   └── pages/
│       ├── auth/
│       │   └── LoginPage.tsx       # Login
│       ├── admin/
│       │   └── EmpresaPage.tsx     # Configuración empresa
│       ├── finance/
│       │   ├── CuentasPage.tsx     # Catálogo de cuentas
│       │   ├── PolizasPage.tsx     # Pólizas contables
│       │   ├── BancosPage.tsx      # Bancos
│       │   ├── BalanzaPage.tsx     # Balanza de comprobación
│       │   └── AsientosAutomaticosPage.tsx  # Asientos automáticos
│       └── DashboardPage.tsx       # Dashboard principal
├── services/
│   ├── api.ts                      # Configuración API base
│   ├── authApi.ts                  # API de autenticación
│   └── financeApi.ts               # API de contabilidad
├── store/
│   ├── index.ts                    # Configuración Redux
│   └── features/
│       └── auth/
│           └── authSlice.ts        # Estado de autenticación
├── App.tsx                         # Componente principal con routing
├── index.tsx                       # Punto de entrada
└── index.css                       # Estilos globales
```

---

## 🔐 Autenticación

### Credenciales de prueba
```
Usuario: admin
Contraseña: admin123456
```

---

## 📄 Páginas Implementadas

### 1. **Login** (`/login`)
- Formulario de autenticación
- Validación de credenciales
- Redirección automática al dashboard

### 2. **Dashboard** (`/dashboard`)
- Estadísticas generales:
  - Total cuentas contables
  - Total pólizas
  - Total bancos
  - Asientos automáticos (24h)
- Estado de asientos automáticos
- Tabla de pólizas recientes

### 3. **Catálogo de Cuentas** (`/finance/cuentas`)
- Tabla con todas las cuentas
- Botón para importar catálogo SAT (115 cuentas)
- Modal para crear nuevas cuentas
- Filtros por tipo y nivel

### 4. **Pólizas Contables** (`/finance/polizas`)
- Listado de pólizas
- Crear pólizas con múltiples movimientos
- Validación de partida doble en tiempo real
- Vista detallada de póliza

### 5. **Bancos** (`/finance/bancos`)
- Listado de cuentas bancarias
- Estadísticas de saldos
- Crear nuevos bancos

### 6. **Balanza de Comprobación** (`/finance/balanza`)
- Selector de rango de fechas
- Tabla con saldos iniciales, cargos, abonos, finales
- Validación de cuadratura
- Totales automáticos

### 7. **Asientos Automáticos** (`/finance/asientos-automaticos`)
- Monitoreo de asientos automáticos
- Estadísticas por estado (procesado, pendiente, fallido)
- Métricas de últimas 24 horas

---

## 🔗 Conexión con Backend

El frontend se conecta al backend en `http://localhost:8000/api/v1`

### Proxy de desarrollo
En `package.json`:
```json
"proxy": "http://localhost:8000"
```

### Variables de entorno
Crear archivo `.env`:
```env
REACT_APP_API_URL=http://localhost:8000/api/v1
```

---

## 🎨 Temas y Estilos

### Tema principal (Ant Design)
```typescript
theme={{
  token: {
    colorPrimary: '#1890ff',
    borderRadius: 6,
  },
}}
```

### Estilos personalizados
Ver `index.css` para:
- Scrollbar personalizado
- Estilos de login
- Tarjetas de estadísticas
- Badges de estado

---

## 📊 Estado Global (Redux)

### Auth Slice
```typescript
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}
```

### RTK Query APIs
- `authApi` - Login, logout, register
- `financeApi` - Cuentas, pólizas, bancos, balanza, asientos

---

## 🚀 Despliegue

### Desarrollo
```bash
npm start
```

### Producción
```bash
npm run build
# Los archivos compilados estarán en frontend/build/
```

### Docker (desde guayabera-erp/)
```bash
docker-compose up -d frontend
```

---

## ✅ Checklist de Funcionalidades

- [x] Login con autenticación JWT
- [x] Layout con sidebar colapsable
- [x] Dashboard con estadísticas
- [x] Catálogo de cuentas con importación SAT
- [x] Crear pólizas con validación de partida doble
- [x] Gestión de bancos
- [x] Balanza de comprobación
- [x] Monitoreo de asientos automáticos
- [x] Routing protegido
- [x] Estado global con Redux
- [x] Integración con backend FastAPI

---

**GuayaberaERP Frontend v0.1.0** - Listo para usar 🎉
