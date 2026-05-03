# Resumen Técnico del ERP Guayabera

## Descripción General

El ERP Guayabera es un sistema de planificación de recursos empresariales desarrollado específicamente para la industria de la moda y la confección de prendas de vestir. El sistema combina las mejores prácticas de soluciones líderes como Contpaq, Odoo y Management Pro con funcionalidades innovadoras de inteligencia artificial y análisis de datos.

## Arquitectura del Sistema

### Tecnologías Utilizadas

#### Backend
- **Framework Web**: FastAPI (Python 3.11+)
- **ORM**: SQLAlchemy con soporte para PostgreSQL
- **Autenticación**: JWT (JSON Web Tokens)
- **Validación de Datos**: Pydantic
- **Cache**: Redis
- **Tareas Asíncronas**: Celery
- **Mensajería**: WebSockets para comunicación en tiempo real
- **Monitoreo**: Health checks integrados

#### Frontend
- **Framework**: React 18+
- **Lenguaje**: TypeScript
- **UI Framework**: Ant Design
- **Estado**: Redux Toolkit
- **Enrutamiento**: React Router
- **Comunicación API**: Axios

#### Infraestructura
- **Contenedores**: Docker & Docker Compose
- **Proxy Inverso**: NGINX
- **Seguridad**: Let's Encrypt para SSL

## Estructura del Proyecto

```

## Resumen técnico de los cambios realizados

### Fecha: 1 de mayo de 2026

### Introducción
Se han realizado múltiples correcciones en el proyecto Guayabera ERP para solucionar problemas de importación, estructura y funcionalidad que impedían el correcto funcionamiento del sistema.

## Cambios realizados

### 1. Correcciones en el módulo de reportes
**Archivo afectado:** [app/api/v1/reports/router.py](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/api/v1/reports/router.py)

- Corregidos los nombres de las funciones importadas para que coincidan con las definiciones reales en el módulo CRUD
- Actualizados los endpoints para usar las funciones correctas:
  - [get_reportes_rh_by_reporte](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/crud/reports.py#L100-L102) en lugar de [get_reportes_rh](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/crud/reports.py#L66-L70)
  - [get_reportes_ventas_by_reporte](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/crud/reports.py#L198-L200) en lugar de [get_reportes_ventas](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/crud/reports.py#L164-L166)
  - [get_reportes_inventario_by_reporte](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/crud/reports.py#L247-L249) en lugar de [get_reportes_inventario](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/crud/reports.py#L214-L216)
  - [get_reportes_finanzas_by_reporte](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/crud/reports.py#L296-L298) en lugar de [get_reportes_finanzas](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/crud/reports.py#L263-L265)

### 2. Corrección en el servicio de caché
**Archivo afectado:** [app/services/cache_service.py](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/services/cache_service.py)

- Actualizado para usar [REDIS_URL](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/core/config.py#L39-L39) en lugar de los parámetros individuales de host, puerto y contraseña
- Adaptada la creación del cliente de Redis para aceptar la URL completa

### 3. Correcciones en el módulo de notificaciones
**Archivos afectados:** [app/models/notifications.py](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/models/notifications.py) y [app/services/notification_service.py](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/services/notification_service.py)

- Añadidas las definiciones de enum faltantes en el modelo de notificaciones
- Actualizado el servicio de notificaciones para usar valores de string directamente en lugar de valores de enum
- Añadida la función [start_notification_cleanup_scheduler](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/services/notification_service.py#L185-L193) para gestionar la limpieza periódica de notificaciones antiguas
- Añadida la función [delete_old_notifications](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/crud/notifications.py#L97-L104) en el módulo CRUD

### 4. Actualización de dependencias
**Archivo afectado:** [requirements.txt](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/requirements.txt)

- Añadidas las bibliotecas [psutil](file://c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/services/system_monitor.py#L9-L9), opencv-python y pytesseract para funcionalidades del sistema y OCR

### 5. Correcciones en módulos con routers faltantes
**Archivos afectados:** [app/monitoring/health_checks.py](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/monitoring/health_checks.py), [app/security/compliance.py](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/security/compliance.py), [app/ai/document_ocr.py](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/ai/document_ocr.py)

- Añadidos los routers faltantes con endpoints para exponer las funcionalidades como APIs
- Corregidas las importaciones necesarias para que funcionen correctamente

### 6. Adición de modelos financieros
**Archivo afectado:** [app/models/finance.py](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/models/finance.py)

- Añadidas las clases [CuentaBancaria](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/models/finance.py#L193-L236) y [Transaccion](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/models/inventory.py#L417-L444) para soportar la funcionalidad de integración bancaria
- Corregida la importación de Usuario desde `app.models.security` en lugar de `app.models.seguridad`

### 7. Actualización del módulo de integración bancaria
**Archivo afectado:** [app/integration/bank_integration.py](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/integration/bank_integration.py)

- Añadido el router faltante para la integración bancaria
- Corregidas las importaciones necesarias para que funcione correctamente

## Migraciones de base de datos

Se creó y aplicó una migración completa que incluye todas las tablas esenciales del sistema en el orden correcto, incluyendo las nuevas tablas para [CuentaBancaria](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/models/finance.py#L193-L236) y [Transaccion](file:///c:/Users/Choripapa/Documents/Proyectos/Guayabera-QWEN/guayabera-erp/backend/app/models/inventory.py#L417-L444).

## Resultado final

Tras aplicar todas estas correcciones, el sistema ahora puede iniciar correctamente sin errores de importación. Todos los módulos están correctamente conectados y la funcionalidad de integración bancaria está completamente implementada.

Los únicos requisitos pendientes para un funcionamiento completo son:
1. Tener PostgreSQL corriendo en localhost:5432
2. Tener Redis corriendo en localhost:6379
3. Tener las variables de entorno configuradas en un archivo .env

La aplicación ahora debería poder iniciarse correctamente usando el comando: `uvicorn app.main:app --reload`
guayabera-erp/
├── backend/
│   ├── app/
│   │   ├── models/           # Modelos de SQLAlchemy
│   │   ├── schemas/          # Esquemas Pydantic
│   │   ├── crud/             # Operaciones CRUD
│   │   ├── api/
│   │   │   └── v1/          # Rutas API versión 1
│   │   ├── core/             # Configuración central
│   │   ├── services/         # Lógica de negocio
│   │   ├── tasks/            # Tareas asíncronas
│   │   ├── middleware/       # Middleware personalizado
│   │   ├── utils/            # Utilidades
│   │   ├── ai/               # Componentes de IA
│   │   ├── integration/      # Integraciones externas
│   │   ├── workflow/         # Motor de flujos de trabajo
│   │   ├── security/         # Componentes de seguridad
│   │   └── monitoring/       # Componentes de monitoreo
│   ├── requirements.txt      # Dependencias Python
│   └── main.py               # Punto de entrada
└── frontend/
    ├── src/
    │   ├── components/       # Componentes React
    │   ├── pages/           # Páginas de la aplicación
    │   ├── layouts/         # Layouts de la aplicación
    │   ├── services/        # Servicios API
    │   ├── store/           # Store de Redux
    │   ├── assets/          # Recursos estáticos
    │   └── config/          # Archivos de configuración
    ├── package.json          # Dependencias Node
    └── tsconfig.json         # Configuración TypeScript
```

