from flask_restful import Resource


class EcommerceData(Resource):


    def get(self):
        from dashapp.base_helper import retrieve_and_clean_data
        retrieve_and_clean_data()
 
        return {"response":200}




