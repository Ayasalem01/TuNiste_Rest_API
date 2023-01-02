from marshmallow import Schema, fields


class plainplaceSchema(Schema): #not conected to any city
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    
#city schemas
class plaincitySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


#the tag schema
class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()




#other schemas -->optional 
class placeUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    city_id=fields.Int()


class placeSchema(plainplaceSchema):
    city_id = fields.Int(required=True, load_only=True)
    city = fields.Nested(plaincitySchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class citySchema(plaincitySchema):
    places = fields.List(fields.Nested(plainplaceSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class TagSchema(PlainTagSchema):
    city_id = fields.Int(load_only=True)
    places = fields.List(fields.Nested(plainplaceSchema()), dump_only=True)
    city = fields.Nested(plaincitySchema(), dump_only=True)


class TagAndplaceSchema(Schema):
    message = fields.Str()
    place = fields.Nested(placeSchema)
    tag = fields.Nested(TagSchema)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)