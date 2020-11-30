from flask_restful import Resource
from dashapp.base_helper import  retrieve_and_clean_data

class EcommerceData(Resource):

    def get(self):
        retrieve_and_clean_data()
 
        return {"response":200}




