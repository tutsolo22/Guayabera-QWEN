# 🎯 Guía Maestra de Desarrollo - GuayaberaERP

## 📋 Información del Proyecto
- **Nombre**: GuayaberaERP
- **Tipo**: ERP Web Textil especializado
- **Inspiración**: CONTPAQi (contabilidad mexicana) + Odoo (modularidad web)
- **Enfoque**: Industria de confección textil (guayaberas y prendas tradicionales)
- **Arquitectura**: Web responsive, modular, escalable
- **Versión**: 0.1.0 (Planificación)

---

## 🗺️ Orden Recomendado de Implementación

Basado en mejores prácticas de ERP y eficiencia operativa, este es el orden **crítico** de implementación:

```
FASE 1: FUNDACIÓN (Semanas 1-4)
  ├── 1.1 Núcleo Administrativo ⭐ PRIMERO
  ├── 1.2 Contabilidad y Finanzas
  └── 1.3 Gestión de Usuarios y Permisos

FASE 2: OPERACIONES (Semanas 5-8)
  ├── 2.1 Compras y Proveedores
  ├── 2.2 Inventarios (3 niveles: MP, WIP, PT)
  └── 2.3 Almacén con QR y Trazabilidad

FASE 3: PRODUCCIÓN (Semanas 9-12)
  ├── 3.1 Módulo de Producción Textil
  ├── 3.2 Integración con GuayaberaCAD
  └── 3.3 Costeo y Control de Calidad

FASE 4: VENTAS Y FACTURACIÓN (Semanas 13-16)
  ├── 4.1 Ventas y Cotizaciones
  ├── 4.2 Facturación CFDI 4.0
  └── 4.3 Clientes y CRM básico

FASE 5: RECURSOS HUMANOS (Semanas 17-20)
  ├── 5.1 Gestión de Empleados
  ├── 5.2 Nómina (IMSS, ISR, INFONAVIT)
  └── 5.3 Control de Asistencia

FASE 6: BUSINESS INTELLIGENCE (Semanas 21-24)
  ├── 6.1 Dashboards y KPIs
  ├── 6.2 Reportes Avanzados
  └── 6.3 Integraciones (WhatsApp, Bancos, PAC)
```

---

## 📊 Progreso General del Proyecto

### FASE 1: FUNDACIÓN
| # | Módulo | Estado | Progreso | Notas |
|---|--------|--------|----------|-------|
| 1.1 | **Núcleo Administrativo** | ⬜ Pendiente | 0% | Catálogo de cuentas, empresa, configuración |
| 1.2 | **Contabilidad y Finanzas** | ⬜ Pendiente | 0% | Asientos, balances, bancos |
| 1.3 | **Usuarios y Permisos** | ⬜ Pendiente | 0% | RBAC, auditoría, roles |

### FASE 2: OPERACIONES
| # | Módulo | Estado | Progreso | Notas |
|---|--------|--------|----------|-------|
| 2.1 | **Compras y Proveedores** | ⬜ Pendiente | 0% | OC, recepción, proveedores |
| 2.2 | **Inventarios (3 niveles)** | ⬜ Pendiente | 0% | MP, WIP, PT con trazabilidad |
| 2.3 | **Almacén con QR** | ⬜ Pendiente | 0% | Ubicación física, escaneo |

### FASE 3: PRODUCCIÓN
| # | Módulo | Estado | Progreso | Notas |
|---|--------|--------|----------|-------|
| 3.1 | **Producción Textil** | ⬜ Pendiente | 0% | Órdenes, rutas de trabajo |
| 3.2 | **Integración CAD** | ⬜ Pendiente | 0% | GuayaberaCAD → ERP |
| 3.3 | **Costeo y Calidad** | ⬜ Pendiente | 0% | Costos automáticos, QC |

### FASE 4: VENTAS Y FACTURACIÓN
| # | Módulo | Estado | Progreso | Notas |
|---|--------|--------|----------|-------|
| 4.1 | **Ventas y Cotizaciones** | ⬜ Pendiente | 0% | Pedidos, clientes |
| 4.2 | **Facturación CFDI 4.0** | ⬜ Pendiente | 0% | Timbrado, PAC |
| 4.3 | **CRM Básico** | ⬜ Pendiente | 0% | Pipeline, oportunidades |

