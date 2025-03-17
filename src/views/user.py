from marshmallow import fields

from src.models import User, ma


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        # load_instance = True
        # fields = ("id", "username", "role")
        # include_relationships = True


class UserIdParameter(ma.Schema):
    user_id = fields.Int(required=True, strict=True)


class CreateUserSchema(ma.SQLAlchemyAutoSchema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    role_id = fields.Integer(required=True, strict=True)
    # class Meta:
    #     fields = ("username", "password", "role_id")


# from src.views.role import RoleSchema
# class UserSchema(ma.Schema):
# class Meta:
# fields = ("id", "username", "role")
####
# role = ma.Nested(RoleSchema)
####
####
# class CreateUserSchema(ma.Schema):
# username = fields.String(required=True)
# password = fields.String(required=True)
# role_id = fields.Integer(required=True, strict=True)
# class Meta:
# fields = ("username", "password", "role_id")
