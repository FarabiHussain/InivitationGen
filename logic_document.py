import os
import datetime
import variables as vars
from docx import Document
from docx.shared import Cm as CM
from docx.shared import Pt as PT
from CTkMessagebox import CTkMessagebox as popup
from path_manager import resource_path
from utils import *
from icecream import ic
from docx.enum.text import WD_ALIGN_PARAGRAPH


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
    output_file = f"{vars.guest_fields['guest_name'].get()}_{(datetime.datetime.now().timestamp())}.docx"

    form_data['[GUEST_INFO]'] = f"{vars.guest_fields['guest1_entry_name'].get()}, born {vars.guest_fields['guest1_entry_birth'].get()}, Passport Number {vars.guest_fields['guest1_entry_passport'].get()}"

    if len(vars.guest_fields['guest2_entry_name'].get()) > 0:
        form_data['[GUEST_INFO]'] += f"{vars.guest_fields['guest2_entry_name'].get()}, born {vars.guest_fields['guest2_entry_birth'].get()}, Passport Number {vars.guest_fields['guest2_entry_passport'].get()}"
    if len(vars.guest_fields['guest3_entry_name'].get()) > 0:
        form_data['[GUEST_INFO]'] += f"{vars.guest_fields['guest3_entry_name'].get()}, born {vars.guest_fields['guest3_entry_birth'].get()}, Passport Number {vars.guest_fields['guest3_entry_passport'].get()}"

    for idx in range(3):
        form_data[f'[HOST{idx+1}_NAME]'] = vars.host1_fields['host1_name'].get()
        form_data[f'[HOST{idx+1}_BIRTH]'] = vars.host1_fields['host1_birth'].get()
        form_data[f'[HOST{idx+1}_STATUS]'] = vars.host1_fields['host1_status'].get()
        form_data[f'[HOST{idx+1}_PASSPORT]'] = vars.host1_fields['host1_passport'].get()
        form_data[f'[HOST{idx+1}_ADDRESS]'] = vars.host1_fields['host1_address'].get()
        form_data[f'[HOST{idx+1}_PHONE]'] = vars.host1_fields['host1_phone'].get()
        form_data[f'[HOST{idx+1}_OCCUPATION]'] = vars.host1_fields['host1_occupation'].get()
        form_data[f'[HOST{idx+1}_EMAIL]'] = vars.host1_fields['host1_email'].get()
        form_data[f'[HOST{idx+1}_RELATION_TO_HOST2]'] = vars.host1_fields['host1_relation_to_host2'].get()

    form_data['[HOST2_NAME]'] = vars.host2_fields['host2_name'].get()
    form_data['[HOST2_BIRTH]'] = vars.host2_fields['host2_birth'].get()
    form_data['[HOST2_STATUS]'] = vars.host2_fields['host2_status'].get()
    form_data['[HOST2_PASSPORT]'] = vars.host2_fields['host2_passport'].get()
    form_data['[HOST2_ADDRESS]'] = vars.host2_fields['host2_address'].get()
    form_data['[HOST2_PHONE]'] = vars.host2_fields['host2_phone'].get()
    form_data['[HOST2_OCCUPATION]'] = vars.host2_fields['host2_occupation'].get()
    form_data['[HOST2_EMAIL]'] = vars.host2_fields['host2_email'].get()
    form_data['[HOST2_RELATION_TO_HOST1]'] = vars.host2_fields['host2_relation_to_host1'].get()

    form_data['[GUEST_NAME]'] = vars.guest_fields['guest_name'].get()
    form_data['[GUEST_BIRTH]'] = vars.guest_fields['guest_birth'].get()
    form_data['[GUEST_CITIZENSHIP]'] = vars.guest_fields['guest_citizenship'].get()
    form_data['[GUEST_PASSPORT]'] = vars.guest_fields['guest_passport'].get()
    form_data['[GUEST_ADDRESS]'] = vars.guest_fields['guest_address'].get()
    form_data['[GUEST_PHONE]'] = vars.guest_fields['guest_phone'].get()
    form_data['[GUEST_OCCUPATION]'] = vars.guest_fields['guest_occupation'].get()
    form_data['[GUEST_PURPOSE]'] = vars.guest_fields['guest_purpose'].get()
    form_data['[GUEST_ARRIVAL]'] = vars.guest_fields['guest_arrival'].get()
    form_data['[GUEST_DEPARTURE]'] = vars.guest_fields['guest_departure'].get()
    form_data['[GUEST_RELATIONSHIP]'] = vars.guest_fields['guest_relationship_to_host1'].get()
    form_data['[GUEST_CANADIAN_ADDRESS]'] = vars.guest_fields['guest_canadian_address'].get()

    form_data['[BEARER]'] = vars.finances_fields['bearer_of_expenses'].get()
    form_data['[ATTACHED]'] = vars.finances_fields['attached_documents'].get()

    return {
        'form_data': form_data, 
        'input_file': input_file, 
        'output_file': output_file
    }


