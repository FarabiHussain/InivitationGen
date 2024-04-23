import os
import datetime
import variables as vars
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from path_manager import resource_path
from doc_modifier import *
from icecream import ic
from Entity import *


# initializes the fill info, output and input files
def initialize_data():
    global entities

    date_on_document = datetime.datetime.now()
    initialize_entities()

    form_data = {
        '[DAY]': format_day(date_on_document.strftime("%d")),
        '[MONTH]': date_on_document.strftime("%B"),
        '[YEAR]': date_on_document.strftime("%Y"),
    }

    form_data['[GUEST_INFO]'] = ""

    for host, label in zip(entities.values(), entities.keys()):
        if "host" in label and host is not None:

            i = label.replace("host_", "")

            form_data[f'[HOST{i}_NAME]'] = host.get('name')
            form_data[f'[HOST{i}_BIRTH]'] = host.get('birth')
            form_data[f'[HOST{i}_STATUS]'] = host.get('status')
            form_data[f'[HOST{i}_PASSPORT]'] = host.get('passport')
            form_data[f'[HOST{i}_ADDRESS]'] = host.get('address')
            form_data[f'[HOST{i}_PHONE]'] = host.get('phone')
            form_data[f'[HOST{i}_OCCUPATION]'] = host.get('occupation')
            form_data[f'[HOST{i}_EMAIL]'] = host.get('email')
            form_data[f'[HOST{i}_RELATION_TO_HOST{"2" if i=="1" else "1"}]'] = host.get('relation_to_other_host').lower()
            form_data['[BEARER]'] = host.get('bearer')

    for guest, label in zip(entities.values(), entities.keys()):
        if "guest" in label and guest is not None:

            i = label.replace("guest_", "")

            form_data['[GUEST_NAMES]'] = format_collective_names(entities)
            form_data['[GUEST_INFO]'] += f"\n{guest.get('name')}, born {guest.get('birth')}, Passport Number {guest.get('passport')}"
            form_data[f'[GUEST{i}_BIRTH]'] = guest.get('birth')
            form_data[f'[GUEST{i}_CITIZENSHIP]'] = guest.get('citizenship')
            form_data[f'[GUEST{i}_PASSPORT]'] = guest.get('passport')
            form_data[f'[GUEST{i}_ADDRESS]'] = guest.get('address')
            form_data[f'[GUEST{i}_PHONE]'] = guest.get('phone')
            form_data[f'[GUEST{i}_OCCUPATION]'] = guest.get('occupation')
            form_data[f'[GUEST{i}_RELATIONSHIP]'] = guest.get('relationship_to_host1')
            form_data[f'[GUEST{i}_CANADIAN_ADDRESS]'] = guest.get('canadian_address')
            form_data[f'[GUEST_PURPOSE]'] = guest.get('purpose')
            form_data[f'[GUEST_ARRIVAL]'] = guest.get('arrival')
            form_data[f'[GUEST_DEPARTURE]'] = guest.get('departure')

    return {
        'form_data': form_data, 
        'input_file': resource_path(f"assets\\templates\\{'2x_host' if entities['host_2'] is not None else '1x_host'}.docx"), 
        'output_file': f"{(datetime.datetime.now().timestamp())}.docx"
    }


