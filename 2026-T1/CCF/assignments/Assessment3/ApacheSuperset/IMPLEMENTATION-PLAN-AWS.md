# CCF Assessment 3 — Implementation Plan (AWS Variant)
*Derived from live session 2026-04-20. Use this as the reference if repeating the deployment on AWS EC2.*

---

## What Changed vs Azure

The Azure deployment used Ubuntu 22.04. AWS free tier defaults to **Amazon Linux 2023** (AL2023), which is RPM-based (Fedora lineage). Every `apt` command fails — the package manager is `dnf`.

| Step | Ubuntu / Azure | Amazon Linux 2023 / AWS |
|---|---|---|
| Update system | `sudo apt update && sudo apt upgrade -y` | `sudo dnf update -y` |
| Install Docker | `sudo apt install -y docker.io docker-compose-v2` | `sudo dnf install -y docker` |
| Compose command | `docker compose up -d` | `docker-compose up -d` (see note below) |
| Docker start | automatic | `sudo systemctl start docker && sudo systemctl enable docker` |

> **Compose note:** AL2023's `docker` package does NOT bundle the Compose plugin. `docker compose` (space) fails. Install the standalone binary manually:
> ```bash
> sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64" \
>   -o /usr/local/bin/docker-compose
> sudo chmod +x /usr/local/bin/docker-compose
> ```
> Then use `docker-compose` (hyphen) for all commands.

---

## Step-by-Step (AWS EC2 / Amazon Linux 2023)

### 0. Prerequisites

- EC2 instance launched (any size with ≥ 2 GB RAM; t3.small or t3.medium recommended for Superset)
- Key pair `.pem` file downloaded
- Security Group with inbound: **port 22** (your IP), **port 8088** (0.0.0.0/0)

---

### 1. SSH into the instance

```bash
chmod 400 ~/Downloads/your-key.pem
ssh -i ~/Downloads/your-key.pem ec2-user@<PUBLIC_IP>
```

Default user on Amazon Linux 2023 is **`ec2-user`** (not `ubuntu`, not `username`).

---

### 2. Install Docker

```bash
sudo dnf update -y
sudo dnf install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
newgrp docker
```

---

### 3. Install Docker Compose (standalone binary)

```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64" \
  -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Verify: `docker-compose --version`

---

### 4. Create the deployment folder

```bash
mkdir ~/superset-deployment && cd ~/superset-deployment
mkdir superset_home && chmod 777 superset_home
```

---

### 5. Create config files — CRITICAL: use heredoc or SCP, never paste into nano

**Why nano fails:** pasting multi-line YAML into nano over SSH corrupts indentation. Docker then creates a *directory* instead of mounting the file, causing `IsADirectoryError` on startup.

**Option A — heredoc (works for short files):**

```bash
cat > config.py << 'EOF'
import os

SECRET_KEY = os.environ["SUPERSET_SECRET_KEY"]
SQLALCHEMY_DATABASE_URI = os.environ["SUPERSET_METADATA_DB_URI"]

CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": os.environ.get("REDIS_HOST", "redis"),
    "CACHE_REDIS_PORT": int(os.environ.get("REDIS_PORT", "6379")),
    "CACHE_REDIS_DB": 1,
}

DATA_CACHE_CONFIG = CACHE_CONFIG
EOF
```

**Option B — SCP from local machine (most reliable for docker-compose.yml):**

Open a second terminal tab on your Mac and run:
```bash
scp -i ~/Downloads/your-key.pem \
  /path/to/docker-compose.yml \
  /path/to/config.py \
  ec2-user@<PUBLIC_IP>:~/superset-deployment/
