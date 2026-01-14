# author: Ali Radwan, date : 21/12/2025

# This module implements the graphical interface of the spreadsheet application.
# It uses the Codeboot library to create HTML elements and handle events.
# The interface allows users to create, edit, save, and manipulate spreadsheets.
# The spreadsheet data is represented as a dictionary with header and data keys.
# The header is a list of column names, and 'data' is a list of rows, 
# where each row is a list of cell values. 

import spreadsheet
import codeboot
from functools import reduce

# Handles the event when a file is dropped onto the web page.
# It takes one parameter: the list of dropped files.
# It must load the first file in the list as a CSV spreadsheet.
def drop(files):
    global current_data
    if len(files) > 0:
        file = files[0]
        name = file.filename
        content = file.content
        current_data = spreadsheet.csvtxt_to_data(content)
        file_name = document.querySelector('#file-name')
        if file_name:
            file_name.textContent = name
        start()

current_data = None
selected_cell = None
current_group_col = None

# Starts the graphical interface, creates the HTML elements, and links event handlers
def init():
    global current_data

    # Install CSS and HTML into the cb-body element
    css = '<style>' + read_file('static/styles.css') + '</style>'
    html = read_file('index.html')
    document.querySelector('#cb-body').innerHTML = css + html

    current_data = spreadsheet.create_empty_data(20, 40)
    drop_file([])
    start()

def start():
    global current_data
     
    document.querySelector('#spreadsheet').innerHTML = ''

    tab_head = document.createElement('thead')
    header_row = document.createElement('tr')
    for i in range(len(current_data['header'])):
        th = document.createElement('th')
        th.textContent = current_data['header'][i]
        th.setAttribute('data-col', i)
        th.setAttribute('data-row', -1)
        th.addEventListener('click', lambda e, c=i: cell_clicked(-1, c))
        header_row.appendChild(th)

    tab_head.appendChild(header_row)
    document.querySelector('#spreadsheet').appendChild(tab_head)

    tab_body = document.createElement('tbody')
    data_rows = current_data['data']
    for r in range(len(data_rows)):
        row = document.createElement('tr')
        for c in range(len(data_rows[r])):
            cell_el = document.createElement('td')
            cell_el.setAttribute('data-row', r)
            cell_el.setAttribute('data-col', c)
            cell_el.textContent = data_rows[r][c]
            cell_el.addEventListener('click', lambda e, r=r, c=c: cell_clicked(r, c))
            row.appendChild(cell_el)
        tab_body.appendChild(row)
    document.querySelector('#spreadsheet').appendChild(tab_body)

def cell(row_idx, col_idx):
    selector = f'[data-row="{row_idx}"][data-col="{col_idx}"]'
    return document.querySelector(selector)

def cell_clicked(row_idx, col_idx): 
    global selected_cell, current_data

    if selected_cell is not None:
        selected_cell.classList.remove('selected')

    selected_cell = cell(row_idx, col_idx)
    selected_cell.classList.add('selected')

    coord_text = f"H{col_idx}" if row_idx == -1 else f"({row_idx}, {col_idx})"
    document.querySelector('#selected-cell').textContent = coord_text

    value = current_data['header'][col_idx] if row_idx == -1 else current_data['data'][row_idx][col_idx]
    document.querySelector('#cell-editor').value = value

def drop_file(files):
    codeboot.add_file_drop_handler(document.querySelector('body'), drop)
    if len(files) > 0:
        drop(files)

def cell_editor_pressed(event):
    global selected_cell, current_data
    if event.key == 'Enter' and selected_cell is not None:
        row_idx = int(selected_cell.getAttribute('data-row'))
        col_idx = int(selected_cell.getAttribute('data-col'))
        new_value = document.querySelector('#cell-editor').value
        if row_idx == -1:
            current_data['header'][col_idx] = new_value
        else:
            current_data['data'] = spreadsheet.update_cell(current_data['data'], row_idx, col_idx, new_value)
        selected_cell.textContent = new_value

def new_sheet_button_clicked():
    global current_data, selected_cell
    current_data = spreadsheet.create_empty_data(20, 40)
    selected_cell = None
    document.querySelector('#selected-cell').textContent = "(X,Y)"
    document.querySelector('#cell-editor').value = ""
    start()

def save_sheet_button_clicked():
    global current_data
    file_name = prompt("Enter the name of the file (with the .csv extension):")
    if not file_name:
        return
    if not (file_name.endswith('.csv')):
        alert("The file name must end with .csv")
        return
    data_to_save = current_data['data']
    if document.querySelector("#stats-row"):
        data_to_save = data_to_save[:-1]
    spreadsheet.save_data({'header': current_data['header'], 'data': data_to_save}, file_name)
    alert(f"Data saved : {file_name}")

def add_row_before_button_clicked():
    global current_data, selected_cell
    if selected_cell is not None:
        row_idx = int(selected_cell.getAttribute('data-row'))
        current_data['data'] = spreadsheet.create_new_row(current_data['data'], row_idx)
        selected_cell = None
        document.querySelector('#selected-cell').textContent = "(X,Y)"
        document.querySelector('#cell-editor').value = ""
        start()

def add_row_after_button_clicked():
    global current_data, selected_cell
    if selected_cell is not None:
        row_idx = int(selected_cell.getAttribute('data-row'))
        current_data['data'] = spreadsheet.create_new_row(current_data['data'], row_idx + 1)
        selected_cell = None
        document.querySelector('#selected-cell').textContent = "(X,Y)"
        document.querySelector('#cell-editor').value = ""
        start()

