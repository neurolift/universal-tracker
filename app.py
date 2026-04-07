from flask import Flask, render_template, request

app = Flask(__name__)


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
    return render_template("index.html")


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

    return render_auth_page(
        active_tab="signin",
        message=f"Signed in as {email}.",
        message_type="success",
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

    return render_auth_page(
        active_tab="signin",
        message=f"Account created for {full_name}. You can sign in now.",
        message_type="success",
    )

if __name__ == "__main__":
    app.run(debug=True)