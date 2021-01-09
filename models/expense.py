from models.base_model import BaseModel
import peewee as pw
from models.user import User
from models.category import Category
from playhouse.hybrid import hybrid_property
from datetime import date

class Expense(BaseModel):
    cat = pw.ForeignKeyField(Category, backref='expenses' )
    category = pw.CharField(null=False)
    description = pw.CharField(null=False)
    amount = pw.DecimalField(decimal_places=2,default=0)
    source = pw.CharField(null=False)
    month = pw.CharField(default=date.today().strftime("%b"))

