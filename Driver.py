# -*- coding: utf-8 -*-

import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker
from database import Base, Customer, Vendor, Image, Menu, Orders

from AES import encrypt, decrypt

app = Flask(__name__)

engine = create_engine('mysql://test:password@35.245.224.212:3306/mobile_canteen')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

def validate_token(token):
    id = decrypt(token)
    session = DBSession()
    user = session.query(Customer).filter_by(customer_id = id)
    if user != None:
        return True
    else:
        return False

@app.route('/register/', methods = ['GET', "POST"])
def user_register():
    if request.method == 'POST':
        session = DBSession()
        data = request.get_data()
        data_dict = json.loads(data)
        if data_dict['type'] == 'customer':
        	find_customer = session.query(Customer).filter_by(phone = data_dict['phone'].decode('utf-8')).first()
        	if find_customer is not None:
        		return jsonify({"error_msg": "Existed"})
        	newCustomer = Customer(name = data_dict['name'], phone = data_dict['phone'], password = encrypt(data_dict["password"]))
        	session.add(newCustomer)
        else:

        	find_vendor = session.query(Vendor).filter_by(phone = data_dict['phone'].decode('utf-8')).first()
        	if find_vendor is not None:
        		return jsonify({"error_msg": "Existed"})
        	newVendor = Vendor(name = data_dict['name'], phone = data_dict['phone'], password = encrypt(data_dict["password"]))
        	session.add(newVendor)
        session.commit()
        session.close()
        return jsonify({"error_msg": None})
    else:
        return jsonify({"error_msg":'POST only'})

@app.route('/login/', methods = ['GET', "POST"])
def user_login():
    if request.method == 'POST':
        session = DBSession()
        data = request.get_data()
        data_dict = json.loads(data)
        if data_dict['type'] == 'customer':
        	customer = session.query(Customer).filter_by(phone = data_dict['phone']).first()
        	if customer is None:
        		return jsonify({'error_msg': "Not Exist", "token":None})
            if customer.password != encrypt(data_dict['password']):
                return jsonify({'error_msg': "Wrong Password", "token":None})
        	uid = customer.customer_id;
        	session.close()
        else:
        	vendor = session.query(Vendor).filter_by(phone = data_dict['phone']).first()
        	if vendor is None:
        		return jsonify({'error_msg': "Not Exist", "token":None})
            if vendor.password != encrypt(data_dict['password']):
                return jsonify({'error_msg': "Wrong Password", "token":None})
        	uid = customer.customer_id;
        	session.close()
        return jsonify({"token":encrypt(str(uid)), "error_msg":None})
    else:
        return jsonify({"error_msg":'POST only'})

@app.route('/menus/')
def get_menus():
    if request.method == 'GET':
        
        # TODO: return today's menu
        return jsonify()

@app.route('/menus/<int:dish_id>/')
def get_dish():
    if request.method == 'GET':
        
        # TODO: return certain dish
        return jsonify()

@app.route('/menus/add/', methods = ['GET', 'POST'])
def publish_dish():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        token = data['token']
        if not validate_token(token):
            return jsonify({"error_msg": "invalid user"})
        name = data["name"]
        description = data["description"]
        ingredients = data["ingredients"]
        quantity = data["quantity"]
        price = data["price"]
        image = data["image"]
        

        return True

@app.route('/vendors/')
def get_vendors():
    if request.method == 'GET':
        
        # TODO: return vendors
        return jsonify()

@app.route('/vendors/<int:vendor_id>/')
def get_vendor():
    if request.method == 'GET':
        
        # TODO: return vendor
        return jsonify()

@app.route('/vendors/<int:vendor_id>/menu/')
def get_vendor_offerings():
    if request.method == 'GET':
        
        # TODO: return vendor's offerings
        return jsonify()

@app.route('/orders/<int:customer_id>/')
def get_customer_orders():
    if request.method == 'GET':
        
        # TODO: return orders
        return jsonify()

@app.route('/orders/<int:customer_id>/<int:dish_id>/')
def get_order():
    if request.method == 'GET':
        
        # TODO: return certain orders
        return jsonify()

@app.route('/orders/add/', methods = ['GET', 'POST'])
def place_order():
    if request.method == 'POST':
        # TODO: place order
        return jsonify()

@app.route('/status/<int:vendor_id>/')
def get_vendor_orders():
    if request.method == 'GET':
        
        # TODO: return certain orders
        return jsonify()

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
