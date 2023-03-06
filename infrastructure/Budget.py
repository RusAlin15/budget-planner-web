class Budget:
    def __init__(self, title):
        self.__title = title
        self.__incomes_dict = {}
        self.__wishes_expense_dict = {}
        self.__expenses_dict = {}
        self.__savings_dict = {}
        self.__total_income = 0
        self.__total_wish_expenses = 0
        self.__total_expenses = 0
        self.__total_savings = 0
        self.__income_id = 0
        self.__savings_id = 0
        self.__expense_id = 0
        self.__wish_expenses_id = 0
        self.__expences_percentage = 0.5
        self.__wishes_percentage = 0.3
        self.__savings_percentage = 0.2

    def add_income(self, record):
        self.__income_id += 1
        self.__total_income += record.value
        self.__incomes_dict[self.__income_id] = record

    def add_saving(self, record):
        self.__savings_id += 1
        self.__total_savings += record.value
        self.__savings_dict[self.__savings_id] = record

    def add_expense(self, record):
        self.__expense_id += 1
        self.__expenses_dict[self.__expense_id] = record
        self.__total_expenses += record.value

    def add_wish_expenses(self, record):
        self.__wish_expenses_id += 1
        self.__wishes_expense_dict[self.__wish_expenses_id] = record
        self.__total_wish_expenses += record.value

    @property
    def title(self) -> str:
        return self.__title

    @property
    def total_income(self):
        return self.__total_income

    @property
    def total_savings(self):
        return self.__total_savings

    @property
    def expences_percentage(self):
        return self.__expences_percentage

    @property
    def wish_percentage(self):
        return self.__wishes_percentage

    @property
    def savings_percentage(self):
        return self.__savings_percentage

    @expences_percentage.setter
    def expences_percentage(self, percentage):
        self.__expences_percentage = percentage

    @wish_percentage.setter
    def wish_percentage(self, percentage):
        self.__wishes_percentage = percentage

    @savings_percentage.setter
    def savings_percentage(self, percentage):
        self.__savings_percentage = percentage

    @property
    def total_expenses(self):
        return self.__total_expenses

    @property
    def total_wish_expense(self):
        return self.__total_wish_expenses

    @property
    def incomes(self):
        return self.get_recording(self.__incomes_dict)

    @staticmethod
    def get_recording(dictionary):
        recoring_dict = {}
        for key, value in dictionary.items():
            recoring_dict[key] = value.recording
        return recoring_dict

    @property
    def expenses(self):
        return self.get_recording(self.__expenses_dict)

    @property
    def savings(self):
        return self.get_recording(self.__savings_dict)

    @property
    def wish_expenses(self):
        return self.get_recording(self.__wishes_expense_dict)

    def show_budget(self):
        text = []
        for key, value in self.incomes.items():
            text.append(f"{key}.  {value}\n")
        return text

    def show_savings(self):
        text = []
        for key, value in self.savings.items():
            text.append(f"{key}.  {value}\n")
        return text

    def show_wishes(self):
        text = []
        for key, value in self.wish_expenses.items():
            text.append(f"{key}.  {value}\n")
        return text

    def show_expenses(self):
        text = []
        for key, value in self.expenses.items():
            text.append(f"{key}.  {value}\n")
        return text

    @property
    def last_income(self):
        return self.__incomes_dict[self.__income_id]

    @property
    def last_expense(self):
        return self.__expenses_dict[self.__expense_id]

    @property
    def last_saving(self):
        return self.__savings_dict[self.__savings_id]

    @property
    def last_wish_expense(self):
        return self.__wishes_expense_dict[self.__wish_expenses_id]

    def edit_income(self, id, record):
        old_value = self.__incomes_dict[id].value
        self.__incomes_dict[id] = record
        self.__total_income += record.value - old_value

    def edit_saving(self, id, record):
        old_value = self.__savings_dict[id].value
        self.__savings_dict[id] = record
        self.__total_savings += record.value - old_value

    def edit_wish_expense(self, id, record):
        old_value = self.__wishes_expense_dict[id].value
        self.__wishes_expense_dict[id] = record
        self.__total_wish_expenses += record.value - old_value

    def edit_expense(self, id, record):
        old_value = self.__expenses_dict[id].value
        self.__expenses_dict[id] = record
        self.__total_expenses += record.value - old_value

    def delete_saving(self, id):
        value = self.__incomes_dict[id].value
        del self.__savings_dict[id]
        self.__total_savings -= value

    def delete_expense(self, id):
        value = self.__expenses_dict[id].value
        del self.__expenses_dict[id]
        self.__total_expenses -= value

    def delete_wish(self, id):
        value = self.__wishes_expense_dict[id].value
        del self.__wishes_expense_dict[id]
        self.__total_wish_expenses -= value

    def delete_income(self, id):
        value = self.__incomes_dict[id].value
        del self.__incomes_dict[id]
        self.__total_income -= value

    @property
    def max_income_id(self):
        return self.__income_id

    @property
    def min_income_id(self):
        min = self.__income_id
        for key in self.__incomes_dict.keys():
            if key < min:
                min = key
        return min

    @property
    def max_expense_id(self):
        return self.__expense_id

    @property
    def min_expense_id(self):
        min = self.__expense_id
        for key in self.__expenses_dict.keys():
            if key < min:
                min = key
        return min

    @property
    def max_wishes_id(self):
        return self.__wish_expenses_id

    @property
    def min_wishes_id(self):
        min = self.__wish_expenses_id
        for key in self.__wishes_expense_dict.keys():
            if key < min:
                min = key
        return min

    @property
    def max_saving_id(self):
        return self.__savings_id

    @property
    def min_saving_id(self):
        min = self.__savings_id
        for key in self.__savings_dict.keys():
            if key < min:
                min = key
        return min