## generate the docx with the input info
def generate_doc():
    init_data = None
    doc = None

    # initiate the data and document
    try:
        init_data = init()
        doc = Document(init_data['input_file'])
    except Exception as e:
        popup(title="", message='Exception in init(): ' + str(e), corner_radius=4)
        return False

    # replace placeholders on the document
    try:
        current_replace = ""
        for paragraph in doc.paragraphs:
            for key, value in init_data['form_data'].items():
                if key in paragraph.text:
                    for run in paragraph.runs:
                        current_replace = value
                        run.text = run.text.replace(key, value)
    except Exception as e:
        popup(title="", message=f'Exception while editing document\n\nPlacing {current_replace}\n\n{e}', corner_radius=4)
        return False

    # add the table containing host1's details
    insert_table(
        document=doc, 
        table_heading="\nMy details are as follows.", 
        table_items=[
            {"label": "Full Name", "info": vars.host1_fields['host1_name'].get()},
            {"label": "Date of Birth", "info": vars.host1_fields['host1_birth'].get()},
            {"label": "Canadian Status", "info": vars.host1_fields['host1_status'].get()},
            {"label": "Passport Number", "info": vars.host1_fields['host1_passport'].get()},
            {"label": "Residential Address", "info": vars.host1_fields['host1_address'].get()},
            {"label": "Phone Number", "info": vars.host1_fields['host1_phone'].get()},
            {"label": "Current Occupation", "info": vars.host1_fields['host1_occupation'].get()},
            {"label": "Email Address", "info": vars.host1_fields['host1_email'].get()},
        ]
    )

    # add the table containing host2's details
    insert_table(
        document=doc, 
        table_heading=f"\n\nMy {vars.host1_fields['host1_relation_to_host2'].get()}'s details are as follows.", 
        table_items=[
            {"label": "Full Name", "info": vars.host2_fields['host2_name'].get()},
            {"label": "Date of Birth", "info": vars.host2_fields['host2_birth'].get()},
            {"label": "Canadian Status", "info": vars.host2_fields['host2_status'].get()},
            {"label": "Passport Number", "info": vars.host2_fields['host2_passport'].get()},
            {"label": "Residential Address", "info": vars.host2_fields['host2_address'].get()},
            {"label": "Phone Number", "info": vars.host2_fields['host2_phone'].get()},
            {"label": "Current Occupation", "info": vars.host2_fields['host2_occupation'].get()},
            {"label": "Email Address", "info": vars.host2_fields['host2_email'].get()},
        ]
    )

    doc.add_page_break() 

    # add the table containing guest's details
    insert_table(
        document=doc, 
        table_heading="The details of the invitee are as follows.", 
        table_items=[
            {"label": "Full Name", "info": vars.guest_fields['guest_name'].get()},
            {"label": "Date of Birth", "info": vars.guest_fields['guest_birth'].get()},
            {"label": "Residential Address", "info": vars.guest_fields['guest_address'].get()},
            {"label": "Phone Number", "info": vars.guest_fields['guest_phone'].get()},
            {"label": "Current Occupation", "info": vars.guest_fields['guest_occupation'].get()},
            {"label": "Relationship to Inviter", "info": vars.guest_fields['guest_relationship_to_host1'].get()},
            {"label": "Purpose of Visit", "info": vars.guest_fields['guest_purpose'].get()},
            {"label": "Arrival Date", "info": vars.guest_fields['guest_arrival'].get()},
            {"label": "Departure Date", "info": vars.guest_fields['guest_departure'].get()},
            {"label": "Primary Residence in Canada", "info": vars.guest_fields['guest_canadian_address'].get()},
        ]
    )

    #
    insert_paragraph(
        paragraph=doc.add_paragraph(),
        text=(
            f"\nThe airfare, travel expenses, would be borne by {vars.guest_fields['guest_name'].get()}. " +
            f"All expenses in connection with {vars.guest_fields['guest_name'].get()}’s visit to Canada will be {vars.finances_fields['bearer_of_expenses'].get()}. " +
            f"Attached with the application are {vars.finances_fields['attached_documents'].get()}." +
            f"\n\nIf any clarification or information is required, please do not hesitate to contact us at our email addresses and phone numbers below."
        )
    )

    # add the table containing guest's details
    insert_table(
        document=doc, 
        table_heading="\n\n\n\n",
        table_items=[
            {"label": "_________________________________", "info": "_________________________________"},
            {"label": vars.host1_fields['host1_name'].get(), "info": vars.host2_fields['host2_name'].get()},
            {"label": vars.host1_fields['host1_email'].get(), "info": vars.host2_fields['host2_email'].get()},
            {"label": vars.host1_fields['host1_phone'].get(), "info": vars.host2_fields['host2_phone'].get()},
        ],
        table_props={
            'color': '#ffffff',
            "cell_alignment": [
                WD_ALIGN_PARAGRAPH.LEFT, 
                WD_ALIGN_PARAGRAPH.LEFT
            ]
        }
    )

    # create the output file
    save_doc(doc, init_data)

