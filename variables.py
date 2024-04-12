from tkinter import StringVar
import customtkinter as ctk, os
from PIL import Image
from path_manager import resource_path


## initalize the variables to be used throughout the app
def init():
    global screen_sizes, form, root, popups, cwd, icons, font_family, label_counter
    global  guest_fields, host1_fields, host2_fields

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
            icons_specs[icon_name] = Image.open(
                resource_path("assets\\icons\\" + icon_name + ".png")
            )

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

    guest_fields = {
        "guest_name": None,
        "guest_birth": None,
        "guest_citizenship": None,
        "guest_passport": None,
        "guest_address": None,
        "guest_phone": None,
        "guest_occupation": None,
        "guest_purpose": None,
        "guest_arrival": None,
        "guest_departure": None,
        "guest_relationship": None,
        "guest_canadian_address": None,
    }

    host1_fields = {
        "host1_name": None,
        "host1_birth": None,
        "host1_status": None,
        "host1_passport": None,
        "host1_address": None,
        "host1_phone": None,
        "host1_occupation": None,
        "host1_email": None,
        "host1_relation_to_host2": None,
    }

    host2_fields = {
        "host2_name": None,
        "host2_birth": None,
        "host2_status": None,
        "host2_passport": None,
        "host2_address": None,
        "host2_phone": None,
        "host2_occupation": None,
        "host2_email": None,
        "host2_relation_to_host1": None,
    }

