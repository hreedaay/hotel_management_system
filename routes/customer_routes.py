from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from models import db, Booking, Room

customer_bp = Blueprint("customer", __name__)

# ✅ Route for rendering the "My Bookings" page
@customer_bp.route("/mybookings", methods=["GET"])
@login_required
def my_bookings():
    return render_template("mybookings.html")

# ✅ API route to fetch the logged-in user's bookings
@customer_bp.route("/api/my_bookings", methods=["GET"])
@login_required
def get_my_bookings_api():
    bookings = (
        db.session.query(Booking, Room.number)
        .join(Room, Booking.room_id == Room.id)
        .filter(Booking.user_id == current_user.id)
        .all()
    )

    # Format data for frontend
    user_bookings = [
        {
            "id": booking.Booking.id,
            "room_number": booking.number,
            "date": booking.Booking.date,
            "status": booking.Booking.status,
        }
        for booking in bookings
    ]

    return jsonify(user_bookings)

@customer_bp.route("/api/cancel_booking/<int:booking_id>", methods=["DELETE"])
@login_required
def cancel_booking(booking_id):
    # Fetch the booking for the current user
    booking = Booking.query.filter_by(id=booking_id, user_id=current_user.id).first()

    if not booking:
        return jsonify({"message": "Booking not found or unauthorized action"}), 404

    # Update booking status instead of deleting
    booking.status = "Cancelled"
    db.session.commit()

    return jsonify({"message": f"Booking for Room {booking.room_id} on {booking.date} has been cancelled."})
