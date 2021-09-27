from chatterbot import trainers
from flask import * 
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_login import LoginManager, UserMixin, login_manager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer


app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

covibot = ChatBot("COVIBOT")
trainer = ListTrainer(covibot)
trainer.train([
    "hi",
    "hello, how can i help you ?",
    "tata",
    "bye, take care!",
    "good morning",
    "good morning",
    "good night",
    "good night",
    "good afternoon",
    "good afternoon",
    "good evening",
    "good evening",
    "what is your name ?",
    "covibot",
    "who created you ?",
    "RAO ANIRUDHRA ",
    "thankyou",
    "welcome",
    "How does COVID-19 spread?",
    "Current evidence suggests that the virus spreads mainly between people who are in close contact with each other, typically within 1 metre (short-range). A person can be infected when aerosols or droplets containing the virus are inhaled or come directly into contact with the eyes, nose, or mouth.",
    "What causes COVID-19?",
    "COVID-19 is caused by infection with the severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2) virus strain",
    "how to book vaccination slot ?",
    "you can book your slot from https://www.cowin.gov.in/",
    "how to prevent corona?",
    "Wear a mask.Clean your hands, Maintain safe distance of 1 meter, Get vaccinated.",
    "self care for corona",
    "1)isolate yourself 2)wear mask of three layer, 3)drink a lot of fluids, 3)monitor temperature,oxygen 4) frequent hand washing for atleast 40 second",
    "what are the side effect of vaccine ?",
    "Reported side effects to COVID-19 vaccines have mostly been mild to moderate and short-lasting. They include: fever, fatigue, headache, muscle pain, chills, diarrhoea, and pain at the injection site.",
    "Covaxin Side Effects",
    "Covaxin can be painful at the injection site, there may be swelling, there may be redness at the place of injection, there may also be dizziness and weakness, rashes all over the body are also likely to increase heartbeat.There may be swelling on the throat and difficulty in breathing, allergic reaction, vomitings, nausea, malaise, fever, headache, body ache, pain in the arm on which the injection has been done, may also occur. Stiffness in the upper arm can have effects. But no clear information has been received about it yet.",
    "Covishield Side Effects",
    "After injecting Covishield, you may have pain at the injection site, may have headaches, may have joint pain, may feel like feverish, general feeling unwell, itching may also at the injection site, Swelling may also look like warmth and tenderness.There is no clear information about this, it has been said on the basis of an assumption that this can happen after the injection, but so far no obvious effects of its bad effects have been revealed.",
    "Covishield vaccine Dose gap",
    "4-6 weeks.",
    "efficacy of covishield",
    "overall after second dose 70-90%.",
    "covaxin dose gap",
    "28 days",
    "efficacy of covaxin",
    "overall after second dose 78-95%"

])

app.config['SECRET_KEY'] = 'c1155c6a351e49eba15c00ce577b259e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.sqlite'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=15)], render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=15)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists. Please choose a different one.")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=15)], render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[InputRequired(), Length(max=50)], render_kw={"placeholder":  "Password"})
    submit = SubmitField("Login")



@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for("dashboard"))
                flash("User does not exist, or invalid username or password.")
    return render_template('login.html', form = form)

@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    return render_template('dash.html')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form = form)
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(covibot.get_response(userText))

@app.route('/logout', methods=["GET","POST"])
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)