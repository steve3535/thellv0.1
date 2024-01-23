from flask import Flask, request, url_for, redirect, render_template
from flask_mail import Message, Mail

app = Flask(__name__)
app.secret_key = '123456'
# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'steve@thelinuxlabs.com'
app.config['MAIL_PASSWORD'] = 'ongz ukyw lezw zimx'
app.config['MAIL_DEFAULT_SENDER'] = 'steve@thelinuxlabs.com'
mail = Mail(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    lastname = request.form['lastname']
    firstname = request.form['firstname']

    try:
        print(f"Hello {lastname}")
    except Exception as e:
        print(e)

    try:
        
  msg = Message("Inscription workshop 'La confiance en soi'", recipients=[email])
  msg.body = f"Thank you for registering!\nusername = {first_name}"
  mail.send(msg)
except Exception as e:
    print("bad credentials for the mail or someth else ...",e)

    print(f"Merci pour votre inscription ! Veuillez vérifier votre email")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)