from flask import Flask, render_template, request, redirect, url_for
from services.album_service import Service
from services.stat_service import Stat_Service

app = Flask(__name__)
album_service = Service()
album_service.create_some_objects()

stat_service = Stat_Service()
stat_service.create_some_objects()

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title = 'Velkommen!', name = 'Jens Jakob Jensen')
    # return '<h1>Velkommen besøgende</h1>'

@app.route('/about')
def about():
    return render_template('about.html', title = 'Om site')

# -------------------------------------------------------------------------

@app.route('/albums')
def all_albums():
    return render_template('albums.html', title = 'Liste over albums', albums = album_service.get_all_album())

# --------STATS-----------------------------------------------------------------

@app.route('/stats')
def all_stats():
    return render_template('stats.html', playername='Frode', title = 'List stat!', stats = stat_service.get_all_stats())


if __name__=='__main__':
    app.run(debug = True)