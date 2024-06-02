import datetime
from typing import List

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from flask_sqlalchemy import SQLAlchemy


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)



class Vendor(Base):
    __tablename__ = "vendors"

    id: Mapped[int] = mapped_column(primary_key=True)
    vendor: Mapped[str] = mapped_column(String(120), unique=True)

    # relationships
    products: Mapped[List['Product']] = relationship(back_populates='vendor')   

    def __repr__(self) -> str:
        return "{}".format(self.vendor)



class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())    
    deleted_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    company: Mapped[str] = mapped_column(String(120), unique=True)
    street: Mapped[str] = mapped_column(String(200), unique=True)
    street_2: Mapped[str] = mapped_column(String(200), nullable=True)
    city: Mapped[str] = mapped_column(String(60))
    state: Mapped[str] = mapped_column(String(25))
    zip: Mapped[str] = mapped_column(String(10))

    contacts: Mapped[List["CustomerContact"]] = relationship(back_populates="company")
    orders: Mapped[List["Order"]] = relationship(back_populates="customer")

    def __repr__(self) -> None:
        return "{}".format(self.company)




class CustomerContact(Base):
    __tablename__ = "customer_contacts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    product: Mapped[str] = mapped_column(String(80))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())    
    deleted_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=True)
    
    company: Mapped["Customer"] = relationship(back_populates="contacts")

    def __repr__(self) -> str:
        return "Name: {} Phone: ({})-{}-{}".format(self.name, self.phone[0:3], self.phone[3:6], self.phone[6:])

    


class ProductCategory(Base):
    __tablename__ = "product_categories"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(120), unique=True)
    info: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # relationships
    products: Mapped[List["Product"]] = relationship(back_populates='category')
    sub_categories: Mapped[List["ProductSubCategory"]] = relationship(back_populates="parent_category")
    

    def __repr__(self) -> str:
        return "{}".format(self.category)





class ProductSubCategory(Base):
    __tablename__ = "product_sub_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_category_id: Mapped[int] = mapped_column(ForeignKey("product_categories.id"))
    sub_category: Mapped[str] = mapped_column(String(120), unique=True)
    info: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # relationships
    parent_category: Mapped["ProductCategory"] = relationship(back_populates="sub_categories")


    def __repr__(self) -> str:
        return "Sub Category: <{}>, Parent Category: <{}>".format(
            self.sub_category, self.parent_category.category)



# This product will not be associated with a warehouse, Product.id will be referenced
# in the InventoryItem class.
class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    product: Mapped[str] = mapped_column(String(80))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())    
    deleted_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('product_categories.id'))
    sub_category_id: Mapped[int] = mapped_column(ForeignKey('product_sub_categories.id'))    
    vendor_id: Mapped[int] = mapped_column(ForeignKey('vendors.id'))
    product: Mapped[str] = mapped_column(String(120), unique=True)
    cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    
    # need to add sizing dimensions

    # relationships
    vendor: Mapped['Vendor'] = relationship(back_populates="products")
    category: Mapped['ProductCategory'] = relationship(back_populates='products')
    sub_category: Mapped['ProductCategory'] = relationship(back_populates='products')
    




class PricingBucket(Base):
    # More information in obsidian-united/pricing/buckets.md
    __tablename__ = "pricing_buckets"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    bucket: Mapped[str] = mapped_column(String(80), unique=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())    
    deleted_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    margin_percent: Mapped[float] = mapped_column(Float, default=0.0) 
    dividend: Mapped[float] = mapped_column(Float, nullable=True, default=0.0)

    # relationships
    # products: Mapped[List["Products"]] 
    # customers: Mapped[List["Customer"]]

    def __repr__(self) -> str:
        return "{}".format(self.bucket)


    def margin_dividend(self) -> None:
        self.dividend = 1.00-(self.margin_percent/100)





class OrderType(Base):
    __tablename__ = "order_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_type: Mapped[str] = mapped_column(String(100), unique=True)
    info: Mapped[str] = mapped_column(String(500), nullable=True)

    # relationships 
    orders: Mapped[List["Order"]] = relationship(back_populates="order_type")

    def __repr__(self) -> None:
        return "{}".format(self.order_type)



class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())    
    deleted_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    customer_id:  Mapped[int] = mapped_column(ForeignKey("customers.id"))
    order_type_id: Mapped[int] = mapped_column(ForeignKey("order_types.id"))
    backorder_iteration: Mapped[int] = mapped_column(Integer, nullable=True)

    customer: Mapped["Customer"] = relationship(back_populates="orders")
    order_type: Mapped["OrderType"] = relationship(back_populates="orders")
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="order")
    

    def __repr__(self) -> None:
        return "Order-{}-{}".format(self.id, self.backorder_iteration)



class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product: Mapped[int] = mapped_column(ForeignKey("products.id"))
    line: Mapped[int] = mapped_column(Integer)

    # relationships
    order: Mapped["Order"] = relationship(back_populates="order_items")


    def __repr__(self) -> None:
        return "Order-{} Line: "


    def get_line_id(self) -> None:
        return



class Warehouse(Base):
    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(primary_key=True)
    codename: Mapped[str] = mapped_column(String(60), unique=True)
    street: Mapped[str] = mapped_column(String(120), nullable=False)
    street_2: Mapped[str] = mapped_column(String(120), nullable=True)
    city: Mapped[str] = mapped_column(String(120, nullable=False))
    state: Mapped[str] = mapped_column(String(120), nullable=False)
    zip_code: Mapped[str] = mapped_column(String(120), nullable=False)

    locations: Mapped[List["WarehouseLocations"]] = relationship(back_populates="warehouse")


    def __repr__(self) -> str:
        return "Warehouse -> {}".format(self.codename)


class WarehouseLocation(Base): 
    __tablename__ = "warehouse_locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"))
    location: Mapped[str] = mapped_column(String(120), unique=True)

    warehouse: Mapped["Warehouse"] = relationship(back_populates="locations")


    def __repr__(self) -> str:
        return "Location: {} Warehouse-ID: {}".format(self.location, self.warehouse_id)



class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())    
    deleted_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    product_id: Mapped[int]
    reserved_status: Mapped[bool] = mapped_column(Boolean, default=False)
    reserved_on: Mapped[int] = mapped_column(ForeignKey("orders.id"))

    reserved_for: Mapped["Order"] = relationship(back_populates="")