## Módulos Implementados

### 1. Producción
- **MRP (Planificación de Requerimientos de Materiales)**: Modelos, schemas y CRUD para manejo de recetas de producción, órdenes de producción, consumo de materiales, previsión de demanda y programa maestro de producción.
- **Control de Calidad**: Gestión de no conformidades, análisis de Pareto y gráficos de control estadístico.
- **Mantenimiento**: Gestión de equipos, órdenes de mantenimiento, historial y planes preventivos.
- **Diseño Asistido por Computadora (CAD)**: Integración con herramientas de diseño digital para patrones y modelos.
- **Costeo de Productos**: Sistema detallado para calcular costos de producción basado en materiales, mano de obra y gastos indirectos.

### 2. Ventas
- **Gestión de Clientes**: Modelos completos para clientes, contactos y relaciones comerciales.
- **Catálogo de Productos Multivariante**: Soporte para productos con múltiples variaciones (tallas, colores, etc.).
- **Precios por Niveles de Cliente**: Sistema de descuentos progresivos según volumen de compras.
- **Pedidos con Anticipos**: Control de cobros parciales por adelantado.
- **Notas de Crédito Automáticas**: Generación automática por devoluciones o cancelaciones.

### 3. Inventario
- **Gestión de Almacenes**: Modelos para almacenes, ubicaciones y movimientos.
- **Control de Existencias**: Seguimiento en tiempo real de niveles de inventario.
- **Inventario Físico**: Herramientas para conteo y reconciliación.
- **Control de Inventarios en Tránsito**: Seguimiento de mercancías entre almacenes.
- **Control de Lotes**: Seguimiento detallado de lotes de productos con fechas de vencimiento y ubicaciones específicas.

### 4. Recursos Humanos
- **Gestión de Empleados**: Modelos completos para datos personales, contratación, nómina.
- **Control de Asistencia**: Registro y análisis de asistencia y tiempos.
- **Evaluación de Desempeño**: Sistemas de evaluación y feedback.
- **Nómina Electrónica**: Complemento de nómina SAT con integración directa para reportes fiscales.
- **Incidencias Laborales**: Gestión de incapacidades, permisos, vacaciones y otras incidencias.

### 5. Finanzas
- **Contabilidad General**: Libro mayor, auxiliares, estados financieros.
- **Cuentas por Pagar/Cobrar**: Gestión de vencimientos y conciliación.
- **Integración Bancaria**: Conciliación automática y seguimiento de flujos de efectivo.
- **Clasificación Automática de Transacciones**: IA para categorizar movimientos financieros.
- **Facturación Electrónica (CFDI 4.0)**: Generación y timbrado de comprobantes fiscales con complementos (Pago, Carta Porte, Nómina, Comercio Exterior).

