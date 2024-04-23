import variables as vars
import customtkinter as ctk
import datetime
from CTkMessagebox import CTkMessagebox
from tkinter import StringVar
from icecream import ic


class GUI:
    def __init__(self, master=None, label_text="", left_offset=0, top_offset=0) -> None:
        # no label text was passed
        if label_text == "":
            label_text = f"Component{vars.generic_counter}"
            vars.generic_counter += 1

        # name the variables based on label text
        prefix = label_text.replace(" ", "_").lower()
        self.textV_name = f"{prefix}_textVariable"
        self.input_name = f"{prefix}_input"

        short_label = label_text.replace("guest1 ", "").replace("guest2 ", "").replace("guest3 ", "")
        short_label = short_label.replace("host1 ", "").replace("host2 ", "").replace("finances ", "")
        short_label = short_label.replace( "entry ", "").replace("combo ", "").replace("datepicker ", "")

        ctk.CTkLabel(
            master, text=short_label, font=vars.font_family
        ).place(x=left_offset + 10, y=top_offset + 10)

    def get(self) -> str:
        field = vars.form[self.input_name]
        return field.get()

    def set(self, new_text: str = "") -> None:
        textvar = vars.form[self.textV_name]
        textvar.set(new_text)

    def reset(self) -> None:
        textvar = vars.form[self.textV_name]
        textvar.set("")


class ComboBox(GUI):
    def __init__(self, master=None, label_text="", options=None, left_offset=0, top_offset=0) -> None:
        """create a new GUI ComboBox object"""

        super().__init__(master, label_text, left_offset, top_offset)

        self.input_name = (self.input_name).replace("_input", "_combobox")
        self.options = options

        vars.form[self.textV_name] = StringVar(value="no options added" if options is None else 'click to choose')

        vars.form[self.input_name] = ctk.CTkComboBox(
            master,
            width=250,
            height=32,
            border_width=0,
            corner_radius=2,
            bg_color="#fff",
            fg_color="#ddd",
            values=options,
            variable=vars.form[self.textV_name],
        )

        vars.form[self.input_name].place(x=left_offset + 210, y=top_offset + 8)


    def get(self) -> str:
        """returns the first option if nothing was selected"""
        if vars.form[self.textV_name].get() == 'click to choose':
            return self.options[0]
        else:
            return vars.form[self.textV_name].get()


class Entry(GUI):
    def __init__(self, master=None, label_text="", left_offset=0, top_offset=0) -> None:
        """create a new GUI Entry object"""

        super().__init__(master, label_text, left_offset, top_offset)

        self.input_name = (self.input_name).replace("_input", "_entry")

        vars.form[self.textV_name] = StringVar(value="")

        vars.form[self.input_name] = ctk.CTkEntry(
            master,
            width=250,
            height=32,
            border_width=0,
            corner_radius=2,
            bg_color="#fff",
            fg_color="#ddd",
            textvariable=vars.form[self.textV_name],
        )

        vars.form[self.input_name].place(x=left_offset + 210, y=top_offset + 8)


