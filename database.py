import sqlite3

DB_NAME = "qinsight.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ocorrencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_ocorrencia TEXT,
            setor TEXT,
            responsavel TEXT,
            tipo_erro TEXT,
            gravidade TEXT,
            status TEXT,
            tempo_resolucao INTEGER,
            descricao TEXT
        )
    """)

    conn.commit()
    conn.close()


def inserir_ocorrencia(data, setor, responsavel, tipo, gravidade, status, tempo, descricao):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ocorrencias (
            data_ocorrencia, setor, responsavel, tipo_erro,
            gravidade, status, tempo_resolucao, descricao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (data, setor, responsavel, tipo, gravidade, status, tempo, descricao))

    conn.commit()
    conn.close()


def listar_ocorrencias():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ocorrencias ORDER BY id DESC")
    dados = cursor.fetchall()

    conn.close()
    return dados