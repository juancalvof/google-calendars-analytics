import streamlit as st
import streamlit.components.v1 as components
import gca_requests as gl
import datetime
import urllib.parse
import pandas as pd
from PIL import Image
import plotly_graphs as pg

# VARIABLES
list_calendar = gl.retrieve_list_calendars()["items"]
list_calendar_names = [x["summary"] for x in list_calendar]

# FUNCTIONS
@st.cache
def df_count_events(list_calendars, type_time_st="BOTH") -> pd.DataFrame:
    global filter_items
    dict_total_events = {}
    for x in list_calendars:
        items = gl.retrieve_calendar_events_by_id(x["id"])

        if type_time_st != "BOTH":
            type_time = "dateTime"
            if type_time_st == "DAYS EVENTS":
                type_time = "date"
            filter_items = [x for x in items if type_time in x["end"]]
        elif type_time_st == "BOTH":
            filter_items = items

        dict_total_events[x["summary"]] = len(filter_items)

    return pd.DataFrame.from_dict(dict_total_events, orient='index', columns=["number of events"])


def dict_events_filter(input_calendar_events, type_time, format_time):
    dict_total_events = {}
    for x in input_calendar_events:
        if type_time in x["end"]:
            date_end = datetime.datetime.strptime(x["end"][type_time], format_time)
            date_start = datetime.datetime.strptime(x["start"][type_time], format_time)
            dict_total_events[x["id"]] = date_end - date_start
    return dict_total_events


def df_events_filter(events, df_events, type_time, format_time, type) -> pd.DataFrame:
    input_calendar = dict_events_filter(events, type_time, format_time)
    df = pd.DataFrame(list(input_calendar.items()), columns=["id", type])
    df["start"] = df["id"].map(df_events.set_index('id')["start"])
    df["end"] = df["id"].map(df_events.set_index('id')["end"])
    # df["recurrence"] = df["id"].map(df_events.set_index('id')["recurrence"])
    df["start"] = df["start"].apply(lambda x: datetime.datetime.strptime(x[type_time], format_time))
    df["end"] = df["end"].apply(lambda x: datetime.datetime.strptime(x[type_time], format_time))
    #Test
    # df['Week number of the year'] = df['start'].map(lambda x: x.strftime('%D'))
    df['Week number of the year'] = df['start'].map(lambda x: x.strftime('%Y/%W'))
    return df.sort_values(by=['Week number of the year'])


@st.cache
def df_group_sum_weeks(df, type, input_calendar_name, dates) -> pd.DataFrame:
    df[input_calendar_name + " " + type] = df[type]
    df_group = df.groupby("Week number of the year")[input_calendar_name + " " + type].sum()
    df_group = df_group.reset_index().set_index("Week number of the year")
    # Streamlit doesnt take class 'pandas.core.indexes.period.PeriodIndex'
    idx = pd.period_range(dates[0], dates[-1], freq="W")
    idx = [str(i.strftime('%Y/%W')) for i in idx]
    df_group = df_group.reindex(idx, fill_value=pd.Timedelta('0 days'))
    if type == "hours":
        df_group[input_calendar_name + " " + type] = (df_group[input_calendar_name + " " + type].dt.seconds / 3600)
    elif type == "days":
        df_group[input_calendar_name + " " + type] = df_group[input_calendar_name + " " + type].dt.days

    return df_group


def specific_analysis(df_events, input_calendar_events, input_calendar_name, type_time, format_time, type, dates):
    df = df_events_filter(input_calendar_events, df_events, type_time, format_time, type)

    st.write(
        f'### **2_b_I TYPE HOURS:** List of events in "{input_calendar_name}" calendar, of type {type}, with Week number of the year of '
        f'the event column ')

    if len(df.index) == 0:
        st.write("No values in this type.")
    else:
        st.dataframe(df)

    st.write(f'### **2_b_II TYPE HOURS:** Total amount of {type} in the events in "{input_calendar_name}" calendar for '
             'each Week number of the year ')

    if len(df.index) == 0:
        st.write("No values in this type.")
    else:
        df_group = df_group_sum_weeks(df, type, input_calendar_name, dates)
        st.dataframe(df_group)
        st.plotly_chart(pg.line_chart(df_group, df_group.index, df_group.columns[0], type), use_container_width=True,
                        config=pg.UNBRAND_CONFIG)


def comparative_analysis(list_calendars_selected, type_time, format_time, type, dates):
    idx = pd.period_range(dates[0], dates[-1], freq="W")
    idx = [str(i.strftime('%Y/%W')) for i in idx]
    df_final = pd.DataFrame(index=idx)
    if len(list_calendars_selected) == 0:
        st.write("No calendar selected.")

    else:
        for calendar in list_calendars_selected:
            input_calendar_id = [x["id"] for x in list_calendar if x["summary"] == calendar][0]
            input_calendar_events = gl.retrieve_calendar_events_by_id(input_calendar_id)

            if len(input_calendar_events) == 0:
                st.write(f"No values in {calendar} calendar.")
            else:
                df_events = pd.DataFrame(input_calendar_events)

                df = df_events_filter(input_calendar_events, df_events, type_time, format_time, type)

                if len(df.index) != 0:
                    df_group = df_group_sum_weeks(df, type, calendar, dates)
                    df_final = df_final.join(df_group)

                else:
                    st.write(f"No {type} events  in {calendar} calendar.")

        st.dataframe(df_final)
        st.plotly_chart(pg.line_chart_multiple(df_final, type),
                        use_container_width=True,
                        config=pg.UNBRAND_CONFIG)


