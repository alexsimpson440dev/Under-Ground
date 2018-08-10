import random
import sys

from flask import Flask, render_template, url_for, request, redirect

from src.data_persist import DataPersist
from src.managers.email_manager import EmailManager
from src.managers.query_manager import QueryManager
from src.managers.session_manager import SessionManager
from src.new_data_validator import NewDataValidator

persist = DataPersist()
session = SessionManager()
query = QueryManager()
email_manager = EmailManager()
validate = NewDataValidator()

app = Flask(__name__, '/static', static_folder='../static', template_folder='../templates')
app.secret_key = "changethisplz"  # todo: change this

# TODO: ABSTRACT METHODS FROM THE SERVER!!! TO MANY LOOPS
# TODO: ^^^ --- PUT VERIFICATION ON PERSISTING SIDE??


@app.route('/')
@app.route('/index.html', methods=['get', 'post'])
def index():
    try:
        if not session.check_session('email'):
            return redirect(url_for('sign_in'))

        if request.method == 'POST':
            sign_out()
            return redirect(url_for('sign_in'))

        return render_template(url_for('index'))

    except:
        error = str(sys.exc_info())
        logger('Log E Error in index')
        logger('Log E ' + error)
        return render_template('error.html')


@app.route('/sign.html')
@app.route('/signin.html', methods=['get', 'post'])
def sign_in():
    try:
        if session.check_session('email'):
            return redirect(url_for('index'))

        if request.method == 'POST':
            credentials = request.form
            if validate.validate_sign_in(credentials):
                return redirect(url_for('index'))

            else:
                return redirect(url_for('sign_in'))

        return render_template(url_for('sign_in'))

    except:
        error = str(sys.exc_info())
        logger('Log E Error in sign_in')
        logger('Log E ' + error)
        return render_template('error.html')


@app.route('/signup.html')
@app.route('/sign/signup', methods=['post', 'get'])
def sign_up():
    try:
        if not session.check_session('email'):
            if request.method == 'POST':
                new_user = request.form
                if validate.validate_user(new_user) and validate.validate_user_info(new_user) is True:
                    manager_id = request.args.get('manager_id')
                    persist.persist_user(new_user, manager_id)
                    return redirect(url_for('index'))
                else:
                    return redirect(url_for('sign_up', Page=3))

            return render_template('signup.html', Page=3)

        return render_template(url_for('index'))

    except:
        error = str(sys.exc_info())
        logger('Log E Error in sign_up')
        logger('Log E ' + error)
        return render_template('error.html')


@app.route('/sign/managerid', methods=['post', 'get'])
def user_link():
    try:
        if session.check_session('email'):
            return redirect(url_for('index'))

        if request.method == 'POST':
            # sends the forms id to validate against manager table and redirects to signup page if valid
            manager = validate.validate_manager_id(request.form['account_id'])
            if manager:
                manager_id = manager.manager_id  # todo: May throw error if no manager exists
                if manager_id:
                    logger('Log: ManagerID found')
                    return redirect(url_for('sign_up', manager_id=manager_id, Page=1))

            else:
                logger('Log: ManagerID not found')

        return render_template('signup.html', Page=0)

    except:
        error = str(sys.exc_info())
        logger('Log E Error in user_link')
        logger('Log E ' + error)
        return render_template('error.html')


@app.route('/signup.html')
@app.route('/sign/requestmanager', methods=['post', 'get'])
def request_manager():
    try:
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

    except:
        error = str(sys.exc_info())
        logger('Log E Error in request_manager')
        logger('Log E ' + error)
        return render_template('error.html')


@app.route('/signup.html')
@app.route('/sign/validatetoken', methods=['post', 'get'])
def validate_token():
    try:
        if not session.check_session('token'):
            return redirect(url_for('sign_in'))

        if request.method == 'POST':
            token = request.form.get('token')

            if validate.validate_manager_token(token) is True:
                return redirect(url_for('manager_signup'))

            else:
                return redirect(url_for('sign_in'))

        return render_template('signup.html', Page=2)

    except:
        error = str(sys.exc_info())
        logger('Log E Error in validate_token')
        logger('Log E ' + error)
        return render_template('error.html')


@app.route('/signup.html')
@app.route('/sign/managersignup', methods=['post', 'get'])
def manager_signup():
    try:
        if not session.check_session('token'):
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

    except:
        error = str(sys.exc_info())
        logger('Log E Error in manager_signup')
        logger('Log E ' + error)
        return render_template('error.html')


@app.route('/createbillaccount', methods=['post', 'get'])
@app.route('/createbillaccount.html', methods=['get'])
def create_bill_account():
    try:
        if not session.check_session('token'):
            return redirect(url_for('sign_in'))

        if request.method == 'POST':
            bill_account = request.form
            if validate.validate_bill_config(bill_account) is True:
                persist.persist_bill_account(bill_account, session.get_session('email'))

                return render_template(url_for('index'))

            return redirect(url_for('create_bill_account'))

        return render_template(url_for('create_bill_account'))

    except:
        error = str(sys.exc_info())
        logger('Log E Error in create_bill_account')
        logger('Log E ' + error)
        return render_template('error.html')


@app.route('/bill')
@app.route('/bill.html', methods=['get', 'post'])
def bill():
    try:
        if not session.check_session('email'):
            return redirect(url_for('sign_in'))

        if request.method == 'POST':
            bills = request.form
            add_bill(bills)

        email_address = session.get_session('email')
        user = query.select_email(email_address)

        # regular user
        if user.user_type == 3:
            account_id = query.select_user_info(user.user_id).account_id
            bill_names = format_bill_config(account_id)

            logger(f'Log: Bill Configuration for Bill Account_ID: {account_id} with User Credentials retrieved.')
            return render_template(url_for('bill'), config=bill_names, edit=False)

        # this would be expected to change when a manager has more than one account
        # manager
        if user.user_type == 1:
            user_id = user.user_id
            manager_id = query.select_manager_uid(user_id).manager_id
            account_id = query.select_bill_account(manager_id).account_id
            bill_names = format_bill_config(account_id)

            logger(f'Log: Bill Configuration for Bill Account_ID: {account_id} with Manager Credentials retrieved.')
            return render_template(url_for('bill'), config=bill_names, edit=True)

        return render_template(url_for('bill'))

    except:
        error = str(sys.exc_info())
        logger('Log E Error in bill')
        logger('Log E ' + error)
        return render_template('error.html')


def format_bill_config(account_id):
    config = query.select_bill_config(account_id)
    bill_names = [config.bill_1, config.bill_2, config.bill_3, config.bill_4, config.bill_5]
    while '' in bill_names:
        bill_names.remove('')

    return bill_names


def add_bill(bills):
    bills = bills.to_dict()

    # validate that these bills are valid
    if validate.validate_bills(bills):
        pass
        # do persist, return true

    else:
        pass
        # do not persist, return false


def sign_out():
    logger('Log: User ' + session.get_session('email') + ' is signing out.')
    session.clear_session('email')


def logger(message):
    print(message)


if __name__ == '__main__':
    app.run(debug=True, port=9999)
