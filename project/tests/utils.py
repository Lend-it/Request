from project.api.models import Request
from project.api.models import Category
from project.api.models import db


def add_request(
    productname,
    startdate,
    enddate,
    description,
    requester,
    productcategoryid,
    lender=None,
):

    request = Request(
        productname,
        startdate,
        enddate,
        description,
        requester,
        lender,
        productcategoryid,
    )

    db.session.add(request)
    db.session.commit()
    return request


def add_category(name):
    category = Category(name)
    db.session.add(category)
    db.session.commit()
    return category
