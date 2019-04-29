# -*- coding: utf-8 -*-

import json
import base64
import uuid
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker
from database import Base, Customer, Vendor, Menu, Orders
from google.cloud import storage
from datetime import date, datetime
from AES import encrypt, decrypt, AES_encrypt

app = Flask(__name__)

engine = create_engine('mysql://test:password@35.245.224.212:3306/mobile_canteen')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

# Change path to fit current platform
TMP_IMAGE_PATH = "F:\\2018CMU\\17781\\tmp\\"
GCP_BUCKET = "mobile-cateen-images"

def validate_token(token, table):
    id = decrypt(token)
    session = DBSession()
    if table == "Vendor":
        user = session.query(Vendor).filter_by(vendor_id = id).first()
    elif table == "Customer":
        user = session.query(Customer).filter_by(customer_id = id).first()
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

def retrieve_image(session, items):
    info = []
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(GCP_BUCKET)
    for item in items:
        image_name = item["image"]
        print(image_name)
        if image_name != None and image_name != "":
            blob = bucket.blob(image_name)
            tmp_image = TMP_IMAGE_PATH + image_name
            blob.download_to_filename(tmp_image)
            with open(tmp_image, "rb") as image_obj:
                image_read = image_obj.read()
                item["image_data"] = base64.b64encode(image_read).decode('utf-8')
            os.remove(tmp_image)

        vendor_id = item["vendor_id"]
        vendor = session.query(Vendor).filter_by(vendor_id=vendor_id).first()
        item["vendor_name"] = vendor.name
        info.append(item)

    return info

def retrieve_order_info(session, orders):
    order_info = []
    for order in orders:
        customer_id = order['customer_id']
        dish_id = order['dish_id']
        customer = session.query(Customer).filter_by(customer_id=customer_id).first()
        order['customer_name'] = customer.name
        dish = session.query(Menu).filter_by(dish_id=dish_id).first()
        order['dish_name'] = dish.name
        order.pop('customer_id', None)
        order.pop('dish_id', None)
        order_info.append(order)
    return order_info

@app.route('/register/', methods = ['GET', "POST"])
def user_register():
    if request.method == 'POST':
        session = DBSession()
        data = request.get_data().decode('utf-8')
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
        data = request.get_data().decode('utf-8')
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
            uid = vendor.vendor_id
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
        session.close()
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
        data = json.loads(request.get_data().decode('utf-8'))
        token = data['token']
        vendor_id = validate_token(token, "Vendor")
        print("vendor_id: %s" % vendor_id)
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
        session = DBSession()
        vendors = session.query(Vendor).all()
        vendor_info = [vendor.serialize for vendor in vendors]
        vendor_info = retrieve_image(session, vendor_info)
        return jsonify(Menu = vendor_info)

@app.route('/vendors/menus')
def get_vendor_menu():
    if request.method == 'GET':
        session = DBSession()
        token = request.args.get('token')
        vendor_id = validate_token(token, "Vendor")
        print("vendor_id: %s" % vendor_id)
        if not vendor_id:
            return jsonify({"error_msg": "invalid user"})
        dishes = session.query(Menu).filter_by(vendor_id = vendor_id).all()
        dish_info = [dish.serialize for dish in dishes]
        dish_info = retrieve_image(session, dish_info)
        session.close()
        return jsonify(Menu = dish_info)

@app.route('/vendors/orders')
def get_vendor_orders():
    if request.method == 'GET':
        session = DBSession()
        token = request.args.get('token')
        vendor_id = validate_token(token, "Vendor")
        print("vendor_id: %s" % vendor_id)
        if not vendor_id:
            return jsonify({"error_msg": "invalid user"})
        orders = session.query(Orders).filter_by(vendor_id = vendor_id).all()
        order_info = [order.serialize for order in orders]
        order_info = retrieve_order_info(session, order_info)
        session.close()

        return jsonify(Orders = order_info)

