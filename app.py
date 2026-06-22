from flask import Flask, render_template, request, redirect, url_for
from services.stadings_us_service import StandingsServiceUS
from services.stadings_local_service import StandingsServiceLocal
from services.team_service import TeamService
from services.result_service import ResultService

app = Flask(__name__)

team_service = TeamService()
result_service = ResultService()
standing_service_us = StandingsServiceUS()
standing_service_local = StandingsServiceLocal()

# Only for test!
# result_service.create_some_objects()

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title = 'Velkommen', 
                           description = 'Forsiden til webstiet')

@app.route('/about')
def about():
    return render_template('about.html', title = 'Om site', 
                           description = 'Dette site er lavet i forbindelse med deltagelse i Python programmeringskursus' )

@app.route('/get-started')
def getstarted():
    return render_template('get-started.html', title = 'Fremgangsmåde', 
                           description = 'Kom igang med brug af sitet' )

#------------------------------------------------------------------------------------------------------------------------------
# local league
#------------------------------------------------------------------------------------------------------------------------------
@app.route('/createteamsauto')
def create_teams_auto():
    team_service.create_some_objects(result_service)
    return redirect(url_for("teams"))

@app.route('/teams')
def teams():
    return render_template('teams/teams.html', title = 'Dansk liga', 
                           description = 'Lokal liga - data kommer fra database', 
                           standing_list = team_service.get_all_teams())

@app.route('/teams/create', methods=['GET', 'POST'])
def create_team():
    if request.method == "POST":
        team_service.create_team(request.form['season'], request.form['city'], request.form['name'], 
                                 request.form['league'], request.form['division'], result_service)
        return redirect(url_for("teams")) 
    else:
        return render_template('teams/create-team.html', title = 'Opret hold', 
                               description = 'Her kan du oprette et hold')

@app.route('/teams/<int:id>/edit', methods=['GET', 'POST'])
def edit_team(id):
    if request.method == "POST":
        teamId = id
        team_service.update_team(teamId, request.form['season'], request.form['city'], request.form['name'],
                                 request.form['league'], request.form['division'])
        return redirect(url_for("teams"))
    else:
        return render_template('teams/edit-team.html', title = 'Rediger hold',
                           description = 'Her kan du redigere dit hold',
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
                               description = 'Opret holdets sejre og nederlag',
                               result = result_service.get_result_by_teamid(teamid))
    
@app.route('/results')
def results():
    return render_template('results/results.html', title = 'Dansk liga resultater', 
                           description = 'Lokal liga - result - data kommer fra database', 
                           result_list = result_service.get_all_results())

@app.route('/standings-local')
def standingslocal():
    return render_template('standings/standingslocal.html', title = 'Dansk liga', 
                           description = 'Dansk liga - data kommer fra SQLite', 
                           standings_dto = standing_service_local.get_stadings(team_service, result_service))

#------------------------------------------------------------------------------------------------------------------------------
# External league by API
#------------------------------------------------------------------------------------------------------------------------------
@app.route('/standings')
def standings():
    return render_template('standings/standings.html', title = 'USA liga', 
                           description = 'USA liga - data kommer fra API', 
                           standings_dto = standing_service_us.get_stadings_dto())

# USA liga
@app.route('/standings/<filter_league>')
def standings_with_filter(filter_league):
    filter_division_querystring = request.args.get('filter-division')

    return render_template('standings/standings.html', title = 'USA liga', 
                           description = 'USA liga - data kommer fra API men filteret', 
                           standings_dto = standing_service_us.get_standings_dto_filter_by_league(filter_league),
                           filter_league = filter_league,
                           filter_division = filter_division_querystring)

if __name__=='__main__':
    app.run(debug = True)