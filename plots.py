import plotly.graph_objects as go
from preprocessing import *


def cases_by_sex():

    # Remove the 'total' row
    filter_df = cases_by_sex_data()[:-1]

    # Get values for age groups, men, and women
    age_groups = filter_df['age_group'].values
    men_data = filter_df['men'].values
    women_data = filter_df['women'].values

    # Create figure
    fig = go.Figure(data=[
        # The <extra></extra> removes "men" in second box for hoverinfo
        go.Bar(name='Men', x=age_groups, y=men_data,
               hovertemplate="Age group: %{x} <br>Infected: %{y} <extra></extra>",
               ),
        go.Bar(name='Women', x=age_groups, y=women_data,
               hovertemplate="Age group: %{x} <br>Infected: %{y} <extra></extra>",
               )
    ])

    # Update the figure layout
    fig.update_layout(
        barmode='group',
        margin={"r": 0, "t": 20, "l": 0, "b": 0},
        hoverlabel={'font_size': 16},
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
    )

    # Update the x axis
    fig.update_xaxes(
        title_text='Age group'
    )

    fig.update_yaxes(
        title_text='Infected'
    )

    return fig


def daily_infected():
    daily_cases = daily_infected_data().iloc[:-1, :]

    fig = go.Figure(
        go.Bar(
            x=daily_cases['date_sample'],
            y=daily_cases['total_daily'],
            hovertemplate="Date: %{x} <br>Infected: %{y} <extra></extra>",
        )
    )

    fig.update_layout(
        # title_text='Daily infected in Denmark',
        yaxis=dict(
            title='Infected'
        ),
        # margin={"r": 10, "t": 50, "l": 10, "b": 20},
        margin={"r": 0, "t": 20, "l": 0, "b": 0},
    )

    return fig


def daily_tests():

    daily_test = daily_tests_data().iloc[:-1, :]

    fig = go.Figure(
        go.Bar(
            x=daily_test['Date'],
            y=daily_test['Tested'],
            hovertemplate="Date: %{x} <br>Tests: %{y} <extra></extra>",
        )
    )

    fig.update_layout(
        # title_text='Daily infected in Denmark',
        yaxis=dict(
            title='Infected'
        ),
        # margin={"r": 10, "t": 50, "l": 10, "b": 20},
        margin={"r": 0, "t": 20, "l": 0, "b": 0},
    )

    return fig


def daily_percent():
    daily_percent_df = daily_infected_percent_data()

    fig = go.Figure(
        go.Bar(
            x=daily_percent_df['date_sample'],
            y=daily_percent_df['percent_positive'],
            hovertemplate="Date: %{x} <br>Percent positive: %{y} <extra></extra>",
        )
    )

    fig.update_layout(
        # title_text='Daily infected in Denmark',
        yaxis=dict(
            title='Percent positive cases'
        ),
        margin={"r": 0, "t": 20, "l": 0, "b": 0},
    )

    return fig


def admitted_over_time():
    admitted_df = admitted_over_time_data()

    fig = go.Figure(
        go.Bar(
            x=admitted_df['Dato'],
            y=admitted_df['Total'],
            hovertemplate="Date: %{x} <br>Admitted: %{y} <extra></extra>",
        )
    )

    fig.update_layout(
        # title_text='Daily infected in Denmark',
        yaxis=dict(
            title='Admitted'
        ),
        margin={"r": 0, "t": 20, "l": 0, "b": 0},
    )

    return fig


def deaths_over_time():

    deaths_df = deaths_over_time_data()

    fig = go.Figure(
        go.Bar(
            x=deaths_df['date'],
            y=deaths_df['deaths'],
            hovertemplate="Date: %{x} <br>Deaths: %{y} <extra></extra>",
        )
    )

    fig.update_layout(
        yaxis=dict(
            title='Deaths'
        ),
        margin={"r": 0, "t": 20, "l": 0, "b": 0},
    )

    return fig


def cumulative_deaths():

    cumulative_deaths_df = deaths_cumulative_data()

    fig = go.Figure(
        go.Bar(
            x=cumulative_deaths_df.index,
            y=cumulative_deaths_df['deaths'],
            hovertemplate="Date: %{x} <br>Deaths: %{y} <extra></extra>",
        )
    )

    fig.update_layout(
        yaxis=dict(
            title='Cumulative deaths'
        ),
        margin={"r": 0, "t": 20, "l": 0, "b": 0},
    )

    return fig

