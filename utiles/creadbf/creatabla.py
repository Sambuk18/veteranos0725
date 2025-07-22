import pandas as pd
from sqlalchemy import create_engine, text
from datetime import date
from sqlalchemy import MetaData, Table, Column, insert

# -----------------------------
# ✅ Configuración usando PyMySQL directamente
DB_USER = 'user_veteranos'
DB_PASSWORD = 'Klaveveteranos'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'Veteranos'

# Motor SQLAlchemy usando PyMySQL
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# -----------------------------
# Crear tabla si no existe
crear_tabla_sql = """
CREATE TABLE IF NOT EXISTS RecibosProcesados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bingo_numero VARCHAR(255),
    apellido_y_nombre VARCHAR(255),
    dni_numero VARCHAR(255),
    celular VARCHAR(255),
    fecha DATE,
    cuota VARCHAR(255),
    recibo VARCHAR(255)
);
"""

with engine.begin() as conn:
    conn.execute(text(crear_tabla_sql))
print("✅ Tabla RecibosProcesados creada/verificada.")

# -----------------------------
# Leer archivo Excel
df = pd.read_excel('recibos_procesados.xlsx')
df.columns = df.columns.str.strip()
print("📌 Columnas detectadas:", df.columns.tolist())

# Limpiar CUOTA
df['CUOTA'] = df['CUOTA'].astype(str).str.split('-').str[0].str.strip()

# Fecha: llenar con hoy si falta
if 'FECHA' not in df.columns:
    df['FECHA'] = date.today()
else:
    df['FECHA'] = df['FECHA'].fillna(date.today())

# Renombrar y convertir a string para evitar errores de tipo
df_final = df[['BINGO_N', 'APELLIDO_Y_NOMBRE', 'DNI_N', 'CELULAR', 'FECHA', 'CUOTA', 'RECIBO']]
df_final = df_final.rename(columns={
    'BINGO_N': 'bingo_numero',
    'APELLIDO_Y_NOMBRE': 'apellido_y_nombre',
    'DNI_N': 'dni_numero',
    'CELULAR': 'celular',
    'FECHA': 'fecha',
    'CUOTA': 'cuota',
    'RECIBO': 'recibo'
}).astype(str)

# -----------------------------
# ✅ SOLUCIÓN: Usar conexión DBAPI compatible
with engine.connect() as conn:
    cursor = conn.connection.cursor()
    sql = """INSERT INTO RecibosProcesados 
             (bingo_numero, apellido_y_nombre, dni_numero, celular, fecha, cuota, recibo) 
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    
    data = [tuple(x) for x in df_final.values]
    cursor.executemany(sql, data)
    conn.connection.commit()

print("✅ Datos importados correctamente 🚀")