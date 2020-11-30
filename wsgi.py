from dashapp import init_app
from dashapp.ecommerce.api import EcommerceData
from flask_restful import Api


app = init_app()

api = Api(app)

api.add_resource(EcommerceData,"/updateData")

if __name__=="__main__":
    app.run()