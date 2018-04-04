from flask import Flask, render_template, url_for, request
from src.querymanager import QueryManager

query = QueryManager()
app = Flask(__name__, '/static', static_folder='../static', template_folder='../templates')

@app.route('/')
@app.route('/signin')
@app.route('/signin.html')
def sign_in():
    return render_template('signin.html')

@app.route('/signup')
@app.route('/signup.html')
def sign_up():
    query.insert_user('username', 'username@gmail.com', 'password')
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
