# 🧵 GuayaberaERP - Sistema ERP Textil

> **El primer ERP especializado en la industria de la confección textil mexicana**

Inspirado en **CONTPAQi** (contabilidad mexicana) + **Odoo** (modularidad web)

[![Status](https://img.shields.io/badge/status-en%20desarrollo-yellow)]()
[![Version](https://img.shields.io/badge/version-0.1.0--alpha-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

---

## 🎯 ¿Qué es GuayaberaERP?

GuayaberaERP es un sistema **ERP (Enterprise Resource Planning)** completo y especializado para la industria textil, con enfoque en la producción de prendas tradicionales mexicanas como la **guayabera yucateca**.

Combina la robustez de los sistemas administrativos mexicanos (CONTPAQi) con la flexibilidad y modularidad de los ERP web modernos (Odoo).

### ✨ Características Únicas

| Característica | GuayaberaERP | ERP Genérico |
|----------------|--------------|--------------|
| **Control de tono en telas** | ✅ Sí, obligatorio | ❌ No |
| **Código QR por rollo** | ✅ Con trazabilidad completa | ❌ Solo código de barras |
| **Diseño de prendas integrado** | ✅ Alforzas, ojales, patrones | ❌ No |
| **Ubicación física en almacén** | ✅ Rack/nivel/posición | ❌ Solo "almacén 1" |
| **CFDI 4.0 México** | ✅ Nativo | ❌ Requiere plugin |
| **Nómina mexicana (IMSS, ISR)** | ✅ Incluido | ❌ Requiere módulo |
| **Enfoque cultural** | ✅ Respeto a tradición textil | ❌ Neutral |

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

```markdown
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
│   │   └── schemas/        # Schemas Pydantic
│   └── requirements.txt
├── frontend/               # React (por desarrollar)
├── database/               # Migraciones Alembic
├── docker/                 # Dockerfiles
├── guayabera-cad/          # Tu MVP CAD integrado
└── docs/                   # Documentación completa
```

---

## 📊 Modelo de Datos

### Núcleo Administrativo
- **Empresa** - Datos fiscales (RFC, régimen)
- **Sucursal** - Almacenes y oficinas
- **Configuración** - Sistema key-value
- **Moneda** - MXN, USD, múltiples monedas
- **Impuesto** - IVA, ISR, IEPS

### Seguridad
- **Usuario** - Usuarios del sistema
- **Rol** - Roles RBAC (Admin, Contador, etc.)
- **Permiso** - Permisos granulares (ver, crear, editar)
- **Auditoría** - Bitácora completa con JSONB

### Próximos Módulos
- **Contabilidad** - Cuentas, pólizas, asientos
- **Inventario** - MP, WIP, PT (3 niveles)
- **Producción** - Órdenes, rutas, costeo
- **Ventas** - Cotizaciones, facturas CFDI

---

## 🔐 Seguridad y Cumplimiento

### Características de Seguridad
- ✅ Autenticación JWT con bcrypt
- ✅ Autorización RBAC (Role-Based Access Control)
- ✅ Auditoría completa con registro de IP, máquina, user agent
- ✅ Datos anteriores/nuevos en JSONB para trazabilidad
- ✅ Cifrado de contraseñas con bcrypt
- ✅ Tokens con expiración configurable

### Cumplimiento México
- ✅ Catálogo de cuentas SAT (importado)
- ✅ CFDI 4.0 (con PAC)
- ✅ Nómina IMSS/ISR/INFONAVIT (complemento SAT)
- ✅ Validación de RFC contra listas negras SAT
- ✅ Auditoría para compliance (implementada)
- ✅ Complementos fiscales (Pago, Carta Porte, Nómina, Comercio Exterior)

---

## 📚 Documentación

| Documento | Descripción |
|-----------|-------------|
| [**GUÍA MAESTRA**](./docs/GUIA_MAESTRA_ERP.md) | Plan completo del ERP, arquitectura, módulos |
| [**QUICKSTART**](./QUICKSTART.md) | Guía de inicio rápido (5 minutos) |
| [**PROGRESO**](./PROGRESO.md) | Estado actual del proyecto |
| [**README CAD**](../guayabera-cad/README.md) | Tu MVP de diseño de guayaberas |

---

## 🎯 Hoja de Ruta (Roadmap)

### Q1 2026 (Enero-Marzo)
- [x] ✅ Fase 1 completa (Administración, Contabilidad, Usuarios)
- [x] ✅ Fase 2 completa (Compras, Inventarios, Almacén)
- [x] ✅ Frontend React funcional

### Q2 2026 (Abril-Junio)
- [x] Fase 3 (Producción Textil + Integración CAD)
- [x] Fase 4 (Ventas + Facturación CFDI 4.0)

### Q3 2026 (Julio-Septiembre)
- [x] Fase 5 (Recursos Humanos + Nómina)
- [x] Fase 6 (Business Intelligence + Integraciones)
- [x] Fase 7 (Optimizaciones y mejoras de rendimiento)

### Q4 2026 (Octubre-Diciembre)
- [ ] Beta testing con talleres reales en Yucatán
- [ ] Optimización y rendimiento
- [ ] Lanzamiento v1.0

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
