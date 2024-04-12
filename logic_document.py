import os
import datetime
import variables as vars
from docx import Document
from docx.shared import Cm as CM
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

    form_data['[HOST1_NAME]'] = vars.host1_fields['host1_name'].get()
    form_data['[HOST1_BIRTH]'] = vars.host1_fields['host1_birth'].get()
    form_data['[HOST1_STATUS]'] = vars.host1_fields['host1_status'].get()
    form_data['[HOST1_PASSPORT]'] = vars.host1_fields['host1_passport'].get()
    form_data['[HOST1_ADDRESS]'] = vars.host1_fields['host1_address'].get()
    form_data['[HOST1_PHONE]'] = vars.host1_fields['host1_phone'].get()
    form_data['[HOST1_OCCUPATION]'] = vars.host1_fields['host1_occupation'].get()
    form_data['[HOST1_EMAIL]'] = vars.host1_fields['host1_email'].get()
    form_data['[HOST1_RELATION_TO_HOST2]'] = vars.host1_fields['host1_relation_to_host2'].get()

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
    form_data['[GUEST_RELATIONSHIP]'] = vars.guest_fields['guest_relationship'].get()
    form_data['[GUEST_CANADIAN_ADDRESS]'] = vars.guest_fields['guest_canadian_address'].get()

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

        write_table(doc, [])

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


# itemized table
def write_table(document, data):

    style = document.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'

    # Table data in a form of list
    table_items = [
        {"label": "", "data": "", "width": 20.0},
    ]

    # Creating a table object
    table_obj = document.add_table(rows=1, cols=len(table_items))

    # add heading in the 1st row of the table
    row = table_obj.rows[0].cells
    for idx, col in enumerate(table_items):
        row[idx].text = col["heading"]

    # # add data from the list to the table
    # for index, entry in enumerate(data):

    #     # Adding a row and then adding data in it.
    #     row = table_obj.add_row().cells

    #     row[0].text = str(index + 1)
    #     row[1].text = str(entry["desc"])
    #     row[2].text = str(entry["qty"])
    #     row[3].text = str(entry["rate"])
    #     row[4].text = str(int(entry["qty"]) * float(entry["rate"]))

    # set the table borders
    for cell in table_obj.rows[0].cells:
        set_cell_border(cell, bottom={"sz": 6, "color": "#AAAAAA", "val": "single", "space": "10"})
        set_cell_border(cell, top={"sz": 6, "color": "#AAAAAA", "val": "single", "space": "15"})

    # set column widths
    for idx, col in enumerate(table_items):
        for index, cell in enumerate(table_obj.columns[idx].cells):
            cell.width = CM(col["width"])

            if index > 0:
                set_cell_border(cell, bottom={"sz": 6, "color": "#DDDDDD", "val": "single", "space": "15"},)

        set_cell_border(cell, bottom={"sz": 6, "color": "#AAAAAA", "val": "single", "space": "0"})

    # set row heights
    for index, row in enumerate(table_obj.rows):
        row.height = CM(1)

    # make_rows_bold(table_obj.rows[0])


# table containing taxes and total
def write_totals_table(document): 
    total_table = document.add_table(rows=1, cols=5)

    gst = vars.form['gst_display_amount'].cget("text")
    pst = vars.form['pst_display_amount'].cget("text")
    total = vars.form['total_display_amount'].cget("text")

    total_table_data = [
        [str("GST @5%"), "", "", "", gst],
        [str("PST @7%"), "", "", "", pst],
        [str("TOTAL"), "", "", "", total],
    ]

    for total_row in total_table_data:
        row = total_table.add_row().cells

        for idx, col in enumerate(total_row):
            row[idx].text = col

        make_rows_bold(total_table.rows[-1])

