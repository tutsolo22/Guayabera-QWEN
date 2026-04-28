# 🚀 Guía de Inicio Rápido - GuayaberaERP

## ⚡ Empezar en 5 Minutos

### 1. Prerrequisitos
- Docker y Docker Compose instalados
- Python 3.11+ (opcional, para desarrollo local)
- Node.js 18+ (opcional, para frontend)

### 2. Levantar el Proyecto

```bash
# Navegar al directorio del ERP
cd guayabera-erp

# Levantar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f backend

# Verificar que está corriendo
curl http://localhost:8000/health
```

### 3. Primeros Pasos

#### Crear Empresa Inicial
```bash
curl -X POST http://localhost:8000/api/v1/admin/empresas \
  -H "Content-Type: application/json" \
  -d '{
    "rfc": "GUA250101ABC",
    "nombre_fiscal": "Guayaberas Yucatecas SA de CV",
    "nombre_comercial": "GuayaberaCAD",
    "regimen_fiscal": "Régimen General de Ley",
    "calle": "Calle 60",
    "numero_exterior": "123",
    "colonia": "Centro",
    "ciudad": "Mérida",
    "estado": "Yucatán",
    "codigo_postal": "97000",
    "telefono": "999-123-4567",
    "email": "info@guayabera-cad.com"
  }'
```

#### Crear Usuario Admin
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@guayabera-cad.com",
    "password": "admin123456",
    "nombre": "Administrador",
    "apellidos": "Sistema"
  }'
```

#### Hacer Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123456"
  }'
```

### 4. Acceder a los Servicios

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| **API Backend** | http://localhost:8000 | - |
| **API Docs (Swagger)** | http://localhost:8000/docs | - |
| **API Docs (Redoc)** | http://localhost:8000/redoc | - |
| **GuayaberaCAD** | http://localhost:3001 | DEV0-0000-0000-0000 |
| **PgAdmin (BD)** | http://localhost:5050 | admin@guayabera-erp.com / admin123 |
| **Redis** | localhost:6379 | Sin contraseña |
| **PostgreSQL** | localhost:5432 | guayabera_user / guayabera_pass_2025 |

---

## 📦 Módulos del Sistema

Guayabera ERP cuenta con una arquitectura modular que permite adaptarse a las necesidades específicas de tu negocio. A continuación se detallan los módulos disponibles:

### 🧵 Producción
- MRP (Planificación de Requerimientos de Materiales)
- Control de calidad
- Gestión de órdenes de producción
- Análisis de Pareto
- Gráficos de control estadístico
- Gestión de recetas y formulas
- Seguimiento de lotes y caducidad

### 🛒 Ventas
- Gestión de clientes
- Catálogo de productos multivariante
- Precios por niveles de cliente
- Pedidos con anticipos
- Notas de crédito automáticas
- Cotizaciones y propuestas comerciales
- CRM integrado

### 📦 Inventario
- Gestión de almacenes
- Control de existencias
- Variaciones de productos
- Inventario físico
- Escaneo de códigos QR y barras
- Alertas de inventario mínimo/máximo

### 👥 Recursos Humanos
- Gestión de empleados
- Control de asistencia
- Nómina
- Evaluación de desempeño
- Capacitación y desarrollo
- Reclutamiento y selección

### 💰 Finanzas
- Contabilidad general
- Cuentas por pagar/cobrar
- Bancos y conciliación
- Facturación electrónica
- Presupuestación colaborativa
- Análisis de desviaciones
- Tesorería y flujo de efectivo

### 🛍️ Compras
- Gestión de proveedores
- Requisiciones y órdenes de compra
- Análisis de proveedores
- Recepción de mercancía
- Devoluciones a proveedores

### 🚚 Logística
- Gestión de almacenes
- Control de entradas/salidas
- Gestión de transporte
- Control de inventarios en tránsito
- Manejo de paquetería y guías

### 📊 Business Intelligence
- Dashboard ejecutivo
- Reportes personalizados
- KPIs personalizados
- Análisis predictivo
- Análisis de sensibilidad
- Exportación de datos a múltiples formatos