def filter_by_dates(dict, type, dates):
    key = "dateTime"
    if type == "DAYS EVENTS":
        key = "date"
    result = [x for x in dict if x["start"][key] >= dates[0] & x['start'][key] <= dates[-1]]
    return result


if __name__ == "__main__":
    # Config page
    st.beta_set_page_config("GOOGLE CALENDARS ANALYTICS", ":calendar:", "wide", "auto")
    st.title("GOOGLE CALENDARS ANALYTICS")
    image = Image.open('IMAGES/google_calendar.jpg')
    st.sidebar.image(image, width=150)

    # 1 General Analysis
    st.write(f"## 1 GOOGLE CALENDARS GENERAL ANALYSIS (ALL CALENDARS)")
    st.sidebar.write(f"#### 1 GOOGLE CALENDARS GENERAL ANALYSIS (ALL CALENDARS)")
    input_calendar_general_type = st.sidebar.selectbox('1_b SELECT EVENTS TYPE:', ["HOURS EVENTS", "DAYS EVENTS",
                                                                                   "BOTH"])
    # Visualize df calendars
    st.write("### **1_a** General information of each calendar")
    list_calendar = gl.retrieve_list_calendars()["items"]
    st.dataframe(pd.DataFrame(list_calendar))

    # Visualize number events calendars
    st.write("### **1_b** Number of events in each calendar")
    df_total_events = df_count_events(list_calendar, input_calendar_general_type)
    st.dataframe(df_total_events)
    st.plotly_chart(pg.bar_chart(df_total_events, df_total_events.index, 'number of events'), use_container_width=True,
                        config=pg.UNBRAND_CONFIG)

    # 2 Specific analysis
    list_calendar_names = [x["summary"] for x in list_calendar]
    st.write(f"---")

    st.write(f'## 2 GOOGLE CALENDAR SPECIFIC ANALYSIS (1 CALENDAR)')
    st.sidebar.write(f'#### 2 GOOGLE CALENDAR SPECIFIC ANALYSIS (1 CALENDAR)')



    input_calendar_name = st.sidebar.selectbox('2 SELECT CALENDAR:', list_calendar_names)

    input_calendar_id = [x["id"] for x in list_calendar if x["summary"] == input_calendar_name][0]

    input_dates_analyze = st.sidebar.date_input("2_b SELECT RANGE OF DATES TO ANALYZE", [datetime.date(2019, 1, 1),
                                                                                       datetime.date.today()],
                                                key="spe_di")

    input_calendar_specific_type = st.sidebar.selectbox('2_b SELECT EVENTS TYPE:', ["HOURS EVENTS", "DAYS EVENTS"],
                                                        key="spe_sb")

    # Visualize events of selected calendar
    input_calendar_events = gl.retrieve_calendar_events_by_id(input_calendar_id)
    if len(input_calendar_events) == 0:
        st.write("No values in this calendar.")
    else:
        #TODO Filter before dataframe
        # df_events = filter_by_dates(input_calendar_events, input_dates_analyze, input_calendar_specific_type)
        df_events = pd.DataFrame(input_calendar_events)

        st.write(f'### **2_a_I** List of events in "{input_calendar_name}" calendar')
        st.dataframe(df_events)

        st.write(f'### **2_a_II** "{input_calendar_name}" calendar visualization')
        input_calendar_id_number = urllib.parse.quote(input_calendar_id)
        components.iframe(
            f"https://calendar.google.com/calendar/embed?src={input_calendar_id_number}&ctz=Europe%2FMadrid",
            width=1200, height=800, scrolling=True)

        if input_calendar_specific_type == "HOURS EVENTS":
            specific_analysis(df_events, input_calendar_events, input_calendar_name, "dateTime", "%Y-%m-%dT%H:%M:%S%z",
                              "hours", input_dates_analyze)

        elif input_calendar_specific_type == "DAYS EVENTS":
            specific_analysis(df_events, input_calendar_events, input_calendar_name, "date", "%Y-%m-%d",
                              "days", input_dates_analyze)
    st.write(f"---")

    # 3 Comparative analysis
    st.write(f'## 3 GOOGLE CALENDAR COMPARATIVE  ANALYSIS (ALL CALENDARS)')
    st.sidebar.write(f'#### 3 GOOGLE CALENDAR COMPARATIVE  ANALYSIS (ALL CALENDARS)')

    input_dates_analyze_comparative = st.sidebar.date_input("3 SELECT RANGE OF DATES TO ANALYZE",
                                                            [datetime.date(2019, 1,
                                                                           1),
                                                             datetime.date.today()],
                                                            key="comp_di")

    input_list_calendars_selected = st.sidebar.multiselect('3 SELECT ANY NUMBER OF CALENDARS:', list_calendar_names)

    input_calendar_specific_type_comparative = st.sidebar.selectbox('3 SELECT EVENTS TYPE:', ["HOURS EVENTS",
                                                                                              "DAYS EVENTS"],
                                                                    key="comp_sb")

    if input_calendar_specific_type_comparative == "HOURS EVENTS":
        comparative_analysis(input_list_calendars_selected, "dateTime", "%Y-%m-%dT%H:%M:%S%z", "hours",
                             input_dates_analyze_comparative)

    elif input_calendar_specific_type_comparative == "DAYS EVENTS":
        comparative_analysis(input_list_calendars_selected, "date", "%Y-%m-%d", "days",
                             input_dates_analyze_comparative)

    st.sidebar.write('Notes: Events with status "cancelled" are omitted.')
    st.write(f"---")
