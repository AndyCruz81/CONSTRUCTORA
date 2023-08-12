import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for,jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Mail, Message
import datetime
from helpers import login_required



app = Flask(__name__)

# Configuración de Flask-Mail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_DEBUG"] = True
app.config["MAIL_USERNAME"] = "minicoc81@gmail.com"
app.config["MAIL_PASSWORD"] = "hmdcxmvxajafnumz"
app.config["MAIL_DEFAULT_SENDER"] = "minicoc81@gmail.com"

# Inicializar la extensión Flask-Mail
mail = Mail(app)

# Utilizacion de FLASH
app.secret_key = "supersecretkey"

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///constructora.db")

# Rutas de la aplicación


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
# @login_required
def index():
    return render_template("index.html")


@app.route("/proyectos")
# @login_required
def nosotros():
    return render_template("proyectos.html")


@app.route("/servicios", methods=["GET", "POST"])
# @login_required
def servicios():
    return render_template("servicios.html")


@app.route("/portafolio")
# @login_required
def portafolio():
    return render_template("portafolio.html")


@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        correo = request.form.get("correo")
        telefono = request.form.get("telefono")
        mensaje = request.form.get("mensaje")

        if not correo:  # Validación del campo de correo
            flash("El campo de correo es obligatorio.", 'error')
            return redirect(url_for("contacto"))

        try:
            # Enviar el correo de confirmación al cliente
            msg_cliente = Message(
                "Confirmación de recepción de mensaje", recipients=[correo]
            )
            msg_cliente.body = f"""
            Hola {nombre},

            Hemos recibido tu mensaje y nos pondremos en contacto contigo pronto.

            Gracias,
            Luli´s Construction
            """
            mail.send(msg_cliente)

            # Procesar los datos recibidos
            # ...
            # db.execute(
            #     "INSERT INTO contactoLibre (nombre, apellido, correo, telefono, mensaje, fecha) VALUES (?, ?, ?, ?, ?, ?)",
            #     (nombre, apellido, correo, telefono, mensaje, datetime.datetime.now())
            # )

            flash("Hemos recibido tu mensaje!", 'success')
            return redirect(url_for("contacto"))
        except Exception as e:
            flash(
                "Hubo un error al enviar el correo. Por favor, inténtalo nuevamente más tarde.",
                'error',
            )
            app.logger.error(str(e))
            return render_template("contacto.html")

    # Renderizar la página de contacto en caso de solicitudes GET o si no se envió el formulario
    return render_template("contacto.html")


@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    if request.method == "POST":
        servicio = request.form.get("ser")
        db.execute(
            "INSERT INTO transacciones (usuario_id, servicio_id, fecha) VALUES(?,?,?)",
            session["user_id"],
            servicio,
            datetime.datetime.now(),
        )

    carrito = db.execute(
        "SELECT * FROM servicios JOIN transacciones ON servicios.id = transacciones.servicio_id WHERE transacciones.usuario_id = ? ORDER BY transacciones.fecha DESC",
        session["user_id"],
    )

    return render_template("carrito.html", carrito=carrito)


# Nueva ruta /eliminar-transaccion/<int:transaccion_id>
# que acepta un parámetro transaccion_id en la URL. La función eliminar_transaccion()
# ejecuta una consulta DELETE en la base de datos para eliminar la transacción con el ID especificado.

@app.route("/eliminar-transaccion/<int:transaccion_id>", methods=["DELETE"])
@login_required
def eliminar_transaccion(transaccion_id):
    db.execute("DELETE FROM transacciones WHERE id = ?", transaccion_id)
    flash("ELIMINADO")
    return jsonify({'message': 'Transacción eliminada exitosamente'})



@app.route("/logIn", methods=["GET", "POST"])
def logIn():
    """Log user in"""

    # Forget any user_id and is_admin
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        if not username:
            flash("Agrega un usuario!", "error")
            return render_template("logIn.html")

        # Ensure password was submitted
        password = request.form.get("password")
        if not password:
            flash("Agrega una contraseña!", "error")
            return render_template("logIn.html")

        # Query database for username
        rows = db.execute("SELECT * FROM usuarios WHERE nombre = ?", (username,))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["contraseña"], password):
            flash("Usuario o contraseña inválidos!", "error")
            return render_template("logIn.html")

        # Check if user is admin
        is_admin = rows[0]["es_admin"]

        # Remember user_id and is_admin in session
        session["user_id"] = rows[0]["id"]
        session["is_admin"] = is_admin

        # Redirect user to appropriate page
        if is_admin:
            return redirect("/admin")
        else:
            return redirect("/cart")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("logIn.html")



@app.route("/Register", methods=["GET", "POST"])
def Register():
    """Register user"""
    if request.method == "GET":
        return render_template("Register.html")
    else:
        username = request.form.get("username")
        mail = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            flash("AGREGA UN USUARIO!", "error")
            return render_template("Register.html")

        if not password:
            flash("AGREGA UNA CONTRASEÑA!", "error")
            return render_template("Register.html")

        if not confirmation:
            flash("CONFIRMA TU CONTRASEÑA!", "error")
            return render_template("Register.html")

        if not mail:
            flash("AGREGA UN CORREO!", "error")
            return render_template("Register.html")

        if password != confirmation:
            flash("CONTRASEÑAS INCORRECTAS", "error")
            return render_template("Register.html")

        filterUser = db.execute(
            "SELECT nombre FROM usuarios WHERE nombre = ?", (username,)
        )

        if len(filterUser) >= 1:
            flash("USUARIO EXISTENTE", "error")
            return render_template("Register.html")
        else:
            hashed_password = generate_password_hash(password)  # Hashear la contraseña
            new_user = db.execute(
                "INSERT INTO usuarios (nombre, correo, contraseña) VALUES (?, ?, ?)",
                username,
                mail,
                hashed_password,
            )
            if not new_user:
                flash("ERROR AL REGISTRARSE", "error")
                return render_template("Register.html")



        session["user_id"] = new_user

        flash("REGISTRADO CON ÉXITO!", "success")
        return redirect("/cart")   # El usuario es administrador


# VERIFICADOR
def verificar_administrador(user_id):
    # Realiza una consulta a la base de datos para obtener el usuario por su ID
    usuario = db.execute("SELECT es_admin FROM usuarios WHERE id = ?", user_id)

    if usuario and usuario[0]["es_admin"]:
        return True  # El usuario es administrador
    else:
        return False  # El usuario no es administrador

@app.route("/admin")
@login_required
def admin():
    if verificar_administrador(session["user_id"]):
        return render_template("admin.html")
    else:
        flash("Acceso denegado. Debes ser administrador para acceder a esta página.", "error")
        return redirect(url_for("index"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/logOut")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


if __name__ == "__main__":
    app.run()
