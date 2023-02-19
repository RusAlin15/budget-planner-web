import streamlit as st
import datetime
import calendar
from infrastructure.Budget import Budget
import pickle

STORAGE_ADDRESS = r"storage.pkl"

st.set_page_config(layout="wide")
column1, empty, column2 = st.columns([0.5, 0.3, 1.5])


def application_load(report_date_selector):
    try:
        with open(STORAGE_ADDRESS, "rb") as file:
            budgets_dict = pickle.load(file)
    except (EOFError, FileNotFoundError):
        budgets_dict = {
            f'{report_date_selector}': Budget(f'{report_date_selector}'),
        }
        application_save(budgets_dict)
    return budgets_dict


def application_save(obj):
    with open(STORAGE_ADDRESS, "wb") as file:
        pickle.dump(obj, file)


def select_report_month():
    this_year = datetime.date.today().year
    this_month = datetime.date.today().month
    report_year = st.selectbox('', range(this_year, this_year - 4, -1))
    month_abbr = calendar.month_abbr[1:]
    report_month_str = st.radio('', month_abbr, index=this_month - 1, horizontal=True)
    return f'{report_month_str}-{report_year}'


if __name__ == '__main__':
    with column1:
        st.title("Calendar View")
        st.write("Select an yead & a month:")

        report_date_selector = select_report_month()
        st.text(report_date_selector)

    budget_dict = application_load(report_date_selector)

    with empty:
        st.empty()
    with column2:
        x = st.slider('x')  # 👈 this is a widget
        st.write(x, 'squared is', x * x)

        st.text(budget_dict)
