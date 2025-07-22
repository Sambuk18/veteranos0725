import pandas as pd

# Ruta del archivo Excel original
archivo_excel = 'original.xlsx'
df = pd.read_excel(archivo_excel)

# Mostrar columnas para verificar
print(df.columns.tolist())

# Usar nombres REALES según tu print
columnas_fijas = ['BINGO_N°', 'APELLIDO_Y_NOMBRE', 'DNI_N°', 'CELULAR']
columnas_recibos = df.columns[4:]  # Desde la quinta columna en adelante

filas_nuevas = []

for index, fila in df.iterrows():
    for col in columnas_recibos:
        recibo = fila[col]
        if pd.notna(recibo):
            filas_nuevas.append({
                'BINGO_N°': fila['BINGO_N°'],
                'APELLIDO_Y_NOMBRE': fila['APELLIDO_Y_NOMBRE'],
                'DNI_N°': fila['DNI_N°'],
                'CELULAR': fila['CELULAR'],
                'CUOTA': col,     # ✅ Nueva columna: nombre de la cuota (columna original)
                'RECIBO': recibo  # ✅ Valor: número de recibo
            })

df_resultado = pd.DataFrame(filas_nuevas)
df_resultado.to_excel('recibos_procesados.xlsx', index=False)

print("✅ Archivo 'recibos_procesados.xlsx' generado con éxito.")
