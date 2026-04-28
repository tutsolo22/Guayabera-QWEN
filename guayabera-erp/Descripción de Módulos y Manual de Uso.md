# Guayabera ERP - Descripción de Módulos y Manual de Uso

ERP especializado para la gestión de una PYME dedicada a la fabricación y comercialización de guayaberas yucatecas.

## Tabla de Contenidos

1. [Visión General del Sistema](#visión-general-del-sistema)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Módulos del Sistema](#módulos-del-sistema)
4. [Guías de Usuario](#guías-de-usuario)
5. [API y Documentación Técnica](#api-y-documentación-técnica)
6. [Seguridad y Cumplimiento](#seguridad-y-cumplimiento)
7. [Optimizaciones de Rendimiento](#optimizaciones-de-rendimiento)
8. [Agentes Locales](#agentes-locales)

## Visión General del Sistema

Guayabera ERP es un sistema integral de planificación de recursos empresariales desarrollado específicamente para una empresa dedicada a la fabricación y comercialización de guayaberas yucatecas. El sistema abarca todos los aspectos del negocio, desde la gestión de inventario y producción hasta la facturación electrónica y nómina.

### Características Principales

- Gestión completa de catálogos de productos textiles
- Integración con proveedores de servicios logísticos
- Gestión de proveedores y compras
- Módulo de producción textil
- Gestión de recursos humanos
- Gestión financiera y contable
- Facturación electrónica (CFDI 4.0)
- Nómina electrónica
- Gestión de clientes y CRM
- Control de calidad
- Gestión de activos
- Inteligencia de negocios
- Integración bancaria
- OCR para lectura de documentos
- Agentes locales para tareas intensivas

## Arquitectura del Sistema

### Tecnologías Utilizadas

- **Backend**: Python con FastAPI
- **Frontend**: React.js con TypeScript
- **Base de Datos**: PostgreSQL
- **Caché**: Redis
- **Colas de Trabajo**: Celery
- **Almacenamiento**: Amazon S3 o sistema de archivos local
- **OCR**: Tesseract, OpenCV
- **Facturación Electrónica**: Integração con Facturama
- **Agentes Locales**: Servicios que se instalan en máquinas cliente

### Patrones de Diseño

- Arquitectura de microservicios
- Patrón MVC
- Inyección de dependencias
- ORM con SQLAlchemy

## Módulos del Sistema

### 1. Administración del Sistema

#### 1.1 Gestión de Usuarios
- Creación, edición y eliminación de usuarios
- Asignación de roles y permisos
- Autenticación y autorización
- Auditoría de actividades

#### 1.2 Gestión de Roles
- Definición de roles con permisos específicos
- Asignación de roles a usuarios
- Control de acceso basado en roles (RBAC)

#### 1.3 Configuración del Sistema
- Parámetros generales del sistema
- Configuración de empresa
- Configuración de facturación electrónica
- Configuración de correo electrónico

### 2. Catálogos

#### 2.1 Productos
- Gestión de catálogo de productos
- Clasificación por categorías y subcategorías
- Gestión de tallas y colores
- Especificaciones técnicas
- Ficha técnica de productos textiles

#### 2.2 Clientes
- Gestión de información de clientes
- Segmentación de clientes
- Historial de compras
- Preferencias de clientes

#### 2.3 Proveedores
- Gestión de proveedores
- Categorización de proveedores
- Evaluación de proveedores
- Contactos y relaciones comerciales

#### 2.4 Agentes
- Gestión de vendedores y agentes comerciales
- Comisiones y remuneración
- Zonas de cobertura
- Desempeño comercial

### 3. Compras

#### 3.1 Solicitud de Compras
- Creación de solicitudes de compra
- Flujo de aprobación jerárquico
- Seguimiento de solicitudes

#### 3.2 Órdenes de Compra
- Generación de órdenes de compra
- Seguimiento de entregas
- Recepción de mercancía
- Conciliación con proveedores

### 4. Ventas

#### 4.1 Presupuestos y Cotizaciones
- Creación de cotizaciones
- Conversión de cotizaciones a pedidos
- Seguimiento de oportunidades

#### 4.2 Pedidos de Clientes
- Gestión de pedidos
- Disponibilidad de inventario
- Seguimiento de cumplimiento

#### 4.3 Facturación
- Generación de facturas electrónicas (CFDI 4.0)
- Complementos fiscales (Pago, Carta Porte, Nómina, Comercio Exterior)
- Cancelación de CFDI
- Validación de RFC contra listas negras del SAT
- Acuse de recibido

### 5. Inventario

#### 5.1 Gestión de Almacenes
- Configuración de múltiples almacenes
- Transferencias entre almacenes
- Niveles de stock mínimo y máximo

#### 5.2 Movimientos de Inventario
- Entradas y salidas de productos
- Ajustes de inventario
- Control de lotes y fechas de vencimiento

#### 5.3 Valorización de Inventario
- Métodos de valorización (PEPS, UEPS, Promedio)
- Costeo de productos
- Evaluación de inventarios

### 6. Producción

#### 6.1 Planificación de Producción
- Planificación maestra de producción
- Requisiciones de materiales
- Programación de órdenes de trabajo

#### 6.2 Órdenes de Producción
- Creación y seguimiento de órdenes
- Asignación de recursos
- Control de avance de producción

#### 6.3 Recetas de Producción
- Fichas técnicas de productos
- Lista de materiales (BOM)
- Procesos de manufactura

### 7. CAD (Diseño Asistido por Computadora)

#### 7.1 Diseño de Productos
- Biblioteca de diseños de guayaberas
- Gestión de patrones y moldes
- Versionado de diseños

#### 7.2 Hojas de Talla
- Generación de hojas de talla
- Optimización de corte
- Control de desperdicios

### 8. RRHH

#### 8.1 Empleados
- Gestión de información de empleados
- Contratos y puestos
- Historial laboral

#### 8.2 Nómina Electrónica
- Timbrado de nómina (CFDI complemento de nómina)
- Incidencias laborales (incapacidades, faltas, permisos)
- Percepciones y deducciones configurables
- Integración con calendario fiscal
- Cálculo de impuestos (ISR, IMSS, Infonavit)

#### 8.3 Beneficios
- Gestión de beneficios
- Seguros médicos
- Vacaciones y días libres

### 9. Finanzas

#### 9.1 Contabilidad General
- Plan de cuentas
- Asientos contables
- Polizas de entrada, salida y ajuste

#### 9.2 Cuentas por Cobrar
- Gestión de clientes
- Seguimiento de cobranza
- Estados de cuenta

#### 9.3 Cuentas por Pagar
- Gestión de proveedores
- Seguimiento de pagos
- Estados de cuenta

#### 9.4 Bancos
- Conciliación bancaria
- Integración con sistemas bancarios
- Control de flujos de efectivo

#### 9.5 Presupuestos
- Elaboración de presupuestos
- Seguimiento de desviaciones
- Análisis de desempeño

### 10. Logística

#### 10.1 Gestión de Almacenes
- Distribución de productos
- Control de picking y packing
- Gestión de rutas

#### 10.2 Transporte
- Gestión de proveedores de transporte
- Seguimiento de envíos
- Costos de logística

### 11. CRM (Gestión de Relación con Clientes)

#### 11.1 Gestión de Leads
- Captura de leads
- Calificación de prospects
- Conversión a clientes

#### 11.2 Atención a Clientes
- Gestión de tickets
- Canal multimedios
- Historial de interacciones

### 12. Gestión de Proyectos

#### 12.1 Planeación de Proyectos
- Definición de proyectos
- Asignación de recursos
- Cronogramas y hitos

#### 12.2 Seguimiento
- Control de avance
- Presupuestos de proyecto
- Gestión de tareas

### 13. Gestión de Activos

#### 13.1 Inventario de Activos
- Registro de activos fijos
- Depreciación de activos
- Mantenimiento de activos

### 14. Control de Calidad

#### 14.1 Procedimientos de Control
- Estándares de calidad
- Procedimientos de inspección
- Certificaciones

#### 14.2 Incidencias de Calidad
- Reporte de defectos
- Acciones correctivas
- Estadísticas de calidad

### 15. Inteligencia de Negocios

#### 15.1 Reportes
- Reportes financieros
- KPIs de negocio
- Análisis de tendencias

#### 15.2 Cuadros de Mando
- Dashboards ejecutivos
- Alertas de negocio
- Indicadores clave de desempeño

### 16. Help Desk

#### 16.1 Gestión de Tickets
- Creación de tickets
- Asignación de prioridades
- Seguimiento de resolución

#### 16.2 Base de Conocimiento
- Artículos de ayuda
- Procedimientos documentados
- Soluciones comunes

### 17. Gestión Avanzada de Contabilidad

#### 17.1 Conciliación Automática
- Reglas de conciliación
- Validación de movimientos
- Identificación de diferencias

#### 17.2 Análisis de Costos
- Centros de costo
- Distribución de costos
- Costeo de productos

### 18. Requisiciones

#### 18.1 Solicitudes Internas
- Solicitud de materiales
- Flujo de aprobación
- Seguimiento de autorizaciones

### 19. Notificaciones

#### 19.1 Sistema de Alertas
- Notificaciones automáticas
- Canales de comunicación
- Personalización de alertas

### 20. Cadena de Suministro

#### 20.1 Gestión de Proveedores
- Evaluación de proveedores
- KPIs de desempeño
- Contratos con proveedores

#### 20.2 Compras Estratégicas
- Análisis de compras
- Negociación con proveedores
- Gestión de contratos

## Guías de Usuario

### Configuración Inicial

1. Crear el usuario administrador
2. Configurar la información de la empresa
3. Establecer el plan de cuentas
4. Configurar catálogos de productos
5. Establecer proveedores y clientes iniciales
6. Configurar parámetros de facturación electrónica

### Flujo de Trabajo Principal

1. **Planeación**: Definir requerimientos de producción
2. **Compras**: Adquirir materias primas
3. **Producción**: Fabricar productos terminados
4. **Ventas**: Atender pedidos de clientes
5. **Inventario**: Controlar stocks
6. **Facturación**: Emitir CFDIs
7. **Finanzas**: Registrar operaciones contables
8. **Reportes**: Analizar resultados

## API y Documentación Técnica

### API RESTful

El sistema expone una API RESTful completa con endpoints para todos los módulos. La documentación interactiva está disponible en `/docs` y `/redoc`.

### Endpoints Principales

- `/api/v1/auth` - Autenticación
- `/api/v1/admin` - Administración
- `/api/v1/finance` - Finanzas
- `/api/v1/inventory` - Inventario
- `/api/v1/production` - Producción
- `/api/v1/sales` - Ventas
- `/api/v1/hr` - Recursos Humanos
- `/api/v1/invoice` - Facturación Electrónica
- `/api/v1/payroll` - Nómina Electrónica
- `/api/v1/agents` - Agentes Locales

## Seguridad y Cumplimiento

### Medidas de Seguridad

- Autenticación multifactor (MFA)
- Cifrado de datos sensibles
- Auditoría completa de todas las operaciones
- Control de accesos basado en roles
- Registro de sesiones de usuario
- Monitoreo de seguridad

### Cumplimiento Fiscal

- Facturación electrónica CFDI 4.0
- Nómina electrónica con complemento SAT
- Validación de RFC contra listas negras
- Reportes fiscales conforme a regulaciones

## Optimizaciones de Rendimiento

### Caching
- Redis para datos frecuentes
- Caching de resultados de consultas
- Caching de objetos complejos

### Colas de Trabajo
- Celery para operaciones asíncronas
- Procesamiento en segundo plano
- Tareas de larga duración

### Índices de Base de Datos
- Índices optimizados para consultas frecuentes
- Índices compuestos para búsquedas complejas
- Análisis de planes de ejecución

### Paginación
- Paginación eficiente para listados grandes
- Paginación basada en cursores
- Consultas optimizadas

### Consultas Optimizadas
- Carga selectiva de relaciones
- Joins optimizados
- Filtrado eficiente

## Agentes Locales

### 1. Descripción General

Los agentes locales son servicios que se instalan en las máquinas de los clientes para realizar tareas intensivas de cómputo, como el procesamiento CAD, el diseño de patrones y la impresión de documentos. Esto permite delegar tareas pesadas a las máquinas locales, reduciendo la carga del servidor central y ahorrando costos de infraestructura.

### 2. Tipos de Agentes

#### 2.1 Agente CAD
- Se encarga de operaciones de diseño asistido por computadora
- Genera patrones y fichas técnicas
- Optimiza el uso de material
- Exporta en diversos formatos (DXF, SVG, PDF)

#### 2.2 Agente de Impresión
- Se encarga de imprimir documentos desde la aplicación web
- Maneja impresoras locales
- Permite seleccionar impresoras específicas
- Soporta impresión en lote

#### 2.3 Agente de Diseño
- Se encarga de renderizar diseños complejos
- Aplica efectos visuales
- Genera vistas previas
- Exporta en múltiples formatos y resoluciones

### 3. Funcionalidades

#### 3.1 Registro de Agentes
- Los agentes se registran automáticamente en el servidor
- Se verifica la autenticación mediante tokens seguros
- Se actualiza la disponibilidad y estado del agente

#### 3.2 Asignación de Tareas
- Distribución automática de tareas entre agentes disponibles
- Balanceo de carga simple
- Seguimiento del progreso de las tareas
- Gestión de errores y reintentos

#### 3.3 Comunicación Segura
- Autenticación mediante tokens únicos por agente
- Validación de identidad del agente
- Cifrado de datos sensibles durante la transmisión

#### 3.4 Supervisión
- Monitoreo del estado de los agentes
- Verificación periódica del estado (heartbeats)
- Alertas cuando un agente deja de responder
- Reportes de rendimiento y utilización

### 4. Implementación Técnica

#### 4.1 API para Agentes
- Endpoints para el registro de nuevos agentes
- Endpoints para la actualización de estado (heartbeats)
- Endpoints para la asignación y ejecución de tareas
- Endpoints para la consulta de estado y capacidades

#### 4.2 Servicio de Comunicación
- Servicio centralizado para la comunicación con agentes
- Gestión de colas de tareas
- Manejo de errores y timeouts
- Registro de operaciones y eventos

#### 4.3 Seguridad
- Generación automática de tokens seguros para cada agente
- Validación de identidad en cada comunicación
- Control de acceso basado en tipos de agentes
- Registro de todas las operaciones en el sistema de auditoría

### 5. Ventajas del Sistema de Agentes

1. **Reducción de Carga del Servidor**: Las tareas intensivas se ejecutan localmente
2. **Mejora de Rendimiento**: Procesamiento más rápido gracias a la potencia local
3. **Ahorro de Costos**: Menos infraestructura de servidor necesaria
4. **Escalabilidad**: Fácil adición de nuevos agentes según demanda
5. **Flexibilidad**: Soporte para diferentes tipos de tareas especializadas
6. **Disponibilidad**: Funcionalidades disponibles incluso con conexión intermitente

---

## Módulos Implementados

Hasta la fecha, se han implementado los siguientes módulos y funcionalidades:

### Módulo de Administración
- Gestión de usuarios, roles y permisos
- Configuración general del sistema
- Gestión de empresas y sucursales

### Módulo de Seguridad
- Autenticación y autorización
- Auditoría de actividades
- Sesiones de usuario

### Módulo de Finanzas
- Plan de cuentas
- Polizas contables
- Cuentas por cobrar y pagar
- Bancos y conciliación
- Presupuestos
- Monitoreo contable

### Módulo de Cadena de Suministro
- Gestión de proveedores
- Compras y órdenes de compra
- Contratos con proveedores

### Módulo de Producción
- Gestión de productos textiles
- Recetas de producción
- Control de calidad
- Gestión de tallas y colores
- Fichas técnicas

### Módulo de RRHH
- Gestión de empleados
- Departamentos y puestos
- Contratos y nómina

### Módulo de Ventas
- Clientes y prospectos
- Oportunidades de venta
- Cotizaciones y pedidos
- Precios por cliente

### Módulo de CAD y Diseño
- Gestión de diseños de productos
- Biblioteca de patrones
- Fichas técnicas de productos

### Módulo de Tallas
- Sistemas de tallas
- Grupos de tallas
- Relaciones de tallas

### Módulo de Help Desk
- Gestión de tickets
- Base de conocimiento
- Priorización de casos

### Módulo de Requisiciones
- Solicitudes internas
- Flujos de aprobación

### Módulo de Notificaciones
- Sistema de alertas
- Canales de notificación
- Personalización de mensajes

### Módulo de Control de Calidad
- Procedimientos de control
- Incidencias de calidad
- Certificaciones

### Módulo de Contabilidad Avanzada
- Conciliación automática
- Análisis de costos
- Distribución de gastos

### Módulo de Logística
- Gestión de almacenes
- Transporte y envíos
- Control de inventario

### Módulo de CRM
- Gestión de clientes
- Leads y oportunidades
- Atención al cliente

### Módulo de Gestión de Proyectos
- Planeación de proyectos
- Asignación de recursos
- Seguimiento de avances

### Módulo de Gestión de Activos
- Inventario de activos fijos
- Depreciación de activos
- Mantenimiento de activos

### Módulo de Inteligencia de Negocios
- Reportes financieros
- KPIs de negocio
- Dashboards ejecutivos

### Módulo de Facturación Electrónica
- Comprobantes fiscales (CFDI 4.0)
- Conceptos y cálculo de impuestos
- Relación de facturas
- Timbrado con Facturama
- Complementos fiscales (Pago, Carta Porte, Nómina, Comercio Exterior)
- Cancelación de CFDI
- Validación de RFC

### Módulo de Configuración de Correo
- Configuración SMTP
- Historial de envíos
- Prueba de configuración

### Módulo de Nómina Electrónica
- Períodos de nómina
- Recibos de nómina
- Percepciones y deducciones
- Incapacidades
- Otros pagos
- Integración con Facturama para timbrado

### Módulo de Agentes Locales
- Tipos de agentes (CAD, Impresión, Diseño)
- Registro y autenticación de agentes
- Asignación automática de tareas
- Comunicación segura entre servidor y agentes
- Supervisión y monitoreo de agentes
- Balanceo de carga entre agentes disponibles

### Optimizaciones Implementadas
- Caching con Redis
- Colas de tareas con Celery
- Middleware de caché para API
- Índices de base de datos
- Paginación eficiente
- Consultas optimizadas
- Sistema de monitoreo y health checks
- Motor de workflows
- OCR para lectura de documentos
- Integración bancaria
- Sistema de seguridad con MFA

Todos los módulos implementados siguen las mejores prácticas de desarrollo, seguridad y cumplimiento fiscal para operar en México.