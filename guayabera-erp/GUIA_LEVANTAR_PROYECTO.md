# Guía para Levantar el Proyecto Guayabera ERP

## Requisitos del Sistema

- Python 3.11+
- Node.js 18+
- PostgreSQL 13+
- Redis
- Docker (opcional pero recomendado)
- Git

## Instalación Paso a Paso

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/guayabera-erp.git
cd guayabera-erp
```

### 2. Configurar el Entorno Backend

#### 2.1 Crear entorno virtual

```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

#### 2.2 Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 2.3 Configurar variables de entorno

Crea un archivo `.env` en el directorio `backend/app/` con el siguiente contenido:

```env
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/guayabera_erp
SECRET_KEY=tu_clave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
FACTURAMA_ENVIRONMENT=development
FACTURAMA_API_KEY=tu_api_key
FACTURAMA_API_LOGIN=tu_login
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=tu_correo@gmail.com
EMAIL_PASSWORD=tu_contraseña
```

### 3. Configurar la Base de Datos

#### 3.1 Iniciar PostgreSQL

Asegúrate de tener PostgreSQL instalado y en ejecución.

#### 3.2 Crear la base de datos

```sql
CREATE DATABASE guayabera_erp;
CREATE USER usuario WITH PASSWORD 'contraseña';
GRANT ALL PRIVILEGES ON DATABASE guayabera_erp TO usuario;
```

#### 3.3 Ejecutar migraciones

```bash
cd backend/app
alembic upgrade head
```

### 4. Configurar Redis

Asegúrate de tener Redis instalado y en ejecución:

```bash
# Iniciar Redis (dependiendo de tu sistema)
redis-server
```

### 5. Configurar el Entorno Frontend

#### 5.1 Ir al directorio frontend

```bash
cd ../frontend  # Desde el directorio backend
```

#### 5.2 Instalar dependencias

```bash
npm install
```

#### 5.3 Configurar variables de entorno

Crea un archivo `.env` en el directorio `frontend/` con el siguiente contenido:

```env
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_WS_URL=ws://localhost:8000/ws
```

### 6. Iniciar los Servicios

#### 6.1 Backend

Desde el directorio `backend/app/`:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 6.2 Frontend

Desde otro terminal, en el directorio `frontend/`:

```bash
npm start
```

#### 6.3 Celery Worker (opcional)

Para procesar tareas asíncronas:

```bash
celery -A app.tasks worker --loglevel=info
```

#### 6.4 Celery Beat (opcional)

Para ejecutar tareas programadas:

```bash
celery -A app.tasks beat --loglevel=info
```

## Configuración con Docker (Alternativa)

Si prefieres usar Docker, puedes seguir estos pasos:

### 1. Construir y levantar contenedores

```bash
docker-compose up --build
```

### 2. Ejecutar migraciones (una vez que los contenedores estén arriba)

```bash
docker-compose exec backend alembic upgrade head
```

## Configuración de Facturama

Para usar la funcionalidad de facturación electrónica:

1. Regístrate en [Facturama](https://www.facturama.mx/)
2. Obtén tus credenciales de API
3. Configura las variables de entorno correspondientes

## Configuración de Correos Electrónicos

Para enviar correos electrónicos desde el sistema:

1. Configura un servidor SMTP (como Gmail o Outlook)
2. Asegúrate de habilitar el acceso de aplicaciones menos seguras o usar OAuth2
3. Configura las variables de entorno correspondientes

## Configuración de Notificaciones

El sistema incluye un servicio de notificaciones que puede enviar mensajes a través de diferentes canales:

1. Notificaciones por correo electrónico
2. Notificaciones push en el navegador
3. Notificaciones en tiempo real a través de WebSocket

## Configuración de Seguridad

El sistema incluye múltiples capas de seguridad:

1. Autenticación JWT
2. Control de permisos por roles
3. Auditoría de seguridad
4. Encriptación de datos sensibles
5. Detección de fraudes

## Configuración de Backup

Para configurar backups regulares de la base de datos:

```bash
# Script de ejemplo para backup diario
pg_dump guayabera_erp > backup_$(date +%Y%m%d_%H%M%S).sql
```

## Solución de Problemas Comunes

### Error de conexión a la base de datos

- Verifica que PostgreSQL esté corriendo
- Confirma que las credenciales en `.env` sean correctas
- Asegúrate de que el puerto 5432 esté disponible

### Error de CORS

- Verifica la configuración de CORS en `main.py`
- Asegúrate de que el frontend esté corriendo en el dominio permitido

### Error con dependencias

- Asegúrate de usar la versión correcta de Python
- Considera usar un entorno virtual
- Verifica que `requirements.txt` esté actualizado

## Configuración de Producción

Para desplegar en producción:

1. Configura SSL/TLS
2. Usa un proxy inverso como NGINX
3. Configura balanceo de carga si es necesario
4. Habilita compresión GZIP
5. Configura monitoreo y logging
6. Establece políticas de backup automáticas

## Actualizaciones

Para actualizar el sistema a la última versión:

```bash
git pull origin main
pip install -r requirements.txt  # Backend
npm install  # Frontend
alembic upgrade head  # Aplicar migraciones
```

---

*Esta guía fue actualizada por última vez en marzo de 2023.*