def add_column_before_button_clicked():
    global current_data, selected_cell
    if selected_cell is not None:
        col_idx = int(selected_cell.getAttribute('data-col'))
        current_data['header'] = spreadsheet.create_new_header_column(current_data['header'], col_idx)
        current_data['data'] = spreadsheet.create_new_column(current_data['data'], col_idx)
        selected_cell = None
        document.querySelector('#selected-cell').textContent = "(X,Y)"
        document.querySelector('#cell-editor').value = ""
        start()

def add_column_after_button_clicked():
    global current_data, selected_cell
    if selected_cell is not None:
        col_idx = int(selected_cell.getAttribute('data-col'))
        current_data['header'] = spreadsheet.create_new_header_column(current_data['header'], col_idx + 1)
        current_data['data'] = spreadsheet.create_new_column(current_data['data'], col_idx + 1)
        selected_cell = None
        document.querySelector('#selected-cell').textContent = "(X,Y)"
        document.querySelector('#cell-editor').value = ""
        start()

def delete_row_button_clicked():
    global current_data, selected_cell
    if selected_cell is not None:
        row_idx = int(selected_cell.getAttribute('data-row'))
        current_data['data'] = spreadsheet.delete_row(current_data['data'], row_idx)
        selected_cell = None
        document.querySelector('#selected-cell').textContent = "(X,Y)"
        document.querySelector('#cell-editor').value = ""
        start()

def delete_column_button_clicked():
    global current_data, selected_cell
    if selected_cell is not None:
        col_idx = int(selected_cell.getAttribute('data-col'))
        current_data['header'] = spreadsheet.delete_header_column(current_data['header'], col_idx)
        current_data['data'] = spreadsheet.delete_column(current_data['data'], col_idx)
        selected_cell = None
        document.querySelector('#selected-cell').textContent = "(X,Y)"
        document.querySelector('#cell-editor').value = ""
        start()

def sum_button_clicked():
    global current_data
    sums_row = []
    num_columns = len(current_data['header'])
    for col_idx in range(num_columns):
        result = spreadsheet.get_sum(current_data['data'], col_idx)
        sums_row.append(str(result) if result is not None else "NaN")

    if document.querySelector("#stats-row"):
        document.querySelector("#stats-row").remove()

    tr = document.createElement('tr')
    tr.id = "stats-row"
    tr.classList.add('stats')
    for value in sums_row:
        td = document.createElement('td')
        td.textContent = value
        tr.appendChild(td)
    document.querySelector('#spreadsheet tbody').appendChild(tr)
    document.querySelector('#clear-stats-button').disabled = False

def clear_stats_button_clicked():
    if document.querySelector("#stats-row"):
        document.querySelector("#stats-row").remove()
    document.querySelector('#clear-stats-button').disabled = True

def group_by_button_clicked():
    global current_data, selected_cell, current_group_col
    if selected_cell is None:
        return   
    col_idx = int(selected_cell.getAttribute('data-col'))
    if current_group_col == col_idx:
        current_group_col = None
        start()
        return
    current_group_col = col_idx
    groups = spreadsheet.get_group_by(current_data['data'], col_idx)
    document.querySelector('#spreadsheet tbody').innerHTML = ''
    for group_val, group_sum in groups:
        tr_head = document.createElement('tr')
        tr_head.classList.add('group-header')        
        td_head = document.createElement('td')
        td_head.textContent = f"Group: {group_val} (Sum: {group_sum})"
        td_head.setAttribute('colspan', str(len(current_data['header'])))
        tr_head.appendChild(td_head)
        document.querySelector('#spreadsheet tbody').appendChild(tr_head)
        for row in current_data['data']:
            if row[col_idx] == group_val:
                tr = document.createElement('tr')
                for cell_val in row:
                    td = document.createElement('td')
                    td.textContent = cell_val
                    tr.appendChild(td)
                document.querySelector('#spreadsheet tbody').appendChild(tr)

# Testing functions
def test_new_sheet_button_clicked():
    global current_data, selected_cell
    current_data = {'header': ['Test'], 'data': [['Val']]}
    selected_cell = "simulate_element"
    new_sheet_button_clicked()
    assert len(current_data['header']) == 20
    assert len(current_data['data']) == 40
    assert selected_cell is None
    assert document.querySelector('#selected-cell').textContent == "(X,Y)"

def test_cell_clicked():
    global selected_cell, current_data
    current_data = {'header': ['Col1'], 'data': [['Hello']]}
    cell_clicked(0, 0)
    assert document.querySelector('#cell-editor').value == 'Hello'
    assert "(0, 0)" in document.querySelector('#selected-cell').textContent

def test_delete_row_button_clicked():
    global current_data, selected_cell
    current_data = {'header': ['A'], 'data': [['Row0'], ['Row1'], ['Row2']]}
    mock_cell = document.createElement('td')
    mock_cell.setAttribute('data-row', '1')
    selected_cell = mock_cell
    delete_row_button_clicked()
    assert len(current_data['data']) == 2
    assert current_data['data'][1] == ['Row2']
    assert selected_cell is None

def test_sum_button_clicked():
    global current_data
    current_data = {'header': ['Nombres'], 'data': [['10'], ['20.5'], ['abc']]}
    sum_button_clicked()
    stats_row = document.querySelector("#stats-row")
    assert stats_row is not None
    assert "30.5" in stats_row.textContent

if __name__ == "__main__":
    test_new_sheet_button_clicked()
    test_cell_clicked()
    test_delete_row_button_clicked()
    test_sum_button_clicked()     

init()
