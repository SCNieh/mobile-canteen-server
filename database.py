# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'

    customer_id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=True)
    password = Column(String(64), nullable=False)
    phone = Column(String(64), nullable=False, unique=True)

    orders = relationship('Orders', backref = 'user')

class Vendor(Base):
    __tablename__ = 'vendor'

    vendor_id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=True)
    password = Column(String(64), nullable=False)
    phone = Column(String(64), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    status = Column(String(16), nullable=False)
    location = Column(String(256), nullable=True)
    image = Column(String(36), nullable=True)

    dishes = relationship('Menu', backref = 'vendor')

    @property
    def serialize(self):
        return {
            'vendor_id': self.vendor_id,
            'name': self.name,
            'phone': self.phone,
            'description': self.description,
            'status': self.status,
            'location': self.location,
            'image': self.image
        }

class Menu(Base):
    __tablename__ = 'menu'

    dish_id = Column(Integer, primary_key=True)
    vendor_id = Column(Integer, ForeignKey('vendor.vendor_id'))
    uuid = Column(String(36), nullable=False, unique=True)
    date = Column(Date, nullable=False)
    name = Column(String(64), nullable=False)
    description = Column(Text, nullable=True)
    ingredients = Column(Text, nullable=True)
    amount = Column(Integer, nullable=False)
    amount_left = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    image = Column(String(36), nullable=True)

    orders = relationship("Orders", backref = 'menu')

    @property
    def serialize(self):
        return {
            'dish_id': self.dish_id,
            'name': self.name,
            'vendor_id': self.vendor_id,
            'date': self.date,
            'description': self.description,
            'ingredients': self.ingredients,
            'amount': self.amount,
            'amount_left': self.amount_left,
            'price': self.price,
            'image': self.image
        }

class Orders(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    vendor_id = Column(Integer, ForeignKey('vendor.vendor_id'))
    dish_id = Column(Integer, ForeignKey('menu.dish_id'))
    status = Column(String(128), nullable=False)
    quantity = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    @property
    def serialize(self):
        return {
            'order_id': self.order_id,
            'customer_id': self.customer_id,
            'dish_id': self.dish_id,
            'status': self.status,
            'quantity': self.quantity,
            'timestamp': self.timestamp
        }

# engine = create_engine('mysql://root:password@localhost:3306/mobile_canteen')
# Base.metadata.create_all(engine)
