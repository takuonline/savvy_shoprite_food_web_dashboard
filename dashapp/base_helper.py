import pandas as pd
import pymongo
import os
from dashapp.ecommerce.models  import *
# from wsgi import db
import dashapp


db_username = os.environ.get("USER")
db_password = os.environ.get("PASSWORD")
 
#process data into different classes

cheap_products = []

expensive_products = []

no_change = []

non_food_items = []


# df = pd.read_csv("ecommerce_data.csv") # for testing  purposes 
# print(db_username,db_password)


def load_from_db():
 
    client = pymongo.MongoClient(f"mongodb+srv://{db_username}:{db_password}@cluster0.mcpct.mongodb.net/ecommerce?retryWrites=true&w=majority")
    db = client["ecommerce"]
    collection = db.shoprite
    #fetch data from Mongodb database

    return pd.DataFrame(list(collection.find()))

def clean_df(df):
    #cleaning the data
    df.set_index("title",inplace=True)
    df["date"] = pd.to_datetime(df["date"])
    df["price"] = df["price"].apply(lambda x: float( (x.strip()).replace(",","").replace("R","") ) )

    # store df
    # df.to_csv("dashapp/ecommerce/data_files/clean_df.csv")

    # df.to_sql(
    #     name="clean_df",
    #     if_exists='replace',
    #     con=db

    # )

    # for i in range(len(data)):
    
    # print(data.iloc[i,0],
    #       data.iloc[i,1],
          
          
    #      )
# title,_id,price,image_url,date)
 
    db.session.add_all([CleanDf(df.index[i],
                                # df.iloc[i,0],
                                df.iloc[i,1],
                                df.iloc[i,2],
                                str(df.iloc[i,3]),
                           
                                ) for i in range(len(df)) ])

    return df

def process_data(df):
    #classify data
    for item_name in df.index.unique():
        count = df[df.index == item_name]["price"].count()
        mean = df[df.index == item_name]["price"].mean()
        last_figure = df[df.index == item_name]["price"][-1]
    
        if(count<=10):
            non_food_items.append(item_name) 

        else:        
            if (last_figure < mean):
                # cheap
                cheap_products.append(item_name)
            elif (last_figure == mean):
                no_change.append(item_name)
            else:
                #expensive
                expensive_products.append(item_name)
        
def clean_old_data():

    db.session.query(NoChangeProducts).delete()
    db.session.commit()

    db.session.query(NonFoodProducts).delete()
    db.session.commit()

    db.session.query(CheapProducts).delete()
    db.session.commit()

    db.session.query(ExpensiveProducts).delete()
    db.session.commit()

    db.session.query(CleanDf).delete()
    db.session.commit()





def store_data():
  
    # store classified data    

    db.session.add_all( [ CheapProducts(i) for i in cheap_products])
    db.session.commit()

    db.session.add_all( [ ExpensiveProducts(i) for i in expensive_products])
    db.session.commit()
    
    db.session.add_all( [ NoChangeProducts(i) for i in non_food_items])
    db.session.commit()
   
    db.session.add_all( [ NonFoodProducts(i) for i in no_change])
    db.session.commit()

    print(NonFoodProducts.query.all())
    print(CheapProducts.query.all())
    print(NoChangeProducts.query.all())
    # print((NoChangeProducts.query.all())))
    print(type(NoChangeProducts.query.all()[0].name))

    print(ExpensiveProducts.query.all())

    print(CleanDf.query.all())




    # with open("dashapp/ecommerce/data_files/cheap.txt","w") as f:
    #     for i in cheap_products:
    #         f.write(i+"\n")

    # with open("dashapp/ecommerce/data_files/expensive.txt","w") as f:
    #     for i in expensive_products:
    #         f.write(i+"\n")

    # with open("dashapp/ecommerce/data_files/non_food.txt","w") as f:
    #     for i in non_food_items:
    #         f.write(i+"\n")

    # with open("dashapp/ecommerce/data_files/no_change.txt","w") as f:
    #     for i in no_change:
    #         f.write(i+"\n")


    

def retrieve_and_clean_data():

    db.create_all()

    clean_old_data()

    df = load_from_db()
    modified_df = clean_df(df)    
    process_data(modified_df)

    store_data()


# def testing_api():

#     df = pd.read_csv("dashapp/ecommerce/data_files/clean_df.csv")

#     with open("dashapp/ecommerce/data_files/cheap.txt","r") as f:
#         cheap_testing = f.read().split("\n")[:-1]


  
# def scrape_data():
#     requests.post("e-scrapy.herokuapp.com/schedule.json",)

