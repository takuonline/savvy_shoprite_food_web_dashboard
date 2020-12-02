# from wsgi import db

from dashapp import db
#####################################

# temp = []

# def set_db(database):

#     # global db

#     temp.append(database)
    

# db=temp[0]

class CheapProducts(db.Model):

    __tablename__ = "cheap_products"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    y_value = db.Column(db.Float)

    def __init__(self,name,y_value):
        self.name = name
        self.y_value = y_value

    def __repr__(self):
        return f"{self.name},{self.y_value}"



class ExpensiveProducts(db.Model):

    __tablename__ = "expensive_products"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    y_value = db.Column(db.Float)

    def __init__(self,name,y_value):
        self.name = name
        self.y_value = y_value

    def __repr__(self):
        return f"{self.name}"


class NoChangeProducts(db.Model):

    __tablename__ = "no_change_products"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return f"{self.name}"


class NonFoodProducts(db.Model):

    __tablename__ = "non_food_products"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return f"{self.name}"



class CleanDf(db.Model):

    __tablename__ = "clean_df"

    # id = db.Column(db.Text,primary_key=True)
    title = db.Column(db.Text)
    image_url = db.Column(db.Text)
    date = db.Column(db.Text,primary_key=True)
    price = db.Column(db.Float)


    def __init__(self,title,price,image_url,date):
        # self.id = id
        self.title = title
        self.image_url = image_url
        self.date = date
        self.price = price

    def __repr__(self):
        return f"{self.title}, {self.image_url}, {self.date}, {self.price} \n"



# class NonFoodProducts(db.Model):

#     __tablename__ = "non_food_products"

#     id = db.Column(db.Integer,primary_key=True)
#     name = db.Column(db.Text)

#     def __init__(self,name):
#         self.name = name

#     def __repr__(self):
#         return f"{self.name}"