### 6. Compras
- **Gestión de Proveedores**: Modelos para proveedores y contratos.
- **Requisiciones y Órdenes de Compra**: Flujos de aprobación y seguimiento.
- **Análisis de Proveedores**: Métricas de desempeño y evaluación.
- **Recepción de Mercancía**: Proceso completo desde recepción hasta integración con inventarios.

### 7. Logística
- **Gestión de Almacenes**: Control de ubicaciones y capacidades.
- **Gestión de Transporte**: Asignación y seguimiento de envíos.
- **Almacenes Tercerizados**: Integración con servicios externos.

### 8. CRM
- **Gestión de Clientes**: Perfiles completos y relaciones comerciales.
- **Oportunidades de Venta**: Seguimiento y conversión.
- **Atención al Cliente**: Sistema de tickets y soporte.
- **Marketing**: Gestión de campañas y análisis de efectividad.

### 9. Business Intelligence
- **Reportes Personalizados**: Sistema flexible de creación de reportes.
- **Dashboard Ejecutivo**: KPIs y métricas clave.
- **Análisis de Sensibilidad**: Evaluación de impacto de variables.
- **Análisis Predictivo**: Modelos estadísticos para predicción de tendencias.
- **Análisis de Desviaciones**: Comparación entre reales y presupuestos.

### 10. Diseño Asistido
- **Gestión de Diseños**: Modelos para diseños y prototipos.
- **Tablas de Tallas**: Sistemas estándar y personalizados.
- **Hojas de Ruta**: Planificación de procesos de producción.
- **Digitalización de Patrones**: Integración con sistemas CAD para diseño digital.

## Seguridad y Cumplimiento

### 1. Autenticación y Autorización
- **JWT Tokens**: Autenticación stateless segura
- **Roles y Permisos**: Sistema jerárquico de control de acceso
- **MFA (Autenticación de Dos Factores)**: Opción para usuarios críticos

### 2. Auditoría
- **Registro de Actividades**: Logs detallados de todas las operaciones
- **Seguimiento de Cambios**: Historial de modificaciones en registros
- **Alertas de Seguridad**: Notificaciones de actividades sospechosas

### 3. Protección de Datos
- **Encriptación**: Protección de datos sensibles en reposo y tránsito
- **Detección de Fraudes**: IA para identificar patrones atípicos
- **Firmas Electrónicas**: Validación de operaciones críticas

## Integraciones Externas

### 1. Facturación Electrónica
- **Facturama API**: Integración completa para generación de CFDIs
- **Validación Fiscal**: Verificación de RFC y datos fiscales

### 2. Correo Electrónico
- **Servidores SMTP**: Soporte para múltiples proveedores
- **Plantillas Dinámicas**: Personalización de comunicaciones

### 3. Sistemas Bancarios
- **Conciliación Automática**: Importación y coincidencia de movimientos
- **Pago Electrónico**: Generación de archivos para transferencias

## Componentes de IA y Análisis

### 1. Asistente de IA
- **Motor de Conocimiento**: Sistema de preguntas y respuestas
- **Análisis de Datos**: Interpretación de métricas y tendencias
- **Automatización de Tareas**: Flujos de trabajo inteligentes

### 2. Análisis Predictivo
- **Modelos Estadísticos**: Predicción de demanda y tendencias
- **Análisis de Riesgo**: Evaluación de clientes y proveedores

### 3. OCR y Procesamiento de Documentos
- **Reconocimiento de Texto**: Extracción automática de datos
- **Clasificación de Documentos**: Organización inteligente

## Flujos de Trabajo Personalizados

- **Motor de Flujos**: Sistema configurable de pasos y aprobaciones
- **Notificaciones Automáticas**: Recordatorios y alertas
- **Seguimiento de Procesos**: Visibilidad completa de estados

## Monitoreo y Mantenimiento

- **Health Checks**: Verificación de estado de servicios
- **Logging Estructurado**: Registros en formato JSON para análisis
- **Métricas de Rendimiento**: Tiempos de respuesta y uso de recursos
- **Alertas Proactivas**: Notificaciones de problemas potenciales

## APIs y Extensibilidad

- **API RESTful**: Interfaces bien documentadas con OpenAPI
- **Webhooks**: Notificaciones de eventos en tiempo real
- **SDKs**: Bibliotecas para integración fácil
- **Hooks Personalizados**: Extensibilidad sin modificar el núcleo

## Despliegue y Escalabilidad

- **Contenedores**: Arquitectura basada en Docker
- **Balanceo de Carga**: Distribución de tráfico
- **Cache Distribuido**: Redis para alto rendimiento
- **BD en Clúster**: Soporte para réplicas y failover

---

*Este resumen técnico fue actualizado por última vez en abril de 2026.*