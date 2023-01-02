import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
#from db import cities
from schemas import citySchema


from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import cityModel

blp = Blueprint("cities", __name__, description="Operations on cities")


@blp.route("/city/<int:city_id>")
class city(MethodView):
    @blp.response(200, citySchema)
    def get(self, city_id):
        city = cityModel.query.get_or_404(city_id)
        return city

    def delete(self, city_id):
        city = cityModel.query.get_or_404(city_id)
        db.session.delete(city)
        db.session.commit()
        return {"message": "city deleted"}

        
@blp.route("/city")
class cityList(MethodView):
    @blp.response(200, citySchema(many=True))
    def get(self):
        return cityModel.query.all()

    @blp.arguments(citySchema)
    @blp.response(201, citySchema)
    def post(self,city_data):
      city = cityModel(**city_data)
      try:
        db.session.add(city)
        db.session.commit()
      except IntegrityError: #i spcified in models the name to be unique
        abort(
            400,
            message="A city with that name already exists.",
        )
      except SQLAlchemyError:
        abort(500, message="An error occurred creating the city.")

      return city