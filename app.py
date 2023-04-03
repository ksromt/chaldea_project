from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hxllxyly'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kirisaki:hxllxyly@localhost/chaldea_test'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


@app.route("/")
def home():
    username = session.get('username', None)
    return render_template("index.html", username=username)


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         user = User(username=username, password=password)
#         db.session.add(user)
#         db.session.commit()
#         flash("Registration successful!", "success")
#         return redirect(url_for("home"))
#     return render_template("register.html")
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if the username already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("This user name has already been registered", "danger")
            return render_template("register.html")
        else:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            # flash("Registration successful!", "success")
            return redirect(url_for("home"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = user.username  # Store the username in a session variable
            flash('login successful！', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed, please check username or password.', 'danger')
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