# create objects of hosts and guests
def initialize_entities():
    global guests_list, hosts_list, entities

    guests_list = []
    hosts_list = []
    entities = {}

    guest_fields = vars.field_dicts[0]
    host_fields = vars.field_dicts[1]

    # append guests
    for i in [1,2,3]:
        new_guest = (Guest({
            'name': guest_fields[f'guest{i}_entry_name'].get(),
            'birth': guest_fields[f'guest{i}_datepicker_birth'].get(),
            'address': guest_fields[f'guest{i}_entry_address'].get(),
            'phone': guest_fields[f'guest{i}_entry_phone'].get(),
            'occupation': guest_fields[f'guest{i}_entry_occupation'].get(),
            'relationship_to_host1': guest_fields[f'guest{i}_entry_relationship_to_host1'].get(),
            'purpose': guest_fields[f'guest{i}_entry_purpose'].get(),
            'canadian_address': guest_fields[f'guest{i}_entry_canadian_address'].get(),
            'passport': guest_fields[f'guest{i}_entry_passport_number'].get(),
            'citizenship': guest_fields[f'guest{i}_entry_citizenship'].get(),

            # the arrival and departure dates are always the same as guest1
            'arrival': guest_fields[f'guest1_datepicker_arrival'].get(),
            'departure': guest_fields[f'guest1_datepicker_departure'].get(),
        }))

        # if not new_guest.is_empty():
        guests_list.append(new_guest)

    # append hosts
    for i in [1,2]:
        new_host = (Host({
            'name': host_fields[f'host{i}_entry_name'].get(),
            'birth': host_fields[f'host{i}_datepicker_birth'].get(),
            'status': host_fields[f'host{i}_entry_status'].get(),
            'passport': host_fields[f'host{i}_entry_passport_number'].get(),
            'address': host_fields[f'host{i}_entry_address'].get(),
            'phone': host_fields[f'host{i}_entry_phone'].get(),
            'occupation': host_fields[f'host{i}_entry_occupation'].get(),
            'email': host_fields[f'host{i}_entry_email'].get(),
            'relation_to_other_host': host_fields[f'host{"1" if i == 1 else "2"}_entry_relationship_to_host{"2" if i == 1 else "1"}'].get(),

            # the bearer of expenses and attached documents are always the same as host1 
            'bearer': host_fields[f'host1_combo_bearer_of_expenses'].get(),
            'attached': host_fields[f'host1_entry_attached_documents'].get(),
        }))

        # if not new_host.is_empty():
        hosts_list.append(new_host)


    entities = {
        "guest_1": None if guests_list[0].is_empty() else guests_list[0],
        "guest_2": None if guests_list[1].is_empty() else guests_list[1],
        "guest_3": None if guests_list[2].is_empty() else guests_list[2],
        "host_1": None if hosts_list[0].is_empty() else hosts_list[0],
        "host_2": None if hosts_list[1].is_empty() else hosts_list[1],
    }


# generate the docx with the input info
def generate_doc():
    data = None
    doc = None

    # initiate the data and document
    try:
        data = initialize_data()
        doc = Document(data['input_file'])
    except Exception as e:
        ErrorPopup(msg=f'Exception while initializing data:\n\n{str(e)}')
        return False


    # perform checks and take confirmation from the user
    try:
        if not user_confirmation(entities):
            return False
    except Exception as e:
        ErrorPopup(msg=f'Exception while taking user confirmation:\n\n{str(e)}')
        return False


    # replace placeholders on the document
    try:
        current_replace = ""

        for paragraph in doc.paragraphs:
            for key, value in data['form_data'].items():
                if key in paragraph.text:
                    for run in paragraph.runs:
                        current_replace = value
                        run.text = run.text.replace(key, value)
    except Exception as e:
        ErrorPopup(msg=f'Exception while editing document\n\nPlacing {current_replace}\n\n{e}')
        return False

    add_intro(doc)
    add_letter_body(doc)
    add_outro(doc)
    save_doc(doc, data)


# prompts user for confirmation before generating the document
def user_confirmation(entities):

    # escape if either guest 1 or host 1 is empty
    if (entities["guest_1"] is None) or (entities["host_1"] is None):
        ErrorPopup(msg="Guest 1 and Host 1 must not be empty.")
        return False

    # check host 1 relation to host 2
    if (entities["host_2"] is not None) and entities["host_1"].is_prop_blank('relation_to_other_host') is True:
        print(entities["host_2"], entities["host_1"])
        ErrorPopup(msg="Host 1's relationship to Host 2 must not be empty when Host 2 is present.")
        return False

    # check host 1 bearer of expenses
    if entities["host_1"].is_prop_blank('bearer') is True or entities["host_1"].get('bearer') is "click to select":
        ErrorPopup(msg="Bearer of expenses in Host 1 must be selected.")
        return False

    # check host 2 relation to host 1
    if (entities["host_2"] is not None) and entities["host_2"].is_prop_blank('relation_to_other_host') is True:
        print(entities["host_2"], entities["host_1"])
        ErrorPopup(msg="Host 2's relationship to Host 1 must not be empty.")
        return False


    for entity, label in zip(entities.values(), entities.keys()):

        # prompt user is an entity is None
        if entity is None:
            if PromptPopup(msg=f"{label.capitalize()} is empty.\n\nContinue?").get() is not True:
                InfoPopup(msg="Operation cancelled.")
                return False
            
        # check for unfilled fields when entity is not None
        else:
            response, invalid_fields = entity.is_complete()

            if response is not True:
                if PromptPopup(msg=f"The following field(s) in {label.capitalize()} are not filled:\n\n  • {(("\n  • ").join(invalid_fields)).replace("_", " ")}\n\nContinue?").get() is not True:
                    InfoPopup(msg="Operation cancelled.")
                    return False

    return True


