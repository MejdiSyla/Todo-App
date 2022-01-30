from email.policy import default
from flask import Flask, redirect, render_template, url_for, request, redirect 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return "<Task %r" % self.id

db.create_all()


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        task_content = request.form["content"]
        new_task = ToDo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue"
    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template("home.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting the note"

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task = ToDo.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form["content"]
        
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue updating the note"

    else:
        return render_template("update.html", task=task)


if __name__ == "__main__":
    app.run(debug=True)