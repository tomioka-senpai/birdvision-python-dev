class ProductSerializer:
    def __init__(self, query_data):
        self.query_data = query_data

    def list_api_serializer(self):
        serialized_data = []
        for to_serialize_item in self.query_data:
            serialized_item = {
                'product_id': to_serialize_item[0],
                'product_name': to_serialize_item[1],
                'product_description': to_serialize_item[2],
                'product_price': to_serialize_item[3],
                'product_inventory': to_serialize_item[4],
                'category': to_serialize_item[5],
                'brand': to_serialize_item[6]
            }
            serialized_data.append(serialized_item)
        return serialized_data

    def create_api_serializer(self):
        payload_data_type_validator = {
            'name': str,
            'description': str,
            'price': float,
            'inventory': int,
            'category': str,
            'brand': str,
        }
        for key in list(payload_data_type_validator.keys()):
            if type(self.query_data.get('key', None)) != payload_data_type_validator[key]:
                raise Exception(f"{key} is a required field")
        return

    def update_api_serializer(self):
        payload_data_type_validator = {
            'name': str,
            'description': str,
            'price': float,
            'inventory': int,
            'category': str,
            'brand': str,
        }
        if any(key not in payload_data_type_validator for key in list(self.query_data.keys())):
            raise Exception("Please check your payload.")
        return
