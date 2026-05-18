#!/bin/bash

# ============================================
# healthcheck.sh — Verifica el stack completo
# ============================================

set -uo pipefail
# Forzamos a que pegue en localhost que es donde expone tu Nginx/Frontend
BASE_URL="${1:-http://localhost}"

ok()   { echo "  [OK]   $1"; }
fail() { echo "  [FAIL] $1"; ERRORS=$((ERRORS+1)); }
ERRORS=0

echo "=== Healthcheck del stack Docker Compose ==="
echo ""

echo "--- Servicios Docker ---"
# Ajustamos los nombres para que coincidan con la nomenclatura estándar de Docker Compose
for svc in backend db frontend; do
    # Buscamos el contenedor que contenga el nombre del servicio
    CONTAINER_ID=$(docker compose ps -q "$svc" 2>/dev/null)
    if [ -n "$CONTAINER_ID" ]; then
        STATUS=$(docker inspect --format='{{.State.Status}}' "$CONTAINER_ID" 2>/dev/null || echo "error")
        if [ "$STATUS" = "running" ]; then
            ok "$svc → running"
        else
            fail "$svc → $STATUS"
        fi
    else
        fail "$svc → contenedor no encontrado"
    fi
done

echo ""
echo "--- Endpoints HTTP ---"

HTTP=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$BASE_URL/health" 2>/dev/null || echo "000")
[ "$HTTP" = "200" ] && ok "GET /health → $HTTP" || fail "GET /health → $HTTP"

HTTP=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$BASE_URL/api/notes" 2>/dev/null || echo "000")
[ "$HTTP" = "200" ] && ok "GET /api/notes → $HTTP" || fail "GET /api/notes → $HTTP"

HTTP=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$BASE_URL/" 2>/dev/null || echo "000")
[ "$HTTP" = "200" ] && ok "GET / (frontend) → $HTTP" || fail "GET / (frontend) → $HTTP"

echo ""
echo "--- DB desde backend ---"
# Usamos python3 de tu máquina local para parsear el JSON del health
DB_STATUS=$(curl -s "$BASE_URL/health" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('db','?'))" 2>/dev/null || echo "?")
[ "$DB_STATUS" = "connected" ] && ok "Postgres → $DB_STATUS" || fail "Postgres → $DB_STATUS"

echo ""
if [ "$ERRORS" -eq 0 ]; then
    echo "========================================="
    echo "🎉 Stack OK — ¡Todos los checks pasaron!"
    echo "========================================="
else
    echo "❌ $ERRORS checks fallaron. Revisar logs."
fi
