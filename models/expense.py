from models.base_model import BaseModel
import peewee as pw
from models.user import User
from models.category import Category
from playhouse.hybrid import hybrid_property
from datetime import date

class Expense(BaseModel):
    category = pw.ForeignKeyField(Category, backref='expenses',default=1 )
    description = pw.CharField(null=False)
    amount = pw.DecimalField(decimal_places=2,default=0)
    source = pw.CharField(null=False)
    month = pw.CharField(default=date.today().strftime("%b"))

    # @hybrid_property
    # def created_month(self):
    #     return self.created_at.date().strftime("%b")