### FASE 5: RECURSOS HUMANOS
| # | Módulo | Estado | Progreso | Notas |
|---|--------|--------|----------|-------|
| 5.1 | **Gestión Empleados** | ⬜ Pendiente | 0% | Expedientes, contratos |
| 5.2 | **Nómina** | ⬜ Pendiente | 0% | Cálculo IMSS, ISR |
| 5.3 | **Control Asistencia** | ⬜ Pendiente | 0% | Entradas, salidas, vacaciones |

### FASE 6: BUSINESS INTELLIGENCE
| # | Módulo | Estado | Progreso | Notas |
|---|--------|--------|----------|-------|
| 6.1 | **Dashboards y KPIs** | ⬜ Pendiente | 0% | Gráficos, métricas |
| 6.2 | **Reportes Avanzados** | ⬜ Pendiente | 0% | Excel, PDF, automáticos |
| 6.3 | **Integraciones** | ⬜ Pendiente | 0% | WhatsApp, Bancos, PAC |

---

## 🏗️ Arquitectura Técnica Recomendada

### Stack Tecnológico (Estilo Odoo + CONTPAQi)

| Capa | Tecnología | Justificación |
|------|------------|---------------|
| **Frontend** | React + TypeScript + Ant Design | Modular, web, enterprise UI |
| **Estado Global** | Redux Toolkit + RTK Query | Manejo de estado eficiente |
| **Backend** | Python + FastAPI | Rápido, moderno, fácil de mantener |
| **ORM** | SQLAlchemy + Alembic | Migraciones de BD robustas |
| **Base de Datos** | PostgreSQL 15+ | Soporta JSON, full-text, replicación |
| **Autenticación** | JWT + OAuth2 | Estándar seguro |
| **Cache** | Redis | Sesiones, caché de consultas |
| **Colas** | Celery + RabbitMQ | Tareas asíncronas (facturación, reportes) |
| **Archivos** | MinIO / AWS S3 | Almacenamiento de documentos |
| **Contenedores** | Docker + Docker Compose | Desarrollo y producción |

### Estructura de Carpetas del Proyecto

```
guayabera-erp/
├── backend/
│   ├── app/
│   │   ├── core/                    # Configuración, seguridad
│   │   ├── models/                  # Modelos SQLAlchemy
│   │   ├── schemas/                 # Pydantic schemas
│   │   ├── api/                     # Endpoints FastAPI
│   │   │   ├── v1/
│   │   │   │   ├── admin/           # Módulo administrativo
│   │   │   │   ├── finance/         # Contabilidad
│   │   │   │   ├── purchases/       # Compras
│   │   │   │   ├── inventory/       # Inventarios
│   │   │   │   ├── production/      # Producción
│   │   │   │   ├── sales/           # Ventas
│   │   │   │   ├── hr/              # Recursos humanos
│   │   │   │   └── reports/         # Reportes
│   │   ├── services/                # Lógica de negocio
│   │   └── workers/                 # Celery tasks
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── modules/                 # Módulos por funcionalidad
│   │   │   ├── admin/
│   │   │   ├── finance/
│   │   │   ├── purchases/
│   │   │   ├── inventory/
│   │   │   ├── production/
│   │   │   ├── sales/
│   │   │   └── hr/
│   │   ├── components/              # Componentes reutilizables
│   │   ├── hooks/                   # Custom hooks
│   │   ├── store/                   # Redux store
│   │   ├── services/                # API calls
│   │   └── utils/                   # Utilidades
│   └── package.json
├── database/
│   ├── migrations/                  # Alembic migrations
│   └── seeds/                       # Datos iniciales
├── docker/
│   ├── docker-compose.yml
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
├── docs/                            # Documentación
└── guayabera-cad/                   # Tu MVP CAD (integrado)
```

---

## 📦 DETALLE DE MÓDULOS - FASE 1: FUNDACIÓN

### 1.1 Núcleo Administrativo ⭐ EMPEZAR AQUÍ

**¿Por qué primero?**
- Define la configuración base de la empresa
- Establece catálogos que todos los módulos usan
- Sin esto, ningún otro módulo funciona correctamente

