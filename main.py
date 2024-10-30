from flask import Flask,render_template,url_for,redirect,request
import sqlite3
import smtplib
import email.message

def enviar_email(us,u):
    corpo_email = f"""
    <p>{us}</p>
    """
    msg = email.message.Message()
    msg['Subject'] = "Ação voluntária"
    msg['From'] = 'gustavossilva030@gmail.com'
    msg['To'] = f'{u}'
    password = 'osyk jfnv rwrt isvp' 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

cnn = sqlite3.connect("usuarios.db",check_same_thread=False)
app = Flask(__name__)

@app.route("/", methods=["POST","GET"])
def index():
    if request.method=="POST":
        nome = request.form.get("nome")
        sobrenome = request.form.get("sobre")
        telefone = request.form.get("telefone")
        email = request.form.get("email")
        text = [nome,sobrenome,email,telefone]
        for line in  text:
            print(line)
        comando="INSERT INTO USERS(NOME,SOBRENOME,TELEFONE,EMAIL) VALUES('",nome,"','",sobrenome,"',",telefone,",'",email,"');"
        comando_t="".join(comando)
        cnn.execute(comando_t)
        cnn.commit()
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/login/",methods=["POST","GET"])
@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "GET":
        return render_template("login.html",logado=True)
    nome_login=request.form.get("nome_login")
    email_login=request.form.get("email_login")
    if request.form.get("telefone_login"):
        telefone_login=int(request.form.get("telefone_login"))
    else:
        telefone_login=request.form.get("telefone_login")
    comando=f"SELECT * FROM USERS"
    comando_t="".join(comando)
    user_login= cnn.execute(comando_t)
    for r in user_login:
        user_email=r[3]
        user_telefone=r[2]
        user_name=r[0]
        if user_email == email_login and user_name == nome_login:
            return redirect(url_for("user"))
        elif user_telefone == telefone_login and user_name == nome_login:
            return redirect(url_for("user"))
        
    return render_template("login.html",logado = False)

@app.route("/user")
def user():
    return render_template("user.html")

@app.route('/admin',methods=["POST","GET"])
def admin():
    user_read=cnn.execute("SELECT * FROM USERS")
    if request.method == "POST":
        for u in user_read:
            user_noti=request.form.get(u[0])
            if user_noti == "":
                nao_enviado=True
            elif user_noti == None:
                nao_enviado=True
            else:   
                comando="UPDATE USERS SET NOTIFICATION='",user_noti,"' WHERE NOME='",u[0],"'"
                enviar_email(us=user_noti,u=u[3])
                comando_t="".join(comando)
                cnn.execute(comando_t)
                cnn.commit()
        return redirect(url_for("admin"))
    return render_template("admin.html",user_read=user_read)

@app.route("/delet/<Email>")
def delet(Email=""):
    if Email:
        comando=f"DELETE FROM USERS WHERE EMAIL='{Email}'"
        comando_t="".join(comando)
        cnn.execute(comando_t)
        cnn.commit()
        return "olhe o terminal"
    else:
        return "digite um email na url"
    #chamar valores pelo o email
if "__main__" == __name__:
    app.run(port="8000", debug=True)
#osyk jfnv rwrt isvp