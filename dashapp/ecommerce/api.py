from flask_restful import Resource

class EcommerceData(Resource):

 
    def get(self):

        from dashapp.base_helper import retrieve_and_clean_data

        try:
            retrieve_and_clean_data()
            # run_all()
            result = {"response":200}
        except :
            result = {"response":"error"}  


 
        return result


