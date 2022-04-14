import csv

def write_to_csv(filename, data):
    with open(filename, mode='w', encoding="utf-8") as employee_file:
        csv_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerows(data)