from flask import Flask, render_template
from config import Config
from models import db
from flask_login import LoginManager
from routes.auth_routes import auth_bp, login_manager
from routes.room_routes import room_bp
from routes.booking_routes import booking_bp
from routes.customer_routes import customer_bp
from routes.customer_room_route import customer1_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)  # Initialize database

# Only initialize login_manager if not already initialized in auth_routes.py
if not hasattr(login_manager, "_app"):
    login_manager.init_app(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(room_bp, url_prefix="/room")
app.register_blueprint(booking_bp, url_prefix="/bookings")
app.register_blueprint(customer_bp, url_prefix="/customer")
app.register_blueprint(customer1_bp, url_prefix="/customer1")  # Change this to "/" if needed

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/management_dashboard")
def management_dashboard():
    return render_template("management_dashboard.html")

@app.route("/customer_dashboard")
def customer_dashboard():
    return render_template("customer_dashboard.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
