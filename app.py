import ssl
from email.message import EmailMessage
from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify, abort
from random import randint
import smtplib
from flask_sqlalchemy import SQLAlchemy
from os.path import abspath

app = Flask(__name__)
db_path = abspath('.') + "\\databases\\users.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secre1234"
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'Item {self.username}'


# genera el codigo numerico de 6 digitos y lo envia por correo
def send_code(email: str) -> int:
    code = randint(100000, 999999)
    __message = f'Tu codigo de autenticacion es: {code}'
    __sender = "proyecto.prueba.mail.2022@gmail.com"
    __p = "fbbdepjnnwywjdlb"
    __port = 465
    __context = ssl.create_default_context()
    __receiver = email
    __smtp_server = "smtp.gmail.com"
    __subject = "codigo de verificacion"

    mail = EmailMessage()
    mail["From"] = __sender
    mail["To"] = __receiver
    mail["Subject"] = __subject
    mail.set_content(__message)

    try:
        with smtplib.SMTP_SSL(__smtp_server, __port, context=__context) as smtp:
            smtp.login(__sender, __p)
            smtp.sendmail(__sender, __receiver, mail.as_string())
        print("mail  enviado")
    except smtplib.SMTPException:
        flash("error al enviar correo")

    return code


@app.errorhandler(405)
def method_not_allowed(error):
    # Create a custom response for the HTTP error
    response = jsonify({'error': 'Method not allowed'})
    # Set the response status code to 405
    response.status_code = 405
    # Return the response
    return response


@app.errorhandler(404)
def not_found(error):
    response = jsonify({'error': 'Not found'})

    response.status_code = 404

    return response


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/check-user', methods=['POST', 'GET'])
def check_user():
    user = None
    email = None
    # if request.method != 'POST':
    #     abort(405)

    username = request.form['username']
    session["username"] = username
    if (user := User.query.filter_by(username=username).first()) is None:
        abort(404)

    email: str = user.email
    session["email"] = email
    print(session["email"])
    return redirect(url_for("login", email=email))


@app.route('/login', methods=['POST', 'GET'])
def login():
    # if request.method != 'POST':
    #     abort(405)
    # Get the user's email address from the form
    email: str = str(session["email"])

    # Generate a code and send it to the user's email
    code: int = send_code(email)
    session["code"] = code

    # Redirect the user to the login page and pass the code as a query parameter
    return redirect(url_for('login_with_code', username=email))


@app.route('/login_with_code', methods=['POST', 'GET'])
def login_with_code():
    return render_template('login_with_code.html', username=session["username"])


@app.route('/verify_code', methods=['POST', 'GET'])
def verify_code():
    # Get the code from the form
    code: int = int(request.form['code'])
    session_code: int = int(session['code'])
    # Check if the code entered by the user matches the code sent to their email
    if code == session_code:
        # If the code is correct, log the user in and redirect them to the dashboard
        session['logged_in'] = True
        print("sesdsion true")
        return redirect(url_for('dashboard'))
    else:
        # If the code is incorrect, show an error message
        error = 'Invalid code. Please try again.'
        print(error)
        print(f"code={code} session_code={session_code}")
        flash(error)
        return render_template('login_with_code.html',username=session["username"])


@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    # Only show the dashboard if the user is logged in
    if session['logged_in']:

        return render_template('dashboard/index.html', username=session["username"])
    else:

        return redirect(url_for('default'))


@app.route("/default")
def default():
    return render_template("default.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    # create the table
    app.run()
