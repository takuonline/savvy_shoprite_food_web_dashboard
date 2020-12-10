import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,Output,State
from sqlalchemy import create_engine
from dashapp.ecommerce.models import *
import os


basedir = os.path.abspath(os.path.dirname(__file__))
path = "sqlite:///"+os.path.join(basedir,"../data.sqlite")
cnx = create_engine(path).connect() 


db.create_all()

# fetch cleaned df 
# df = pd.read_csv("dashapp/ecommerce/data_files/clean_df.csv")
df = pd.read_sql("clean_df",cnx)
 
# is very inefficient
# data_dict = {
#     "title":[i.title for i in CleanDf.query.all()],
#     "price":[i.price for i in CleanDf.query.all()],
#     "image_url":[i.image_url for i in CleanDf.query.all()],
#     "date":[i.date for i in CleanDf.query.all()]
# }

# df = pd.DataFrame(data_dict)


df.set_index("title",inplace=True)
df["date"] = pd.to_datetime(df["date"])
df["price"] = df["price"].apply(lambda x: float(x) )
   

# fetch stored processed data
cheap_products = []

expensive_products = []

y_expensive_values = []

y_cheap_values = []


for i in CheapProducts.query.all():
    cheap_products.append(i.name)
    y_cheap_values.append(i.y_value)

for i in ExpensiveProducts.query.all():
    expensive_products.append(i.name)
    y_expensive_values.append(i.y_value)


no_change = [i.name for i in  NoChangeProducts.query.all()]

non_food_items = [i.name for i in  NonFoodProducts.query.all()]

dash_app = dash.Dash(__name__)


# style variables
bg_color_dark = "rgba(0,0,0,.3)"
bg_color_pink = "rgba(220,71,170,.3)"
primary_color = "#6b0f1a"
secondary_color = "#db6ab5"

# demo_url = 'https://www.shoprite.co.za/medias/10129363EA-checkers300Wx300H?context=bWFzdGVyfGltYWdlc3w2MTg4NHxpbWFnZS9wbmd8aW1hZ2VzL2gxMi9oYTcvODk1NTU0MjQwNTE1MC5wbmd8ZmQxODhjNTYxMGRiNTFiZDdjOWFhMTUyY2M4NDNmZjM4MTNkOTlkNTI0MzZhZjVhOTMwY2IzYTIzNDJjYzcyNg'

main_div_bg_style = {
    "background": "linear-gradient(to bottom left, #6b0f1a, #b01268)",
    "width": "100%",
    "height": "100%", 
    "color":"white",
    "fontFamily":"Montserrat, Helvetica"
}

#styles 
side_bar_style = {"backgroundColor":bg_color_dark,
                    "width":"20%",
                    "flex":"1 0 10%",
                    "marginTop":"1rem"
                        }

main_hero_style_row1 = {"display":"flex",
                    "flexWrap":"wrap",
                    "width":"100%",
                    "flex":"1 0 80%"
    
}

main_hero_style = {"display":"flex",
                    "flexWrap":"wrap",
                    "width":"100%",
                    "flex":"1 0 80%"
    
}

graph_and_dropdown_style = { "margin":"1.2rem",
                            "borderRadius": "10%",
                            "display":"flex",
                            "flexDirection":"column",
                            "flex":"4 1 50%"
                        }

dropdown_style = {"padding":"1rem",
                    "color":"black",
                    "marginTop":"1rem",
                    "flexWrap":"wrap",
              }

 
product_image_style = { "flex":"3 1 20%",
                    "display":"inline-block",
                    "backgroundColor":bg_color_dark,
                    "padding":"2rem",
                    "marginTop":"1rem",
                    "marginRight":"1rem",
                    "height":"68%"
}

mini_div_bg_style = {"backgroundColor":secondary_color,
                    "width":"6rem",
                    "height":"6rem",
                    "padding":"1rem 2rem",
                     "borderRadius":"4%",
                     "margin":"1rem"
                    }


# process cheap products
cheap_product_list = []


# for product_name in cheap_products:
    
#     min_value = df[df.index==product_name]["price"].min()
#     max_value = df[df.index==product_name]["price"].max()
#     current_price =  df[df.index==product_name]["price"][-1]
    
#     average_price = (min_value+max_value)/2
    
#     y = (current_price-average_price)*100/average_price
#     y_cheap_values.append(y)
    
cheap_product_list.append(go.Bar(
                                 x=cheap_products,
                                 y=y_cheap_values,
                                #  name=product_name,
                                ))

                            
# process expensive products 
expensive_product_list = []


# for product_name in expensive_products:

#     min_value = df[df.index==product_name]["price"].min()
#     max_value = df[df.index==product_name]["price"].max()
#     current_price =  df[df.index==product_name]["price"][-1]
    
#     average_price = (min_value+max_value)/2
    
#     y = (current_price-average_price)*100/average_price
#     y_expensive_values.append(y)
    


expensive_product_list.append(go.Bar(
                                 x=expensive_products,
                                 y=y_expensive_values,
                                #  name=product_name,
                                ))

# get a combined list of processed data
combined_list = expensive_products + cheap_products + no_change



