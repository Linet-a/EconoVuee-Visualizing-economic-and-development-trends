from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.data import gapminder

# External Bootstrap CSS
external_stylesheets = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css"]

# Initialize app
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Load dataset
df = gapminder(datetimes=True, centroids=True, pretty_names=True)
df["Year"] = df.Year.dt.year

# Dropdown options
continents = [{'label': c, 'value': c} for c in df['Continent'].unique()]
years = [{'label': str(y), 'value': y} for y in sorted(df['Year'].unique())]

# --- Chart Functions ---

def create_table():
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns), align='left'),
        cells=dict(values=[df[col] for col in df.columns], align='left')
    )])
    fig.update_layout(paper_bgcolor='#e5ecf6', margin=dict(t=0, l=0, r=0, b=0), height=700)
    return fig

def create_pop_chart(continent='Europe', year=1952):
    filtered = df[(df['Continent'] == continent) & (df['Year'] == year)]
    filtered = filtered.sort_values(by='Population', ascending=False).head(15)
    fig = px.bar(filtered, x='Country', y='Population', color='Country',
                 title=f'Top 15 Populations in {continent} ({year})', text_auto=True)
    fig.update_layout(paper_bgcolor='#e5ecf6', height=600)
    return fig

def create_gdp_chart(continent='Europe', year=1952):
    filtered = df[(df['Continent'] == continent) & (df['Year'] == year)]
    filtered = filtered.sort_values(by='GDP per Capita', ascending=False).head(15)
    fig = px.bar(filtered, x='Country', y='GDP per Capita', color='Country',
                 title=f'Top 15 GDP per Capita in {continent} ({year})', text_auto=True)
    fig.update_layout(paper_bgcolor='#e5ecf6', height=600)
    return fig

def create_lifeexp_chart(continent='Europe', year=1952):
    filtered = df[(df['Continent'] == continent) & (df['Year'] == year)]
    filtered = filtered.sort_values(by='Life Expectancy', ascending=False).head(15)
    fig = px.bar(filtered, x='Country', y='Life Expectancy', color='Country',
                 title=f'Top 15 Life Expectancies in {continent} ({year})')
    fig.update_layout(paper_bgcolor='#e5ecf6', height=600)
    return fig

def create_choropleth_map(variable='Life Expectancy', year=1952):
    filtered = df[df['Year'] == year]
    fig = px.choropleth(filtered, color=variable,
                        locations='ISO Alpha Country Code', locationmode='ISO-3',
                        hover_name='Country', hover_data=[variable],
                        color_continuous_scale='RdYlBu',
                        title=f'{variable} Choropleth Map ({year})')
    fig.update_layout(dragmode=False, paper_bgcolor='#e5ecf6', height=600, margin=dict(l=0, r=0))
    return fig

# --- Layout ---
app.layout = html.Div([
    html.Div([
        html.H1("Economic & Development Trends", className='text-center fw-bold my-3'),

        dcc.Tabs([
            dcc.Tab(label='Dataset', children=[
                html.Br(),
                dcc.Graph(figure=create_table())
            ]),

            dcc.Tab(label='Population', children=[
                html.Br(), html.Label("Continent:"), dcc.Dropdown(id='cont_pop', options=continents, value='Africa', clearable=False),
                html.Label("Year:"), dcc.Dropdown(id='year_pop', options=years, value=1952, clearable=False),
                html.Br(),
                dcc.Graph(id='population')
            ]),

            dcc.Tab(label='GDP Per Capita', children=[
                html.Br(), html.Label("Continent:"), dcc.Dropdown(id='cont_gdp', options=continents, value='Africa', clearable=False),
                html.Label("Year:"), dcc.Dropdown(id='year_gdp', options=years, value=1952, clearable=False),
                html.Br(),
                dcc.Graph(id='gdp')
            ]),

            dcc.Tab(label='Life Expectancy', children=[
                html.Br(), html.Label("Continent:"), dcc.Dropdown(id='cont_life_exp', options=continents, value='Africa', clearable=False),
                html.Label("Year:"), dcc.Dropdown(id='year_life_exp', options=years, value=1952, clearable=False),
                html.Br(),
                dcc.Graph(id='life_exp')
            ]),

            dcc.Tab(label='Choropleth Map', children=[
                html.Br(), html.Label("Variable:"), dcc.Dropdown(id='var_map', options=[
                    {'label': 'Population', 'value': 'Population'},
                    {'label': 'GDP per Capita', 'value': 'GDP per Capita'},
                    {'label': 'Life Expectancy', 'value': 'Life Expectancy'},
                ], value='Life Expectancy', clearable=False),
                html.Label("Year:"), dcc.Dropdown(id='year_map', options=years, value=1952, clearable=False),
                html.Br(),
                dcc.Graph(id='choropleth_map')
            ]),
        ])
    ], className='col-10 mx-auto')
], style={'background-color': '#e5ecf6', 'minHeight': '100vh'})

# --- Callbacks ---
@callback(Output('population', 'figure'), [Input('cont_pop', 'value'), Input('year_pop', 'value')])
def update_population_chart(continent, year):
    return create_pop_chart(continent, year)

@callback(Output('gdp', 'figure'), [Input('cont_gdp', 'value'), Input('year_gdp', 'value')])
def update_gdp_chart(continent, year):
    return create_gdp_chart(continent, year)

@callback(Output('life_exp', 'figure'), [Input('cont_life_exp', 'value'), Input('year_life_exp', 'value')])
def update_life_chart(continent, year):
    return create_lifeexp_chart(continent, year)

@callback(Output('choropleth_map', 'figure'), [Input('var_map', 'value'), Input('year_map', 'value')])
def update_map(variable, year):
    return create_choropleth_map(variable, year)

# --- Run app ---
if __name__ == '__main__':
    app.run(debug=True)


    