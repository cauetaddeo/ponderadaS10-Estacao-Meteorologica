import sqlite3

def get_db_connection():
    # Timeout e PRAGMAs para evitar erro 'database is locked' [cite: 125-132]
    conn = sqlite3.connect('dados.db', timeout=10)
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA busy_timeout=5000')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.close()

def inserir_leitura(temp, umid, pressao=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO leituras (temperatura, umidade, pressao) VALUES (?, ?, ?)',
        (temp, umid, pressao)
    )
    id_novo = cursor.lastrowid
    conn.commit()
    conn.close()
    return id_novo

def listar_leituras(limite=50):
    conn = get_db_connection()
    leituras = conn.execute('SELECT * FROM leituras ORDER BY timestamp DESC LIMIT ?', (limite,)).fetchall()
    conn.close()
    return leituras

def deletar_leitura(id_leitura):
    conn = get_db_connection()
    conn.execute('DELETE FROM leituras WHERE id = ?', (id_leitura,))
    conn.commit()
    conn.close()

def atualizar_leitura(id_leitura, temp, umid, pressao):
    conn = get_db_connection()
    conn.execute('''
        UPDATE leituras 
        SET temperatura = ?, umidade = ?, pressao = ?
        WHERE id = ?
    ''', (temp, umid, pressao, id_leitura))
    conn.commit()
    conn.close()


def obter_leitura(id_leitura):
    conn = get_db_connection()
    leitura = conn.execute('SELECT * FROM leituras WHERE id = ?', (id_leitura,)).fetchone()
    conn.close()
    return leitura
