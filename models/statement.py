import os
from models.base_model import BaseModel
import peewee as pw
from models.user import User
from playhouse.hybrid import hybrid_property
from datetime import date

class Statement(BaseModel):
    user = pw.ForeignKeyField(User, backref='statements')
    exp_url = pw.CharField(null=True)
    month = pw.CharField(default=date.today().strftime("%B %Y"))

    @hybrid_property
    def statement_url(self):
        return os.environ.get("AWS_S3_DOMAIN") + self.exp_url