layout = html.Div(
    [
       
        html.Div( #empty div
            style={
                "paddingTop":"1rem"
            }
        ),

        html.Div( # top navbar header
        html.H1(f"Shoprite Analysis ({len(set(combined_list))} products)",
                style = {
                    "marginLeft":"21rem",
                    "padding":".5rem", 
                    "fontSize":"1.3rem",
                    "margin-bottom": 0
                }
                
               
               ),  style = {
                    "backgroundColor":"rgba(0,0,0,.5)",
                }
            
            
        ),
        
        
        html.Div(
            [
                #side navbar
                html.Div(
                    
                        [
                            
                        html.H1("Shoprite",className="side-navbar-text__header", style={"marginLeft":"1rem",
                                                                                         "margin-top":"3rem"}),

                        html.H3("Food Category",className="side-navbar-text__category",style={"marginLeft":"2rem"}),

                        #  html.H3("Food Category",className="side-navbar-text__category",style={"marginLeft":"2rem"})

                        ],
                className="side-navbar",
                style=side_bar_style
                        ),


                #main hero area
                html.Div(
                    [
                        
                    # row 1   ####################################################    
                        html.Div([ # main hero area row 1 (graph + dropdown + productlist) 
                            
                           
                        #graph and dropdown  div
                        html.Div(
                        [ 
                            
                            
                            #graph only div
                            html.Div([
                                   #graph
                                    dcc.Graph(id="main_graph",), 
                            ],
                            style={#graph div styling
                                
                            }),
 
                            
                            html.Div( #dropdown below the graph div
                            [   dcc.Dropdown(id="dropdown",
                                options=[{'label': i, 'value': i}  for i in combined_list],
                                multi=True,
                               value=df.index[0]
                              )
                                
                            ],style=dropdown_style
                            )
                            
                        ],style=graph_and_dropdown_style
                        ),
                        
                        #product image
                        html.Div(
                        [
                            
                            
                            html.Div(# mini image div bg
                                [
                                    html.H3("Product Image",className="product-image__header",style={"color":"white",
                                                          "fontWeight":900,
                                                           "fontSize":"1.3rem",
                                                           "margin": 0,
                                                           "textAlign": "center"
                                                           
                                                          }),
                                    
                                    html.Img(
                                    id="mini_divs_image",
                                    className="product-image__image",
                                    style={
                                        "width":"100%"
                                    }       
                                            )
                                    
                                ]
                                ,

                            ),
                            
                             
                        ],className="product-image",
                            style=product_image_style
                        
                        ),
                         
                            
                            
                        ],style= main_hero_style_row1),
                        
                        
                        # row 2 ##############################################
                html.Div([ # main hero area row 2 (3 min divs) 
                            
                        
                        html.Div(# outer div  with 3 min div - image,price change
                        [
                            
                             html.Div(# minimum price div bg
                                [
                                    html.H3("Minimum Price",style={"color":"#911145",
                                                          "fontWeight":900,
                                                           "fontSize":"1rem",
                                                           "margin": 0,
                                                           "textAlign": "center",
                                                               
                                                          }),
                                    
                                    html.P(id="mini_divs_min_price",style={"color":"white",
                                                       "fontWeight":900,
                                                        "fontSize":"1.5rem",
                                                         "textAlign": "center",
                                                        "margin":".7rem"
                                                        
                                                       })
                                    
                                ]
                                ,
                                style=mini_div_bg_style
                            ),
                            
                            
                            
                            
                            
                            
                            
                            
                             html.Div(# mini price div bg
                                [
                                    html.H3("Maximum Price",style={"color":"#911145",
                                                          "fontWeight":900,
                                                           "fontSize":"1rem",
                                                           "margin": 0,
                                                           "textAlign": "center",
                                                               
                                                          }),
                                    
                                    html.P(id="mini_divs_max_price",style={"color":"white",
                                                       "fontWeight":900,
                                                        "fontSize":"1.5rem",
                                                         "textAlign": "center",
                                                        "margin":".7rem"
                                                        
                                                       })
                                    
                                ]
                                ,
                                style=mini_div_bg_style
                            ),
                            
                            
                             html.Div(# mini change div bg
                                [
                                    html.H3("Average Price",style={"color":"#911145",
                                                          "fontWeight":900,
                                                           "fontSize":"1rem",
                                                           "margin": 0,
                                                           "textAlign": "center",
                                                          
                                                          }
                                           ),
                                    
                                    html.P(id="mini_divs_average_price",style={
                                                        "color":"white",
                                                        "fontWeight":900,
                                                        "fontSize":"1.5rem",
                                                        "textAlign": "center",
                                                        "margin":".7rem" 
                                                                               }
                                          )
                                    
                                ]
                                ,
                                style=mini_div_bg_style
                            ),
                            
                         ],style={ #out div to 3 mini divs
                            "display":"flex",
                            "justifyContent":"space-around",
                            "alignItems":"center",
                            "flexWrap":"wrap",
                            "marginLeft":"1rem"
                            
                        }
                        
                        )
                        
                         ]),
                        
                      
                        #row 3 ############################################################################################
                        
                        html.Div([
                            
                            #row 3 bg
                            html.Div([
                                html.Div(# header
                                     html.P(f"Best buys ({len(cheap_products)} products)",
                                           style={
                                                 "margin": 0
                                           }),
                                    style={
                                        "backgroundColor":secondary_color,
                                        "padding":".7rem",
                                       
                                    }
                                ),
                                
                                
                                dcc.Graph(
                                    id = "mini-bar-1",
                                figure={

                                    "data":cheap_product_list,
                                      "layout": go.Layout(title="Price decrease",
                                                        plot_bgcolor="rgba(0,0,0,0)",
                                                        paper_bgcolor="rgba(0,0,0,0)",
                                                        font={"color":"white",},
                                                        grid={"columns":1,},
                                                        hovermode="closest",
                                                        # xaxis={
                                                        #     "title":"Product Names"
                                                        # },
                                                        yaxis={
                                                            "title": "Price decrease in Percentage"
                                                        }
                                                        )
                                     }
                                        )
                            ],style={
                                "flex":" 1 0 45%",
                                "margin":"1rem",
                            }),
                            
                            
                            html.Div([
                                html.Div(# header
                                    html.P(f"Worst buys ({len(expensive_products)} products)",
                                           style={
                                                 "margin": 0
                                           }),
                                    style={
                                        "backgroundColor":secondary_color,
                                        "padding":".7rem",
                                        
                                    }
                                ),
                                
                                 dcc.Graph(
                                    id = "mini-bar-2",
                                figure={
                                    "data":expensive_product_list,
                                      "layout": go.Layout(title="Price increase",
                                                        plot_bgcolor="rgba(0,0,0,0)",
                                                        paper_bgcolor="rgba(0,0,0,0)",
                                                        font={"color":"white",},
                                                        grid={"columns":1,},
                                                        hovermode="closest",
                                                        # xaxis={
                                                        #     "title":"Product Names"
                                                        # },
                                                        yaxis={
                                                            "title": "Price increase in Percentage"
                                                                }

                                                        )
                               
                                        }
                                            )
                                
                                
                            ],style={
                                "flex":" 1 0 45%",
                                "margin":"1rem",
                                "marginLeft":0
                            }),
                            
                         
                            
                        ],style = {# best and worst rows
                            "display":"flex",
                            "width": "100%",
                            "backgroundColor":bg_color_dark,
                            "padding":"1rem",
                            "margin":"1rem",
                            "marginTop":0
                           
                                }
                        ),


                        html.P("Made with ❤ by Takudzwa Makusha(tbmakusha@gmail.com)",style={
                            "color":"white",
                            "fontSize":"14px",
                            "textAlign":"center",
                            "marginLeft":"1rem",
                            "display":"inline-block"


                        }),

                       html.A(" (Github_repo)",
                           href="https://github.com/takuonline/shoprite_food",
                           style={
                               "color":"yellow",
                               "textDecoration":"none",
                               "alignSelf":"center",
                               "fontSize":"14px",
                               "marginLeft":"1rem"
                           }
                       )
                        
                        
                        # row 4 ############################################################################################
                        
                        
                        # html.Div(
                        #     [
                        #         dcc.Graph(
                                
                        #         figure = {
                        #             "data":bubble_product_list,
                        #             # "data":[go.Scatter(x=[1,2,3,4],y=[3,5,8,9],mode="markers",marker={"size":[20,50,130,200]})],
                        #              "layout": go.Layout(title="Bubble plot",
                        #                                 plot_bgcolor="rgba(0,0,0,0)",
                        #                                 paper_bgcolor="rgba(0,0,0,0)",
                        #                                 font={"color":"white",},
                        #                                 grid={"columns":1,},
                        #                                 hovermode="closest"
                        #                                 )
                                
                        #         }
                        #         )
                        #     ],style={"backgroundColor":"#dc47aa",
                        #             "marginLeft":"1rem"
                        #             })
                    ],
                style=main_hero_style
                )

    
            ],
        style={ #div containing the side bar and main hero area
                "display":"flex",

                }
            )
          
],style=main_div_bg_style
)


@dash_app.callback(Output("main_graph","figure"),
             [Input("dropdown","value")])
def select_product_graph(product_list):
    
    if len(product_list)==1:
        product_title = product_list[0]
    else:
        product_title = ""
        
    return {
        "data": [  go.Scatter(x=df[df.index==product_name]["date"],
                              y=df[df.index==product_name]["price"],
#                               fillcolor="rgba(255,0,0,.3)",
                              name=product_name,
                          
                             ) for product_name in product_list  ],
        
        "layout": go.Layout(title=product_title,
                            plot_bgcolor="rgba(0,0,0,0)",
                            paper_bgcolor="rgba(0,0,0,.3)",
                            font={"color":"white",},
                            grid={"columns":1,},
                            hovermode="closest"
                            
                            )
        }

# if __name__=="__main__":
#     dash_app.run_server(
#     debug=True,
#     dev_tools_hot_reload=True,
#     # use_reloader=False # to use in jupyter
# )
