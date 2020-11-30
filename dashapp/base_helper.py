import pandas as pd
import pymongo
import os
# import requests


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
    df.to_csv("dashapp/ecommerce/data_files/clean_df.csv")
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
        
def store_data():
  
    # store classified data
    with open("dashapp/ecommerce/data_files/cheap.txt","w") as f:
        for i in cheap_products:
            f.write(i+"\n")

    with open("dashapp/ecommerce/data_files/expensive.txt","w") as f:
        for i in expensive_products:
            f.write(i+"\n")

    with open("dashapp/ecommerce/data_files/non_food.txt","w") as f:
        for i in non_food_items:
            f.write(i+"\n")

    with open("dashapp/ecommerce/data_files/no_change.txt","w") as f:
        for i in no_change:
            f.write(i+"\n")


    

def retrieve_and_clean_data():
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

