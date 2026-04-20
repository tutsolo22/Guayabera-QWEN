# 🚀 GUÍA COMPLETA: Levantar GuayaberaERP

**Última actualización:** 16 de Abril de 2026  
**Estado:** ✅ Listo para ejecutar  
**Versión:** 0.1.0

---

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Levantar con Docker (Recomendado)](#levantar-con-docker-recomendado)
3. [Servicios Disponibles](#servicios-disponibles)
4. [Primeras Pruebas](#primeras-pruebas)
5. [Solución de Problemas](#solución-de-problemas)

---

## 📦 Requisitos Previos

Asegúrate de tener instalado:

| Software | Versión | Link |
|----------|---------|------|
| Docker Desktop | Último | https://www.docker.com/products/docker-desktop |
| Windows Terminal (Opcional) | Último | Microsoft Store |

**Verificar instalaciones:**

```powershell
docker --version
docker-compose --version
```

**Resultado esperado:**
```
Docker version 24.0.0+
Docker Compose version 2.x+
```

---

## 🐳 Levantar con Docker (Recomendado)

### Paso 1: Verificar Carpeta del Proyecto

```powershell
cd C:\Users\Choripapa\Documents\Proyectos\Guayabera-QWEN\guayabera-erp
dir
```

**Debería mostrar:**
```
📁 backend/
📁 frontend/
📁 docker/
📁 database/
📁 docs/
📄 docker-compose.yml
📄 .env (backend)
... otros archivos
```

### Paso 2: Limpiar Contenedores Anteriores (Si existen)

```powershell
# Detener todos
docker-compose down

# Si quieres eliminar volúmenes (¡cuidado, borra datos!)
# docker-compose down -v
```

### Paso 3: Levantar Todo

```powershell
# Desde la raíz del proyecto
docker-compose up -d

# Ver el progreso (opcional)
docker-compose logs -f
```

**Esto tomará 2-3 minutos la primera vez.**

### Paso 4: Esperar a que Termine

Verás mensajes como:

```
[+] Running 7/7
 ✓ Network guayabera-network Created
 ✓ Container guayabera-erp-db          Running (health: starting)
 ✓ Container guayabera-erp-redis       Running (health: starting)
 ✓ Container guayabera-erp-api         Running
 ✓ Container guayabera-erp-web         Running
 ✓ Container guayabera-erp-worker      Running
 ✓ Container guayabera-erp-pgadmin     Running
```

### Paso 5: Verificar Estado

```powershell
docker-compose ps
```

**Resultado esperado:**

```
CONTAINER ID  IMAGE  COMMAND  CREATED  STATUS
guayabera-erp-db         postgres:15      Up 2 minutes (healthy)
guayabera-erp-redis      redis:7          Up 2 minutes (healthy)
guayabera-erp-api        fastapi          Up 1 minute
guayabera-erp-web        react            Up 1 minute
guayabera-erp-worker     celery           Up 1 minute
guayabera-erp-beat       celery-beat      Up 1 minute
guayabera-erp-pgadmin    pgadmin4         Up 1 minute
```

✅ **Si todos dicen "Up", ¡vas bien!**

---

## 🌐 Servicios Disponibles

Abre estas URLs en tu navegador:

| Servicio | URL | Credenciales | Descripción |
|----------|-----|--------------|-------------|
| **Frontend** | http://localhost:3000 | admin / admin123456 | La aplicación web |
| **API Docs** | http://localhost:8000/docs | - | Documentación Swagger |
| **API (Redoc)** | http://localhost:8000/redoc | - | Documentación alternativa |
| **PgAdmin** | http://localhost:5050 | admin@guayabera-erp.com / admin123 | Gestor de BD |

---

## ✅ Primeras Pruebas

### Test 1: Verificar Backend

```powershell
curl http://localhost:8000
```

**Respuesta esperada:**
```json
{
  "message": "GuayaberaERP API",
  "version": "0.1.0",
  "status": "running"
}
```

### Test 2: Abrir Frontend

1. Ve a http://localhost:3000
2. Deberías ver la página de **Login**
3. Usa estas credenciales:
   - **Usuario:** `admin`
   - **Contraseña:** `admin123456`

### Test 3: Dashboard

Después de login, verás:
- ✅ Estadísticas de contabilidad
- ✅ Pólizas registradas
- ✅ Cuentas bancarias
- ✅ Asientos automáticos

### Test 4: Importar Catálogo SAT (Importante)

En la interfaz, ve a:

**Contabilidad → Catálogo de Cuentas**

Haz clic en el botón **"Importar Catálogo SAT"** (el primero que aparece).

Deberías ver el mensaje:
```
✅ Catálogo importado: 115 cuentas
```

### Test 5: Crear una Póliza de Prueba

1. Ve a **Contabilidad → Pólizas**
2. Haz clic en **"Nueva Póliza"**
3. Completa los datos:

| Campo | Valor |
|-------|-------|
| Tipo | Diario |
| Descripción | Póliza de prueba |
| Centro de Costo | Operaciones |

4. Añade dos movimientos:

**Movimiento 1 (Cargo):**
- Cuenta: 1101040001 (Inventario MP)
- Cargo: $10,000
- Abono: $0

**Movimiento 2 (Abono):**
- Cuenta: 2101010001 (Proveedores)
- Cargo: $0
- Abono: $10,000

5. Verifica que aparezca el indicador **✅ Póliza Cuadrada**
6. Haz clic en **Guardar**

✅ **¡Tu primera póliza está lista!**

---

## 🔍 Ver Logs

Para ver lo que está pasando en tiempo real:

```powershell
# Todos los logs
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend

# Solo BD
docker-compose logs -f postgres

# Solo Redis
docker-compose logs -f redis

# Solo Celery
docker-compose logs -f celery-worker
```

**Para salir:** Presiona `Ctrl + C`

---

## 🛑 Detener Todo

```powershell
# Detener los servicios
docker-compose stop

# Detener y eliminar contenedores
docker-compose down

# Detener todo Y borrar volúmenes (¡cuidado!)
docker-compose down -v
```

---

## 🐛 Solución de Problemas

### ❌ Error: Puerto 3000 o 8000 ya en uso

**Problema:**
```
bind: address already in use
```

**Solución:**

```powershell
# Encontrar proceso
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Matar proceso (reemplaza PID)
taskkill /PID <PID> /F
```

Ejemplo:
```powershell
taskkill /PID 12345 /F
```

### ❌ Error: PostgreSQL no inicia

**Problema:**
```
failed to initialize database
```

**Solución:**

```powershell
# Limpiar volúmenes
docker-compose down -v

# Volver a levantar
docker-compose up -d
```

### ❌ Error: Frontend no conecta con Backend

**Problema:**
```
Failed to fetch from http://localhost:8000
```

**Solución:**

1. Verifica que el backend esté corriendo:
   ```powershell
   docker-compose ps backend
   ```

2. Verifica los logs del backend:
   ```powershell
   docker-compose logs backend
   ```

3. Recarga el navegador (Ctrl + F5)

### ❌ Error: Login no funciona

**Problema:**
```
Invalid credentials
```

**Solución:**

Las credenciales por defecto son:
- **Usuario:** `admin`
- **Contraseña:** `admin123456`

Si siguen sin funcionar:

```powershell
# Resetear BD
docker-compose down -v
docker-compose up -d

# Esperar 30 segundos
# Intentar de nuevo
```

### ❌ Conflicto de Dependencias npm

**Ya está arreglado en el Dockerfile.frontend con `--legacy-peer-deps`**

Si aún así falla:

```powershell
# Reconstruir imagen
docker-compose build --no-cache frontend

# Levantar de nuevo
docker-compose up -d
```

### ❌ Celery no procesa tareas

**Verificar que esté corriendo:**

```powershell
docker-compose logs celery-worker
```

**Si ves errores, reinicia:**

```powershell
docker-compose restart celery-worker
docker-compose restart celery-beat
```

---

## 📊 Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────┐
│         GUAYABERA ERP COMPLETO                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Frontend (React)         Backend (FastAPI)         │
│  ✓ Login                 ✓ Autenticación JWT       │
│  ✓ Dashboard             ✓ Contabilidad            │
│  ✓ Pólizas               ✓ Bancos                  │
│  ✓ Balanza               ✓ Asientos Automáticos    │
│  ✓ Administración         ✓ Monitoreo              │
│  ✓ Usuarios              ✓ APIs RESTful            │
│                                                     │
│  puerto: 3000            puerto: 8000              │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  PostgreSQL Database       Redis Cache              │
│  ✓ 17 tablas             ✓ Sesiones               │
│  ✓ Datos completos       ✓ Caché                  │
│  ✓ SAT integrado         ✓ Colas                  │
│                                                     │
│  puerto: 5432            puerto: 6379             │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Celery Workers          PgAdmin                   │
│  ✓ Procesamiento async   ✓ Gestor BD             │
│  ✓ Reintentos            ✓ Puerto: 5050          │
│  ✓ Tareas programadas    ✓ Estadísticas          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 📈 Progreso del Proyecto

| Módulo | Estado | Líneas |
|--------|--------|--------|
| 1.1 Administración | ✅ 100% | 650 |
| 1.2 Contabilidad | ✅ 100% | 900 |
| 1.3 Usuarios/Permisos | ✅ 100% | 400 |
| 1.4 Asientos Automáticos | ✅ 100% | 1,560 |
| **Frontend Visual** | ✅ 100% | 1,850 |
| **Otros Módulos** | ⏳ Pendiente | - |
| **TOTAL** | 🟡 ~20% | 5,360 |

---

## 🎯 Próximos Pasos

Una vez que todo esté corriendo:

1. ✅ Probar Login
2. ✅ Importar Catálogo SAT
3. ✅ Crear Pólizas
4. ⏳ Desarrollar Módulo de Compras
5. ⏳ Integrar Inventarios (3 niveles)
6. ⏳ Módulo de Producción Textil

---

## 📞 Soporte Rápido

| Pregunta | Respuesta |
|----------|-----------|
| ¿Dónde está la documentación? | `docs/` carpeta |
| ¿Cómo agrego usuarios? | Frontend → Admin → Usuarios |
| ¿Cómo veo errores? | `docker-compose logs -f` |
| ¿Puedo modificar código? | Sí, los volúmenes están mapeados |

---

## ✨ ¡Listo!

Ahora tienes un ERP textil completo corriendo localmente.

**Próximo paso:** Abre http://localhost:3000 y ¡comienza a usar GuayaberaERP! 🎉

---

*Documento creado: Abril 2026*  
*Proyecto: GuayaberaERP v0.1.0*
