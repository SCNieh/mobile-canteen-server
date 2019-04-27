# -*- coding: utf-8 -*-

import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="username",
  passwd="password"
)

mycursor = mydb.cursor()

app = Flask(__name__)

@app.route('/login/', methods = ['GET', "POST"])
def user_register():
    if request.method == 'POST':
        data = request.get_data()
        # TODO: register
        return jsonify()
    else:
        return 'POST only'

@app.route('/login/', methods = ['GET', "POST"])
def user_login():
    if request.method == 'POST':
        data = request.get_data()
        # TODO: verification
        return jsonify()
    else:
        return 'POST only'

@app.route('/menus/')
def get_menus():
    if request.method == 'GET':
        mycursor.execute("SELECT * FROM menu")
        myresult = mycursor.fetchall()
        # TODO: return today's menu
        return jsonify()

@app.route('/menus/<int:dish_id>/')
def get_dish():
    if request.method == 'GET':
        mycursor.execute("SELECT * FROM menu WHERE dish_id = %d" % dish_id)
        myresult = mycursor.fetchall()
        # TODO: return certain dish
        return jsonify()

@app.route('/menus/add/', methods = ['GET', 'POST'])
def publish_dish():
    if request.method == 'POST':
        # TODO: add dish to db
        return True

@app.route('/vendors/')
def get_vendors():
    if request.method == 'GET':
        mycursor.execute("SELECT * FROM vendor")
        myresult = mycursor.fetchall()
        # TODO: return vendors
        return jsonify()

@app.route('/vendors/<int:vendor_id>/')
def get_vendor():
    if request.method == 'GET':
        mycursor.execute("SELECT * FROM vendor WHERE vendor_id = %d" % vendor_id)
        myresult = mycursor.fetchall()
        # TODO: return vendor
        return jsonify()

@app.route('/vendors/<int:vendor_id>/menu/')
def get_vendor_offerings():
    if request.method == 'GET':
        mycursor.execute("SELECT * FROM menu WHERE vendor_id = %d" % vendor_id)
        myresult = mycursor.fetchall()
        # TODO: return vendor's offerings
        return jsonify()

@app.route('/orders/<int:customer_id>/')
def get_orders():
    if request.method == 'GET':
        mycursor.execute("SELECT * FROM order WHERE customer_id = %d" % customer_id)
        myresult = mycursor.fetchall()
        # TODO: return orders
        return jsonify()

@app.route('/orders/<int:customer_id>/<int:dish_id>/')
def get_order():
    if request.method == 'GET':
        mycursor.execute("SELECT * FROM order WHERE customer_id = %d AND dish_id = %d" % (customer_id, dish_id))
        myresult = mycursor.fetchall()
        # TODO: return certain orders
        return jsonify()

@app.route('/orders/add/', methods = ['GET', 'POST'])
def place_order():
    if request.method == 'POST':
        # TODO: place order
        return jsonify()

@app.route('/status/<int:vendor_id>/')
def get_order():
    if request.method == 'GET':
        mycursor.execute("SELECT * FROM status WHERE vendor_id = %d" % vendor_id)
        myresult = mycursor.fetchall()
        # TODO: return certain orders
        return jsonify()
