import plotly.express as px
import plotly.graph_objects as go
import gca_main_functions as mf
import streamlit as st

UNBRAND_CONFIG = dict(modeBarButtonsToRemove=['sendDataToCloud', 'toggleSpikelines', 'hoverCompareCartesian'],
                      displaylogo=False, showLink=False,displayModeBar=False, showTips=False)


def test_line_chart():
    df = px.data.gapminder().query("continent=='Oceania'")
    fig = px.line(df, x="year", y="lifeExp", color='country')
    return fig


def line_chart(df, x, y, type, input_calendar_name):

    color = [x["backgroundColor"] for x in mf.list_calendar if input_calendar_name == x["summary"]][0]
    fig = px.line(df, x=x, y=y, template="simple_white")
    fig.update_xaxes(
        tickangle=270,
        dtick="M1",
        tickformat="%Y",
        ticklabelmode="period",
        showspikes=True,
        spikethickness=1,
        fixedrange=True)
    fig.update_yaxes(showspikes=True, fixedrange=True, spikethickness=1)
    fig.update_traces(marker_color=color, line_color=color)

    fig.update_layout(xaxis_title='YEAR AND WEEK NUMBER OF THE YEAR',
                      yaxis_title=type.upper())
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x")
    return fig


def line_chart_multiple(df, type):
    fig = go.Figure()
    for column in df.columns:
        color = [x["backgroundColor"] for x in mf.list_calendar if column == x["summary"]][0]
        fig.add_trace(go.Scatter(x=df.index, y=df[column], name=column, line=dict(color=color)))
    fig.update_xaxes(
        tickangle=270,
        dtick="M1",
        tickformat="%b\n%Y",
        ticklabelmode="period",
        showspikes=True,
        spikethickness=1,
        fixedrange=True)
    fig.update_yaxes(showspikes=True, fixedrange=True, spikethickness=1)
    fig.update_layout(template="simple_white")
    fig.update_layout(xaxis_title='YEAR AND WEEK NUMBER OF THE YEAR',
                      yaxis_title=type.upper())
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x")
    # fig.update_traces(marker_color='rgb(200,210,240)', marker_line_color='rgb(8,48,107)',
    #                   marker_line_width=1.5, line_color='rgb(0,255,194)')
    return fig

def bar_chart(df, x, y):
    fig = px.bar(df, x=x, y=y, template="simple_white",
                 labels={'number of events': 'NUMBER OF EVENTS PER CALENDAR', 'index': 'CALENDAR NAME'})
    fig.update_xaxes(showspikes=True, fixedrange=True, spikethickness=1)
    fig.update_yaxes(showspikes=True, fixedrange=True, spikethickness=1)
    fig.update_layout(hovermode='x')
    fig.update_traces(marker_color='rgb(0,255,194)', marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5)
    fig.update_traces(hovertemplate=None)
    return fig