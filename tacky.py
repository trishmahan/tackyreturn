from flask import Flask, render_template, request

app = Flask(__name__)
@app.route('/')
def tacky_form():
    return render_template('form.html')

@app.route('/home',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        if result['trait'] == "brave":
            return render_template("gryf.html",result = result)
        elif result['trait'] == "loyal":#loyal wise cunning
            return render_template("huff.html",result = result)
        elif result['trait'] == "wise":#loyal wise cunning
            return render_template("rav.html",result = result)
        elif result['trait'] == "cunning":#loyal wise cunning
            return render_template("slyth.html",result = result)
        else:
            return render_template("home.html",result = result)

# @app.route('/hoggy-hoggy-hogwartz',methods = ['POST', 'GET'])
# def result():
#    if request.method == 'POST':
#       result = request.form
#       return render_template("home.html",result = result)

if __name__ == '__main__':
    app.run(debug = True)