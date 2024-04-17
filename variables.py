from tkinter import StringVar
import customtkinter as ctk, os
from PIL import Image
from path_manager import resource_path


## initalize the variables to be used throughout the app
def init():
    global screen_sizes, form, root, popups, cwd, icons, font_family, label_counter, combobox_counter
    global guest_fields, host_fields, finances_fields

    cwd = os.getcwd()

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    root.resizable(False, False)
    font_family = ctk.CTkFont(family="Roboto Bold")

    screen_sizes = {"ws": root.winfo_screenwidth(), "hs": root.winfo_screenheight()}
    form = {"version": "v1.0.0"}
    popups = {"printer": None, "history": None, "elem": {}}

    icons = {}
    icons_specs = {
        "folder": None,
        "clear": None,
        "docx": None,
    }

    # define the
    for icon_name in list(icons_specs.keys()):
        try:
            icons_specs[icon_name] = Image.open(resource_path("assets\\icons\\" + icon_name + ".png"))
            img_size = icons_specs[icon_name].size
            img_ratio = img_size[0]/img_size[1]

            icons[icon_name] = ctk.CTkImage(
                light_image=None,
                dark_image=icons_specs[icon_name],
                size=(25*img_ratio, 25),
            )
        except Exception as e:
            pass

    label_counter = 0
    combobox_counter = 0

    guest_fields = {}

    for idx in range(3):
        guest_fields[f'guest{idx+1}_entry_name'] = None
        guest_fields[f'guest{idx+1}_entry_birth'] = None
        guest_fields[f'guest{idx+1}_entry_citizenship'] = None
        guest_fields[f'guest{idx+1}_entry_passport'] = None
        guest_fields[f'guest{idx+1}_entry_address'] = None
        guest_fields[f'guest{idx+1}_entry_phone'] = None
        guest_fields[f'guest{idx+1}_entry_occupation'] = None
        guest_fields[f'guest{idx+1}_entry_purpose'] = None
        guest_fields[f'guest{idx+1}_entry_arrival'] = None
        guest_fields[f'guest{idx+1}_entry_departure'] = None
        guest_fields[f'guest{idx+1}_entry_relationship_to_host1'] = None
        guest_fields[f'guest{idx+1}_entry_canadian_address'] = None

    host_fields = {
        "host1_entry_relation_to_host2": None,
        "host2_entry_relation_to_host1": None,
    }

    for idx in range(2):
        host_fields[f'host{idx+1}_entry_name'] = None
        host_fields[f'host{idx+1}_entry_birth'] = None
        host_fields[f'host{idx+1}_entry_status'] = None
        host_fields[f'host{idx+1}_entry_passport'] = None
        host_fields[f'host{idx+1}_entry_address'] = None
        host_fields[f'host{idx+1}_entry_phone'] = None
        host_fields[f'host{idx+1}_entry_occupation'] = None
        host_fields[f'host{idx+1}_entry_email'] = None

    finances_fields = {
        "finances_combo_bearer_of_expenses": None,
        "finances_entry_attached_documents": None,
    }

