from dashapp import init_app



app = init_app()

# db = SQLAlchemy(app)


if __name__=="__main__":
    app.run(host="0.0.0.0")