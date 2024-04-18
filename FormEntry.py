import variables as vars
import customtkinter as ctk
from tkinter import StringVar


class FormEntry:
    def __init__(self, master=None, label_text="", left_offset=0, top_offset=0) -> None:
        """create a new label and entry field"""

        # no label text was passed
        if label_text == "":
            label_text = f"FormEntry{vars.label_counter}"
            vars.label_counter += 1

        # name the variables based on label text
        prefix = label_text.replace(" ", "_").lower()
        self.textV_name = f"{prefix}_textVariable"
        self.input_name = f"{prefix}_input"

        short_label = label_text.replace("guest1 ", "").replace("guest2 ", "").replace("guest3 ", "").replace("host1 ", "").replace("host2 ", "").replace("finances ", "")
        short_label = short_label.replace( "entry ", "").replace("combo ", "")

        ctk.CTkLabel(
            master, text=short_label, font=vars.font_family
        ).place(x=left_offset + 10, y=top_offset + 10)

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

    def get(self) -> str:
        """return the entry's data as string"""
        field = vars.form[self.input_name]
        return field.get()

    def set(self, new_text: str = "") -> None:
        """set the entry's data"""
        textvar = vars.form[self.textV_name]
        textvar.set(new_text)

    def reset(self) -> None:
        """reset the entry's data"""
        textvar = vars.form[self.textV_name]
        textvar.set("")

