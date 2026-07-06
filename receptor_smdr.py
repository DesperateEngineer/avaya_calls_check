import socket
import datetime
import os
import time

# Configuración
HOST = '0.0.0.0'  # Escucha en todas las interfaces
PORT = 9000       # Puerto
DIR_CSV = '/var/smdr_datos' # Carpeta donde se guardarán los CSV

# Crear directorio si no existe
os.makedirs(DIR_CSV, exist_ok=True)

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor SMDR escuchando en el puerto {PORT}...")
        
        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    while True:
                        data = conn.recv(2048)
                        if not data:
                            break # El conmutador cerró la conexión
                        
                        linea = data.decode('utf-8', errors='ignore').strip()
                        if linea:
                            # Generar nombre del archivo basado en la fecha actual
                            hoy = datetime.date.today().strftime('%Y-%m-%d')
                            archivo_csv = os.path.join(DIR_CSV, f"llamadas_{hoy}.csv")
                            
                            # Escribir la línea en el archivo
                            with open(archivo_csv, 'a') as f:
                                f.write(linea + '\n')
            except Exception as e:
                print(f"Error de conexión: {e}")
                time.sleep(5) # Esperar antes de reconectar en caso de caída

if __name__ == "__main__":
    iniciar_servidor()
