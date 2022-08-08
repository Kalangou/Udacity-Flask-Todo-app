import sys
from unicodedata import name
from flask import Flask, abort, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import desc

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/todosapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

'''
    Definition de la classe Todos
'''
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self) -> str:
        return f'<Todo {self.id} {self.description}>'

# db.create_all()

'''
    Methode création d'un todo
'''
@app.route('/todos/create', methods=['POST'])
def create_todo():
    body={}
    error = False
    try:
        description =  request.get_json()['description']
        todo = Todo(description=description)
        body['description'] = todo.description
        db.session.add(todo)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if  error == True:
            abort(400)
        else:
            return jsonify(body)

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())

if __name__ == '__main__' :
    app.run(host="0.0.0.0")