from flask import Blueprint, render_template, request, jsonify
from models import db, Room

room_bp = Blueprint("room", __name__)

@room_bp.route("/rooms", methods=["GET"])
def get_rooms():
    return render_template("rooms.html")  # Serve the HTML page

@room_bp.route("/api/rooms", methods=["GET"])
def get_rooms_api():
    rooms = Room.query.all()
    return jsonify([{"id": r.id, "number": r.number, "type": r.type, "price": r.price, "status": r.status} for r in rooms])

@room_bp.route("add", methods=["POST"])
def add_room():
    data = request.get_json()
    if not data or "number" not in data or "type" not in data or "price" not in data:
        return jsonify({"error": "Invalid data"}), 400

    new_room = Room(
        number=int(data["number"]),
        type=data["type"],
        price=float(data["price"]),
        status="Available"
    )
    db.session.add(new_room)
    db.session.commit()

    return jsonify({"message": "Room added successfully", "room": {"id": new_room.id, "number": new_room.number, "type": new_room.type, "price": new_room.price, "status": new_room.status}})

@room_bp.route("delete/<int:room_id>", methods=["DELETE"])
def delete_room(room_id):
    room = Room.query.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404

    db.session.delete(room)
    db.session.commit()
    return jsonify({"message": "Room deleted successfully"})


@room_bp.route("update/<int:room_id>", methods=["PUT"])
def update_room(room_id):
    data = request.get_json()

    if not data or "status" not in data or "price" not in data:
        return jsonify({"error": "Invalid data"}), 400

    room = Room.query.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404

    room.status = data["status"]
    room.price = float(data["price"])  # Convert price to float before saving

    db.session.commit()

    return jsonify({
        "message": "Room updated successfully",
        "room": {
            "id": room.id,
            "number": room.number,
            "type": room.type,
            "price": room.price,
            "status": room.status
        }
    })

