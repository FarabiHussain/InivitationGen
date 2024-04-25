from tkinter import StringVar
import customtkinter as ctk, os
from PIL import Image
from path_manager import resource_path


# initalize the variables to be used throughout the app
def init():
    global screen_sizes, form, root, popups, cwd, icons, font_family, generic_counter, field_dicts
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("dark-blue")

    cwd = os.getcwd()
    root = ctk.CTk()
    root.resizable(False, False)
    font_family = ctk.CTkFont(family="Roboto Bold")
    screen_sizes = {"ws": root.winfo_screenwidth(), "hs": root.winfo_screenheight()}
    form = {"version": "v0.0.3"}
    popups = {"printer": None, "history": None, "elem": {}}
    icons = populate_icons()
    generic_counter = 0

    field_dicts = []
    field_dicts.append(define_guest_fields())
    field_dicts.append(define_host_fields())
    # field_dicts.append(define_finances_fields())


def define_guest_fields():
    fields = {}

    for i in range(3):
        fields[f'guest{i+1}_entry_name'] = None
        fields[f'guest{i+1}_datepicker_birth'] = None
        fields[f'guest{i+1}_entry_citizenship'] = None
        fields[f'guest{i+1}_entry_passport_number'] = None
        fields[f'guest{i+1}_entry_address'] = None
        fields[f'guest{i+1}_entry_phone'] = None
        fields[f'guest{i+1}_entry_occupation'] = None
        fields[f'guest{i+1}_entry_purpose'] = None
        fields[f'guest{i+1}_entry_relationship_to_host1'] = None
        fields[f'guest{i+1}_entry_canadian_address'] = None

        if i==0:
            fields[f'guest{i+1}_datepicker_arrival'] = None
            fields[f'guest{i+1}_datepicker_departure'] = None

    return fields


def define_host_fields():
    fields = {}

    for i in range(2):
        fields[f'host{i+1}_entry_name'] = None
        fields[f'host{i+1}_datepicker_birth'] = None
        fields[f'host{i+1}_entry_status'] = None
        fields[f'host{i+1}_entry_passport_number'] = None
        fields[f'host{i+1}_entry_address'] = None
        fields[f'host{i+1}_entry_phone'] = None
        fields[f'host{i+1}_entry_occupation'] = None
        fields[f'host{i+1}_entry_email'] = None

        # fields only in host1
        if i==0:
            fields["host1_entry_relationship_to_host2"] = None
            fields[f"host{i+1}_combo_bearer_of_expenses"] = None,
            fields[f"host{i+1}_entry_attached_documents"] = None,

        # fields only in host2
        elif i==1:
            fields["host2_entry_relationship_to_host1"] = None

    return fields


def populate_icons():
    icons = {"folder": None, "clear": None, "docx": None, "test": None}

    for icon_name in list(icons.keys()):
        try:
            icons[icon_name] = Image.open(resource_path("assets\\icons\\" + icon_name + ".png"))
            img_size = icons[icon_name].size
            img_ratio = img_size[0]/img_size[1]

            icons[icon_name] = ctk.CTkImage(
                light_image=None,
                dark_image=icons[icon_name],
                size=(25*img_ratio, 25),
            )
        except Exception as e:
            pass

    return icons