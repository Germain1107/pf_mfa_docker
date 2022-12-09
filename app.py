from flask import Flask, request, render_template, redirect, url_for, flash
from random import randint
from smtplib import SMTP
from flask_sqlalchemy import SQLAlchemy
from os.path import abspath

app = Flask(__name__)
db_path = abspath('.') + "users.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


# genera el codigo numerico de 6 digitos y lo envia por correo
def send_code(email):
    code = randint(100000, 999999)
    message = f'Your authentication code is: {code}'

    # Send the email with the code using the SMTP library
    with SMTP('smtp.gmail.com', 587) as smtp:
        __usr = "germainstephens07@gmail.com"
        __p = "Ger11yeli21"
        smtp.ehlo()
        smtp.starttls()
        smtp.login(__usr, __p)
        smtp.sendmail(__usr, email, message)

    return code


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/check-user', methods=['POST'])
def check_user():
    user = None
    username = None
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()

    if user:
        flash("usuario registrado")
        return redirect(url_for("index"))
    else:
        # User does not exist
        message = f"Usuario: {username} no esta registrado"
        flash(message)
        return redirect(url_for("index", message=message))


@app.route('/login', methods=['POST'])
def login():
    # Get the user's email address from the form
    email = request.form['username']

    # Generate a code and send it to the user's email
    code = send_code(email)

    # Redirect the user to the login page and pass the code as a query parameter
    return redirect(url_for('login_with_code', code=code, email=email))


@app.route('/login_with_code')
def login_with_code():
    # Get the code from the query parameters
    code = request.args.get('code')

    # Render the login page with the code
    return render_template('login_with_code.html', code=code)


@app.route('/verify_code', methods=['POST'])
def verify_code():
    # Get the code from the form
    code = request.form['code']

    # Check if the code entered by the user matches the code sent to their email
    if code == session['code']:
        # If the code is correct, log the user in and redirect them to the dashboard
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    else:
        # If the code is incorrect, show an error message
        error = 'Invalid code. Please try again.'
        return render_template('login_with_code.html', code=code, error=error)


@app.route('/dashboard')
def dashboard():
    # Only show the dashboard if the user is logged in
    if session['logged_in']:
        return render_template('login_with_code.html')
    else:
        return redirect(url_for('login'))


if __name__ == "__main__":
    # create the table
    # db.create_all()
    app.run(debug=True)
