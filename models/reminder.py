from models.base_model import BaseModel
import peewee as pw
from models.user import User

class Reminder(BaseModel):
    user = pw.ForeignKeyField(User, backref='reminders')
    group = pw.CharField(null=False)
    description = pw.CharField(null=False)
    status = pw.BooleanField(default=False)
    dateline = pw.DateTimeField(null=True)

   