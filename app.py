from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku

import os

app = Flask(__name__)
heroku = Heroku(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
    os.path.join(basedir, "app.sqlite")

CORS(app)


db = SQLAlchemy(app)
ma = Marshmallow(app)


class Card(db.Model):
    __tablename__ = "cards"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(500))
    favorite = db.Column(db.Boolean)

    def __init__(self, text, image, favorite):
        self.text = text
        self.image = image
        self.favorite = favorite


class CardSchema(ma.Schema):
    class Meta:
        fields = ("id", "text", "image", "favorite")


card_schema = CardSchema()
cards_schema = CardSchema(many=True)


@app.route("/card/<id>", methods=["GET"])
def get_card(id):
    card = Card.query.get(id)
    result = card_schema.jsonify(card)


@app.route("/cards", methods=['GET'])
def get_cards():
    all_cards = Card.query.all()
    result = cards_schema.dump(all_cards)

    return jsonify(result.data)


@app.route("/add-card", methods=["POST"])
def add_cards():
    text = request.json["text"]
    image = request.json["image"]
    favorite = request.json["favorite"]

    record = Card(text, image, favorite)
    db.session.add(record)
    db.session.commit()

    return jsonify("card Posted!")


@app.route("/card/<id>", methods=["PUT"])
def update_card(id):
    card = card.query.get(id)

    text = request.json["text"]
    image = request.json["image"]
    favorite = request.json["favorite"]

    card.text = text
    card.image = image
    card.favorite = favorite

    db.session.commit()

    return jsonify("Update Successful")


@app.route("/card/<id>", methods=["DELETE"])
def delete_card(id):
    record = card.query.get(id)
    db.session.delete(record)

    db.session.commit()

    return jsonify("Record Deleted!")


if __name__ == "__main__":
    app.debug = True
    app.run()