class DatePicker(GUI):
    def __init__(self, master=None, label_text="", left_offset=0, top_offset=0) -> None:
        """create a new GUI DatePicker object"""

        super().__init__(master, label_text, left_offset, top_offset)

        self.month_picker = (self.input_name).replace("_input", "_month")
        self.day_picker = (self.input_name).replace("_input", "_day")
        self.year_picker = (self.input_name).replace("_input", "_year")
        self.today = datetime.datetime.now()

        vars.form[f'{self.textV_name}_month'] = StringVar(value=self.today.strftime("%b"))
        vars.form[f'{self.textV_name}_day'] = StringVar(value=self.today.strftime("%d"))
        vars.form[f'{self.textV_name}_year'] = StringVar(value=self.today.strftime("%Y"))

        vars.form[self.day_picker] = ctk.CTkComboBox(
            master,
            width=70,
            height=32,
            border_width=0,
            corner_radius=2,
            bg_color="#fff",
            fg_color="#ddd",
            values=self.populate_days(),
            variable=vars.form[f'{self.textV_name}_day'],
        )
        vars.form[self.day_picker].place(x=left_offset + 300, y=top_offset + 8)

        vars.form[self.month_picker] = ctk.CTkComboBox(
            master,
            width=80,
            height=32,
            border_width=0,
            corner_radius=2,
            bg_color="#fff",
            fg_color="#ddd",
            values=self.populate_months(),
            variable=vars.form[f'{self.textV_name}_month'],
            command=self.repopulate_days
        )
        vars.form[self.month_picker].place(x=left_offset + 210, y=top_offset + 8)

        vars.form[self.year_picker] = ctk.CTkComboBox(
            master,
            width=80,
            height=32,
            border_width=0,
            corner_radius=2,
            bg_color="#fff",
            fg_color="#ddd",
            values=self.populate_years(),
            variable=vars.form[f'{self.textV_name}_year'],
            command=self.repopulate_days
        )
        vars.form[self.year_picker].place(x=left_offset + 380, y=top_offset + 8)


    # returns a list of days depending on the month
    def populate_days(self) -> list:
        days=[]

        months = {
            "Jan": "31",
            "Feb": "29" if (int(vars.form[f'{self.textV_name}_year'].get()) % 4 == 0) else "28",
            "Mar": "31",
            "Apr": "30",
            "May": "31",
            "Jun": "30",
            "Jul": "31",
            "Aug": "31",
            "Sep": "30",
            "Oct": "31",
            "Nov": "30",
            "Dec": "31",
        }

        selected_month = months[(vars.form[f'{self.textV_name}_month'].get())]

        for i in range(1, int(selected_month)+1):
            days.append(str(i))

        return days


    # returns a list of month names
    def populate_months(self) -> list:
        return ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


    # returns a list of years
    def populate_years(self) -> list:
        years = []

        for i in range(10):
            next_year = int(vars.form[f'{self.textV_name}_year'].get()) - 10 + i
            years.append(str(next_year))

        for i in range(11):
            next_year = int(vars.form[f'{self.textV_name}_year'].get()) + i
            years.append(str(next_year))

        return years


    # recalculates the number of days to pick from, based on the month
    def repopulate_days(self, _) -> None:
        vars.form[self.day_picker].configure(values=self.populate_days())


    # set the date picker back to the current date
    def reset(self) -> None:
        vars.form[f'{self.textV_name}_month'].set(self.today.strftime("%b"))
        vars.form[f'{self.textV_name}_day'].set(self.today.strftime("%d"))
        vars.form[f'{self.textV_name}_year'].set(self.today.strftime("%Y"))


    # return a formatted date
    def get(self) -> str:
        m = vars.form[f'{self.textV_name}_month'].get()
        d = vars.form[f'{self.textV_name}_day'].get()
        y = vars.form[f'{self.textV_name}_year'].get()

        return f"{m} {d}, {y}"


    # set the date 
    def set(self, m: str|int = None, d: str|int = None, y: str|int = None) -> str:
        if m is None:
            m = self.today.strftime("%b")
        if d is None:
            d = self.today.strftime("%d")
        if y is None:
            y = self.today.strftime("%Y")

        if type(m) is str:
            vars.form[f'{self.textV_name}_month'].set(m)
        else:
            monthnames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            vars.form[f'{self.textV_name}_month'].set(monthnames[m])

        vars.form[f'{self.textV_name}_day'].set(str(d))
        vars.form[f'{self.textV_name}_year'].set(str(y))

        return self.get()


class InfoPopup():
    def __init__(self, msg="InfoPopup") -> None:
        CTkMessagebox(title="Info", message=msg)


class ErrorPopup():
    def __init__(self, msg="ErrorPopup") -> None:
        CTkMessagebox(title="Error", message=msg, icon="cancel")


class PromptPopup():
    def __init__(self, msg="PromptPopup", func=lambda:()) -> None:
        self.prompt = CTkMessagebox(title="Confirm", message=msg, icon="question", option_1="Yes", option_2="Cancel")
        self.func = func

        if (self.prompt.get() == "Yes"):
            func()


    def execute(self):
        self.func()


    def get(self):
        return True if self.prompt.get() is "Yes" else False

