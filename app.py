from flask import Flask, send_file
from flask_restful import Api

from resources.products.productApi import Products, SingleProduct

app = Flask(__name__)
app.config['SECRET_KEY'] = "$$$$$$$$$$$$#####@"
api = Api(app)
api.add_resource(Products, '/products/')
api.add_resource(SingleProduct, '/products/<int:product_id>')

