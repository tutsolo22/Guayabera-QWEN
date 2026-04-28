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

*Este resumen técnico fue actualizado por última vez en mayo de 2025.*