from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'secret_key'

client = MongoClient('mongodb://localhost:27017/')
db = client.food_delivery
menu = db.menu
orders = db.orders

@app.route('/')
def home():
    items = list(menu.find())
    return render_template('index.html', items=items)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item = {
        "name": request.form['name'],
        "price": float(request.form['price']),
        "qty": int(request.form['qty'])
    }
    session.setdefault('cart', []).append(item)
    session.modified = True
    return redirect('/')

@app.route('/cart')
def cart():
    return render_template('cart.html', cart=session.get('cart', []))

@app.route('/place_order')
def place_order():
    cart = session.get('cart', [])
    if cart:
        orders.insert_one({"items": cart})
        session['cart'] = []
        return render_template('order.html', status="Order Placed!")
    return render_template('order.html', status="Cart Empty!")

if __name__ == '__main__':
    app.run(debug=True)
