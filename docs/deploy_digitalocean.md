# Deploy DigitalOcean (VPS) - Django + Postgres (sem Docker)

## Requisitos

- Dominio apontando para o IP do VPS
- Python 3.12+ e virtualenv
- Postgres
- Nginx

## Passo a passo (Django + Gunicorn)

1) Instale pacotes do sistema

- sudo apt update
- sudo apt install -y python3 python3-venv python3-pip postgresql nginx \
  libpq-dev libcairo2 libgdk-pixbuf-2.0-0 libpango-1.0-0 libpangocairo-1.0-0 \
  libpangoft2-1.0-0 libffi-dev shared-mime-info fonts-dejavu-core wkhtmltopdf

Obs: wkhtmltopdf so e necessario se PDF_ENGINE=wkhtmltopdf.

2) Crie banco e usuario Postgres

- sudo -u postgres psql
- CREATE DATABASE cejamsys;
- CREATE USER cejamsys_user WITH PASSWORD 'sua_senha';
- GRANT ALL PRIVILEGES ON DATABASE cejamsys TO cejamsys_user;
- \q

3) Clone o projeto e crie a venv

- git clone <repo>
- cd CEJAM
- python3 -m venv .venv
- source .venv/bin/activate
- pip install -r requirements.txt

4) Configure o ambiente

- cp backend/.env.example backend/.env
- Ajuste: DEBUG=False, SECRET_KEY, ALLOWED_HOSTS, USE_SQLITE=0, DB_*, CORS_ALLOWED_ORIGINS

5) Migre e colete estaticos

- python backend/manage.py migrate
- python backend/manage.py collectstatic --noinput

6) Suba com Gunicorn (exemplo manual)

- cd backend
- gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 3

## Systemd (opcional)

Crie o service `/etc/systemd/system/cejamsys.service` (ajuste paths e usuario):

[Unit]
Description=CEJAM Django
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/srv/cejamsys/backend
EnvironmentFile=/srv/cejamsys/backend/.env
ExecStart=/srv/cejamsys/.venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 3
Restart=always

[Install]
WantedBy=multi-user.target

- sudo systemctl daemon-reload
- sudo systemctl enable --now cejamsys

## Nginx (proxy + SSL)

Exemplo de bloco server (ajuste dominio):

server {
    listen 80;
    server_name api.seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

Use Certbot para SSL:

- sudo apt install -y certbot python3-certbot-nginx
- sudo certbot --nginx -d api.seu-dominio.com

## Observacoes

- Rode `migrate` e `collectstatic` antes de subir o Gunicorn.
- Para limpar dados do Postgres em producao:
  - sudo -u postgres psql -d cejamsys -c 'DROP SCHEMA public CASCADE; CREATE SCHEMA public;'
