from flask import Flask, render_template, request, url_for, redirect, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)


class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(250), unique=True,
						nullable=False)
	password = db.Column(db.String(250),
						nullable=False)

db.init_app(app)

with app.app_context():
	db.create_all()

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

@app.route('/register', methods=["GET", "POST"])
def register():
	if request.method == "POST":
		user = Users(username=request.form.get("username"),
					password=request.form.get("password"))
		db.session.add(user)
		db.session.commit()
		return redirect(url_for("login"))
	return render_template("sign_up.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    redirect_url = request.args.get('redirect') or url_for('home')
    if request.method == "POST":
        user = Users.query.filter_by(username=request.form.get("username")).first()
        if user is None:
            return render_template("login.html")
        if user.password == request.form.get("password"):
            print("User authenticated!")
            login_user(user)
            return redirect(redirect_url)
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/is_auth")
def is_auth():
    return jsonify({"is_auth": current_user.is_authenticated})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

