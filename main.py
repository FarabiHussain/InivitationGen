from tkinter import StringVar
import docx, os
import variables as vars
import customtkinter as ctk
from logic_document import *
from document_utils import *
from logic_records import *
from logic_gui import *
from path_manager import *
from form_entry import *

##############################################################################################
## INITIALIZATION
##############################################################################################

vars.init()

# calculate x and y coordinates for the Tk root window
h = 800
w = 1520
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
document = docx.Document(resource_path(cwd + "\\assets\\templates\\receipt.docx"))

##############################################################################################
## FRAMES
##############################################################################################

screen_w = str(vars.screen_sizes['ws'])
screen_h = str(vars.screen_sizes['hs'])

header_font = ctk.CTkFont(family="Roboto Bold", size=20)
ctk.CTkLabel(vars.root, text="Guest Information", font=header_font).place(x=190, y=20)
ctk.CTkLabel(vars.root, text="Host 1 Information", font=header_font).place(x=700, y=20)
ctk.CTkLabel(vars.root, text="Host 2 Information", font=header_font).place(x=1220, y=20)
vars.form['guest_frame'] = ctk.CTkFrame(vars.root, corner_radius=2, border_width=1, width=480, height=490, fg_color='#ffffff')
vars.form['guest_frame'].place(x=20, y=60)
vars.form['host1_frame'] = ctk.CTkFrame(vars.root, corner_radius=2, border_width=1, width=480, height=490, fg_color='#ffffff')
vars.form['host1_frame'].place(x=520, y=60)
vars.form['host2_frame'] = ctk.CTkFrame(vars.root, corner_radius=2, border_width=1, width=480, height=490, fg_color='#ffffff')
vars.form['host2_frame'].place(x=1020, y=60)

##############################################################################################
## INPUT SECTION
##############################################################################################

guest_fields = {
    "Guest Full Name": None,
    "Guest Date of Birth": None,
    "Guest Citizenship": None,
    "Guest Passport Number": None,
    "Guest Residential Address": None,
    "Guest Phone Number": None,
    "Guest Current Occupation": None,
    "Guest Purpose of Visit": None,
    "Guest Arrival Date": None,
    "Guest Departure Date": None,
    "Guest Relationship to Host": None,
    "Guest Address in Canada": None,
}

host1_fields = {
    "Host 1 Full Name": None,
    "Host 1 Date of Birth": None,
    "Host 1 Status in Canada": None,
    "Host 1 Passport Number": None,
    "Host 1 Residential Address": None,
    "Host 1 Phone Number": None,
    "Host 1 Current Occupation": None,
    "Host 1 Email Address": None,
    "Host 1 Relationship to Host 2": None,
}

host2_fields = {
    "Host 2 Full Name": None,
    "Host 2 Date of Birth": None,
    "Host 2 Status in Canada": None,
    "Host 2 Passport Number": None,
    "Host 2 Residential Address": None,
    "Host 2 Phone Number": None,
    "Host 2 Current Occupation": None,
    "Host 2 Email Address": None,
    "Host 2 Relationship to Host 1": None,
}

for index, field in enumerate(guest_fields.keys()):
    guest_fields[field] = FormEntry(master=vars.form['guest_frame'], label_text=field, left_offset=5, top_offset=40*index)

for index, field in enumerate(host1_fields.keys()):
    host1_fields[field] = FormEntry(master=vars.form['host1_frame'], label_text=field, left_offset=5, top_offset=55*index)

for index, field in enumerate(host2_fields.keys()):
    host2_fields[field] = FormEntry(master=vars.form['host2_frame'], label_text=field, left_offset=5, top_offset=55*index)



##############################################################################################
## BUTTONS
##############################################################################################

def test():
    print(guest_fields["Guest Full Name"].get())

vars.form['add_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['add_item'], border_width=0, corner_radius=2, fg_color="#38bc41", command=lambda:test(), width=72, height=36)
# vars.form['add_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['add_item'], border_width=0, corner_radius=2, fg_color="#38bc41", command=lambda:add_item(), width=72, height=36)
# vars.form['clear_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['clear'], border_width=0, corner_radius=2, fg_color="#c41212", command=lambda:clear_fields(), width=72, height=36)
# vars.form['docx_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['docx'], border_width=0, corner_radius=2, fg_color="#383FBC", command=lambda:generate_invoice(cwd), width=72, height=36)
# vars.form['output_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['folder'], border_width=0, corner_radius=2, fg_color="#808080", command=lambda:os.startfile(cwd + "\\output"), width=72, height=36)

vars.form['add_btn'].place(x=20, y=h-55)
# vars.form['clear_btn'].place(x=102, y=h-55)
# vars.form['docx_btn'].place(x=182, y=h-55)
# vars.form['output_btn'].place(x=263, y=h-55)


vars.root.mainloop()