import streamlit as st
import numpy as np
import pandas as pd
import datetime
import calendar

column1, column2 = st.columns(2)


def select_report_month():
    global report_year, report_month_str
    this_year = datetime.date.today().year
    this_month = datetime.date.today().month
    report_year = st.selectbox('', range(this_year, this_year - 4, -1))
    month_abbr = calendar.month_abbr[1:]
    report_month_str = st.radio('', month_abbr, index=this_month - 1, horizontal=True)
    return f'{report_year}-{report_month_str}'

if __name__ == '__main__':

    with column1:
        st.title("Calendar View Example")
        st.write("Select a month:")

        report_date_selector =  select_report_month()
        st.text(report_date_selector)

    with column2:
        x = st.slider('x')  # 👈 this is a widget
        st.write(x, 'squared is', x * x)


        if st.checkbox('Show dataframe'):
            chart_data = pd.DataFrame(
                np.random.randn(20, 3),
                columns=['a', 'b', 'c'])

            chart_data

