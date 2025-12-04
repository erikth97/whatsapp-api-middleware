# Guía de Deployment

Guía completa para desplegar WhatsApp API Middleware en producción.

## 🎯 Pre-requisitos

### VPS
- Ubuntu 24.04 LTS
- 32GB RAM mínimo
- Docker 28.5+
- Docker Compose v2.40+
- Traefik configurado y corriendo

### DNS
- Dominio configurado apuntando a IP del VPS
- Registro A: api.bdcmotomex.com → 72.60.115.230

### GitHub
- Repositorio clonado en VPS
- SSH keys configuradas
- Secrets configurados en GitHub Actions

## 📋 Proceso de Setup Inicial

### 1. Configurar SSH Keys
```bash
# En el VPS
ssh-keygen -t ed25519 -C "github-vps" -f ~/.ssh/github_vps
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_actions_deploy

# Agregar clave pública de actions a authorized_keys
cat ~/.ssh/github_actions_deploy.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# Agregar clave pública de VPS a GitHub
cat ~/.ssh/github_vps.pub
# Copiar y agregar en: https://github.com/settings/keys
```

### 2. Clonar Repositorio
```bash
# Configurar Git
git config --global user.name "erikth97"
git config --global user.email "e.fabianth@gmail.com"

# Crear directorio
cd /root
mkdir -p whatsapp-api-middleware
cd whatsapp-api-middleware

# Clonar
git clone git@github.com:erikth97/whatsapp-api-middleware.git .
```

### 3. Configurar .env de Producción
```bash
# Copiar template
cp .env.example .env

# Generar API Key segura
openssl rand -hex 32

# Editar .env
nano .env
```

**Configuración mínima:**
```env
ENVIRONMENT=production
DEBUG=false
API_KEY=<tu-api-key-generada>
N8N_WEBHOOK_URL=http://n8n:5678/webhook
ALLOWED_ORIGINS=https://api.bdcmotomex.com
```

### 4. Configurar docker-compose.yml

**Verificar configuración de red:**
```bash
# Ver red de Traefik
docker network ls
docker inspect <traefik-container> | grep -A 5 Networks
```

**Ajustar docker-compose.yml:**
```yaml
networks:
  root_default:  # Usar el nombre correcto de tu red
    external: true
```

**Ajustar certresolver:**
```bash
# Ver config de Traefik
docker inspect <traefik-container> | grep certificatesresolvers

# Usar el nombre correcto en labels:
- "traefik.http.routers.whatsapp-api.tls.certresolver=mytlschallenge"
```

### 5. Build y Deploy Inicial
```bash
# Build
docker compose build

# Start
docker compose up -d

# Ver logs
docker compose logs -f api

# Verificar health
docker exec whatsapp-api-middleware python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
```

### 6. Configurar GitHub Secrets

En: https://github.com/erikth97/whatsapp-api-middleware/settings/secrets/actions

**Agregar 3 secrets:**

1. `VPS_HOST`
   - Value: 72.60.115.230

2. `VPS_USERNAME`
   - Value: root

3. `SSH_PRIVATE_KEY`
   - Value: Contenido completo de `~/.ssh/github_actions_deploy` (clave privada)

## 🚀 Deploy Manual
```bash
# Conectar al VPS
ssh root@72.60.115.230

# Ir al proyecto
cd ~/whatsapp-api-middleware

# Pull cambios
git pull origin main

# Rebuild
docker compose down
docker compose build
docker compose up -d

# Verificar
docker compose ps
docker compose logs -f api
```

## 🤖 Deploy Automático (CI/CD)

### Workflow GitHub Actions

El workflow se activa automáticamente en cada `git push` a `main`.

**Proceso:**
1. GitHub Actions se conecta al VPS vía SSH
2. Ejecuta `git pull origin main`
3. Ejecuta `docker compose down`
4. Ejecuta `docker compose build`
5. Ejecuta `docker compose up -d`
6. Espera 10 segundos
7. Ejecuta health check con Python
8. Si health check falla → rollback automático