# set up folders and save files, print if needed
def save_doc(doc, init_data):
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
        ic(e)
        popup(title="", message='Exception: ' + str(e), corner_radius=4)
        return False


# insert table with the passed data
def insert_table(document, table_heading=None, table_items=[], table_props=None):
    style = document.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'

    if table_props is None:
        table_props = {
            "color": "#AAAAAA",
            "cell_alignment": [
                WD_ALIGN_PARAGRAPH.LEFT, 
                WD_ALIGN_PARAGRAPH.RIGHT
            ]
        }

    # add the table heading
    try:
        if table_heading is not None:
            insert_paragraph(
                paragraph=document.add_paragraph(),
                text=table_heading,
                bolded=True,
                italicized=False
            )
    except Exception as e:
        popup(title="", message=f'Exception when adding table heading: {table_heading}\n\n{e}', corner_radius=4)
        return False

    # add the table contents
    try:
        # Creating a table object
        table_obj = document.add_table(rows=len(table_items), cols=len(table_items[0]))

        # add rows
        for idx, row in enumerate(table_obj.rows):
            curr_row = row.cells
            row.height = CM(0.50)
            curr_row[0].text = table_items[idx]['label']
            curr_row[0].paragraphs[0].alignment = table_props['cell_alignment'][0]
            curr_row[1].text = table_items[idx]['info']
            curr_row[1].paragraphs[0].alignment = table_props['cell_alignment'][1]

        # set column widths and borders
        for idx, _ in enumerate(table_items[0]):
            for cell in (table_obj.columns[idx].cells):
                cell.width = CM(20)
                set_cell_border(cell, top={"sz": 1, "color": table_props['color'], "val": "single", "space": "4"})
                set_cell_border(cell, bottom={"sz": 1, "color": table_props['color'], "val": "single", "space": "0"})
    except Exception as e:
        popup(title="", message=f'Exception when adding table contents\n\n{e}', corner_radius=4)
        return False


# insert a new paragraph
def insert_paragraph(paragraph, text="", bolded=False, italicized=False):

    if bolded or italicized:
        runner = paragraph.add_run(text)
        runner.bold = bolded
        runner.italic = italicized

    else:
        new_p = OxmlElement("w:p")
        paragraph._p.addnext(new_p)
        paragraph.paragraph_format.space_before = PT(0)
        paragraph.paragraph_format.space_after = PT(0)
        new_para = Paragraph(new_p, paragraph._parent)
        new_para.add_run(text)
