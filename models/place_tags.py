from db import db


class placesTags(db.Model):
    __tablename__ = "places_tags"

    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey("places.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))