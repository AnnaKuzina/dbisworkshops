"""
Тут написати умову до завдання
"""

from flask import Flask, render_template, request, make_response, session, redirect, url_for, flash


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index1.html")



@app.route('/api', methods=['POST'])
def apiPost():
    if request.form["action"] == "sum":
        a = request.form["A"]
        b = request.form["B"]
        response = make_response(redirect(url_for('index')))
        response.set_cookie("result", str(int(a) + int(b)))
        return response




if __name__ == '__main__':
    app.run(debug=True)
