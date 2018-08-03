import random
import sys

from flask import Flask, render_template, url_for, request, redirect

from src.data_persist import DataPersist
from src.managers.email_manager import EmailManager
from src.managers.session_manager import SessionManager
from src.new_data_validator import NewDataValidator

persist = DataPersist()
session = SessionManager()
email_manager = EmailManager()
validate = NewDataValidator()

app = Flask(__name__, '/static', static_folder='../static', template_folder='../templates')
app.secret_key = "changethisplz"  # todo: change this

# TODO: ABSTRACT METHODS FROM THE SERVER!!! TO MANY LOOPS
# TODO: ^^^ --- PUT VERIFICATION ON PERSISTING SIDE??


@app.route('/', methods=['get', 'post'])
@app.route('/signin.html', methods=['get', 'post'])
def sign_in():
    if session.check_session('email'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        credentials = request.form
        if validate.validate_sign_in(credentials):
            return render_template(url_for('index'))

        else:
            return redirect(url_for('sign_in'))
            # check for valid username
            # if valid, check that password matches
            # if both, sign in
            # else, return false - error logging in username or password is incorrect

    return render_template(url_for('sign_in'))


@app.route('/index.html', methods=['get', 'post'])
def index():
    if session.check_session('email') is False:
        return redirect(url_for('sign_in'))

    if request.method == 'POST':
        sign_out()
        return redirect(url_for('sign_in'))

    return render_template(url_for('index'))


@app.route('/signup.html')
@app.route('/sign/signup', methods=['post', 'get'])
def sign_up():
        if session.check_session('email') is False:
            if request.method == 'POST':
                new_user = request.form
                if validate.validate_user(new_user) and validate.validate_user_info(new_user) is True:
                    print("Valid")
                    manager_id = request.args.get('manager_id')
                    print(manager_id)
                    persist.persist_user(new_user, manager_id)
                    return render_template(url_for('sign_in'))  # todo: move to home page
                else:
                    print("Not Valid")
                    return redirect(url_for('sign_up', Page=3))

            else:
                return render_template('signup.html', Page=3)

        else:
            return redirect(url_for('index'))


@app.route('/sign/managerid', methods=['post', 'get'])
def user_link():
        if session.check_session('email'):
            return redirect(url_for('index'))
    # try:
        # clears session -- continue
        if request.method == 'POST':
            # sends the forms id to validate against manager table and redirects to signup page if valid
            manager = validate.validate_manager_id(request.form['account_id'])
            manager_id = manager.manager_id  # todo: May throw error if no manager exists

            if manager_id:
                print('correct manager ID')
                print(manager_id)
                return redirect(url_for('sign_up', manager_id=manager_id, Page=1))

            else:
                print('incorrect manager ID')

        else:
            return render_template('signup.html', Page=0)

    # except:
    #     error = sys.exc_info()
    #     print(error)
    #     return redirect(url_for('sign_in'))  # todo: error page


@app.route('/signup.html')
@app.route('/sign/requestmanager', methods=['post', 'get'])
def request_manager():
    if session.check_session('email'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        session.set_session('token', random.randint(100000, 999999))
        email = request.form.get('email')
        email_manager.send_email(email)

        return redirect(url_for('validate_token'))

    else:
        if session.check_session('email') is False:
            return render_template('signup.html', Page=1)

    return redirect(url_for('index'))


@app.route('/signup.html')
@app.route('/sign/validatetoken', methods=['post', 'get'])
def validate_token():
    if session.check_session('token') is False:
        return redirect(url_for('sign_in'))

    if request.method == 'POST':
        token = request.form.get('token')

        if validate.validate_manager_token(token) is True:
            return redirect(url_for('manager_signup'))

        else:
            return redirect(url_for('sign_in'))

    return render_template('signup.html', Page=2)


@app.route('/signup.html')
@app.route('/sign/managersignup', methods=['post', 'get'])
def manager_signup():
    if session.check_session('token') is False:
        return redirect(url_for('sign_in'))

    if session.check_session('email') is False:
        if request.method == 'POST':
            new_manager = request.form
            if validate.validate_user(new_manager) and validate.validate_user_info(new_manager) is True:
                persist.persist_manager(new_manager)
                return redirect(url_for('create_bill_account'))
            else:
                return redirect(url_for('manager_signup'))

        return render_template('signup.html', Page=3)

    else:
        return redirect(url_for('index'))


@app.route('/createbillaccount', methods=['post', 'get'])
@app.route('/createbillaccount.html', methods=['get'])
def create_bill_account():
    if session.check_session('token') is False:
        return redirect(url_for('sign_in'))

    if request.method == 'POST':
        bill_account = request.form
        if validate.validate_bill_config(bill_account) is True:
            persist.persist_bill_account(bill_account, session.get_session('email'))

            return render_template(url_for('sign_in'))

        return redirect(url_for('create_bill_account'))

    return render_template(url_for('create_bill_account'))


def sign_out():
    print('Log: User ' + session.get_session('email') + ' is signing out.')
    session.clear_session('email')


if __name__ == '__main__':
    app.run(debug=True)
