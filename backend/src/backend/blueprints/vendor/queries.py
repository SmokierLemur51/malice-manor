from flask_sqlalchemy import SQLAlchemy
from .extensions import vendor_login_manager

from ...models.models import Vendor

@vendor_login_manager.user_loader
def load_vendor(vendor_id):
    return Vendor.get(vendor_id)