from flask import Blueprint, render_template, request, jsonify
from models import db, Room, Booking
from flask_login import login_required, current_user

customer1_bp = Blueprint("customer1", __name__)

@customer1_bp.route("/book_room", methods=["GET"])
@login_required
def book_room_page():
    return render_template("book_room.html")

@customer1_bp.route("/book_room", methods=["POST"])
@login_required
def book_room():
    data = request.get_json()
    room_number = data.get("room_number")
    date = data.get("date")

    if not room_number or not date:
        return jsonify({"message": "Missing room number or date"}), 400

    # Check if the room exists
    print(f"Received room number: {room_number}")  # Debugging
    room = Room.query.filter_by(number=room_number).first()
    print(f"Found room: {room}")  # Debugging
    if not room:
        return jsonify({"message": "Invalid room number"}), 400

    # Check if the room is already booked on that date
    existing_booking = Booking.query.filter_by(room_id=room.id, date=date).first()
    if existing_booking:
        return jsonify({"message": "Room is already booked, try another date"}), 400

    # Create a new booking
    new_booking = Booking(user_id=current_user.id, room_id=room.id, date=date, status="Pending")
    db.session.add(new_booking)
    db.session.commit()

    return jsonify({"message": f"Room {room.number} booked successfully for {date}!"})
