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

# --------STATS-----------------------------------------------------------------

@app.route('/stats')
def all_stats():
    return render_template('stats.html', playername='Frode', title = 'List stat!', stats = stat_service.get_all_stats())

@app.route('/stats/<id>')
def stat_by_entry(id):
    stats = stat_service.get_all_stats()

# ------------------------------------------------------------------------------------------------
@app.route('/albums')
def all_albums():
    return render_template('albums.html', title = 'Alle albums', albums = album_service.get_all_albums())

@app.route('/albums/<id>')
def album_by_entry(id):
    album = album_service.find_album_by_id(int(id))
    if album is not None:
        return render_template('album-details.html', album = album)
    return '<h1>Intet album kunne findes</h1>'

@app.route('/albums/create', methods=['GET', 'POST'])
def create_album():
    return render_template('create-album.html', title='nyt album')
    
@app.route('/albums/<id>/edit', methods=['GET', 'POST'])
def edit_album(id):
    album = album_service.find_album_by_id(int(id))
    if album is not None:
        if request.method == "POST":
            album.title = request.form['title']
            album.artist = request.form['artist']
            album.release_year = request.form['release_year']
            updated_album = album_service.update_album(album)
            return redirect(url_for("album_by_entry", id = updated_album.id))
        else:
            return render_template('edit-album.html', album = album)
    else:
        return '<h1>Findes ikke!</h1>'
    
@app.route('/albums/<id>/delete', methods=['GET', 'POST'])
def delete_album(id):
    album = album_service.find_album_by_id(int(id))
    if album is not None:
        if request.method == "POST":
            album_service.delete_album(album.id)
            return redirect(url_for("all_albums"))
        else:
            return render_template('delete-album.html', album = album, title='sletning')
    else:
        return '<h1>Album er allerede slettet</h1>'

if __name__=='__main__':
    app.run(debug = True)
