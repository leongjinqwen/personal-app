from models.base_model import BaseModel
import peewee as pw
from models.user import User
from playhouse.hybrid import hybrid_property

class Category(BaseModel):
    user = pw.ForeignKeyField(User, backref='categories')
    name = pw.CharField(null=False)
