from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, cityModel,placeModel
from schemas import TagSchema,  TagAndplaceSchema

blp = Blueprint("Tags", "tags", description="Operations on tags")


@blp.route("/city/<int:city_id>/tag")
class TagsIncity(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, city_id):
        city = cityModel.query.get_or_404(city_id)

        return city.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, city_id):
        if TagModel.query.filter(TagModel.city_id == city_id).first():
            abort(400, message="A tag with that name already exists in that city.")

        tag = TagModel(**tag_data, city_id=city_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )

        return tag

#manipulate tags to place=> add or delete the tags
@blp.route("/place/<int:place_id>/tag/<int:tag_id>")
class LinkTagsToplace(MethodView):
    @blp.response(201, TagSchema)
    def post(self, place_id, tag_id):
        place = placeModel.query.get_or_404(place_id)
        tag = TagModel.query.get_or_404(tag_id)

        place.tags.append(tag)

        try:
            db.session.add(place)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return tag

    @blp.response(200, TagAndplaceSchema)
    def delete(self, place_id, tag_id):
        place = placeModel.query.get_or_404(place_id)
        tag = TagModel.query.get_or_404(tag_id)

        place.tags.remove(tag)

        try:
            db.session.add(place)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return {"message": "place removed from tag", "place": place, "tag": tag}





@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(
        202,
        description="Deletes a tag if no place is tagged with it.",
        example={"message": "Tag deleted."},
    )


    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more places. In this case, the tag is not deleted.",
    ) 
    #to actually delete a whole tag 
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.places:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(
            400,
            message="Could not delete tag. Make sure tag is not associated with any places, then try again.",)
