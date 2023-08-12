# Luli's Construction

#### Video Demo: [URL AQUÍ](enlace al video demostrativo de tu proyecto)

## Descripción
Luli's Construction es una página web que muestra información sobre una empresa de construcción ficticia. Proporciona a los usuarios una visión general de los servicios ofrecidos, proyectos destacados y un formulario de contacto. El sitio web está desarrollado utilizando HTML, CSS, Flask, Jinja, SQLite3 y JavaScript.

## Estructura del proyecto
El proyecto se organiza de la siguiente manera:

- `app.py`: El archivo principal que contiene la lógica del servidor Flask y las rutas de la aplicación web. Aquí se configuran las dependencias necesarias, como Flask, Flask-Mail y SQLite, y se establecen las rutas para las diferentes páginas y funciones del sitio web.
- `templates/`: Esta carpeta contiene las plantillas HTML utilizando el lenguaje de plantillas Jinja para generar contenido dinámico. Incluye las plantillas para la página de inicio (`index.html`), proyectos (`proyectos.html`), servicios (`servicios.html`), portafolio (`portafolio.html`) y contacto (`contacto.html`).
- `static/`: Aquí se encuentran los archivos estáticos, como hojas de estilo CSS, scripts de JavaScript y archivos de imagen.

## Base de datos
La aplicación utiliza una base de datos SQLite para almacenar información relacionada con los usuarios, servicios y transacciones. La estructura de la base de datos es la siguiente:

### Tabla `usuarios`
- `ID` (clave primaria): Identificador único del usuario.
- `nombre`: Nombre del usuario.
- `correo`: Correo electrónico del usuario.
- `contraseña`: Contraseña del usuario (almacenada de forma segura mediante el uso de bcrypt).
- `es_admin`: Indicador booleano que especifica si el usuario tiene privilegios de administrador.

### Tabla `servicios`
- `ID` (clave primaria): Identificador único del servicio.
- `nombre`: Nombre del servicio.
- `descripcion`: Descripción del servicio.
- `precio`: Precio del servicio.

### Tabla `transacciones`
- `ID` (clave primaria): Identificador único de la transacción.
- `usuario_id` (clave foránea): ID del usuario asociado a la transacción.
- `servicio_id` (clave foránea): ID del servicio asociado a la transacción.
- `fecha`: Fecha de la transacción.

## Seguridad de contraseña
La aplicación implementa medidas de seguridad para las contraseñas de los usuarios. Se utiliza la función `bcrypt.checkpw()` de la biblioteca bcrypt para verificar si la contraseña ingresada coincide con la contraseña almacenada en la base de datos. Esto garantiza que las contraseñas se almacenen de forma segura mediante el uso de un algoritmo de hash robusto.

## Configuración y uso
Asegúrate de tener instalado Python (versión X.X.X o superior) en tu entorno de desarrollo. Sigue estos pasos para configurar y ejecutar el proyecto en tu máquina local:

1. Clona este repositorio en tu máquina local.
2. Crea un entorno virtual: `python3 -m venv env`.
3. Activa el entorno virtual:
   - En Windows: `.\env\Scripts\activate`.
   - En macOS/Linux: `source env/bin/activate`.
4. Instala las dependencias del proyecto: `pip install -r requirements.txt`.
5. Configura las variables necesarias en el archivo `app.py`, como las credenciales de correo electrónico para Flask-Mail.
6. Ejecuta la aplicación: `python app.py`.
7. Abre tu navegador web y visita `http://localhost:5000` para ver la página web de Luli's Construction.

## Funcionalidades principales
- Página de inicio (`index.html`): Muestra una descripción general de la empresa y los servicios ofrecidos.
- Página de proyectos (`proyectos.html`): Muestra una lista de proyectos destacados.
- Página de servicios (`servicios.html`): Proporciona información detallada sobre los diferentes servicios ofrecidos por la empresa.
- Página de portafolio (`portafolio.html`): Muestra un portafolio de trabajos anteriores realizados por la empresa.
- Página de contacto (`contacto.html`): Permite a los usuarios enviar mensajes de contacto a la empresa. Los mensajes son enviados por correo electrónico utilizando Flask-Mail.
- Carrito de compras (`cart.html`): Permite a los usuarios agregar servicios al carrito y realizar transacciones.

## Consideraciones de diseño
- La aplicación utiliza Flask como framework web para el desarrollo del servidor.
- Se utiliza el lenguaje de plantillas Jinja para generar contenido dinámico en las páginas HTML.
- La base de datos SQLite se utiliza para almacenar la información de las transacciones de los usuarios.
- Se implementa una autenticación básica con sesiones de usuario utilizando Flask-Session.
- Se utiliza Flask-Mail para enviar correos electrónicos de confirmación al cliente cuando envía un mensaje de contacto.

