import os.path
from pesel import PESEL

def pesel(input_file_path):
    root, ext = os.path.splitext(input_file_path)
    output_file_path = root + "-birthdays" + ext

    invalid_list = []

    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        for line_number, pesel_line in enumerate(input_file, 1):
            pesel_line = pesel_line.rstrip()
            try:
                pesel = PESEL().from_string(pesel_line)
            except ValueError:
                invalid_list.append([line_number, pesel_line])
                continue

            processed_line = "{pesel} : {birthday}".format(**{
                "pesel": pesel_line,
                "birthday": pesel.to_date("%d-%m-%Y")
                })

            print(processed_line, file=output_file)

    retval = {
        "processed": line_number,
        "valid": line_number - len(invalid_list),
        "invalid": len(invalid_list),
        "invalid_list": invalid_list,
        }
    return retval
