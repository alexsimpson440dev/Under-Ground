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
    return render_template('signin.html')

@app.route('/signup', methods=['post', 'get'])
@app.route('/signup.html')
def sign_up():
    #try:
        if sessionAPI.check_session() is False:
            if request.method == 'POST':
                select.select_email("email")
                new_user = request.form
                validate.validate_user(new_user)


                return render_template(url_for('sign_in')) # <-------------use something else, not right ------------->

            else:
                return render_template(url_for('sign_up'))

        else:
            return redirect(url_for('sign_up'))
    #except:
        '''print('fail')
        error = sys.exc_info()[0]
        print(error)
        return redirect(url_for('sign_up'))'''


if __name__ == '__main__':
    app.run(debug=True)
