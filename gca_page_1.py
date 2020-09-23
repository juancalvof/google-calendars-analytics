import streamlit as st
import gca_requests as gl
import pandas as pd
import plotly_graphs as pg
import gca_main_functions as mf


def gca_page_1():
    # Config page
    st.title("GOOGLE CALENDARS ANALYTICS")

    # 1 General Analysis
    st.write(f"## 1 GOOGLE CALENDARS GENERAL ANALYSIS (ALL CALENDARS)")
    st.sidebar.write(f"#### 1 GOOGLE CALENDARS GENERAL ANALYSIS (ALL CALENDARS)")
    input_calendar_general_type = st.sidebar.selectbox('1_b SELECT EVENTS TYPE:', ["HOURS EVENTS", "DAYS EVENTS",
                                                                                   "BOTH"])
    # Visualize df calendars
    st.write("### **1_a** General information of each calendar")
    list_calendar = gl.retrieve_list_calendars()["items"]
    st.dataframe(pd.DataFrame(mf.list_calendar))

    # Visualize number events calendars
    st.write("### **1_b** Number of events in each calendar")
    df_total_events = mf.df_count_events(list_calendar, input_calendar_general_type)
    st.dataframe(df_total_events)
    st.plotly_chart(pg.bar_chart(df_total_events, df_total_events.index, 'number of events'), use_container_width=True,
                        config=pg.UNBRAND_CONFIG)
    st.sidebar.write(f"---")
    st.write(f"---")
