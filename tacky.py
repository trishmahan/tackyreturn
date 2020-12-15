from flask import Flask, render_template, request

app = Flask(__name__)
@app.route('/')
def tacky_form():
    return render_template('form.html')

@app.route('/home',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("home.html",result = result)

if __name__ == '__main__':
   app.run(debug = True)