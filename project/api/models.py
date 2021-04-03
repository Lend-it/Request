from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql
import uuid

db = SQLAlchemy()


class Category(db.Model):
    __tablename__ = "product_category"

    productcategoryid = db.Column(
        db.SmallInteger, primary_key=True, autoincrement=True, nullable=False
    )
    name = db.Column(db.Text, nullable=False)

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {
            "productcategoryid": self.productcategoryid,
            "name": self.name,
        }


class Request(db.Model):
    __tablename__ = "request"

    requestid = db.Column(
        postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    productname = db.Column(db.Text, nullable=False)
    startdate = db.Column(db.Date, nullable=False)
    enddate = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    requester = db.Column(db.Text, nullable=False)
    finalized = db.Column(db.Boolean, nullable=False, default=False)
    lender = db.Column(db.Text, nullable=True)
    productcategoryid = db.Column(
        db.SmallInteger, db.ForeignKey("product_category.productcategoryid")
    )

    def __init__(
        self,
        productname,
        startdate,
        enddate,
        description,
        requester,
        lender,
        productcategoryid,
    ):
        self.productname = productname
        self.startdate = startdate
        self.enddate = enddate
        self.description = description
        self.requester = requester
        self.lender = lender
        self.productcategoryid = productcategoryid

    def to_json(self):
        return {
            "requestid": self.requestid,
            "productname": self.productname,
            "startdate": self.startdate,
            "enddate": self.enddate,
            "description": self.description,
            "requester": self.requester,
            "finalized": self.finalized,
            "lender": self.lender,
            "productcategoryid": self.productcategoryid,
        }
