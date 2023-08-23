import dash
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

load_figure_template("minty")

df_data = pd.read_csv("supermarket_sales.csv")
df_data["Date"] = pd.to_datetime(df_data["Date"])

app = dash.Dash(
    external_stylesheets=[dbc.themes.MINTY]
)

# =========  Layout  =========== #
app.layout = html.Div(children=[

                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            html.H2("CM PARTNERS", style={"font-family":"Voltaire", "font-size":"60px"}),

                            html.Hr(),

                            html.H5("Cidades:",style={"margin-top":"30px"}),
                            dcc.Checklist((df_data["City"].value_counts().index),
                                          df_data["City"].value_counts().index,id="check_city",
                                          inputStyle={"margin-right":"5px"}
                            ),

                            html.H5("Variável de análise",style={"margin-top":"30px"}),
                            dcc.RadioItems(["gross income", "Rating"], "gross income", id="main_variable")
                        ], style={"height":"100vh", "margin":"20px", "padding":"20px"})
                    ], sm=3),

                    dbc.Col([
                        dbc.Row([
                           dbc.Label("Gráficos",style={"text-align":"center","font-size":"50px","margin-top":"10px","color":"#000"}),
                           dbc.Col([dcc.Graph(id="city_fig")],style={"margin-top":"80px"}, sm=4),
                           dbc.Col([dcc.Graph(id="payment_fig")],style={"margin-top":"80px"}, sm=4),
                           dbc.Col([dcc.Graph(id="gender_fig")], sm=4)
                        ]),

                        dbc.Row([
                            dcc.Graph(id="income_per_date_fig")
                        ]),

                        dbc.Row([
                            dcc.Graph(id="income_per_product_fig")
                        ])

                    ],sm=9)
                ])

])


# =========  Callback  =========== #
@app.callback(
     [
     Output('city_fig', 'figure'),
     Output('payment_fig', 'figure'),
     Output('gender_fig', 'figure'),
     Output('income_per_date_fig', 'figure'),
     Output('income_per_product_fig', 'figure')
     ],

    [
        Input('check_city', 'value'),
        Input('main_variable', 'value')
    ])

def render_graphs(cities, main_variable):
    operation = np.sum if main_variable == "gross income" else np.mean

    df_filtered = df_data[df_data["City"].isin(cities)]

    df_city = df_filtered.groupby("City")[main_variable].apply(operation).to_frame().reset_index()
    df_payment = df_filtered.groupby(["Payment"])[main_variable].apply(operation).to_frame().reset_index()
    df_gender = df_filtered.groupby(["Gender"])[main_variable].apply(operation).to_frame().reset_index()

    df_income_time = df_filtered.groupby("Date")[[main_variable]].apply(operation).reset_index()
    df_product_income = df_filtered.groupby(["Product line", "City"])[[main_variable]].apply(operation).reset_index()



    fig_city = px.bar(df_city, x="City", y=main_variable, color="City")
    fig_payment = px.bar(df_payment, y="Payment", x=main_variable, orientation="h", color="Payment")
    fig_gender = px.bar(df_gender, y="Gender", x=main_variable,color="Gender", barmode="group")
    fig_income_data = px.bar(df_income_time, y=main_variable, x="Date")
    fig_product_income = px.bar(df_product_income,x=main_variable, y="Product line", orientation="h", barmode="group", color="City")



    fig_city.update_layout(margin=dict(l=0, r=20, t=20, b=20), height=200, template="minty")
    fig_payment.update_layout(margin=dict(l=0, r=20, t=20, b=20), height=200, template="minty")
    fig_income_data.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=150, template="minty")
    fig_product_income.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=350)

    return fig_city, fig_payment, fig_gender,fig_income_data, fig_product_income

if __name__ == "__main__":
    app.run_server(debug=True)