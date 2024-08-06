import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import plotly.io as pio

# Set default plotly color scale
pio.templates.default = "plotly_white"

# Load dataset
df = pd.read_csv("jobs_in_data 3.csv") 

# Initialize Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Interactive Data Science Job Salaries Dashboard"),

    # Theme Switcher
    html.Label("Select Theme"),
    dcc.RadioItems(
        id='theme-radio',
        options=[
            {'label': 'Light', 'value': 'plotly_white'},
            {'label': 'Dark', 'value': 'plotly_dark'}
        ],
        value='plotly_white'
    ),

    # Dropdown for Job Title
    html.Label("Select Job Title"),
    dcc.Dropdown(
        id='job-title-dropdown',
        options=[{'label': job, 'value': job} for job in df['job_title'].unique()],
        value=['Data Scientist'],
        multi=True
    ),

    # Dropdown for Experience Level
    html.Label("Select Experience Level"),
    dcc.Dropdown(
        id='experience-level-dropdown',
        options=[{'label': level, 'value': level} for level in df['experience_level'].unique()],
        value=['Senior'],
        multi=True
    ),

    # Dropdown for Employment Type
    html.Label("Select Employment Type"),
    dcc.Dropdown(
        id='employment-type-dropdown',
        options=[{'label': emp_type, 'value': emp_type} for emp_type in df['employment_type'].unique()],
        value=['Full-time'],
        multi=True
    ),

    # Dropdown for Company Size
    html.Label("Select Company Size"),
    dcc.Dropdown(
        id='company-size-dropdown',
        options=[{'label': size, 'value': size} for size in df['company_size'].unique()],
        value=['M'],
        multi=True
    ),

    # Multi-Select Dropdown for Job Category
    html.Label("Select Job Categories"),
    dcc.Dropdown(
        id='job-category-dropdown',
        options=[{'label': category, 'value': category} for category in df['job_category'].unique()],
        value=['Data Science and Research'],
        multi=True
    ),

    # Slider for Salary Range
    html.Label("Select Salary Range"),
    dcc.RangeSlider(
        id='salary-slider',
        min=df['salary_in_usd'].min(),
        max=df['salary_in_usd'].max(),
        step=5000,
        marks={i: f'${i}' for i in range(int(df['salary_in_usd'].min()), int(df['salary_in_usd'].max()) + 1, 20000)},
        value=[df['salary_in_usd'].min(), df['salary_in_usd'].max()]
    ),

    # Slider for Work Years
    html.Label("Select Work Year Range"),
    dcc.RangeSlider(
        id='work-year-slider',
        min=df['work_year'].min(),
        max=df['work_year'].max(),
        step=1,
        marks={i: str(i) for i in range(int(df['work_year'].min()), int(df['work_year'].max()) + 1)},
        value=[df['work_year'].min(), df['work_year'].max()]
    ),

    # Checkbox for Filtering by Currency
    html.Label("Filter by Currency"),
    dcc.Checklist(
        id='currency-checklist',
        options=[{'label': currency, 'value': currency} for currency in df['salary_currency'].unique()],
        value=['USD']
    ),

    # Bar Chart
    dcc.Graph(id='bar-chart'),

    # Scatter Plot
    dcc.Graph(id='scatter-plot'),

    # Box Plot
    dcc.Graph(id='box-plot'),

    # Pie Chart
    dcc.Graph(id='pie-chart'),

    # Histogram
    dcc.Graph(id='histogram'),

    # Sunburst Chart
    dcc.Graph(id='sunburst'),

    # Line Chart
    dcc.Graph(id='line-chart'),

    # Heatmap
    dcc.Graph(id='heatmap'),

    # Parallel Coordinates Plot
    dcc.Graph(id='parallel-coordinates'),

    # Correlation Matrix
    dcc.Graph(id='correlation-matrix'),

    # Map Visualization for Salary by Location
    dcc.Graph(id='map-visualization'),

    # Pie Chart for Employment Type Distribution
    dcc.Graph(id='employment-type-pie-chart'),

    # Interactive Table
    html.Label("Data Table"),
    dcc.Graph(id='data-table'),

    # Trend Analysis Chart
    html.Label("Trend Analysis"),
    dcc.Dropdown(
        id='trend-dropdown',
        options=[
            {'label': 'Salary by Job Title', 'value': 'job_title'},
            {'label': 'Salary by Company Location', 'value': 'company_location'}
        ],
        value='job_title'
    ),
    dcc.Graph(id='trend-analysis-chart'),

    # Hypothesis Testing
    html.Label("Hypothesis Testing"),
    dcc.Dropdown(
        id='hypothesis-dropdown',
        options=[
            {'label': 'Salary vs Experience Level', 'value': 'salary_experience'},
            {'label': 'Salary vs Job Title', 'value': 'salary_job'},
            {'label': 'Salary vs Company Size', 'value': 'salary_company_size'}
        ],
        value='salary_experience'
    ),
    dcc.Graph(id='hypothesis-plot')
])

