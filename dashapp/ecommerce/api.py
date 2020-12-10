from flask_restful import Resource
from datetime import datetime

class EcommerceData(Resource):

    def get(self):
        start_time = datetime.now()

        from dashapp.base_helper import retrieve_and_clean_data

        try:
            retrieve_and_clean_data()
            # run_all()
            end_time = datetime.now()

            time = end_time-start_time

            result = {"response":200,
                        "start_time":str(start_time),
                        "end_time":str(end_time),
                        "time":str(time)
            }
        except :
            end_time = datetime.now()
            time = end_time-start_time
            result = {"response":"error",
                        "start_time":str(start_time),
                        "end_time":str(end_time),
                        "time":str(time)
                    }  


 
        return result


