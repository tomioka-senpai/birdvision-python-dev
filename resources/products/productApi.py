import logging

from flask import request, make_response, jsonify
from flask_restful import Resource

from baked_response import BakedResponse
from database.database_handler import DatabaseHandler
from decorators import authorization
from serializer.product_serializer import ProductSerializer

logger = logging.getLogger(__name__)


class Products(Resource):

    @authorization
    def get(self, *args, **kwargs):
        try:
            query_params = request.args
            database_handler = DatabaseHandler()
            products = database_handler.list_products(
                page_number=query_params['page_number'], entry_limit=query_params['page_size']
            )
            response = BakedResponse.get_baked_200_response(data=products)
            return make_response(jsonify(response), 200)
        except Exception as e:
            logger.error(f"LISTING_API | CRITICAL_RED | ERROR: {str(e)}")
            response = BakedResponse.get_baked_500_response()
            return make_response(jsonify(response), 500)

    @authorization
    def post(self, *args, **kwargs):
        try:
            payload = request.data
            product_serializer = ProductSerializer(payload)
            product_serializer.create_api_serializer()
            database_handler = DatabaseHandler()
            database_handler.create_a_new_product_entry(database_entry_kwargs=payload)
            response = BakedResponse.get_baked_200_response(data={})
            return make_response(jsonify(response), 200)
        except Exception as e:
            logger.error(f"CREATING_API | CRITICAL_RED | ERROR: {str(e)}")
            response = BakedResponse.get_baked_500_response()
            return make_response(jsonify(response), 500)


class SingleProduct(Resource):

    @authorization
    def get(self, product_id):
        try:
            database_handler = DatabaseHandler()
            product = database_handler.get_product(product_id)
            response = BakedResponse.get_baked_200_response(data=product)
            return make_response(jsonify(response), 200)
        except Exception as e:
            logger.error(f"CREATING_API | CRITICAL_RED | ERROR: {str(e)}")
            response = BakedResponse.get_baked_500_response()
            return make_response(jsonify(response), 500)

    @authorization
    def put(self, product_id):
        try:
            payload = request.data
            database_handler = DatabaseHandler()
            product_serializer = ProductSerializer(payload)
            product_serializer.update_api_serializer()
            database_handler.update_product(product_id, update_parameters=request.data)
            response = BakedResponse.get_baked_200_response(data={'product_id': product_id})
            return make_response(jsonify(response), 200)
        except Exception as e:
            logger.error(f"UPDATING_API | CRITICAL_RED | ERROR: {str(e)}")
            response = BakedResponse.get_baked_500_response()
            return make_response(jsonify(response), 500)

    @authorization
    def delete(self, product_id):
        try:
            database_handler = DatabaseHandler()
            database_handler.delete_product(product_id)
            response = BakedResponse.get_baked_200_response(data={'product_id': product_id})
            return make_response(jsonify(response), 200)
        except Exception as e:
            logger.error(f"UPDATING_API | CRITICAL_RED | ERROR: {str(e)}")
            response = BakedResponse.get_baked_500_response()
            return make_response(jsonify(response), 500)
