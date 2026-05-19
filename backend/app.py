import datetime
import os
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)


def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "notesdb"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres")
    )


def init_db():
    # Bucle de reintentos para esperar a que Postgres esté 100% listo
    retries = 5
    while retries > 0:
        try:
            print("Intentando conectar a la base de datos para inicializar tabla...")
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("¡Base de datos conectada y tabla 'notes' verificada con éxito!")
            break
        except Exception as e:
            retries -= 1
            print(
                f"Postgres no está listo aún ({e}). "
                f"Reintentando en 3 segundos... (Intentos restantes: {retries})"
            )
            time.sleep(3)


# Inicialización segura antes de levantar las rutas de la API
init_db()


@app.route("/health")
def health():
    try:
        conn = get_conn()
        conn.close()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {e}"

    return jsonify({
        "status": "ok",
        "db": db_status,
        "time": datetime.datetime.utcnow().isoformat()
    })


@app.route("/api/notes", methods=["GET"])
def get_notes():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, title, content, created_at FROM notes ORDER BY created_at DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {"id": r[0], "title": r[1], "content": r[2], "created_at": str(r[3])}
            for r in rows
        ])
    except Exception as e:
        print(f"Error en GET /api/notes: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/notes", methods=["POST"])
def create_note():
    try:
        data = request.get_json()
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO notes (title, content) VALUES (%s, %s) RETURNING id",
            (data["title"], data.get("content", ""))
        )
        note_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"id": note_id, "message": "nota creada"}), 201
    except Exception as e:
        print(f"Error en POST /api/notes: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM notes WHERE id = %s", (note_id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "nota eliminada"})
    except Exception as e:
        print(f"Error en DELETE /api/notes: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