**Funcionalidades:**
- [ ] Configuración de empresa (RFC, nombre, dirección, régimen fiscal)
- [ ] Catálogo de cuentas contables (precargado SAT México)
- [ ] Configuración de monedas (MXN, USD)
- [ ] Configuración de impuestos (IVA, ISR, IEPS)
- [ ] Gestión de sucursales/almacenes
- [ ] Parámetros del sistema (escalas, formatos, horarios)
- [ ] Logs del sistema

**Entregables:**
```
✅ API: /api/v1/admin/*
✅ Frontend: Panel de configuración
✅ BD: Tablas empresa, sucursal, configuracion
```

**Tablas de Base de Datos:**
```sql
- admin_empresa (id, rfc, nombre, regimen_fiscal, direccion, created_at)
- admin_sucursal (id, empresa_id, nombre, direccion, es_principal)
- admin_configuracion (id, clave, valor, tipo, descripcion)
- admin_moneda (id, codigo, nombre, simbolo, tasa_cambio)
- admin_impuesto (id, nombre, tasa, tipo, vigente_desde)
```

---

### 1.2 Contabilidad y Finanzas

**Inspiración CONTPAQi:**
- Catálogo de cuentas mexicano (SAT)
- Pólizas (diario, ingreso, egreso)
- Balanzas de comprobación
- Estados financieros automáticos

**Funcionalidades:**
- [ ] Catálogo de cuentas (importar desde SAT)
- [ ] Pólizas contables (manual y automáticas)
- [ ] Asientos contables automáticos desde otros módulos
- [ ] Balanza de comprobación
- [ ] Estado de resultados
- [ ] Balance general
- [ ] Módulo de bancos (cuentas bancarias, conciliación)
- [ ] Centros de costo
- [ ] Cierre contable mensual/anual

**Integraciones Automáticas:**
```
Compras → Asiento: Débito Inventario MP, Crédito Bancos
Ventas → Asiento: Débito Clientes, Crédito Ventas
Producción → Asiento: Débito Inventario PT, Crédito WIP + MP
Nómina → Asiento: Débito Gasto Nómina, Crédito Bancos + IMSS
```

**Tablas de Base de Datos:**
```sql
- cont_cuenta (id, codigo, nombre, tipo, nivel, es_cuenta_mayor)
- cont_poliza (id, numero, tipo, fecha, descripcion, estado)
- cont_poliza_detalle (id, poliza_id, cuenta_id, cargo, abono)
- cont_asiento (id, poliza_id, modulo_origen, referencia_externa)
- cont_banco (id, nombre, cuenta, clabe, saldo_actual)
- cont_conciliacion (id, banco_id, fecha, estado)
- cont_centro_costo (id, codigo, nombre, activo)
```

---

### 1.3 Gestión de Usuarios y Permisos

**Modelo RBAC (Role-Based Access Control) + ABAC (Attribute-Based)**

**Funcionalidades:**
- [ ] Gestión de usuarios (crear, editar, desactivar)
- [ ] Gestión de roles (predefinidos y custom)
- [ ] Permisos granulares (ver, crear, editar, eliminar por módulo)
- [ ] Asignación de permisos a roles
- [ ] Asignación de múltiples roles a usuarios
- [ ] Sobrescritura de permisos por usuario
- [ ] Sistema de auditoría completo
- [ ] Línea de tiempo de cambios
- [ ] Registro de IP, nombre de máquina, user agent

**Roles Predefinidos:**
| Rol | Permisos |
|-----|----------|
| **Super Admin** | Acceso total |
| **Administrador** | Todos los módulos excepto contabilidad avanzada |
| **Contador** | Contabilidad, bancos, reportes financieros |
| **Almacén** | Inventarios, almacén, compras |
| **Producción** | Producción, calidad, costeo |
| **Vendedor** | Ventas, cotizaciones, CRM |
| **Operario** | Solo registrar producción (sin costos) |
| **RRHH** | Empleados, nómina (sin ver salarios de otros) |
| **Auditor** | Solo lectura + auditoría |

**Sistema de Auditoría:**
```python
# Cada cambio crítico genera registro:
{
  "usuario_id": "uuid",
  "usuario_nombre": "Juan Pérez",
  "ip_address": "192.168.1.100",
  "nombre_maquina": "DESKTOP-ABC123",
  "user_agent": "Chrome 120 / Windows 11",
  "accion": "UPDATE",
  "modulo": "inventario",
  "entidad": "inv_unidad_mp",
  "entidad_id": "uuid",
  "datos_anteriores": {...},
  "datos_nuevos": {...},
  "timestamp": "2025-11-23T15:30:00Z"
}
```

