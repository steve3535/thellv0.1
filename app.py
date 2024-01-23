from flask import Flask, request, url_for, redirect, render_template
from flask_mail import Message, Mail
import mysql.connector 

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

db_host = '127.0.0.1'
db_port = 3307
db_user = 'admin'
db_password = 'admin'
db_name = 'signup_db'


def usergen(x,y):
    return x.lower()[1]+y

def sendmsg(rcpt,fname):
    try:       
       msg = Message("Inscription thelinuxlabs", recipients=[rcpt])
       msg.body = f"Cher {fname},\nMerci pour votre inscription.\n"
       mail.send(msg)
    except Exception as e:
       print(e)

def user_exists(email):
    try:
        conn = mysql.connector.connect(
           host = db_host,
           port = db_port,
           user = db_user,
           password = db_password,
           database = db_name 
        )

        cursor = conn.cursor()

        select_query = "select count(*) from signup where email = %s"
        
        cursor.execute(select_query,(email,))
        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return count > 0


    except mysql.connector.Error as e:
        print(e)


def newmember(fname,lname,email):
    if user_exists(email):
        return False 
    
    try:
        conn = mysql.connector.connect(
           host = db_host,
           port = db_port,
           user = db_user,
           password = db_password,
           database = db_name 
        )

        cursor = conn.cursor()

        insert_query = "INSERT INTO signup(firstname,lastname,email) values(%s,%s,%s);"
        
        data = (fname,lname,email)

        cursor.execute(insert_query,data)

        conn.commit()

        cursor.close()
        conn.close()

        return True


    except mysql.connector.Error as e:
        print(e)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    lastname = request.form['lastname']
    firstname = request.form['firstname']

    #gen username
    username = usergen(firstname.lower(),lastname.lower())

    #new member 
    if newmember(firstname,lastname,email):
        message = "Merci pour votre inscription ! Veuillez vérifier votre email"
    else:
        message = "Oups! un utilisateur avec la meme adresse email existe déjà"
    
    #return redirect(url_for('index'))
    return render_template('index.html',message=message)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)