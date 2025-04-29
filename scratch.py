import traceback
from functools import wraps
from flask import Flask,redirect,url_for,render_template,request,flash
import config

app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home():
    
    return render_template('index.html')

@app.route('/about', methods=['GET','POST'])
def about():
    
    return render_template('about.html')

@app.route("/examples", methods=['GET','POST'])
def examples():

    return render_template('examples.html')

@app.route('/run-code', methods=['GET', 'POST'])
def run_code():
    result = None
    error = None
    if request.method == 'POST':
        user_code = request.form.get('code')
        try:
            # Execute the code entered by the user
            exec_globals = {}
            exec(user_code, exec_globals)
            result = exec_globals.get('result', 'No result returned.')
        except Exception as e:
            error = traceback.format_exc()  # Capture detailed error info
    return render_template('run_code.html', result=result, error=error)

app.secret_key = 'your_secret_key'  # Needed for flash messages

users = {}  # Simple dictionary to store users temporarily

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if username in users:
            flash('Username already exists. Please choose another.', 'danger')
        else:
            users[username] = {'email': email, 'password': password}
            flash('Account created successfully! You can now sign in.', 'success')
            return redirect('/signin')
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.get(username)

        if user and user['password'] == password:
            session['user'] = username
            flash(f'Welcome back, {username}!', 'success')
            return redirect('/')
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    return render_template('signin.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out successfully.', 'info')
    return redirect('/')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please sign in to access this page.', 'warning')
            return redirect(url_for('signin'))  # Change to your actual sign-in route function name
        return f(*args, **kwargs)
    return decorated_function


if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=config.PORT,debug=config.DEBUG, host=config.HOST)