**Tablas de Base de Datos:**
```sql
- seg_usuario (id, username, email, password_hash, activo, ultimo_acceso)
- seg_rol (id, nombre, descripcion, es_sistema)
- seg_permiso (id, modulo, accion, descripcion)
- seg_rol_permiso (id, rol_id, permiso_id)
- seg_usuario_rol (id, usuario_id, rol_id)
- seg_usuario_permiso (id, usuario_id, permiso_id, concedido)
- seg_auditoria (id, usuario_id, accion, modulo, entidad, entidad_id, 
                 datos_anteriores JSONB, datos_nuevos JSONB, 
                 ip_address, nombre_maquina, user_agent, timestamp)
```

---

## 🎯 PLAN DE ACCIÓN INMEDIATO

### Semana 1-2: Configuración del Proyecto

**Día 1-3: Setup Técnico**
- [ ] Crear repositorio Git
- [ ] Configurar Docker Compose (PostgreSQL, Redis, FastAPI, React)
- [ ] Estructura de carpetas completa
- [ ] CI/CD básico (GitHub Actions)

**Día 4-7: Núcleo Administrativo (Módulo 1.1)**
- [ ] Modelo de Empresa
- [ ] Modelo de Sucursal
- [ ] Configuración del sistema
- [ ] API endpoints básicos
- [ ] Frontend: Pantalla de configuración inicial

**Día 8-10: Catálogo de Cuentas**
- [ ] Importar catálogo SAT México
- [ ] API para gestionar cuentas
- [ ] Frontend: Árbol de cuentas contables

---

### Semana 3-4: Contabilidad Básica

**Día 11-14: Pólizas y Asientos**
- [ ] CRUD de pólizas contables
- [ ] Asientos con partida doble (validación cargo = abono)
- [ ] API de asientos automáticos

**Día 15-17: Reportes Financieros**
- [ ] Balanza de comprobación
- [ ] Estado de resultados básico
- [ ] Balance general

**Día 18-20: Bancos**
- [ ] Gestión de cuentas bancarias
- [ ] Conciliación manual
- [ ] Importación de movimientos (CSV)

---

### Semana 4: Usuarios y Permisos

**Día 21-24: Sistema de Autenticación**
- [ ] Login/Logout
- [ ] JWT tokens
- [ ] Protección de rutas

**Día 25-27: RBAC**
- [ ] CRUD de roles
- [ ] CRUD de permisos
- [ ] Asignación de roles a usuarios

**Día 28-30: Auditoría**
- [ ] Middleware de auditoría automática
- [ ] Vista de línea de tiempo
- [ ] Reportes de auditoría

---

## 📊 Checklist General de Funcionalidades

