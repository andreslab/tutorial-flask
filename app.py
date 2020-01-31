#https://www.youtube.com/watch?v=Z1RJmh_OqeA

#to freeze libraries of env "pip freeze > requirements.txt"



from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app) #inicializacion

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return'<Task %r>' % self.id

#then define database, i create
#1. in terminal execute "python"
#2. write "from app import db"
#3. and then "db.create_all()"

@app.route('/')
def index():
    return "Hello Word"

@app.route('/hola', methods=['POST', 'GET'])
def template_index():
    if request.method == 'POST':
        task_content = request.form['content'] #content is in form
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/hola')
        except:
            return "There was a issue adding your task"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/hola')
    except:
        return 'Thre was a problem that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:  
            db.session.commit()
            return redirect('/hola')
        except:
            return 'There was a issue updating your task'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)