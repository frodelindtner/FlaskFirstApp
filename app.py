from flask import Flask, render_template, request, redirect, url_for
from services.customer_service import CustomerService
from services.order_service import OrderService
from services.product_service import ProductService
from services.stadings_da_service import StandingsServiceLocal
from services.stadings_us_service import StandingsServiceUS

app = Flask(__name__)

customer_service = CustomerService()
order_service = OrderService()
product_service = ProductService()
standing_service_local = StandingsServiceLocal()
standing_service_us = StandingsServiceUS()

standing_service_local.create_some_objects()


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

# dansk liga
@app.route('/teams')
def teams():
    return render_template('teams/teams.html', title = 'Dansk liga', 
                           description = 'Lokal liga - data kommer fra database', 
                           standing_list = standing_service_local.get_all_teams())

# USA liga
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
                           description = 'USA liga - data kommer fra API', 
                           standings_dto = standing_service_us.get_standings_dto_filter_by_league(filter_league),
                           filter_league = filter_league,
                           filter_division = filter_division_querystring)





    

if __name__=='__main__':
    app.run(debug = True)
