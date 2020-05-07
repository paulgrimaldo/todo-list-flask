import unittest
from flask import render_template, session, redirect, url_for
from flask_login import login_required
from app import create_app

app = create_app()


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def handle_not_found(error):
    user_ip = session.get('user_ip')
    print('User IP: {}'.format(user_ip))
    return render_template('404.html', error=error)


@app.route('/', methods=['GET'])
@login_required
def index():
    return redirect('/todos/list')


if __name__ == "__main__":
    app.run(debug=True)
