from db import db


class cityModel(db.Model):
    __tablename__ = "cities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    places = db.relationship("placeModel", back_populates="city", lazy="dynamic",cascade="all, delete")
    tags = db.relationship("TagModel", back_populates="city", lazy="dynamic")