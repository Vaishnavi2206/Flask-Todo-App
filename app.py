from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'test_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):  
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())
    
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/',methods=['GET'])
def index():
    todos = Todo.query.all();
    return render_template('index.html',todos=todos)

@app.route('/create',methods=['GET'])
def create():
    return render_template('form.html')

@app.route('/submit',methods=['POST'])
def submit():
    title = request.form.get('title')
    description = request.form.get('description')
    
    if title and description:
        new_todo = Todo(title=title,description=description)
        db.session.add(new_todo)
        db.session.commit()
        flash("Todo created successfully!", 'success')
        return redirect('/');
    return "Error Missing Data", 400

@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    todo = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.description = request.form['description']
        db.session.commit();
        flash("Todo edited successfully!", 'success')
        return redirect('/')
    return render_template('form.html',todo=todo, action="edit")
    
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    flash("Todo deleted successfully!", 'success')
    return redirect('/')

@app.get('/projects/')
def hello_projects():
    return "Hello projects"

if __name__ == "__main__":
    app.run(debug=True)
    



