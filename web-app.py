import streamlit as st
import datetime
import calendar
from infrastructure.Budget import Budget
from infrastructure.Record import Record
import pickle
import pandas as pd
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, \
    ColumnsAutoSizeMode

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
    report_month_str = st.selectbox('', month_abbr, index=this_month - 1)
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

    return budget_text, expenses_text, wishes_text, savings_text


if __name__ == '__main__':
    with st.sidebar:
        st.title("Calendar View")

        date_selector = select_report_month()
        budgets_dict = application_load()
        ratio = {
            'A': ('A: 40% expenses, 30% wishes, 30% savings', 0.4, 0.3, 0.3),
            'B': ('B: 50% expenses, 30% wishes, 20% savings', 0.5, 0.3, 0.2),
            'C': ('C: 20% expenses, 30% wishes, 50% savings', 0.2, 0.3, 0.5),

        }
        st.write(ratio['A'][0])
        st.write(ratio['B'][0])
        st.write(ratio['C'][0])
        selector = st.select_slider(
            'Select a range of color wavelength',
            options=['A', 'B', 'C'],
            value=('B'))
        st.write('You selected:', ratio[selector][0])
        st.write(ratio[selector][0])
    try:
        current_item = budgets_dict[date_selector]
    except KeyError:
        budgets_dict[f'{date_selector}'] = Budget(f'{date_selector}')
        application_save(budgets_dict)
        current_item = budgets_dict[date_selector]

    current_item.expences_percentage = ratio[selector][1]
    current_item.wish_percentage = ratio[selector][2]
    current_item.savings_percentage = ratio[selector][3]

    left_column, right_column, = st.columns(2)
    budget_txt, expenses_txt, wishes_txt, savings_txt = get_budget_details(current_item)
    show_state = "Income"

    with left_column:
        left_l_column, left_r_column = st.columns(2)
        with left_l_column:
            budget_button = st.button("Budget")
            st.text(budget_txt)
            st.text("")
            st.text("")
            st.text("")
            st.text("")
            st.text("")

            expenses_button = st.button("Expense")
            st.text(expenses_txt)
        with left_r_column:
            wishes_button = st.button("Wishes")
            st.text(wishes_txt)

            savings_button = st.button("Savings")
            st.text(savings_txt)

    with right_column:

        right_l_column, right_r_column = st.columns(2)

        with right_l_column:
            add_title = '<p style="font-family:sans-serif; color:White; font-size: 20px;">Add Entry</p>'
            st.markdown(add_title, unsafe_allow_html=True)

            genre = st.radio(
                "Select Entry Type",
                ('Income', 'Expense', 'Wish', 'Saving'))
            title = st.text_input('Insert Title', value=f"One Time {genre}")

        with right_r_column:
            st.text("")
            value = st.number_input('Insert Value', value=500.0, min_value=0.0, step=100.0)
            description = st.text_input(
                "Insert Details",
                value=f"{genre} Description"
            )
            date = st.date_input(
                "Insert date",
                datetime.datetime.today(),
            )
            month_abbr = calendar.month_abbr[1:]
            add_date = f'{month_abbr[date.month - 1]}-{date.year}'
        submitted = st.button("Submit")
        if submitted:
            if submitted and genre == "Income":
                try:
                    budgets_dict[add_date].add_income(Record(title, value, date, description))
                except KeyError:
                    budgets_dict[add_date] = Budget(f'{add_date}')
                    budgets_dict[add_date].add_income(Record(title, value, date, description))
            elif submitted and genre == "Expense":
                try:
                    budgets_dict[add_date].add_expense(Record(title, value, date, description))
                except KeyError:
                    budgets_dict[add_date] = Budget(f'{add_date}')
                    budgets_dict[add_date].add_expense(Record(title, value, date, description))
            elif submitted and genre == "Wish":
                try:
                    budgets_dict[add_date].add_wish_expenses(
                        Record(title, value, date, description))
                except KeyError:
                    budgets_dict[add_date] = Budget(f'{add_date}')
                    budgets_dict[add_date].add_wish_expenses(
                        Record(title, value, date, description))
            elif genre == "Saving":
                try:
                    budgets_dict[add_date].add_saving(Record(title, value, date, description))
                except KeyError:
                    budgets_dict[add_date] = Budget(f'{add_date}')
                    budgets_dict[add_date].add_saving(Record(title, value, date, description))
            application_save(budgets_dict)
            st.experimental_rerun()

    with st.container():
        left_show_col, right_show_col = st.columns(2)
        with left_show_col:
            text_placeholder = st.empty()
            text_placeholder.text("Income")
            df_placeholder = st.empty()
            df = pd.DataFrame.from_dict(current_item.incomes, orient='index')
            df_placeholder.dataframe(df)
            if budget_button:
                show_state = "Income"
                df = pd.DataFrame.from_dict(current_item.incomes, orient='index')
                df_placeholder.dataframe(df)
            if expenses_button:
                show_state = "Expense"
                df = pd.DataFrame.from_dict(current_item.expenses, orient='index')
                df_placeholder.dataframe(df)
            if wishes_button:
                show_state = "Wish"
                df = pd.DataFrame.from_dict(current_item.wish_expenses, orient='index')
                df_placeholder.dataframe(df)
            if savings_button:
                show_state = "Saving"
                df = pd.DataFrame.from_dict(current_item.savings, orient='index')
                df_placeholder.dataframe(df)
        with right_show_col:
            left_del_col, right_del_col = st.columns(2)

            with left_del_col:
                add_title = rf'<p style="font-family:sans-serif; color:White; font-size: 20px;">Delete {show_state}</p>'
                st.markdown(add_title, unsafe_allow_html=True)
                if show_state == "Income":
                    delete_id = st.number_input(
                        f"Select {show_state} index you want to delete",
                        min_value=current_item.min_income_id,
                        max_value=current_item.max_income_id,
                    )

                if show_state == "Expense":
                    delete_id = st.number_input(
                        f"Select {show_state} index you want to delete",
                        min_value=current_item.min_expense_id,
                        max_value=current_item.max_expense_id,
                    )
                if show_state == "Wish":
                    delete_id = st.number_input(
                        f"Select {show_state} index you want to delete",
                        min_value=current_item.min_wishes_id,
                        max_value=current_item.max_wishes_id,
                    )
                if show_state == "Saving":
                    delete_id = st.number_input(
                        f"Select {show_state} index you want to delete",
                        min_value=current_item.min_saving_id,
                        max_value=current_item.max_saving_id,
                    )
            with right_del_col:
                st.text('')
                st.text('')
                st.text('')
                st.text('')
                st.text('')
                delete_submitted = st.button("Delete")

            if delete_submitted:
                if show_state == "Income":
                    try:
                        current_item.delete_income(delete_id)
                    except KeyError:
                        pass
                elif show_state == "Expense":
                    try:
                        current_item.delete_expense(delete_id)
                    except KeyError:
                        pass
                elif show_state == "Wish":
                    try:
                        current_item.delete_wish(delete_id)
                    except KeyError:
                        pass
                elif show_state == "Saving":
                    try:
                        current_item.delete_saving(delete_id)
                    except KeyError:
                        pass
                application_save(budgets_dict)
                st.experimental_rerun()

            add_title = rf'<p style="font-family:sans-serif; color:White; font-size: 20px;">Edit {show_state}</p>'
            st.markdown(add_title, unsafe_allow_html=True)
            if show_state == "Income":
                edit_id = st.number_input(
                    f"Select {show_state} index you want to edit",
                    min_value=current_item.min_income_id,
                    max_value=current_item.max_income_id,
                )
            if show_state == "Expense":
                edit_id = st.number_input(
                    f"Select {show_state} index you want to edit",
                    min_value=current_item.min_expense_id,
                    max_value=current_item.max_expense_id,
                )
            if show_state == "Wish":
                edit_id = st.number_input(
                    f"Select {show_state} index you want to edit",
                    min_value=current_item.min_wishes_id,
                    max_value=current_item.max_wishes_id,
                )
            if show_state == "Saving":
                edit_id = st.number_input(
                    f"Select {show_state} index you want to edit",
                    min_value=current_item.min_saving_id,
                    max_value=current_item.max_saving_id,
                )
            right_l_column, right_r_column = st.columns(2)
            with right_l_column:
                try:
                    show_title = current_item.incomes[edit_id]["Title"]
                except:
                    show_title = ""
                try:
                    show_value = current_item.incomes[edit_id]["Value"]
                except:
                    show_value = 0.0
                title = st.text_input('Edit Title', value=show_title)
                value = st.number_input('Edit Value', value=show_value, step=100.0)

            with right_r_column:
                try:
                    show_description = current_item.incomes[edit_id]["Description"]
                except:
                    show_description = ""

                try:
                    show_date = current_item.incomes[edit_id]["Date"]
                except:
                    show_date = datetime.datetime.today()
                description = st.text_input(
                    "Edit Details",
                    value=show_description
                )
                date = st.date_input(
                    "Edit date",
                    value=show_date
                )
                month_abbr = calendar.month_abbr[1:]
                add_date = f'{month_abbr[date.month - 1]}-{date.year}'
            edit_button = st.button("Edit")
            if edit_button:
                if show_state == "Income":
                    try:
                        current_item.edit_income(edit_id, Record(title, value, date, description))
                    except KeyError:
                        pass
                elif show_state == "Expense":
                    try:
                        current_item.edit_expense(edit_id, Record(title, value, date, description))
                    except KeyError:
                        pass
                elif show_state == "Wish":
                    try:
                        current_item.edit_wish_expense(edit_id,
                                                       Record(title, value, date, description))
                    except KeyError:
                        pass
                elif show_state == "Saving":
                    try:
                        current_item.edit_saving(edit_id, Record(title, value, date, description))
                    except KeyError:
                        pass
                application_save(budgets_dict)
                st.experimental_rerun()
