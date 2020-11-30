from flask import Flask

def init_app():

    app = Flask(__name__,instance_relative_config=False)

    # app.config.from_object("config.Config")

    with app.app_context():

        from dashapp import routes
        from dashapp.ecommerce.dashboard import create_dashboard

        app = create_dashboard(app)
 
        return app