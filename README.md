
# Mis Finanzas – Sistema de Control de Gastos

Aplicación web académica desarrollada con Python, Flask y SQLite. Permite iniciar sesión, registrar gastos, consultar un resumen y generar reportes por rango de fechas con opción de exportación CSV.

## Funcionalidades

- Inicio de sesión con usuario y contraseña.
- Registro de gastos: fecha, descripción y monto en soles.
- Panel con total acumulado, total del mes, total del día y cantidad de movimientos.
- Historial de los últimos gastos y opción para eliminar registros.
- Reporte con filtros por fecha inicial y final.
- Exportación del reporte a CSV, compatible con Excel.
- Base de datos SQLite creada automáticamente al iniciar la aplicación.

## Requisitos

- Python 3.10 o superior.
- pip.

## Instalación y ejecución

1. Descarga o clona este repositorio.
2. Abre una terminal dentro de la carpeta del proyecto.

### Windows

Crea un entorno virtual:

    python -m venv venv

Activa el entorno virtual:

    venv\Scripts\activate

### Linux / macOS

    python3 -m venv venv
    source venv/bin/activate

3. Instala las dependencias:

    pip install -r requirements.txt

4. Ejecuta la aplicación:

    python app.py

5. Abre tu navegador e ingresa a:

    http://127.0.0.1:5000

## Credenciales de acceso

| Campo | Valor |
|---|---|
| Usuario | `admin` |
| Contraseña | `123` |

La cuenta se crea automáticamente la primera vez que se inicia el programa. La contraseña se almacena como hash en SQLite.

## Capturas de pantalla

Las siguientes imágenes corresponden a las pantallas reales del sistema Mis Finanzas.

### 1. Inicio de sesión

![Inicio de sesión](capturas/login.png)

### 2. Panel principal y registro de gastos

![Panel principal](capturas/dashboard.png)

### 3. Reporte y exportación

![Reporte de gastos](capturas/report.png)

## ¿Cómo funciona?

1. El usuario ingresa con las credenciales indicadas.
2. En el panel principal completa fecha, descripción y monto; luego selecciona **Guardar gasto**.
3. El sistema almacena el movimiento en la base de datos `gastos.db` y actualiza los totales.
4. En **Reportes** puede indicar un periodo con las fechas Desde y Hasta y seleccionar **Filtrar**.
5. Con **Exportar CSV** descarga los movimientos del periodo para abrirlos en una hoja de cálculo.
6. La opción **Cerrar sesión** finaliza el acceso.

## Estructura del proyecto

    control_gastos/
    ├── app.py
    ├── requirements.txt
    ├── README.md
    ├── .gitignore
    ├── static/
    │   └── style.css
    ├── templates/
    │   ├── base.html
    │   ├── login.html
    │   ├── dashboard.html
    │   └── report.html
    └── capturas/
        ├── login.png
        ├── dashboard.png
        └── report.png

## Tecnologías utilizadas

- Python 3
- Flask
- SQLite
- HTML5 y CSS3

## Nota de seguridad

Las credenciales `admin` / `123` se incluyen porque forman parte de los requisitos académicos. No deben utilizarse en un sistema real. Antes de publicar una aplicación para uso real, configura una clave secreta segura mediante la variable de entorno `SECRET_KEY`, cambia las credenciales y utiliza HTTPS.

## Autor

Robin Méndez Solórzano

Proyecto académico – Sistema de Control de Gastos.