### 🎨 Diseño Asistido
- Gestión de diseños
- Tablas de tallas
- Hojas de ruta de producción
- Gestión de muestras y prototipos

---

## ⚙️ Funcionalidades Avanzadas

### 🤖 Inteligencia Artificial
- Asistente de IA con base de conocimientos
- Clasificación automática de transacciones
- Detección de fraudes
- Análisis predictivo de demanda
- Optimización de precios

### 🔐 Seguridad
- Auditoría de seguridad
- Control de versiones
- Encriptación de datos
- Firmas electrónicas
- Autenticación multifactor
- Políticas de retención de datos

### 🔗 Integraciones
- Facturación electrónica (Facturama, Timbrado SAT)
- Integración bancaria (Santander, BBVA, Banamex)
- Correos electrónicos (SMTP, SendGrid, Mailgun)
- Notificaciones en tiempo real (WebSocket, Push)
- API pública para integración con sistemas externos

---

## 📚 Endpoints Disponibles (Todos los módulos completos)

### Administración
```
POST   /api/v1/admin/empresas              # Crear empresa
GET    /api/v1/admin/empresas              # Listar empresas
GET    /api/v1/admin/empresas/{id}         # Obtener empresa
PUT    /api/v1/admin/empresas/{id}         # Actualizar empresa

POST   /api/v1/admin/sucursales            # Crear sucursal
GET    /api/v1/admin/empresas/{id}/sucursales  # Listar sucursales

GET    /api/v1/admin/configuracion         # Listar configuración
POST   /api/v1/admin/configuracion         # Crear/actualizar config
GET    /api/v1/admin/configuracion/{clave} # Obtinar config por clave

GET    /api/v1/admin/monedas               # Listar monedas
GET    /api/v1/admin/impuestos             # Listar impuestos
```

### Autenticación
```
POST   /api/v1/auth/login                  # Login
POST   /api/v1/auth/register               # Registro
GET    /api/v1/auth/me                     # Info usuario actual
POST   /api/v1/auth/logout                 # Logout
```

### Compras
```
POST   /api/v1/supply-chain/proveedores    # Crear proveedor
GET    /api/v1/supply-chain/proveedores    # Listar proveedores
POST   /api/v1/supply-chain/ordenes-compra # Crear orden de compra
GET    /api/v1/supply-chain/ordenes-compra # Listar órdenes
```

### Ventas
```
POST   /api/v1/sales/clientes              # Crear cliente
GET    /api/v1/sales/clientes              # Listar clientes
POST   /api/v1/sales/pedidos               # Crear pedido
GET    /api/v1/sales/pedidos               # Listar pedidos
POST   /api/v1/sales/cotizaciones          # Crear cotización
GET    /api/v1/sales/cotizaciones          # Listar cotizaciones
```

### Inventario
```
POST   /api/v1/inventory/productos         # Crear producto
GET    /api/v1/inventory/productos         # Listar productos
POST   /api/v1/inventory/movimientos       # Registrar movimiento
GET    /api/v1/inventory/movimientos       # Listar movimientos
```

### Producción
```
POST   /api/v1/production/ordenes          # Crear orden de producción
GET    /api/v1/production/ordenes          # Listar órdenes
POST   /api/v1/production/recetas          # Crear receta de producción
GET    /api/v1/production/recetas          # Listar recetas
```

### Contabilidad
```
POST   /api/v1/finance/polizas             # Crear póliza contable
GET    /api/v1/finance/polizas             # Listar pólizas
POST   /api/v1/finance/cuentas             # Crear cuenta contable
GET    /api/v1/finance/cuentas             # Listar cuentas
POST   /api/v1/finance/bancos              # Crear cuenta bancaria
GET    /api/v1/finance/bancos              # Listar cuentas bancarias
```

### Facturación Electrónica
```
POST   /api/v1/invoice/comprobantes        # Crear comprobante fiscal
GET    /api/v1/invoice/comprobantes        # Listar comprobantes
POST   /api/v1/invoice/conceptos           # Crear concepto fiscal
GET    /api/v1/invoice/conceptos           # Listar conceptos
POST   /api/v1/invoice/timbrar/{id}        # Timbrar CFDI con Facturama
POST   /api/v1/invoice/cancelar/{id}       # Cancelar CFDI
```

