import sqlite3 as sql
import os

bd_path = os.path.join(os.path.dirname(__file__), "..\\preguntas\\lecturas.db")

con = sql.connect(bd_path)
cur = con.cursor()

cur.execute("CREATE TABLE lecturas(id INTEGER PRIMARY KEY, titulo, lectura)")

cur.execute("""
            CREATE TABLE preguntas(
            id INTEGER,
            id_lectura INTEGER,
            texto,
            PRIMARY KEY(id, id_lectura),
            FOREIGN KEY (id_lectura) REFERENCES lecturas(id)
            )""")

cur.execute("""
            CREATE TABLE respuestas(
            id INTEGER,
            id_lectura INTEGER,
            id_pregunta INTEGER,
            texto,
            esCorrecta,
            PRIMARY KEY(id, id_lectura, id_pregunta),
            FOREIGN KEY (id_lectura) REFERENCES lecturas(id),
            FOREIGN KEY (id_pregunta) REFERENCES preguntas(id))""")

res = cur.execute("SELECT * FROM lecturas")
print(res.fetchall())

res = cur.execute("SELECT name FROM pragma_table_info('respuestas')")
print(res.fetchall())

con.commit()

cur.close()
con.close()