import pandas as pd
import datetime
import glob
import os
import smtplib
from email.message import EmailMessage

# --- CONFIGURACIÓN ---
DIR_CSV = '/var/smdr_datos'
REMITENTE = 'emisorcorreo@something.com'
PASSWORD = 'EMAIL'
DESTINATARIOS = ['receptor@something.com']
SMTP_SERVER = 'mail.something.com'
SMTP_PORT = 587
# ---------------------

# Determinar el mes anterior
hoy = datetime.date.today()
primer_dia_mes_actual = hoy.replace(day=1)
ultimo_dia_mes_anterior = primer_dia_mes_actual - datetime.timedelta(days=1)
mes_reporte = ultimo_dia_mes_anterior.strftime('%Y-%m')

# Buscar archivos del mes anterior
patron_busqueda = os.path.join(DIR_CSV, f"llamadas_{mes_reporte}-*.csv")
archivos_mes = glob.glob(patron_busqueda)

if not archivos_mes:
    print("No hay datos para generar el reporte de este mes.")
    exit()

# Definir los nombres de las columnas según la configuración de tu Avaya (ajústalas si varían)
columnas = ['Call_Start', 'Duration', 'Ring_Time', 'Caller', 'Direction', 'Dialed_Number', 'Extension', 'Is_Internal', 'Call_ID']

# Leer y consolidar todos los CSV
df = pd.concat((pd.read_csv(f, names=columnas, on_bad_lines='skip') for f in archivos_mes), ignore_index=True)

# Crear el Excel
nombre_excel = f"Reporte_Llamadas_{mes_reporte}.xlsx"
with pd.ExcelWriter(nombre_excel, engine='openpyxl') as writer:
    # Hoja 1: Detalle Completo
    df.to_excel(writer, sheet_name='Detalle', index=False)
    
    # Hoja 2: Resumen (conteo por dirección de llamada)
    resumen = df['Direction'].value_counts().reset_index()
    resumen.columns = ['Tipo de Llamada', 'Total']
    resumen.to_excel(writer, sheet_name='Resumen', index=False)
    
    # Hoja 3: Por extensión
    por_extension = df['Extension'].value_counts().reset_index()
    por_extension.columns = ['Extensión', 'Total Llamadas']
    por_extension.to_excel(writer, sheet_name='Por Extensión', index=False)

# Enviar por correo
msg = EmailMessage()
msg['Subject'] = f"Reporte Mensual de Llamadas - {mes_reporte}"
msg['From'] = REMITENTE
msg['To'] = ", ".join(DESTINATARIOS)
msg.set_content(f"Se adjunta el reporte de llamadas telefónicas consolidado del mes de {mes_reporte}.")

with open(nombre_excel, 'rb') as f:
    msg.add_attachment(f.read(), maintype='application', subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=nombre_excel)

with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()
    server.login(REMITENTE, PASSWORD)
    server.send_message(msg)

print("Reporte generado y enviado con éxito.")
