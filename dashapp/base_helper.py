import pandas as pd
import pymongo
import os
from dashapp.ecommerce.models  import *
# from wsgi import db
import dashapp
from sqlalchemy import create_engine

# db_username = os.environ.get("USER")
# db_password = os.environ.get("PASSWORD")
db_username = "takuonline"
db_password = "tablmak11"
#process data into different classes

cheap_products = []

expensive_products = []

no_change = []

non_food_items = []

y_expensive_values = []

y_cheap_values = []
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
    
    df["date"] = pd.to_datetime(df["date"])
    df["price"] = df["price"].apply(
        lambda x: float((x.strip()).replace(",", "").replace("R", "").split()[-1])
    )
    df["date_only"] = df["date"].dt.date

    df = df.drop_duplicates(subset = ["title",'date_only'], keep = 'last')
    df.drop(["date_only","_id"], axis=1,inplace=True)

    # store df
    # df.to_csv("dashapp/ecommerce/data_files/clean_df.csv")

    basedir = os.path.abspath(os.path.dirname(__file__))
    path = "sqlite:///" + os.path.join(basedir,"data.sqlite")
    cnx = create_engine(path).connect() 

    df.set_index("title",inplace=True)
    # df.drop("_id",inplace=True,axis=1)
    df.to_sql("clean_df",cnx,if_exists="replace")

    return df

def process_data(df):
   
    #classify data into cheap, expensive , non food items and the no change classes
    for item_name in df.index.unique():
        count = df[df.index == item_name]["price"].count()
        mean = df[df.index == item_name]["price"].mean()
        last_figure = df[df.index == item_name]["price"][-1]
        # try:
        #     second_from_last_figure = df[df.index == item_name]["price"][-2]
        # except IndexError:
        #     second_from_last_figure=last_figure

            
        
    # 7 is an abitrary number, this number can be anything but it need to bew a low value until
    # This part of the code can be removed only after all the non food items have been deleted from the mongodb database
        if(count < 7):
            non_food_items.append(item_name) 
        else:        
            if (last_figure < mean):
                # cheap
                cheap_products.append(item_name)

            elif (last_figure == mean):
                #no change
                no_change.append(item_name)

            elif (last_figure > mean):
                #expensive
                expensive_products.append(item_name)

            else:
                #non food item
                non_food_items.append(item_name)


def further_processing(df):
    # computes the min , max , average price for each unique item
    # these values are used for the y coordinate for the bar graph
   

    for product_name in cheap_products:
    
        # min_value = df[df.index==product_name]["price"].min()
        # max_value = df[df.index==product_name]["price"].max()

        current_price = df[df.index==product_name]["price"][-1]

        # if (type(current_price) != float ):
        #     current_price = df[df.index==product_name]["price"][-2]

        #     if (type(current_price) != float ):
        #         current_price = df[df.index==product_name]["price"][-3]

        #         if (type(current_price) != float ):
        #             current_price = df[df.index==product_name]["price"].mean()
                    
        average_price = df[df.index==product_name]["price"].mean()

        y = (current_price-average_price)*100/average_price

       

        y_cheap_values.append(y)


    for product_name in expensive_products:

        # min_value = df[df.index==product_name]["price"].min()
        # max_value = df[df.index==product_name]["price"].max()
        current_price =  df[df.index==product_name]["price"][-1]

        # if (type(current_price) != float ):
        #     current_price = df[df.index==product_name]["price"][-2]

        #     if (type(current_price) != float ):
        #         current_price = df[df.index==product_name]["price"][-3]

        #         if (type(current_price) != float ):
        #             current_price = df[df.index==product_name]["price"].mean()


        # previous_price = df[df.index==product_name]["price"][-2]
      
        average_price = df[df.index==product_name]["price"].mean()
        
        # y = (current_price-average_price)*100/average_price
        y = (current_price-average_price)*100/average_price


        y_expensive_values.append(y)





        
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

    db.session.add_all( [ CheapProducts(i,j) for i,j in zip(cheap_products,y_cheap_values)])
    db.session.commit()

    db.session.add_all( [ ExpensiveProducts(i,j) for i,j in zip(expensive_products,y_expensive_values)])
    db.session.commit()
    
    db.session.add_all( [ NoChangeProducts(i) for i in non_food_items])
    db.session.commit()
   
    db.session.add_all( [ NonFoodProducts(i) for i in no_change])
    db.session.commit()



def retrieve_and_clean_data():

    db.create_all()

    df = load_from_db()

    clean_old_data()

    modified_df = clean_df(df)    

    process_data(modified_df)

    further_processing(modified_df)

    store_data()


# def testing_api():

#     df = pd.read_csv("dashapp/ecommerce/data_files/clean_df.csv")

#     with open("dashapp/ecommerce/data_files/cheap.txt","r") as f:
#         cheap_testing = f.read().split("\n")[:-1]


  
# def scrape_data():
#     requests.post("e-scrapy.herokuapp.com/schedule.json",)

