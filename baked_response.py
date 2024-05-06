class BakedResponse:
    @staticmethod
    def get_baked_200_response(data):
        return {
            'code': 200,
            'data': data,
            'errors': "",
            'message': "Success"
        }

    @staticmethod
    def get_baked_500_response():
        return {
            'code': 500,
            'data': {},
            'errors': 'It is not you. It is us, Please try after sometime.',
            'message': 'Internal Server Error'
        }

    @staticmethod
    def get_baked_401_response():
        return {
            'code': 401,
            'data': {},
            'errors': "Sorry Cannot Authorize You. Please Check if you have provided the right credentials.",
            'message': "Unauthorized Request."
        }