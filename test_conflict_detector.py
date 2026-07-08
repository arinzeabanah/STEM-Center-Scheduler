"""SQLAlchemy models for rooms and scheduled events."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=10)

    events = db.relationship("Event", backref="room", lazy=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "capacity": self.capacity}


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    description = db.Column(db.Text, default="")
    organizer_name = db.Column(db.String(80), nullable=False)
    organizer_email = db.Column(db.String(120), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, index=True)
    end_time = db.Column(db.DateTime, nullable=False)
    google_event_id = db.Column(db.String(120), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "organizer_name": self.organizer_name,
            "organizer_email": self.organizer_email,
            "room_id": self.room_id,
            "room_name": self.room.name if self.room else None,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "google_event_id": self.google_event_id,
            "synced_to_google": self.google_event_id is not None,
        }
