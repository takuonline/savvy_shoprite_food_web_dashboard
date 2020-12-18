import dash
from dashapp.ecommerce.base import layout,df
from dash.dependencies import Input,Output,State
import plotly.graph_objects as go
import pandas as pd

def create_dashboard(server):

    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashapp/",
    )
    dash_app.layout = layout

    create_callbacks(dash_app)

    return dash_app.server


def create_callbacks(dash_app):


    @dash_app.callback(Output("main_graph","figure"),
                [Input("dropdown","value")])
    def select_product_graph(product_list):
        
        if len(product_list)==1:
            product_title = product_list[0]
        else:
            product_title = ""

        data_graph = [  go.Scatter(x=df[df.index==product_name]["date"],
                                y=df[df.index==product_name]["price"],
    #                               fillcolor="rgba(255,0,0,.3)",
                                name=product_name,
                                mode="lines"
                            
                                ) for product_name in product_list  ]

    #     mean_graph = [  go.Scatter(x=df[df.index==product_name]["date"],
    #                             y=df[df.index==product_name]["price"].mean(),
    # #                               fillcolor="rgba(255,0,0,.3)",
    #                             name=product_name,
    #                             mode="lines"
                            
    #                             ) for product_name in product_list  ]
            
        return {
            "data":  data_graph   ,
            
            "layout": go.Layout(title=product_title,
                                plot_bgcolor="rgba(0,0,0,0)",
                                paper_bgcolor="rgba(0,0,0,.3)",
                                font={"color":"white",},
                                grid={"columns":1,},
                                hovermode="closest"
                                
                                )
            }


    @dash_app.callback(Output("mini_divs_image","src"),
                [Input("dropdown","value")])
    def select_product_image(product_list):
        
        if (len(product_list)>0 and len(df[df.index==product_list[-1]]["image_url"])>0 ):
            url = df[df.index==product_list[-1]]["image_url"][0] 
        else:
            url=""
        
        return url



    @dash_app.callback(Output("mini_divs_min_price","children"),
                [Input("dropdown","value")])
    def select_product_min_price(product_list):
        
        if (len(product_list)>0):
            min_price = df[df.index==product_list[-1]]['price'].min()
        else:
            min_price=0  
        

        return f"R{min_price}"


    @dash_app.callback(Output("mini_divs_max_price","children"),
                [Input("dropdown","value")])
    def select_product_max_price(product_list):
        
        if (len(product_list)>0):
            max_price = df[df.index==product_list[-1]]['price'].max()
        else:
            max_price=0
        

        return f"R{max_price}"


    @dash_app.callback(Output("mini_divs_average_price","children"),
                [Input("dropdown","value")])
    def select_product_average_price(product_list):
        
        if (len(product_list)>0):
            # max_price = df[df.index==product_list[-1]]['price'].max()
            # min_price = df[df.index==product_list[-1]]['price'].min()
            # av_price = round((max_price+min_price)/2,2)
            av_price = round(df[df.index==product_list[-1]]['price'].mean(),2)
        else:
            av_price="-"

        return f"R{av_price}"




    