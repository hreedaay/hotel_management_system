from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Enum
import sqlite3

db = SQLAlchemy()

# User Table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="customer")  # New column

    bookings = db.relationship("Booking", backref="user", lazy=True)

    def is_management(self):
        return self.role == "management"

# Room Table
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Added missing column
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=True)  # This replaces availability

    def mark_as_booked(self):
        self.status = "Booked"  # Use a string instead of a boolean

    def mark_as_available(self):
        self.status = "Available"  # Use a string instead of a boolean


# Booking Table
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    status = db.Column(Enum("Pending", "Confirmed", "Cancelled", name="booking_status"),
                       default="Pending", nullable=False, server_default="Pending")

# Function to initialize the database
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


def get_available_rooms(date):
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, number, type, price FROM rooms
        WHERE id NOT IN (SELECT room_id FROM bookings WHERE date = ?)
    """, (date,))

    rooms = [{"id": row[0], "number": row[1], "type": row[2], "price": row[3]} for row in cursor.fetchall()]
    conn.close()

    return rooms