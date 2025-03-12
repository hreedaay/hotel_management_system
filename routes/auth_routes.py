from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint("auth", __name__)
login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Delete Account Route
@auth_bp.route("/delete_account", methods=["POST"])
@login_required
def delete_account():
    user = User.query.get(current_user.id)

    if user:
        db.session.delete(user)
        db.session.commit()
        flash("Your account has been deleted successfully.", "success")
        logout_user()

    return redirect(url_for("auth.login"))  # Redirect to signup or login page

# Signup Route
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role", "customer")  # Default role is "customer"

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please log in.", "danger")
            return redirect(url_for("auth.signup"))

        # Hash password before saving
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        new_user = User(username=username, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash("Signup successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("index.html")


@auth_bp.route('/login', methods=['GET', 'POST'])  # Fixed route
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!", "success")

            if user.role == "management":
                return redirect(url_for("management_dashboard"))
            else:
                return redirect(url_for("customer_dashboard"))

        flash("Invalid credentials", "danger")

    return render_template("index.html")  # Ensure you have a login.html template


# Logout Route
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
