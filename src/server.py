from flask import Flask, render_template, url_for, request
app = Flask(__name__, '/static', static_folder='../static', template_folder='../templates')

@app.route('/')
@app.route('/signin')
@app.route('/signin.html')
def sign_in():
    return render_template('signin.html')

@app.route('/signup')
@app.route('/signup.html')
def sign_up():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
