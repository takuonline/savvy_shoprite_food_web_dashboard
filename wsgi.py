from dashapp import init_app
# import logging



app = init_app()



if __name__=="__main__":
    # from waitress import serve

    # serve(app,host="0.0.0.0",port=8080)

    app.run(host="0.0.0.0",
    # debug=True
    )