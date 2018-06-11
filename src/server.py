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

# TODO: ABSTRACT METHODS FROM THE SERVER!!! TO MANY LOOPS
# TODO: ^^^ --- PUT VERIFICATION ON PERSISTING SIDE??


@app.route('/')
@app.route('/signin')
@app.route('/signin.html')
def sign_in():
    session_manager.clear_session()
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
                    persist.persist_user(new_user, manager_id)
                    return render_template(url_for('sign_in'))
                else:
                    print("Not Valid")
                    return redirect(url_for('sign_up'))

            else:
                return render_template(url_for('sign_up'))

        else:
            return redirect(url_for('sign_up'))  # todo: sign out the current user, return to sign up


@app.route('/userlink', methods=['post', 'get'])
@app.route('/userlink.html', methods=['get'])
def user_link():
    try:
        # clears session -- continue
        session_manager.clear_session()
        if request.method == 'POST':
            # sends the forms id to validate against manager table and redirects to signup page if valid
            manager = validate.validate_manager_id(request.form['account_id'])
            manager_id = manager.manager_id

            if manager_id:
                print('correct manager ID')
                print(manager_id)
                return redirect(url_for('sign_up', manager_id=manager_id))

            else:
                print('incorrect manager ID')

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
                    return redirect(url_for('create_bill_account'))
                else:
                    print("Not Valid")
                    return render_template(url_for('manager_signup'))

            else:
                return render_template(url_for('manager_signup'))

        else:
            return redirect(url_for('manager_signup'))  # todo: sign out the current user, return to sign up


@app.route('/createbillaccount', methods=['post', 'get'])
@app.route('/createbillaccount.html', methods=['get'])
def create_bill_account():
    if request.method == 'POST':
        # no current validation needed. One default account type for now
        bill_account = request.form
        if validate.validate_bill_config(bill_account) is True:
            persist.persist_bill_account(bill_account, session_manager.get_session('email'))

            return render_template(url_for('sign_in'))

        return redirect(url_for('create_bill_account'))

    return render_template(url_for('create_bill_account'))


if __name__ == '__main__':
    app.run(debug=True)