```
FASE 1: FUNDACIÓN
[ ] 1.1 Núcleo Administrativo
    [ ] Configuración empresa
    [ ] Catálogo de cuentas SAT
    [ ] Monedas e impuestos
    [ ] Sucursales
[ ] 1.2 Contabilidad y Finanzas
    [ ] Pólizas contables
    [ ] Asientos automáticos
    [ ] Balanza de comprobación
    [ ] Estado de resultados
    [ ] Balance general
    [ ] Bancos y conciliación
[ ] 1.3 Usuarios y Permisos
    [ ] Login/Logout
    [ ] RBAC completo
    [ ] Auditoría completa
    [ ] Línea de tiempo

FASE 2: OPERACIONES
[ ] 2.1 Compras
    [ ] Gestión de proveedores
    [ ] Órdenes de compra
    [ ] Recepción de mercancía
    [ ] Facturas de proveedores
[ ] 2.2 Inventarios
    [ ] Materia prima (con QR, color, tono)
    [ ] En producción (WIP)
    [ ] Producto terminado
    [ ] Movimientos de inventario
[ ] 2.3 Almacén
    [ ] Ubicación física (rack/nivel/posición)
    [ ] Escaneo QR
    [ ] Políticas de rotación (PEPS, UEPS)

FASE 3: PRODUCCIÓN
[ ] 3.1 Producción Textil
    [ ] Órdenes de producción
    [ ] Rutas de trabajo
    [ ] Control por etapas
[ ] 3.2 Integración CAD
    [ ] Importar desde GuayaberaCAD
    [ ] Generación automática de OP
[ ] 3.3 Costeo y Calidad
    [ ] Costeo automático
    [ ] Control de calidad
    [ ] KPI de producción

FASE 4: VENTAS Y FACTURACIÓN
[ ] 4.1 Ventas
    [ ] Cotizaciones
    [ ] Pedidos de venta
    [ ] Clientes
[ ] 4.2 Facturación CFDI 4.0
    [ ] Timbrado con PAC
    [ ] Cancelación
    [ ] PDF de factura
[ ] 4.3 CRM
    [ ] Pipeline de ventas
    [ ] Oportunidades

FASE 5: RECURSOS HUMANOS
[ ] 5.1 Empleados
    [ ] Expedientes
    [ ] Contratos
    [ ] Documentos
[ ] 5.2 Nómina
    [ ] Cálculo IMSS
    [ ] Cálculo ISR
    [ ] Recibos de nómina
[ ] 5.3 Asistencia
    [ ] Registro entradas/salidas
    [ ] Vacaciones
    [ ] Ausencias

FASE 6: BUSINESS INTELLIGENCE
[ ] 6.1 Dashboards
    [ ] KPIs financieros
    [ ] KPIs de producción
    [ ] KPIs de ventas
[ ] 6.2 Reportes
    [ ] Exportación Excel/PDF
    [ ] Reportes automáticos
[ ] 6.3 Integraciones
    [ ] WhatsApp Business
    [ ] Bancos (Open Banking)
    [ ] PAC facturación
```

---

## 🚀 Recomendaciones Clave

### ✅ Haz Esto
1. **Empieza por el núcleo administrativo** - Sin configuración de empresa y catálogo de cuentas, nada más funciona
2. **Implementa auditoría desde el día 1** - No lo dejes para después, es crítico para compliance
3. **Usa Docker desde el inicio** - Facilita desarrollo y despliegue
4. **Importa catálogo SAT México** - Ya viene estructurado con cuentas estándar
5. **Diseña APIs RESTful limpias** - Te servirán para integraciones futuras
6. **Prueba con datos reales de talleres textiles** - Valida con usuarios reales

### ❌ No Hagas Esto
1. **No empieces por producción** - Necesitas contabilidad e inventarios primero
2. **No ignores la contabilidad mexicana** - CFDI, IMSS, SAT son obligatorios
3. **No hardcodes configuración** - Todo debe ser parametrizable
4. **No olvides la auditoría** - Es requisito legal y de control interno
5. **No copies ERPs genéricos** - Tu ventaja es la especialización textil

---

## 📈 Métricas de Éxito por Fase

| Fase | Criterio de Éxito | Métrica |
|------|-------------------|---------|
| 1 | Sistema administrativo funcional | Empresa configurada + 100 cuentas contables importadas |
| 2 | Operaciones funcionando | OC creada → Recepción → Inventario actualizado |
| 3 | Producción integrada | OP creada → MP consumida → PT generado |
| 4 | Facturación funcionando | Venta → Factura timbrada → Asiento contable automático |
| 5 | Nómina calculada | Empleado registrado → Nómina calculada → Asiento automático |
| 6 | Dashboards en vivo | KPIs actualizados en tiempo real |

---

## 🎓 Próximos Pasos Inmediatos

### Esta Semana:
1. ✅ **Crear repositorio** con estructura completa
2. ✅ **Configurar Docker Compose** con PostgreSQL, Redis, FastAPI
3. ✅ **Implementar módulo 1.1** (Núcleo Administrativo)
4. ✅ **Importar catálogo SAT** de cuentas contables

### Siguiente Semana:
5. ⏳ **Contabilidad básica** (pólizas, asientos)
6. ⏳ **Sistema de login** con JWT
7. ⏳ **RBAC básico** (roles y permisos)

---

**¿Listo para comenzar?** 

Te recomiendo que empecemos con:
1. **Setup del proyecto** (Docker + estructura)
2. **Módulo 1.1: Núcleo Administrativo** (empresa, configuración, catálogo de cuentas)
3. **Módulo 1.3: Usuarios y Permisos** (para que todo tenga seguridad desde el inicio)

¿Por cuál quieres que empiece? 🚀