# add a paragraph at the beginning of the letter
def add_intro(doc):
    intro_text = (
        f"This letter is to express my " +
        f"interest in inviting {format_collective_names(entities)} to Canada " + 
        f"and to furthermore support their Temporary Resident Visa application."
    )

    if entities['host_2'] is not None:
        intro_text = (
            f"This letter is to express me and my {entities['host_1'].get('relation_to_other_host')}'s " +
            f"interest in inviting {format_collective_names(entities)} to Canada " + 
            f"and to furthermore support their Temporary Resident Visa application."
        )

    insert_paragraph(paragraph=doc.add_paragraph(), text=intro_text)


# adds tables containing hosts amd guests details
def add_letter_body(doc):
    for entity, label in zip(entities.values(), entities.keys()):
        if "host" in label and entity is not None:
            insert_table(
                document=doc, 
                table_heading="\nMy details are as follows," if "1" in label else f"\n\nMy {entity.get('relation_to_other_host')}'s details are as follows,", 
                table_items=[
                    {"label": "Full Name", "info": entity.get('name')},
                    {"label": "Date of Birth", "info": entity.get('birth')},
                    {"label": "Canadian Status", "info": entity.get('status')},
                    {"label": "Passport Number", "info": entity.get('passport')},
                    {"label": "Residential Address", "info": entity.get('address')},
                    {"label": "Phone Number", "info": entity.get('phone')},
                    {"label": "Current Occupation", "info": entity.get('occupation')},
                    {"label": "Email Address", "info": entity.get('email')},
                ]
            )


    for entity, label in zip(entities.values(), entities.keys()):
        if "guest" in label and entity is not None:

            insert_table(
                document=doc, 
                table_heading=f"\n\nThe details of {entity.get('name')} are as follows,", 
                table_items=[
                    {"label": "Full Name", "info": entity.get('name')},
                    {"label": "Date of Birth", "info": entity.get('birth')},
                    {"label": "Citizen of", "info": entity.get('citizenship')},
                    {"label": "Passport No.", "info": entity.get('passport')},
                    {"label": "Residential Address", "info": entity.get('address')},
                    {"label": "Phone Number", "info": entity.get('phone')},
                    {"label": "Current Occupation", "info": entity.get('occupation')},
                    {"label": "Relationship to Inviter", "info": entity.get('relationship_to_host1')},
                    {"label": "Purpose of Visit", "info": entity.get('purpose')},
                    {"label": "Arrival Date", "info": entity.get('arrival')},
                    {"label": "Departure Date", "info": entity.get('departure')},
                    {"label": "Primary Residence in Canada", "info": entity.get('canadian_address')},
                ]
            )


# add a paragraph at the end of the letter
def add_outro(doc):
    outro_text=(
        f"The airfare, travel expenses, would be borne by {format_collective_names(entities)}. " +
        f"All expenses in connection with their visit to Canada will be {entities['host_1'].get("bearer")}. "
    )

    # attached documents
    if len(entities['host_1'].get("attached")) > 0:
        outro_text += f"\n\nAttached with the application are {entities['host_1'].get("attached")}. "

    outro_text += f"\n\nIf any clarification or information is required, please do not hesitate to contact us at our email addresses and phone numbers below."

    insert_paragraph(paragraph=doc.add_paragraph(), text=(outro_text))

    # table for hosts to sign
    insert_table(
        document=doc, 
        table_heading="\n\n\n\n",
        table_items=[
            {"label": "_________________________________", "info": "" if entities['host_2'] is None else "_________________________________"},
            {"label": entities['host_1'].get('name'), "info": "" if entities['host_2'] is None else entities['host_2'].get('name')},
            {"label": entities['host_1'].get('email'), "info": "" if entities['host_2'] is None else entities['host_2'].get('email')},
            {"label": entities['host_1'].get('phone'), "info": "" if entities['host_2'] is None else entities['host_2'].get('phone')},
        ],
        table_props={
            'color': '#ffffff',
            "cell_alignment": [
                WD_ALIGN_PARAGRAPH.LEFT, 
                WD_ALIGN_PARAGRAPH.LEFT
            ]
        }
    )