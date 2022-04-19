import csv

def write_to_csv(filename, data):
    with open(filename, mode='w', encoding="utf-8") as file:
        csv_writer = csv.writer(file, delimiter=',')

        for row in data:
            csv_writer.writerow(row)