@app.route('/vendors/status', methods = ['GET', 'POST'])
def vendor_status():
    if request.method == 'GET':
        session = DBSession()
        token = request.args.get('token')
        vendor_id = validate_token(token, "Vendor")
        print("vendor_id: %s" % vendor_id)
        if not vendor_id:
            return jsonify({"error_msg": "invalid user"})
        vendor = session.query(Vendor).filter_by(vendor_id = vendor_id).first()
        session.close()
        return jsonify({"status": vendor.status, "error_msg": None})
    elif request.method == 'POST':
        session = DBSession()
        token = request.args.get('token')
        vendor_id = validate_token(token, "Vendor")
        print("vendor_id: %s" % vendor_id)
        if not vendor_id:
            return jsonify({"error_msg": "invalid user"})
        data = json.loads(request.get_data().decode('utf-8'))
        vendor = session.query(Vendor).filter_by(vendor_id = vendor_id).first()
        vendor.status = data["status"]
        session.add(vendor)
        session.commit()
        session.close()
        return jsonify({"error_msg": None})

@app.route('/orders/status/', methods = ['GET', 'POST'])
def order_status():
    if request.method == 'GET':
        session = DBSession()
        data_dict = json.loads(request.get_data().decode('utf-8'))
        order_id = data_dict["order_id"]
        order = session.query(Orders).filter_by(order_id = order_id).first()
        session.close()
        return jsonify({"status": order.status, "error_msg": None})
    elif request.method == 'POST':
        session = DBSession()
        data = json.loads(request.get_data().decode('utf-8'))
        order_id = data["order_id"]
        order = session.query(Orders).filter_by(order_id = order_id).first()
        order.status = data["status"]
        session.add(order)
        session.commit()
        session.close()
        return jsonify({"error_msg": None})

@app.route('/orders/<int:customer_id>/<int:dish_id>/')
def get_order():
    if request.method == 'GET':
        
        # TODO: return certain orders
        return jsonify()

@app.route('/orders/add/', methods = ['GET', 'POST'])
def place_order():
    if request.method == 'POST':
        session = DBSession()
        data_dict = json.loads(request.get_data().decode('utf-8'))
        amount = data_dict['amount']
        dish_id = data_dict['dish_id']
        customer_id = decrypt(data_dict['token'])
        customer = session.query(Customer).filter_by(customer_id = customer_id).first()
        if not customer:
            return jsonify({'error_msg':'no such user'})
        
        dish = session.query(Menu).filter_by(dish_id = dish_id).first()
        if not dish:
            return jsonify({'error_msg':'do not have this dish'})
        if dish.amount_left < amount:
            return jsonify({'error_msg':'not enough dishes'})
        dish.amount_left -= amount
        newOrder = Orders(customer_id = customer_id, dish_id = dish_id, status = 'Not yet', quantity = amount, timestamp = datetime.now(), vendor_id = dish.vendor_id)
        session.add(dish)
        session.add(newOrder)
        session.commit()
        session.close()
        return jsonify({'error_msg':None})

@app.route('/customers/info', methods = ['GET', 'POST'])
def customer_info():
    if request.method == 'GET':
        session = DBSession()
        token = request.args.get('token')
        customer_id = decrypt(token)
        customer = session.query(Customer).filter_by(customer_id = customer_id).first()
        if not customer:
            return jsonify({'error_msg':'no such user'})

        session.close()
        return jsonify({'error_msg':None, 'phone':customer.phone, 'name':customer.name})
    elif request.method == 'POST':
        session = DBSession()
        data = json.loads(request.get_data().decode('utf-8'))
        customer_id = decrypt(data['token'])
        customer = session.query(Customer).filter_by(customer_id = customer_id).first()
        if not customer:
            return jsonify({'error_msg':'no such user'})
        if 'name' in data and data['name']:
            customer.name = data['name']
        if 'phone' in data and data['phone']:
            customer.phone = data['phone']
        if 'password' in data and data['password']:
            customer.password = AES_encrypt(data['password'])

        session.add(customer)
        session.commit()
        session.close()

        return jsonify({'error_msg':None})

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
