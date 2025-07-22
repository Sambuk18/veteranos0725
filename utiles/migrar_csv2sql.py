from flask import Flask, request, jsonify
import pandas as pd
from sqlalchemy import create_engine, text, exc
import os
import re
import io
import traceback
from werkzeug.utils import secure_filename
from datetime import datetime
from dotenv import load_dotenv  # Nueva importación

# Cargar variables de entorno desde .env
load_dotenv('/var/www/veteranos_app/sistema/.env')

app = Flask(__name__)

# Configuración de la base de datos (ahora desde variables de entorno)
DB_CONFIG = {
    'user': os.getenv('DB_USER', 'user_veteranos'),  # Valor por defecto si no existe
    'password': os.getenv('DB_PASSWORD', 'Klaveveteranos'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'Veteranos'),
    'port': int(os.getenv('DB_PORT', '3306'))  # Convertir a entero
}

# Configuración de seguridad
ALLOWED_EXTENSIONS = {'csv'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_column_name(name):
    """Limpia los nombres de columna para que sean válidos en SQL"""
    name = str(name).strip()
    name = re.sub(r'[^\w]', '_', name)
    name = re.sub(r'_+', '_', name)
    if name[0].isdigit():
        name = f'col_{name}'
    return name.lower()

def get_db_engine():
    connection_string = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    return create_engine(connection_string, pool_pre_ping=True)

def parse_date(date_str):
    """Convierte fechas en formato dd/mm/yyyy al formato yyyy-mm-dd"""
    if pd.isna(date_str) or str(date_str).strip() in ['', 'NULL', 'null']:
        return None
    
    try:
        # Intenta con formato día/mes/año
        date_obj = datetime.strptime(str(date_str).strip(), '%d/%m/%Y')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        try:
            # Intenta otros formatos comunes
            date_obj = pd.to_datetime(date_str, dayfirst=True)
            return date_obj.strftime('%Y-%m-%d')
        except:
            return None

def infer_type(series):
    """Infiere el tipo de dato SQL adecuado para una columna"""
    if series.dropna().empty:
        return 'VARCHAR(255)'
    
    sample = series.dropna().iloc[0] if not series.dropna().empty else ''
    
    # Detección de fechas
    if parse_date(sample):
        return 'DATE'
    
    # Luego números
    try:
        pd.to_numeric(series.dropna())
        if (series.dropna() % 1 == 0).all():
            return 'INT'
        else:
            return 'FLOAT'
    except:
        # Finalmente texto
        max_len = series.dropna().astype(str).map(len).max()
        return f'VARCHAR({min(65535, max(255, int(max_len * 1.5)))})'

def convert_value(value, col_type):
    """Convierte valores según el tipo de columna"""
    if pd.isna(value) or str(value).strip() in ['', 'NULL', 'null']:
        return None
    
    try:
        if 'INT' in col_type:
            return int(float(value))
        elif 'FLOAT' in col_type:
            return float(value)
        elif 'DATE' in col_type:
            return parse_date(value)
        else:
            return str(value)
    except:
        return str(value)

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    try:
        # Verificar archivo
        if 'file' not in request.files:
            return jsonify({'error': 'No se proporcionó archivo', 'success': False}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nombre de archivo vacío', 'success': False}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Tipo de archivo no permitido', 'success': False}), 400

        # Leer y validar CSV
        file_content = file.stream.read().decode('utf-8')
        if not file_content.strip():
            return jsonify({'error': 'El archivo está vacío', 'success': False}), 400

        try:
            df = pd.read_csv(
                io.StringIO(file_content),
                delimiter=request.form.get('delimiter', ','),
                na_values=['', 'NULL', 'null', ' ', '\\N', 'NA', 'N/A'],
                keep_default_na=False,
                dtype=str,
                engine='python'
            )
        except Exception as e:
            return jsonify({'error': f'Error al leer CSV: {str(e)}', 'success': False}), 400

        if df.empty:
            return jsonify({'error': 'El CSV no contiene datos', 'success': False}), 400

        # Sanitizar nombres de columnas
        df.columns = [clean_column_name(col) for col in df.columns]

        # Configuración de la tabla
        table_name = secure_filename(request.form.get('table_name', os.path.splitext(file.filename)[0].lower()))
        replace_table = request.form.get('replace_table', 'false').lower() == 'true'

        # Conexión a la base de datos
        engine = get_db_engine()
        
        try:
            with engine.begin() as conn:
                if replace_table:
                    conn.execute(text(f"DROP TABLE IF EXISTS `{table_name}`"))
                
                # Crear tabla dinámica
                column_types = {}
                create_sql = f"CREATE TABLE `{table_name}` ("
                for col in df.columns:
                    col_type = infer_type(df[col])
                    column_types[col] = col_type
                    create_sql += f"`{col}` {col_type}, "
                
                create_sql = create_sql.rstrip(', ') + ")"
                conn.execute(text(create_sql))

                # Insertar datos
                if not df.empty:
                    # Preparamos los datos convertidos al tipo correcto
                    data_to_insert = []
                    for _, row in df.iterrows():
                        row_data = {}
                        for col in df.columns:
                            row_data[col] = convert_value(row[col], column_types[col])
                        data_to_insert.append(row_data)
                    
                    # Construimos la consulta INSERT dinámica
                    columns = ', '.join([f'`{col}`' for col in df.columns])
                    placeholders = ', '.join([':%s' % col for col in df.columns])
                    insert_sql = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"
                    
                    # Ejecutamos para cada fila con parámetros nombrados
                    for row in data_to_insert:
                        conn.execute(text(insert_sql), row)

            return jsonify({
                'success': True,
                'message': f'Datos importados en {table_name}',
                'rows_imported': len(df),
                'table_schema': create_sql
            })

        except exc.SQLAlchemyError as e:
            return jsonify({
                'error': f'Error de base de datos: {str(e)}',
                'success': False,
                'type': 'database_error'
            }), 500

    except Exception as e:
        app.logger.error(f"Error inesperado: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'error': f'Error interno: {str(e)}',
            'success': False,
            'type': 'internal_error',
            'traceback': traceback.format_exc() if app.debug else None
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5550)
    
    
#     curl -X POST \
#   -F "file=@/home/sambu/Proyectos/Vete_001/utiles/recibos.csv" \
#   -F "table_name=prueba" \
#   -F "delimiter=," \
#   -F "replace_table=true" \
#   http://localhost:5000/upload-csv
######### curl -X POST -F "file=@/var/www/veteranos_app/sistema/utiles/recibos0625.csv" -F "table_name=prueba"  -F "delimiter=," -F "replace_table=true" http://localhost:5550/upload-csv
#INSERT INTO data_bingo (
#    fecha,
#    nombre_apellido,
#    pesos,
#    carton_nro,
#    serie,
#    recibo_nro,
#    forma_de_pago,
#    tipo,
#    comision
#)
#SELECT
#    fecha,
#    nombre_y_apellido,
#    pesos,
#    carton_n_,
#    serie,
#    recibo_n_,
#    forma_de_pago,
#    unnamed_7,
#    comision
#FROM prueba;