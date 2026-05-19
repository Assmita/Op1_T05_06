# ── Stage 1: builder ────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# Buscamos el archivo dentro de la subcarpeta backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Stage 2: imagen final (sin herramientas de build) ───
FROM python:3.12-slim AS final

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

WORKDIR /app

# Copiar solo las dependencias instaladas desde el builder
COPY --from=builder /install /usr/local

# Copiar el código desde la subcarpeta backend
COPY backend/app.py .

# Script de inicio desde la subcarpeta backend
COPY backend/entrypoint.sh .

# CURA ANTI-ERRORES: Forzamos formato Unix y damos permisos de ejecucion
RUN apt-get update && apt-get install -y sed && rm -rf /var/lib/apt/lists/* \
    && sed -i 's/\r$//' entrypoint.sh \
    && chmod +x entrypoint.sh

# Usuario no-root
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]