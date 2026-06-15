from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title = 'Velkommen!', name = 'Jens Jakob Jensen')
    # return '<h1>Velkommen besøgende</h1>'

@app.route('/about')
def about():
    return render_template('about.html', title = 'Om site')


if __name__=='__main__':
    app.run(debug = True)