```

---

### 6. docker-compose.yml

The working version mounts `config.py` via `SUPERSET_CONFIG_PATH`. Do not use the `SUPERSET__SQLALCHEMY_DATABASE_URI` double-underscore env var — it is not reliably picked up by `apache/superset:latest`.

```yaml
services:
  redis:
    image: redis:7-alpine
    restart: unless-stopped
    volumes:
      - redis-data:/data
    networks:
      - superset-network

  postgres:
    image: postgres:15-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: superset
      POSTGRES_USER: superset
      POSTGRES_PASSWORD: "YOUR_DB_PASSWORD"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - superset-network

  superset:
    image: apache/superset:latest
    restart: unless-stopped
    depends_on:
      - postgres
      - redis
    environment:
      SUPERSET_SECRET_KEY: "YOUR_SECRET_KEY"
      SUPERSET_CONFIG_PATH: /app/pythonpath/superset_config.py
      SUPERSET_METADATA_DB_URI: "postgresql+psycopg2://superset:YOUR_DB_PASSWORD@postgres:5432/superset"
      PYTHONPATH: /tmp/pythonpath
      REDIS_HOST: redis
      REDIS_PORT: "6379"
    ports:
      - "8088:8088"
    volumes:
      - ./superset_home:/app/superset_home
      - ./config.py:/app/pythonpath/superset_config.py:ro
    networks:
      - superset-network
    command:
      - sh
      - -c
      - >
        pip install --no-cache-dir --target /tmp/pythonpath psycopg2-binary &&
        superset db upgrade &&
        superset fab create-admin
        --username admin
        --firstname Admin
        --lastname User
        --email admin@superset.com
        --password "YOUR_ADMIN_PASSWORD" || true &&
        superset init &&
        superset run -h 0.0.0.0 -p 8088 --with-threads

volumes:
  redis-data:
  postgres-data:

networks:
  superset-network:
    driver: bridge
```

---

### 7. Launch

```bash
docker-compose up -d
docker-compose logs -f superset
```

Wait until you see:
```
* Running on http://0.0.0.0:8088
```

Then `Ctrl+C`.

---

### 8. Verify locally on the VM

```bash
curl -I http://localhost:8088
# expect: HTTP/1.1 302 FOUND
```

---

### 9. Access from browser — THE ISP PORT-BLOCKING PROBLEM

Port 8088 is non-standard. Many ISPs, university networks, and corporate proxies silently drop outbound connections to it. This makes the browser time out even when everything on the server is correctly configured.

**Symptoms:**
- `curl -I http://localhost:8088` on the VM → 302 ✅
- Security Group has 8088 open ✅
- NACL allows all traffic ✅
- Firewalld not installed ✅
- Browser → `ERR_CONNECTION_TIMED_OUT` ❌

**The fix — SSH tunnel:**

Open a second terminal tab on your Mac:
```bash
ssh -i ~/Downloads/your-key.pem -L 8088:localhost:8088 ec2-user@<PUBLIC_IP> -N
```

Then open your browser at:
```
http://localhost:8088
```

**How this works:** The `-L 8088:localhost:8088` flag tells SSH to forward your local port 8088 through the already-established SSH connection (port 22) to the server's localhost:8088. Your ISP sees only normal SSH traffic on port 22 — it never touches port 8088 at all. The `-N` flag means "no shell, just forward."

This is also why SSH to port 22 worked but the browser to port 8088 didn't — port 22 is universally allowed, port 8088 is not.

---

### 10. Shut down to save costs

When done:
```bash
# On the VM
docker-compose down

# In AWS console: stop or terminate the instance
```

---

## Pitfall Log (learned the hard way)

| Pitfall | What happened | Fix |
|---|---|---|
| Wrong SSH username | Used `username` literally instead of `ec2-user` | AL2023 default user is `ec2-user` |
| `apt` not found | Ubuntu muscle memory on an RPM distro | Use `dnf` on AL2023 |
| `docker compose` not found | AL2023 doesn't bundle Compose plugin | Install standalone binary via curl |
| YAML indentation broken | Pasted multi-line YAML into nano over SSH | Use heredoc `cat << 'EOF'` or SCP |
| Docker creates directory instead of file | Container started before bind-mount file existed | Always create files first, then `docker-compose up` |
| `IsADirectoryError` on superset_config.py | Docker created dir for missing mount target | `docker-compose down`, `rm -rf` the dir, create file, restart |
| Browser timeout on port 8088 | ISP filtering non-standard port | SSH tunnel: `-L 8088:localhost:8088` |

---

## Key Differences Summary: Azure vs AWS

| Aspect | Azure (Assessment 3) | AWS (this guide) |
|---|---|---|
| VM OS | Ubuntu 22.04 | Amazon Linux 2023 |
| Package manager | apt | dnf |
| Docker Compose | bundled as plugin | install standalone binary |
| Firewall/NSG | Azure NSG (subnet level) | Security Group (instance level) |
| SSH user | azureuser | ec2-user |
| Free tier VM | B1s (1 vCPU, 1 GB) — too small for Superset | t2.micro (1 vCPU, 1 GB) — also too small; use t3.small |
| Port access | Direct browser access worked | SSH tunnel needed (ISP blocks 8088) |
