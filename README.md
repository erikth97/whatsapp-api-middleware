# WhatsApp API Middleware

API middleware para sistema de notificaciones WhatsApp del Centro de Atención a Clientes (CAT) de Motomex.

## 📋 Descripción

Sistema de notificaciones automáticas vía WhatsApp Business para reducir volumen de llamadas al CAT en 60-70%. Integra el sistema Motomex con n8n y Respond.io para envío automatizado de actualizaciones de pedidos.

## 🏗️ Arquitectura
```
Sistema Motomex → API Middleware → n8n → Respond.io → WhatsApp Business API
```

## 🚀 Stack Tecnológico

- **Backend:** FastAPI (Python 3.12)
- **Containerización:** Docker + Docker Compose
- **Reverse Proxy:** Traefik (SSL automático con Let's Encrypt)
- **Automatización:** n8n
- **Mensajería:** Respond.io + WhatsApp Business API
- **CI/CD:** GitHub Actions
- **Hosting:** VPS Hostinger (Ubuntu 24.04)

## 📦 Requisitos

### Local
- Python 3.12+
- pip
- virtualenv

### Producción
- Docker 28.5+
- Docker Compose v2.40+
- Traefik configurado
- Dominio con DNS configurado

## 🔧 Instalación Local
```bash
# Clonar repositorio
git clone git@github.com:erikth97/whatsapp-api-middleware.git
cd whatsapp-api-middleware

# Crear virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash
# source venv/bin/activate     # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# Ejecutar
uvicorn app.main:app --reload

# API disponible en http://localhost:8000
# Swagger UI en http://localhost:8000/docs
```

## 🐳 Deploy Producción

### Deploy Manual
```bash
# Conectar al VPS
ssh root@72.60.115.230

# Ir al proyecto
cd ~/whatsapp-api-middleware

# Pull cambios
git pull origin main

# Rebuild y restart
docker compose down
docker compose build
docker compose up -d

# Verificar logs
docker compose logs -f api
```

### Deploy Automático (CI/CD)

Cada `git push` a `main` despliega automáticamente vía GitHub Actions:
```bash
git add .
git commit -m "feat: nueva funcionalidad"
git push origin main

# GitHub Actions automáticamente:
# 1. Se conecta al VPS
# 2. Pull cambios
# 3. Rebuild Docker
# 4. Restart container
# 5. Health check
# 6. Rollback si falla
```

## 🌐 URLs Producción

- **API:** https://api.bdcmotomex.com
- **Health:** https://api.bdcmotomex.com/health
- **Docs:** https://api.bdcmotomex.com/docs

## 🔐 Variables de Entorno

### `.env` Local/Producción
```env
# Environment
ENVIRONMENT=production
DEBUG=false

# API Configuration
API_KEY=your-secure-api-key-here

# n8n Configuration
N8N_WEBHOOK_URL=http://n8n:5678/webhook
N8N_TIMEOUT=30

# Respond.io Configuration
RESPOND_IO_API_TOKEN=your-token-here
RESPOND_IO_CHANNEL_ID=244792
RESPOND_IO_WHATSAPP_CLOUD_API_ID=333516

# Logging
LOG_LEVEL=INFO

# CORS
ALLOWED_ORIGINS=https://api.bdcmotomex.com
```

## 📊 Endpoints

### `GET /`
Endpoint raíz - información del servicio

**Response:**
```json
{
  "message": "Hello World from WhatsApp API Middleware!",
  "status": "running",
  "version": "0.1.1"
}
```

### `GET /health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "service": "whatsapp-api-middleware"
}
```

## 🔄 CI/CD

### GitHub Actions Workflow

El proyecto incluye CI/CD automático configurado en `.github/workflows/deploy.yml`:

- **Trigger:** Push a branch `main`
- **Acciones:**
  1. Conecta al VPS vía SSH
  2. Pull cambios de GitHub
  3. Rebuild imagen Docker
  4. Restart contenedor
  5. Health check automático
  6. Rollback si falla

### GitHub Secrets Requeridos

- `VPS_HOST`: IP del servidor (72.60.115.230)
- `VPS_USERNAME`: Usuario SSH (root)
- `SSH_PRIVATE_KEY`: Clave privada SSH

## 🏢 Infraestructura

### VPS Hostinger
- **IP:** 72.60.115.230
- **OS:** Ubuntu 24.04.3 LTS
- **RAM:** 32GB
- **CPU:** 8 cores
- **Hostname:** srv977744

### Red Docker
- **Red:** root_default
- **Traefik:** root-traefik-1 (172.18.0.2)
- **n8n:** root-n8n-1 (172.18.0.3)
- **API:** whatsapp-api-middleware (auto-asignada)

## 📝 Estructura del Proyecto
```
whatsapp-api-middleware/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD
├── app/
│   └── main.py                 # FastAPI application
├── tests/
│   └── __init__.py
├── .env.example                # Template variables entorno
├── .gitignore
├── Dockerfile                  # Multi-stage Docker build
├── docker-compose.yml          # Compose con Traefik labels
├── requirements.txt            # Dependencias Python
└── README.md                   # Esta documentación
```

## 🧪 Testing
```bash
# Ejecutar tests (cuando se implementen)
pytest

# Health check local
curl http://localhost:8000/health

# Health check producción
curl https://api.bdcmotomex.com/health
```

## 🐛 Troubleshooting

### Container no inicia
```bash
# Ver logs
docker compose logs -f api

# Verificar config
docker compose config

# Restart
docker compose restart api
```

### SSL no funciona
```bash
# Ver logs Traefik
docker logs root-traefik-1 | grep -i certificate

# Verificar DNS
nslookup api.bdcmotomex.com
```

### Deploy falla en GitHub Actions

1. Verificar secrets en GitHub
2. Verificar conexión SSH al VPS
3. Ver logs del workflow en Actions

## 👥 Equipo

- **Arquitecto:** Erik Tamayo
- **Departamento:** Innovación
- **Empresa:** Motomex

## 📄 Licencia

Proyecto interno de Motomex - Todos los derechos reservados

## 🔗 Links

- **Repositorio:** https://github.com/erikth97/whatsapp-api-middleware
- **API Producción:** https://api.bdcmotomex.com
- **Respond.io:** Channel 244792

---

**Última actualización:** Diciembre 2025  
**Versión:** 0.1.1  
**Estado:** ✅ Producción
