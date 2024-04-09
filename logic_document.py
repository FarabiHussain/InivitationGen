import os
import datetime
import variables as vars
from docx import Document
from CTkMessagebox import CTkMessagebox as popup
from path_manager import resource_path
from utils import *
from icecream import ic


## initializes the fill info, output and input files
def init():
    # date_on_document = datetime.datetime.strptime(vars.form['document_date'], '%d/%m/%Y')
    date_on_document = datetime.datetime.now()

    form_data = {
        '[DAY]': format_day(date_on_document.strftime("%d")),
        '[MONTH]': date_on_document.strftime("%B"),
        '[YEAR]': date_on_document.strftime("%Y"),
    }

    # include client 2 if the name is filled
    # TO-DO

    # set the input and output files
    input_file = resource_path("assets\\templates\\double.docx")
    output_file = f"Invitation & Declaration - {vars.guest_fields['guest_name'].get()}.docx"

    form_data['[HOST1_NAME]'] = vars.host1_fields['host_1_name'].get()
    form_data['[HOST1_BIRTH]'] = vars.host1_fields['host_1_birth'].get()
    form_data['[HOST1_ADDRESS]'] = vars.host1_fields['host_1_address'].get()
    form_data['[GUEST_NAME]'] = vars.guest_fields['guest_name'].get()
    form_data['[GUEST_BIRTH]'] = vars.guest_fields['guest_birth'].get()
    form_data['[GUEST_PASSPORT]'] = vars.guest_fields['guest_passport'].get()

    # form_data['[EMAIL1]'] = vars.form["email_address_1"]
    # form_data['[PHONE1]'] = format_phone(vars.form["phone_number_1"])

    return {
        'form_data': form_data, 
        'input_file': input_file, 
        'output_file': output_file
    }


## generate the docx with the input info
def process_docs():

    init_data = None
    doc = None

    # initiate the data and document
    try:
        init_data = init()
        ic(init_data)
        doc = Document(init_data['input_file'])
    except Exception as e:
        popup(title="", message='Exception in init(): ' + str(e), corner_radius=4)
        return False

    # edit the document 

    current_replace = ""

    try:
        for paragraph in doc.paragraphs:
            for key, value in init_data['form_data'].items():
                if key in paragraph.text:
                    for run in paragraph.runs:
                        current_replace = value
                        run.text = run.text.replace(key, value)

    except Exception as e:
        # popup(title="", message='Exception while editing document: ' + str(e), corner_radius=4)
        popup(title="", message='Exception while editing document: ' + current_replace, corner_radius=4)
        return False

    # set up folders and save files, print if needed
    try:
        # set up the output directory
        output_dir = os.getcwd() + "\\output\\"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # save the file to the output folder
        doc.save(output_dir + init_data['output_file'])

        # open the word file
        os.startfile(output_dir + init_data['output_file'])

        # return the filename
        return init_data['output_file']

    except Exception as e:
        print('Exception: ' + str(e))
        popup(title="", message='Exception: ' + str(e), corner_radius=4)
        return False

