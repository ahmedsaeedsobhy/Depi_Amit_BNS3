from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Load Data
df = pd.read_csv("G:/DEPI/Depi_Amit_AI_BNS3/Tasks/DataBase/Final_project/fordgobike2.csv")

app = Dash()
app.title = "Ford GoBike Interactive Dashboard"

# ==========================
# Styling
# ==========================
section_style = {
    'padding': '20px',
    'marginBottom': '20px',
    'borderRadius': '10px',
    'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'
}
kpi_style = {
    'backgroundColor': '#f8f9fa',
    'borderRadius': '8px',
    'padding': '15px',
    'width': '30%',
    'textAlign': 'center',
    'boxShadow': '0px 0px 5px rgba(0,0,0,0.05)'
}

# ==========================
# Layout
# ==========================
app.layout = html.Div([
    html.H1("Ford GoBike Interactive Dashboard", style={'textAlign': 'center'}),

    # Overview KPIs
    html.Div([
        html.H2("Overview KPIs"),
        html.Div([
            html.Div(id='total-trips', style=kpi_style),
            html.Div(id='avg-duration', style=kpi_style),
            html.Div(id='top-station', style=kpi_style)
        ], style={'display': 'flex', 'justifyContent': 'space-around'})
    ], style=section_style),

    # Overall Distributions
    html.Div([
        html.H2("Overall User Distributions"),

        html.Label("Select Distribution Type:"),
        dcc.Dropdown(
            id='distribution-dropdown',
            options=[
                {'label': 'Gender Distribution', 'value': 'gender'},
                {'label': 'User Type Distribution', 'value': 'user_type'},
                {'label': 'Age Group Distribution', 'value': 'age_group'}
            ],
            value='gender',
            clearable=False,
            style={'width': '50%'}
        ),

        html.Br(),
        dcc.Graph(id='overall-distribution-chart')
    ], style=section_style),

    # Filtered Trip Duration Distribution
    html.Div([
        html.H2("Trip Duration Group Distribution with Filters"),

        html.Div([

            # Left Sidebar (Filters)
            html.Div([
                html.H4("Filters", style={'textAlign': 'center'}),

                html.Label("Select Age Range:"),
                dcc.RangeSlider(
                    id='age-slider',
                    min=20,
                    max=80,
                    step=10,
                    value=[20, 80],
                    marks={i: str(i) for i in range(20, 81, 10)}
                ),

                html.Br(),

                html.Label("Select Gender(s):"),
                dcc.Checklist(
                    id='gender-checklist',
                    options=[{'label': g, 'value': g} for g in df['member_gender'].unique()],
                    value=list(df['member_gender'].unique())
                ),

                html.Br(),

                html.Label("Select User Type(s):"),
                dcc.Checklist(
                    id='user-type-checklist',
                    options=[{'label': t, 'value': t} for t in df['user_type'].unique()],
                    value=list(df['user_type'].unique())
                ),
            ],
            style={
                'width': '25%',
                'padding': '20px',
                'backgroundColor': '#f8f9fa',
                'borderRadius': '10px',
                'boxShadow': '0px 0px 5px rgba(0,0,0,0.05)',
                'marginRight': '20px'
            }),

            # Right Side (Chart)
            html.Div([
                dcc.Graph(id='trip-duration-group-chart', style={'height': '500px'})
            ], style={'width': '75%'})

        ], style={'display': 'flex', 'flexDirection': 'row'})
    ], style=section_style)
])

# ==========================
# Callbacks
# ==========================

# Overview KPIs
@app.callback(
    [Output('total-trips', 'children'),
     Output('avg-duration', 'children'),
     Output('top-station', 'children')],
    Input('distribution-dropdown', 'value')
)
def show_overall_kpis(_):
    total_trips = len(df)
    avg_duration = round(df['duration_min'].mean(), 2)
    top_station = df['start_station_name'].value_counts().idxmax()
    return (
        f"Total Trips: {total_trips:,}",
        f"Avg Duration: {avg_duration} mins",
        f"Most Popular Start Station: {top_station}"
    )


# Overall Distributions
@app.callback(
    Output('overall-distribution-chart', 'figure'),
    Input('distribution-dropdown', 'value')
)
def update_overall_distribution(selected_chart):
    if selected_chart == 'gender':
        fig = px.pie(
            df,
            names='member_gender',
            title="Gender Distribution",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

    elif selected_chart == 'user_type':
        fig = px.pie(
            df,
            names='user_type',
            title="User Type Distribution",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

    else:  # age_group
        age_group_df = df['Age_Group'].value_counts().reset_index()
        age_group_df.columns = ['Age Group', 'Count']
        fig = px.bar(
            age_group_df,
            x='Age Group',
            y='Count',
            title="Age Distribution",
            color_discrete_sequence=['#636EFA']
        )

        fig.update_layout(xaxis={'categoryorder': 'array',
           'categoryarray': ['20-29', '30-39', '40-49', '50-59', '60-69', '70-80']},
           title_x=0.5, paper_bgcolor='white', plot_bgcolor='white')
    return fig


# Filtered Trip Duration Distribution
@app.callback(
    Output('trip-duration-group-chart', 'figure'),
    [Input('age-slider', 'value'),
     Input('gender-checklist', 'value'),
     Input('user-type-checklist', 'value')]
)
def update_trip_duration_chart(age_range, selected_genders, selected_user_types):
    filtered = df[
        (df['age'] >= age_range[0]) &
        (df['age'] <= age_range[1]) &
        (df['member_gender'].isin(selected_genders)) &
        (df['user_type'].isin(selected_user_types))
    ]

    grouped = filtered['trip_dur'].value_counts().reset_index()
    grouped.columns = ['Trip Duration Group', 'Count']

    fig = px.bar(
        grouped,
        x='Trip Duration Group',
        y='Count',
        color='Trip Duration Group',
        title="Trip Duration Group Distribution",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(
        xaxis_title="Trip Duration Group",
        yaxis_title="Number of Trips",
        xaxis={'categoryorder': 'array',
           'categoryarray': ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60+']},
        title_x=0.5,
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    return fig


# ==========================
# Run App
# ==========================
if __name__ == "__main__":
    app.run(debug=True)