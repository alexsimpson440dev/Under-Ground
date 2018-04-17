from flask import Flask, render_template, url_for, request, redirect
from src.query_manager import QueryManager
from src.apis.session_api import SessionAPI
from src.new_data_validator import NewDataValidator
import sys

from src.queries.select import Select

select = Select()

sessionAPI = SessionAPI()
query = QueryManager()
validate = NewDataValidator()

app = Flask(__name__, '/static', static_folder='../static', template_folder='../templates')

@app.route('/')
@app.route('/signin')
@app.route('/signin.html')
def sign_in():
    return render_template(url_for('sign_in'))


@app.route('/signup', methods=['post', 'get'])
@app.route('/signup.html')
def sign_up():
    try:
        if sessionAPI.check_session() is False:
            if request.method == 'POST':
                new_user = request.form
                if validate.validate_user(new_user) and validate.validate_user_info(new_user) is True:
                    print("Valid")
                    return render_template(url_for('sign_in'))
                else:
                    print("Not Valid")
                    return render_template(url_for('sign_up'))

            else:
                return render_template(url_for('sign_up'))

        else:
            return redirect(url_for('sign_up')) # sign out the current user, return to sign up
    except:
        error = sys.exc_info()[0]
        print(error)
        return redirect(url_for('sign_up'))


if __name__ == '__main__':
    app.run(debug=True)
