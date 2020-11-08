import plotly.graph_objects as go


def bar_cases_by_sex(cases_by_sex):
    # Remove the total row
    filter_df = cases_by_sex[:-1]

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
        #margin={"r": 10, "t": 10, "l": 10, "b": 0},
        # title_text='January 2013 Sales Report',
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



'''fig = px.choropleth_mapbox(cases_sum_df, geojson=geojson,
                               locations='code',
                               color='infected',
                               featureidkey="properties.KOMKODE",
                               color_continuous_scale="Inferno_r",
                               range_color=(0, 2500),
                               mapbox_style='carto-positron',
                               center={'lat': 55.9397, 'lon': 11.5},  # 'lon': 9.5156
                               zoom=5.6  # 5.6
                               # scope='europe',
                               # projection="mercator",
                               )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      dragmode=False)'''
