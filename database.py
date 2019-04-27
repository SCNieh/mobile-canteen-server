# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'

    customer_id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=True)
    password = Column(String(64), nullable=False)
    phone = Column(String(64), nullable=True)

    orders = relationship('Orders', backref = 'user')

class Vendor(Base):
    __tablename__ = 'vendor'

    vendor_id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=True)
    password = Column(String(64), nullable=False)
    phone = Column(String(64), nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String(16), nullable=False)
    location = Column(String(256), nullable=False)

    images = relationship('Image', backref = 'vendor')
    dishes = relationship('Menu', backref = 'vendor')
    status = relationship('Status', backref = 'vendor')

class Image(Base):
    __tablename__ = 'image'
    
    image_id = Column(Integer, primary_key=True)
    url = Column(String(512), nullable=False)
    vendor_id = Column(Integer, ForeignKey('vendor.vendor_id'))
    dish_id = Column(Integer, ForeignKey('menu.dish_id'))

class Menu(Base):
    __tablename__ = 'menu'

    dish_id = Column(Integer, primary_key=True)
    vendor_id = Column(Integer, ForeignKey('vendor.vendor_id'))
    date = Column(Date, nullable=False)
    name = Column(String(64), nullable=False)
    description = Column(Text, nullable=True)
    ingredient = Column(Text, nullable=True)
    amount = Column(Integer, nullable=False)
    amount_left = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    dishes = relationship('Images', backref = 'menu')
    orders = relationship("Orders", backref = 'menu')

class Orders(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    dish_id = Column(Integer, ForeignKey('menu.dish_id'))

engine = create_engine('mysql://test:password@35.245.224.212:3306/mobile_canteen')
# Base.metadata.create_all(engine)