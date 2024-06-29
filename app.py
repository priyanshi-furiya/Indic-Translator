from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('page1.html')


@app.route('/page2.html')
def translator():
    return render_template('page2.html')


@app.route('/page3.html')
def record():
    return render_template('page3.html')

@app.route('/page4.html')
def scan():
    return render_template('page4.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080, host="0.0.0.0")
