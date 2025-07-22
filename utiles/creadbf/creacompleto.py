import pandas as pd
from sqlalchemy import create_engine, text
import re

# -----------------------------
# Configuración conexión
DB_USER = 'user_veteranos'
DB_PASSWORD = 'Klaveveteranos'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'Veteranos'

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# -----------------------------
# ✅ Crear tabla si no existe con todos los campos
crear_tabla_sql = """
CREATE TABLE IF NOT EXISTS RecibosProcesados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bingo_numero VARCHAR(255),
    apellido_y_nombre VARCHAR(255),
    dni_numero VARCHAR(255),
    celular VARCHAR(255),
    cuota VARCHAR(255),
    recibo VARCHAR(255),
    monto VARCHAR(255),
    serie VARCHAR(255),
    fecha DATE
);
"""

with engine.begin() as conn:
    conn.execute(text(crear_tabla_sql))

print("✅ Tabla RecibosProcesados creada/verificada.")

# -----------------------------
# ✅ Función para extraer SOLO el número de la celda CUOTA
def extraer_numero_cuota(cuota_valor):
    if pd.isna(cuota_valor):
        return None
    match = re.search(r'\d+', str(cuota_valor))
    if match:
        return match.group(0)
    return None

# -----------------------------
# ✅ Leer Excel y procesar por FILA
archivo_excel = '/home/sistema/utiles/recibos_procesados.xlsx'
df = pd.read_excel(archivo_excel)
print(df.columns.tolist())

filas_nuevas = []

with engine.connect() as conn:
    for idx, fila in df.iterrows():
        cuota_raw = fila['CUOTA']
        cuota_num = extraer_numero_cuota(cuota_raw)

        recibo_valor = fila['RECIBO']
        if pd.notna(recibo_valor) and str(recibo_valor).strip() != "":
            recibo_str = str(recibo_valor).strip()

            if recibo_str.isnumeric():
                sql = text("""
                    SELECT pesos, serie, fecha 
                    FROM data_bingo 
                    WHERE recibo_nro = :recibo
                    LIMIT 1;
                """)
                result = conn.execute(sql, {'recibo': recibo_str}).fetchone()
                if result:
                    monto, serie, fecha = result
                else:
                    monto, serie, fecha = '', '', None
            else:
                monto, serie, fecha = '', '', None

            filas_nuevas.append({
                'BINGO_N°': fila['BINGO_N°'],
                'APELLIDO_Y_NOMBRE': fila['APELLIDO_Y_NOMBRE'],
                'DNI_N°': fila['DNI_N°'],
                'CELULAR': fila['CELULAR'],
                'CUOTA': cuota_num,      # ✅ SOLO número extraído de la celda CUOTA
                'RECIBO': recibo_str,    # ✅ Valor de la celda RECIBO
                'MONTO': monto,
                'SERIE': serie,
                'FECHA': fecha
            })

# -----------------------------
# ✅ Guardar a Excel para control
df_resultado = pd.DataFrame(filas_nuevas)
df_resultado = df_resultado.where(pd.notnull(df_resultado), None)
df_resultado.to_excel('recibos_procesados.xlsx', index=False)
print("✅ Archivo 'recibos_procesados.xlsx' generado con cuota limpia y recibo correcto.")

# -----------------------------
# ✅ Insertar en tabla RecibosProcesados
with engine.connect() as conn:
    cursor = conn.connection.cursor()
    sql_insert = """
        INSERT INTO RecibosProcesados 
        (bingo_numero, apellido_y_nombre, dni_numero, celular, cuota, recibo, monto, serie, fecha)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data_insert = [
        (
            r['BINGO_N°'],
            r['APELLIDO_Y_NOMBRE'],
            r['DNI_N°'],
            r['CELULAR'],
            r['CUOTA'],
            r['RECIBO'],
            r['MONTO'],
            r['SERIE'],
            r['FECHA']
        )
        for _, r in df_resultado.iterrows()
    ]
    cursor.executemany(sql_insert, data_insert)
    conn.connection.commit()

print(f"✅ Insertados {len(data_insert)} registros en RecibosProcesados 🚀")
