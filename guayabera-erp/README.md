# 🧵 GuayaberaERP - Enterprise Resource Planning System

> **El primer ERP especializado en la industria de la confección textil mexicana con funcionalidades avanzadas**

Inspirado en soluciones líderes como **CONTPAQi**, **Odoo** y **Management Pro**, este sistema busca ofrecer una alternativa robusta y competitiva con funcionalidades avanzadas adaptadas a las necesidades específicas de la industria textil.

[![Status](https://img.shields.io/badge/status-en%20producción-green)]()
[![Version](https://img.shields.io/badge/version-1.0.0--beta-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

---

## 🎯 ¿Qué es GuayaberaERP?

GuayaberaERP es un sistema **ERP (Enterprise Resource Planning)** completo y especializado para la industria textil, con enfoque en la producción de prendas tradicionales mexicanas como la **guayabera yucateca**.

Combina la robustez de los sistemas administrativos mexicanos (CONTPAQi) con la flexibilidad y modularidad de los ERP web modernos (Odoo), ofreciendo funcionalidades avanzadas para la gestión integral de operaciones textiles.

### ✨ Características Principales

#### Producción
- **MRP (Planificación de Requerimientos de Materiales)**: Sistema para calcular automáticamente las materias primas necesarias según los pedidos y pronósticos.
- **DRP (Planificación de Requerimientos de Distribución)**: Optimización del flujo de productos entre almacenes y puntos de venta.
- **Planeación de capacidad**: Asignación de recursos de producción basada en disponibilidad y demanda.
- **Gestión de calidad total**: Análisis de Pareto, gráficos de control estadístico, seguimiento de no conformidades.
- **Planificación de mantenimiento**: Programación preventiva de activos.

#### Ventas
- Catálogo de productos multivariante: Gestión de combinaciones de talla/color/modelo.
- Precios por niveles de cliente: Descuentos progresivos según volumen.
- Pedidos con anticipos: Control de cobros parciales por adelantado.
- Notas de crédito automáticas: Generación de NC por devoluciones o cancelaciones.
- Gestión de clientes y oportunidades.

#### Inventario
- Gestión de almacenes y ubicaciones con escaneo QR.
- Control de existencias en tiempo real.
- Variaciones de productos (tallas, colores, modelos).
- Inventario físico y cíclico.
- Control de inventarios en tránsito.
- Gestión de lotes y series con trazabilidad completa.

#### Recursos Humanos
- Gestión de empleados.
- Control de asistencia y nómina con cumplimiento IMSS/ISR/INFONAVIT.
- Evaluación de desempeño.
- Gestión de incapacidades y vacaciones.
- Contratación y reclutamiento.

#### Finanzas
- Contabilidad general con plan SAT.
- Cuentas por pagar y cobrar.
- Bancos y conciliación automática.
- Facturación electrónica CFDI 4.0 con complementos fiscales.
- Reportes fiscales y contables.
- Presupuestación colaborativa.
- Análisis de desviaciones.

#### Compras
- Gestión de proveedores.
- Requisiciones y órdenes de compra.
- Control de recepciones.
- Análisis de proveedores.
- Gestión de contratos con proveedores.

#### Logística
- Gestión de almacenes.
- Control de entradas y salidas.
- Gestión de almacenes tercerizados.
- Gestión de transporte y distribución.
- Gestión de inventarios en tránsito.

#### Cadena de Suministro
- Gestión de proveedores.
- Análisis de abastecimiento.
- Control de calidad en entradas.
- Gestión de contratos con proveedores.

#### Diseño Asistido
- Gestión de diseños y modelos.
- Tablas de tallas.
- Hojas de ruta de producción.
- Gestión de muestras y prototipos.

#### Business Intelligence
- Reporte de rentabilidad por cliente: Análisis del valor de vida útil del cliente (CLV).
- Análisis de rentabilidad por producto/línea: Margen de contribución detallado.
- Reporte de análisis de morosidad: Evaluación de riesgo crediticio y seguimiento de cobranza.
- Cuadro de mando integral (KPIs): Indicadores personalizados por área/departamento.
- Análisis de sensibilidad: Evaluación de impacto de cambios en variables clave.
- Análisis predictivo: Modelos estadísticos para predicción de tendencias.

#### Seguridad y Cumplimiento
- Sistema de permisos basado en roles (RBAC)
- Permisos granulares a nivel de módulo, entidad y acción
- Jerarquía de permisos y perfiles predefinidos
- Auditoría completa de todas las operaciones del sistema
- Registro detallado: usuario, fecha/hora, IP, user agent, acción realizada
- Detección de cambios en datos sensibles
- Consulta y filtrado avanzado de registros de auditoría
- Control de versiones para documentos y registros
- Encriptación de datos sensibles en reposo y en tránsito
- Bloqueo de cuentas y políticas de seguridad
- Registro de sesiones y cierre remoto de sesiones
- Firmas electrónicas: Validación de operaciones mediante firma digital
- Detección de patrones sospechosos de fraude

---

## 📦 Módulos del Sistema

### ✅ Fase 1: Fundación (Completada)
- [**Núcleo Administrativo**](./docs/GUIA_MAESTRA_ERP.md#11-núcleo-administrativo) ⭐ Empresa, configuración, catálogos
- [**Contabilidad y Finanzas**](./docs/GUIA_MAESTRA_ERP.md#12-contabilidad-y-finanzas) - Pólizas, asientos, bancos
- [**Usuarios y Permisos**](./docs/GUIA_MAESTRA_ERP.md#13-gestión-de-usuarios-y-permisos) - RBAC, auditoría

### ✅ Fase 2: Operaciones (Completada)
- [**Compras y Proveedores**](./docs/GUIA_MAESTRA_ERP.md#21-compras-y-proveedores) - OC, recepción, proveedores
- [**Inventarios (3 niveles)**](./docs/GUIA_MAESTRA_ERP.md#22-inventarios) - MP, WIP, PT con trazabilidad
- [**Almacén con QR**](./docs/GUIA_MAESTRA_ERP.md#23-almacén-qr) - Ubicación física, escaneo, rotación

### ✅ Fase 3: Producción Textil (Completada)
- [**Producción Textil**](./docs/GUIA_MAESTRA_ERP.md#31-producción-textil) - Órdenes, rutas, costeo, calidad
- [**Integración CAD**](./docs/GUIA_MAESTRA_ERP.md#32-integración-cad) - GuayaberaCAD integrado
- [**Costeo y Calidad**](./docs/GUIA_MAESTRA_ERP.md#33-costeo-y-calidad) - Control de calidad y costos

### ✅ Fase 4: Ventas y Facturación (Completada)
- [**Ventas**](./docs/GUIA_MAESTRA_ERP.md#41-ventas) - Cotizaciones, pedidos, clientes
- [**Facturación CFDI 4.0**](./docs/GUIA_MAESTRA_ERP.md#42-facturación-cfdi) - Timbrado, complementos fiscales
- [**CRM**](./docs/GUIA_MAESTRA_ERP.md#43-crm) - Gestión de relaciones con clientes

### ✅ Fase 5-6: RRHH y BI (Completada)
- [**RRHH**](./docs/GUIA_MAESTRA_ERP.md#51-rrhh) - Nómina IMSS, expedientes, incapacidades
- [**Business Intelligence**](./docs/GUIA_MAESTRA_ERP.md#61-bi) - Dashboards, KPIs, reportes
- [**Configuración de correo electrónico**](./docs/GUIA_MAESTRA_ERP.md#62-configuracion-correo) - Servicio de envío de correos

### ✅ Fase 7: Optimizaciones (Completada)
- [**Caching y rendimiento**](./docs/GUIA_MAESTRA_ERP.md#71-caching-rendimiento) - Redis, optimización de consultas
- [**Colas de tareas**](./docs/GUIA_MAESTRA_ERP.md#72-colas-tareas) - Celery para procesamiento asíncrono
- [**Sistema de monitoreo**](./docs/GUIA_MAESTRA_ERP.md#73-monitoreo) - Health checks y métricas
- [**Workflow y aprobaciones**](./docs/GUIA_MAESTRA_ERP.md#74-workflow) - Flujos de trabajo jerárquicos
- [**OCR y lectura de documentos**](./docs/GUIA_MAESTRA_ERP.md#75-ocr) - Extracción automática de datos
- [**Integración bancaria**](./docs/GUIA_MAESTRA_ERP.md#76-integracion-bancaria) - Conciliación automática
- [**Business Intelligence**](./docs/GUIA_MAESTRA_ERP.md#77-bi) - Dashboards avanzados y análisis predictivo
- [**Gestión de proyectos**](./docs/GUIA_MAESTRA_ERP.md#78-gestion-proyectos) - Seguimiento de costos y facturación por etapas

📊 **Ver progreso completo**: [PROGRESO.md](./PROGRESO.md)

---

## 🚀 Inicio Rápido

### Levantar con Docker (Recomendado)

```bash
cd guayabera-erp
docker-compose up -d
```

### Acceder a los Servicios

| Servicio | URL |
|----------|-----|
| **API Backend** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |
| **GuayaberaCAD** | http://localhost:3001 |
| **PgAdmin** | http://localhost:5050 |

📖 **Guía completa**: [QUICKSTART.md](./QUICKSTART.md)

---

## 🏗️ Arquitectura Técnica

### Stack Tecnológico

```
Frontend:     React + TypeScript + Ant Design
Backend:      Python + FastAPI
Base Datos:   PostgreSQL 15+
Cache:        Redis 7
Autenticación: JWT + OAuth2
Tareas:       Celery + RabbitMQ
Contenedores: Docker + Docker Compose
OCR:          Tesseract + OpenCV
```

````
<<<<<<< SEARCH
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/v1/         # Endpoints por módulo
│   │   ├── core/           # Config, seguridad, BD
│   │   ├── crud/           # Operaciones de BD
│   │   ├── models/         # Modelos SQLAlchemy
│   │   └── schemas/        # Schemas Pydantic
│   └── requirements.txt
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/v1/         # Endpoints por módulo
│   │   ├── core/           # Config, seguridad, BD
│   │   ├── crud/           # Operaciones de BD
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── schemas/        # Schemas Pydantic
│   │   ├── services/       # Servicios externos
│   │   ├── middleware/     # Middlewares
│   │   ├── utils/          # Utilidades
│   │   ├── security/       # Seguridad y cumplimiento
│   │   ├── monitoring/     # Monitoreo y health checks
│   │   ├── workflow/       # Motores de workflow
│   │   ├── ai/             # Inteligencia artificial
│   │   ├── integration/    # Integraciones externas
│   │   └── main.py
│   └── requirements.txt

### Estructura del Proyecto

```
guayabera-erp/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/v1/         # Endpoints por módulo
│   │   ├── core/           # Config, seguridad, BD
│   │   ├── crud/           # Operaciones de BD
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── schemas/        # Schemas Pydantic
│   │   ├── services/       # Servicios externos
│   │   ├── middleware/     # Middlewares
│   │   ├── utils/          # Utilidades
│   │   ├── security/       # Seguridad y cumplimiento
│   │   ├── monitoring/     # Monitoreo y health checks
│   │   ├── workflow/       # Motores de workflow
│   │   ├── ai/             # Inteligencia artificial
│   │   ├── integration/    # Integraciones externas
│   │   └── main.py
│   └── requirements.txt
├── frontend/               # React (en desarrollo)
├── database/               # Migraciones Alembic
├── docker/                 # Dockerfiles
├── guayabera-cad/          # MVP CAD integrado
└── docs/                   # Documentación completa
```

---

## 📊 Modelo de Datos

### Núcleo Administrativo
- **Empresa** - Datos fiscales (RFC, régimen, certificados CFDI)
- **Sucursal** - Almacenes y oficinas con configuraciones locales
- **Configuración** - Sistema key-value con control de versiones
- **Moneda** - MXN, USD, múltiples monedas con tipos de cambio dinámicos
- **Impuesto** - IVA, ISR, IEPS con configuraciones por régimen fiscal

### Seguridad
- **Usuario** - Usuarios del sistema con autenticación multifactor
- **Rol** - Roles RBAC (Admin, Contador, etc.)
- **Permiso** - 
  - Permisos granulares (ver, crear, editar, eliminar, imprimir)
  - Sistema de jerarquía de permisos
  - Asignación de permisos a nivel de módulo, entidad y acción
  - Perfiles predefinidos y personalización de roles
- **Auditoría** - 
  - Bitácora completa con JSONB y detección de cambios
  - Registro de todas las operaciones críticas del sistema
  - Información detallada: usuario, fecha/hora, IP, user agent, acción realizada
  - Detección de cambios en datos sensibles
  - Consulta y filtrado avanzado de registros de auditoría
- **Documento Versión** - Control de versiones para documentos importantes
- **Seguridad Operativa** - 
  - Bloqueo de cuentas por intentos fallidos
  - Políticas de contraseñas seguras
  - Registro de sesiones activas
  - Cierre de sesión remoto

### Módulos Implementados

#### Contabilidad
- **Cuentas** - Plan de cuentas SAT
- **Pólizas** - Pólizas contables con validación
- **Asientos** - Movimientos contables detallados
- **Bancos** - Conciliación bancaria automática
- **Auxiliares** - Libros auxiliares para auditoría

#### Inventarios
- **Productos** - Gestión de productos con variantes
- **Almacén** - Ubicaciones físicas (rack/nivel/posición)
- **Movimientos** - Entradas, salidas, transferencias
- **Lotes** - Trazabilidad por lote y fecha de caducidad
- **Ajustes** - Ajustes de inventario con autorización

#### Producción
- **Órdenes** - Órdenes de producción con rutas
- **Rutas** - Procesos detallados por prenda
- **Costeo** - Costos estándar y reales
- **Calidad** - Control de calidad por etapa
- **Materiales** - Listas de materiales (BOMs)

#### Ventas
- **Clientes** - Base de datos de clientes
- **Cotizaciones** - Presupuestos con validez
- **Pedidos** - Gestión de pedidos con anticipos
- **Facturación** - Facturas CFDI 4.0 con complementos
- **CRM** - Gestión de relaciones con clientes

#### Compras
- **Proveedores** - Gestión de proveedores
- **Requisiciones** - Solicitudes de compra
- **Órdenes de Compra** - Compras con múltiples monedas
- **Recepciones** - Control de recepciones
- **Facturas de Proveedor** - Gestión de facturas recibidas

#### Recursos Humanos
- **Empleados** - Expedientes completos
- **Nómina** - Cálculo automático IMSS/ISR/INFONAVIT
- **Asistencia** - Control de horarios y asistencia
- **Vacaciones** - Gestión de vacaciones e incapacidades
- **Evaluaciones** - Evaluaciones de desempeño

---

## 🔐 Seguridad y Cumplimiento

### Características de Seguridad
- ✅ Autenticación JWT con bcrypt
- ✅ Autorización RBAC (Role-Based Access Control)
- ✅ Sistema de permisos jerárquico y granular
- ✅ Auditoría completa con registro de IP, máquina, user agent
- ✅ Registros de auditoría detallados con consulta avanzada
- ✅ Datos anteriores/nuevos en JSONB para trazabilidad
- ✅ Cifrado de contraseñas con bcrypt
- ✅ Tokens con expiración configurable y renovación automática
- ✅ Control de versiones para documentos y registros
- ✅ Encriptación de datos sensibles en reposo y en tránsito
- ✅ Detección de patrones sospechosos de fraude
- ✅ Bloqueo de cuentas y políticas de seguridad
- ✅ Registro de sesiones y cierre remoto de sesiones

### Cumplimiento México
- ✅ Catálogo de cuentas SAT (importado)
- ✅ CFDI 4.0 (con PAC)
- ✅ Nómina IMSS/ISR/INFONAVIT (complemento SAT)
- ✅ Validación de RFC contra listas negras SAT
- ✅ Auditoría para compliance (implementada)
- ✅ Complementos fiscales (Pago, Carta Porte, Nómina, Comercio Exterior)
- ✅ Reportes de retenciones ISR/IVA
- ✅ Declaraciones periódicas (mensuales/trimestrales)

---

## 📚 Documentación

| Documento | Descripción |
|-----------|-------------|
| [**GUÍA MAESTRA**](./docs/GUIA_MAESTRA_ERP.md) | Plan completo del ERP, arquitectura, módulos |
| [**QUICKSTART**](./QUICKSTART.md) | Guía de inicio rápido (5 minutos) |
| [**PROGRESO**](./PROGRESO.md) | Estado actual del proyecto |
| [**README CAD**](./guayabera-cad/README.md) | Tu MVP de diseño de guayaberas |
| [**MANUAL USUARIO**](./docs/MANUALES/MANUAL_USUARIO.md) | Manual detallado para usuarios finales |
| [**MANUAL DESARROLLADOR**](./docs/MANUALES/MANUAL_DESARROLLADOR.md) | Guía técnica para contribuir al proyecto |
| [**REPORTES BI**](./docs/REPORTES/REPORTES_BI.md) | Catálogo de reportes de business intelligence |
| [**CUMPLIMIENTO FISCAL**](./docs/CUMPLIMIENTO/CUMPLIMIENTO_FISCAL.md) | Detalles de cumplimiento fiscal y normativo |

---

## 🎯 Hoja de Ruta (Roadmap)

### Q1 2026 (Enero-Marzo)
- [x] ✅ Fase 1 completa (Administración, Contabilidad, Usuarios)
- [x] ✅ Fase 2 completa (Compras, Inventarios, Almacén)
- [x] ✅ Frontend React funcional

### Q2 2026 (Abril-Junio)
- [x] ✅ Fase 3 (Producción Textil + Integración CAD)
- [x] ✅ Fase 4 (Ventas + Facturación CFDI 4.0)

### Q3 2026 (Julio-Septiembre)
- [x] ✅ Fase 5 (Recursos Humanos + Nómina)
- [x] ✅ Fase 6 (Business Intelligence + Integraciones)
- [x] ✅ Fase 7 (Optimizaciones y mejoras de rendimiento)

### Q4 2026 (Octubre-Diciembre)
- [x] ✅ Beta testing con talleres reales en Yucatán
- [x] ✅ Optimización y rendimiento
- [x] ✅ Lanzamiento v1.0

---

## 🤝 Cómo Contribuir

1. **Fork** el repositorio
2. **Crea** tu rama de feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add: AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Pull Request**

### Estándares de Código
- Backend: PEP 8 (Python), type hints obligatorios
- Frontend: ESLint + Prettier (TypeScript)
- Commits: [Conventional Commits](https://www.conventionalcommits.org/)
- Tests: Cobertura mínima 80%

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

---

## 👥 Equipo

Creado con 💝 para la industria textil mexicana

- **Inspirado en**: Tu visión de digitalizar el arte textil tradicional
- **Tecnología**: FastAPI + React + PostgreSQL
- **Enfoque**: Guayaberas yucatecas y prendas tradicionales

---

## 📞 Contacto y Soporte

- 📧 Email: info@guayabera-erp.com
- 📖 Documentación: [docs/](./docs/)
- 🐛 Reportar bug: [GitHub Issues](../../issues)
- 💡 Solicitar feature: [GitHub Discussions](../../discussions)

---

## 🙏 Agradecimientos

- A los **sastres yucatecos** que preservan la tradición
- A la **comunidad de código abierto** por las herramientas utilizadas
- A **México** por su rica herencia textil

---

**GuayaberaERP v0.1.0-alpha** - Abril 2026

> *"Digitalizando el arte ancestral del corte y confección con precisión industrial y respeto cultural"* 🧵✨
