import streamlit as st
import datetime
import calendar
from infrastructure.Budget import Budget
from infrastructure.Record import Record
import pickle
import pandas as pd
import numpy as np

STORAGE_ADDRESS = r"storage.pkl"

st.set_page_config(layout="wide")


def application_load():
    try:
        with open(STORAGE_ADDRESS, "rb") as file:
            budgets_dict = pickle.load(file)
    except (EOFError, FileNotFoundError):
        st.write("INOT ERROR")
        budgets_dict = {}
        application_save(budgets_dict)
    return budgets_dict


def application_save(obj):
    with open(STORAGE_ADDRESS, "wb") as file:
        pickle.dump(obj, file)


def select_report_month():
    this_year = datetime.date.today().year
    this_month = datetime.date.today().month
    month_abbr = calendar.month_abbr[1:]
    report_month_str = st.radio('', month_abbr, index=this_month - 1, horizontal=True)
    report_year = st.selectbox('', range(this_year, this_year - 4, -1))
    return f'{report_month_str}-{report_year}'


def get_budget_details(item):
    recommanded_wishes = round((item.total_income) * (item.wish_percentage), 2)
    recommanded_expences = round((item.total_income) * (item.expences_percentage), 2)
    recommanded_savings = round((item.total_income) * (item.savings_percentage), 2)
    try:
        wishes_usage = round((item.total_wish_expense / recommanded_wishes) * 100, 2)
        expenses_usage = round((item.total_expenses / recommanded_expences) * 100, 2)
        savings_usage = round((item.total_savings / recommanded_savings) * 100, 2)
    except ZeroDivisionError:
        wishes_usage = 0
        expenses_usage = 0
        savings_usage = 0

    budget_text = f"Total income {item.total_income} RON\n"

    wishes_text = f"Recommended budget: {recommanded_wishes} RON\n\n" \
                  f"Total spent: {item.total_wish_expense} RON\n\n" \
                  f"Percentage: {wishes_usage} %"
    expenses_text = f"Recommended budget: {recommanded_expences} RON\n\n" \
                    f"Total spent: {item.total_expenses} RON\n\n" \
                    f"Percentage: {expenses_usage} %"
    savings_text = f"Recommended budget: {recommanded_savings} RON\n\n" \
                   f"Total spent: {item.total_savings} RON\n\n" \
                   f"Percentage: {savings_usage} %"

    return budget_text, wishes_text, expenses_text, savings_text


if __name__ == '__main__':
    with st.sidebar:
        st.title("Calendar View")
        st.write("Select an year & a month:")

        date_selector = select_report_month()
        budgets_dict = application_load()
        st.write(date_selector)
    try:
        current_item = budgets_dict[date_selector]
    except (KeyError):
        budgets_dict[f'{date_selector}'] = Budget(f'{date_selector}')
        application_save(budgets_dict)
        current_item = budgets_dict[date_selector]

    left_column, right_column, = st.columns(2)
    budget_txt, expenses_txt, wishes_txt, savings_txt = get_budget_details(current_item)

    with left_column:
        left_l_column, left_r_column = st.columns(2)
        with left_l_column:
            budget_title = '<p style="font-family:sans-serif; color:White; font-size: 30px;">Budget</p>'
            st.markdown(budget_title, unsafe_allow_html=True)
            st.text(budget_txt)
            st.text("")
            st.text("")
            st.text("")
            st.text("")
            st.text("")

            expenses_title = '<p style="font-family:sans-serif; color:White; font-size: 30px;">Expenses</p>'
            st.markdown(expenses_title, unsafe_allow_html=True)
            st.text(expenses_txt)
        with left_r_column:
            wishes_title = '<p style="font-family:sans-serif; color:White; font-size: 30px;">Wishes</p>'
            st.markdown(wishes_title, unsafe_allow_html=True)
            st.text(wishes_txt)

            savings_title = '<p style="font-family:sans-serif; color:White; font-size: 30px;">Savings</p>'
            st.markdown(savings_title, unsafe_allow_html=True)
            st.text(savings_txt)

    with right_column:
        add_title = '<p style="font-family:sans-serif; color:White; font-size: 30px;">Add Entry</p>'
        st.markdown(add_title, unsafe_allow_html=True)

        right_l_column, right_r_column = st.columns(2)
        with right_l_column:
            title = st.text_input('Insert Title', placeholder='Salar')
            genre = st.radio(
                "Select Entry Type",
                ('Income', 'Expense', 'Wish', 'Saving'))

        with right_r_column:
            value = st.number_input('Insert Value', step=1.0)
            description = st.text_input(
                "Insert Details",
                placeholder="Salar Alin"
            )
            date = st.date_input(
                "Insert date",
                datetime.datetime.today(),
            )
            month_abbr = calendar.month_abbr[1:]
            add_date = f'{month_abbr[date.month - 1]}-{date.year}'
        if st.button("ADD"):
            try:
                budgets_dict[add_date].add_income(Record(title, value, date, description))
            except KeyError:
                budgets_dict[f'{date_selector}'] = Budget(f'{add_date}')
                budgets_dict[add_date].add_income(Record(title, value, date, description))
            application_save(budgets_dict)
            st._rerun()

    with st.container():
        column1, column2, column3, column4 = st.columns(4)
        with column1:
            st.write(current_item.show_budget())
        with column2:
            st.write(current_item.show_expenses())
        with column3:
            st.write(current_item.show_wishes())
        with column4:
            st.write(current_item.show_savings())

            df = pd.DataFrame(
                np.random.randn(15, 20),
                columns=('col %d' % i for i in range(20)))

            st.dataframe(df)  # Same as st.write(df)
