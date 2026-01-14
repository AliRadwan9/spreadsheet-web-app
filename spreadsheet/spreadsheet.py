# author: Ali Radwan, date : 21/12/2025

# This module contains functions for manipulating a simple spreadsheet data structure.
# The spreadsheet data structure consists of a header row and a table of data rows.
# Each row is represented as an array of strings, where each string corresponds to a cell in
# that row. The header row contains the names of the columns, and the data rows contain the actual data.
# The module provides functions for creating, modifying, and querying the spreadsheet data structure.
# It also includes functions for reading from and writing to CSV files. 


from functools import reduce
# fonctions imported:

def split_lines(content):
    lines = content.split('\n')
    if lines[-1] == '': lines.pop()

    return lines
def write_csv(path, content):
    write_file(path, '\n'.join(map(lambda row: ','.join(row), content)))

def sums(values):
    return reduce(lambda x, y: x+y, values, 0)


# a function that saves the data structure representing the spreadsheet to a CSV file.
# it takes two parameters data and file_path. data is the data structure representing
# the spreadsheet and file_path is the path of the CSV file where the data should be saved

def save_data(data, file_path):
    header = data['header']
    data_rows = data['data']
    csv_content = [header]
    for row in data_rows:
        csv_content.append(row)
    write_csv(file_path, csv_content)

# a function that converts CSV text to data structure that represents the spreadsheet.
# it takes a single parameter csvtext which is the content of a CSV file as text.

def csvtxt_to_data(csvtext):
    lines = split_lines(csvtext)
    if not lines:
        return {'header': [], 'data': []}
    lines_cut = []
    for line in lines:
        lines_cut.append(line.split(','))
    header = lines_cut[0] 
    data = lines_cut[1:] 
    return {'header': header, 'data': data}

# Creates and returns a header row for the spreadsheet.
# It takes a single parameter num_cols which is the number of columns.
# It contains num_cols column names of the form Column x
# where x starts at 1 for the first column.

def create_empty_data_header(num_cols):
    header = []
    for i in range(num_cols):
        header.append("Column " + str(i + 1))
    return header

# a function that creates an empty data structure for the spreadsheet.
# its made of an array of arrays representing the cells.it takes two parameters 
# num_cols and num_rows which are the number of columns and number of rows respectively. 

def create_empty_data(num_cols, num_rows):
    header = create_empty_data_header(num_cols)
    data = []
    for r in range(num_rows):
        row = []
        for c in range(num_cols):
            row.append('')
        data.append(row)
    return {'header': header, 'data': data}

# Creates and returns a new header row by inserting a new column name
# at position 'col_idx'. The name of the new column is "Column x"
# where x is the correct column number for the inserted position.

def create_new_header_column(header, col_idx):
    new_header = list(header)
    new_header.insert(col_idx, "column" + str(col_idx + 1))
    return new_header

# Creates and returns a new table by inserting a new empty column
# at position 'col_idx' in each row of the table 'data'.
# All cells in the new column are initialized with empty strings.

def create_new_column(data, col_idx):
    new_data = []
    for row in data:
        new_row = row[:col_idx] + [''] + row[col_idx:]
        new_data.append(new_row)
    return new_data

# Creates and returns a new table by inserting a new empty row
# at position 'row_idx'. The row contains as many empty cells
# as there are columns in the table.

def create_new_row(data, row_idx):
    if data:
        num_cols = len(data[0])
    else:
        num_cols = 0
    new_row = []
    for i in range(num_cols):
        new_row.append('')
    return data[:row_idx] + [new_row] + data[row_idx:]

# Creates and returns a new header row by removing the column name
# at position 'col_idx' from the header.

def delete_header_column(header, col_idx):
    if not (0 <= col_idx < len(header)): return header
    new_header = list(header)
    new_header.pop(col_idx)  

    return new_header

# Creates and returns a new table by removing the column at position 'col_idx'
# from every row of the table 'data'.

def delete_column(data, col_idx):
    new_data = []
    for row in data:
        new_row = row[:col_idx] + row[col_idx + 1:]
        new_data.append(new_row)
    return new_data

# Creates and returns a new table by removing the row at position 'row_idx'
# from the table 'data'. it takes two parameters data and row_idx which are the index
# of the row to be deleted and the table data itself.
 
def delete_row(data, row_idx):
    return data[:row_idx] + data[row_idx + 1:]

# Creates and returns a new table where the cell located at (row_idx, col_idx)
# is replaced with 'new_value'. All other cells remain unchanged.

def update_cell(data, row_idx, col_idx, new_value):
    new_data = []
    for i in range(len(data)):
        current_row = list(data[i])
        if i == row_idx and 0 <= col_idx < len(current_row):
            current_row[col_idx] = new_value
        new_data.append(current_row)          
    return new_data    

# checks if the string s represents a valid number (integer or decimal).
# it returns True if s is a valid number, False otherwise.

def valid_number(s):
    if not s: return False
    s_t = s
    if s_t[0] == '-': s_t = s_t[1:]
    if s_t.count('.') > 1: return False
    s_t = s_t.replace('.', '')  
    return s_t.isdigit()

# returns the sum of all numeric values in column 'col_idx'.
# If the column contains no numeric values, the function returns None.

def get_sum(data, col_idx):
    if not data or not (0 <= col_idx < len(data[0])): return None 
    nums = []
    for row in data:
        val = row[col_idx]
        if valid_number(val):
            nums.append(float(val))
    return sums(nums) if nums else None

# Groups the rows of the table based on the values in column 'col_idx'.
# Returns a list of groups, where each group is a list of rows
# that all share the same value in that column.

