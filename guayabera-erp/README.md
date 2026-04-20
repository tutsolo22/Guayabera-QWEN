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

### ✅ Fase 1: Fundación (En Progreso)
- [**Núcleo Administrativo**](./docs/GUIA_MAESTRA_ERP.md#11-núcleo-administrativo) ⭐ Empresa, configuración, catálogos
- [**Contabilidad y Finanzas**](./docs/GUIA_MAESTRA_ERP.md#12-contabilidad-y-finanzas) - Pólizas, asientos, bancos
- [**Usuarios y Permisos**](./docs/GUIA_MAESTRA_ERP.md#13-gestión-de-usuarios-y-permisos) - RBAC, auditoría

### 🔜 Fase 2: Operaciones
- **Compras y Proveedores** - OC, recepción, proveedores
- **Inventarios (3 niveles)** - MP, WIP, PT con trazabilidad
- **Almacén con QR** - Ubicación física, escaneo, rotación

### 🔮 Fase 3-6: Producción, Ventas, RRHH, BI
- **Producción Textil** - Órdenes, rutas, costeo, calidad
- **Ventas y Facturación CFDI 4.0** - Timbrado, CRM
- **Recursos Humanos** - Nómina IMSS, expedientes
- **Business Intelligence** - Dashboards, KPIs, reportes

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
```

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
- ✅ Catálogo de cuentas SAT (por importar)
- ✅ CFDI 4.0 (por implementar con PAC)
- ✅ Nómina IMSS/ISR/INFONAVIT (planificado)
- ✅ Auditoría para compliance (implementada)

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
- [ ] ✅ Fase 1 completa (Administración, Contabilidad, Usuarios)
- [ ] ✅ Fase 2 completa (Compras, Inventarios, Almacén)
- [ ] Frontend React funcional

### Q2 2026 (Abril-Junio)
- [ ] Fase 3 (Producción Textil + Integración CAD)
- [ ] Fase 4 (Ventas + Facturación CFDI 4.0)

### Q3 2026 (Julio-Septiembre)
- [ ] Fase 5 (Recursos Humanos + Nómina)
- [ ] Fase 6 (Business Intelligence + Integraciones)

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

**GuayaberaERP v0.1.0-alpha** - Noviembre 2025

> *"Digitalizando el arte ancestral del corte y confección con precisión industrial y respeto cultural"* 🧵✨
