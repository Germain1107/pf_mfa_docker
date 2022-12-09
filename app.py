from flask import Flask, request, render_template, redirect, url_for
from random import randint
from smtplib import SMTP

app = Flask(__name__)


# genera el codigo numerico de 6 digitos y lo envia por correo
def send_code(email):
    code = randint(100000, 999999)
    message = 'Your authentication code is: {}'.format(code)

    # Send the email with the code using the SMTP library
    with SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('YOUR_EMAIL_ADDRESS', 'YOUR_EMAIL_PASSWORD')
        smtp.sendmail('YOUR_EMAIL_ADDRESS', email, message)

    return code


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    # Get the user's email address from the form
    email = request.form['email']

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
    app.run(debug=True)