# Callback to update charts based on filters
@app.callback(
    [Output('bar-chart', 'figure'),
     Output('scatter-plot', 'figure'),
     Output('box-plot', 'figure'),
     Output('pie-chart', 'figure'),
     Output('histogram', 'figure'),
     Output('sunburst', 'figure'),
     Output('line-chart', 'figure'),
     Output('heatmap', 'figure'),
     Output('parallel-coordinates', 'figure'),
     Output('correlation-matrix', 'figure'),
     Output('map-visualization', 'figure'),
     Output('employment-type-pie-chart', 'figure'),
     Output('data-table', 'figure'),
     Output('trend-analysis-chart', 'figure'),
     Output('hypothesis-plot', 'figure')],
    [Input('job-title-dropdown', 'value'),
     Input('experience-level-dropdown', 'value'),
     Input('employment-type-dropdown', 'value'),
     Input('company-size-dropdown', 'value'),
     Input('job-category-dropdown', 'value'),
     Input('salary-slider', 'value'),
     Input('work-year-slider', 'value'),
     Input('currency-checklist', 'value'),
     Input('theme-radio', 'value'),
     Input('trend-dropdown', 'value'),
     Input('hypothesis-dropdown', 'value')]
)
def update_charts(selected_job_titles, selected_experience_levels, selected_employment_types,
                   selected_company_sizes, selected_job_categories, selected_salary_range,
                   selected_work_year_range, selected_currencies, selected_theme,
                   selected_trend, selected_hypothesis):
    
    # Filter dataset based on selections
    filtered_df = df[
        (df['job_title'].isin(selected_job_titles)) &
        (df['experience_level'].isin(selected_experience_levels)) &
        (df['employment_type'].isin(selected_employment_types)) &
        (df['company_size'].isin(selected_company_sizes)) &
        (df['job_category'].isin(selected_job_categories)) &
        (df['salary_in_usd'] >= selected_salary_range[0]) &
        (df['salary_in_usd'] <= selected_salary_range[1]) &
        (df['work_year'] >= selected_work_year_range[0]) &
        (df['work_year'] <= selected_work_year_range[1]) &
        (df['salary_currency'].isin(selected_currencies))
    ]

    # Apply theme
    pio.templates.default = selected_theme

    # Bar Chart: Average salary by job title
    bar_chart = px.bar(filtered_df, x='job_title', y='salary_in_usd', title='Average Salary by Job Title')

    # Scatter Plot: Salary vs Experience Level, colored by Location
    scatter_plot = px.scatter(filtered_df, x='experience_level', y='salary_in_usd', color='employee_residence', title='Salary vs. Experience Level')

    # Box Plot: Salary distribution by location
    box_plot = px.box(filtered_df, x='company_location', y='salary_in_usd', title='Salary Distribution by Location')

    # Pie Chart: Distribution of job titles
    pie_chart = px.pie(filtered_df, names='job_title', title='Distribution of Job Titles')

    # Histogram: Salary distribution
    histogram = px.histogram(filtered_df, x='salary_in_usd', title='Salary Distribution')

    # Sunburst Chart: Salary by Job Title and Location
    sunburst = px.sunburst(filtered_df, path=['job_title', 'company_location'], values='salary_in_usd', title='Salary by Job Title and Location')

    # Line Chart: Salary trends over years
    line_chart = px.line(filtered_df, x='work_year', y='salary_in_usd', color='job_title', title='Salary Trends Over Years')

    # Heatmap: Salary by Job Title and Location
    heatmap = px.density_heatmap(filtered_df, x='job_title', y='company_location', z='salary_in_usd', title='Salary by Job Title and Location')

    # Parallel Coordinates Plot: Multidimensional data visualization
    parallel_coordinates = px.parallel_coordinates(filtered_df, color='salary_in_usd',
                                                   dimensions=['work_year', 'experience_level', 'company_size'],
                                                   title='Parallel Coordinates Plot')

    # Correlation Matrix
    corr_matrix = filtered_df[['salary_in_usd', 'work_year']].corr()
    correlation_matrix = go.Figure(data=go.Heatmap(z=corr_matrix.values,
                                                  x=corr_matrix.columns,
                                                  y=corr_matrix.index,
                                                  colorscale='Viridis'),
                                   layout=go.Layout(title='Correlation Matrix'))

    # Map Visualization: Salary by Location
    map_visualization = px.scatter_geo(filtered_df, locations='company_location', size='salary_in_usd',
                                      title='Salary by Location')

    # Pie Chart: Employment Type Distribution
    employment_type_pie_chart = px.pie(filtered_df, names='employment_type', title='Employment Type Distribution')

    # Interactive Table: Display detailed data
    data_table = go.Figure(data=[go.Table(
        header=dict(values=list(filtered_df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[filtered_df[col] for col in filtered_df.columns],
                   fill_color='lavender',
                   align='left'))
    ], layout=go.Layout(title='Data Table'))

    # Trend Analysis Chart
    if selected_trend == 'job_title':
        trend_analysis_chart = px.line(filtered_df, x='work_year', y='salary_in_usd', color='job_title', title='Salary Trends by Job Title')
    elif selected_trend == 'company_location':
        trend_analysis_chart = px.line(filtered_df, x='work_year', y='salary_in_usd', color='company_location', title='Salary Trends by Company Location')

    # Hypothesis Testing
    if selected_hypothesis == 'salary_experience':
        hypothesis_plot = px.box(filtered_df, x='experience_level', y='salary_in_usd', title='Salary vs Experience Level')
    elif selected_hypothesis == 'salary_job':
        hypothesis_plot = px.box(filtered_df, x='job_title', y='salary_in_usd', title='Salary vs Job Title')
    elif selected_hypothesis == 'salary_company_size':
        hypothesis_plot = px.box(filtered_df, x='company_size', y='salary_in_usd', title='Salary vs Company Size')

    return (bar_chart, scatter_plot, box_plot, pie_chart, histogram, sunburst, line_chart, heatmap, parallel_coordinates, correlation_matrix, map_visualization, employment_type_pie_chart, data_table, trend_analysis_chart, hypothesis_plot)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
