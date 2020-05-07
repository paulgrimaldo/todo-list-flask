from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app.forms.delete_todo_form import DeleteTodoForm
from app.db.firestore_service import get_todos, add_todo, delete_todo, update_todo_status
from app.forms.todo_form import TodoForm
from app.forms.update_todo_status_form import UpdateTodoStatusForm
from . import todos


@todos.route('/list', methods=['GET', 'POST'])
@login_required
def index():
    username = current_user.id

    todos = get_todos(username)

    todo_form = TodoForm()
    update_form = UpdateTodoStatusForm()
    delete_form = DeleteTodoForm()

    context = {
        'todos': todos,
        'todo_form': todo_form,
        'delete_form': delete_form,
        'update_form': update_form
    }

    if todo_form.validate_on_submit():
        add_todo(username, todo_form.description.data)
        flash('Todo added successfully')
    return render_template('index.html', **context)


@todos.route('/delete/<todo_id>', methods=['POST'])
@login_required
def delete(todo_id):
    username = current_user.id

    delete_todo(user_id=username, todo_id=todo_id)

    flash('Todo deleted successfully')

    return redirect(url_for('index'))


@todos.route('/update/<todo_id>/<int:done>', methods=['POST'])
@login_required
def update(todo_id, done):
    username = current_user.id

    update_todo_status(username, {'todo_id': todo_id, 'done': done})

    flash('Todo status updated')

    return redirect(url_for('index'))