def get_group_by(data, col_idx):

    if not data or not (0 <= col_idx < len(data[0])): return []
    target_col = 1 if col_idx == 0 else 0
    sorted_rows = []

    for r in data:
        sorted_rows.append([r[col_idx]] + r)
    sorted_rows.sort()

    res = []
    curr_val = None
    curr_nums = []

    for row in sorted_rows:

        if row[0] != curr_val:
            if curr_val is not None:
                numeric = []

                for v in curr_nums:
                    if valid_number(v): numeric.append(float(v))
                res.append((curr_val, sums(numeric) if numeric else 0.0))

            curr_val = row[0]
            curr_nums = []
        curr_nums.append(row[target_col + 1])

    if curr_val is not None:
        numeric = []

        for v in curr_nums:
            if valid_number(v): numeric.append(float(v))
        res.append((curr_val, sums(numeric) if numeric else 0.0))
    return res

# helper function to copy data for testing purposes
# it creates and returns a  copy of the given  array 'data'.

def copy_data(data):
    new_data = []
    for row in data:
        new_row = []
        for cell in row:
            new_row.append(cell)
        new_data.append(new_row)
    return new_data

def test_delete_header_column():
    h = ['Column 1', 'Column 2']
    assert delete_header_column(h, 0) == ['Column 1']
   

def test_save_data():
    data = {
        'header': ['head1', 'head2', 'head3'],
        'data': [['dat1', 'dat2', 'dat3'], ['dat4', 'dat5', 'dat6']]
    }
    file_path = 'test_output.csv'
    save_data(data, file_path)
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    correct_content = "head1,head2,head3\ndat1,dat2,dat3\ndat4,dat5,dat6\n"
    assert content == correct_content

def test_csvtxt_to_data():
    csvtext = "head1,head2,head3\ndat1,dat2,dat3\ndat4,dat5,dat6"
    data = csvtxt_to_data(csvtext)
    assert data['header'] == ['head1', 'head2', 'head3']
    assert data['data'] == [['dat1', 'dat2', 'dat3'], ['dat4', 'dat5', 'dat6']]

    csvtext_empty = ""
    data_empty = csvtxt_to_data(csvtext_empty)
    assert data_empty['header'] == []
    assert data_empty['data'] == []
    csvtext_header = "head1,head2,head3"

    data_header = csvtxt_to_data(csvtext_header)
    assert data_header['header'] == ['head1', 'head2', 'head3']
    assert data_header['data'] == []

def test_create_empty_data_header():
    assert create_empty_data_header(4) == ['Column 1', 'Column 2', 'Column 3', 'Column 4']
    
    assert create_empty_data_header(1) == ['Column 1']

    assert create_empty_data_header(0) == []

def test_create_empty_data():
    data = create_empty_data(3, 2)
    assert data['header'] == ['', '', '']
    assert data['data'] == [['', '', ''], ['', '', '']]
    data_empty = create_empty_data(0, 0)
    assert data_empty['header'] == []
    assert data_empty['data'] == []


def test_create_new_header_column():
    header = ['Column 1', 'Column 2', 'Column 3']

    expected_mid = ['Column 1', 'Column 2', 'Column 3', 'Column 4']
    assert create_new_header_column(header, 1) == expected_mid
    
    expected_start = ['Column 1', 'Column 2', 'Column 3', 'Column 4']
    assert create_new_header_column(header, 0) == expected_start
    
    expected_end = ['Column 1', 'Column 2', 'Column 3', 'Column 4']
    assert create_new_header_column(header, 3) == expected_end

def test_create_new_column():
    test_data = [['A1', 'B1', 'C1'], ['A2', 'B2', 'C2']]

    expected_mid = [['A1', '', 'B1', 'C1'], ['A2', '', 'B2', 'C2']]
    assert create_new_column(test_data, 1) == expected_mid

    expected_end = [['A1', 'B1', 'C1', ''], ['A2', 'B2', 'C2', '']]
    assert create_new_column(test_data, 3) == expected_end
    
    expected_start = [['', 'A1', 'B1', 'C1'], ['', 'A2', 'B2', 'C2']]
    assert create_new_column(test_data, 0) == expected_start
    
def test_create_new_row():
    test_data = [['A1', 'B1'], ['A2', 'B2']]
    
    expected_mid = [['A1', 'B1'], ['', ''], ['A2', 'B2']]
    assert create_new_row(test_data, 1) == expected_mid
    
    expected_start = [['', ''], ['A1', 'B1'], ['A2', 'B2']]
    assert create_new_row(test_data, 0) == expected_start

    assert create_new_row([], 0) == []
    
def test_delete_column():
    data = [['A', '10'], ['B', '20']]
    assert delete_column(copy_data(data), 0) == [['10'], ['20']]

def test_delete_row():
    data = [['A'], ['B']]
    assert delete_row(copy_data(data), 0) == [['B']]
    
def test_update_cell():
    data = [['A']]
    assert update_cell(copy_data(data), 0, 0, 'B') == [['B']]
    
def test_get_sum():
    data = [['10'], ['20']]
    assert get_sum(data, 0) == 30.0
    
def test_get_group_by():
    data = [['X', '10'], ['X', '5']]
    res = get_group_by(data, 0)
    assert res[0] == ('X', 15.0)

if __name__ == "__main__":
    test_save_data() 
    test_csvtxt_to_data() 
    test_create_empty_data_header()
    test_create_empty_data()
    test_create_new_header_column()
    test_create_new_column()
    test_create_new_row()
    test_delete_header_column()
    test_delete_column()
    test_delete_row()
    test_update_cell()
    test_get_sum()
    test_get_group_by()
