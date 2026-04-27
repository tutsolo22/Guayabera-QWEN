# 🤖 Sistema de Agentes de Codificación - GuayaberaERP

## Descripción

Sistema inteligente de agentes autónomos para acelerar el desarrollo del ERP. Cada agente está especializado en una área específica del desarrollo de software.

## 📋 Agentes Implementados (Fase 2)

### 1. **Database Agent** (`database_agent`)
Especializado en generación de código de base de datos.

**Capacidades:**
- `generate_model`: Genera modelos SQLAlchemy automáticamente
- `generate_schema`: Crea esquemas Pydantic para validación
- `generate_crud`: Genera funciones CRUD completas
- `analyze_existing_models`: Analiza modelos existentes

**Ejemplo de uso:**
```bash
curl -X POST http://localhost:8000/api/v1/agents/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "database_agent",
    "action": "analyze_models",
    "parameters": {}
  }'
```

### 2. **Testing Agent** (`testing_agent`)
Especializado en generación de pruebas automatizadas.

**Capacidades:**
- `generate_unit_test`: Crea pruebas unitarias con pytest
- `generate_integration_test`: Genera pruebas de integración
- `generate_api_test`: Crea pruebas específicas de API
- `generate_fixture`: Genera fixtures para tests
- `analyze_test_coverage`: Analiza cobertura de pruebas

**Ejemplo de uso:**
```bash
curl -X POST http://localhost:8000/api/v1/agents/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "testing_agent",
    "action": "generate_unit_test",
    "parameters": {
      "module_name": "finance",
      "function_name": "create_transaction",
      "module_type": "crud"
    }
  }'
```

### 3. **UI/UX Agent** (`uiux_agent`)
Especializado en generación de componentes React y páginas.

**Capacidades:**
- `generate_component`: Crea componentes React reutilizables
- `generate_page`: Genera páginas completas con CRUD
- `generate_service`: Crea servicios API TypeScript
- `generate_form`: Genera formularios con validación
- `generate_table`: Crea tablas con Ant Design
- `analyze_ui_structure`: Analiza estructura UI existente

**Ejemplo de uso:**
```bash
curl -X POST http://localhost:8000/api/v1/agents/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "uiux_agent",
    "action": "generate_page",
    "parameters": {
      "page_name": "purchase_orders",
      "has_crud": true,
      "api_endpoint": "/api/v1/purchases"
    }
  }'
```

## 🏗️ Arquitectura

```
agents/
├── core/                    # Núcleo del sistema
│   └── __init__.py         # BaseAgent, AgentOrchestrator
├── database_agent/         # Agente de base de datos
│   └── __init__.py
├── testing_agent/          # Agente de pruebas
│   └── __init__.py
├── uiux_agent/             # Agente de UI/UX
│   └── __init__.py
├── structure_agent/        # Agente de estructura (pendiente)
├── security_agent/         # Agente de seguridad (pendiente)
└── coding_agent/           # Agente de codificación (pendiente)
```

## 🔌 Endpoints API

### Listar agentes disponibles
```bash
GET /api/v1/agents/
```

### Obtener estado de un agente
```bash
GET /api/v1/agents/{agent_name}/status
```

### Ejecutar tarea en agente
```bash
POST /api/v1/agents/execute
{
  "agent_type": "database_agent",
  "action": "generate_model",
  "parameters": {
    "model_name": "PurchaseOrder",
    "table_name": "purchase_orders",
    "fields": [
      {"name": "supplier_id", "type": "Integer", "nullable": false},
      {"name": "total_amount", "type": "Float", "nullable": false}
    ]
  }
}
```

### Análisis automático
```bash
# Analizar modelos de base de datos
POST /api/v1/agents/database/analyze

# Analizar cobertura de tests
POST /api/v1/agents/testing/coverage

# Analizar estructura UI
POST /api/v1/agents/uiux/analyze
```

## 📝 Flujo de Trabajo Típico

