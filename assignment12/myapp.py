
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.data as pldata
import pandas as pd

# Load gapminder dataset
df = pldata.gapminder()

# Get unique countries
countries = df['country'].drop_duplicates().sort_values()


app = dash.Dash(__name__)
server = app.server  # For Render.com deployment

app.layout = html.Div([
	html.H1('GDP Per Capita Growth by Country'),
	dcc.Dropdown(
		id='country-dropdown',
		options=[{'label': c, 'value': c} for c in countries],
		value='Canada',
		clearable=False
	),
	dcc.Graph(id='gdp-growth')
])

@app.callback(
	Output('gdp-growth', 'figure'),
	Input('country-dropdown', 'value')
)
def update_graph(selected_country):
	filtered = df[df['country'] == selected_country]
	fig = px.line(
		filtered,
		x='year',
		y='gdpPercap',
		title=f'GDP Per Capita Growth: {selected_country}',
		labels={'gdpPercap': 'GDP Per Capita', 'year': 'Year'}
	)
	return fig

if __name__ == "__main__":
	app.run(debug=True)
