#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# TODO: add functionality to all routes

@app.route('/events')
def get_events():
    events = Event.query.all()
    response_body = []

    for event in events:
            response_body.append({
            "id": event.id,
            "name": event.name,
            "location": event.location
            })

    return make_response(response_body, 200)


@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    event = Event.query.filter_by(id=id).first()

    if event:
        response_body = []

        for session in event.sessions:
            response_body.append({
                "id": session.id,
                "title": session.title,
                "start_time": session.start_time.isoformat()
            })

        return make_response(response_body, 200)

    return make_response(
        {"error": "Event not found"},
        404
    )


@app.route('/speakers')
def get_speakers():
    speakers = Speaker.query.all()

    response_body = []

    for speaker in speakers:
        response_body.append({
            "id": speaker.id,
            "name": speaker.name
        })

    return make_response(response_body, 200)


@app.route('/speakers/<int:id>')
def get_speaker(id):
    speaker = Speaker.query.filter_by(id=id).first()

    if not speaker:
        return make_response(
            {"error": "Speaker not found"},
            404
        )

    if speaker.bio:
        bio_text = speaker.bio.bio_text
    else:
        bio_text = "No bio available"

    response_body = {
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": bio_text
    }

    return make_response(response_body, 200)


@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    session = Session.query.filter_by(id=id).first()

    if not session:
        return make_response(
            {"error": "Session not found"}, 404
        )
    response_body = []

    for speaker in session.speakers:
        if speaker.bio:
            bio_text = speaker.bio.bio_text
        else:
            bio_text = "No bio available"

        response_body.append({
            "id": speaker.id,
            "name": speaker.name,
            "bio_text": bio_text
        })

    return make_response(response_body, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)