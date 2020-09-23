import streamlit as st
import streamlit.components.v1 as components
import gca_requests as gl
import datetime
import urllib.parse
import pandas as pd
import gca_main_functions as mf


def gca_page_2():
    st.title("GOOGLE CALENDARS ANALYTICS PAGE 2")
    st.write(f'## 2 GOOGLE CALENDAR SPECIFIC ANALYSIS (1 CALENDAR)')
    st.sidebar.write(f'#### 2 GOOGLE CALENDAR SPECIFIC ANALYSIS (1 CALENDAR)')

    input_calendar_name = st.sidebar.selectbox('2 SELECT CALENDAR:', mf.list_calendar_names)

    input_calendar_id = [x["id"] for x in mf.list_calendar if x["summary"] == input_calendar_name][0]

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
            mf.specific_analysis(df_events, input_calendar_events, input_calendar_name, "dateTime",
                                "%Y-%m-%dT%H:%M:%S%z",
                              "hours", input_dates_analyze)

        elif input_calendar_specific_type == "DAYS EVENTS":
            mf.specific_analysis(df_events, input_calendar_events, input_calendar_name, "date", "%Y-%m-%d",
                              "days", input_dates_analyze)
    st.sidebar.write(f"---")
    st.write(f"---")
