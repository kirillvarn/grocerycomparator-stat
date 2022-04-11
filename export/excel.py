from openpyxl import Workbook


def save(data, filename="sample", header=[]):
    wb = Workbook()
    ws = wb.active

    if len(header) != 0:
        ws.append(header)

    for i in data:
        ws.append(i)

    wb.save(f"{filename}.xlsx")
