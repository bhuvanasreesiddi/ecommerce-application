import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "eco_secret"

# ---------------- ECO SCORE LOGIC ---------------- #
def calculate_eco_score(material):
    material_scores = {
        "Bamboo": 90,
        "Recycled Plastic": 80,
        "Organic Cotton": 85,
        "Steel": 70,
        "Glass": 75,
        "Plastic": 40
    }
    score = material_scores.get(material, 50)
    return score

def get_eco_grade(score):
    if score >= 85:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 60:
        return "C"
    return "D"
# ---------------- PRODUCTS ---------------- #
products = [
    {"id": 1, "name": "Bamboo Toothbrush", "price": 120, "material": "Bamboo"},
    {"id": 2, "name": "Reusable Steel Bottle", "price": 350, "material": "Steel"},
    {"id": 3, "name": "Organic Cotton T-Shirt", "price": 699, "material": "Organic Cotton"},
    {"id": 4, "name": "Glass Storage Jar", "price": 250, "material": "Glass"},
    {"id": 5, "name": "Recycled Plastic Notebook", "price": 180, "material": "Recycled Plastic"},
    {"id": 6, "name": "Eco Shopping Bag", "price": 150, "material": "Organic Cotton"},
    {"id": 7, "name": "Bamboo Cutlery Set", "price": 220, "material": "Bamboo"},
    {"id": 8, "name": "Steel Lunch Box", "price": 400, "material": "Steel"},
    {"id": 9, "name": "Glass Water Bottle", "price": 300, "material": "Glass"},
    {"id": 10, "name": "Recycled Plastic Chair", "price": 1200, "material": "Recycled Plastic"},
    {"id": 11, "name": "Organic Cotton Bedsheet", "price": 1499, "material": "Organic Cotton"},
    {"id": 12, "name": "Bamboo Hair Brush", "price": 199, "material": "Bamboo"},
    {"id": 13, "name": "Steel Coffee Mug", "price": 280, "material": "Steel"},
    {"id": 14, "name": "Glass Tea Cup Set", "price": 450, "material": "Glass"},
    {"id": 15, "name": "Eco Yoga Mat", "price": 999, "material": "Organic Cotton"},
    {"id": 16, "name": "Bamboo Straw Set", "price": 99, "material": "Bamboo"},
    {"id": 17, "name": "Reusable Grocery Bags", "price": 220, "material": "Organic Cotton"},
    {"id": 18, "name": "Steel Food Container", "price": 500, "material": "Steel"},
    {"id": 19, "name": "Glass Spice Jar Set", "price": 650, "material": "Glass"},
    {"id": 20, "name": "Recycled Plastic Pen Pack", "price": 140, "material": "Recycled Plastic"},
    {"id": 21, "name": "Organic Cotton Hoodie", "price": 1299, "material": "Organic Cotton"},
    {"id": 22, "name": "Bamboo Bath Towel", "price": 799, "material": "Bamboo"},
    {"id": 23, "name": "Steel Water Jug", "price": 750, "material": "Steel"},
    {"id": 24, "name": "Glass Lunch Box", "price": 600, "material": "Glass"},
    {"id": 25, "name": "Recycled Plastic Storage Box", "price": 850, "material": "Recycled Plastic"},
    {"id": 26, "name": "Organic Cotton Socks", "price": 299, "material": "Organic Cotton"},
    {"id": 27, "name": "Bamboo Laptop Stand", "price": 1100, "material": "Bamboo"},
    {"id": 28, "name": "Steel Cutlery Set", "price": 950, "material": "Steel"},
    {"id": 29, "name": "Glass Serving Bowl", "price": 550, "material": "Glass"},
    {"id": 30, "name": "Recycled Plastic Dustbin", "price": 400, "material": "Recycled Plastic"},
]
for product in products:
    score = calculate_eco_score(product["material"])
    product["eco_score"] = score
    product["eco_grade"] = get_eco_grade(score)
    product["image"] = f"images/product{product['id']}.jpg"

