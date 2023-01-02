
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from db import db
from models import placeModel
from sqlalchemy.exc import SQLAlchemyError

#from db import places
from schemas import placeSchema, placeUpdateSchema #placeUpdateSchema

blp = Blueprint("places", __name__, description="Operations on places")


@blp.route("/place/<int:place_id>")
class place(MethodView):
    @jwt_required()
    @blp.response(200, placeSchema)
    def get(self, place_id):
        place = placeModel.query.get_or_404(place_id)
        return place

        #delete command-----------------
     
    @jwt_required() 
    def delete(self, place_id):
        place = placeModel.query.get_or_404(place_id)
        db.session.delete(place)
        db.session.commit()
        return {"message": "place deleted."}
        
        #update command---------------------
    @blp.arguments(placeUpdateSchema)
    @blp.response(200, placeSchema)
    def put(self,place_data, place_id):
       place = placeModel.query.get(place_id)
       if place:
        place.price = place_data["price"]
        place.name = place_data["name"]
       else:
        place = placeModel(id=place_id, **place_data)

       db.session.add(place)
       db.session.commit()

       return place

@blp.route("/place")
class placeList(MethodView):
    @jwt_required()
    @blp.response(200, placeSchema(many=True))
    def get(self):
        return placeModel.query.all()

#---------------------------------------------------create place:POST
    @jwt_required()
    @blp.arguments(placeSchema)
    @blp.response(201, placeSchema)
    def post(self,place_data):
        
        place = placeModel(**place_data)

        try:
          db.session.add(place)
          db.session.commit()
        except SQLAlchemyError:
          abort(500, message="An error occurred while inserting the place.")

        return place
        