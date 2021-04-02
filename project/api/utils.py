from project.api.models import Category


def get_category_name(requests: list) -> list:
    for request in requests:
        productcategoryid = request["productcategoryid"]
        category = Category.query.filter_by(productcategoryid=productcategoryid).first()
        request["categoryname"] = category.name

    return requests