### Para crear un nuevo módulo completo:

1. **Database Agent** genera modelo, schema y CRUD
2. **Coding Agent** crea endpoints API (pendiente)
3. **Testing Agent** genera pruebas automáticas
4. **UI/UX Agent** crea página y componentes frontend
5. **Security Agent** verifica permisos (pendiente)
6. **Structure Agent** valida calidad de código (pendiente)

## 🚀 Próximos Agentes (Fase 3)

### Coding Agent
- Generación automática de endpoints API
- Creación de lógica de negocio
- Integración con servicios externos

### Structure Agent
- Análisis de calidad de código
- Detección de code smells
- Sugerencias de refactorización
- Verificación de patrones de diseño

### Security Agent
- Escaneo de vulnerabilidades
- Verificación de permisos RBAC
- Auditoría de código sensible
- Validación de sanitización de inputs

## 💡 Ejemplos de Uso

### Ejemplo 1: Crear módulo de Compras completo

```python
# 1. Generar modelo
POST /api/v1/agents/execute
{
  "agent_type": "database_agent",
  "action": "generate_model",
  "parameters": {
    "model_name": "PurchaseOrder",
    "fields": [
      {"name": "supplier_id", "type": "Integer", "nullable": False},
      {"name": "order_date", "type": "DateTime", "nullable": False},
      {"name": "total_amount", "type": "Float", "nullable": False},
      {"name": "status", "type": "String", "nullable": False}
    ]
  }
}

# 2. Generar schema
POST /api/v1/agents/execute
{
  "agent_type": "database_agent",
  "action": "generate_schema",
  "parameters": {
    "schema_name": "PurchaseOrder",
    "fields": [
      {"name": "supplier_id", "python_type": "int"},
      {"name": "order_date", "python_type": "datetime"},
      {"name": "total_amount", "python_type": "float"},
      {"name": "status", "python_type": "str"}
    ]
  }
}

# 3. Generar CRUD
POST /api/v1/agents/execute
{
  "agent_type": "database_agent",
  "action": "generate_crud",
  "parameters": {
    "model_name": "PurchaseOrder",
    "schema_name": "PurchaseOrder"
  }
}

# 4. Generar pruebas
POST /api/v1/agents/execute
{
  "agent_type": "testing_agent",
  "action": "generate_integration_test",
  "parameters": {
    "module_name": "purchase_orders",
    "endpoint": "/api/v1/purchase-orders"
  }
}

# 5. Generar página frontend
POST /api/v1/agents/execute
{
  "agent_type": "uiux_agent",
  "action": "generate_page",
  "parameters": {
    "page_name": "purchase_orders",
    "has_crud": True,
    "api_endpoint": "/api/v1/purchase-orders"
  }
}
```

## 📊 Estado del Sistema

| Agente | Estado | Versión | Prioridad |
|--------|--------|---------|-----------|
| Database Agent | ✅ Activo | 1.0.0 | Alta |
| Testing Agent | ✅ Activo | 1.0.0 | Alta |
| UI/UX Agent | ✅ Activo | 1.0.0 | Alta |
| Coding Agent | ⏳ Pendiente | - | Media |
| Structure Agent | ⏳ Pendiente | - | Media |
| Security Agent | ⏳ Pendiente | - | Baja |

## 🔧 Configuración

Los agentes utilizan las siguientes dependencias:
- `jinja2>=3.1.0`: Para templates de código
- `pydantic`: Para validación de datos
- `fastapi`: Para endpoints API

## 📈 Métricas

Cada agente reporta:
- Estado actual (idle, running, completed, error)
- Progreso de la tarea (0-100%)
- Tiempo de ejecución
- Errores encontrados

## 🛠️ Desarrollo Futuro

- Integración con IA para generación más inteligente
- Soporte para múltiples lenguajes de programación
- Plantillas personalizables por proyecto
- Historial de tareas ejecutadas
- Sistema de colas para tareas asíncronas
