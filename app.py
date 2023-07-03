from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # Telling Flask to use the current module as the starting point of the application.

app.app_context().push() # Provides access to context (important resources)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' # Path to Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disables modification tracking which improves performance 
                                                     # Modifications refer to changes in the database

db = SQLAlchemy(app) # Gets App

class Todo(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route('/')
def index():
    # Show all Todos
    todo_list = Todo.query.all()  # Returns List of all Items
    print(todo_list)
    return render_template('base.html', todo_list=todo_list)


@app.route("/add", methods = ["POST"])
def add():
# Add new items to the list
    title = request.form.get("title") # Gets from HTML (templates)
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index")) # Redirects user to home page


@app.route("/update/<int:todo_id>") # Used to identify which item to update
def update(todo_id):

    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index")) # Redirects user to home page



@app.route("/delete/<int:todo_id>") # Used to identify which item to update
def delete(todo_id):
    # Allows user to delete items
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index")) # Redirects user to home page



if __name__ == "__main__": # Code block that only runs when the script is executed directly (run)
    db.create_all()
    app.run(debug=True) # Begins development server 
   
