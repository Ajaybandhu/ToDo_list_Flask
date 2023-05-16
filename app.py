from flask import Flask,render_template,url_for,redirect,request
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

app =Flask(__name__ )
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///sqlite.db'

db.init_app(app)
app_context =app.app_context()
class ToDO(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    title =db.Column(db.String(100))
    complete =db.Column(db.Boolean, default=False) 




@app.route('/')
def index():
    todo_list =ToDO.query.all()
    total_todo =ToDO.query.count()
    completed_todo =ToDO.query.filter_by(complete=True).count()
    uncomplete_todo=total_todo-completed_todo
    return render_template('dashboard/index.html',**locals())

@app.route('/add',methods=['POST'])
def add():
    title = request.form.get('title')
    new_todo =ToDO(title=title,complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    todo =ToDO.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>')
def update(id):
    todo = ToDO.query.filter_by(id=id).first()
    todo.complete=not todo.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('dashboard/about.html')


if __name__ == '__main__':
    app.run(debug=True)




