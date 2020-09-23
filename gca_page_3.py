import streamlit as st
import datetime
import gca_main_functions as mf


def gca_page_3():
    # 3 Comparative analysis
    st.write(f'## 3 GOOGLE CALENDAR COMPARATIVE  ANALYSIS (ALL CALENDARS)')
    st.sidebar.write(f'#### 3 GOOGLE CALENDAR COMPARATIVE  ANALYSIS (ALL CALENDARS)')

    input_dates_analyze_comparative = st.sidebar.date_input("3 SELECT RANGE OF DATES TO ANALYZE",
                                                            [datetime.date(2019, 1,
                                                                           1),
                                                             datetime.date.today()],
                                                            key="comp_di")

    input_list_calendars_selected = st.sidebar.multiselect('3 SELECT ANY NUMBER OF CALENDARS:', mf.list_calendar_names)

    input_calendar_specific_type_comparative = st.sidebar.selectbox('3 SELECT EVENTS TYPE:', ["HOURS EVENTS",
                                                                                              "DAYS EVENTS"],
                                                                    key="comp_sb")

    if input_calendar_specific_type_comparative == "HOURS EVENTS":
        mf.comparative_analysis(input_list_calendars_selected, "dateTime", "%Y-%m-%dT%H:%M:%S%z", "hours",
                             input_dates_analyze_comparative)

    elif input_calendar_specific_type_comparative == "DAYS EVENTS":
        mf.comparative_analysis(input_list_calendars_selected, "date", "%Y-%m-%d", "days",
                             input_dates_analyze_comparative)
    st.sidebar.write(f"---")
    st.write(f"---")
