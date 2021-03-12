from database_singleton import Singleton
from sqlalchemy.dialects.postgresql import UUID
import uuid

db = Singleton().database_connection()

class Category(db.Model):
    __tablename__ = "product_category"

    productcategoryid = db.Column(db.SmallInteger, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.Text, nullable=False)

    def __init__(self, name):
        self.name = name


class Request(db.Model):
    __tablename__ = "request"

    requestid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    productname = db.Column(db.Text, nullable=False)
    startdate = db.Column(db.Date, nullable=False)
    enddate = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    requester = db.Column(db.Text, nullable=False)
    lender = db.Column(db.Text, nullable=False)
    productcategoryid = db.Column(db.SmallInteger, db.ForeignKey('product_category.productcategoryid'))

    def __init__(self, productname, startdate, enddate, description, requester, lender, productcategoryid):
        self.productname = productname
        self.startdate = startdate
        self.enddate = enddate
        self.description = description
        self.requester = requester
        self.lender = lender
        self.productcategoryid = productcategoryid
