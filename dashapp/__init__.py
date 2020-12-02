from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from dashapp.ecommerce.api import EcommerceData
import os
def init_app():

    app = Flask(__name__,instance_relative_config = False)

    # setting up database
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+os.path.join(basedir,"data.sqlite")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    global db
    db = SQLAlchemy(app)
    

    # app.config.from_object("config.Config")

    with app.app_context():
        
        from dashapp import routes
        from dashapp.ecommerce.dashboard import create_dashboard
        
        app = create_dashboard(app)

        db.create_all()

        #setting up an api
        api = Api(app)
        api.add_resource(EcommerceData,"/updateData")

 
        return app

       