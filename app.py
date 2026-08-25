from flask import Flask, render_template, request, redirect, url_for
from services.stadings_service import StandingsService
from services.team_service import TeamService
from services.result_service import ResultService
from services.player_service import PlayerService
from services.tournament_service import TournamentService

app = Flask(__name__)

team_service = TeamService()
result_service = ResultService()
standing_service = StandingsService()
player_service = PlayerService()
tournament_service = TournamentService()

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title = 'Velkommen')

@app.route('/about')
def about():
    return render_template('about.html', title = 'Om site')

@app.route('/get-started')
def getstarted():
    return render_template('get-started.html', title = 'Fremgangsmåde')

#------------------------------------------------------------------------------------------------------------------------------
# local league admin
#------------------------------------------------------------------------------------------------------------------------------
@app.route('/createteamsauto')
def create_teams_auto():
    team_service.create_some_objects(result_service)
    return redirect(url_for("teams"))

@app.route('/teams')
def teams():
    return render_template('teams/teams.html', title = 'Lokal liga', 
                           teams = team_service.get_all_teams())

@app.route('/teams/create', methods=['GET', 'POST'])
def create_team():
    if request.method == "POST":
        team_service.create_team(request.form['season'], request.form['city'], request.form['name'], 
                                 request.form['league'], request.form['division'], result_service)
        return redirect(url_for("teams")) 
    else:
        return render_template('teams/create-team.html', title = 'Opret hold')

@app.route('/teams/<int:id>/edit', methods=['GET', 'POST'])
def edit_team(id):
    if request.method == "POST":
        teamId = id
        team_service.update_team(teamId, request.form['season'], request.form['city'], request.form['name'],
                                 request.form['league'], request.form['division'])
        return redirect(url_for("teams"))
    else:
        return render_template('teams/edit-team.html', title = 'Rediger hold',
                           team = team_service.get_team_by_id(id))

@app.route('/teams/<int:id>/delete')
def delete_team(id):
    team_service.delete_team(id)
    result_service.delete_result_by_teamid(id)
    return redirect(url_for("teams"))

@app.route('/players')
def players():
    return render_template('players/players.html', title = 'Spillere',
                           players = player_service.get_all_players())

@app.route('/players/create', methods=['GET', 'POST'])
def create_player():
    if request.method == "POST":
        player_service.create_player(
            int(request.form['teamid']),
            request.form['first_name'],
            request.form['last_name'],
            request.form['position'],
            int(request.form['jersey_number'])
        )
        return redirect(url_for("players"))
    else:
        return render_template('players/create-player.html', title = 'Opret spiller',
                               teams = team_service.get_all_teams())

@app.route('/players/<int:id>/edit', methods=['GET', 'POST'])
def edit_player(id):
    if request.method == "POST":
        player_service.update_player(
            id,
            int(request.form['teamid']),
            request.form['first_name'],
            request.form['last_name'],
            request.form['position'],
            int(request.form['jersey_number'])
        )
        return redirect(url_for("players"))
    else:
        return render_template('players/edit-player.html', title = 'Rediger spiller',
                               player = player_service.get_player_by_id(id),
                               teams = team_service.get_all_teams())

@app.route('/players/<int:id>/delete')
def delete_player(id):
    player_service.delete_player(id)
    return redirect(url_for("players"))

@app.route('/team/<int:id>/add-win')
@app.route('/team/<int:id>/add-win/<selected_filter>')
def add_win_team(id, selected_filter = None):
    """ 
    Adds a win to the team with the given id 
    """
    result_service.add_win_team(id)
    if selected_filter != None:
        return redirect(url_for("standingslocal") + "/" + selected_filter)
    else:
        return redirect(url_for("standingslocal"))
#------------------------------------------------------------------------------------------------------------------------------
# Results local league
#------------------------------------------------------------------------------------------------------------------------------
@app.route('/results/<int:teamid>/edit', methods=['GET','POST'])
def edit_result(teamid):
    if request.method == "POST":
        resultid = int(request.form['id']) # result id
        result_service.update_result(resultid, teamid, request.form['wins'], request.form['losses'])
        return redirect(url_for("standingslocal"))
    else:
        return render_template('results/edit-result.html', title = 'Holdets resultater',
                               result = result_service.get_result_by_teamid(teamid))
    
@app.route('/results')
def results():
    """
    Showing results from local league
    """
    return render_template('results/results.html', title = 'Dansk liga resultater', 
                           results = result_service.get_all_results())

