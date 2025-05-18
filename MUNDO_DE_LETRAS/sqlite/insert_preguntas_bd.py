import sqlite3 as sql
import os, json

bd_path = os.path.join(os.path.dirname(__file__), "..\\preguntas\\lecturas.db")

con = sql.connect(bd_path)
cur = con.cursor()

for i in range(1, 11):
  with open(os.path.join(os.path.dirname(__file__), f"..\\preguntas\\preguntas{i}.json"), "r", encoding="utf-8") as f:
    data = json.load(f)
    
    for elem in data:
      cur.execute("INSERT INTO preguntas(id, id_lectura, texto) VALUES(?, ?, ?)", (int(elem["pregunta"][0]), i, elem["pregunta"]))

      j = 0
      for opc in elem["opciones"]:
        esCorrecta = 1 if elem["respuesta"] == j else 0

        cur.execute("INSERT INTO respuestas(id, id_lectura, id_pregunta, texto, esCorrecta) VALUES(?, ?, ?, ?, ?)", (j, i, int(elem["pregunta"][0]), opc, esCorrecta))
        j = 1 + j
  
  con.commit()

cur.close()
con.close()