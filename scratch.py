import traceback
from flask import Flask,redirect,url_for,render_template,request
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


if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=config.PORT,debug=config.DEBUG, host=config.HOST)