### Test del CI/CD
```bash
# Local
echo "# Test" >> README.md
git add README.md
git commit -m "test: CI/CD"
git push origin main

# Ver en GitHub Actions
# https://github.com/erikth97/whatsapp-api-middleware/actions

# Verificar en producción
curl https://api.bdcmotomex.com/health
```

## 🔍 Troubleshooting

### Container no inicia
```bash
# Ver logs
docker compose logs api

# Ver eventos
docker compose events

# Verificar permisos
ls -la /root/whatsapp-api-middleware

# Verificar .env
cat .env | grep -v "KEY\|TOKEN"
```

### SSL no funciona
```bash
# Ver logs Traefik
docker logs root-traefik-1 | grep -i "api.bdcmotomex\|certificate"

# Verificar DNS
nslookup api.bdcmotomex.com

# Forzar renovación SSL
docker restart root-traefik-1
```

### Health check falla
```bash
# Verificar que el contenedor esté corriendo
docker ps | grep whatsapp

# Verificar red
docker inspect whatsapp-api-middleware | grep -A 10 Networks

# Test interno
docker exec whatsapp-api-middleware python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Test desde Traefik
curl http://localhost:8000/health
```

### GitHub Actions falla

**Error: SSH connection failed**
- Verificar VPS_HOST en secrets
- Verificar que SSH_PRIVATE_KEY está completo
- Test SSH: `ssh -i ~/.ssh/github_actions_deploy root@72.60.115.230`

**Error: git pull failed**
- Verificar que github_vps key está en GitHub
- Verificar permisos: `chmod 600 ~/.ssh/github_vps`

**Error: docker command not found**
- Verificar que Docker está instalado en VPS
- Verificar PATH del usuario root

## 📊 Verificación Post-Deploy
```bash
# 1. Container running
docker ps | grep whatsapp-api-middleware

# 2. Health check
curl https://api.bdcmotomex.com/health

# 3. API endpoint
curl https://api.bdcmotomex.com/

# 4. Swagger UI
# Abrir: https://api.bdcmotomex.com/docs

# 5. Logs sin errores
docker compose logs api | tail -50

# 6. SSL válido
openssl s_client -connect api.bdcmotomex.com:443 -servername api.bdcmotomex.com < /dev/null 2>/dev/null | grep "Verify return code"
# Debe mostrar: Verify return code: 0 (ok)
```

## 🔄 Rollback Manual
```bash
# Ver commits
git log --oneline -5

# Rollback a commit anterior
git reset --hard <commit-hash>

# Rebuild y restart
docker compose down
docker compose build
docker compose up -d
```

## 🛡️ Seguridad

### Actualizar API Key
```bash
# Generar nueva
openssl rand -hex 32

# Actualizar .env
nano .env

# Restart
docker compose restart api
```

### Rotar SSH Keys
```bash
# Generar nueva
ssh-keygen -t ed25519 -C "github-actions-new" -f ~/.ssh/github_actions_new

# Agregar a authorized_keys
cat ~/.ssh/github_actions_new.pub >> ~/.ssh/authorized_keys

# Actualizar secret en GitHub
cat ~/.ssh/github_actions_new

# Test
ssh -i ~/.ssh/github_actions_new root@72.60.115.230 "echo 'OK'"

# Remover clave vieja después de confirmar
```

## 📝 Checklist Pre-Deploy

- [ ] VPS con Docker instalado
- [ ] Traefik corriendo
- [ ] DNS configurado y propagado
- [ ] SSH keys configuradas
- [ ] GitHub secrets configurados
- [ ] .env de producción configurado
- [ ] docker-compose.yml ajustado (red y certresolver)
- [ ] Test de conexión SSH
- [ ] Test de git pull

## 📝 Checklist Post-Deploy

- [ ] Container corriendo (docker ps)
- [ ] Health check OK
- [ ] API responde
- [ ] SSL válido
- [ ] Swagger UI accesible
- [ ] Logs sin errores críticos
- [ ] GitHub Actions workflow exitoso

---

**Última actualización:** Diciembre 2025
