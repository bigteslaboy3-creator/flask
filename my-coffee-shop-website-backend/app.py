from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

PRODUCTS = {
    "Hot Beverages": {
        "name": "Hot Beverages",
        "image": "hot-beverages.png",
        "desc": "Wide range of steaming hot coffee to make your fresh and lights."
    },
    "Cold Beverages": {
        "name": "Cold Beverages",
        "image": "cold-beverages.png",
        "desc": "Creamy and frothy cold coffee to make you cool."
    },
    "Refreshment": {
        "name": "Refreshment",
        "image": "refreshment.png",
        "desc": "Fruits and icy refreshing drink to make feel refresh"
    },
    "Special Combos": {
        "name": "Special Combos",
        "image": "special-combo.png",
        "desc": "Your favorite eating and drinking combinations"
    },
    "Dessert": {
        "name": "Dessert",
        "image": "desserts.png",
        "desc": "Satiate your palate and take you on a culinary treat."
    },
    "Burger & French Fries": {
        "name": "Burger & French Fries",
        "image": "burger-frenchfries.png",
        "desc": "Quick bites to satisfy your small size hunger."
    },
    "French Fries": {
        "name": "French Fries",
        "image": "fries-1.png",
        "desc": "Crispy and golden fries to complement your meal."
    },
    "Spaghetti & Chicken Leg": {
        "name": "Spaghetti & Chicken Leg",
        "image": "spageti-and-chicken-leg.png",
        "desc": "Delicious spaghetti paired with a juicy chicken leg."
    }
}

@app.route('/')
def index():
    return render_template('index.html', cart=session.get('cart', []))

@app.route('/add_to_cart/<item>', methods=['POST'])
def add_to_cart(item):
    cart = session.get('cart', [])
    cart = [c for c in cart if isinstance(c, dict)]
    for cart_item in cart:
        if cart_item.get('name') == item:
            cart_item['qty'] += 1
            break
    else:
        product = PRODUCTS.get(item)
        if product:
            cart.append({
                "name": product["name"],
                "image": product["image"],
                "desc": product["desc"],
                "qty": 1
            })
    session['cart'] = cart
    session.modified = True
    return jsonify({"success": True})

@app.route('/remove_from_cart/<item>', methods=['POST'])
def remove_from_cart(item):
    cart = session.get('cart', [])
    cart = [cart_item for cart_item in cart if cart_item.get('name') != item]
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('index'))

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('index'))

@app.route('/update_cart/<item>/<action>', methods=['POST'])
def update_cart(item, action):
    cart = session.get('cart', [])
    for cart_item in cart:
        if isinstance(cart_item, dict) and cart_item.get('name') == item:
            if action == 'increase':
                cart_item['qty'] += 1
            elif action == 'decrease' and cart_item['qty'] > 1:
                cart_item['qty'] -= 1
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)