@app.route('/standings-local')
@app.route('/standings-local/<league>')
def standingslocal(league = None):
    """
    Showing local league standings with optional filter
    """
    if league == None:
        return render_template('standings/standingslocal.html', title = 'Dansk liga', 
                               standings = standing_service.get_stadings_local(team_service, result_service),
                               filter_options = team_service.create_filters())
    else:
        return render_template('standings/standingslocal.html', title = 'Dansk liga med filter', 
                               standings = standing_service.get_stadings_local_filter_by_league(team_service, result_service, league),
                               filter_options = team_service.create_filters(),
                               selected_league = league)
    
#------------------------------------------------------------------------------------------------------------------------------
# External league by API - USA MLB
#------------------------------------------------------------------------------------------------------------------------------

@app.route('/standings')
@app.route('/standings/') # https://stackoverflow.com/questions/40365390/trailing-slash-in-flask-route
@app.route('/standings/<filter_league>')
@app.route('/standings/<filter_league>/<filter_division>')
def standings_with_filter(filter_league = None, filter_division = None):
    """
    Showing standings from USA API with optional filter
    """
    if filter_league == None:
        return render_template('standings/standings.html', title = 'USA liga', 
                               standings = standing_service.get_stadings_us())
    else:
        return render_template('standings/standings.html', title = 'USA liga med filter', 
                               standings = standing_service.get_standings_us_filter_by_league(filter_league),
                               filter_league = filter_league,
                               filter_division = filter_division)    

#------------------------------------------------------------------------------------------------------------------------------
# Exposing local leage by endpoint
#------------------------------------------------------------------------------------------------------------------------------

@app.route('/api/standings', methods = ['GET'])
def get_all_local_standings():
    """
    Exposing local league standings as JSON
    """
    customers = standing_service.get_all_local_standings_json(team_service, result_service)
    return customers

#------------------------------------------------------------------------------------------------------------------------------
# Tournament management
#------------------------------------------------------------------------------------------------------------------------------

@app.route('/tournaments')
def tournaments():
    tournament_teams_count = {}
    for tournament in tournament_service.get_all_tournaments():
        tournament_teams_count[tournament.id] = len(tournament_service.get_tournament_teams(tournament.id))
    return render_template('tournaments/tournaments.html', title='Turneringer',
                           tournaments=tournament_service.get_all_tournaments(),
                           tournament_teams_count=tournament_teams_count)

@app.route('/tournaments/create', methods=['GET', 'POST'])
def create_tournament():
    if request.method == 'POST':
        tournament_service.create_tournament(
            request.form['name'],
            int(request.form['season']),
            request.form['format']
        )
        return redirect(url_for('tournaments'))
    return render_template('tournaments/create-tournament.html', title='Opret turnering')

@app.route('/tournaments/<int:id>/edit', methods=['GET', 'POST'])
def edit_tournament(id):
    tournament = tournament_service.get_tournament_by_id(id)
    if tournament is None:
        return redirect(url_for('tournaments'))

    if request.method == 'POST':
        tournament_service.update_tournament(
            id,
            request.form['name'],
            int(request.form['season']),
            request.form['format']
        )
        return redirect(url_for('edit_tournament', id=id))

    team_lookup = {team.id: team.name for team in team_service.get_all_teams()}
    tournament_teams = []
    for tournament_team in tournament_service.get_tournament_teams(id):
        team = team_service.get_team_by_id(tournament_team.team_id)
        if team is not None:
            tournament_teams.append(team)

    matches = tournament_service.get_tournament_matches(id)
    return render_template('tournaments/edit-tournament.html', title='Rediger turnering',
                           tournament=tournament,
                           all_teams=team_service.get_all_teams(),
                           tournament_teams=tournament_teams,
                           matches=matches,
                           team_lookup=team_lookup)

@app.route('/tournaments/<int:id>/add-team', methods=['POST'])
def add_team_to_tournament(id):
    tournament_service.add_team_to_tournament(id, int(request.form['teamid']))
    return redirect(url_for('edit_tournament', id=id))

@app.route('/tournaments/<int:id>/remove-team/<int:teamid>')
def remove_team_from_tournament(id, teamid):
    tournament_service.remove_team_from_tournament(id, teamid)
    return redirect(url_for('edit_tournament', id=id))

@app.route('/tournaments/<int:id>/generate-schedule')
def generate_tournament_schedule(id):
    tournament_service.generate_schedule(id)
    return redirect(url_for('edit_tournament', id=id))

@app.route('/tournaments/<int:tournament_id>/matches/<int:match_id>/score', methods=['POST'])
def update_tournament_match_score(tournament_id, match_id):
    home_score = int(request.form.get('home_score', 0))
    away_score = int(request.form.get('away_score', 0))
    tournament_service.update_match_score(match_id, home_score, away_score)
    return redirect(url_for('edit_tournament', id=tournament_id))

if __name__=='__main__':
    app.run(debug = True)