materials = ["Bamboo", "Recycled Plastic", "Organic Cotton", "Steel", "Glass", "Plastic"]

# Ensure product images exist
if not os.path.exists(os.path.join("static", "images", "product1.jpg")):
    try:
        from generate_images import generate_product_image
        os.makedirs(os.path.join("static", "images"), exist_ok=True)
        for p in products:
            img_path = os.path.join("static", "images", f"product{p['id']}.jpg")
            if not os.path.exists(img_path):
                generate_product_image(p, img_path)
    except Exception as e:
        print(f"Warning generating images: {e}")

# ---------------- START ROUTE ---------------- #

@app.route("/")
def start():
    if "user" in session:
        return redirect("/home")
    return redirect("/login")

# ---------------- LOGIN ---------------- #

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form["email"]
        return redirect("/home")
    return render_template("login.html",active_page="login")


# ---------------- REGISTER ---------------- #

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        session["user"] = request.form["email"]  # Auto login after register
        return redirect("/home")
    return render_template("register.html",active_page="register")


# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------------- HOME / PRODUCTS ---------------- #

@app.route("/home")
def home():
    if "user" not in session:
        return redirect("/login")

    query = request.args.get("search", "").strip()
    if query:
        filtered = [
            p for p in products
            if query.lower() in p["name"].lower() or query.lower() in p["material"].lower()
        ]
        return render_template("index.html", products=filtered, query=query, active_page="home")

    return render_template("index.html", products=products, active_page="home")


# ---------------- ADD TO CART ---------------- #

@app.route("/add/<int:id>")
def add_to_cart(id):
    if "user" not in session:
        return redirect("/login")

    if "cart" not in session:
        session["cart"] = {}

    cart = session["cart"]
    cart[str(id)] = cart.get(str(id), 0) + 1

    session.modified = True
    return redirect("/home")


# ---------------- VIEW CART ---------------- #

@app.route("/cart")
def cart():
    if "user" not in session:
        return redirect("/login")

    cart_items = []
    total = 0
    cart = session.get("cart", {})

    for id_str, qty in cart.items():
        id = int(id_str)
        product = next((p for p in products if p["id"] == id), None)

        if product:
            item_total = product["price"] * qty
            total += item_total

            cart_items.append({
                "id": id,
                "name": product["name"],
                "price": product["price"],
                "quantity": qty,
                "item_total": item_total
            })

    return render_template("cart.html", cart=cart_items, total=total,active_page="cart")


# ---------------- INCREASE QUANTITY ---------------- #

@app.route("/increase/<int:id>")
def increase(id):
    if "cart" in session and str(id) in session["cart"]:
        session["cart"][str(id)] += 1
        session.modified = True
    return redirect("/cart")


# ---------------- DECREASE QUANTITY ---------------- #

@app.route("/decrease/<int:id>")
def decrease(id):
    if "cart" in session and str(id) in session["cart"]:
        if session["cart"][str(id)] > 1:
            session["cart"][str(id)] -= 1
        else:
            session["cart"].pop(str(id))
        session.modified = True
    return redirect("/cart")


# ---------------- PAYMENT ---------------- #

@app.route("/payment", methods=["GET", "POST"])
def payment():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        session["feedback"] = request.form.get("feedback", "")
        session.pop("cart", None)  # Clear cart after payment
        return redirect(url_for("thankyou"))

    return render_template("payment.html", active_page="payment")


# ---------------- THANK YOU ---------------- #

@app.route("/thankyou")
def thankyou():
    if "user" not in session:
        return redirect("/login")

    feedback = session.pop("feedback", None)
    return render_template("thankyou.html", active_page="thankyou", feedback=feedback)


# ---------------- RUN APP ---------------- #

if __name__ == "__main__":
    app.run(debug=True)
