from tkinter import StringVar
import docx, os
import variables as vars
import customtkinter as ctk
from icecream import ic
from tabview import *
from logic_document import *
from logic_gui import *
from path_manager import *
from form_entry import *

##############################################################################################
## INITIALIZATION
##############################################################################################

vars.init()

# calculate x and y coordinates for the Tk root window
h = 620
w = 520
x = (vars.screen_sizes['ws']/2) - (w/2)
y = (vars.screen_sizes['hs']/2) - (h/2)

os.system("cls")
vars.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

try:
    vars.root.iconbitmap(resource_path("assets\\icons\\logo.ico"))
except Exception as e:
    pass

vars.root.configure(fg_color='white')
vars.root.title(f"AMCAIM Lettr ({vars.form['version']})")

cwd = os.getcwd()
font_family = vars.font_family

try:
    document = docx.Document(resource_path(cwd + "\\assets\\templates\\double.docx"))
except Exception as e:
    pass

##############################################################################################
## FRAMES
##############################################################################################

container = Tabview(vars.root, ["Guest", "Host 1", "Host 2"])
container_tabs = container.get_tabs()

screen_w = str(vars.screen_sizes['ws'])
screen_h = str(vars.screen_sizes['hs'])

header_font = ctk.CTkFont(family="Roboto Bold", size=20)
vars.form['guest_frame'] = ctk.CTkFrame(container_tabs['Guest'], corner_radius=4, fg_color='#ffffff')
vars.form['guest_frame'].pack(expand=True, fill="both", padx=10, pady=10)
vars.form['host1_frame'] = ctk.CTkFrame(container_tabs['Host 1'], corner_radius=4, fg_color='#ffffff')
vars.form['host1_frame'].pack(expand=True, fill="both", padx=10, pady=10)
vars.form['host2_frame'] = ctk.CTkFrame(container_tabs['Host 2'], corner_radius=4, fg_color='#ffffff')
vars.form['host2_frame'].pack(expand=True, fill="both", padx=10, pady=10)

##############################################################################################
## INPUT SECTION
##############################################################################################

field_dicts = [vars.guest_fields, vars.host1_fields, vars.host2_fields]
field_frames = ['guest_frame', 'host1_frame', 'host2_frame']

for current_dict, current_frame in zip(field_dicts, field_frames):
    for index, field in enumerate(current_dict.keys()):
        entry_label = field.replace("_", " ")
        current_dict[field] = FormEntry(master=vars.form[current_frame], label_text=entry_label, left_offset=5, top_offset=40*index)

##############################################################################################
## BUTTONS
##############################################################################################

vars.form['test_btn'] = ctk.CTkButton(vars.root, text="TEST", border_width=0, corner_radius=2, command=lambda:testfill_fields(), width=72, height=36)
vars.form['clear_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['clear'], border_width=0, corner_radius=2, fg_color="#c41212", command=lambda:clear_fields(), width=72, height=36)
vars.form['docx_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['docx'], border_width=0, corner_radius=2, fg_color="#383FBC", command=lambda:process_docs(), width=72, height=36)
# vars.form['output_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['folder'], border_width=0, corner_radius=2, fg_color="#808080", command=lambda:os.startfile(cwd + "\\output"), width=72, height=36)

vars.form['test_btn'].place(x=w-470, y=h-60)
vars.form['clear_btn'].place(x=w-380, y=h-60)
vars.form['docx_btn'].place(x=w-290, y=h-60)
# vars.form['output_btn'].place(x=w-200, y=h-60)


vars.root.mainloop()