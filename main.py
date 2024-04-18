import docx, os
import variables as vars
import customtkinter as ctk
from icecream import ic
from tabview import *
from logic_document import *
from logic_gui import *
from path_manager import *
from FormEntry import *
from FormCombo import *

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
vars.root.title(f"AMCAIM Invitation Generator ({vars.form['version']})")

cwd = os.getcwd()
font_family = vars.font_family

try:
    document = docx.Document(resource_path(cwd + "\\assets\\templates\\double.docx"))
except Exception as e:
    pass

##############################################################################################
## FRAMES
##############################################################################################

container = Tabview(
    vars.root, 
    [
        "Guest 1", 
        "Guest 2", 
        "Guest 3", 
        "Host 1", 
        "Host 2", 
        "Finances"
    ]
)

container_tabs = container.get_tabs()

screen_w = str(vars.screen_sizes['ws'])
screen_h = str(vars.screen_sizes['hs'])

header_font = ctk.CTkFont(family="Roboto Bold", size=20)
vars.form['guest1_frame'] = ctk.CTkFrame(container_tabs['Guest 1'], corner_radius=4, fg_color='#ffffff')
vars.form['guest1_frame'].pack(expand=True, fill="both", padx=10, pady=10)
vars.form['guest2_frame'] = ctk.CTkFrame(container_tabs['Guest 2'], corner_radius=4, fg_color='#ffffff')
vars.form['guest2_frame'].pack(expand=True, fill="both", padx=10, pady=10)
vars.form['guest3_frame'] = ctk.CTkFrame(container_tabs['Guest 3'], corner_radius=4, fg_color='#ffffff')
vars.form['guest3_frame'].pack(expand=True, fill="both", padx=10, pady=10)
vars.form['host1_frame'] = ctk.CTkFrame(container_tabs['Host 1'], corner_radius=4, fg_color='#ffffff')
vars.form['host1_frame'].pack(expand=True, fill="both", padx=10, pady=10)
vars.form['host2_frame'] = ctk.CTkFrame(container_tabs['Host 2'], corner_radius=4, fg_color='#ffffff')
vars.form['host2_frame'].pack(expand=True, fill="both", padx=10, pady=10)
vars.form['finances_frame'] = ctk.CTkFrame(container_tabs['Finances'], corner_radius=4, fg_color='#ffffff')
vars.form['finances_frame'].pack(expand=True, fill="both", padx=10, pady=10)

##############################################################################################
## INPUT SECTION
##############################################################################################

field_dicts = [
    vars.guest_fields, 
    vars.host_fields, 
    vars.finances_fields
]

for current_dict in field_dicts:
    offset = 0

    for field_idx, field in enumerate(current_dict.keys()):

        # keep track of these for component names and positions
        entry_label = field.replace("_", " ")
        prev_frame = f"{list(current_dict.keys())[field_idx-1].split("_")[0]}_frame"
        curr_frame = f'{field.split("_")[0]}_frame'

        # reset the offset from top when a new frame is reached
        is_new_frame = prev_frame != curr_frame
        if is_new_frame:
            offset = 0

        # display the right component
        if '_combo_' in field:
            current_dict[field] = FormCombo(
                master=vars.form[curr_frame], 
                label_text=entry_label, 
                options=[
                    "paid for by me and will be my responsibility.", 
                    "their own responsibility and will be paid for by themselves. I will provide additional support if any assistance is needed."
                ], 
                left_offset=5, 
                top_offset=40*offset
            )

        elif '_entry_' in field:
            current_dict[field] = FormEntry(
                master=vars.form[curr_frame], 
                label_text=entry_label, 
                left_offset=5, 
                top_offset=40*offset
            )

        offset += 1



##############################################################################################
## BUTTONS
##############################################################################################

vars.form['test_btn'] = ctk.CTkButton(vars.root, text="", border_width=0, corner_radius=2, command=lambda:testfill_fields(), width=72, height=36)
vars.form['clear_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['clear'], border_width=0, corner_radius=2, fg_color="#c41212", command=lambda:clear_fields(), width=72, height=36)
vars.form['docx_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['docx'], border_width=0, corner_radius=2, fg_color="#383FBC", command=lambda:generate_doc(), width=72, height=36)
vars.form['output_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['folder'], border_width=0, corner_radius=2, fg_color="#808080", command=lambda:os.startfile(cwd + "\\output"), width=72, height=36)

vars.form['test_btn'].place(x=w-105, y=h-60)
vars.form['clear_btn'].place(x=w-485, y=h-60)
vars.form['docx_btn'].place(x=w-395, y=h-60)
vars.form['output_btn'].place(x=w-305, y=h-60)

testfill_fields()
generate_doc()
# vars.root.mainloop()
# vars.root.after(1000, lambda: vars.root.quit())
# vars.root.after(1000, lambda: vars.root.destroy())