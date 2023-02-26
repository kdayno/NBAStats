from dash import html
import dash

dash.register_page(__name__, name='Page Not Found')

layout = html.Div(children=[
    html.H1("OOPS! PAGE NOT FOUND"),
    html.H2("WE ARE SORRY, BUT THE PAGE YOU REQUESTED WAS NOT FOUND")
], className='error-page')
