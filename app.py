from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load products
with open('data/products.json') as f:
    products = json.load(f)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/browse')
def browse():
    return render_template('browse.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((item for item in products if item["id"] == product_id), None)
    if product:
        if 'cart' not in session:
            session['cart'] = []
        session['cart'].append(product)
        session.modified = True
    return redirect(url_for('browse'))

@app.route('/cart')
def cart():
    return render_template('cart.html', cart=session.get('cart', []))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Mock payment processing
        session['order'] = session.get('cart', [])
        session.pop('cart', None)
        return redirect(url_for('order_confirmation'))
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html', order=session.get('order', []))

@app.route('/order_tracking')
def order_tracking():
    return render_template('order_tracking.html')

if __name__ == '__main__':
    app.run(debug=True)
