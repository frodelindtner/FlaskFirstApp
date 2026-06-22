from flask import Flask, render_template, request, redirect, url_for
from services.stadings_us_service import StandingsServiceUS
from services.team_service import TeamService

app = Flask(__name__)

team_service = TeamService()
standing_service_us = StandingsServiceUS()

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
    team_service.create_some_objects()
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
                                 request.form['league'], request.form['division'])
        return redirect(url_for("teams")) 
    else:
        return render_template('teams/create-team.html', title = 'Opret hold', 
                               description = 'Her kan du oprette et hold')

@app.route('/teams/<int:id>/edit', methods=['GET', 'POST'])
def edit_team(id):
    if request.method == "POST":
        teamId = int(request.form['id'])
        print(teamId)
        team_service.update_team(teamId, request.form['season'], request.form['city'], request.form['name'],
                                 request.form['league'], request.form['division'])
        return redirect(url_for("teams"))
    else:
        return render_template('teams/edit-team.html', title = 'Rediger hold',
                           description = 'Her kan du redigere dit hold',
                           team = team_service.get_team_by_id(id))


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
