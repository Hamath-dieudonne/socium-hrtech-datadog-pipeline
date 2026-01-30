# ============================================
# Dockerfile - Socium Metrics Agent
# ============================================

FROM python:3.11-slim

# Métadonnées
LABEL description="Socium Metrics Agent - Pipeline MongoDB to Datadog"

# Variables d'environnement Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Répertoire de travail
WORKDIR /app

# Copier requirements.txt
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt


# Copier le code source
COPY *.py .


# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Commande par défaut (garde le container actif)
CMD ["tail", "-f", "/dev/null"]
