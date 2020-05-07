import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential, {
    'projectId': 'todo-app-python'
})
db = firestore.client()


def get_users():
    return db.collection('users').get()


def get_user(username):
    return db.collection('users').document(username).get()


def get_todos(user_id):
    return db \
        .collection('users') \
        .document(user_id) \
        .collection('todos') \
        .get()


def register_user(user_data):
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({'password': user_data.password})


def add_todo(user_id, description):
    todos_ref = db.collection('users').document(user_id).collection('todos')
    todos_ref.add({'description': description, 'done': False})


def delete_todo(user_id, todo_id):
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.delete()


def update_todo_status(user_id, todo_data):
    todo_ref = _get_todo_ref(user_id, todo_data['todo_id'])
    todo_ref.update({'done': not bool(todo_data['done'])})


def _get_todo_ref(user_id, todo_id):
    return db.document('users/{}/todos/{}'.format(user_id, todo_id))
