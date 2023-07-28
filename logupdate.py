log_file_path = 'status_info.log'
def delete_row_from_log_file(row_to_delete):
    # Read the entire content of the log file
    with open(log_file_path, 'r') as log_file:
        lines = log_file.readlines()

    # Find the index of the row to delete
    index_to_delete = None
    for i, line in enumerate(lines):
        if row_to_delete in line:
            index_to_delete = i
            break

    # If the row is found, remove it from the content
    if index_to_delete is not None:
        del lines[index_to_delete]

        # Write the modified content back to the log file without blank lines
        with open(log_file_path, 'w') as log_file:
            log_file.writelines(line for line in lines if line.strip())

        print("Row deleted successfully.")
    
    with open(log_file_path, 'a') as log_file:
        log_file.write('\n')


def findlocation(location):
    with open(log_file_path, 'r') as log_file:
        for row in log_file:
            print(row)
            elements = row.split(" ")
            print(elements[0])
            if(elements[0]==location):
                return True,row
    return False,row
            