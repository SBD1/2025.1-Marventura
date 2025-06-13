import psycopg2

def connect():
    return psycopg2.connect(
        dbname="gamedb",
        user="gameuser",
        password="gamepass",
        host="localhost"
    )

def listar_ilhas():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ilha;")
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
