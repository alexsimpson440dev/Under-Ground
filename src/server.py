import random
import sys

from flask import Flask, render_template, url_for, request, redirect

from src.data_persist import DataPersist
from src.managers.email_manager import EmailManager
from src.managers.session_manager import SessionManager
from src.new_data_validator import NewDataValidator

persist = DataPersist()
session_manager = SessionManager()
email_manager = EmailManager()
validate = NewDataValidator()

app = Flask(__name__, '/static', static_folder='../static', template_folder='../templates')
app.secret_key = "changethisplz"  # todo: change this


@app.route('/')
@app.route('/signin')
@app.route('/signin.html')
def sign_in():
    return render_template(url_for('sign_in'))


@app.route('/signup', methods=['post', 'get'])
@app.route('/signup.html', methods=['get'])
def sign_up():
        if session_manager.check_session('email') is False:
            if request.method == 'POST':
                new_user = request.form
                if validate.validate_user(new_user) and validate.validate_user_info(new_user) is True:
                    print("Valid")
                    manager_id = request.args.get('manager_id')
                    print(manager_id)
                    persist.persist_user(new_user, manager_id=request.args.get('manager_id'))
                    return render_template(url_for('sign_in'))
                else:
                    print("Not Valid")
                    return render_template(url_for('sign_up'))

            else:
                return render_template(url_for('sign_up'))

        else:
            return redirect(url_for('sign_up'))  # todo: sign out the current user, return to sign up


@app.route('/userlink', methods=['post', 'get'])
@app.route('/userlink.html', methods=['get'])
def user_link():
    try:
        if session_manager.check_session('email') is False:
            if request.method == 'POST':
                manager_id = validate.validate_manager_id(request.form['account_id'])
                if manager_id is False:
                    print('incorrect manager ID')

                else:
                    print('correct manager ID')
                    print(manager_id)
                    return render_template('signup.html', manager_id=manager_id)

            else:
                return render_template(url_for('user_link'))

        else:
            return render_template(url_for('user_link'))  # todo: home page

    except:
        error = sys.exc_info()
        print(error)
        return redirect(url_for('sign_in'))  # todo: error page


@app.route('/managerinfo')
@app.route('/managerinfo.html')
def manager_info():
    if session_manager.check_session('email') is False:
        return render_template(url_for('manager_info'))

    else:
        return redirect(url_for('home'))


@app.route('/requestmanager', methods=['post', 'get'])
@app.route('/requestmanager.html', methods=['get'])
def request_manager():
    if request.method == 'POST':
        session_manager.set_token_session(random.randint(100000, 999999))
        email = request.form.get('email')
        email_manager.send_email(email)

        return redirect(url_for('validate_token'))

    else:
        return render_template(url_for('request_manager'))


@app.route('/validatemanager', methods=['post', 'get'])
@app.route('/validatemanager.html', methods=['get'])
def validate_token():
    if request.method == 'POST':
        token = request.form.get('token')

        if validate.validate_manager_token(token) is True:
            return redirect(url_for('manager_signup'))

        else:
            return redirect(url_for('sign_in'))

    return render_template(url_for('validate_token'))


@app.route('/managersignup', methods=['post', 'get'])
@app.route('/managersignup.html', methods=['get'])
def manager_signup():
        if session_manager.check_session('email') is False:
            if request.method == 'POST':
                new_manager = request.form
                if validate.validate_user(new_manager) and validate.validate_user_info(new_manager) is True:
                    print("Valid Data")
                    persist.persist_manager(new_manager)
                    return redirect(url_for('sign_in'))
                else:
                    print("Not Valid")
                    return render_template(url_for('manager_signup'))

            else:
                return render_template(url_for('manager_signup'))

        else:
            return redirect(url_for('manager_signup'))  # todo: sign out the current user, return to sign up


if __name__ == '__main__':
    app.run(debug=True)
