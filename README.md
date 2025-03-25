# Sistema de Newsletter

Un sistema de newsletter desarrollado con Flask que permite gestionar suscripciones y enviar newsletters a suscriptores.

## Características

- Registro de suscriptores
- Panel de administración
- Envío de newsletters
- Gestión de suscripciones/desuscripciones

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   ```
3. Activar el entorno virtual:
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
4. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Configuración

1. Crear un archivo `.env` en la raíz del proyecto
2. Configurar las siguientes variables:
   ```
   FLASK_APP=app
   FLASK_ENV=development
   SECRET_KEY=tu_clave_secreta
   DATABASE_URL=sqlite:///newsletter.db
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=tu_email@gmail.com
   MAIL_PASSWORD=tu_contraseña
   ```

## Ejecución

```bash
flask run
```
