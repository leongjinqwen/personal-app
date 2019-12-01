from models.base_model import BaseModel
import peewee as pw
from models.user import User

class Expense(BaseModel):
    user = pw.ForeignKeyField(User, backref='expenses')
    category = pw.CharField(null=False)
    description = pw.CharField(null=False)
    amount = pw.DecimalField(decimal_places=2,default=0)
    source = pw.CharField(null=False)

   