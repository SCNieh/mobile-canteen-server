# -*- coding: utf-8 -*-

import json
import base64
import uuid
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker
from database import Base, Customer, Vendor, Image, Menu, Orders
from google.cloud import storage
from datetime import date
from AES import encrypt, decrypt, AES_encrypt

app = Flask(__name__)

engine = create_engine('mysql://root:password@localhost:3306/mobile_canteen')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

TMP_IMAGE_PATH = "F:\\2018CMU\\17781\\tmp\\"
GCP_BUCKET = "mobile-cateen-images"

def validate_token(token):
    id = decrypt(token)
    session = DBSession()
    user = session.query(Customer).filter_by(customer_id = id)
    if user != None:
        return id
    else:
        return None

def upload_image(image):
    image_decode = base64.b64decode(image)
    image_name = str(uuid.uuid4())
    tmp_image = TMP_IMAGE_PATH + image_name
    with open(tmp_image, 'wb') as image_obj:
        image_obj.write(image_decode)

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(GCP_BUCKET)
    blob = bucket.blob(image_name)
    blob.upload_from_filename(tmp_image)
    os.remove(tmp_image)

    return image_name

def retrieve_image(session, dish_info):
    info = []
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(GCP_BUCKET)
    for dish in dish_info:
        image_name = dish["image"]       
        blob = bucket.blob(image_name)
        tmp_image = TMP_IMAGE_PATH + image_name
        blob.download_to_filename(tmp_image)
        with open(tmp_image, "rb") as image_obj:
            image_read = image_obj.read()
            dish["image_data"] = base64.b64encode(image_read)
        info.append(dish)

    return info

@app.route('/register/', methods = ['GET', "POST"])
def user_register():
    if request.method == 'POST':
        session = DBSession()
        data = request.get_data()
        data_dict = json.loads(data)
        if data_dict['type'] == 'customer':
        	find_customer = session.query(Customer).filter_by(phone = data_dict['phone']).first()
        	if find_customer:
        		return jsonify({"error_msg": "Existed"})
        	newCustomer = Customer(name = data_dict['name'], phone = data_dict['phone'], password = AES_encrypt(data_dict["password"]))
        	session.add(newCustomer)
        else:
            find_vendor = session.query(Vendor).filter_by(phone = data_dict['phone']).first()
            if find_vendor:
                return jsonify({"error_msg": "Existed"})
            newVendor = Vendor(name = data_dict['name'], phone = data_dict['phone'], password = AES_encrypt(data_dict["password"]), status = "unavaliable")
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
            if not customer:
                return jsonify({'error_msg': "Not Exist", "token": None})
            if customer.password != AES_encrypt(data_dict['password']):
                return jsonify({'error_msg': "Wrong Password", "token":None})
            uid = customer.customer_id
            session.close()
        else:
            vendor = session.query(Vendor).filter_by(phone = data_dict['phone']).first()
            if not vendor:
                return jsonify({'error_msg': "Not Exist", "token": None})
            if vendor.password != AES_encrypt(data_dict['password']):
                return jsonify({'error_msg': "Wrong Password", "token":None})
            uid = vendor.vendor_id;
            session.close()
        return jsonify({"token":encrypt(str(uid)), "error_msg":None})
    else:
        return jsonify({"error_msg":'POST only'})

@app.route('/menus/')
def get_menus():
    if request.method == 'GET':
        session = DBSession()
        dishes = session.query(Menu).all()
        dish_info = [dish.serialize for dish in dishes]
        dish_info = retrieve_image(session, dish_info)
        return jsonify(Menu = dish_info)

@app.route('/menus/<int:dish_id>/')
def get_dish():
    if request.method == 'GET':
        session = DBSession()

        # TODO: return certain dish
        return jsonify()

@app.route('/menus/add/', methods = ['GET', 'POST'])
def publish_dish():
    if request.method == 'POST':
        session = DBSession()
        data = json.loads(request.get_data())
        token = data['token']
        vendor_id = validate_token(token)
        if not vendor_id:
            return jsonify({"error_msg": "invalid user"})
        name = data["name"]
        if "description" in data:
            description = data["description"]
        else:
            description = ""
        if "ingredients" in data:
            ingredients = data["ingredients"]
        else:
            ingredients = ""
        quantity = data["quantity"]
        price = data["price"]
        image = data["image"]
        image_name = upload_image(image)
        uid = str(uuid.uuid4())
        new_dish = Menu(vendor_id=vendor_id, uuid=uid, date=date.today(), name=name, description=description, ingredients=ingredients, amount=quantity, amount_left=quantity, price=price, image=image_name)
        session.add(new_dish)
        session.commit()
        session.close()

        return jsonify({"error_msg": None})

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
