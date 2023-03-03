from flask import Flask,render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy

# db connect
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/serda/OneDrive/Masaüstü/sa/todo.db'
db = SQLAlchemy(app)

# db Column add
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80))
    complate = db.Column(db.Boolean())


# route index.html
@app.route("/")
def index():
   todos = User.query.all()
   return render_template("index.html",todos = todos)

# todo tamamla
@app.route("/complate/<string:id>")
def complatetodo(id):
    todo = User.query.filter_by(id = id).first()

    todo.complate = not todo.complate

    db.session.commit()

    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def delete(id):
    todo = User.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

# add todo
@app.route("/add", methods = ["POST"])
def todoadd():
    title = request.form.get("title")
    newtodo = User(title = title, complate = False)
    db.session.add(newtodo)
    db.session.commit()

    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
