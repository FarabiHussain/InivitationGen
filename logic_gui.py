from tkinter import StringVar
import variables as vars
import customtkinter as ctk
import re, names, random
from CTkMessagebox import CTkMessagebox as popup
from icecream import ic


# reset all input fields and delete all receipt items
def clear_fields():
    for current_dict in [vars.guest_fields, vars.host_fields, vars.finances_fields]:
        for elem in current_dict.keys():
            current_dict[elem].reset()
    return


#
def testfill_fields():
    host1_gender = 'male'
    host2_gender = 'female'
    host_names = [names.get_full_name(gender=host1_gender), names.get_full_name(gender=host2_gender)]
    guest_names = [
        names.get_full_name(gender=random.choice(['male', 'female'])),
        names.get_full_name(gender=random.choice(['male', 'female'])),
        names.get_full_name(gender=random.choice(['male', 'female'])),
    ]

    for idx in range(3):
        vars.guest_fields[f"guest{idx+1}_entry_name"].set(guest_names[idx])
        vars.guest_fields[f"guest{idx+1}_entry_birth"].set("January 1, 1994")
        vars.guest_fields[f"guest{idx+1}_entry_citizenship"].set("United Kingdom")
        vars.guest_fields[f"guest{idx+1}_entry_passport"].set(f"{str(random.randint(1000000, 9999999))}")
        vars.guest_fields[f"guest{idx+1}_entry_address"].set("100 Some Place, City, Country")
        vars.guest_fields[f"guest{idx+1}_entry_phone"].set(f"{random.choice(["431", "204"])}{str(random.randint(1000000, 9999999))}")
        vars.guest_fields[f"guest{idx+1}_entry_occupation"].set("Student")
        vars.guest_fields[f"guest{idx+1}_entry_purpose"].set("Visit")
        vars.guest_fields[f"guest{idx+1}_entry_arrival"].set("April 15, 2024")
        vars.guest_fields[f"guest{idx+1}_entry_departure"].set("April 30, 2024")
        vars.guest_fields[f"guest{idx+1}_entry_relationship_to_host1"].set("Sibling")
        
        # if (idx == 0 or idx == 1):
        vars.guest_fields[f"guest{idx+1}_entry_canadian_address"].set("100 Random Street, Winnipeg, MB")

    for idx in range(2):
        vars.host_fields[f"host{idx+1}_entry_name"].set(host_names[idx])
        vars.host_fields[f"host{idx+1}_entry_birth"].set("January 1, 1990")
        vars.host_fields[f"host{idx+1}_entry_status"].set("Citizen")
        vars.host_fields[f"host{idx+1}_entry_passport"].set("YYYYYYYYY")
        vars.host_fields[f"host{idx+1}_entry_address"].set("100 Random Street, Winnipeg, MB")
        vars.host_fields[f"host{idx+1}_entry_email"].set(host_names[idx].replace(" ", "").lower() + "@email.com")
        vars.host_fields[f"host{idx+1}_entry_occupation"].set("Project Manager")
        vars.host_fields[f"host{idx+1}_entry_phone"].set(random.choice(["431", "204"]) + str(random.randint(1000000, 9999999)))
        vars.host_fields[f"host{1 if idx == 0 else 2}_entry_relation_to_host{2 if idx == 0 else 1}"].set("Husband" if idx == 0 else "Wife" )

    return


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