### Nómina Electrónica
```
POST   /api/v1/payroll/periods             # Crear período de nómina
GET    /api/v1/payroll/periods             # Listar períodos
POST   /api/v1/payroll                     # Crear nómina
GET    /api/v1/payroll                     # Listar nóminas
POST   /api/v1/payroll/perceptions         # Crear percepción
GET    /api/v1/payroll/perceptions         # Listar percepciones
POST   /api/v1/payroll/deductions          # Crear deducción
GET    /api/v1/payroll/deductions          # Listar deducciones
POST   /api/v1/payroll/incapacities        # Crear incapacidad
GET    /api/v1/payroll/incapacities        # Listar incapacidades
POST   /api/v1/payroll/other-payments      # Crear otro pago
GET    /api/v1/payroll/other-payments      # Listar otros pagos
```

### Configuración de Correo
```
POST   /api/v1/email-config                # Crear configuración de correo
GET    /api/v1/email-config                # Obtener configuración
PUT    /api/v1/email-config/{id}           # Actualizar configuración
POST   /api/v1/email-config/test           # Probar configuración de correo
GET    /api/v1/email-config/history        # Historial de envíos
```

---

## 🔧 Desarrollo Local (Sin Docker)

### Backend
```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Copiar archivo de entorno
cp .env.example .env

# Ejecutar
uvicorn app.main:app --reload --port 8000
```

### Base de Datos
```bash
# Instalar PostgreSQL localmente
# Crear base de datos
createdb -U postgres guayabera_erp

# O usar Docker solo para BD
docker run -d --name guayabera-db \
  -e POSTGRES_DB=guayabera_erp \
  -e POSTGRES_USER=guayabera_user \
  -e POSTGRES_PASSWORD=guayabera_pass_2025 \
  -p 5432:5432 \
  postgres:15-alpine
```

---

## 🎯 Siguientes Pasos Recomendados

### ✅ Esta Semana
1. **Probar endpoints actuales** con Postman o curl
2. **Crear migraciones Alembic** para versionar BD
3. **Implementar middleware de auditoría** automática
4. **Agregar catálogo de cuentas SAT** importado

### ✅ Próxima Semana
5. **Crear frontend básico** con React
6. **Módulo de contabilidad** (pólizas, asientos)
7. **Sistema de permisos** en endpoints (middleware)

---

## 🐛 Solución de Problemas

### Error: "Database not connected"
```bash
# Verificar PostgreSQL
docker-compose ps postgres

# Ver logs
docker-compose logs postgres

# Reiniciar
docker-compose restart postgres
```

### Error: "Port already in use"
```bash
# Cambiar puertos en docker-compose.yml
ports:
  - "8001:8000"  # En vez de 8000:8000
```

### Error: "Token inválido"
- Verificar que SECRET_KEY en .env sea el mismo
- Token expira en 60 minutos por defecto

---

## 📞 Recursos Adicionales

- **Guía Completa**: `docs/GUIA_MAESTRA_ERP.md`
- **Progreso**: `PROGRESO.md`
- **Documentación API**: http://localhost:8000/docs
- **README General**: `README.md`

---

## 🧠 Consejos para el Desarrollo

### Organización del Código
- El código está organizado por módulos en el directorio `/backend/app/api/v1`
- Cada módulo tiene su propia carpeta con modelos, esquemas, rutas y servicios
- La lógica de negocio se encuentra en `/backend/app/core` y `/backend/app/utils`

### Buenas Prácticas
- Utiliza migraciones Alembic para cualquier cambio en la base de datos
- Sigue el principio de responsabilidad única en las funciones
- Documenta tu código con docstrings claros
- Escribe pruebas unitarias para nuevas funcionalidades

---

**¡Listo! Ya puedes empezar a desarrollar el ERP más completo para la industria textil mexicana** 🧵✨