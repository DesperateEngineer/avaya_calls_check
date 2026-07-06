# Avaya SMDR Logger & Reporter 📞📊

Un sistema ligero, funcional y autónomo para capturar registros de llamadas telefónicas (SMDR) desde un conmutador Avaya IP Office, almacenarlos localmente y generar reportes mensuales consolidados en Excel de forma automática.

Diseñado para operar en servidores Linux (Ubuntu/Debian) minimizando dependencias y sin necesidad de bases de datos complejas ni software comercial.

## ⚙️ Arquitectura del Sistema

El proyecto opera en una sola vía de comunicación (Avaya -> Servidor) y se divide en dos fases:

1. **Captura en Tiempo Real (Daemon):** Un script en Python operando como servicio de sistema (`systemd`) mantiene abierto un puerto TCP. El conmutador Avaya se conecta a este puerto y envía un registro de texto por cada llamada terminada. El script guarda estos registros en archivos CSV separados por día.
2. **Consolidación Mensual (Cron):** El día 1 de cada mes, un segundo script procesa todos los CSV del mes anterior, genera un archivo Excel con el detalle y totales por extensión, y lo envía por correo electrónico (SMTP).

> **Contingencia (Buffer):** El sistema aprovecha la memoria interna del Avaya. Si el servidor Linux se reinicia o pierde red, el conmutador retiene las llamadas (hasta 3,000 registros). Al restablecerse la conexión TCP, el Avaya envía el historial atrasado de golpe, evitando pérdida de datos.

## 🛠️ Requisitos Previos

* Conmutador Avaya IP Office (con acceso a IP Office Manager o Web Manager).
* Servidor con Linux (Ubuntu/Debian).
* Python 3 instalado.
* Librerías de Python: `pandas`, `openpyxl`.
* Acceso a una cuenta de correo con envío SMTP habilitado.

## 🚀 Instalación y Configuración

### 1. Configuración del Emisor (Avaya IP Office)
1. Ingresa a la administración del conmutador.
2. Ve a **System** > Pestaña **SMDR**.
3. Configura los siguientes parámetros:
   * **Output:** `SMDR Only` (o `TCP`).
   * **IP Address:** La IP de tu servidor Linux.
   * **TCP Port:** `9000` (o el puerto definido en tu script).
   * **Records to Buffer:** `3000`.
4. Guarda los cambios usando el método **Merge** (Fusionar) para evitar reinicios.

### 2. Configuración del Servidor (Linux)
Instala las dependencias necesarias:
```bash
sudo apt update
sudo apt install python3-pandas python3-openpyxl -y
