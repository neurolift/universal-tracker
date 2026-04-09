from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from src.models import User, Stock, Metal, Portfolio, db
from src import fetchers, database
import os
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')  # Change this in production

# Initialize database
db.create_tables([User], safe=True)
database.create_table()


def build_default_portfolio():
    portfolio = Portfolio()
    portfolio.get_portfolio_data()
    return portfolio


def refresh_and_store_portfolio():
    portfolio = build_default_portfolio()
    fetchers.update_all_assets(portfolio.assets)

    for asset in portfolio.assets:
        database.save_asset(asset)

    return database.load_assets()


def render_auth_page(active_tab="signin", message=None, message_type="success", form_data=None):
    return render_template(
        "login.html",
        active_tab=active_tab,
        message=message,
        message_type=message_type,
        form_data=form_data or {},
    )

@app.route("/", methods=["GET"])
def index():
    assets = []
    total_value = 0.0
    asset_prices = {}

    if 'user_id' in session:
        assets = database.load_assets()
        if not assets:
            assets = refresh_and_store_portfolio()
        total_value = sum(item["price"] for item in assets)
        asset_prices = {item["symbol"]: item["price"] for item in assets}

    return render_template(
        "index.html",
        user_name=session.get('user_name', 'Investor'),
        user_email=session.get('user_email', ''),
        assets=assets,
        total_value=total_value,
        asset_prices=asset_prices,
    )


@app.route("/refresh", methods=["POST"])
def refresh_prices():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    refresh_and_store_portfolio()
    return redirect(url_for('index'))


@app.route("/api/prices", methods=["GET"])
def get_prices_api():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    previous_assets = {item["symbol"]: item["price"] for item in database.load_assets()}
    assets = refresh_and_store_portfolio()

    response_assets = []
    for item in assets:
        prev_price = previous_assets.get(item["symbol"], item["price"])
        change_pct = 0.0
        if prev_price:
            change_pct = ((item["price"] - prev_price) / prev_price) * 100

        response_assets.append(
            {
                "symbol": item["symbol"],
                "name": item["name"],
                "price": item["price"],
                "change_pct": change_pct,
            }
        )

    return jsonify({"assets": response_assets})


@app.route("/dashboard", methods=["GET"])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    assets = database.load_assets()
    if not assets:
        assets = refresh_and_store_portfolio()

    total_value = sum(item["price"] for item in assets)
    return render_template(
        "dashboard.html",
        assets=assets,
        total_value=total_value,
        asset_count=len(assets),
    )


@app.route("/login", methods=["GET"])
def login():
    active_tab = request.args.get("tab", "signin")
    if active_tab not in {"signin", "signup"}:
        active_tab = "signin"

    return render_template(
        "login.html",
        active_tab=active_tab,
        message=None,
        message_type="success",
        form_data={},
    )


@app.route("/signin", methods=["POST"])
def signin():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        return render_auth_page(
            active_tab="signin",
            message="Please enter both email and password.",
            message_type="error",
            form_data={"signin_email": email},
        )

    # Check if user exists and password is correct
    user = User.get_by_email(email)
    if user and user.check_password(password):
        session['user_id'] = user.id
        session['user_email'] = user.email
        session['user_name'] = user.full_name
        return redirect(url_for('index'))
    
    return render_auth_page(
        active_tab="signin",
        message="Invalid email or password.",
        message_type="error",
        form_data={"signin_email": email},
    )


@app.route("/signup", methods=["POST"])
def signup():
    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")
    accepted_terms = request.form.get("terms") == "on"

    if not full_name or not email:
        return render_auth_page(
            active_tab="signup",
            message="Name and email are required.",
            message_type="error",
            form_data={"signup_name": full_name, "signup_email": email},
        )

    if len(password) < 6:
        return render_auth_page(
            active_tab="signup",
            message="Password must be at least 6 characters long.",
            message_type="error",
            form_data={"signup_name": full_name, "signup_email": email},
        )

    if password != confirm_password:
        return render_auth_page(
            active_tab="signup",
            message="Password and confirm password do not match.",
            message_type="error",
            form_data={"signup_name": full_name, "signup_email": email},
        )

    if not accepted_terms:
        return render_auth_page(
            active_tab="signup",
            message="You must accept the terms to create an account.",
            message_type="error",
            form_data={"signup_name": full_name, "signup_email": email},
        )

    # Check if email already exists
    if User.get_by_email(email):
        return render_auth_page(
            active_tab="signup",
            message="Email already registered. Please sign in instead.",
            message_type="error",
            form_data={"signup_name": full_name, "signup_email": email},
        )

    # Create new user
    try:
        user = User.create(
            id=str(uuid.uuid4()),
            full_name=full_name,
            email=email,
            password_hash=""
        )
        user.set_password(password)
        user.save()
        
        return render_auth_page(
            active_tab="signin",
            message=f"Account created! Please sign in.",
            message_type="success",
            form_data={"signin_email": email},
        )
    except Exception as e:
        return render_auth_page(
            active_tab="signup",
            message=f"Error creating account: {str(e)}",
            message_type="error",
            form_data={"signup_name": full_name, "signup_email": email},
        )


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)