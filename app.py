from flask import Flask, request, url_for, redirect, render_template
from flask_mail import Message, Mail
import mysql.connector,subprocess  
import socket 

cluster=[{'name':'popos','ip':'','admin_user':'steve'}]
CLUSTER0_ADMIN_USER="steve"


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

def get_current_ip(hostname):
    return socket.gethostbyname(hostname)

def usergen(x,y):
    return x.lower()[0]+y

def sendmsg(rcpt,fname,link):
    try:       
       msg = Message("Inscription thelinuxlabs", recipients=[rcpt])
       msg.body = f"Cher {fname},\nMerci pour votre inscription.\nConnectez vous à la plateforme en utilisant le lien {link} valable 24h.\n"
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


def create_ipa_user(username,fname,lname,email):
    cluster[0]['ip']=get_current_ip("kwakousteve.ddns.net")
    #print(cluster[0]['ip'])
    cmd = ['ssh','-p','2222',f'{cluster[0]["admin_user"]}@{cluster[0]["ip"]}','ssh','idm','sudo','ipa','user-add',f'{username}','--first',fname,'--last',lname,'--email',email,f'--homedir="/home/{username}"','--shell="/bin/bash"']
    #print(cmd)
    try:
        result = subprocess.run(cmd,text=True,capture_output=True)
        print(result.stdout) 
        if result.returncode == 0:
            print(username+' created successfully on IPA')
            return True 
    except Exception as e:
        print('error -->',e)
        return False  

     # cmd_output=subprocess.run(['ssh',f'ubuntu@{PUBLIC_IP}','sudo','useradd','-m',email,'-s','/bin/bash'],text=True,capture_output=True)


def create_teleport_user(username):
    cmd = ['sudo','tctl','users','add',f'{username}','--logins',f'{username}','--roles=access','--ttl=24h']
    try:
        result = subprocess.run(cmd,text=True,capture_output=True)
        print('Teleport user created successfully')
        link=result.stdout.split('\n')[1]
        # print(link)
        # print("-->"+str(link))
        # print(f'Lien de connexion {link} valide pour 24h.')
        
        return link
    except Exception as e:
        print(e)
        return "" 

def newmember(fname,lname,email):
    if user_exists(email):
        return False 
    
    #gen username
    username = usergen(fname.lower(),lname.lower())

    
    if not(create_ipa_user(username,fname,lname,email)):
        print('unable to create ipa user')
        return False 

    link=create_teleport_user(username)
    if len(link)==0:
        print('unable to create teleport user')
        return False 
    else:
        sendmsg(email,fname,link)
    
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

    
    #new member 
    if newmember(firstname,lastname,email):
        message = "Merci pour votre inscription ! Veuillez vérifier votre email"
    else:
        message = "Oups! une erreur a empêché la création de votre compte - contactez steve@thelinuxlabs.com"
    
    #return redirect(url_for('index'))
    return render_template('index.html',message=message)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)