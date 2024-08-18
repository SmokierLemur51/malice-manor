from typing import List

from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from sqlalchemy.exc import IntegrityError

from ..models import (
    ProductCategory,
    ProductSubCategory,
    Product,
    Vendor,
)
from ..queries import (
    parse_for_category_id,
    parse_for_sub_category_id,
    parse_for_vendor_id,
)



def populate_products(db: SQLAlchemy) -> None:
    vendors = db.session.scalars(db.select(Vendor)).all()
    sub_categories = db.session.scalars(db.select(ProductSubCategory)).all()
    categories = db.session.scalars(db.select(ProductCategory)).all()
    products = [

        Product(
            # other fields handled by default
            category_id=parse_for_category_id(categories, ""),
            sub_category_id=parse_for_sub_category_id(sub_categories, ""),
            vendors=parse_for_vendor_id(vendors, ""),
            uom="",
            quantity=,
            quantity_info="",
            name="",
            info="",
            selling=,
        ),
        Product(
            category_id=parse_for_category_id(categories, ""),
            sub_category_id=parse_for_sub_category_id(sub_categories, ""),
            vendors=parse_for_vendor_id(vendors, ""),
            uom_id=,
            quantity=,
            name="",
            info="",
            selling=,
        ),
    ]
    with current_app.app_context():
        try:
            db.session.add_all(products)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            print(IntegrityError)
