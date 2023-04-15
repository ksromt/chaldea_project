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

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('posts', lazy=True))


@app.route("/")
def home():
    username = session.get('username', None)
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template("index.html", username=username, posts=posts)


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

@app.route("/create_post", methods=["GET", "POST"])
def create_post():
    if not session.get('username'):
        flash('You must be logged in to create a post.', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        author_id = User.query.filter_by(username=session['username']).first().id
        post = Post(title=title, content=content, author_id=author_id)
        db.session.add(post)
        db.session.commit()
        flash("Post created successfully!", "success")
        return redirect(url_for("home"))
    return render_template("create_post.html")

@app.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if session.get('username') != post.author.username:
        flash("You can only edit your own posts.", "danger")
        return redirect(url_for('home'))
    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        db.session.commit()
        flash("Post updated successfully!", "success")
        return redirect(url_for("home"))
    return render_template("edit_post.html", post=post)

@app.route("/post/<int:post_id>")
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("view_post.html", post=post)



if __name__ == "__main__":
    app.run(debug=True)
