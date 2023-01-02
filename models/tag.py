from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    city_id = db.Column(db.Integer(), db.ForeignKey("cities.id"), nullable=False)

    city = db.relationship("cityModel", back_populates="tags")
    places = db.relationship("placeModel", back_populates="tags", secondary="places_tags")