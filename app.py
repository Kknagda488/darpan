from flask import Flask,render_template,request,redirect,flash,url_for
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,LoginManager
from flask_mail import Mail


app = Flask(__name__)
db = SQLAlchemy()
DB_NAME = "darpan.db"
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/darpan"
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = "kknagda488@gmail.com",
    MAIL_PASSWORD = "cpyozwlnpynpihch"
    )
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    age = db.Column(db.String(10),nullable=False)
    email = db.Column(db.String(900), nullable=False,)
    password = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    def __repr__(self):
        return '<User %r>' % self.username
class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    msg = db.Column(db.String(120),  nullable=False)
    date = db.Column(db.String(12), nullable=True)
@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email =request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('LOgin ho gyaa',category='success')
                return redirect(url_for('index'))
            else:
                flash('password glt hai ',category='error')
        else:
            flash('glt  email hai shai dalo',category='error') 

    return render_template("login.html")
@app.route("/register",methods=['GET','POST'])
def register():  
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        password = request.form.get("password")
        password1 = request.form.get("password1")

        user = User.query.filter_by(email=email).first()
        if user:
             flash('Already have acount !!',category='error')
        if len(email) < 4:
            flash("Email to short !!",category='error')
        elif len(name)< 4:
            flash("Name to small !!",category='error')
        elif password != password1:
            flash("password not match !!",category='error')
        elif len(password1)<= 6:
            flash("password to short",category='error')
        else:
            flash("Account created",category='sucess')
            new_user = User(email=email,name=name,password =generate_password_hash(password1, method='sha256'),age=age,gender=gender)

            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
    return render_template("register.html")
@app.route("/index")
def index():
    return render_template("index.html")
@app.route("/ptsd")
def ptsd():
    return render_template("ptsd.html")

@app.route("/peer_pressure")
def peer_pressure():
    return render_template("peer_pressure.html")
@app.route("/schizophrenia")
def schizophrenia():
    return render_template("schizophrenia.html")

@app.route("/drug")
def drug():
    return render_template("drug.html")

@app.route("/depression")
def depression():
    return render_template("depression.html")
@app.route("/anxity")
def anxity():
    return render_template("anxity.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")
@app.route("/contact",methods=['GET','POST'])
def contact():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        entry = Contacts(name=name, msg=message, email=email)
        db.session.add(entry)
        db.session.commit()
        mail.send_message(f'New message from {email}',
                          sender = email,
                          recipients = "kknagda488@gmail.com",
                          body = name + "\n" + message + "\n"
                          )
        if len(message) > 1:
            flash('Sent Sucessfuly','success')
            # return redirect('/contact')
    return render_template('contact.html')

@app.route("/about")
def about():
    return render_template("about.html")
if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)