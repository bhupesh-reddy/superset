# superset

Production-leaning Apache Superset stack that runs locally first, then on a server. Data persists in Docker **named volumes**.

## Prereqs
- Docker Engine 24+ and Compose plugin
- Ports: default 8088

## 1) Configure env
```bash
cp env/.env.example env/.env
cp env/.env.example env/.env.local
# edit .env and .env.local, set SUPERSET_SECRET_KEY and admin creds
