# Apex Sports Store – Deployment Guide

## Overview

This repository contains a **Django** project that implements a dark‑mode, premium‑style sports product store with a custom admin panel.  The application is ready to be deployed to production using **Docker** on a VPS (e.g., DigitalOcean, AWS EC2) with **PostgreSQL**, **Nginx** as a reverse proxy, and **Certbot** for automated HTTPS certificates.

## Prerequisites

- A virtual machine (Linux) with Docker Engine and Docker Compose installed.
- A domain name that points to the VM’s public IP.
- (Optional) A GitHub repository where the code resides – this will be used for the CI/CD pipeline.

## Repository Structure

```
.
├─ apex_project/                # Django project
│  ├─ __init__.py
│  ├─ settings.py               # Development settings (DEBUG=True)
│  ├─ settings_production.py    # Production settings (DEBUG=False, PostgreSQL, security)
│  ├─ urls.py
│  └─ wsgi.py
├─ store/                       # Django app with models, views, admin
├─ static/                      # CSS & JS assets
│  ├─ css/custom.css
│  └─ js/main.js
├─ templates/                   # HTML templates
├─ Dockerfile                   # Multi‑stage Docker build
├─ docker-compose.yml           # Services: db, web, nginx, certbot
├─ requirements.txt             # Python dependencies (including dj‑database‑url)
├─ nginx.conf                   # Nginx configuration for static/media and proxy
├─ .env.example                 # Example environment variables
└─ README.md                    # This file
```

## 1. Prepare the VPS

1. **Install Docker & Docker Compose** (Ubuntu example):
   ```bash
   sudo apt update
   sudo apt install -y docker.io docker-compose
   sudo usermod -aG docker $USER
   newgrp docker
   ```
2. **Clone the repository** to `/opt/apex_store` (or any path you prefer).
   ```bash
   git clone <YOUR_REPO_URL> /opt/apex_store
   cd /opt/apex_store
   ```
3. **Create an `.env` file** from the example:
   ```bash
   cp .env.example .env
   # Edit .env with your own secret keys and domain
   nano .env
   ```
   Example contents:
   ```text
   DJANGO_SECRET_KEY=super-secret-production-key
   DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   POSTGRES_DB=apexdb
   POSTGRES_USER=apexuser
   POSTGRES_PASSWORD=verystrongpassword
   ```
   The `docker-compose.yml` will automatically load this file.

## 2. Build & Run the Stack

```bash
docker compose up -d --build
```

Docker Compose will:
- Pull the PostgreSQL image and start a database container.
- Build the Django web image, run migrations, collect static files, and seed the DB (via `populate_db.py`).
- Start Nginx which serves static files, media files, and proxies traffic to the Django gunicorn server.
- Launch Certbot (initially idle) – after the first successful HTTPS request it will obtain a certificate.

## 3. Verify the Deployment

- Open `http://<YOUR_DOMAIN>` in a browser – you should see the home page.
- After a few seconds, Certbot will obtain an HTTPS cert; reload the page with `https://` – the lock icon should appear.
- Access the admin panel at `https://<YOUR_DOMAIN>/admin/` using the credentials created by `populate_db.py` (`admin` / `admin123`).
- Test cart, checkout, and media uploads.

## 4. CI/CD Pipeline (GitHub Actions)

A minimal workflow is provided in `.github/workflows/docker-deploy.yml`.  It builds the Docker images and pushes them to Docker Hub (or any registry) on every push to the `main` branch, then runs an SSH command on the VPS to pull the new images and restart the stack.

### Steps to enable:
1. **Create repository secrets** in GitHub:
   - `DOCKER_USERNAME` & `DOCKER_PASSWORD` – Docker Hub credentials.
   - `SSH_HOST`, `SSH_USER`, `SSH_PRIVATE_KEY` – SSH access to the VPS.
2. **Push changes** – the workflow automatically triggers.

## 5. Maintenance

- **Database backups**: Use `docker exec apex_postgres pg_dump -U $POSTGRES_USER $POSTGRES_DB > backup.sql`.
- **Static files**: Already served by WhiteNoise (in‑app) and Nginx for better caching.
- **Scaling**: Increase `workers` in the `web` service command or add a separate `worker` service for background tasks.

---

### Troubleshooting

- **Container fails to start** – Check logs with `docker compose logs web`.
- **Static assets missing** – Ensure `python manage.py collectstatic --noinput` runs successfully during the container start (the Dockerfile already does this).
- **HTTPS not obtained** – Verify domain DNS points to the VPS IP and port `80` is open for Certbot validation.

---

**Enjoy your production‑ready, premium‑styled sports store!**
