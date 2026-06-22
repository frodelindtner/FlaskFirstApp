from flask import Flask, render_template, request, redirect, url_for
from services.stadings_service import StandingsService
from services.team_service import TeamService
from services.result_service import ResultService

app = Flask(__name__)

team_service = TeamService()
result_service = ResultService()
standing_service = StandingsService()

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
    return render_template('teams/teams.html', title = 'Dansk liga', 
                           standing_list = team_service.get_all_teams())

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
    return render_template('results/results.html', title = 'Dansk liga resultater', 
                           result_list = result_service.get_all_results())

@app.route('/standings-local')
def standingslocal():
    return render_template('standings/standingslocal.html', title = 'Dansk liga', 
                           standings_dto = standing_service.get_stadings_local(team_service, result_service))

#------------------------------------------------------------------------------------------------------------------------------
# External league by API
#------------------------------------------------------------------------------------------------------------------------------
@app.route('/standings')
def standings():
    return render_template('standings/standings.html', title = 'USA liga', 
                           standings_dto = standing_service.get_stadings_us())

# USA liga
@app.route('/standings/<filter_league>')
def standings_with_filter(filter_league):
    filter_division_querystring = request.args.get('filter-division')

    return render_template('standings/standings.html', title = 'USA liga med filter', 
                           standings_dto = standing_service.get_standings_us_filter_by_league(filter_league),
                           filter_league = filter_league,
                           filter_division = filter_division_querystring)

if __name__=='__main__':
    app.run(debug = True)