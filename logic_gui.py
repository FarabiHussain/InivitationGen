from tkinter import StringVar
import variables as vars
import customtkinter as ctk
import re, names, random
from CTkMessagebox import CTkMessagebox as popup
from icecream import ic


# reset all input fields and delete all receipt items
def clear_fields():
    for current_dict in vars.field_dicts:
        for elem in current_dict.keys():
            current_dict[elem].reset()
    return


# populate fields with random dummy data for testing
def testfill_fields():
    clear_fields()

    guest_fields = vars.field_dicts[0]
    host_fields = vars.field_dicts[1]

    host1_gender = 'male'
    host2_gender = 'female'
    host_names = [names.get_full_name(gender=host1_gender), names.get_full_name(gender=host2_gender)]
    guest_names = [
        names.get_full_name(gender=random.choice(['male', 'female'])),
        names.get_full_name(gender=random.choice(['male', 'female'])),
        names.get_full_name(gender=random.choice(['male', 'female'])),
    ]


    for i in range(1):
        guest_fields[f"guest{i+1}_entry_name"].set(guest_names[i])
        guest_fields[f"guest{i+1}_datepicker_birth"].set(m=random.randint(0,11), d=random.randint(1,28), y=random.randint(2000,2010))
        guest_fields[f"guest{i+1}_entry_citizenship"].set("United Kingdom")
        guest_fields[f"guest{i+1}_entry_passport_number"].set(f"{str(random.randint(1000000, 9999999))}")
        guest_fields[f"guest{i+1}_entry_address"].set("3 Richmond Road, London, WC10 3YT, UK")
        guest_fields[f"guest{i+1}_entry_phone"].set(f"{random.choice(["431", "204"])}{str(random.randint(1000000, 9999999))}")
        guest_fields[f"guest{i+1}_entry_occupation"].set("Student")
        guest_fields[f"guest{i+1}_entry_purpose"].set("Visit")
        guest_fields[f"guest{i+1}_entry_relationship_to_host1"].set("Sibling")
        guest_fields[f"guest{i+1}_entry_canadian_address"].set("3386 St Mary's Rd, Winnipeg, MB R3B 3K6")

    guest_fields[f"guest1_datepicker_arrival"].set(m="Aug", d=15, y=2024)
    guest_fields[f"guest1_datepicker_departure"].set(m="Aug", d=30, y=2024)

    for i in range(2):
        host_fields[f"host{i+1}_entry_name"].set(host_names[i])
        host_fields[f"host{i+1}_datepicker_birth"].set(m=random.randint(0,11), d=random.randint(1,28), y=random.randint(1970,2000))
        host_fields[f"host{i+1}_entry_status"].set("Citizen")
        host_fields[f"host{i+1}_entry_passport_number"].set("YYYYYYYYY")
        host_fields[f"host{i+1}_entry_address"].set("3386 St Mary's Rd, Winnipeg, MB R3B 3K6")
        host_fields[f"host{i+1}_entry_email"].set(host_names[i].replace(" ", "").lower() + "@email.com")
        host_fields[f"host{i+1}_entry_occupation"].set("Project Manager")
        host_fields[f"host{i+1}_entry_phone"].set(random.choice(["431", "204"]) + str(random.randint(1000000, 9999999)))
        host_fields[f"host{1 if i == 0 else 2}_entry_relationship_to_host{2 if i == 0 else 1}"].set("Husband" if i == 0 else "Wife" )


# perform a check for the presence of special characters
def check_special(variables, is_string = False):
    special_chars_list = ["\\", "/", ":", "*", "?", "\"", "<", ">" ,"|"]

    if (is_string is False):
        special_chars_list.append(",")
        special_chars_list.append(" ")

    for var in variables:
        if any(bad_char in var for bad_char in special_chars_list):
            popup(title="", message=f'The following special characters cannot be used:\n{(" ").join(special_chars_list)}', corner_radius=2)
            return False
        
    return True


# perform a check for the presence of alphabets in the fields
def check_alphabets(variables: list):
    for var in variables:
        if re.search('[A-Za-z]', var) is not None:
            popup(title="", message=f'Only Client and Desc fields can contain alphabets.', corner_radius=2)
            return False
        
    return True


# perform a check for an empty string
def check_empty(variables: list):
    for var in variables:
        if len(var) < 1:
            popup(title="", message=f'Fields must not be empty.', corner_radius=2)
            return False

    return True