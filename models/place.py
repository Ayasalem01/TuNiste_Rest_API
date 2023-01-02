from db import db


class placeModel(db.Model):
    __tablename__ = "places"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    city_id = db.Column(
        db.Integer, db.ForeignKey("cities.id"), unique=False, nullable=False
    )
    city = db.relationship("cityModel", back_populates="places")
    tags = db.relationship("TagModel", back_populates="places", secondary="places_tags")