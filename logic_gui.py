from tkinter import StringVar
import variables as vars
import customtkinter as ctk
import re, names, random
from CTkMessagebox import CTkMessagebox as popup
from icecream import ic


# reset all input fields and delete all receipt items
def clear_fields():
    for current_dict in [vars.guest_fields, vars.host1_fields, vars.host2_fields]:
        for elem in current_dict.keys():
            current_dict[elem].reset()


def testfill_fields():
    host1_gender = random.choice(['male', 'female'])
    host2_gender = 'male' if host1_gender == 'female' else 'female'
    host1_name = names.get_full_name(gender=host1_gender)
    host2_name = names.get_full_name(gender=host2_gender)
    guest_name = names.get_full_name(gender=random.choice(['male', 'female']))

    vars.guest_fields["guest_name"].set(guest_name)
    vars.guest_fields["guest_birth"].set("January 1st, 1994")
    vars.guest_fields["guest_citizenship"].set("United Kingdom")
    vars.guest_fields["guest_passport"].set("XXXXXXXXX")
    vars.guest_fields["guest_address"].set("100 Some Place, City, Country")
    vars.guest_fields["guest_phone"].set(random.choice(["431", "204"]) + str(random.randint(1000000, 9999999)))
    vars.guest_fields["guest_occupation"].set("Student")
    vars.guest_fields["guest_purpose"].set("Visit")
    vars.guest_fields["guest_arrival"].set("April 30, 2024")
    vars.guest_fields["guest_departure"].set("April 15, 2024")
    vars.guest_fields["guest_relationship"].set("brother")
    vars.guest_fields["guest_canadian_address"].set("100 Random Street, Winnipeg, MB")

    vars.host1_fields["host_1_name"].set(host1_name)
    vars.host1_fields["host_1_birth"].set("January 1st, 1990")
    vars.host1_fields["host_1_status"].set("Citizen")
    vars.host1_fields["host_1_passport"].set("YYYYYYYYY")
    vars.host1_fields["host_1_address"].set("100 Random Street, Winnipeg, MB")
    vars.host1_fields["host_1_phone"].set(host1_name.replace(" ", "").lower() + "@email.com")
    vars.host1_fields["host_1_occupation"].set("Project Manager")
    vars.host1_fields["host_1_email"].set(random.choice(["431", "204"]) + str(random.randint(1000000, 9999999)))
    vars.host1_fields["host_1_relation_to_host_2"].set("wife")

    vars.host2_fields["host_2_name"].set(host2_name)
    vars.host2_fields["host_2_birth"].set("December 31, 1992")
    vars.host2_fields["host_2_status"].set("Citizen")
    vars.host2_fields["host_2_passport"].set("ZZZZZZZZZ")
    vars.host2_fields["host_2_address"].set("100 Random Street, Winnipeg, MB")
    vars.host2_fields["host_2_phone"].set(host1_name.replace(" ", "").lower() + "@email.com")
    vars.host2_fields["host_2_occupation"].set("Health Care Worker")
    vars.host2_fields["host_2_email"].set(random.choice(["431", "204"]) + str(random.randint(1000000, 9999999)))
    vars.host2_fields["host_2_relation_to_host_1"].set("husband")


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