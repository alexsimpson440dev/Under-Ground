from flask import Flask, render_template, url_for, request, redirect
from src.query_manager import QueryManager
from src.managers.session_manager import SessionManager
from src.managers.email_manager import EmailManager
from src.new_data_validator import NewDataValidator
from src.data_persist import DataPersist
import random
import sys

persist = DataPersist()
session_manager = SessionManager()
email_manager = EmailManager()
query = QueryManager()
validate = NewDataValidator()

app = Flask(__name__, '/static', static_folder='../static', template_folder='../templates')
app.secret_key = "changethisplz"


@app.route('/')
@app.route('/signin')
@app.route('/signin.html')
def sign_in():
    return render_template(url_for('sign_in'))


@app.route('/userlink', methods=['post', 'get'])
@app.route('/userlink.html')
def user_link():
    try:
        if session_manager.check_session('email') is False:
            if request.method == 'POST':
                manager = validate.validate_manager_id(request.form('account_id'))
                if manager is False:
                    print('incorrect manager ID')

                else:
                    print('correct manager ID')
                    return render_template(url_for('user_link'))

            else:
                return render_template(url_for('user_link'))

        else:
            return render_template(url_for('user_link'))  # todo: home page

    except:
        error = sys.exc_info()
        print(error)
        return redirect(url_for('sign_in'))  # todo: error page


@app.route('/signup', methods=['post', 'get'])
@app.route('/signup.html')
def sign_up():
    try:
        if session_manager.check_session('email') is False:
            if request.method == 'POST':
                new_user = request.form
                if validate.validate_user(new_user) and validate.validate_user_info(new_user) is True:
                    print("Valid")
                    persist.persist_user(new_user, manager_id='?')  # todo: get from user link. Validated then passed.
                    return render_template(url_for('sign_in'))
                else:
                    print("Not Valid")
                    return render_template(url_for('sign_up'))

            else:
                return render_template(url_for('sign_up'))

        else:
            return redirect(url_for('sign_up'))  # todo: sign out the current user, return to sign up
    except:
        error = sys.exc_info()
        print(error)
        return redirect(url_for('sign_up'))


@app.route('/managerinfo')
@app.route('/managerinfo.html')
def manager_info():
    if session_manager.check_session('email') is False:
        return render_template(url_for('manager_info'))

    else:
        return redirect(url_for('home'))


@app.route('/requestmanager', methods=['post', 'get'])
@app.route('/requestmanager.html')
def request_manager():
    if request.method == 'POST':
        session_manager.set_token_session(random.randint(100000, 999999))
        email = request.form.get('email')
        email_manager.send_email(email)

        return render_template('validatemanager.html')

    else:
        return render_template(url_for('request_manager'))


@app.route('/validatemanager', methods=['post', 'get'])
@app.route('/validatemanager.html')
def validate_token():
    if request.method == 'POST':
        token = request.form.get('token')

        if validate.validate_manager_token(token) is True:
            return render_template('managersignup.html')

        else:
            return redirect(url_for('sign_in'))

    return render_template(url_for('validate_token'))


@app.route('/managersignup', methods=['post', 'get'])
@app.route('/managersignup.html')
def manager_signup():
        if session_manager.check_session('email') is False:
            if request.method == 'POST':
                new_manager = request.form
                if validate.validate_user(new_manager) and validate.validate_user_info(new_manager) is True:
                    print("Valid Data")
                    persist.persist_manager(new_manager)
                    return render_template(url_for('sign_in'))
                else:
                    print("Not Valid")
                    return render_template(url_for('manager_signup'))

            else:
                return render_template(url_for('manager_signup'))

        else:
            return redirect(url_for('manager_signup'))  # todo: sign out the current user, return to sign up


if __name__ == '__main__':
    app.run(debug=True)
