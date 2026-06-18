from flask import Flask, render_template, request, redirect, url_for
from services.album_service import Service
from services.stat_service import Stat_Service
from services.customer_service import CustomerService
from services.order_service import OrderService
from services.product_service import ProductService

app = Flask(__name__)
album_service = Service()
album_service.create_some_objects()

stat_service = Stat_Service()
stat_service.create_some_objects()

customer_service = CustomerService()
# has customer data in data
order_service = OrderService()
product_service = ProductService()

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title = 'Velkommen!', name = 'Jens Jakob Jensen')

@app.route('/about')
def about():
    return render_template('about.html', title = 'Om site')

# --------CUSTOMER-----------------------------------------------------------------

@app.route('/customers')
def customers():
    customers = customer_service.get_all_customers()
    return render_template('/customers/customers.html', cus_list = customers)

@app.route('/customers/create', methods=['GET', 'POST'])
def create_customer():
    if request.method == 'POST':
        customer_service.create_customers(request.form['name'], request.form['mail'], int(request.form['phone']))
        return redirect(url_for('customers'))
    else:
        return render_template('/customers/create-customer.html')

@app.route('/customers/<int:id>')
def customer_details(id):
    customer = customer_service.get_customer_by_id(id)
    if customer is not None:
        return render_template('/customers/customer-details.html', customer = customer)
    else:
        return '<h1>NOT FOUND in Customer table</h1>'

# ------------------------------------------------------ JSON ----------------------------
@app.route('/api/customers/<int:id>')
def get_customer_by_id_json(id):
    customer = customer_service.get_customer_by_id(id)
    return customer.to_json()

@app.route('/api/customers')
def get_all_customes_json():
    customers = customer_service.get_all_customers_json()
    return customers


# --------STATS-----------------------------------------------------------------

@app.route('/stats')
def all_stats():
    return render_template('stats.html', playername='Frode', title = 'List stat!', stats = stat_service.get_all_stats())

@app.route('/stats/<id>')
def stat_by_entry(id):
    stats = stat_service.get_all_stats()

# ---------------------------------------------------------------- ORDERS -------------------------------------------------------------------------------
@app.route('/orders')
def orders():
    orders = order_service.get_orders()
    return render_template('orders/orders.html', orders_list = orders)

@app.route('/orders/<id>')
def order_by_id(id):
    order = order_service.get_order_by_id(int(id))
    if order is not None:
        return render_template('orders/order-details.html', order = order)
    else:
        return '<h1>NO SUCH ORDER IN OUR DB</h1>'
    
@app.route('/orders/create', methods=['GET', 'POST'])
def create_order():
    if request.method == "POST":
        paid = False
        try:
            if request.form['paid']:
                paid = True
        except:
            paid = False
        
        # See the html-page for more info about how the values are created
        order_service.create_order(
            int(request.form['cid']),
            int(request.form['pid']),
            paid,
            int(request.form['quantity']))
        return redirect(url_for("orders")) # function called "orders" in app.py
    else:
        # Since an order includes a customer and a product, we get both lists from our service
        customers = customer_service.get_customers()
        products = product_service.get_products()
        return render_template('orders/create-order.html', customers = customers, products = products)

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
