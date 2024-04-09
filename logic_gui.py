from tkinter import StringVar
import variables as vars
import customtkinter as ctk
import re
from CTkMessagebox import CTkMessagebox as popup
from icecream import ic


# reset all input fields and delete all receipt items
def clear_fields():
    for current_dict in [vars.guest_fields, vars.host1_fields, vars.host2_fields]:
        for elem in current_dict.keys():
            current_dict[elem].reset()


def testfill_fields():
    
    vars.guest_fields["guest_name"] = None
    vars.guest_fields["guest_birth"] = None
    vars.guest_fields["guest_citizenship"] = None
    vars.guest_fields["guest_passport"] = None
    vars.guest_fields["guest_address"] = None
    vars.guest_fields["guest_phone"] = None
    vars.guest_fields["guest_occupation"] = None
    vars.guest_fields["guest_purpose"] = None
    vars.guest_fields["guest_arrival"] = None
    vars.guest_fields["guest_departure"] = None
    vars.guest_fields["guest_relationship"] = None
    vars.guest_fields["guest_canadian_address"] = None

    vars.host1_fields["host_1_name"] = None
    vars.host1_fields["host_1_birth"] = None
    vars.host1_fields["host_1_status"] = None
    vars.host1_fields["host_1_passport"] = None
    vars.host1_fields["host_1_address"] = None
    vars.host1_fields["host_1_phone"] = None
    vars.host1_fields["host_1_occupation"] = None
    vars.host1_fields["host_1_email"] = None
    vars.host1_fields["host_1_relation_to_host_2"] = None

    vars.host2_fields["host_2_name"] = None
    vars.host2_fields["host_2_birth"] = None
    vars.host2_fields["host_2_status"] = None
    vars.host2_fields["host_2_passport"] = None
    vars.host2_fields["host_2_address"] = None
    vars.host2_fields["host_2_phone"] = None
    vars.host2_fields["host_2_occupation"] = None
    vars.host2_fields["host_2_email"] = None
    vars.host2_fields["host_2_relation_to_host_1"] = None


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